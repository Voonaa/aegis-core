"""Directory layout constants for Aegis Toolkit.

Separates install-time (read-only) paths from runtime user-data (writable) paths.
- INSTALL_DIR : where the app is installed (may be Program Files — READ ONLY)
- APPDATA_DIR : per-user writable data directory (LOCALAPPDATA\AegisCore)
"""

import os
from pathlib import Path

# ── Install-time paths (read-only after install) ─────────────────────────────
INSTALL_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent

# Source assets — only read at runtime
PLUGINS_DIR: Path = INSTALL_DIR / "plugins"

# ── User-writable data paths (LOCALAPPDATA\AegisCore) ────────────────────────
APPDATA_DIR: Path = Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))) / "AegisCore"

CONFIG_DIR:   Path = APPDATA_DIR / "config"
PROFILES_DIR: Path = CONFIG_DIR / "profiles"
LOGS_DIR:     Path = APPDATA_DIR / "logs"
BACKUP_DIR:   Path = APPDATA_DIR / "backup"
TEMP_DIR:     Path = APPDATA_DIR / "temp"

# Backwards-compatible alias
PROJECT_ROOT: Path = INSTALL_DIR
