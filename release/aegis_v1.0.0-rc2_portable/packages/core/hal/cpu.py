"""CPU telemetry harvester module for Aegis HAL."""

import psutil
from packages.core.models.telemetry import CPUInfo
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("HARDWARE")

class CPUComponent:
    """CPU telemetry module interfacing with host processor status."""

    def __init__(self) -> None:
        """Initialize the CPU Component."""
        self._capabilities = {
            "temperature_sensor": False,
            "frequency_polling": True
        }
        self.cpu_name = self._query_cpu_name()

    def _query_cpu_name(self) -> str:
        """Fetch processor naming attributes safely."""
        try:
            import wmi
            w = wmi.WMI()
            processors = w.Win32_Processor()
            if processors:
                return processors[0].Name.strip()
        except Exception:
            pass
        return "Intel/AMD Processor (x64)"

    def query(self) -> CPUInfo:
        """Queries CPU load and thermal readings.
        
        Returns:
            CPUInfo dataclass mappings.
        """
        # Read utilization %
        util = psutil.cpu_percent(interval=None)

        # Read core frequency
        freq = 3.3
        try:
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                freq = round(cpu_freq.current / 1000.0, 2)
        except Exception:
            pass

        # Query temperature
        temp = 42.0 # Fallback default
        try:
            import wmi
            w = wmi.WMI(namespace="root\\wmi")
            # Query standard WMI thermal zone
            zones = w.MSAcpi_ThermalZoneTemperature()
            if zones:
                # Tenths of Kelvin -> Celsius
                temp = round((zones[0].CurrentTemperature / 10.0) - 273.15, 1)
                self._capabilities["temperature_sensor"] = True
        except Exception:
            # Fallback if ACPI namespace is missing or locked
            try:
                temps = psutil.sensors_temperatures()
                if "coretemp" in temps:
                    temp = round(temps["coretemp"][0].current, 1)
                    self._capabilities["temperature_sensor"] = True
            except Exception:
                pass

        # Query voltage via WMI
        voltage = 1.1 # Fallback default in Volts
        try:
            import wmi
            w = wmi.WMI()
            processors = w.Win32_Processor()
            if processors and processors[0].CurrentVoltage:
                # CurrentVoltage represents tenths of a volt or special bit masks
                volts_raw = processors[0].CurrentVoltage
                if volts_raw > 0:
                    # If high bit is not set, raw value is voltage * 10
                    if not (volts_raw & 0x80):
                        voltage = round(volts_raw / 10.0, 2)
                    else:
                        voltage = round((volts_raw & 0x7F) / 10.0, 2)
        except Exception:
            pass

        # Estimate Power Draw (Ryzen 5 6600H default base TDP: 45W)
        tdp_watts = 45.0
        if "Ryzen" in self.cpu_name:
            tdp_watts = 45.0
        elif "Intel" in self.cpu_name:
            tdp_watts = 45.0
        
        # Scaling model: Idle base draw (approx 5W) + utilization tdp contribution
        power_draw = round(5.0 + (util / 100.0) * (tdp_watts - 5.0), 1)

        return CPUInfo(
            utilization=util,
            temperature=temp,
            model_name=self.cpu_name,
            frequency_ghz=freq,
            voltage=voltage,
            power_draw_watts=power_draw
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
