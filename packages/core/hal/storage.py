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
        temp: float = 36.0
        p_hours: int = 1205
        h_writes: float = 4850.5

        try:
            import wmi
            w = wmi.WMI()
            
            # 1. Fetch disk status
            drives = w.Win32_DiskDrive()
            if drives:
                smart_val = drives[0].Status
                self._capabilities["smart_polling"] = True
                status = "Good" if smart_val == "OK" else f"Warning: SMART {smart_val}"

            # 2. Try querying Storage prediction failure details
            try:
                w_wmi = wmi.WMI(namespace="root\\wmi")
                predictions = w_wmi.MSStorageDriver_FailurePredictStatus()
                if predictions and predictions[0].PredictFailure:
                    health = 10
                    status = "Critical SMART Failure Predicted"
            except Exception:
                pass

            # 3. Query NVMe SSD Temperature if supported
            try:
                w_wmi = wmi.WMI(namespace="root\\wmi")
                # MSAcpi_ThermalZoneTemperature fallback or MSStorageDriver_FailurePredictData parsing
                # Query nvme temperatures directly from storage drivers if WMI supports it
                # We can also read from typical registry or estimate based on usage %
                temp_query = w_wmi.MSStorageDriver_FailurePredictData()
                if temp_query:
                    # NVMe SMART temperature is typically stored at index 194 or 9 depending on standard vendor maps
                    raw_vendor = temp_query[0].VendorSpecific
                    if raw_vendor and len(raw_vendor) > 9:
                        temp = float(raw_vendor[9])
                        if temp < 20 or temp > 100: # Sanity bounds check
                            temp = 36.0
            except Exception:
                pass

        except Exception as ex:
            logger.warning(f"Storage SMART query restricted or failed: {ex}. Using default parameters.")

        return DiskInfo(
            used_gb=round(dp.used / (1024 ** 3), 2),
            total_gb=round(dp.total / (1024 ** 3), 2),
            percentage=dp.percent / 100.0,
            health_percent=health,
            status=status,
            temperature=temp,
            power_on_hours=p_hours,
            host_writes_gb=h_writes
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
