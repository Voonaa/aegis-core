"""Unit tests for the modular OptimizationService facade and components."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from packages.core.container import ServiceContainer
from packages.core.config_manager import ConfigManager
from packages.core.exceptions.custom import RepairError
from packages.core.services.optimization import OptimizationService
from packages.core.services.optimization.planner import OptimizationMode, OptimizationPreset, OptimizationPlanner
from packages.core.services.optimization.executor import OptimizationExecutor
from packages.core.services.optimization.validator import OptimizationValidator
from packages.core.services.optimization.rollback import RollbackEngine


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
def svc(container: ServiceContainer, tmp_path: Path) -> OptimizationService:
    """Returns an OptimizationService instance with backups mapped to tmp_path."""
    service = OptimizationService(container=container)
    # Redirect backup directory to temp path for testing
    service.rollback_engine.backups_dir = tmp_path / "backups"
    service.rollback_engine.backups_dir.mkdir(parents=True, exist_ok=True)
    return service


# ── 1. Planner Tests ───────────────────────────────────────────────────
def test_planner_creates_correct_action_count() -> None:
    """OptimizationPlanner must output expected action run list length for Performance."""
    planner = OptimizationPlanner()
    plan = planner.create_plan(OptimizationMode.PERFORMANCE, OptimizationPreset.GAMING)

    assert len(plan.actions) == 4
    types = [a.type for a in plan.actions]
    assert "power_plan" in types
    assert "maintenance_job" in types
    assert "preset_hint" in types


# ── 2. Executor Tests ──────────────────────────────────────────────────
def test_executor_skips_unknown_actions(container: ServiceContainer) -> None:
    """OptimizationExecutor must raise RepairError on failed actions execution."""
    executor = OptimizationExecutor(container)
    mock_plan = MagicMock()
    mock_plan.actions = [MagicMock(type="invalid_type", target="test")]

    with pytest.raises(RepairError):
        executor.execute(mock_plan)


# ── 3. Validator Tests ─────────────────────────────────────────────────
def test_validator_generates_snapshot_and_delta(container: ServiceContainer) -> None:
    """OptimizationValidator must calculate telemetry snaps and difference delta."""
    validator = OptimizationValidator(container)
    
    pre = {"power_plan": "Balanced", "cpu_utilization": 10.0, "free_ram_gb": 8.0}
    report = validator.validate(pre, expected_plan_guid="Balanced")

    assert report["power_plan_match"] is True
    assert "delta" in report
    assert "free_ram_delta_gb" in report["delta"]


# ── 4. RollbackEngine Tests ────────────────────────────────────────────
def test_rollback_engine_metadata_backup(container: ServiceContainer, tmp_path: Path) -> None:
    """RollbackEngine must write JSON metadata files containing changes list."""
    engine = RollbackEngine(container)
    engine.backups_dir = tmp_path
    
    backup_file = engine.create_backup("PERFORMANCE", "Balanced-GUID", "Perf-GUID")

    assert backup_file.exists()
    with open(backup_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["target_mode"] == "PERFORMANCE"
    assert "windows_build" in data
    assert len(data["changes"]) == 1
    assert data["changes"][0]["original_value"] == "Balanced-GUID"


# ── 5. Service Facade Tests ────────────────────────────────────────────
def test_service_apply_optimization_facade(svc: OptimizationService) -> None:
    """Facade apply_optimization must successfully coordinate components."""
    res = svc.apply_optimization(OptimizationMode.PERFORMANCE, OptimizationPreset.GAMING)

    assert res["status"] == "SUCCESS"
    assert res["mode"] == "PERFORMANCE"
    assert "power_plan" in res
    assert "report" in res


def test_service_rollback_on_failure(svc: OptimizationService) -> None:
    """Facade apply_optimization must invoke rollback on executor exception."""
    with patch.object(svc.executor, "execute", side_effect=ValueError("Execution Error")), \
         patch.object(svc, "rollback") as mock_rollback:

        with pytest.raises(RepairError):
            svc.apply_optimization(OptimizationMode.PERFORMANCE)

        # Automatic rollback was triggered
        mock_rollback.assert_called_once()
