"""Unified Service Registry bootstrap helper.

Instantiates and registers all core, HAL, and telemetry diagnostics services
into the Aegis ServiceContainer dependency injection shell.
"""

from pathlib import Path
from packages.core.container import ServiceContainer
from packages.core.config_manager import ConfigManager
from apps.desktop.ui.theme import ThemeManager
from packages.core.services.privilege_service import PrivilegeService
from packages.core.event_bus import EventBus
from packages.core.jobs import JobManager
from packages.core.services.repair_service import RepairService
from packages.core.services.maintenance_service import MaintenanceService
from packages.core.services.health_service import HealthService as HealthEngine
from packages.core.profile_manager import ProfileManager
from packages.core.services.recommendation import RecommendationService
from packages.core.plugins.loader import PluginLoader
from packages.core.command_registry import CommandRegistry
from packages.core.services.report_service import ReportService
from packages.core.services.hardware_service import HardwareService
from packages.core.services.windows_intelligence import WindowsIntelligenceService
from packages.core.services.optimization import OptimizationService
from packages.core.repositories.telemetry_repository import TelemetryRepository
from packages.core.services.telemetry_history_service import TelemetryHistoryService
from packages.core.services.export import ExportService
from packages.core.services.trend_analysis import TrendAnalysisService


def bootstrap_services(
    container: ServiceContainer,
    profiles_dir: Path,
    plugins_dir: Path,
    config_file: Path,
    default_settings: dict
) -> None:
    """Instantiates and registers all system services into the container.
    
    Args:
        container: The ServiceContainer instance to register services on.
        profiles_dir: Path to directory containing hardware profile overlays.
        plugins_dir: Path to directory containing runtime plugins.
        config_file: Path to settings JSON configuration file.
        default_settings: Default fallback configuration values dictionary.
    """
    # 1. Initialize & Register ConfigManager
    config_mgr = ConfigManager(config_path=config_file, default_settings=default_settings)
    container.register("config", config_mgr)

    # 2. Initialize & Register ThemeManager
    theme_mgr = ThemeManager()
    container.register("theme", theme_mgr)

    # 3. Initialize & Register PrivilegeService
    privilege_service = PrivilegeService()
    container.register("privilege_service", privilege_service)

    # 4. Initialize & Register EventBus
    event_bus = EventBus()
    container.register("event_bus", event_bus)

    # 5. Initialize & Register JobManager
    job_manager = JobManager(container=container)
    container.register("job_manager", job_manager)

    # 6. Initialize & Register RepairService
    repair_service = RepairService(container=container)
    container.register("repair_service", repair_service)

    # 7. Initialize & Register MaintenanceService
    maintenance_service = MaintenanceService(container=container)
    container.register("maintenance_service", maintenance_service)

    # 8. Initialize & Register HealthEngine
    health_engine = HealthEngine()
    container.register("health_engine", health_engine)

    # 9. Initialize & Register ProfileManager
    profile_manager = ProfileManager(profiles_dir=profiles_dir)
    container.register("profile_mgr", profile_manager)

    # 10. Initialize & Register RecommendationService
    recommendation_service = RecommendationService()
    container.register("recommendation_service", recommendation_service)

    # 11. Initialize & Register PluginLoader
    plugin_loader = PluginLoader(plugins_dir=plugins_dir)
    container.register("plugin_loader", plugin_loader)

    # 12. Initialize & Register CommandRegistry
    cmd_registry = CommandRegistry()
    container.register("command_registry", cmd_registry)

    # 13. Initialize & Register ReportService
    report_service = ReportService(container=container)
    container.register("report_service", report_service)

    # 14. Initialize & Register HardwareService
    demo_mode = config_mgr.get("demo_mode", True)
    hardware_service = HardwareService(container=container, demo_mode=demo_mode)
    container.register("hardware_service", hardware_service)

    # 15. Initialize & Register WindowsIntelligenceService
    intelligence_service = WindowsIntelligenceService()
    container.register("intelligence_service", intelligence_service)

    # 16. Initialize & Register OptimizationService
    optimization_service = OptimizationService(container=container)
    container.register("optimization_service", optimization_service)

    # 17. Initialize & Register SQLite TelemetryRepository
    project_root = config_file.resolve().parent.parent.parent
    db_path = project_root / "apps" / "desktop" / "config" / "telemetry_history.db"
    telemetry_repo = TelemetryRepository(db_path=db_path)
    container.register("telemetry_repository", telemetry_repo)

    # 18. Initialize & Register TelemetryHistoryService
    telemetry_history_service = TelemetryHistoryService(container=container, repository=telemetry_repo)
    container.register("telemetry_history_service", telemetry_history_service)

    # 19. Initialize & Register ExportService
    export_service = ExportService()
    container.register("export_service", export_service)

    # 20. Initialize & Register TrendAnalysisService
    trend_analysis_service = TrendAnalysisService(container=container)
    container.register("trend_analysis_service", trend_analysis_service)

    # Trigger 7-day rolling history database cleanup on startup
    telemetry_history_service.clean_old_records(days=7)

    # Subscribe to TELEMETRY_UPDATED to record state into SQLite history database
    from packages.core.constants import events
    event_bus.subscribe(events.TELEMETRY_UPDATED, telemetry_history_service.log_telemetry)
