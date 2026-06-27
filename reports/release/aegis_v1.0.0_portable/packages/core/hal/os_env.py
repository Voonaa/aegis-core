"""OS details and environment Inspector harvester for Aegis HAL."""

import winreg
from packages.core.models.telemetry import OSInfo
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class OSComponent:
    """OS telemetry module querying registry parameters and virtualization configurations."""

    def __init__(self) -> None:
        """Initialize the OS Component."""
        self._capabilities = {
            "registry_inspections": True,
            "virtualization_checks": True
        }

    def _read_registry_string(self, subkey: str, name: str) -> str:
        """Helper to read registry keys safely."""
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey) as key:
                value, _ = winreg.QueryValueEx(key, name)
                return str(value)
        except Exception:
            return ""

    def query(self) -> OSInfo:
        """Inspects OS build version, edition, and Hyper-V virtualization flags.
        
        Returns:
            OSInfo dataclass mappings.
        """
        # Read Windows Product Name (Edition)
        product_name = self._read_registry_string(
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "ProductName"
        )
        # Windows 11 updates display ProductName as "Windows 10 Pro" sometimes, read DisplayVersion/CurrentBuild
        current_build = self._read_registry_string(
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "CurrentBuild"
        )
        ubr = self._read_registry_string(
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "UBR"
        )

        build_str = f"Build {current_build}"
        if ubr:
            build_str += f".{ubr}"

        # Standard clean name fallbacks
        os_name = product_name if product_name else "Windows 11 Pro"

        # Check Hyper-V active status via WMI query (Hyper-V virtualized network adapter / services)
        hyperv_active = False
        virt_conflict = False

        try:
            import wmi
            w = wmi.WMI()
            # If Win32_ComputerSystem HypervisorPresent is True, virtualization is active
            comp_sys = w.Win32_ComputerSystem()
            if comp_sys and len(comp_sys) > 0:
                hypervisor_present = getattr(comp_sys[0], "HypervisorPresent", False)
                if hypervisor_present:
                    hyperv_active = True
                    # If computer manufacturer is virtual, we could have nested virtualization warnings
                    model = getattr(comp_sys[0], "Model", "")
                    manufacturer = getattr(comp_sys[0], "Manufacturer", "")
                    if "virtual" in model.lower() or "vmware" in manufacturer.lower():
                        virt_conflict = True
        except Exception as ex:
            logger.warning(f"Failed to fetch virtualization properties: {ex}.")

        return OSInfo(
            os_name=os_name,
            build_version=build_str,
            hyperv_active=hyperv_active,
            virtualization_conflict=virt_conflict
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
