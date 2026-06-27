"""RAM telemetry harvester module for Aegis HAL."""

import psutil
from packages.core.models.telemetry import RAMInfo

class RAMComponent:
    """RAM telemetry module interfacing with host memory status."""

    def __init__(self) -> None:
        """Initialize the RAM Component."""
        self._capabilities = {
            "physical_polling": True
        }

    def query(self) -> RAMInfo:
        """Queries RAM utilization ratios.
        
        Returns:
            RAMInfo dataclass mapping.
        """
        vm = psutil.virtual_memory()
        return RAMInfo(
            used_gb=round(vm.used / (1024 ** 3), 2),
            total_gb=round(vm.total / (1024 ** 3), 2),
            percentage=vm.percent / 100.0
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capabilities mappings."""
        return self._capabilities
