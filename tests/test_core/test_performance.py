"""Performance regression tests for Aegis Core Platform critical engines."""

import time
import pytest
from unittest.mock import patch, MagicMock
from packages.core.services.health_service import HealthService
from packages.core.services.recommendation import RecommendationService
from packages.core.models.telemetry import (
    TelemetryReport, CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo
)


def test_health_engine_performance() -> None:
    """HealthService calculation must execute in under 10 milliseconds."""
    svc = HealthService()
    
    # Warm-up run
    svc.calculate_score(10.0, 50.0, 0.4, 95, 95, False)
    
    start_time = time.perf_counter()
    
    # 100 iterations to get an accurate average representation
    for _ in range(100):
        svc.calculate_score(10.0, 50.0, 0.4, 95, 95, False)
        
    end_time = time.perf_counter()
    avg_duration_ms = ((end_time - start_time) / 100) * 1000.0
    
    # Assertion Gate: Must be well under 10ms
    assert avg_duration_ms < 10.0, f"Health Engine calculation took {avg_duration_ms:.3f}ms (threshold < 10ms)"


def test_recommendation_performance() -> None:
    """Recommendation engine mapping rules must execute in under 5 milliseconds."""
    svc = RecommendationService()
    report = TelemetryReport(
        cpu=CPUInfo(25.0, 55.0, "Test CPU", 3.5, 1.2, 20.0),
        ram=RAMInfo(8.0, 16.0, 0.5),
        disk=DiskInfo(100.0, 500.0, 0.2, 95, "OK", 35.0, 1000, 500.0),
        battery=BatteryInfo(80, False, 90, 120, 50000, 45000, 200),
        os=OSInfo("Windows 11", "22H2", False, False),
        health_score=90,
        gpu_model="Test GPU",
        gpu_utilization=15.0,
        gpu_temperature=60.0,
        network_adapter="Ethernet",
        ip_address="192.168.1.1",
        network_latency_ms=5.0
    )
    
    # Warm-up run
    svc.get_recommendations(report)
    
    start_time = time.perf_counter()
    for _ in range(100):
        svc.get_recommendations(report)
    end_time = time.perf_counter()
    
    avg_duration_ms = ((end_time - start_time) / 100) * 1000.0
    
    # Assertion Gate: Must be well under 5ms
    assert avg_duration_ms < 5.0, f"Recommendation Engine rules took {avg_duration_ms:.3f}ms (threshold < 5ms)"


@patch("wmi.WMI")
@patch("psutil.cpu_percent")
@patch("psutil.cpu_freq", create=True)
@patch("psutil.sensors_temperatures", create=True)
def test_hal_cpu_query_performance(
    mock_sensors: MagicMock,
    mock_freq: MagicMock,
    mock_cpu_pct: MagicMock,
    mock_wmi_class: MagicMock
) -> None:
    """Mocked CPU HAL harvester query must execute in under 100 milliseconds to avoid GUI stutter."""
    from packages.core.hal.cpu import CPUComponent
    
    # Mock inputs to bypass actual WMI system calls overhead
    mock_cpu_pct.return_value = 25.0
    mock_freq.return_value = MagicMock(current=3300.0)
    mock_sensors.return_value = {}
    
    mock_wmi = MagicMock()
    mock_wmi_class.return_value = mock_wmi
    
    # Mock CPU names and properties
    proc_mock = MagicMock()
    proc_mock.Name = "AMD Ryzen 7 5800H"
    proc_mock.CurrentVoltage = 12
    mock_wmi.Win32_Processor.return_value = [proc_mock]
    mock_wmi.MSAcpi_ThermalZoneTemperature.return_value = []
    
    comp = CPUComponent()
    
    # Warm-up run
    comp.query()
    
    start_time = time.perf_counter()
    for _ in range(20):
        comp.query()
    end_time = time.perf_counter()
    
    avg_duration_ms = ((end_time - start_time) / 20) * 1000.0
    
    # Assertion Gate: Must be well under 100ms
    assert avg_duration_ms < 100.0, f"HAL CPU Harvester took {avg_duration_ms:.3f}ms (threshold < 100ms)"
