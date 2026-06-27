"""Windows active repair engine executing elevated DISM, SFC, and CHKDSK subprocesses."""

import re
import time
import subprocess
from typing import Callable
from packages.core.exceptions.custom import RepairError
from packages.core.container import ServiceContainer
from packages.core.services.privilege_service import PrivilegeService
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class RepairService:
    """Manages system integrity repair tools, capturing subprocess progress streams."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Repair Service.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        self.priv_svc: PrivilegeService = container.get("privilege_service")
        
        # Regex patterns to parse progress values from stdout lines
        self.dism_regex = re.compile(r"\[=*\s*(?P<pct>\d+(\.\d+)?)\%\s*=*(?:\])?")
        self.sfc_regex = re.compile(r"Verification\s+(?P<pct>\d+)\%\s+complete")
        
        logger.info("Repair Service initialized.")

    def _verify_privileges(self) -> None:
        """Ensures process is running elevated before triggering repair operations."""
        config_mgr = self.container.get("config")
        demo_mode = config_mgr.get("demo_mode", True)

        if not demo_mode and not self.priv_svc.is_admin():
            logger.error("Attempted elevated task without Administrator privileges.")
            raise RepairError("Administrative privileges required. Please relaunch Aegis as Administrator.")

    def run_sfc(self, progress_callback: Callable[[float], None]) -> None:
        """Runs SFC Scannow subprocess checking for system file corruptions.
        
        Args:
            progress_callback: Callback progress tracker.
        """
        self._verify_privileges()
        config_mgr = self.container.get("config")
        
        if config_mgr.get("demo_mode", True):
            self._simulate_progress("SFC scan Verification", progress_callback)
            return

        logger.info("Starting live SFC Scannow verification process.")
        progress_callback(0.0)
        
        try:
            # Launch elevated command subprocess with hidden windows flags
            proc = subprocess.Popen(
                ["sfc", "/scannow"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=0x08000000 # CREATE_NO_WINDOW
            )
            
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                
                # Try to parse percentage complete
                match = self.sfc_regex.search(line)
                if match:
                    pct = float(match.group("pct"))
                    progress_callback(pct / 100.0)
            
            proc.wait()
            if proc.returncode != 0:
                logger.error(f"SFC scan exited with code: {proc.returncode}")
                # Note: SFC code 0 means no integrity violations, 1 means errors repaired, other codes might indicate failure
                if proc.returncode not in [0, 1]:
                    raise RepairError(f"SFC scan failed. Process exited with error code: {proc.returncode}")

            progress_callback(1.0)
            
        except Exception as ex:
            if not isinstance(ex, RepairError):
                raise RepairError(f"SFC subprocess failed: {ex}")
            raise ex

    def run_dism(self, progress_callback: Callable[[float], None]) -> None:
        """Runs DISM Restorehealth subprocess repairing Windows component stores.
        
        Args:
            progress_callback: Callback progress tracker.
        """
        self._verify_privileges()
        config_mgr = self.container.get("config")
        
        if config_mgr.get("demo_mode", True):
            self._simulate_progress("DISM RestoreHealth Image Scan", progress_callback)
            return

        logger.info("Starting live DISM Restorehealth image scan.")
        progress_callback(0.0)
        
        try:
            proc = subprocess.Popen(
                ["dism", "/online", "/cleanup-image", "/restorehealth"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=0x08000000 # CREATE_NO_WINDOW
            )
            
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                
                match = self.dism_regex.search(line)
                if match:
                    pct = float(match.group("pct"))
                    progress_callback(pct / 100.0)
            
            proc.wait()
            if proc.returncode != 0:
                logger.error(f"DISM exited with code: {proc.returncode}")
                raise RepairError(f"DISM repair failed. Process exited with error code: {proc.returncode}")

            progress_callback(1.0)
            
        except Exception as ex:
            if not isinstance(ex, RepairError):
                raise RepairError(f"DISM subprocess execution failed: {ex}")
            raise ex

    def run_chkdsk(self, progress_callback: Callable[[float], None]) -> None:
        """Runs CHKDSK verify operations.
        
        Args:
            progress_callback: Callback progress tracker.
        """
        self._verify_privileges()
        config_mgr = self.container.get("config")
        
        if config_mgr.get("demo_mode", True):
            self._simulate_progress("CHKDSK File System Verify", progress_callback)
            return

        logger.info("Starting live CHKDSK verify on active drive.")
        progress_callback(0.0)
        
        try:
            # We run read-only check so we don't lock the OS drive on runtime
            proc = subprocess.Popen(
                ["chkdsk", "c:"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=0x08000000 # CREATE_NO_WINDOW
            )
            
            # CHKDSK prints stages, we'll parse text stages or increment progress linearly
            stage = 0
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                
                # Check for stage text: "Stage 1: ...", "Stage 2: ...", etc.
                if "Stage" in line:
                    stage += 1
                    # CHKDSK has 3 stages (sometimes 5), mock progress based on stages
                    progress_callback(min(0.9, stage * 0.25))
            
            proc.wait()
            if proc.returncode != 0:
                logger.error(f"CHKDSK verify exited with code: {proc.returncode}")
                raise RepairError(f"CHKDSK failed. Process exited with error code: {proc.returncode}")
            
            progress_callback(1.0)
            
        except Exception as ex:
            if not isinstance(ex, RepairError):
                raise RepairError(f"CHKDSK verify failed: {ex}")
            raise ex

    def _simulate_progress(self, task_label: str, progress_callback: Callable[[float], None]) -> None:
        """Simulate task progress steps for Demo Mode."""
        logger.info(f"Simulating progress for task: {task_label}")
        progress_callback(0.0)
        for i in range(1, 101):
            time.sleep(0.05) # Total duration ~5 seconds
            progress_callback(i / 100.0)
