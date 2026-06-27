"""Unit tests for the Aegis SDK public interface layer."""

import pytest
from packages.core.container import ServiceContainer
from packages.core.event_bus import EventBus


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    """Reset ServiceContainer singleton between tests."""
    ServiceContainer._instance = None
    yield
    ServiceContainer._instance = None


def test_hardware_sdk_importable() -> None:
    """HardwareSDK must be importable without errors."""
    from packages.sdk.hardware import HardwareSDK  # noqa: F401


def test_repair_sdk_importable() -> None:
    """RepairSDK must be importable without errors."""
    from packages.sdk.repair import RepairSDK  # noqa: F401


def test_report_sdk_importable() -> None:
    """ReportSDK must be importable without errors."""
    from packages.sdk.report import ReportSDK  # noqa: F401


def test_sdk_init_exports_aegis_sdk() -> None:
    """The SDK __init__ must export AegisSDK class."""
    from packages.sdk import AegisSDK  # noqa: F401
    assert AegisSDK is not None


def test_aegis_sdk_has_hardware_repair_report() -> None:
    """AegisSDK instance must expose .hardware, .repair, and .report attributes."""
    from packages.sdk import AegisSDK
    from packages.sdk.hardware import HardwareSDK
    from packages.sdk.repair import RepairSDK
    from packages.sdk.report import ReportSDK

    # Provide minimal container so AegisSDK can instantiate
    container = ServiceContainer()
    container.register("event_bus", EventBus())

    sdk = AegisSDK()

    assert hasattr(sdk, "hardware")
    assert hasattr(sdk, "repair")
    assert hasattr(sdk, "report")
    assert isinstance(sdk.hardware, HardwareSDK)
    assert isinstance(sdk.repair, RepairSDK)
    assert isinstance(sdk.report, ReportSDK)
