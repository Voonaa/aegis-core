"""System reports wrapper class for Aegis SDK."""

from packages.core.container import ServiceContainer
from packages.core.services.report_service import ReportService

class ReportSDK:
    """Interface to export system diagnostics reports in Markdown and JSON configurations."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Report SDK.
        
        Args:
            container: DI Service container reference.
        """
        self._container = container

    def generate(self) -> str:
        """Triggers compilation and writes system diagnostic reports.
        
        Returns:
            Success message detailing written paths.
        """
        rep_svc: ReportService = self._container.get("report_service")
        return rep_svc.generate_report()
