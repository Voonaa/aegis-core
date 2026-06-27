"""Unit tests targeting application configuration and settings parsing."""

import json
import pytest
from pathlib import Path
from packages.core.container import ServiceContainer
from packages.core.config_manager import ConfigManager
from apps.desktop.ui.theme import ThemeManager
from packages.core.command_registry import CommandRegistry
from packages.core.services.health_service import HealthService as HealthEngine
from packages.core.profile_manager import ProfileManager
from packages.core.plugins.loader import PluginLoader
from packages.core.event_bus import EventBus
from packages.core.services.privilege_service import PrivilegeService
from packages.core.services.repair_service import RepairService
from packages.core.services.maintenance_service import MaintenanceService
from packages.core.jobs import JobManager
from packages.core.services.recommendation import RecommendationService
from apps.desktop.app import AegisApp, DEFAULT_SETTINGS

@pytest.fixture(autouse=True)
def setup_test_container(tmp_path: Path) -> ServiceContainer:
    """Fixture to build and configure a fresh ServiceContainer instance."""
    # Retrieve/create container
    container = ServiceContainer()
    
    # Re-register test mock values
    config_file = tmp_path / "settings.json"
    config_mgr = ConfigManager(config_path=config_file, default_settings=DEFAULT_SETTINGS)
    container._services["config"] = config_mgr  # Direct reset bypasses standard logging checks

    theme_file = tmp_path / "theme.json"
    theme_mgr = ThemeManager(config_path=theme_file)
    container._services["theme"] = theme_mgr

    container._services["health_engine"] = HealthEngine()
    container._services["profile_manager"] = ProfileManager(profiles_dir=tmp_path)
    container._services["plugin_loader"] = PluginLoader(plugins_dir=tmp_path)
    container._services["command_registry"] = CommandRegistry()
    container._services["event_bus"] = EventBus()
    container._services["privilege_service"] = PrivilegeService()
    container._services["job_manager"] = JobManager(container=container)
    container._services["repair_service"] = RepairService(container=container)
    container._services["maintenance_service"] = MaintenanceService(container=container)
    container._services["recommendation_service"] = RecommendationService()
    
    return container

def test_fallback_settings(setup_test_container: ServiceContainer) -> None:
    """Verifies default settings are loaded if the file is missing."""
    container = setup_test_container
    config_mgr: ConfigManager = container.get("config")
    
    # Assert initial config values match defaults
    assert config_mgr.settings == DEFAULT_SETTINGS
    
    # Instantiate the application shell properties directly to test parsing fallback
    app = AegisApp(container)
    assert app.config == config_mgr
    app.destroy()

def test_loaded_settings(setup_test_container: ServiceContainer, tmp_path: Path) -> None:
    """Verifies that settings values are parsed correctly from files."""
    container = setup_test_container
    
    custom_settings = {
        "app_name": "Aegis Custom Test",
        "version": "1.2.3",
        "log_level": "DEBUG",
        "telemetry_interval_ms": 500,
        "admin_required": False
    }
    
    # Save custom overrides
    config_mgr: ConfigManager = container.get("config")
    config_mgr.settings = custom_settings
    config_mgr.save()
    
    # Instantiates AegisApp with container loaded custom values
    app = AegisApp(container)
    assert app.config.get("app_name") == "Aegis Custom Test"
    assert app.config.get("version") == "1.2.3"
    assert app.config.get("log_level") == "DEBUG"
    assert app.config.get("telemetry_interval_ms") == 500
    assert not app.config.get("admin_required")
    app.destroy()

def test_config_manager_set_and_get(tmp_path: Path) -> None:
    config_file = tmp_path / "settings.json"
    defaults = {"key1": "val1", "key2": "val2"}
    mgr = ConfigManager(config_path=config_file, default_settings=defaults)
    
    # Test initial get
    assert mgr.get("key1") == "val1"
    
    # Test set and auto-save
    mgr.set("key1", "new_val")
    assert mgr.get("key1") == "new_val"
    
    # Test get missing key with default
    assert mgr.get("missing_key", "fallback") == "fallback"

def test_config_manager_corrupt_file(tmp_path: Path) -> None:
    config_file = tmp_path / "corrupt_settings.json"
    # Write corrupt JSON content
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("not a valid json dictionary")
        
    defaults = {"app_name": "Aegis Default"}
    mgr = ConfigManager(config_path=config_file, default_settings=defaults)
    # Verify falls back to default settings
    assert mgr.get("app_name") == "Aegis Default"

def test_config_manager_save_error(tmp_path: Path) -> None:
    # Use directory path instead of file path to trigger OS IO exception on save
    invalid_path = tmp_path / "directory_instead_of_file"
    invalid_path.mkdir()
    
    defaults = {"app_name": "Aegis Default"}
    mgr = ConfigManager(config_path=invalid_path, default_settings=defaults)
    # Save call should not crash despite exception
    mgr.save()

