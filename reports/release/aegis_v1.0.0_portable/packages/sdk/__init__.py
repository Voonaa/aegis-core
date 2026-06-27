"""Aegis Core SDK public API entry point."""

from packages.core.container import ServiceContainer
from packages.sdk.hardware import HardwareSDK
from packages.sdk.repair import RepairSDK
from packages.sdk.report import ReportSDK

class AegisSDK:
    """Unified entry point exposing Aegis Core logic for GUI, CLI, and plugins."""

    def __init__(self) -> None:
        """Initialize the Aegis SDK by resolving the Service Container."""
        self._container = ServiceContainer()
        self.hardware = HardwareSDK(self._container)
        self.repair = RepairSDK(self._container)
        self.report = ReportSDK(self._container)

    @property
    def version(self) -> str:
        """Returns the current Aegis Core platform version."""
        config = self._container.get("config")
        return str(config.get("version", "0.3.0"))
