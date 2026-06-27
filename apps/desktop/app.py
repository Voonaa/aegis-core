"""Main application UI Shell class for Aegis Core Platform."""

import customtkinter as ctk
import packages.core.constants.events as events
from packages.core.container import ServiceContainer
from packages.core.config_manager import ConfigManager
from apps.desktop.ui.theme import ThemeManager
from apps.desktop.ui.sidebar import SidebarFrame
from apps.desktop.ui.console import DeveloperConsoleFrame
from apps.desktop.ui.dashboard import DashboardPage
from apps.desktop.ui.maintenance import MaintenancePage
from apps.desktop.ui.settings import SettingsPage
from apps.desktop.ui.monitor import MonitorPage
from apps.desktop.ui.report import ReportPage
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

# Configuration defaults as fallback
DEFAULT_SETTINGS: dict = {
    "app_name": "Aegis Core Platform",
    "version": "1.0.0-rc2",
    "log_level": "INFO",
    "telemetry_interval_ms": 1000,
    "admin_required": True
}

import json
import platform
from pathlib import Path

class AboutDialog(ctk.CTkToplevel):
    """About Dialog displaying build metadata and system info."""

    def __init__(self, parent: any, theme: ThemeManager) -> None:
        """Initialize the About Dialog."""
        super().__init__(parent)
        self.theme = theme
        
        self.title("About Aegis Core")
        self.geometry("460x420")
        self.resizable(False, False)
        self.configure(fg_color=theme.get_color("bg_primary"))
        
        # Transient & Modal focus
        self.transient(parent)
        self.grab_set()

        # Center dialog relative to parent app window
        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width() // 2) - 230
        py = parent.winfo_y() + (parent.winfo_height() // 2) - 210
        self.geometry(f"+{px}+{py}")

        metadata = self._load_metadata()
        self._build_ui(metadata)

    def _load_metadata(self) -> dict:
        metadata = {
            "version": "1.0.0-rc2",
            "build_timestamp": "Local Development",
            "commit_hash": "DEBUG-DEV",
            "python_version": platform.python_version(),
            "architecture": platform.machine(),
            "profile": "Generic Host Profile"
        }
        try:
            meta_path = Path(__file__).resolve().parent / "config" / "build_metadata.json"
            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    metadata.update(data)
        except Exception:
            pass
        return metadata

    def _build_ui(self, metadata: dict) -> None:
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_lg = self.theme.get_spacing("spacing_lg")

        # Brand Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(padx=spacing_lg, pady=(spacing_lg, spacing_sm), fill="x")

        logo_lbl = ctk.CTkLabel(header_frame, text="🛡", font=self.theme.get_font("font_size_xl", "bold"))
        logo_lbl.pack(side="left", padx=(0, spacing_sm))

        title_lbl = ctk.CTkLabel(header_frame, text="AEGIS CORE", font=self.theme.get_font("font_size_lg", "bold"), text_color=self.theme.get_color("text_primary"))
        title_lbl.pack(side="left")

        # Info card frame
        card = ctk.CTkFrame(
            self,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        card.pack(padx=spacing_lg, pady=spacing_sm, fill="both", expand=True)

        # Fields list
        fields = [
            ("Platform Version", metadata["version"]),
            ("Build Timestamp", metadata["build_timestamp"]),
            ("Commit Hash", metadata["commit_hash"]),
            ("Python Runtime", f"v{metadata['python_version']}"),
            ("Architecture", metadata["architecture"]),
            ("Loaded Profile", metadata["profile"])
        ]

        for label, val in fields:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=spacing_md, pady=spacing_xs)
            
            lbl_w = ctk.CTkLabel(row, text=label, font=self.theme.get_font("font_size_md", "bold"), text_color=self.theme.get_color("text_muted"))
            lbl_w.pack(side="left")

            val_w = ctk.CTkLabel(row, text=val, font=self.theme.get_font("font_size_md"), text_color=self.theme.get_color("text_primary"))
            val_w.pack(side="right")

        # License text
        license_lbl = ctk.CTkLabel(
            self,
            text="Distributed under MIT License. Copyright © 2026 Aegis Team.",
            font=self.theme.get_font("font_size_sm"),
            text_color=self.theme.get_color("text_muted")
        )
        license_lbl.pack(pady=(spacing_sm, spacing_lg))

class NotificationToast(ctk.CTkFrame):
    """Slide-in notification overlay component."""

    def __init__(self, master: any, theme: ThemeManager, message: str, status_type: str = "success") -> None:
        """Initialize the Notification Toast.
        
        Args:
            master: Root parent container widget.
            theme: Active style theme manager.
            message: Text notification message.
            status_type: Alert severity tier (success, warning, danger).
        """
        color_token = "status_success"
        if status_type == "warning":
            color_token = "status_warning"
        elif status_type == "danger":
            color_token = "status_danger"

        spacing_md = theme.get_spacing("spacing_md")
        spacing_lg = theme.get_spacing("spacing_lg")
        spacing_xl = theme.get_spacing("spacing_xl")

        super().__init__(
            master=master,
            corner_radius=theme.get_radius("corner_radius_md"),
            fg_color=theme.get_color("bg_card"),
            border_width=2,
            border_color=theme.get_color(color_token)
        )

        self.msg_lbl = ctk.CTkLabel(
            self,
            text=message,
            font=theme.get_font("font_size_md"),
            text_color=theme.get_color("text_primary"),
            padx=spacing_lg,
            pady=spacing_md
        )
        self.msg_lbl.pack(fill="both", expand=True)

        # Slide-in position placement overlay
        self.place(relx=1.0, rely=0.0, anchor="ne", x=-spacing_xl, y=spacing_xl)
        
        # Schedule auto-destruct after 3.5 seconds
        self.after(3500, self.destroy)


class AegisApp(ctk.CTk):
    """Main Application GUI Shell managing layouts routing and initialization logs."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Aegis App main window launcher.
        
        Args:
            container: Service container reference.
        """
        super().__init__()
        self.container = container
        
        # Retrieve core managers from ServiceContainer
        self.config: ConfigManager = container.get("config")
        self.theme: ThemeManager = container.get("theme")
        self.event_bus = container.get("event_bus")

        logger.info("Initializing Aegis Core desktop workspace shell...")

        # Visual styling setup
        ctk.set_appearance_mode(self.theme.theme_mode)
        ctk.set_default_color_theme("blue")

        # Window properties config
        self.title(f"🛡 {self.config.get('app_name')} - v{self.config.get('version')} RC2")
        self.geometry("1020x660")
        self.minsize(800, 520)
        self.configure(fg_color=self.theme.get_color("bg_primary"))

        # Root Grid Layout weights
        self.grid_rowconfigure(0, weight=1)  # Viewport layout flex
        self.grid_rowconfigure(1, weight=0)  # Statusbar
        self.grid_columnconfigure(0, weight=0)  # Sidebar (Fixed)
        self.grid_columnconfigure(1, weight=1)  # Viewport & console (Flex)

        self._build_interface()

        # Subscribe to notification events
        self.event_bus.subscribe(events.NOTIFICATION_TRIGGERED, self.show_notification)

    def _build_interface(self) -> None:
        """Create and grid core layout frame elements."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        # 1. Instantiate the navigation Sidebar on Column 0
        self.sidebar = SidebarFrame(
            master=self,
            theme=self.theme,
            on_navigate=self.navigate_to,
            version=self.config.get("version", "1.0.0-rc2")
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # 2. Main content viewport frame on Column 1
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=0, column=1, sticky="nsew")
        self.right_container.grid_rowconfigure(0, weight=1)  # Viewpage frame (Flex)
        self.right_container.grid_rowconfigure(1, weight=0)  # CLI Console frame (Fixed)
        self.right_container.grid_columnconfigure(0, weight=1)

        # 3. Instantiate the Developer Console at the bottom
        self.console = DeveloperConsoleFrame(
            master=self.right_container,
            theme=self.theme
        )
        self.console.grid(row=1, column=0, padx=spacing_xl, pady=(spacing_xs, spacing_md), sticky="ew")

        # 4. Instantiate Viewport Pages
        self.pages: dict[str, any] = {
            "Dashboard": DashboardPage(self.right_container, self.theme),
            "Monitor": MonitorPage(self.right_container, self.theme),
            "Maintenance": MaintenancePage(
                master=self.right_container,
                theme=self.theme,
                log_callback=self.console.write_log
            ),
            "Report": ReportPage(self.right_container, self.theme),
            "Settings": SettingsPage(self.right_container, self.theme),
        }

        # 5. Bottom Status bar indicator panel
        self.statusbar = ctk.CTkFrame(
            self,
            height=24,
            corner_radius=0,
            fg_color=self.theme.get_color("bg_sidebar"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        self.statusbar.grid(row=1, column=1, sticky="ew")
        
        self.status_lbl = ctk.CTkLabel(
            self.statusbar,
            text="Status: Ready | System Profile: Auto-Detecting...",
            font=self.theme.get_font("font_size_sm"),
            text_color=self.theme.get_color("text_muted"),
            padx=spacing_md
        )
        self.status_lbl.pack(side="left")

        # Start by showing default view (using BasePage lifecycle show hook)
        self.active_page_name = "Dashboard"
        self.pages[self.active_page_name].show()
        logger.info(f"Default layout initialized: {self.active_page_name} Page active.")

    def navigate_to(self, page_name: str) -> None:
        """Routes viewport to show selected page.
        
        Args:
            page_name: Targeted page view identifier name.
        """
        # About is a dialog, not a page
        if page_name == "About":
            self.show_about_dialog()
            # Reset sidebar highlight back to active page
            self.sidebar._highlight_button(self.active_page_name)
            return

        if page_name not in self.pages:
            logger.error(f"Routing request failed. Unknown page path target: {page_name}")
            return

        logger.info(f"User requested navigation path: {self.active_page_name} -> {page_name}")
        self.console.write_log(f"Routing viewport: show {page_name} page...", "USER")

        # Hide current view, show newly selected view using BasePage hooks
        self.pages[self.active_page_name].hide()
        self.active_page_name = page_name
        self.pages[page_name].show()

        # Update status bar text
        self.status_lbl.configure(text=f"Status: Active view switched to {page_name}")

    def show_notification(self, message: str, status_type: str = "success") -> None:
        """Triggers a slide-in floating notification toast overlay.
        
        Args:
            message: Event alert text.
            status_type: Severity tier (success, warning, danger).
        """
        logger.info(f"Triggering UI notification toast: {message} ({status_type})")
        NotificationToast(self, self.theme, message, status_type)

    def update_profile_status(self, profile_name: str) -> None:
        """Updates the status bar system profile label.
        
        Args:
            profile_name: Dynamic name of the loaded laptop profile.
        """
        self.status_lbl.configure(text=f"Status: Ready | System Profile: {profile_name}")

    def show_about_dialog(self) -> None:
        """Spawns the About Dialog modal."""
        logger.info("Spawning About modal dialog overlay.")
        AboutDialog(self, self.theme)
