"""SQLite-based telemetry history service recording system usage parameters and rolling policy."""

import sqlite3
import time
from pathlib import Path
from typing import Optional
from packages.core.container import ServiceContainer
from packages.core.models.telemetry import TelemetryReport
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class TelemetryHistoryService:
    """Manages local SQLite telemetry log stores and history queries."""

    def __init__(self, container: ServiceContainer, db_path: Optional[Path] = None) -> None:
        """Initialize the Telemetry History Service.
        
        Args:
            container: DI Service container reference.
            db_path: Optional override path for the database file.
        """
        self.container = container
        
        if db_path is None:
            # Standard location under apps/desktop/config/
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            self.db_path = project_root / "apps" / "desktop" / "config" / "telemetry_history.db"
        else:
            self.db_path = db_path
            
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        logger.info(f"Telemetry History database initialized at: {self.db_path}")

    def _init_db(self) -> None:
        """Initializes database schema and indexes."""
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

    def log_telemetry(self, report: TelemetryReport) -> None:
        """Saves a new snapshot record of the TelemetryReport to SQLite.
        
        Args:
            report: The active TelemetryReport to parse and store.
        """
        conn = None
        try:
            # Query active power plan via OptimizationService if available
            power_plan = "Balanced"
            try:
                opt_svc = self.container.get("optimization_service")
                state = opt_svc.capture_current_state()
                power_plan = state.get("power_plan", "Balanced")
            except Exception:
                pass

            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO telemetry_logs (
                    timestamp, cpu_utilization, cpu_temperature, ram_percentage,
                    disk_health_percent, battery_health_percent, network_latency_ms,
                    health_score, active_power_plan
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                time.time(),
                report.cpu.utilization,
                report.cpu.temperature,
                report.ram.percentage,
                report.disk.health_percent,
                report.battery.health_percent,
                report.network_latency_ms,
                report.health_score,
                power_plan
            ))
            conn.commit()
            logger.debug("Telemetry record written to SQLite.")
        except Exception as ex:
            logger.error(f"Failed to write telemetry log to SQLite: {ex}")
        finally:
            if conn:
                conn.close()

    def get_history(self, limit_hours: int = 168) -> list[dict]:
        """Queries telemetry logs for the last N hours.
        
        Args:
            limit_hours: Hours range. Default is 168 (7 days).
            
        Returns:
            List of telemetry records formatted as dictionaries.
        """
        records = []
        cutoff_time = time.time() - (limit_hours * 3600)
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM telemetry_logs 
                WHERE timestamp >= ? 
                ORDER BY timestamp ASC
            """, (cutoff_time,))
            for row in cursor.fetchall():
                records.append(dict(row))
        except Exception as ex:
            logger.error(f"Failed to query telemetry logs history: {ex}")
        finally:
            if conn:
                conn.close()
        return records

    def clean_old_records(self, days: int = 7) -> int:
        """Deletes telemetry log rows older than N days to prevent database bloating.
        
        Args:
            days: Max age threshold. Default is 7 days.
            
        Returns:
            Number of deleted records.
        """
        cutoff_time = time.time() - (days * 24 * 3600)
        deleted = 0
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("DELETE FROM telemetry_logs WHERE timestamp < ?", (cutoff_time,))
            deleted = cursor.rowcount
            conn.commit()
            if deleted > 0:
                logger.info(f"Cleaned up {deleted} stale telemetry logs older than {days} days.")
        except Exception as ex:
            logger.error(f"Failed to execute rolling telemetry database cleanup: {ex}")
        finally:
            if conn:
                conn.close()
        return deleted
