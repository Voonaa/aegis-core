"""Optimization Executor running safe power plan switching and maintenance task runs."""

import subprocess
from typing import Callable
from packages.core.container import ServiceContainer
from packages.core.exceptions.custom import RepairError
from packages.core.services.optimization.planner import OptimizationPlan
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class OptimizationExecutor:
    """Runs planned optimization action items (Daya, DNS, Cleanup)."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Optimization Executor.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        logger.info("Optimization Executor initialized.")

    def execute(self, plan: OptimizationPlan) -> list[dict]:
        """Runs the action plan sequence item by item.
        
        Args:
            plan: The planned action items sequence.
            
        Returns:
            List of operation log dictionaries.
        """
        results = []
        for action in plan.actions:
            logger.debug(f"Executing: type={action.type}, target={action.target}")
            
            status = "PENDING"
            error_details = None

            try:
                if action.type == "power_plan":
                    self._apply_power_plan(action.target)
                    status = "SUCCESS"
                elif action.type == "maintenance_job":
                    self._run_maintenance(action.target)
                    status = "SUCCESS"
                elif action.type == "preset_hint":
                    # Hints do not modify registry/services but log details
                    logger.debug(f"Optimization hint applied: {action.target} with params {action.params}")
                    status = "SUCCESS"
                else:
                    raise RepairError(f"Unknown action type: {action.type}")
            except Exception as ex:
                status = "FAILED"
                error_details = str(ex)
                logger.error(f"Action execution failed: {action.type} {action.target} - {ex}")
                raise RepairError(f"Executor failed at action {action.type}:{action.target} - {ex}")

            results.append({
                "type": action.type,
                "target": action.target,
                "status": status,
                "error": error_details
            })

        return results

    def _apply_power_plan(self, plan_guid: str) -> None:
        """Uses Windows powercfg command to set active power scheme."""
        config_mgr = self.container.get("config")
        if config_mgr.get("demo_mode", True):
            logger.debug(f"Demo Mode: Switched power plan to GUID {plan_guid}")
            return

        try:
            out = subprocess.run(
                ["powercfg", "/setactive", plan_guid],
                capture_output=True,
                text=True,
                creationflags=0x08000000
            )
            if out.returncode != 0:
                raise RepairError(f"powercfg setactive failed: {out.stderr}")
            logger.info(f"Active power scheme GUID switched to: {plan_guid}")
        except Exception as ex:
            raise RepairError(f"Failed to execute powercfg plan switch: {ex}")

    def _run_maintenance(self, job_name: str) -> None:
        """Invokes safe system cleaning routines via MaintenanceService."""
        config_mgr = self.container.get("config")
        
        # Resolve MaintenanceService
        try:
            maint_svc = self.container.get("maintenance_service")
        except KeyError:
            logger.warning("MaintenanceService not found in container. Skipping job.")
            return

        # Dummy callback
        def noop_cb(p: float) -> None:
            pass

        if job_name == "dns_flush":
            maint_svc.flush_dns(noop_cb)
        elif job_name == "temp_cleanup":
            maint_svc.clean_temp_files(noop_cb)
        else:
            logger.warning(f"Unknown maintenance job requested: {job_name}")
