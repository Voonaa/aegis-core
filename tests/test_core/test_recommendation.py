"""Unit tests for the RecommendationService rules engine."""

import pytest
from packages.core.services.recommendation import RecommendationService
from packages.core.models.telemetry import (
    TelemetryReport, CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo
)


@pytest.fixture
def svc() -> RecommendationService:
    """Returns a fresh RecommendationService instance."""
    return RecommendationService()


def _make_report(
    cpu_temp: float = 50.0,
    cpu_util: float = 20.0,
    ram_percent: float = 0.5,
    disk_health: int = 95,
    battery_health: int = 95,
    virt_conflict: bool = False,
) -> TelemetryReport:
    """Build a TelemetryReport with controlled parameters for rule testing."""
    return TelemetryReport(
        cpu=CPUInfo(
            utilization=cpu_util,
            temperature=cpu_temp,
            model_name="Test CPU",
            frequency_ghz=3.5,
            voltage=1.2,
            power_draw_watts=25.0,
        ),
        ram=RAMInfo(used_gb=8.0, total_gb=16.0, percentage=ram_percent),
        disk=DiskInfo(
            used_gb=100.0,
            total_gb=500.0,
            percentage=0.2,
            health_percent=disk_health,
            status="OK",
            temperature=35.0,
            power_on_hours=1000,
            host_writes_gb=500.0,
        ),
        battery=BatteryInfo(
            percentage=80,
            is_charging=False,
            health_percent=battery_health,
            time_remaining_mins=120,
            design_capacity_mwh=50000,
            current_capacity_mwh=47500,
            cycle_count=150,
        ),
        os=OSInfo(
            os_name="Windows 11",
            build_version="22H2",
            hyperv_active=False,
            virtualization_conflict=virt_conflict,
        ),
        health_score=90,
        gpu_model="Test GPU",
        gpu_utilization=10.0,
        gpu_temperature=55.0,
        network_adapter="Ethernet",
        ip_address="192.168.1.1",
        network_latency_ms=5.0,
    )


def test_healthy_system_returns_default(svc: RecommendationService) -> None:
    """A system with all metrics within normal bounds must return the healthy fallback."""
    report = _make_report()
    advices = svc.get_recommendations(report)

    assert len(advices) == 1
    assert advices[0]["priority"] == "LOW"
    assert "Healthy" in advices[0]["title"]


def test_high_temp_triggers_high_priority(svc: RecommendationService) -> None:
    """CPU temperature above 75°C must trigger a HIGH priority thermal recommendation."""
    report = _make_report(cpu_temp=80.0)
    advices = svc.get_recommendations(report)

    titles = [a["title"] for a in advices]
    priorities = [a["priority"] for a in advices]

    assert any("Thermal" in t or "Processor" in t for t in titles)
    assert "HIGH" in priorities


def test_elevated_temp_triggers_normal_priority(svc: RecommendationService) -> None:
    """CPU temperature between 65–75°C must trigger a NORMAL priority recommendation."""
    report = _make_report(cpu_temp=70.0)
    advices = svc.get_recommendations(report)

    priorities = [a["priority"] for a in advices]
    assert "NORMAL" in priorities
    # Must not be HIGH (only elevated, not critical)
    assert "HIGH" not in priorities


def test_ssd_wear_triggers_alert(svc: RecommendationService) -> None:
    """SSD health below 80% must trigger an SSD health recommendation."""
    report = _make_report(disk_health=70)
    advices = svc.get_recommendations(report)

    titles = [a["title"] for a in advices]
    assert any("SSD" in t or "Storage" in t or "Disk" in t for t in titles)


def test_battery_wear_triggers_alert(svc: RecommendationService) -> None:
    """Battery health below 80% must trigger a battery degradation recommendation."""
    report = _make_report(battery_health=70)
    advices = svc.get_recommendations(report)

    titles = [a["title"] for a in advices]
    assert any("Battery" in t for t in titles)


def test_high_ram_triggers_alert(svc: RecommendationService) -> None:
    """RAM usage above 85% must trigger a memory utilization recommendation."""
    report = _make_report(ram_percent=0.90)
    advices = svc.get_recommendations(report)

    titles = [a["title"] for a in advices]
    assert any("Memory" in t or "RAM" in t for t in titles)


def test_multiple_issues_returns_all_alerts(svc: RecommendationService) -> None:
    """Multiple triggered rules must all appear in the recommendation list."""
    report = _make_report(
        cpu_temp=80.0,
        ram_percent=0.90,
        disk_health=70,
        battery_health=70,
    )
    advices = svc.get_recommendations(report)

    # Should have at least 4 recommendations (thermal + ram + ssd + battery)
    assert len(advices) >= 4


def test_virt_conflict_triggers_alert(svc: RecommendationService) -> None:
    """Virtualization conflict flag must trigger a conflict recommendation."""
    report = _make_report(virt_conflict=True)
    advices = svc.get_recommendations(report)

    titles = [a["title"] for a in advices]
    assert any("Virtualization" in t or "Hyper" in t or "Conflict" in t for t in titles)
