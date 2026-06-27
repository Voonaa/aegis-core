"""Modular system optimization facade orchestrating Planner, Executor, Validator, and Rollback engine."""

from typing import Optional
from packages.core.container import ServiceContainer
from packages.core.exceptions.custom import RepairError
from packages.core.services.optimization.planner import OptimizationPlanner, OptimizationMode, OptimizationPreset
from packages.core.services.optimization.executor import OptimizationExecutor
from packages.core.services.optimization.validator import OptimizationValidator
from packages.core.services.optimization.rollback import RollbackEngine
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class OptimizationService:
    """Gateway coordinating planner, executor, validation checks, and automatic system recovery."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Optimization Service facade.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        self.planner = OptimizationPlanner()
        self.executor = OptimizationExecutor(container)
        self.validator = OptimizationValidator(container)
        self.rollback_engine = RollbackEngine(container)
        logger.info("Modular Optimization Service facade initialized.")

    def apply_optimization(self, mode: OptimizationMode, preset: Optional[OptimizationPreset] = None) -> dict:
        """Plans, backs up, executes, and validates system optimizations with rollback recovery.
        
        Args:
            mode: Target main power plan mode.
            preset: Optional performance optimization sub-preset.
            
        Returns:
            Validation report dictionary mapping changes delta.
        """
        logger.info(f"Optimization trigger received: mode={mode.value}, preset={preset.value if preset else 'None'}")

        # 1. Plan actions list
        plan = self.planner.create_plan(mode, preset)

        # 2. Capture Pre-optimization state
        pre_snap = self.validator.get_system_snapshot()
        pre_plan = pre_snap["power_plan"]

        # 3. Create restore point (Windows + local metadata JSON)
        target_guid = self.planner.power_plans.get(mode)
        self.rollback_engine.create_backup(mode.value, pre_plan, target_guid or "Balanced")
        self.rollback_engine.trigger_windows_restore_point()

        try:
            # 4. Execute optimization actions
            self.executor.execute(plan)

            # 5. Brief validation wait & verify changes
            import time
            time.sleep(0.05)
            report = self.validator.validate(pre_snap, expected_plan_guid=target_guid)
            
            # Save telemetry comparison report to reports/diagnostics/opt_report.json
            import json
            from pathlib import Path
            report_file = Path("reports/diagnostics/opt_report.json")
            report_file.parent.mkdir(parents=True, exist_ok=True)
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

            return {
                "status": "SUCCESS",
                "mode": mode.value,
                "power_plan": report["post_state"]["power_plan"],
                "report": report
            }

        except Exception as ex:
            logger.error(f"Tuning execution failure: {ex}. Initiating recovery rollback.")
            # Trigger recovery rollback
            self.rollback()
            raise RepairError(f"Optimization execution failed. Host was safely rolled back. Details: {ex}")

    def rollback(self) -> dict:
        """Invokes the RollbackEngine to recover settings to previous state."""
        return self.rollback_engine.rollback()

    def capture_current_state(self) -> dict:
        """Wrapper getting current validator snapshot."""
        return self.validator.get_system_snapshot()
