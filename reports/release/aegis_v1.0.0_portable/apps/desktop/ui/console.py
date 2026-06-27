"""Developer Console CLI frame component for Aegis Core Platform."""

import customtkinter as ctk
import datetime
from apps.desktop.ui.theme import ThemeManager
from packages.core.container import ServiceContainer
from packages.core.command_registry import CommandRegistry

class DeveloperConsoleFrame(ctk.CTkFrame):
    """Developer console component rendering interactive text shell and input fields."""

    def __init__(self, master: any, theme: ThemeManager) -> None:
        """Initialize the Console Frame.
        
        Args:
            master: The parent container widget.
            theme: Active style theme manager.
        """
        spacing_xs = theme.get_spacing("spacing_xs")
        spacing_sm = theme.get_spacing("spacing_sm")

        super().__init__(
            master=master,
            corner_radius=theme.get_radius("corner_radius_md"),
            fg_color=theme.get_color("bg_primary"),
            border_width=1,
            border_color=theme.get_color("border")
        )
        self.theme = theme

        # Retrieve CommandRegistry from the DI ServiceContainer
        container = ServiceContainer()
        self.registry: CommandRegistry = container.get("command_registry")

        # Layout grids
        self.grid_rowconfigure(0, weight=1)  # Terminal TextBox
        self.grid_rowconfigure(1, weight=0)  # Input console field
        self.grid_columnconfigure(0, weight=1)

        self._build_console()

    def _build_console(self) -> None:
        """Build elements: text area box, inputs prefix label, and active textbox entries."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")

        # Row 0: Textbox terminal view
        self.terminal = ctk.CTkTextbox(
            self,
            fg_color=self.theme.get_color("bg_sidebar"),
            text_color="#E5E7EB",
            font=("Consolas", 11),
            corner_radius=self.theme.get_radius("corner_radius_sm"),
            border_spacing=4,
            wrap="word"
        )
        self.terminal.grid(row=0, column=0, padx=spacing_sm, pady=(spacing_sm, spacing_xs), sticky="nsew")
        self.terminal.configure(state="disabled")

        # Configure custom styling tags for coloring log levels
        self.terminal.tag_config("INFO", foreground="#E5E7EB")
        self.terminal.tag_config("WARNING", foreground=self.theme.get_color("status_warning"))
        self.terminal.tag_config("ERROR", foreground=self.theme.get_color("status_danger"))
        self.terminal.tag_config("USER", foreground="#60A5FA")

        # Row 1: CLI Entry line
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=1, column=0, padx=spacing_sm, pady=(spacing_xs, spacing_sm), sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        prefix_label = ctk.CTkLabel(
            input_frame,
            text="aegis> ",
            font=("Consolas", 12, "bold"),
            text_color="#60A5FA"
        )
        prefix_label.grid(row=0, column=0, padx=(4, 0), pady=0, sticky="w")

        self.cmd_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="type 'help' for command directories...",
            font=("Consolas", 12),
            fg_color=self.theme.get_color("bg_primary"),
            border_width=0,
            text_color="#FFFFFF"
        )
        self.cmd_input.grid(row=0, column=1, padx=4, pady=0, sticky="ew")

        # Bind Enter/Return key actions
        self.cmd_input.bind("<Return>", self._handle_input)

        # Print initial boot message
        self.write_log("Aegis CLI Developer Console initialized. Ready for operations.", "INFO")

    def write_log(self, message: str, level: str = "INFO") -> None:
        """Appends log records to terminal view textbox safely.
        
        Args:
            message: Text string message to output.
            level: Severity tag for colored layouts (INFO, WARNING, ERROR, USER).
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}\n"

        self.terminal.configure(state="normal")
        self.terminal.insert("end", formatted, level)
        self.terminal.configure(state="disabled")
        self.terminal.see("end")

    def _handle_input(self, event: any) -> None:
        """Processes Enter keyboard inputs, handles command parser triggers."""
        raw_cmd: str = self.cmd_input.get().strip()
        self.cmd_input.delete(0, "end")

        if not raw_cmd:
            return

        # Echo input to terminal logs
        self.write_log(f"aegis> {raw_cmd}", "USER")

        # Clear command is handled locally by the console view
        if raw_cmd.lower() == "clear":
            self.terminal.configure(state="normal")
            self.terminal.delete("1.0", "end")
            self.terminal.configure(state="disabled")
            return

        # Route execution to core registry CommandRegistry
        output = self.registry.execute(raw_cmd)
        if output:
            self.write_log(output, "INFO")
