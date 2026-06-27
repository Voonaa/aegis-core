import pytest
from unittest.mock import MagicMock
from packages.core.container import ServiceContainer
from packages.core.event_bus import EventBus
from packages.core.models.telemetry import TelemetryReport, CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo

@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    """Reset ServiceContainer singleton between tests."""
    ServiceContainer._instance = None
    yield
    ServiceContainer._instance = None

def test_hardware_sdk_methods() -> None:
    from packages.sdk.hardware import HardwareSDK
    
    container = ServiceContainer()
    hw_service = MagicMock()
    
    # Mock data structs
    cpu = CPUInfo(25.0, 50.0, "Intel", 2.5, 1.1, 35.0)
    ram = RAMInfo(4.0, 8.0, 50.0)
    disk = DiskInfo(100.0, 250.0, 40.0, 95, "Ok", 35.0, 800, 1000.0)
    battery = BatteryInfo(90, True, 98, 60, 50000, 48000, 12)
    os_info = OSInfo("Win11", "22H2", False, False)
    
    report = TelemetryReport(
        cpu=cpu, ram=ram, disk=disk, battery=battery, os=os_info,
        health_score=99, gpu_model="Intel HD", gpu_utilization=5.0,
        gpu_temperature=40.0, network_adapter="Wifi", ip_address="127.0.0.1",
        network_latency_ms=5.0
    )
    hw_service.gather_telemetry.return_value = report
    container.register("hardware_service", hw_service)
    
    sdk = HardwareSDK(container)
    assert sdk.telemetry_report() == report
    assert sdk.cpu_info() == cpu
    assert sdk.ram_info() == ram
    assert sdk.storage_info() == disk
    assert sdk.battery_info() == battery
    assert sdk.os_info() == os_info

def test_repair_sdk_methods() -> None:
    from packages.sdk.repair import RepairSDK
    
    container = ServiceContainer()
    job_mgr = MagicMock()
    rep_svc = MagicMock()
    maint_svc = MagicMock()
    
    job_mgr.submit.side_effect = lambda name, fn: f"job_{name.replace(' ', '_').lower()}"
    
    container.register("job_manager", job_mgr)
    container.register("repair_service", rep_svc)
    container.register("maintenance_service", maint_svc)
    
    sdk = RepairSDK(container)
    
    assert sdk.sfc() == "job_sfc_scannow_verification"
    assert sdk.dism() == "job_dism_restorehealth_image_scan"
    assert sdk.chkdsk() == "job_chkdsk_file_system_verify"
    assert sdk.flush_dns() == "job_dns_cache_flush"
    assert sdk.clean_temp() == "job_temporary_files_cleanup"
    assert sdk.clean_components() == "job_dism_component_store_cleanup"

def test_report_sdk_methods() -> None:
    from packages.sdk.report import ReportSDK
    
    container = ServiceContainer()
    rep_svc = MagicMock()
    rep_svc.generate_report.return_value = "report_success"
    container.register("report_service", rep_svc)
    
    sdk = ReportSDK(container)
    assert sdk.generate() == "report_success"

def test_sdk_init_exports_aegis_sdk() -> None:
    """The SDK __init__ must export AegisSDK class."""
    from packages.sdk import AegisSDK
    assert AegisSDK is not None

def test_aegis_sdk_has_hardware_repair_report() -> None:
    """AegisSDK instance must expose .hardware, .repair, and .report attributes."""
    from packages.sdk import AegisSDK
    from packages.sdk.hardware import HardwareSDK
    from packages.sdk.repair import RepairSDK
    from packages.sdk.report import ReportSDK

    container = ServiceContainer()
    container.register("event_bus", EventBus())

    sdk = AegisSDK()

    assert hasattr(sdk, "hardware")
    assert hasattr(sdk, "repair")
    assert hasattr(sdk, "report")
    assert isinstance(sdk.hardware, HardwareSDK)
    assert isinstance(sdk.repair, RepairSDK)
    assert isinstance(sdk.report, ReportSDK)
