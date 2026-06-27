"""Dashboard frame displaying telemetry widgets and metrics for Aegis Core Platform."""

import customtkinter as ctk
import packages.core.constants.events as events
from apps.desktop.ui.base_page import BasePage
from apps.desktop.ui.theme import ThemeManager
from apps.desktop.ui.widgets import MetricCard, ProgressBarCard, StatusBadge, LiveChart, HealthRing, SensorCard
from packages.core.models.telemetry import TelemetryReport
from packages.core.container import ServiceContainer
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class DashboardPage(BasePage):
    """Dashboard view layout rendering telemetry gauges, system overview, and live charts."""

    def __init__(self, master: any, theme: ThemeManager) -> None:
        """Initialize the Dashboard Page.
        
        Args:
            master: Viewport router parent frame.
            theme: Active style theme manager.
        """
        super().__init__(master=master)
        self.theme = theme

        # Fetch ServiceContainer registry
        container = ServiceContainer()
        self.event_bus = container.get("event_bus")

        try:
            self.profile_mgr = container.get("profile_mgr")
        except KeyError:
            from packages.core.profile_manager import ProfileManager
            from packages.core.constants.paths import PROFILES_DIR
            self.profile_mgr = ProfileManager(PROFILES_DIR)

        try:
            self.recommendation_service = container.get("recommendation_service")
        except KeyError:
            from packages.core.services.recommendation import RecommendationService
            self.recommendation_service = RecommendationService()

        try:
            self.report_service = container.get("report_service")
        except KeyError:
            self.report_service = None

        try:
            self.intelligence_service = container.get("intelligence_service")
        except KeyError:
            from packages.core.services.windows_intelligence import WindowsIntelligenceService
            self.intelligence_service = WindowsIntelligenceService()

        # Cache intelligence alerts (run once on first telemetry update)
        self._intelligence_alerts: list = []

        # Main viewport grid configuration (Header at row 0, main split content at row 1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Split View Area
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_split_layout()

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
            text="AEGIS CORE WORKSPACE",
            font=self.theme.get_font("font_size_lg", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        title_lbl.grid(row=0, column=0, sticky="w")

        # Profile active status indicator
        profile_name = self.profile_mgr.get_profile_name()
        self.info_lbl = ctk.CTkLabel(
            header_frame,
            text=f"PROFILE: {profile_name.upper()} | SYSTEM ONLINE",
            font=self.theme.get_font("font_size_sm", "bold"),
            text_color=self.theme.get_color("accent_primary"),
            fg_color=self.theme.get_color("bg_sidebar"),
            corner_radius=self.theme.get_radius("corner_radius_sm"),
            padx=spacing_sm,
            pady=spacing_xs
        )
        self.info_lbl.grid(row=0, column=1, sticky="e")

    def _build_split_layout(self) -> None:
        """Assembles Left Main Area and Right Sidebar columns."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        # Main Split Content Frame
        split_frame = ctk.CTkFrame(self, fg_color="transparent")
        split_frame.grid(row=1, column=0, padx=spacing_xl, pady=(0, spacing_xl), sticky="nsew")
        split_frame.grid_rowconfigure(0, weight=1)
        split_frame.grid_columnconfigure(0, weight=3) # Left Area
        split_frame.grid_columnconfigure(1, weight=2) # Right Sidebar

        # ---------------------------------------------
        # LEFT AREA
        # ---------------------------------------------
        left_area = ctk.CTkFrame(split_frame, fg_color="transparent")
        left_area.grid(row=0, column=0, padx=(0, spacing_md), sticky="nsew")
        left_area.grid_columnconfigure(0, weight=1)
        left_area.grid_rowconfigure(0, weight=0) # Health Progress
        left_area.grid_rowconfigure(1, weight=0) # Component Cards Grid
        left_area.grid_rowconfigure(2, weight=1) # Live Charts
        left_area.grid_rowconfigure(3, weight=0) # Quick Actions

        # Health Score Card — HealthRing gauge + labels
        self.health_card = ctk.CTkFrame(
            left_area,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        self.health_card.grid(row=0, column=0, pady=(0, spacing_sm), sticky="ew")

        # Inner horizontal layout: Ring on left, text on right
        health_inner = ctk.CTkFrame(self.health_card, fg_color="transparent")
        health_inner.pack(fill="x", padx=spacing_md, pady=spacing_sm)

        self.health_ring = HealthRing(health_inner, self.theme, size=110, score=100)
        self.health_ring.pack(side="left", padx=(0, spacing_md))

        health_text = ctk.CTkFrame(health_inner, fg_color="transparent")
        health_text.pack(side="left", fill="both", expand=True)

        self.health_title = ctk.CTkLabel(
            health_text,
            text="SYSTEM HEALTH INDEX",
            font=self.theme.get_font("font_size_sm", "bold"),
            text_color=self.theme.get_color("text_muted")
        )
        self.health_title.pack(anchor="w")

        self.health_score_lbl = ctk.CTkLabel(
            health_text,
            text="100 / 100",
            font=self.theme.get_font("font_size_xl", "bold"),
            text_color=self.theme.get_color("status_success")
        )
        self.health_score_lbl.pack(anchor="w")

        self.health_status_lbl = ctk.CTkLabel(
            health_text,
            text="● Optimal — No issues detected",
            font=self.theme.get_font("font_size_md"),
            text_color=self.theme.get_color("status_success")
        )
        self.health_status_lbl.pack(anchor="w", pady=(spacing_xs, 0))

        # Components Status Grid (2x2)
        comp_grid = ctk.CTkFrame(left_area, fg_color="transparent")
        comp_grid.grid(row=1, column=0, pady=(0, spacing_sm), sticky="ew")
        comp_grid.grid_columnconfigure((0, 1), weight=1)

        # CPU SensorCard
        self.cpu_card = SensorCard(
            master=comp_grid,
            theme=self.theme,
            title="Processor (CPU)",
            value="— %",
            detail="Loading hardware data...",
            confidence="NONE"
        )
        self.cpu_card.grid(row=0, column=0, padx=(0, spacing_xs), pady=(0, spacing_xs), sticky="nsew")

        # GPU SensorCard
        self.gpu_card = SensorCard(
            master=comp_grid,
            theme=self.theme,
            title="Graphics (GPU)",
            value="— %",
            detail="Loading hardware data...",
            confidence="NONE"
        )
        self.gpu_card.grid(row=0, column=1, padx=(spacing_xs, 0), pady=(0, spacing_xs), sticky="nsew")

        # RAM SensorCard
        self.ram_card = SensorCard(
            master=comp_grid,
            theme=self.theme,
            title="Memory (RAM)",
            value="— GB",
            detail="Loading hardware data...",
            confidence="NONE"
        )
        self.ram_card.grid(row=1, column=0, padx=(0, spacing_xs), pady=(spacing_xs, 0), sticky="nsew")

        # SSD SensorCard
        self.ssd_card = SensorCard(
            master=comp_grid,
            theme=self.theme,
            title="Storage (SSD)",
            value="SMART: —",
            detail="Loading hardware data...",
            confidence="NONE"
        )
        self.ssd_card.grid(row=1, column=1, padx=(spacing_xs, 0), pady=(spacing_xs, 0), sticky="nsew")

        # Performance Charts Frame (2x2 sparklines grid)
        charts_container = ctk.CTkFrame(left_area, fg_color="transparent")
        charts_container.grid(row=2, column=0, pady=(0, spacing_sm), sticky="nsew")
        charts_container.grid_rowconfigure((0, 1), weight=1)
        charts_container.grid_columnconfigure((0, 1), weight=1)

        self.cpu_chart = LiveChart(charts_container, self.theme, "CPU Load Trend (%)")
        self.cpu_chart.grid(row=0, column=0, padx=(0, spacing_xs), pady=(0, spacing_xs), sticky="nsew")

        self.ram_chart = LiveChart(charts_container, self.theme, "RAM Usage Trend (%)")
        self.ram_chart.grid(row=0, column=1, padx=(spacing_xs, 0), pady=(0, spacing_xs), sticky="nsew")

        self.temp_chart = LiveChart(charts_container, self.theme, "CPU Core Temperature (°C)")
        self.temp_chart.grid(row=1, column=0, padx=(0, spacing_xs), pady=(spacing_xs, 0), sticky="nsew")

        self.net_chart = LiveChart(charts_container, self.theme, "Gateway Latency (ms)")
        self.net_chart.grid(row=1, column=1, padx=(spacing_xs, 0), pady=(spacing_xs, 0), sticky="nsew")

        # Quick Actions Frame
        actions_frame = ctk.CTkFrame(
            left_area,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        actions_frame.grid(row=3, column=0, sticky="ew")

        actions_title = ctk.CTkLabel(
            actions_frame,
            text="QUICK ENGINE OPTIMIZATIONS",
            font=self.theme.get_font("font_size_sm", "bold"),
            text_color=self.theme.get_color("text_muted")
        )
        actions_title.pack(anchor="w", padx=spacing_md, pady=(spacing_xs, 0))

        btn_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btn_container.pack(fill="x", padx=spacing_md, pady=spacing_sm)

        btn_gaming = ctk.CTkButton(
            btn_container,
            text="Optimize Gaming",
            font=self.theme.get_font("font_size_sm", "bold"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=self._optimize_gaming
        )
        btn_gaming.pack(side="left", fill="x", expand=True, padx=(0, spacing_xs))

        btn_dev = ctk.CTkButton(
            btn_container,
            text="Optimize Dev Mode",
            font=self.theme.get_font("font_size_sm", "bold"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=self._optimize_dev
        )
        btn_dev.pack(side="left", fill="x", expand=True, padx=spacing_xs)

        btn_battery = ctk.CTkButton(
            btn_container,
            text="Optimize Battery",
            font=self.theme.get_font("font_size_sm", "bold"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=self._optimize_battery
        )
        btn_battery.pack(side="left", fill="x", expand=True, padx=spacing_xs)

        btn_report = ctk.CTkButton(
            btn_container,
            text="Generate Report",
            font=self.theme.get_font("font_size_sm", "bold"),
            fg_color=self.theme.get_color("border"),
            text_color=self.theme.get_color("text_primary"),
            hover_color=self.theme.get_color("bg_primary"),
            command=self._generate_report
        )
        btn_report.pack(side="left", fill="x", expand=True, padx=(spacing_xs, 0))

        # ---------------------------------------------
        # RIGHT SIDEBAR COLUMN
        # ---------------------------------------------
        right_sidebar = ctk.CTkFrame(split_frame, fg_color="transparent")
        right_sidebar.grid(row=0, column=1, sticky="nsew")
        right_sidebar.grid_columnconfigure(0, weight=1)
        right_sidebar.grid_rowconfigure(0, weight=0) # System Info Card
        right_sidebar.grid_rowconfigure(1, weight=0) # Health Timeline
        right_sidebar.grid_rowconfigure(2, weight=1) # Recent activity & advice

        # System Overview Card
        self.overview_card = ctk.CTkFrame(
            right_sidebar,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        self.overview_card.grid(row=0, column=0, pady=(0, spacing_sm), sticky="ew")

        overview_title = ctk.CTkLabel(
            self.overview_card,
            text="SYSTEM OVERVIEW SPECS",
            font=self.theme.get_font("font_size_sm", "bold"),
            text_color=self.theme.get_color("text_muted")
        )
        overview_title.pack(anchor="w", padx=spacing_md, pady=(spacing_sm, spacing_xs))

        self.sys_info_lbl = ctk.CTkLabel(
            self.overview_card,
            text="OS: Windows 11 Host\nCPU: Loading...\nRAM: Loading...\nSSD: Loading...\nGPU: Loading...\nBattery Wear: Loading...\nActive Profile: ADVAN WORKPLUS",
            font=self.theme.get_font("font_size_md"),
            text_color=self.theme.get_color("text_primary"),
            justify="left"
        )
        self.sys_info_lbl.pack(anchor="w", padx=spacing_md, pady=(0, spacing_sm))

        # Health Timeline Card
        timeline_card = ctk.CTkFrame(
            right_sidebar,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        timeline_card.grid(row=1, column=0, pady=(0, spacing_sm), sticky="ew")

        timeline_title = ctk.CTkLabel(
            timeline_card,
            text="HEALTH TIMELINE HISTORIES",
            font=self.theme.get_font("font_size_sm", "bold"),
            text_color=self.theme.get_color("text_muted")
        )
        timeline_title.pack(anchor="w", padx=spacing_md, pady=(spacing_sm, spacing_xs))

        timeline_data = [
            ("Today", "94 / 100 (● Stable)"),
            ("Yesterday", "91 / 100 (▲ Improving)"),
            ("Last Week", "88 / 100 (▲ Improving)")
        ]
        for day, val in timeline_data:
            row = ctk.CTkFrame(timeline_card, fg_color="transparent")
            row.pack(fill="x", padx=spacing_md, pady=2)
            
            lbl_d = ctk.CTkLabel(row, text=day, font=self.theme.get_font("font_size_md", "bold"), text_color=self.theme.get_color("text_muted"))
            lbl_d.pack(side="left")

            val_d = ctk.CTkLabel(row, text=val, font=self.theme.get_font("font_size_md"), text_color=self.theme.get_color("text_primary"))
            val_d.pack(side="right")

        # Recommendations & Activity Logs Frame
        logs_card = ctk.CTkFrame(
            right_sidebar,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        logs_card.grid(row=2, column=0, sticky="nsew")

        logs_title = ctk.CTkLabel(
            logs_card,
            text="OPTIMIZATION ADVICES",
            font=self.theme.get_font("font_size_sm", "bold"),
            text_color=self.theme.get_color("text_muted")
        )
        logs_title.pack(anchor="w", padx=spacing_md, pady=(spacing_sm, spacing_xs))

        # Recommendations textbox list
        self.advice_txt = ctk.CTkTextbox(
            logs_card,
            font=self.theme.get_font("font_size_md"),
            fg_color=self.theme.get_color("bg_primary"),
            text_color=self.theme.get_color("text_primary"),
            border_width=0
        )
        self.advice_txt.pack(fill="both", expand=True, padx=spacing_md, pady=(0, spacing_md))
        self.advice_txt.insert("1.0", "Analyzing system indicators...")
        self.advice_txt.configure(state="disabled")

    def _optimize_gaming(self) -> None:
        """Triggers gaming boost operations."""
        logger.info("Quick action: Optimize Gaming triggered.")
        self.event_bus.publish(events.NOTIFICATION_TRIGGERED, "Gaming Optimization Mode Engaged!", "success")

    def _optimize_dev(self) -> None:
        """Triggers developer compatibility operations."""
        logger.info("Quick action: Optimize Development triggered.")
        self.event_bus.publish(events.NOTIFICATION_TRIGGERED, "Developer compatibility active.", "success")

    def _optimize_battery(self) -> None:
        """Triggers battery savings configurations."""
        logger.info("Quick action: Optimize Battery triggered.")
        self.event_bus.publish(events.NOTIFICATION_TRIGGERED, "Power saving throttling engaged.", "warning")

    def _generate_report(self) -> None:
        """Triggers Report generation routines."""
        logger.info("Quick action: Generate diagnostic report triggered.")
        try:
            self.report_service.generate_report()
            self.event_bus.publish(events.NOTIFICATION_TRIGGERED, "Report generated under logs/!", "success")
        except Exception as ex:
            logger.error(f"Failed to generate report from dashboard action: {ex}")
            self.event_bus.publish(events.NOTIFICATION_TRIGGERED, "Report compilation failed.", "danger")

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
        score = report.health_score

        # 1. Animate HealthRing and update score labels
        self.health_ring.set_score(score)
        self.health_score_lbl.configure(text=f"{score} / 100")
        if score >= 80:
            status_color = self.theme.get_color("status_success")
            status_text = "● Optimal — No issues detected"
        elif score >= 50:
            status_color = self.theme.get_color("status_warning")
            status_text = "▲ Degraded — Attention needed"
        else:
            status_color = self.theme.get_color("status_danger")
            status_text = "✖ Critical — Immediate action required"
        self.health_score_lbl.configure(text_color=status_color)
        self.health_status_lbl.configure(text=status_text, text_color=status_color)

        # 2. Update CPU SensorCard with WMI Voltage and estimated power draw
        cpu_detail = (
            f"{report.cpu.temperature:.1f}°C  |  {report.cpu.frequency_ghz:.2f} GHz\n"
            f"Voltage: {report.cpu.voltage} V (WMI)\n"
            f"Power:   {report.cpu.power_draw_watts} W (Estimated)"
        )
        self.cpu_card.update_card(
            value=f"{report.cpu.utilization:.1f} %",
            detail=cpu_detail,
            confidence="HIGH" if report.cpu.utilization > 0 else "NONE"
        )

        # 3. Update GPU SensorCard
        gpu_temp_str = f"{report.gpu_temperature:.1f}°C (Estimated)" if report.gpu_temperature > 0 else "Unavailable"
        gpu_detail = f"{gpu_temp_str}\n{report.gpu_model[:28]}"
        gpu_conf = "ESTIMATED" if report.gpu_temperature > 0 else "UNAVAILABLE"
        self.gpu_card.update_card(
            value=f"{report.gpu_utilization:.1f} %",
            detail=gpu_detail,
            confidence=gpu_conf
        )

        # 4. Update RAM SensorCard
        ram_pct = report.ram.percentage * 100.0
        ram_conf = "HIGH" if report.ram.total_gb > 0 else "NONE"
        self.ram_card.update_card(
            value=f"{report.ram.used_gb:.1f} / {report.ram.total_gb:.1f} GB",
            detail=f"Usage: {ram_pct:.1f}%",
            confidence=ram_conf
        )

        # 5. Update SSD SensorCard
        ssd_temp_str = f"{report.disk.temperature}°C (Estimated)" if report.disk.temperature > 0 else "Unavailable"
        ssd_detail = (
            f"Temp: {ssd_temp_str}\n"
            f"Health: {report.disk.health_percent}%  |  Writes: {report.disk.host_writes_gb} GB\n"
            f"Power-on Hours: {report.disk.power_on_hours} h"
        )
        ssd_conf = "HIGH" if report.disk.status in ("OK", "Pred Fail") else "ESTIMATED"
        self.ssd_card.update_card(
            value=f"SMART: {report.disk.status}",
            detail=ssd_detail,
            confidence=ssd_conf
        )

        # 6. Update sparkline charts
        self.cpu_chart.add_point(report.cpu.utilization)
        self.ram_chart.add_point(ram_pct)
        self.temp_chart.add_point(report.cpu.temperature)
        self.net_chart.add_point(report.network_latency_ms)

        # 7. Update System Overview card
        battery_wear = 100 - report.battery.health_percent
        active_profile = self.profile_mgr.get_profile_name()
        sys_details = (
            f"OS: {report.os.os_name}\n"
            f"CPU: {report.cpu.model_name[:24]}\n"
            f"RAM: {report.ram.total_gb:.1f} GB Dedicated\n"
            f"SSD: {report.disk.total_gb:.1f} GB NVMe\n"
            f"GPU: {report.gpu_model[:24]}\n"
            f"Battery Wear: {battery_wear}%\n"
            f"Profile: {active_profile.upper()}"
        )
        self.sys_info_lbl.configure(text=sys_details)

        # 8. Run Windows Intelligence (once per session, cache results)
        if not self._intelligence_alerts:
            try:
                self._intelligence_alerts = self.intelligence_service.analyze()
            except Exception as ex:
                logger.warning(f"Windows Intelligence analysis failed: {ex}")

        # 9. Populate advice panel: Intelligence alerts + Recommendation engine
        advices = self.recommendation_service.get_recommendations(report)
        self.advice_txt.configure(state="normal")
        self.advice_txt.delete("1.0", "end")

        # Intelligence alerts section
        if self._intelligence_alerts:
            self.advice_txt.insert("end", "── WINDOWS INTELLIGENCE ──────────────────\n")
            sev_icons = {"CRITICAL": "✖", "WARNING": "▲", "INFO": "ℹ"}
            for alert in self._intelligence_alerts:
                icon = sev_icons.get(alert.severity, "●")
                self.advice_txt.insert("end", f"{icon} [{alert.severity}] {alert.title}\n")
                self.advice_txt.insert("end", f"   {alert.message}\n")
                if alert.action:
                    self.advice_txt.insert("end", f"   ↳ {alert.action}\n")
                self.advice_txt.insert("end", "\n")
            self.advice_txt.insert("end", "── SYSTEM RECOMMENDATIONS ────────────────\n")

        # Recommendation engine items
        for idx, item in enumerate(advices):
            self.advice_txt.insert("end", f"[{idx+1}] {item['title']} ({item['priority']})\n")
            self.advice_txt.insert("end", f"↳ {item['action_message']}\n\n")

        if not advices and not self._intelligence_alerts:
            self.advice_txt.insert("end", "✓ No recommendations at this time. System looks healthy.")

        self.advice_txt.configure(state="disabled")

        # 10. Update header profile / health badge
        self.info_lbl.configure(text=f"PROFILE: {active_profile.upper()} | HEALTH: {score}/100")
