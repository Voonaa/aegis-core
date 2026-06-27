"""Reusable CustomTkinter layout widgets for Aegis Core Platform."""

import customtkinter as ctk
import tkinter as tk
from apps.desktop.ui.theme import ThemeManager

class MetricCard(ctk.CTkFrame):
    """Card widget rendering individual telemetry parameters."""

    def __init__(
        self,
        master: any,
        theme: ThemeManager,
        title: str,
        value: str = "N/A",
        subtitle: str = ""
    ) -> None:
        """Initialize the Metric Card.
        
        Args:
            master: Parent container.
            theme: Style theme manager.
            title: Card metric title label text.
            value: Large readout metric value.
            subtitle: Small descriptor sub-label text.
        """
        spacing_xs = theme.get_spacing("spacing_xs")
        spacing_lg = theme.get_spacing("spacing_lg")

        super().__init__(
            master=master,
            corner_radius=theme.get_radius("corner_radius_lg"),
            fg_color=theme.get_color("bg_card"),
            border_width=1,
            border_color=theme.get_color("border")
        )
        self.theme = theme

        self.title_label = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=theme.get_font("font_size_sm", "bold"),
            text_color=theme.get_color("text_muted")
        )
        self.title_label.pack(anchor="w", padx=spacing_lg, pady=(spacing_lg, spacing_xs))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=theme.get_font("font_size_xl", "bold"),
            text_color=theme.get_color("text_primary")
        )
        self.value_label.pack(anchor="w", padx=spacing_lg, pady=0)

        self.sub_label = ctk.CTkLabel(
            self,
            text=subtitle,
            font=theme.get_font("font_size_md"),
            text_color=theme.get_color("text_muted")
        )
        self.sub_label.pack(anchor="w", padx=spacing_lg, pady=(spacing_xs, spacing_lg))

    def update_value(self, new_value: str, new_subtitle: str | None = None) -> None:
        """Updates display readouts dynamically.
        
        Args:
            new_value: Main metric value.
            new_subtitle: Sub-text string descriptor.
        """
        self.value_label.configure(text=new_value)
        if new_subtitle is not None:
            self.sub_label.configure(text=new_subtitle)


class ProgressBarCard(ctk.CTkFrame):
    """Metric card containing a horizontal progress bar loader."""

    def __init__(
        self,
        master: any,
        theme: ThemeManager,
        title: str,
        value: str = "N/A",
        percentage: float = 0.0
    ) -> None:
        """Initialize the Progress Bar Card.
        
        Args:
            master: Parent container.
            theme: Theme manager.
            title: Title string.
            value: Readout string.
            percentage: Floating point value bounds [0.0 - 1.0].
        """
        spacing_xs = theme.get_spacing("spacing_xs")
        spacing_sm = theme.get_spacing("spacing_sm")
        spacing_lg = theme.get_spacing("spacing_lg")

        super().__init__(
            master=master,
            corner_radius=theme.get_radius("corner_radius_lg"),
            fg_color=theme.get_color("bg_card"),
            border_width=1,
            border_color=theme.get_color("border")
        )
        self.theme = theme

        self.title_label = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=theme.get_font("font_size_sm", "bold"),
            text_color=theme.get_color("text_muted")
        )
        self.title_label.pack(anchor="w", padx=spacing_lg, pady=(spacing_lg, spacing_xs))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=theme.get_font("font_size_xl", "bold"),
            text_color=theme.get_color("text_primary")
        )
        self.value_label.pack(anchor="w", padx=spacing_lg, pady=0)

        # Progress bar configuration
        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=spacing_sm,
            corner_radius=theme.get_radius("corner_radius_sm"),
            fg_color=theme.get_color("bg_primary"),
            progress_color=theme.get_color("accent_primary")
        )
        self.progress_bar.pack(anchor="w", padx=spacing_lg, pady=(spacing_sm, spacing_lg), fill="x", expand=True)
        self.progress_bar.set(percentage)

    def update_progress(self, new_value: str, percentage: float) -> None:
        """Updates metrics and progress loader.
        
        Args:
            new_value: Readout text.
            percentage: Progress bar fraction [0.0 - 1.0].
        """
        self.value_label.configure(text=new_value)
        self.progress_bar.set(percentage)

        # Dynamic warning coloring based on utilization percent
        if percentage >= 0.9:
            self.progress_bar.configure(progress_color=self.theme.get_color("status_danger"))
        elif percentage >= 0.8:
            self.progress_bar.configure(progress_color=self.theme.get_color("status_warning"))
        else:
            self.progress_bar.configure(progress_color=self.theme.get_color("accent_primary"))


class StatusBadge(ctk.CTkFrame):
    """Component rendering LED status color circles beside descriptor labels."""

    def __init__(
        self,
        master: any,
        theme: ThemeManager,
        name: str,
        status_type: str = "success"
    ) -> None:
        """Initialize the Status Badge.
        
        Args:
            master: Parent container.
            theme: Theme manager.
            name: Status name descriptor.
            status_type: Alert categorization (success, warning, danger).
        """
        super().__init__(master=master, fg_color="transparent")
        self.theme = theme

        # Resolve transparent background by searching parent tree
        bg_color = master.cget("fg_color")
        if bg_color == "transparent":
            parent = master
            while parent:
                try:
                    p_color = parent.cget("fg_color")
                    if p_color != "transparent":
                        bg_color = p_color
                        break
                except Exception:
                    pass
                parent = parent.master
            if bg_color == "transparent":
                bg_color = theme.get_color("bg_primary")

        # Draw LED Circle Canvas
        self.canvas = tk.Canvas(
            self,
            width=14,
            height=14,
            bg=bg_color,
            highlightthickness=0
        )
        self.canvas.pack(side="left", padx=(4, 8), pady=0)

        self.label = ctk.CTkLabel(
            self,
            text=name,
            font=theme.get_font("font_size_md", "normal"),
            text_color=theme.get_color("text_primary")
        )
        self.label.pack(side="left", anchor="w")

        self.update_status(status_type)

    def update_status(self, status_type: str) -> None:
        """Repaints the LED canvas color matching target status types.
        
        Args:
            status_type: Core alert tier string (success, warning, danger).
        """
        color_token = "status_success"
        if status_type == "warning":
            color_token = "status_warning"
        elif status_type == "danger":
            color_token = "status_danger"

        color = self.theme.get_color(color_token)
        self.canvas.delete("all")
        self.canvas.create_oval(2, 2, 12, 12, fill=color, outline="")
