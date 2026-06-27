"""Directory layout constants for Aegis Toolkit."""

from pathlib import Path

# Resolve absolute workspace paths
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_DIR: Path = PROJECT_ROOT / "apps" / "desktop" / "config"
PROFILES_DIR: Path = CONFIG_DIR / "profiles"

LOGS_DIR: Path = PROJECT_ROOT / "logs"
PLUGINS_DIR: Path = PROJECT_ROOT / "plugins"
BACKUP_DIR: Path = PROJECT_ROOT / "backup"
TEMP_DIR: Path = PROJECT_ROOT / "temp"
