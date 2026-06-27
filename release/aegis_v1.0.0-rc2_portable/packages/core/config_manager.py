"""Configuration management system for Aegis Toolkit."""

import json
from pathlib import Path
from typing import Any
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class ConfigManager:
    """Manages reading, writing, and caching of application configurations."""

    def __init__(self, config_path: Path, default_settings: dict[str, Any]) -> None:
        """Initialize the Config Manager.
        
        Args:
            config_path: Path to the settings.json file.
            default_settings: Default settings dictionary fallback.
        """
        self.config_path = config_path
        self.defaults = default_settings
        self.settings: dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        """Reload configuration settings from the JSON file."""
        if not self.config_path.exists():
            logger.warning(f"Configuration file missing at {self.config_path}. Generating default configuration.")
            self.settings = self.defaults.copy()
            self.save()
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.settings = data
                else:
                    logger.error("Configuration file format corrupt. Resetting to defaults.")
                    self.settings = self.defaults.copy()
        except Exception as ex:
            logger.error(f"Failed to read configuration: {ex}. Using default configuration.", exc_info=True)
            self.settings = self.defaults.copy()

    def save(self) -> None:
        """Write the cached configuration settings to disk."""
        try:
            # Ensure parent directories exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
            logger.info(f"Configuration values saved to disk: {self.config_path}")
        except Exception as ex:
            logger.error(f"Failed to write configuration to file: {ex}", exc_info=True)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value matching target key.
        
        Args:
            key: Configuration setting name.
            default: Fallback value if setting key is missing.
            
        Returns:
            The configuration setting value.
        """
        return self.settings.get(key, self.defaults.get(key, default))

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration setting name.
            value: Configuration value to store.
        """
        self.settings[key] = value
        logger.info(f"Setting updated: {key} = {value}")
        self.save()
