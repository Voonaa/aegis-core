"""Unit tests for TrendAnalysisService mathematical gradients, forecasting, and period delta comparisons."""

import pytest
import time
from pathlib import Path
from unittest.mock import MagicMock
from packages.core.container import ServiceContainer
from packages.core.config_manager import ConfigManager
from packages.core.services.telemetry_history_service import TelemetryHistoryService
from packages.core.services.trend_analysis import TrendAnalysisService


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    """Reset ServiceContainer singleton between tests."""
    ServiceContainer._instance = None
    yield
    ServiceContainer._instance = None


@pytest.fixture
def container(tmp_path: Path) -> ServiceContainer:
    """Returns a ServiceContainer with mock settings registered."""
    c = ServiceContainer()
    config_file = tmp_path / "settings.json"
    config_mgr = ConfigManager(config_path=config_file, default_settings={"demo_mode": True})
    c.register("config", config_mgr)
    return c


@pytest.fixture
def trend_svc(container: ServiceContainer) -> TrendAnalysisService:
    """Returns a TrendAnalysisService instance with mock history registry."""
    # Register mock history service returning seed arrays
    mock_history = MagicMock(spec=TelemetryHistoryService)
    container.register("telemetry_history_service", mock_history)
    
    return TrendAnalysisService(container=container)


def test_gradient_slope_math(trend_svc: TrendAnalysisService) -> None:
    """calculate_gradient must return positive coefficients on upward trends and negative on downward."""
    upward = [10.0, 12.0, 14.0, 16.0, 18.0]
    downward = [50.0, 48.0, 46.0, 44.0, 42.0]
    flat = [30.0, 30.0, 30.0, 30.0, 30.0]

    assert trend_svc.calculate_gradient(upward) > 0.0
    assert trend_svc.calculate_gradient(downward) < 0.0
    assert trend_svc.calculate_gradient(flat) == 0.0
    assert trend_svc.calculate_gradient([5.0]) == 0.0


def test_analyze_trends_forecasts_battery_degrade(trend_svc: TrendAnalysisService) -> None:
    """analyze_trends must detect degradation and project battery limits target months."""
    # Seed mock history with downward battery values
    mock_history = trend_svc.container.get("telemetry_history_service")
    mock_history.get_history.return_value = [
        {"cpu_temperature": 40.0, "ram_percentage": 0.3, "battery_health_percent": 95},
        {"cpu_temperature": 41.0, "ram_percentage": 0.3, "battery_health_percent": 94},
        {"cpu_temperature": 42.0, "ram_percentage": 0.3, "battery_health_percent": 93}
    ]

    report = trend_svc.analyze_trends()

    assert report["status"] == "SUCCESS"
    assert report["gradients"]["battery_health"] < 0.0
    assert "Degrading" in report["battery_forecast"]


def test_compare_yesterday_vs_today_delta(trend_svc: TrendAnalysisService) -> None:
    """compare_yesterday_vs_today must calculate delta load shift averages correctly."""
    mock_history = trend_svc.container.get("telemetry_history_service")
    now_ts = time.time()
    
    # 2 records today, 2 records yesterday (yesterday cutoff is 86400s)
    mock_history.get_history.return_value = [
        {"timestamp": now_ts - 100000, "cpu_utilization": 40.0, "health_score": 100},
        {"timestamp": now_ts - 90000, "cpu_utilization": 50.0, "health_score": 100},
        {"timestamp": now_ts - 1000, "cpu_utilization": 20.0, "health_score": 90},
        {"timestamp": now_ts - 500, "cpu_utilization": 30.0, "health_score": 90}
    ]

    res = trend_svc.compare_yesterday_vs_today()

    assert res["status"] == "SUCCESS"
    # Today load average = 25.0%. Yesterday = 45.0%. Delta = -20.0%
    assert res["cpu_utilization"]["delta"] == -20.0
    assert res["health_score"]["delta"] == -10.0
