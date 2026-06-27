"""Hardware components wrapper class for Aegis SDK."""

from packages.core.models.telemetry import TelemetryReport, CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo
from packages.core.container import ServiceContainer
from packages.core.services.hardware_service import HardwareService

class HardwareSDK:
    """Interface to access Aegis Core Hardware Abstraction Layer (HAL) properties."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Hardware SDK.
        
        Args:
            container: DI Service container reference.
        """
        self._container = container

    def _get_service(self) -> HardwareService:
        return self._container.get("hardware_service")

    def telemetry_report(self) -> TelemetryReport:
        """Assembles and returns the full TelemetryReport payload.
        
        Returns:
            Latest TelemetryReport dataclass.
        """
        return self._get_service().gather_telemetry()

    def cpu_info(self) -> CPUInfo:
        """Gets CPU clock, usage, model, and core temperature details."""
        return self.telemetry_report().cpu

    def ram_info(self) -> RAMInfo:
        """Gets RAM capacity bounds and percentage usage."""
        return self.telemetry_report().ram

    def storage_info(self) -> DiskInfo:
        """Gets SSD SMART status and partition usages."""
        return self.telemetry_report().disk

    def battery_info(self) -> BatteryInfo:
        """Gets battery degradation, charge states, and cycle wear."""
        return self.telemetry_report().battery

    def os_info(self) -> OSInfo:
        """Gets Windows environment registry builds and Hyper-V settings."""
        return self.telemetry_report().os
