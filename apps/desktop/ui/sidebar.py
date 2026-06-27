"""Left-hand navigation panel layout for Aegis Core Platform."""

import customtkinter as ctk
from typing import Callable
from apps.desktop.ui.theme import ThemeManager

class SidebarFrame(ctk.CTkFrame):
    """Sidebar component managing visual buttons and view routing callbacks."""

    def __init__(
        self,
        master: any,
        theme: ThemeManager,
        on_navigate: Callable[[str], None],
        version: str = "0.1.0"
    ) -> None:
        """Initialize the Sidebar layout frame.
        
        Args:
            master: The parent container widget.
            theme: The active visual theme manager reference.
            on_navigate: Routing callback triggered on nav clicks.
            version: Current release version string.
        """
        super().__init__(
            master=master,
            corner_radius=0,
            fg_color=theme.get_color("bg_sidebar")
        )
        self.theme = theme
        self.on_navigate = on_navigate
        self.version = version
        self.buttons: dict[str, ctk.CTkButton] = {}
        self.active_page: str = "Dashboard"

        # Initialize widget layout grid
        self.grid_rowconfigure(0, weight=0)  # Brand
        self.grid_rowconfigure(1, weight=1)  # Space / Navigation list
        self.grid_rowconfigure(2, weight=0)  # Footer version
        self.grid_columnconfigure(0, weight=1)

        self._build_sidebar()

    def _build_sidebar(self) -> None:
        """Build brand labels, nav triggers, and version strings."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_lg = self.theme.get_spacing("spacing_lg")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        # Row 0: Branding Title Header
        brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        brand_frame.grid(row=0, column=0, padx=spacing_lg, pady=(spacing_xl, spacing_xl * 1.3), sticky="nsew")

        brand_icon = ctk.CTkLabel(
            brand_frame,
            text="🛡",
            font=self.theme.get_font("font_size_xl")
        )
        brand_icon.pack(side="left", padx=(0, spacing_sm))

        brand_label = ctk.CTkLabel(
            brand_frame,
            text="AEGIS",
            font=self.theme.get_font("font_size_xl", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        brand_label.pack(side="left")

        # Row 1: Vertical Navigation Buttons Layout Frame
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.grid(row=1, column=0, padx=spacing_md, pady=0, sticky="new")
        nav_frame.grid_columnconfigure(0, weight=1)

        menu_items = [
            ("Dashboard", "🏠"),
            ("Maintenance", "🛠"),
            ("Settings", "⚙")
        ]

        for i, (name, icon) in enumerate(menu_items):
            btn = ctk.CTkButton(
                nav_frame,
                text=f"  {icon}  {name}",
                font=self.theme.get_font("font_size_md", "normal"),
                anchor="w",
                height=40,
                corner_radius=self.theme.get_radius("corner_radius_md"),
                fg_color="transparent",
                text_color=self.theme.get_color("text_primary"),
                hover_color=self.theme.get_color("border"),
                command=lambda p=name: self._handle_click(p)
            )
            btn.grid(row=i, column=0, padx=0, pady=spacing_xs, sticky="ew")
            self.buttons[name] = btn

        # Highlight default page Selection state
        self._highlight_button(self.active_page)

        # Row 2: Footer Version display
        footer = ctk.CTkLabel(
            self,
            text=f"Version {self.version}",
            font=self.theme.get_font("font_size_sm"),
            text_color=self.theme.get_color("text_muted")
        )
        footer.grid(row=2, column=0, padx=spacing_lg, pady=spacing_lg, sticky="s")

    def _handle_click(self, page_name: str) -> None:
        """Process nav click actions, update routing callbacks."""
        if page_name == self.active_page:
            return
        
        self.active_page = page_name
        self._highlight_button(page_name)
        self.on_navigate(page_name)

    def _highlight_button(self, active_name: str) -> None:
        """Toggle button highlight background styles matching active states."""
        for name, btn in self.buttons.items():
            if name == active_name:
                btn.configure(
                    fg_color=self.theme.get_color("accent_primary"),
                    hover_color=self.theme.get_color("accent_primary")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color=self.theme.get_color("border")
                )
