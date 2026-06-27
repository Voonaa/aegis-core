"""Unit tests for SQLite TelemetryRepository isolated DB layer."""

import pytest
import sqlite3
import time
from pathlib import Path
from packages.core.repositories.telemetry_repository import TelemetryRepository


@pytest.fixture
def repo(tmp_path: Path) -> TelemetryRepository:
    """Returns a TelemetryRepository mapped to a temp file database."""
    db_file = tmp_path / "test_repo.db"
    return TelemetryRepository(db_path=db_file)


def test_schema_created_successfully(repo: TelemetryRepository) -> None:
    """Repository must initialize SQLite database file and indices."""
    assert repo.db_path.exists()
    
    conn = sqlite3.connect(str(repo.db_path))
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='telemetry_logs'")
        tables = [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()
        
    assert "telemetry_logs" in tables


def test_save_inserts_record(repo: TelemetryRepository) -> None:
    """save() must successfully write row dict data to SQLite."""
    record = {
        "timestamp": time.time(),
        "cpu_utilization": 30.5,
        "cpu_temperature": 55.0,
        "ram_percentage": 0.45,
        "disk_health_percent": 99,
        "battery_health_percent": 100,
        "network_latency_ms": 12.0,
        "health_score": 98,
        "active_power_plan": "Performance"
    }
    
    repo.save(record)
    logs = repo.fetch_range(start_time=time.time() - 3600)
    
    assert len(logs) == 1
    assert logs[0]["cpu_utilization"] == 30.5
    assert logs[0]["active_power_plan"] == "Performance"


def test_delete_older_than_purges_rows(repo: TelemetryRepository) -> None:
    """delete_older_than() must purge stale rows and return rowcount deleted."""
    # Seed old record
    old_record = {
        "timestamp": time.time() - 10000,
        "cpu_utilization": 80.0,
        "cpu_temperature": 75.0,
        "ram_percentage": 0.9,
        "disk_health_percent": 80,
        "battery_health_percent": 75,
        "network_latency_ms": 20.0,
        "health_score": 50,
        "active_power_plan": "Balanced"
    }
    # Seed new record
    new_record = dict(old_record)
    new_record["timestamp"] = time.time()
    new_record["cpu_utilization"] = 10.0
    
    repo.save(old_record)
    repo.save(new_record)
    
    deleted = repo.delete_older_than(cutoff_time=time.time() - 5000)
    
    assert deleted == 1
    remaining = repo.fetch_range(start_time=time.time() - 3600)
    assert len(remaining) == 1
    assert remaining[0]["cpu_utilization"] == 10.0
