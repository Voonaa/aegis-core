"""Rules-based Recommendation Engine for Aegis Toolkit."""

from packages.core.models.telemetry import TelemetryReport
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class RecommendationService:
    """Matches live system parameters against threshold rules to generate recommendations."""

    def __init__(self) -> None:
        """Initialize the Recommendation Service."""
        logger.info("Recommendation Service initialized.")

    def get_recommendations(self, report: TelemetryReport) -> list[dict]:
        """Runs rule matching on the provided TelemetryReport.
        
        Args:
            report: Mapped TelemetryReport payload.
            
        Returns:
            List of optimization advice dictionaries.
        """
        advices = []

        # Rule 1: Virtualization conflicts
        if report.os.virtualization_conflict:
            advices.append({
                "title": "Nested Virtualization Conflict",
                "priority": "HIGH",
                "action_message": "Nested Hyper-V instances are active inside a virtual environment. Consider disabling hypervisor services if you encounter BSOD crashes during gaming."
            })

        # Rule 2: High thermals
        if report.cpu.temperature > 75.0:
            advices.append({
                "title": "High Processor Thermals",
                "priority": "HIGH",
                "action_message": "CPU temperature exceeded 75°C. Clean laptop fan exhaust vents or limit active background processing load."
            })
        elif report.cpu.temperature > 65.0:
            advices.append({
                "title": "Elevated Core Temperature",
                "priority": "NORMAL",
                "action_message": "CPU core temperature is slightly elevated. Verify laptop bottom vents are not obstructed."
            })

        # Rule 3: Storage write degradation
        if report.disk.health_percent < 80:
            advices.append({
                "title": "SSD Health Wear Alert",
                "priority": "HIGH",
                "action_message": "Solid State Drive health dropped below 80%. Perform regular data backups to prevent file loss."
            })

        # Rule 4: Battery wear
        if report.battery.health_percent < 80:
            advices.append({
                "title": "Battery Degradation Detected",
                "priority": "NORMAL",
                "action_message": "Battery capacity is under 80% of original design limits. Limit gaming on battery power."
            })

        # Rule 5: RAM usage bottlenecks
        if report.ram.percentage > 0.85:
            advices.append({
                "title": "High Memory Utilization",
                "priority": "NORMAL",
                "action_message": "RAM usage is critical (above 85%). Close unnecessary background apps or web browser tabs."
            })

        # Default fallback if all checks pass
        if not advices:
            advices.append({
                "title": "System Parameters Healthy",
                "priority": "LOW",
                "action_message": "All Aegis telemetry indicators report normal, healthy host operation boundaries."
            })

        logger.debug(f"Recommendation Engine compiled {len(advices)} advice items.")
        return advices
