"""Device profile manager querying motherboard identifiers and parsing configurations."""

import json
from pathlib import Path
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class ProfileManager:
    """Manages dynamic hardware motherboard queries and overlays matching profile JSON assets."""

    def __init__(self, profiles_dir: Path) -> None:
        """Initialize the Profile Manager.
        
        Args:
            profiles_dir: Path to directory containing laptop profile JSON overlays.
        """
        self.profiles_dir = profiles_dir
        self.manufacturer: str = "GENERIC"
        self.model: str = "WINDOWS DEVICE"
        self.profile_name: str = "generic_windows"
        self.profile_data: dict = {}
        
        self.detect_profile()

    def detect_profile(self) -> str:
        """Queries WMI motherboard identifiers to activate corresponding configurations.
        
        Returns:
            Matched profile name descriptor string.
        """
        try:
            import wmi
            w = wmi.WMI()
            boards = w.Win32_BaseBoard()
            if boards and len(boards) > 0:
                self.manufacturer = boards[0].Manufacturer.strip()
                self.model = boards[0].Product.strip()
                logger.info(f"Motherboard detected: Manufacturer='{self.manufacturer}', Model='{self.model}'")
        except Exception as ex:
            logger.warning(f"Failed to query motherboard baseboard via WMI: {ex}. Using generic defaults.")

        # Normalize name for profile match
        mfr_lower = self.manufacturer.lower()
        model_lower = self.model.lower()

        # Check keyword matches
        if "advan" in mfr_lower or "workplus" in model_lower:
            self.profile_name = "advan_workplus"
            profile_file = self.profiles_dir / "advan_workplus.json"
        else:
            self.profile_name = "generic_windows"
            profile_file = self.profiles_dir / "generic_windows.json"

        # Load matched file configs
        self.profile_data = self._load_profile_file(profile_file)
        logger.info(f"Active device profile mapped: '{self.profile_name}' from {profile_file}")
        return self.profile_name

    def _load_profile_file(self, file_path: Path) -> dict:
        """Loads profile configuration values from the JSON file."""
        if not file_path.exists():
            logger.error(f"Target profile overlay file not found: {file_path}")
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as ex:
            logger.error(f"Failed to parse profile overlay file {file_path}: {ex}", exc_info=True)
            return {}

    def get_profile_data(self) -> dict:
        """Gets currently active loaded configuration properties."""
        return self.profile_data

    def get_profile_name(self) -> str:
        """Gets active profile name descriptor string."""
        return self.profile_data.get("profile_name", f"{self.manufacturer} {self.model}")
