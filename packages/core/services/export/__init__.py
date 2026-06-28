"""Export Service context facade leveraging strategy patterns to write telemetry reports."""

from pathlib import Path
from packages.core.logger import get_subsystem_logger
from packages.core.services.export.strategies import (
    ExportStrategy, CSVExportStrategy, JSONExportStrategy, MarkdownExportStrategy, HTMLExportStrategy
)

from packages.core.constants.paths import APPDATA_DIR

logger = get_subsystem_logger("SYSTEM")


class ExportService:
    """Manages format strategy resolution and writes target documents to reports/diagnostics/."""

    def __init__(self) -> None:
        """Initialize the Export Service."""
        self.diagnostics_dir = APPDATA_DIR / "reports" / "diagnostics"
        self.diagnostics_dir.mkdir(parents=True, exist_ok=True)
        
        # Registry strategies map
        self._strategies: dict[str, ExportStrategy] = {
            "csv": CSVExportStrategy(),
            "json": JSONExportStrategy(),
            "md": MarkdownExportStrategy(),
            "html": HTMLExportStrategy()
        }
        logger.info("Strategy Pattern Export Service initialized.")

    def export_data(self, format_name: str, data: list[dict], filename: str) -> Path:
        """Resolves target strategy and formats historical data to target output path.
        
        Args:
            format_name: Target format format token (csv/json/md/html).
            data: Historical telemetry records list.
            filename: Target output file name.
            
        Returns:
            The formatted output Path object.
        """
        fmt_lower = format_name.lower().strip()
        strategy = self._strategies.get(fmt_lower)
        if not strategy:
            logger.error(f"Strategy resolution failed. Format '{fmt_lower}' is not supported.")
            raise ValueError(f"Unsupported export format strategy: '{fmt_lower}'")

        dest_file = self.diagnostics_dir / filename
        out_path = strategy.export(data, dest_file)
        logger.info(f"Telemetry history exported via {strategy.__class__.__name__} to: {out_path.name}")
        return out_path
