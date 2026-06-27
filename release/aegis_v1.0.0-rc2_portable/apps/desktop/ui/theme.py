"""Visual theme manager parsing design tokens for Aegis Toolkit."""

import json
from pathlib import Path
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

# Standard styling defaults as a fallback configuration
DEFAULT_THEME: dict = {
    "theme_mode": "dark",
    "colors": {
        "bg_primary": "#1A1A1A",
        "bg_sidebar": "#111827",
        "bg_card": "#1F2937",
        "border": "#374151",
        "accent_primary": "#2563EB",
        "text_primary": "#FFFFFF",
        "text_muted": "#9CA3AF",
        "status_success": "#22C55E",
        "status_warning": "#FACC15",
        "status_danger": "#EF4444"
    }
}

class ThemeManager:
    """Manages look-and-feel style tokens loaded from theme assets (Singleton)."""

    _instance: "ThemeManager | None" = None

    def __new__(cls, *args: any, **kwargs: any) -> "ThemeManager":
        """Enforces Singleton design pattern for ThemeManager."""
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize the manager loading custom styling overrides if available.
        
        Args:
            config_path: Path to the theme configuration JSON file.
        """
        if self._initialized:
            return

        if config_path is None:
            desktop_root: Path = Path(__file__).resolve().parent.parent
            config_path = desktop_root / "config" / "theme.json"

        self.config_path = config_path
        self.theme_data = self._load_theme()
        self._initialized = True

    def _load_theme(self) -> dict:
        """Loads configuration maps from files, handles fallback rules.
        
        Returns:
            Dictionary detailing color design system keys.
        """
        if not self.config_path.exists():
            logger.warning(f"Theme file missing at {self.config_path}. Reverting to baseline colors.")
            return DEFAULT_THEME

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "colors" in data and isinstance(data["colors"], dict):
                    return data
                logger.error("Theme configuration file format corrupt. Resetting to standard configurations.")
                return DEFAULT_THEME
        except Exception as ex:
            logger.error(f"Failed to decode styling rules: {ex}. Reverting to backup theme.", exc_info=True)
            return DEFAULT_THEME

    def get_color(self, token_name: str) -> str:
        """Retrieves hexadecimal color value matching token.
        
        Args:
            token_name: Color token key.
            
        Returns:
            Hex string mapping style.
        """
        colors = self.theme_data.get("colors", DEFAULT_THEME["colors"])
        return colors.get(token_name, DEFAULT_THEME["colors"].get(token_name, "#FFFFFF"))

    @property
    def theme_mode(self) -> str:
        """Gets visual mode (dark/light) configuration string."""
        return self.theme_data.get("theme_mode", DEFAULT_THEME["theme_mode"])

    def get_spacing(self, token: str, default: int = 8) -> int:
        """Retrieves layout spacing padding token.
        
        Args:
            token: Spacing token key (e.g. spacing_sm).
            default: Fallback default integer value.
        """
        layout = self.theme_data.get("layout", {})
        return int(layout.get(token, default))

    def get_radius(self, token: str, default: int = 8) -> int:
        """Retrieves layout corner radius token.
        
        Args:
            token: Radius token key (e.g. corner_radius_md).
            default: Fallback default integer value.
        """
        layout = self.theme_data.get("layout", {})
        return int(layout.get(token, default))

    def get_font(self, size_token: str, weight: str = "normal") -> tuple[str, int, str]:
        """Retrieves a font configurations tuple compatible with CustomTkinter labels.
        
        Args:
            size_token: Typography font size token key (e.g. font_size_md).
            weight: Typography font weight label ('normal', 'bold').
        """
        typography = self.theme_data.get("typography", {})
        family = typography.get("font_family", "Segoe UI")
        size = int(typography.get(size_token, 12))
        return (family, size, weight)
