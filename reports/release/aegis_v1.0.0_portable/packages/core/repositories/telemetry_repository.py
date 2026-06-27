"""TelemetryRepository handling SQLite database connection operations, schemas, writes, and cleanups."""

import sqlite3
from pathlib import Path
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class TelemetryRepository:
    """Manages raw SQL query execution, inserts, and rolling deletions in SQLite telemetry database."""

    def __init__(self, db_path: Path) -> None:
        """Initialize the Telemetry Repository.
        
        Args:
            db_path: Path to target SQLite database file.
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """Configures schema tables and database indices."""
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    cpu_utilization REAL,
                    cpu_temperature REAL,
                    ram_percentage REAL,
                    disk_health_percent INTEGER,
                    battery_health_percent INTEGER,
                    network_latency_ms REAL,
                    health_score INTEGER,
                    active_power_plan TEXT
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_telemetry_logs_timestamp 
                ON telemetry_logs(timestamp)
            """)
            conn.commit()
        except Exception as ex:
            logger.error(f"Failed to initialize SQLite telemetry database: {ex}", exc_info=True)
        finally:
            if conn:
                conn.close()

    def save(self, record: dict) -> None:
        """Inserts a new telemetry log row.
        
        Args:
            record: Data dictionary mapping column fields to database rows.
        """
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO telemetry_logs (
                    timestamp, cpu_utilization, cpu_temperature, ram_percentage,
                    disk_health_percent, battery_health_percent, network_latency_ms,
                    health_score, active_power_plan
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record["timestamp"],
                record["cpu_utilization"],
                record["cpu_temperature"],
                record["ram_percentage"],
                record["disk_health_percent"],
                record["battery_health_percent"],
                record["network_latency_ms"],
                record["health_score"],
                record["active_power_plan"]
            ))
            conn.commit()
        except Exception as ex:
            logger.error(f"Failed to save telemetry log to SQLite: {ex}")
        finally:
            if conn:
                conn.close()

    def fetch_range(self, start_time: float) -> list[dict]:
        """Queries telemetry log rows from start_time ordered by timestamp.
        
        Args:
            start_time: Cutoff timestamp filter.
            
        Returns:
            List of telemetry records formatted as dictionaries.
        """
        records = []
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM telemetry_logs 
                WHERE timestamp >= ? 
                ORDER BY timestamp ASC
            """, (start_time,))
            for row in cursor.fetchall():
                records.append(dict(row))
        except Exception as ex:
            logger.error(f"Failed to fetch telemetry history range: {ex}")
        finally:
            if conn:
                conn.close()
        return records

    def delete_older_than(self, cutoff_time: float) -> int:
        """Deletes rows older than cutoff_time to control database size.
        
        Args:
            cutoff_time: Cutoff timestamp filter.
            
        Returns:
            Number of deleted logs.
        """
        deleted = 0
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("DELETE FROM telemetry_logs WHERE timestamp < ?", (cutoff_time,))
            deleted = cursor.rowcount
            conn.commit()
        except Exception as ex:
            logger.error(f"Failed to purge stale telemetry logs: {ex}")
        finally:
            if conn:
                conn.close()
        return deleted
