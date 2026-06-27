"""Settings page rendering application configurations for Aegis Core Platform."""

import customtkinter as ctk
from apps.desktop.ui.base_page import BasePage
from apps.desktop.ui.theme import ThemeManager
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class SettingsPage(BasePage):
    """Settings page viewport allowing adjustments to system configurations and styling."""

    def __init__(self, master: any, theme: ThemeManager) -> None:
        """Initialize the Settings Page.
        
        Args:
            master: Parent routing frame.
            theme: Active style theme manager.
        """
        super().__init__(master=master)
        self.theme = theme

        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Settings Group
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_settings_group()

    def _build_header(self) -> None:
        """Render page headers."""
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=spacing_xl, pady=(spacing_xl, spacing_md), sticky="ew")

        title_lbl = ctk.CTkLabel(
            header_frame,
            text="APPLICATION CONFIGURATIONS",
            font=self.theme.get_font("font_size_lg", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        title_lbl.pack(side="left", anchor="w")

    def _build_settings_group(self) -> None:
        """Render settings panels."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_lg = self.theme.get_spacing("spacing_lg")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        settings_frame = ctk.CTkFrame(
            self,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        settings_frame.grid(row=1, column=0, padx=spacing_xl, pady=(0, spacing_xl), sticky="nsew")
        settings_frame.grid_columnconfigure(0, weight=1)

        # Setting Group 1: General configuration
        gen_lbl = ctk.CTkLabel(
            settings_frame,
            text="Diagnostics & Telemetry Speed",
            font=self.theme.get_font("font_size_md", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        gen_lbl.pack(anchor="w", padx=spacing_lg, pady=(spacing_lg, spacing_sm))

        rate_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        rate_frame.pack(fill="x", padx=spacing_lg, pady=spacing_xs)

        rate_lbl = ctk.CTkLabel(
            rate_frame,
            text="Refresh Interval (Seconds):",
            font=self.theme.get_font("font_size_md"),
            text_color=self.theme.get_color("text_muted")
        )
        rate_lbl.pack(side="left", anchor="w")

        rate_dropdown = ctk.CTkOptionMenu(
            rate_frame,
            values=["1.0s", "2.0s", "5.0s"],
            width=90,
            corner_radius=self.theme.get_radius("corner_radius_sm"),
            fg_color=self.theme.get_color("accent_primary"),
            button_color=self.theme.get_color("accent_primary"),
            button_hover_color=self.theme.get_color("border")
        )
        rate_dropdown.pack(side="left", padx=spacing_md)
        rate_dropdown.set("1.0s")

        # Divider
        divider = ctk.CTkFrame(
            settings_frame,
            height=1,
            fg_color=self.theme.get_color("border")
        )
        divider.pack(fill="x", padx=spacing_lg, pady=spacing_lg)

        # Setting Group 2: Visual styling
        style_lbl = ctk.CTkLabel(
            settings_frame,
            text="Appearance Mode",
            font=self.theme.get_font("font_size_md", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        style_lbl.pack(anchor="w", padx=spacing_lg, pady=(0, spacing_sm))

        theme_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=spacing_lg, pady=spacing_xs)

        theme_lbl = ctk.CTkLabel(
            theme_frame,
            text="Color Palette Theme Mode:",
            font=self.theme.get_font("font_size_md"),
            text_color=self.theme.get_color("text_muted")
        )
        theme_lbl.pack(side="left", anchor="w")

        theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Force Dark Mode",
            font=self.theme.get_font("font_size_md"),
            progress_color=self.theme.get_color("accent_primary")
        )
        theme_switch.pack(side="left", padx=spacing_md)
        theme_switch.select() # Check by default

        # Divider 2
        divider2 = ctk.CTkFrame(
            settings_frame,
            height=1,
            fg_color=self.theme.get_color("border")
        )
        divider2.pack(fill="x", padx=spacing_lg, pady=spacing_lg)

        # About Trigger Button
        about_btn = ctk.CTkButton(
            settings_frame,
            text="Show Platform Version & About Details",
            font=self.theme.get_font("font_size_md", "bold"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=self._launch_about
        )
        about_btn.pack(anchor="w", padx=spacing_lg, pady=(0, spacing_lg))

    def _launch_about(self) -> None:
        try:
            self.winfo_toplevel().show_about_dialog()
        except Exception as ex:
            logger.error(f"Failed to launch about dialog from settings viewport: {ex}")

    def refresh(self) -> None:
        """Lifecycle hook triggered when page displays."""
        logger.info("SettingsPage: View displayed.")

    def cleanup(self) -> None:
        """Lifecycle hook triggered when page hides."""
        logger.debug("SettingsPage: View hidden.")
