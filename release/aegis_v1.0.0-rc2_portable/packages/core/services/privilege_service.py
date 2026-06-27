"""Privilege manager service verifying UAC levels and executing elevated subprocesses."""

import sys
import ctypes
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class PrivilegeService:
    """Manages UAC admin detection and elevated executable execution wrappers."""

    def __init__(self) -> None:
        """Initialize the Privilege Service."""
        logger.info("Privilege Service initialized.")

    def is_admin(self) -> bool:
        """Verifies if the current process has administrator rights.
        
        Returns:
            True if running with Administrator privileges, False otherwise.
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception as ex:
            logger.warning(f"Failed to check admin status: {ex}. Assuming user-mode.")
            return False

    def relaunch_as_admin(self) -> bool:
        """Prompts for UAC elevation by relaunching the application process.
        
        Returns:
            True if elevation process was successfully triggered.
        """
        if self.is_admin():
            logger.info("Application is already running with administrative privileges.")
            return True

        logger.info("Relaunching process as Admin: requesting UAC credentials.")
        try:
            # Relaunch current Python executable with original arguments
            script_path = sys.argv[0]
            args = " ".join(sys.argv[1:])
            
            # Use ctypes shell runas verb to elevate
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                f'"{script_path}" {args}', 
                None, 
                1 # SW_SHOWNORMAL
            )
            
            if int(ret) > 32:
                logger.info("UAC elevation triggered. Closing user-mode process.")
                sys.exit(0)
            else:
                logger.warning(f"UAC elevation rejected by user. Shell error code: {ret}")
                return False
        except Exception as ex:
            logger.error(f"UAC elevation prompt failed: {ex}", exc_info=True)
            return False

    def run_elevated_command(self, command: str, arguments: str) -> bool:
        """Executes a target binary with admin rights via UAC prompts.
        
        Args:
            command: Executable binary path (e.g. cmd.exe, powershell.exe).
            arguments: CLI arguments (e.g. '/c sfc /scannow').
            
        Returns:
            True if execution request completed.
        """
        logger.info(f"Requesting elevated command: {command} {arguments}")
        try:
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                command, 
                arguments, 
                None, 
                0 # SW_HIDE (run in background)
            )
            return int(ret) > 32
        except Exception as ex:
            logger.error(f"Failed to run elevated command: {ex}", exc_info=True)
            return False
