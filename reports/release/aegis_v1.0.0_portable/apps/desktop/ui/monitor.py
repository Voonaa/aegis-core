"""Monitor Page — deep live charts view for Aegis Core Platform."""

import customtkinter as ctk
import packages.core.constants.events as events
from apps.desktop.ui.base_page import BasePage
from apps.desktop.ui.theme import ThemeManager
from apps.desktop.ui.widgets import LiveChart
from packages.core.models.telemetry import TelemetryReport
from packages.core.container import ServiceContainer
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class MonitorPage(BasePage):
    """Full-viewport live chart monitor — four independent sensor trend charts."""

    def __init__(self, master: any, theme: ThemeManager) -> None:
        """Initialize the Monitor Page.

        Args:
            master: Viewport router parent frame.
            theme: Active style theme manager.
        """
        super().__init__(master=master)
        self.theme = theme

        container = ServiceContainer()
        self.event_bus = container.get("event_bus")

        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Charts grid
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_charts()

    def _build_header(self) -> None:
        """Render page header."""
        spacing_xl = self.theme.get_spacing("spacing_xl")
        spacing_md = self.theme.get_spacing("spacing_md")

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=spacing_xl, pady=(spacing_xl, spacing_md), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="LIVE SYSTEM MONITOR",
            font=self.theme.get_font("font_size_lg", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Real-time performance telemetry — all sensor readings",
            font=self.theme.get_font("font_size_md"),
            text_color=self.theme.get_color("text_muted")
        )
        subtitle.grid(row=1, column=0, sticky="w")

    def _build_charts(self) -> None:
        """Render 2x2 full-size live chart grid."""
        spacing_xl = self.theme.get_spacing("spacing_xl")
        spacing_sm = self.theme.get_spacing("spacing_sm")

        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.grid(row=1, column=0, padx=spacing_xl, pady=(0, spacing_xl), sticky="nsew")
        charts_frame.grid_rowconfigure((0, 1), weight=1)
        charts_frame.grid_columnconfigure((0, 1), weight=1)

        self.cpu_chart = LiveChart(charts_frame, self.theme, "CPU Utilization (%)", max_points=60)
        self.cpu_chart.grid(row=0, column=0, padx=(0, spacing_sm), pady=(0, spacing_sm), sticky="nsew")

        self.ram_chart = LiveChart(charts_frame, self.theme, "RAM Usage (%)", max_points=60)
        self.ram_chart.grid(row=0, column=1, padx=(spacing_sm, 0), pady=(0, spacing_sm), sticky="nsew")

        self.temp_chart = LiveChart(charts_frame, self.theme, "CPU Core Temperature (°C)", max_points=60)
        self.temp_chart.grid(row=1, column=0, padx=(0, spacing_sm), pady=(spacing_sm, 0), sticky="nsew")

        self.net_chart = LiveChart(charts_frame, self.theme, "Gateway Latency (ms)", max_points=60)
        self.net_chart.grid(row=1, column=1, padx=(spacing_sm, 0), pady=(spacing_sm, 0), sticky="nsew")

    def on_resume(self) -> None:
        """Subscribe to telemetry events when page becomes active."""
        logger.info("MonitorPage: Subscribing to telemetry EventBus.")
        self.event_bus.subscribe(events.TELEMETRY_UPDATED, self._on_telemetry_received)

    def on_pause(self) -> None:
        """Unsubscribe from telemetry events when page is hidden."""
        logger.info("MonitorPage: Unsubscribing from telemetry EventBus.")
        self.event_bus.unsubscribe(events.TELEMETRY_UPDATED, self._on_telemetry_received)

    def _on_telemetry_received(self, report: TelemetryReport) -> None:
        """Update all 4 live charts from incoming telemetry report.

        Args:
            report: Mapped TelemetryReport payload.
        """
        self.cpu_chart.add_point(report.cpu.utilization)
        self.ram_chart.add_point(report.ram.percentage * 100.0)
        self.temp_chart.add_point(report.cpu.temperature)
        self.net_chart.add_point(report.network_latency_ms)
