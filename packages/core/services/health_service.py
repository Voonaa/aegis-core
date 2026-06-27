"""Weighted health scoring service for Aegis Toolkit."""

from packages.core.models.telemetry import TelemetryReport
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class HealthService:
    """Calculates overall host system Health Score based on component telemetry metrics."""

    def __init__(self) -> None:
        """Initialize the Health Service."""
        logger.info("Health Service initialized.")

    def calculate_score(
        self,
        cpu_util: float,
        cpu_temp: float,
        ram_percent: float,
        disk_health: int,
        battery_health: int,
        virt_conflict: bool
    ) -> int:
        """Calculates system health rating index [0 - 100] using weighted rules.
        
        Args:
            cpu_util: CPU utilization percentage.
            cpu_temp: CPU thermal reading (Celsius).
            ram_percent: RAM usage fraction [0.0 - 1.0].
            disk_health: SSD SMART health wear percentage.
            battery_health: Battery charge degradation health score.
            virt_conflict: Boolean flag indicating virtualization configurations clash.
            
        Returns:
            Calculated health score scale [0 - 100].
        """
        # 1. Storage component (Max 20 points)
        s_storage = round((disk_health / 100.0) * 20.0)

        # 2. Battery component (Max 20 points)
        s_battery = round((battery_health / 100.0) * 20.0)

        # 3. Thermal component (Max 20 points)
        # Deduct 0.5 points per 1C over 65C
        if cpu_temp <= 65.0:
            s_thermal = 20.0
        else:
            s_thermal = max(0.0, 20.0 - ((cpu_temp - 65.0) * 0.5))
        s_thermal = round(s_thermal)

        # 4. Memory component (Max 20 points)
        # Deduct 1.0 point per 1% usage over 80%
        ram_percentage = ram_percent * 100.0
        if ram_percentage <= 80.0:
            s_memory = 20.0
        else:
            s_memory = max(0.0, 20.0 - (ram_percentage - 80.0))
        s_memory = round(s_memory)

        # 5. OS Integrity component (Max 20 points)
        s_os = 20
        if virt_conflict:
            s_os -= 10 # Deduct for conflict warnings

        # Total combined score sum
        total_score = s_storage + s_battery + s_thermal + s_memory + s_os
        logger.debug(
            f"Health calculated: Total={total_score} "
            f"(Disk={s_storage}, Bat={s_battery}, Temp={s_thermal}, RAM={s_memory}, OS={s_os})"
        )
        
        return int(max(0, min(100, total_score)))
