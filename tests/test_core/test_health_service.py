"""Unit tests for the HealthService weighted scoring engine."""

import pytest
from packages.core.services.health_service import HealthService


@pytest.fixture
def svc() -> HealthService:
    """Returns a fresh HealthService instance."""
    return HealthService()


def _score(
    svc: HealthService,
    cpu_util: float = 10.0,
    cpu_temp: float = 50.0,
    ram_percent: float = 0.4,
    disk_health: int = 100,
    battery_health: int = 100,
    virt_conflict: bool = False,
) -> int:
    """Helper to call calculate_score with defaults for brevity."""
    return svc.calculate_score(
        cpu_util=cpu_util,
        cpu_temp=cpu_temp,
        ram_percent=ram_percent,
        disk_health=disk_health,
        battery_health=battery_health,
        virt_conflict=virt_conflict,
    )


def test_perfect_score(svc: HealthService) -> None:
    """All metrics at ideal values must yield score of 100."""
    result = _score(svc)
    assert result == 100


def test_thermal_penalty_moderate(svc: HealthService) -> None:
    """CPU temp at 70°C must reduce the thermal component below 20."""
    result = _score(svc, cpu_temp=70.0)
    # 70°C is 5°C over 65°C threshold → 5 × 0.5 = 2.5 points deducted
    assert result < 100
    assert result >= 80  # Still healthy overall


def test_thermal_penalty_critical(svc: HealthService) -> None:
    """CPU temp at 105°C must zero out the thermal component."""
    result = _score(svc, cpu_temp=105.0)
    # Thermal component = 0; total = 80 max
    assert result <= 80


def test_ram_penalty(svc: HealthService) -> None:
    """RAM usage above 80% must deduct memory points."""
    result = _score(svc, ram_percent=0.95)
    # 95% usage → 15% over threshold → 15 points deducted from memory
    assert result < 100
    assert result >= 80


def test_virtualization_conflict_penalty(svc: HealthService) -> None:
    """Virtualization conflict flag must deduct OS integrity points."""
    without_conflict = _score(svc, virt_conflict=False)
    with_conflict = _score(svc, virt_conflict=True)

    assert with_conflict < without_conflict
    assert (without_conflict - with_conflict) == 10  # 10 point deduction


def test_score_clamped_at_100(svc: HealthService) -> None:
    """Score must never exceed 100 even with perfect inputs."""
    result = _score(svc, disk_health=200, battery_health=200)
    assert result <= 100


def test_score_clamped_at_0(svc: HealthService) -> None:
    """Score must never go below 0 even with all worst-case inputs."""
    result = _score(
        svc,
        cpu_temp=200.0,
        ram_percent=1.0,
        disk_health=0,
        battery_health=0,
        virt_conflict=True,
    )
    assert result >= 0


def test_disk_health_scales_linearly(svc: HealthService) -> None:
    """Disk health at 50% must contribute exactly 10 points (half of 20 max)."""
    full = _score(svc, disk_health=100)
    half = _score(svc, disk_health=50)
    # Difference should be exactly 10 points (storage component)
    assert (full - half) == 10
