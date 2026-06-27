import os
import tempfile
import shutil
import unittest
from pathlib import Path
from packages.core.container import ServiceContainer
from packages.core.bootstrap import bootstrap_services

class TestBootstrap(unittest.TestCase):
    def setUp(self):
        # Create temp directories for profiles and plugins, and temp file for config
        self.temp_dir = tempfile.mkdtemp()
        self.profiles_dir = Path(self.temp_dir) / "profiles"
        self.plugins_dir = Path(self.temp_dir) / "plugins"
        self.config_file = Path(self.temp_dir) / "settings.json"
        
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs(self.plugins_dir, exist_ok=True)
        
        self.default_settings = {
            "app_name": "Aegis Test",
            "version": "1.0.0",
            "log_level": "INFO",
            "telemetry_interval_ms": 1000,
            "admin_required": False
        }
        self.container = ServiceContainer()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_bootstrap_services_registration(self):
        # Trigger bootstrapping of services
        bootstrap_services(
            container=self.container,
            profiles_dir=self.profiles_dir,
            plugins_dir=self.plugins_dir,
            config_file=self.config_file,
            default_settings=self.default_settings
        )
        
        # Verify core components are successfully registered in the container
        self.assertIsNotNone(self.container.get("config"))
        self.assertIsNotNone(self.container.get("theme"))
        self.assertIsNotNone(self.container.get("privilege_service"))
        self.assertIsNotNone(self.container.get("event_bus"))
        self.assertIsNotNone(self.container.get("job_manager"))
        self.assertIsNotNone(self.container.get("repair_service"))
        self.assertIsNotNone(self.container.get("maintenance_service"))
        self.assertIsNotNone(self.container.get("health_engine"))
        self.assertIsNotNone(self.container.get("profile_mgr"))
        self.assertIsNotNone(self.container.get("recommendation_service"))
        self.assertIsNotNone(self.container.get("plugin_loader"))
        self.assertIsNotNone(self.container.get("command_registry"))
        self.assertIsNotNone(self.container.get("report_service"))
        self.assertIsNotNone(self.container.get("hardware_service"))
        self.assertIsNotNone(self.container.get("intelligence_service"))
        self.assertIsNotNone(self.container.get("optimization_service"))
        self.assertIsNotNone(self.container.get("telemetry_repository"))
        self.assertIsNotNone(self.container.get("telemetry_history_service"))
        self.assertIsNotNone(self.container.get("export_service"))
        self.assertIsNotNone(self.container.get("trend_analysis_service"))

if __name__ == "__main__":
    unittest.main()
