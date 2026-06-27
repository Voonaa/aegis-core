"""Unit tests for SQLite TelemetryHistoryService and ExportService."""

import json
import pytest
import sqlite3
import time
from pathlib import Path
from unittest.mock import MagicMock
from packages.core.container import ServiceContainer
from packages.core.config_manager import ConfigManager
from packages.core.services.telemetry_history_service import TelemetryHistoryService
from packages.core.services.export_service import ExportService
from packages.core.models.telemetry import TelemetryReport, CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    """Reset ServiceContainer singleton between tests."""
    ServiceContainer._instance = None
    yield
    ServiceContainer._instance = None


@pytest.fixture
def container(tmp_path: Path) -> ServiceContainer:
    """Returns a minimal ServiceContainer with config registered."""
    c = ServiceContainer()
    config_file = tmp_path / "settings.json"
    config_mgr = ConfigManager(config_path=config_file, default_settings={"demo_mode": True})
    c.register("config", config_mgr)
    return c


@pytest.fixture
def history_svc(container: ServiceContainer, tmp_path: Path) -> TelemetryHistoryService:
    """Returns a TelemetryHistoryService running on a temporary SQLite DB path."""
    db_file = tmp_path / "telemetry_test.db"
    return TelemetryHistoryService(container=container, db_path=db_file)


@pytest.fixture
def export_svc(tmp_path: Path) -> ExportService:
    """Returns an ExportService mapping exports to a temporary directory."""
    service = ExportService()
    service.diagnostics_dir = tmp_path
    return service


def test_db_initialization_and_schema(history_svc: TelemetryHistoryService) -> None:
    """SQLite database schema tables and columns must initialize correctly."""
    assert history_svc.db_path.exists()
    
    conn = sqlite3.connect(str(history_svc.db_path))
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(telemetry_logs)")
        cols = [col[1] for col in cursor.fetchall()]
    finally:
        conn.close()
        
    assert "id" in cols
    assert "cpu_utilization" in cols
    assert "cpu_temperature" in cols
    assert "active_power_plan" in cols


def test_log_telemetry_insertion(history_svc: TelemetryHistoryService) -> None:
    """log_telemetry must successfully record TelemetryReport data to SQLite table."""
    report = TelemetryReport(
        cpu=CPUInfo(10.0, 45.0, "i7", 2.5, 1.0, 12.0),
        ram=RAMInfo(4.0, 8.0, 0.5),
        disk=DiskInfo(50.0, 256.0, 0.1, 95, "OK", 30.0, 500, 200.0),
        battery=BatteryInfo(90, True, 95, -1, 4000, 3800, 20),
        os=OSInfo("Win11", "22621", False, False),
        health_score=95,
        gpu_model="Intel HD",
        gpu_utilization=5.0,
        gpu_temperature=40.0,
        network_adapter="Wi-Fi",
        ip_address="192.168.1.5",
        network_latency_ms=10.0
    )

    history_svc.log_telemetry(report)
    logs = history_svc.get_history(limit_hours=1)

    assert len(logs) == 1
    assert logs[0]["cpu_utilization"] == 10.0
    assert logs[0]["health_score"] == 95
    assert logs[0]["active_power_plan"] == "Balanced"


def test_rolling_cleanup_rules(history_svc: TelemetryHistoryService) -> None:
    """clean_old_records must remove logs older than target days threshold."""
    # Seed db directly with one new and one very old record
    conn = sqlite3.connect(str(history_svc.db_path))
    try:
        cursor = conn.cursor()
        # insert old record (10 days ago)
        old_time = time.time() - (10 * 24 * 3600)
        cursor.execute("""
            INSERT INTO telemetry_logs (timestamp, cpu_utilization, health_score) 
            VALUES (?, ?, ?)
        """, (old_time, 90.0, 100))
        # insert new record
        cursor.execute("""
            INSERT INTO telemetry_logs (timestamp, cpu_utilization, health_score) 
            VALUES (?, ?, ?)
        """, (time.time(), 15.0, 95))
        conn.commit()
    finally:
        conn.close()

    deleted = history_svc.clean_old_records(days=7)

    assert deleted == 1
    remaining = history_svc.get_history(limit_hours=240)
    assert len(remaining) == 1
    assert remaining[0]["cpu_utilization"] == 15.0


def test_export_formats_creation(export_svc: ExportService) -> None:
    """ExportService must format data dicts and write clean output CSV, JSON, MD, HTML files."""
    data = [
        {
            "id": 1,
            "timestamp": time.time(),
            "cpu_utilization": 25.0,
            "cpu_temperature": 50.0,
            "ram_percentage": 0.4,
            "disk_health_percent": 98,
            "battery_health_percent": 95,
            "network_latency_ms": 15.0,
            "health_score": 90,
            "active_power_plan": "Performance"
        }
    ]

    csv_path = export_svc.export_to_csv(data)
    json_path = export_svc.export_to_json(data)
    md_path = export_svc.export_to_markdown(data)
    html_path = export_svc.export_to_html(data)

    assert csv_path.exists()
    assert json_path.exists()
    assert md_path.exists()
    assert html_path.exists()

    # Verify JSON structure parsing
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    assert json_data[0]["cpu_utilization"] == 25.0
    assert json_data[0]["active_power_plan"] == "Performance"
