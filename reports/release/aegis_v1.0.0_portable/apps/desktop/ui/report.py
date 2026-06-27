"""Report Page — diagnostic report viewer and export for Aegis Core Platform."""

import customtkinter as ctk
import packages.core.constants.events as events
from apps.desktop.ui.base_page import BasePage
from apps.desktop.ui.theme import ThemeManager
from packages.core.container import ServiceContainer
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class ReportPage(BasePage):
    """Scrollable report viewer with export trigger for the last generated diagnostic report."""

    def __init__(self, master: any, theme: ThemeManager) -> None:
        """Initialize the Report Page.

        Args:
            master: Viewport router parent frame.
            theme: Active style theme manager.
        """
        super().__init__(master=master)
        self.theme = theme

        container = ServiceContainer()
        self.event_bus = container.get("event_bus")

        try:
            self.report_service = container.get("report_service")
        except KeyError:
            self.report_service = None

        self.grid_rowconfigure(0, weight=0)  # Header + actions
        self.grid_rowconfigure(1, weight=1)  # Scrollable report text
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_report_viewer()

    def _build_header(self) -> None:
        """Render header and action buttons."""
        spacing_xl = self.theme.get_spacing("spacing_xl")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xs = self.theme.get_spacing("spacing_xs")

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=spacing_xl, pady=(spacing_xl, spacing_md), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="DIAGNOSTIC REPORT",
            font=self.theme.get_font("font_size_lg", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Last generated system diagnostic summary — read-only view",
            font=self.theme.get_font("font_size_md"),
            text_color=self.theme.get_color("text_muted")
        )
        subtitle.grid(row=1, column=0, sticky="w")

        # Action Buttons
        btn_row = ctk.CTkFrame(header, fg_color="transparent")
        btn_row.grid(row=0, column=1, rowspan=2, sticky="e")

        btn_generate = ctk.CTkButton(
            btn_row,
            text="Generate Report",
            font=self.theme.get_font("font_size_sm", "bold"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            width=130,
            command=self._generate_report
        )
        btn_generate.pack(side="left", padx=(0, spacing_sm))

        btn_refresh = ctk.CTkButton(
            btn_row,
            text="Refresh View",
            font=self.theme.get_font("font_size_sm", "bold"),
            fg_color=self.theme.get_color("border"),
            text_color=self.theme.get_color("text_primary"),
            hover_color=self.theme.get_color("bg_primary"),
            width=110,
            command=self._load_report_content
        )
        btn_refresh.pack(side="left")

    def _build_report_viewer(self) -> None:
        """Render scrollable text area for report content."""
        spacing_xl = self.theme.get_spacing("spacing_xl")

        card = ctk.CTkFrame(
            self,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        card.grid(row=1, column=0, padx=spacing_xl, pady=(0, spacing_xl), sticky="nsew")
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)

        self.report_txt = ctk.CTkTextbox(
            card,
            font=self.theme.get_font("font_size_md"),
            fg_color=self.theme.get_color("bg_primary"),
            text_color=self.theme.get_color("text_primary"),
            border_width=0,
            wrap="none"
        )
        self.report_txt.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        # Default placeholder
        self._set_report_text("No report loaded.\n\nClick 'Generate Report' to compile a fresh diagnostic report,\nor 'Refresh View' to reload the last saved report.")

    def _set_report_text(self, content: str) -> None:
        """Replaces report textbox content safely."""
        self.report_txt.configure(state="normal")
        self.report_txt.delete("1.0", "end")
        self.report_txt.insert("1.0", content)
        self.report_txt.configure(state="disabled")

    def _generate_report(self) -> None:
        """Triggers report generation and refreshes the view."""
        if self.report_service is None:
            logger.error("ReportPage: report_service not registered in ServiceContainer.")
            self._set_report_text("Report service is unavailable. Please restart Aegis.")
            return

        logger.info("ReportPage: Generating new diagnostic report...")
        try:
            result = self.report_service.generate_report()
            self.event_bus.publish(events.NOTIFICATION_TRIGGERED, "Diagnostic report generated!", "success")
            self._load_report_content()
        except Exception as ex:
            logger.error(f"ReportPage: Report generation failed: {ex}")
            self._set_report_text(f"Report generation failed:\n{ex}")

    def _load_report_content(self) -> None:
        """Loads and displays the last saved report from disk."""
        from packages.core.constants.paths import PROJECT_ROOT
        import os

        report_dir = PROJECT_ROOT / "logs" / "reports"
        if not report_dir.exists():
            self._set_report_text("No reports found. Run 'Generate Report' first.")
            return

        # Find the most recent report file
        report_files = sorted(report_dir.glob("*.md"), key=os.path.getmtime, reverse=True)
        if not report_files:
            report_files = sorted(report_dir.glob("*.txt"), key=os.path.getmtime, reverse=True)

        if not report_files:
            self._set_report_text("No report files found in logs/reports/.\nClick 'Generate Report' to create one.")
            return

        try:
            latest = report_files[0]
            content = latest.read_text(encoding="utf-8")
            self._set_report_text(f"Report: {latest.name}\n{'=' * 60}\n\n{content}")
            logger.info(f"ReportPage: Loaded report from {latest}")
        except Exception as ex:
            self._set_report_text(f"Failed to read report file:\n{ex}")

    def on_resume(self) -> None:
        """Auto-refresh report content when page becomes visible."""
        logger.info("ReportPage: Page activated — auto-refreshing report view.")
        self._load_report_content()
