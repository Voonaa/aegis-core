"""Unit tests for the WindowsIntelligenceService detection engine."""

import pytest
from unittest.mock import patch, MagicMock
from packages.core.services.windows_intelligence import WindowsIntelligenceService
from packages.core.models.intelligence import IntelligenceAlert


@pytest.fixture
def svc() -> WindowsIntelligenceService:
    """Returns a fresh WindowsIntelligenceService instance."""
    return WindowsIntelligenceService()


def test_analyze_returns_list(svc: WindowsIntelligenceService) -> None:
    """`analyze()` must always return a list (may be empty on a clean system)."""
    result = svc.analyze()
    assert isinstance(result, list)


def test_analyze_items_are_intelligence_alerts(svc: WindowsIntelligenceService) -> None:
    """Every item returned by `analyze()` must be an IntelligenceAlert instance."""
    result = svc.analyze()
    for item in result:
        assert isinstance(item, IntelligenceAlert)


def test_alert_severity_always_valid(svc: WindowsIntelligenceService) -> None:
    """All alerts must have severity of INFO, WARNING, or CRITICAL."""
    valid_severities = {"INFO", "WARNING", "CRITICAL"}
    result = svc.analyze()
    for alert in result:
        assert alert.severity in valid_severities, f"Invalid severity: {alert.severity}"


def test_check_failure_does_not_propagate(svc: WindowsIntelligenceService) -> None:
    """If one check raises an unexpected exception, analyze() must still return without raising."""
    # Patch all registry calls to raise an exception
    with patch("winreg.OpenKey", side_effect=OSError("Access denied")):
        result = svc.analyze()

    # Must not raise; must return an empty list or partial list
    assert isinstance(result, list)


def test_hyperv_detected_when_registry_present(svc: WindowsIntelligenceService) -> None:
    """When Hyper-V registry key is present with HypervisorPresent=1, alert must be generated."""
    mock_key = MagicMock()

    def mock_query(key: object, name: str) -> tuple:
        if name == "HypervisorPresent":
            return (1, None)
        raise FileNotFoundError

    with patch("winreg.OpenKey", return_value=mock_key), \
         patch("winreg.QueryValueEx", side_effect=mock_query):
        result = svc._check_hyperv()

    assert result is not None
    assert result.severity in {"WARNING", "CRITICAL"}
    assert "Hyper-V" in result.title


def test_hyperv_returns_none_when_key_missing(svc: WindowsIntelligenceService) -> None:
    """When the Hyper-V registry key does not exist, `_check_hyperv` must return None."""
    with patch("winreg.OpenKey", side_effect=FileNotFoundError):
        result = svc._check_hyperv()

    assert result is None


def test_all_checks_run_independently(svc: WindowsIntelligenceService) -> None:
    """Even if some checks fail, the remaining checks must still run."""
    call_count = []

    original_checks = [
        svc._check_hyperv,
        svc._check_memory_integrity,
        svc._check_vbs,
        svc._check_hibernate,
        svc._check_fast_startup,
    ]

    def tracking_check(fn: object) -> object:
        def wrapper() -> None:
            call_count.append(1)
            raise OSError("Simulated failure")
        return wrapper

    # Patch individual checks with tracking wrappers
    svc._check_hyperv = tracking_check(svc._check_hyperv)  # type: ignore[method-assign]
    svc._check_memory_integrity = tracking_check(svc._check_memory_integrity)  # type: ignore[method-assign]
    svc._check_vbs = tracking_check(svc._check_vbs)  # type: ignore[method-assign]
    svc._check_hibernate = tracking_check(svc._check_hibernate)  # type: ignore[method-assign]
    svc._check_fast_startup = tracking_check(svc._check_fast_startup)  # type: ignore[method-assign]

    result = svc.analyze()

    # All 5 checks must have been attempted
    assert len(call_count) == 5
    # Despite all failing, result must still be a list
    assert isinstance(result, list)
