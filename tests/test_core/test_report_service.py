import os
import json
import unittest
from unittest.mock import MagicMock
from packages.core.container import ServiceContainer
from packages.core.services.report_service import ReportService
from packages.core.models.telemetry import TelemetryReport, CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo
import packages.core.constants.paths as paths

class TestReportService(unittest.TestCase):
    def setUp(self):
        self.container = ServiceContainer()
        
        # Setup mock hardware telemetry report
        self.cpu_mock = CPUInfo(
            utilization=23.5,
            temperature=55.0,
            model_name="Intel Test i7",
            frequency_ghz=3.2,
            voltage=1.2,
            power_draw_watts=45.0
        )
        self.ram_mock = RAMInfo(
            used_gb=8.0,
            total_gb=16.0,
            percentage=50.0
        )
        self.disk_mock = DiskInfo(
            used_gb=200.0,
            total_gb=500.0,
            percentage=40.0,
            health_percent=98,
            status="Healthy",
            temperature=38.0,
            power_on_hours=1200,
            host_writes_gb=4500.0
        )
        self.battery_mock = BatteryInfo(
            percentage=85,
            is_charging=False,
            health_percent=95,
            time_remaining_mins=180,
            design_capacity_mwh=60000,
            current_capacity_mwh=57000,
            cycle_count=45
        )
        self.os_mock = OSInfo(
            os_name="Windows 11 Test",
            build_version="22631",
            hyperv_active=True,
            virtualization_conflict=False
        )
        self.report_mock = TelemetryReport(
            cpu=self.cpu_mock,
            ram=self.ram_mock,
            disk=self.disk_mock,
            battery=self.battery_mock,
            os=self.os_mock,
            health_score=92,
            gpu_model="NVIDIA Test GPU",
            gpu_utilization=15.0,
            gpu_temperature=42.0,
            network_adapter="Intel Ethernet",
            ip_address="192.168.1.100",
            network_latency_ms=12.5
        )
        
        self.hardware_service = MagicMock()
        self.hardware_service.gather_telemetry.return_value = self.report_mock
        
        self.profile_mgr = MagicMock()
        self.profile_mgr.get_profile_name.return_value = "TEST-PROFILE"
        
        self.rec_svc = MagicMock()
        self.rec_svc.analyze_issues.return_value = []
        
        self.container.register("hardware_service", self.hardware_service)
        self.container.register("profile_mgr", self.profile_mgr)
        self.container.register("recommendation_service", self.rec_svc)
        
        self.report_service = ReportService(container=self.container)

    def test_generate_report_writes_files(self):
        # Trigger report generation
        res = self.report_service.generate_report()
        self.assertIn("Report generated successfully", res)
        
        temp_dir = paths.TEMP_DIR
        json_path = temp_dir / "system_report.json"
        md_path = temp_dir / "system_report.md"
        
        self.assertTrue(json_path.exists())
        self.assertTrue(md_path.exists())
        
        # Verify JSON report structure
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["system"]["os"], "Windows 11 Test")
            self.assertEqual(data["processor"]["model"], "Intel Test i7")
            self.assertEqual(data["memory"]["percentage"], 50.0)
            self.assertEqual(data["storage"]["health_percent"], 98)
            self.assertEqual(data["battery"]["charge_percent"], 85)
            self.assertEqual(data["graphics"]["gpu_model"], "NVIDIA Test GPU")
            self.assertEqual(data["network"]["ip_address"], "192.168.1.100")
            
        # Verify MD report highlights
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("# Aegis Diagnostics System Report", content)
            self.assertIn("Windows 11 Test", content)
            self.assertIn("Intel Test i7", content)
            self.assertIn("NVIDIA Test GPU", content)
            self.assertIn("Intel Ethernet", content)

        # Cleanup files
        if json_path.exists():
            os.remove(json_path)
        if md_path.exists():
            os.remove(md_path)

if __name__ == "__main__":
    unittest.main()
