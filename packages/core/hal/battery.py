"""Battery telemetry harvester module for Aegis HAL."""

import psutil
from packages.core.models.telemetry import BatteryInfo
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("HARDWARE")

class BatteryComponent:
    """Battery telemetry module querying WMI classes for design limits and health indexes."""

    def __init__(self) -> None:
        """Initialize the Battery Component."""
        self._capabilities = {
            "battery_present": False,
            "wear_polling": False
        }
        # Check if battery is physically wired
        battery = psutil.sensors_battery()
        if battery is not None:
            self._capabilities["battery_present"] = True

    def query(self) -> BatteryInfo:
        """Queries battery charge ratios and wear indices.
        
        Returns:
            BatteryInfo dataclass mappings.
        """
        if not self._capabilities["battery_present"]:
            # Desktop fallback default
            return BatteryInfo(
                percentage=100,
                is_charging=True,
                health_percent=100,
                time_remaining_mins=-1
            )

        # Query basic charge status via psutil
        battery = psutil.sensors_battery()
        percent: int = int(battery.percent) if battery else 100
        charging: bool = battery.power_plugged if battery else True
        secs_left: int = int(battery.secsleft) if battery else -1
        mins_remaining = int(secs_left // 60) if secs_left > 0 else -1

        # Query detailed health attributes via WMI
        health: int = 100
        try:
            import wmi
            w = wmi.WMI()
            batteries = w.Win32_Battery()
            if batteries and len(batteries) > 0:
                self._capabilities["wear_polling"] = True
                b = batteries[0]
                
                # Check design vs actual full charge capacity
                # If namespaces map, compute: (FullChargeCapacity / DesignCapacity) * 100
                design = getattr(b, "DesignCapacity", None)
                full = getattr(b, "FullChargeCapacity", None)
                if design and full and design > 0:
                    health = int(min(100, (full / design) * 100.0))
        except Exception as ex:
            logger.warning(f"Battery WMI details query failed or restricted: {ex}. Using default health metrics.")

        return BatteryInfo(
            percentage=percent,
            is_charging=charging,
            health_percent=health,
            time_remaining_mins=mins_remaining
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
