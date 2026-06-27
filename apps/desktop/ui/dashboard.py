"""Dashboard frame displaying telemetry widgets and metrics for Aegis Core Platform."""

import customtkinter as ctk
import packages.core.constants.events as events
from apps.desktop.ui.base_page import BasePage
from apps.desktop.ui.theme import ThemeManager
from apps.desktop.ui.widgets import MetricCard, ProgressBarCard, StatusBadge
from packages.core.models.telemetry import TelemetryReport
from packages.core.container import ServiceContainer
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class DashboardPage(BasePage):
    """Dashboard view layout rendering telemetry gauges and health indicators."""

    def __init__(self, master: any, theme: ThemeManager) -> None:
        """Initialize the Dashboard Page.
        
        Args:
            master: Viewport router parent frame.
            theme: Active style theme manager.
        """
        super().__init__(master=master)
        self.theme = theme

        # Fetch EventBus from Singleton Container
        container = ServiceContainer()
        self.event_bus = container.get("event_bus")

        # Main viewport layouts config
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Grid telemetry cards
        self.grid_rowconfigure(2, weight=1)  # Charts / performance graphics
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_telemetry_grid()
        self._build_performance_chart()

    def _build_header(self) -> None:
        """Render page header and profile indicator strings."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=spacing_xl, pady=(spacing_xl, spacing_md), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_lbl = ctk.CTkLabel(
            header_frame,
            text="DASHBOARD TELEMETRY",
            font=self.theme.get_font("font_size_lg", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        title_lbl.grid(row=0, column=0, sticky="w")

        self.info_lbl = ctk.CTkLabel(
            header_frame,
            text="PROFILE: GENERIC WINDOWS DEVICE | HEALTH: 100/100",
            font=self.theme.get_font("font_size_sm", "bold"),
            text_color=self.theme.get_color("accent_primary"),
            fg_color=self.theme.get_color("bg_sidebar"),
            corner_radius=self.theme.get_radius("corner_radius_sm"),
            padx=spacing_sm,
            pady=spacing_xs
        )
        self.info_lbl.grid(row=0, column=1, sticky="e")

    def _build_telemetry_grid(self) -> None:
        """Draw CPU, RAM, Disk, Temperature, and Battery metrics cards."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.grid(row=1, column=0, padx=spacing_xl, pady=0, sticky="ew")
        grid_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # CPU Card
        self.cpu_card = MetricCard(
            master=grid_frame,
            theme=self.theme,
            title="Processor (CPU)",
            value="N/A",
            subtitle="Detecting..."
        )
        self.cpu_card.grid(row=0, column=0, padx=(0, spacing_sm), pady=spacing_sm, sticky="nsew")

        # RAM Card (Progress bar)
        self.ram_card = ProgressBarCard(
            master=grid_frame,
            theme=self.theme,
            title="Memory (RAM)",
            value="N/A",
            percentage=0.0
        )
        self.ram_card.grid(row=0, column=1, padx=spacing_xs, pady=spacing_sm, sticky="nsew")

        # Battery Card
        self.battery_card = MetricCard(
            master=grid_frame,
            theme=self.theme,
            title="Battery Status",
            value="N/A",
            subtitle="Detecting..."
        )
        self.battery_card.grid(row=0, column=2, padx=(spacing_sm, 0), pady=spacing_sm, sticky="nsew")

    def _build_performance_chart(self) -> None:
        """Render status indicators and dummy graph frames."""
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_lg = self.theme.get_spacing("spacing_lg")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        chart_frame = ctk.CTkFrame(
            self,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        chart_frame.grid(row=2, column=0, padx=spacing_xl, pady=spacing_lg, sticky="nsew")
        
        chart_frame.grid_rowconfigure(0, weight=0) # Badge headers
        chart_frame.grid_rowconfigure(1, weight=1) # Graphic body
        chart_frame.grid_columnconfigure(0, weight=1)

        # Status Badge bar at top
        status_bar = ctk.CTkFrame(chart_frame, fg_color="transparent")
        status_bar.grid(row=0, column=0, padx=spacing_lg, pady=spacing_md, sticky="ew")

        # Status metrics
        self.status_ssd = StatusBadge(status_bar, self.theme, "SSD: Good", "success")
        self.status_ssd.pack(side="left", padx=spacing_lg)

        self.status_net = StatusBadge(status_bar, self.theme, "Internet: Connected", "success")
        self.status_net.pack(side="left", padx=spacing_lg)

        self.status_hyperv = StatusBadge(status_bar, self.theme, "Hyper-V: Active", "warning")
        self.status_hyperv.pack(side="left", padx=spacing_lg)

        self.status_driver = StatusBadge(status_bar, self.theme, "Drivers: Verified", "success")
        self.status_driver.pack(side="left", padx=spacing_lg)

        # Dynamic graph placeholder frame
        graph_placeholder = ctk.CTkFrame(chart_frame, fg_color=self.theme.get_color("bg_primary"), corner_radius=self.theme.get_radius("corner_radius_md"))
        graph_placeholder.grid(row=1, column=0, padx=spacing_lg, pady=(0, spacing_lg), sticky="nsew")
        
        # Center title message inside graph area
        graph_lbl = ctk.CTkLabel(
            graph_placeholder,
            text="[ Telemetry chart graphics canvas - Active in Sprint 3 ]",
            font=self.theme.get_font("font_size_md"),
            text_color=self.theme.get_color("text_muted")
        )
        graph_lbl.pack(expand=True)

    def on_resume(self) -> None:
        """Resumes telemetry update timers. Subscribes to telemetry events."""
        logger.info("DashboardPage: Subscribing to EventBus telemetry updates.")
        self.event_bus.subscribe(events.TELEMETRY_UPDATED, self._on_telemetry_received)

    def on_pause(self) -> None:
        """Pauses telemetry update timers. Unsubscribes from events."""
        logger.info("DashboardPage: Unsubscribing from EventBus telemetry updates.")
        self.event_bus.unsubscribe(events.TELEMETRY_UPDATED, self._on_telemetry_received)

    def _on_telemetry_received(self, report: TelemetryReport) -> None:
        """Callback triggered when the Hardware telemetry service publishes updates.
        
        Args:
            report: Mapped TelemetryReport payload.
        """
        # 1. Update CPU Card
        self.cpu_card.update_value(
            new_value=f"{report.cpu.utilization:.1f} %",
            new_subtitle=f"{report.cpu.temperature:.1f}°C | {report.cpu.frequency_ghz:.2f} GHz"
        )
        
        # 2. Update RAM Card
        self.ram_card.update_progress(
            new_value=f"{report.ram.used_gb:.1f} / {report.ram.total_gb:.1f} GB",
            percentage=report.ram.percentage
        )

        # 3. Update Battery Card
        charge_str = "Charging" if report.battery.is_charging else "Discharging"
        self.battery_card.update_value(
            new_value=f"{report.battery.percentage} %",
            new_subtitle=f"{charge_str} | Wear: {100 - report.battery.health_percent}%"
        )

        # 4. Update Status Badges
        self.status_ssd.update_status("success" if report.disk.status == "Good" else "danger")
        
        # Hyper-V virtualization conflict LED toggle
        if report.os.virtualization_conflict:
            self.status_hyperv.update_status("danger")
            self.status_hyperv.label.configure(text="Hyper-V: Conflict Warning")
        else:
            self.status_hyperv.update_status("success" if report.os.hyperv_active else "warning")
            self.status_hyperv.label.configure(text=f"Hyper-V: {'On' if report.os.hyperv_active else 'Off'}")

        # Update Header Profile name
        self.info_lbl.configure(text=f"PROFILE: {report.os.os_name.upper()} | HEALTH: {report.health_score}/100")
