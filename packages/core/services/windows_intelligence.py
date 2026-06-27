"""Windows Intelligence detection service for Aegis Core Platform.

This service reads Windows Registry and WMI namespaces to detect
contextual system states that may affect performance or stability.
It never guesses — if a value cannot be read, the alert is suppressed.
"""

import winreg
from packages.core.models.intelligence import IntelligenceAlert
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class WindowsIntelligenceService:
    """Detects Windows system states and produces labeled IntelligenceAlert items."""

    def __init__(self) -> None:
        """Initialize the Windows Intelligence Service."""
        logger.info("Windows Intelligence Service initialized.")

    def analyze(self) -> list[IntelligenceAlert]:
        """Runs all detection rules and returns a list of IntelligenceAlert items.

        Each detection is independent — a failure in one does not affect others.

        Returns:
            List of IntelligenceAlert dataclass instances.
        """
        alerts: list[IntelligenceAlert] = []

        checks = [
            self._check_hyperv,
            self._check_memory_integrity,
            self._check_vbs,
            self._check_hibernate,
            self._check_fast_startup,
        ]

        for check_fn in checks:
            try:
                result = check_fn()
                if result is not None:
                    alerts.append(result)
            except Exception as ex:
                logger.debug(f"Windows Intelligence check '{check_fn.__name__}' skipped: {ex}")

        logger.debug(f"Windows Intelligence produced {len(alerts)} alert(s).")
        return alerts

    # ------------------------------------------------------------------
    # Individual detection rules
    # ------------------------------------------------------------------

    def _check_hyperv(self) -> IntelligenceAlert | None:
        """Detects if Hyper-V hypervisor is active (affects VMware/gaming performance)."""
        key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                # If the key exists, Hyper-V services are installed
                enabled_val, _ = winreg.QueryValueEx(key, "HypervisorPresent")
                if enabled_val:
                    return IntelligenceAlert(
                        title="Hyper-V Hypervisor Active",
                        message="Hyper-V is running. VMware Workstation and some games may run slower or fail to start.",
                        severity="WARNING",
                        category="VIRTUALIZATION",
                        action="Disable Hyper-V via 'bcdedit /set hypervisorlaunchtype off' and reboot to restore full native performance."
                    )
        except (FileNotFoundError, OSError):
            # Key not present = Hyper-V not installed or not active
            pass
        return None

    def _check_memory_integrity(self) -> IntelligenceAlert | None:
        """Detects if Memory Integrity (HVCI) is enabled (reduces Ryzen CPU performance)."""
        key_path = r"SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                enabled_val, _ = winreg.QueryValueEx(key, "Enabled")
                if enabled_val == 1:
                    return IntelligenceAlert(
                        title="Memory Integrity (HVCI) Enabled",
                        message="Hypervisor-Protected Code Integrity is active. This can reduce GPU/CPU performance by 5–15% on AMD Ryzen systems.",
                        severity="WARNING",
                        category="SECURITY",
                        action="Disable via Windows Security → Device Security → Core Isolation → Memory Integrity. Requires reboot."
                    )
        except (FileNotFoundError, OSError):
            pass
        return None

    def _check_vbs(self) -> IntelligenceAlert | None:
        """Detects if Virtualization Based Security (VBS) is active."""
        key_path = r"SYSTEM\CurrentControlSet\Control\DeviceGuard"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                enabled_val, _ = winreg.QueryValueEx(key, "EnableVirtualizationBasedSecurity")
                if enabled_val == 1:
                    return IntelligenceAlert(
                        title="VBS (Virtualization Based Security) Active",
                        message="VBS is enabled. This uses hardware virtualization which can impact gaming frame rates.",
                        severity="INFO",
                        category="SECURITY",
                        action="Can be disabled in Group Policy or via BIOS settings if gaming performance is the priority."
                    )
        except (FileNotFoundError, OSError):
            pass
        return None

    def _check_hibernate(self) -> IntelligenceAlert | None:
        """Detects if Windows Hibernate mode is disabled."""
        key_path = r"SYSTEM\CurrentControlSet\Control\Power"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                # HibernateEnabled: 0 = disabled, 1 = enabled
                val, _ = winreg.QueryValueEx(key, "HibernateEnabled")
                if val == 0:
                    return IntelligenceAlert(
                        title="Hibernate Mode Disabled",
                        message="Hibernate is turned off. On a laptop, this means you cannot save full system state on low battery.",
                        severity="INFO",
                        category="POWER",
                        action="Re-enable via 'powercfg /hibernate on' in an Administrator terminal."
                    )
        except (FileNotFoundError, OSError):
            pass
        return None

    def _check_fast_startup(self) -> IntelligenceAlert | None:
        """Detects if Fast Startup (Hybrid Boot) is disabled."""
        key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Power"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                val, _ = winreg.QueryValueEx(key, "HiberbootEnabled")
                if val == 0:
                    return IntelligenceAlert(
                        title="Fast Startup Disabled",
                        message="Windows Fast Startup is off. Boot times may be slower than necessary.",
                        severity="INFO",
                        category="POWER",
                        action="Enable via Control Panel → Power Options → Choose what the power buttons do → Turn on Fast Startup."
                    )
        except (FileNotFoundError, OSError):
            pass
        return None
