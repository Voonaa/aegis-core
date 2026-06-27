"""Maintenance optimizations service executing temp files cleanup and network flushing."""

import os
import shutil
import tempfile
import time
import subprocess
from pathlib import Path
from typing import Callable
from packages.core.exceptions.custom import RepairError
from packages.core.container import ServiceContainer
from packages.core.services.privilege_service import PrivilegeService
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class MaintenanceService:
    """Manages files cleaning, DNS flush cache resets, and DISM component cleanups."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Maintenance Service.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        self.priv_svc: PrivilegeService = container.get("privilege_service")
        logger.info("Maintenance Service initialized.")

    def flush_dns(self, progress_callback: Callable[[float], None]) -> None:
        """Flushes the Windows DNS Resolver cache.
        
        Args:
            progress_callback: Callback progress tracker.
        """
        config_mgr = self.container.get("config")
        if config_mgr.get("demo_mode", True):
            self._simulate_progress("DNS Cache Flush", progress_callback)
            return

        logger.info("Starting live DNS resolver cache flush.")
        progress_callback(0.0)
        
        try:
            # ipconfig /flushdns does not require admin elevation, but we track progress
            progress_callback(0.2)
            res = subprocess.run(
                ["ipconfig", "/flushdns"],
                capture_output=True,
                text=True,
                creationflags=0x08000000 # CREATE_NO_WINDOW
            )
            
            if res.returncode != 0:
                logger.error(f"DNS Flush returned exit code: {res.returncode}. Stderr: {res.stderr}")
                raise RepairError(f"DNS Resolver Flush failed: {res.stderr}")

            progress_callback(1.0)
            logger.info("DNS cache flushed successfully.")
            
        except Exception as ex:
            raise RepairError(f"DNS Resolver Flush failed: {ex}")

    def clean_temp_files(self, progress_callback: Callable[[float], None]) -> None:
        """Cleans Windows User and System temp directories.
        
        Args:
            progress_callback: Callback progress tracker.
        """
        config_mgr = self.container.get("config")
        if config_mgr.get("demo_mode", True):
            self._simulate_progress("Temporary Files Cleanup", progress_callback)
            return

        logger.info("Starting temporary folder cleanups.")
        progress_callback(0.0)

        # Resolve temp directories
        temp_paths = [
            Path(tempfile.gettempdir()),              # User AppData Local Temp
            Path("C:/Windows/Temp")                    # System Temp
        ]

        files_to_delete = []
        for temp_path in temp_paths:
            if temp_path.exists():
                try:
                    for child in temp_path.iterdir():
                        files_to_delete.append(child)
                except Exception as ex:
                    logger.warning(f"Unable to read temp path {temp_path}: {ex}")

        if not files_to_delete:
            progress_callback(1.0)
            logger.info("No temp files found to delete.")
            return

        total_files = len(files_to_delete)
        deleted_count = 0
        failed_count = 0

        for index, path in enumerate(files_to_delete):
            try:
                if path.is_file() or path.is_symlink():
                    os.unlink(path)
                elif path.is_dir():
                    shutil.rmtree(path)
                deleted_count += 1
            except Exception:
                # File/Folder is locked by another running process (expected)
                failed_count += 1
            
            # Update progress
            progress_callback(index / total_files)

        progress_callback(1.0)
        logger.info(f"Cleanup finished. Deleted: {deleted_count}, Locked/Skipped: {failed_count}")

    def clean_component_store(self, progress_callback: Callable[[float], None]) -> None:
        """Executes elevated DISM StartComponentCleanup task.
        
        Args:
            progress_callback: Callback progress tracker.
        """
        config_mgr = self.container.get("config")
        if config_mgr.get("demo_mode", True):
            self._simulate_progress("DISM Component Store Cleanup", progress_callback)
            return

        if not self.priv_svc.is_admin():
            raise RepairError("Administrative privileges required. Please relaunch Aegis as Administrator.")

        logger.info("Starting live Component Store Cleanup task.")
        progress_callback(0.0)
        
        try:
            # Launch elevated DISM Component Cleanup
            proc = subprocess.Popen(
                ["dism", "/online", "/cleanup-image", "/startcomponentcleanup"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=0x08000000 # CREATE_NO_WINDOW
            )
            
            # Progress parser helper (DISM prints progress lines)
            progress_regex = re.compile(r"\[=*\s*(?P<pct>\d+(\.\d+)?)\%\s*=*(?:\])?")
            
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                
                match = progress_regex.search(line)
                if match:
                    pct = float(match.group("pct"))
                    progress_callback(pct / 100.0)

            proc.wait()
            if proc.returncode != 0:
                logger.error(f"Component Store Cleanup exited with code: {proc.returncode}")
                raise RepairError(f"Component Store Cleanup failed. Process exited with error code: {proc.returncode}")

            progress_callback(1.0)
            logger.info("Component Store Cleanup task complete.")
            
        except Exception as ex:
            raise RepairError(f"Component Store Cleanup subprocess execution failed: {ex}")

    def _simulate_progress(self, task_label: str, progress_callback: Callable[[float], None]) -> None:
        """Simulate task progress steps for Demo Mode."""
        logger.info(f"Simulating progress for task: {task_label}")
        progress_callback(0.0)
        for i in range(1, 101):
            time.sleep(0.03) # Total duration ~3 seconds
            progress_callback(i / 100.0)
