"""Rollback Engine managing OS checkpoints, registry backups, and settings restoration."""

import os
import json
import time
import subprocess
from pathlib import Path
from packages.core.container import ServiceContainer
from packages.core.exceptions.custom import RepairError
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class RollbackEngine:
    """Manages local JSON backups, metadata, OS restore points fallback check, and rollback executions."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Rollback Engine.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        self.backups_dir = Path("apps/desktop/config/backups")
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Rollback Engine initialized.")

    def check_restore_point_enabled(self) -> bool:
        """Queries registry or system to see if Checkpoint-Computer is enabled on the host OS."""
        config_mgr = self.container.get("config")
        if config_mgr.get("demo_mode", True):
            return True

        try:
            import winreg
            # Check SystemRestore registry settings key
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                "Software\\Microsoft\\Windows NT\\CurrentVersion\\SystemRestore",
                0, winreg.KEY_READ
            ) as key:
                val, _ = winreg.QueryValueEx(key, "SystemRestorePointCreationFrequency")
                # If key exists, restore points are typically supported/enabled
                return True
        except FileNotFoundError:
            # If subkey exists but parameter missing, it's generally enabled
            return True
        except Exception:
            return False

    def create_backup(self, target_mode: str, original_plan: str, new_plan: str) -> Path:
        """Creates a JSON backup containing structured metadata and changes details list."""
        os_build = "10.0.22621"  # Default fallback
        
        # Get Windows OS Build details if available
        config_mgr = self.container.get("config")
        if not config_mgr.get("demo_mode", True):
            try:
                import platform
                os_build = f"{platform.system()} {platform.release()} (Build {platform.version()})"
            except Exception:
                pass

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file_timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = self.backups_dir / f"restore_{file_timestamp}.json"

        # Create structured metadata
        backup_data = {
            "timestamp": timestamp,
            "windows_build": os_build,
            "target_mode": target_mode,
            "changes": [
                {
                    "type": "power_plan",
                    "original_value": original_plan,
                    "new_value": new_plan
                }
            ]
        }

        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2)

        logger.info(f"Local backup JSON written: {backup_file.name}")
        return backup_file

    def trigger_windows_restore_point(self) -> None:
        """Triggers PowerShell checkpoint creation if system restore points are enabled."""
        if not self.check_restore_point_enabled():
            logger.warning("Windows System Restore is disabled on the host OS. Skipping system checkpoint.")
            return

        try:
            # Trigger asynchronous elevated subprocess checkpoint
            cmd = (
                "Powershell.exe -Command \"Checkpoint-Computer "
                "-Description 'Aegis Pre-Optimization Restore Point' "
                "-RestorePointType MODIFY_SETTINGS\""
            )
            subprocess.Popen(
                cmd,
                shell=True,
                creationflags=0x08000000
            )
            logger.info("Triggered OS Checkpoint-Computer command in background.")
        except Exception as ex:
            logger.warning(f"Failed to execute Checkpoint-Computer: {ex}")

    def rollback(self) -> dict:
        """Restores plan GUIDs from the latest local JSON backup file."""
        backups = sorted(list(self.backups_dir.glob("restore_*.json")))
        if not backups:
            logger.warning("No local restore points found to rollback.")
            return {"status": "FAILED", "reason": "No restore points found"}

        target_file = backups[-1]
        logger.info(f"Executing rollback from file: {target_file.name}")

        try:
            with open(target_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            changes = data.get("changes", [])
            restored_count = 0

            for change in changes:
                if change.get("type") == "power_plan":
                    orig = change.get("original_value")
                    if orig:
                        self._apply_power_plan_raw(orig)
                        restored_count += 1

            # Cleanup backup file
            try:
                target_file.unlink()
            except Exception:
                pass

            logger.info(f"Rollback completed. Restored {restored_count} system settings.")
            return {"status": "SUCCESS", "restored_file": target_file.name}

        except Exception as ex:
            logger.error(f"Rollback execution failure on {target_file.name}: {ex}")
            return {"status": "FAILED", "reason": str(ex)}

    def _apply_power_plan_raw(self, plan_guid: str) -> None:
        """Executes raw powercfg settings switch during rollback recovery."""
        config_mgr = self.container.get("config")
        if config_mgr.get("demo_mode", True):
            logger.debug(f"Demo Mode Rollback: powercfg GUID restored to {plan_guid}")
            return

        try:
            out = subprocess.run(
                ["powercfg", "/setactive", plan_guid],
                capture_output=True,
                text=True,
                creationflags=0x08000000
            )
            if out.returncode != 0:
                raise RepairError(f"powercfg failed: {out.stderr}")
            logger.debug(f"Power plan GUID restored to {plan_guid}")
        except Exception as ex:
            raise RepairError(f"Failed to switch power scheme: {ex}")
