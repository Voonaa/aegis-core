"""Unit tests for the telemetry data model dataclasses."""

import pytest
from packages.core.models.telemetry import (
    CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo, TelemetryReport
)


def _make_cpu(**kwargs: object) -> CPUInfo:
    defaults = dict(utilization=25.0, temperature=55.0, model_name="Test CPU",
                    frequency_ghz=3.5, voltage=1.2, power_draw_watts=20.0)
    defaults.update(kwargs)
    return CPUInfo(**defaults)  # type: ignore[arg-type]


def _make_ram(**kwargs: object) -> RAMInfo:
    defaults = dict(used_gb=8.0, total_gb=16.0, percentage=0.5)
    defaults.update(kwargs)
    return RAMInfo(**defaults)  # type: ignore[arg-type]


def _make_disk(**kwargs: object) -> DiskInfo:
    defaults = dict(used_gb=100.0, total_gb=512.0, percentage=0.2,
                    health_percent=95, status="OK", temperature=35.0,
                    power_on_hours=2000, host_writes_gb=600.0)
    defaults.update(kwargs)
    return DiskInfo(**defaults)  # type: ignore[arg-type]


def _make_battery(**kwargs: object) -> BatteryInfo:
    defaults = dict(percentage=80, is_charging=False, health_percent=90,
                    time_remaining_mins=120, design_capacity_mwh=50000,
                    current_capacity_mwh=45000, cycle_count=200)
    defaults.update(kwargs)
    return BatteryInfo(**defaults)  # type: ignore[arg-type]


def _make_os(**kwargs: object) -> OSInfo:
    defaults = dict(os_name="Windows 11", build_version="22H2",
                    hyperv_active=False, virtualization_conflict=False)
    defaults.update(kwargs)
    return OSInfo(**defaults)  # type: ignore[arg-type]


def _make_report(**kwargs: object) -> TelemetryReport:
    defaults = dict(
        cpu=_make_cpu(), ram=_make_ram(), disk=_make_disk(),
        battery=_make_battery(), os=_make_os(),
        health_score=90, gpu_model="Test GPU",
        gpu_utilization=15.0, gpu_temperature=60.0,
        network_adapter="Ethernet", ip_address="192.168.1.1",
        network_latency_ms=5.0,
    )
    defaults.update(kwargs)
    return TelemetryReport(**defaults)  # type: ignore[arg-type]


# ── CPUInfo ────────────────────────────────────────────────────────────
def test_cpu_info_creation() -> None:
    """CPUInfo must be creatable with all required fields."""
    cpu = _make_cpu()
    assert cpu.utilization == 25.0
    assert cpu.model_name == "Test CPU"
    assert cpu.voltage == 1.2


def test_cpu_info_is_frozen() -> None:
    """CPUInfo must be immutable (frozen dataclass)."""
    cpu = _make_cpu()
    with pytest.raises((AttributeError, TypeError)):
        cpu.utilization = 99.0  # type: ignore[misc]


# ── RAMInfo ────────────────────────────────────────────────────────────
def test_ram_info_percentage_range() -> None:
    """RAM percentage must be within [0.0, 1.0] when constructed correctly."""
    ram = _make_ram(percentage=0.75)
    assert 0.0 <= ram.percentage <= 1.0


# ── DiskInfo ───────────────────────────────────────────────────────────
def test_disk_info_health_range() -> None:
    """DiskInfo health_percent must be an integer in [0, 100]."""
    disk = _make_disk(health_percent=85)
    assert 0 <= disk.health_percent <= 100
    assert isinstance(disk.health_percent, int)


def test_disk_info_status_is_string() -> None:
    """DiskInfo status field must be a string."""
    disk = _make_disk()
    assert isinstance(disk.status, str)


# ── BatteryInfo ────────────────────────────────────────────────────────
def test_battery_info_fields_exist() -> None:
    """BatteryInfo must expose all expected fields."""
    bat = _make_battery()
    assert hasattr(bat, "percentage")
    assert hasattr(bat, "is_charging")
    assert hasattr(bat, "health_percent")
    assert hasattr(bat, "design_capacity_mwh")
    assert hasattr(bat, "current_capacity_mwh")
    assert hasattr(bat, "cycle_count")


# ── TelemetryReport ────────────────────────────────────────────────────
def test_telemetry_report_is_frozen() -> None:
    """TelemetryReport must be immutable after creation."""
    report = _make_report()
    with pytest.raises((AttributeError, TypeError)):
        report.health_score = 50  # type: ignore[misc]


def test_telemetry_report_health_score_range() -> None:
    """health_score must be an integer within [0, 100]."""
    report = _make_report(health_score=75)
    assert 0 <= report.health_score <= 100
    assert isinstance(report.health_score, int)


def test_telemetry_report_contains_all_components() -> None:
    """TelemetryReport must contain cpu, ram, disk, battery, os sub-models."""
    report = _make_report()
    assert isinstance(report.cpu, CPUInfo)
    assert isinstance(report.ram, RAMInfo)
    assert isinstance(report.disk, DiskInfo)
    assert isinstance(report.battery, BatteryInfo)
    assert isinstance(report.os, OSInfo)
