"""Developer console CLI commands registry pattern for Aegis Toolkit."""

from typing import Callable, Any
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("USER")

class CommandRegistry:
    """Maintains console routing commands mapping string tokens to callbacks."""

    def __init__(self) -> None:
        """Initialize the Command Registry."""
        self._commands: dict[str, tuple[Callable[..., str], str]] = {}
        logger.info("Command Registry initialized.")

    def register(self, command_name: str, callback: Callable[..., str], help_text: str = "") -> None:
        """Registers a console string to execution handler.
        
        Args:
            command_name: Command name token.
            callback: Execution handler. Must return a status string output.
            help_text: Short explanation string.
        """
        name_lower = command_name.lower().strip()
        self._commands[name_lower] = (callback, help_text)
        logger.info(f"Console command registered: '{name_lower}'")

    def execute(self, command_line: str) -> str:
        """Parses and triggers registered command routines.
        
        Args:
            command_line: Raw input text command string.
            
        Returns:
            Status text string output returned by the command handler.
        """
        parts = command_line.strip().split()
        if not parts:
            return ""

        cmd_name = parts[0].lower()
        args = parts[1:]

        if cmd_name not in self._commands:
            logger.warning(f"Console input routing failed: Command '{cmd_name}' not found.")
            return f"Command '{cmd_name}' unrecognized. Type 'help' for command options."

        callback, _ = self._commands[cmd_name]
        try:
            logger.info(f"Executing console command: '{cmd_name}' with args {args}")
            return callback(*args)
        except Exception as ex:
            logger.error(f"Console command execution failed: {ex}", exc_info=True)
            return f"Execution Error: {ex}"

    def get_help_list(self) -> dict[str, str]:
        """Gets help information maps for all registered commands."""
        return {name: help_text for name, (_, help_text) in self._commands.items()}
