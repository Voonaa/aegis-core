"""Storage telemetry harvester module for Aegis HAL."""

import psutil
from packages.core.models.telemetry import DiskInfo
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("HARDWARE")

class StorageComponent:
    """Storage telemetry module interfacing with host drive partitioning and S.M.A.R.T attributes."""

    def __init__(self) -> None:
        """Initialize the Storage Component."""
        self._capabilities = {
            "partition_polling": True,
            "smart_polling": False
        }

    def query(self) -> DiskInfo:
        """Queries drive storage partition metrics and S.M.A.R.T status.
        
        Returns:
            DiskInfo dataclass mappings.
        """
        # Read storage partitions limits
        dp = psutil.disk_usage("/")
        
        # Default fallback values
        health: int = 98
        status: str = "Good"

        try:
            import wmi
            # Query Win32 Disk status
            w = wmi.WMI()
            drives = w.Win32_DiskDrive()
            if drives:
                smart_val = drives[0].Status
                self._capabilities["smart_polling"] = True
                if smart_val != "OK":
                    health = 30
                    status = f"Warning: SMART {smart_val}"
                else:
                    health = 98
                    status = "Good"
            
            # If Admin UAC is present, query WMI failure predictions namespace
            try:
                w_wmi = wmi.WMI(namespace="root\\wmi")
                predictions = w_wmi.MSStorageDriver_FailurePredictStatus()
                if predictions:
                    if predictions[0].PredictFailure:
                        health = 10
                        status = "Critical SMART Failure Predicted"
            except Exception:
                # ACPI/UAC failure prediction namespace restricted
                pass

        except Exception as ex:
            logger.warning(f"Storage SMART query restricted or failed: {ex}. Using mock defaults.")
            status = "Good (Telemetry Fallback)"

        return DiskInfo(
            used_gb=round(dp.used / (1024 ** 3), 2),
            total_gb=round(dp.total / (1024 ** 3), 2),
            percentage=dp.percent / 100.0,
            health_percent=health,
            status=status
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
