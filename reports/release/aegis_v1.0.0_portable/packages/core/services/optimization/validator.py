"""Optimization Validator validating system state and compiling delta telemetry comparison metrics."""

import time
from typing import Optional
from packages.core.container import ServiceContainer
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class OptimizationValidator:
    """Verifies that power schemes and telemetry boundaries are valid post-tuning."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Optimization Validator.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        logger.info("Optimization Validator initialized.")

    def get_system_snapshot(self) -> dict:
        """Queries the current active power plan GUID and hardware load boundaries.
        
        Returns:
            Snapshot dictionary containing plan GUID and load statistics.
        """
        # Resolve config manager & hardware service
        config_mgr = self.container.get("config")
        demo_mode = config_mgr.get("demo_mode", True)
        
        active_plan = "Balanced"
        cpu_util = 10.0
        free_ram_gb = 8.0

        # Query Power plan GUID
        if not demo_mode:
            try:
                import subprocess
                out = subprocess.run(
                    ["powercfg", "/getactivescheme"],
                    capture_output=True,
                    text=True,
                    creationflags=0x08000000
                )
                if out.returncode == 0:
                    parts = out.stdout.split(":")
                    if len(parts) > 1:
                        active_plan = parts[1].strip().split()[0]
            except Exception:
                pass

            # Query hardware telemetry metrics safely
            try:
                import psutil
                cpu_util = psutil.cpu_percent(interval=None)
                vm = psutil.virtual_memory()
                free_ram_gb = vm.available / (1024 ** 3)
            except Exception:
                pass

        return {
            "power_plan": active_plan,
            "cpu_utilization": round(cpu_util, 1),
            "free_ram_gb": round(free_ram_gb, 2),
            "timestamp": time.time()
        }

    def validate(self, pre_snap: dict, expected_plan_guid: Optional[str] = None) -> dict:
        """Runs validation checks, verifies the plan changes, and returns delta analysis.
        
        Args:
            pre_snap: Pre-optimization telemetry snapshot.
            expected_plan_guid: Expected GUID plan value to verify.
            
        Returns:
            Validation report dictionary with differences mapped.
        """
        post_snap = self.get_system_snapshot()
        
        # Verify plan change
        plan_verified = True
        if expected_plan_guid:
            # Under live conditions check match, under demo bypass
            config_mgr = self.container.get("config")
            if not config_mgr.get("demo_mode", True):
                plan_verified = (post_snap["power_plan"] == expected_plan_guid)

        # Delta analysis
        ram_delta_gb = post_snap["free_ram_gb"] - pre_snap["free_ram_gb"]
        cpu_delta = post_snap["cpu_utilization"] - pre_snap["cpu_utilization"]

        report = {
            "timestamp": time.time(),
            "power_plan_match": plan_verified,
            "pre_state": pre_snap,
            "post_state": post_snap,
            "delta": {
                "free_ram_delta_gb": round(ram_delta_gb, 3),
                "cpu_utilization_delta": round(cpu_delta, 2)
            }
        }

        logger.info(f"Optimization validated. Power plan target match: {plan_verified}")
        return report
