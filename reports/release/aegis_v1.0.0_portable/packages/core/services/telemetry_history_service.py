"""Telemetry history service recording system usage parameters and delegating database logs to TelemetryRepository."""

import time
from pathlib import Path
from typing import Optional
from packages.core.container import ServiceContainer
from packages.core.models.telemetry import TelemetryReport
from packages.core.repositories.telemetry_repository import TelemetryRepository
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class TelemetryHistoryService:
    """Manages telemetry historical log records and calls TelemetryRepository."""

    def __init__(self, container: ServiceContainer, repository: TelemetryRepository) -> None:
        """Initialize the Telemetry History Service.
        
        Args:
            container: DI Service container reference.
            repository: Isolated TelemetryRepository database instance.
        """
        self.container = container
        self.repository = repository
        logger.info("Telemetry History Service initialized using repository layer.")

    def log_telemetry(self, report: TelemetryReport) -> None:
        """Parses TelemetryReport data and inserts it into database via repository.
        
        Args:
            report: The active TelemetryReport to parse and store.
        """
        try:
            power_plan = "Balanced"
            try:
                opt_svc = self.container.get("optimization_service")
                state = opt_svc.capture_current_state()
                power_plan = state.get("power_plan", "Balanced")
            except Exception:
                pass

            record = {
                "timestamp": time.time(),
                "cpu_utilization": report.cpu.utilization,
                "cpu_temperature": report.cpu.temperature,
                "ram_percentage": report.ram.percentage,
                "disk_health_percent": report.disk.health_percent,
                "battery_health_percent": report.battery.health_percent,
                "network_latency_ms": report.network_latency_ms,
                "health_score": report.health_score,
                "active_power_plan": power_plan
            }
            self.repository.save(record)
            logger.debug("Telemetry record logged successfully via repository.")
        except Exception as ex:
            logger.error(f"TelemetryHistoryService failed to log record: {ex}")

    def get_history(self, limit_hours: int = 168) -> list[dict]:
        """Queries telemetry logs for the last N hours.
        
        Args:
            limit_hours: Hours range filter. Default is 168 (7 days).
            
        Returns:
            List of telemetry records formatted as dictionaries.
        """
        cutoff_time = time.time() - (limit_hours * 3600)
        return self.repository.fetch_range(cutoff_time)

    def clean_old_records(self, days: int = 7) -> int:
        """Deletes telemetry log rows older than N days.
        
        Args:
            days: Max age threshold. Default is 7 days.
            
        Returns:
            Number of deleted records.
        """
        cutoff_time = time.time() - (days * 24 * 3600)
        deleted = self.repository.delete_older_than(cutoff_time)
        if deleted > 0:
            logger.info(f"Purged {deleted} telemetry history records older than {days} days.")
        return deleted
