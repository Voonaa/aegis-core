"""System Diagnostics Report Generator Service for Aegis Toolkit."""

import json
from pathlib import Path
from packages.core.models.telemetry import TelemetryReport
from packages.core.container import ServiceContainer
import packages.core.constants.paths as paths
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class ReportService:
    """Compiles and exports system diagnostic reports in Markdown and JSON formats."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Report Service.
        
        Args:
            container: Service container reference.
        """
        self.container = container
        logger.info("Report Service initialized.")

    def generate_report(self) -> str:
        """Queries telemetry service, compiles, and writes diagnostics reports to disk.
        
        Returns:
            Success message detailing written paths.
        """
        try:
            hardware_service = self.container.get("hardware_service")
            profile_mgr = self.container.get("profile_mgr")
            
            # Fetch latest data payload
            report: TelemetryReport = hardware_service.gather_telemetry()
            profile_name = profile_mgr.get_profile_name()
            
            # Resolve temp folders
            temp_dir: Path = paths.TEMP_DIR
            temp_dir.mkdir(parents=True, exist_ok=True)

            json_path = temp_dir / "system_report.json"
            md_path = temp_dir / "system_report.md"

            # 1. Compile JSON report
            report_dict = {
                "system": {
                    "os": report.os.os_name,
                    "build": report.os.build_version,
                    "profile": profile_name,
                    "hyperv_active": report.os.hyperv_active,
                    "virtualization_conflict": report.os.virtualization_conflict
                },
                "processor": {
                    "model": report.cpu.model_name,
                    "frequency_ghz": report.cpu.frequency_ghz,
                    "utilization_percent": report.cpu.utilization,
                    "temperature_c": report.cpu.temperature
                },
                "memory": {
                    "used_gb": report.ram.used_gb,
                    "total_gb": report.ram.total_gb,
                    "percentage": report.ram.percentage
                },
                "graphics": {
                    "gpu_model": report.gpu_model
                },
                "storage": {
                    "used_gb": report.disk.used_gb,
                    "total_gb": report.disk.total_gb,
                    "health_percent": report.disk.health_percent,
                    "status": report.disk.status
                },
                "battery": {
                    "charge_percent": report.battery.percentage,
                    "is_charging": report.battery.is_charging,
                    "health_percent": report.battery.health_percent,
                    "time_remaining_mins": report.battery.time_remaining_mins
                },
                "network": {
                    "adapter": report.network_adapter,
                    "ip_address": report.ip_address
                },
                "health_score": report.health_score
            }

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(report_dict, f, indent=2)

            # 2. Compile Markdown report
            md_content = self._compile_markdown_report(report, profile_name)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            logger.info(f"Diagnostics reports exported successfully: {md_path}")
            return f"Report generated successfully!\n  - JSON: {json_path}\n  - Markdown: {md_path}"

        except Exception as ex:
            logger.error(f"Failed to generate system report: {ex}", exc_info=True)
            return f"Error: Diagnostics report compiler failed: {ex}"

    def _compile_markdown_report(self, report: TelemetryReport, profile_name: str) -> str:
        """Assembles Markdown content layout."""
        # Query matching engine
        rec_svc = self.container.get("recommendation_service")
        advice_items = rec_svc.get_recommendations(report)

        advices = []
        for item in advice_items:
            icon = "[x]" if item["priority"] == "LOW" else "[ ]"
            advices.append(f"{icon} **{item['title']}** [{item['priority']}]: {item['action_message']}")
        
        advice_str = "\n".join(advices)

        return f"""# Aegis Diagnostics System Report

## Summary
* **Active Profile**: {profile_name}
* **Global Health Rating**: **{report.health_score} / 100**
* **Operating System**: {report.os.os_name} ({report.os.build_version})

---

## Hardware Telemetry

### Processor (CPU)
* **Model**: {report.cpu.model_name}
* **Frequency**: {report.cpu.frequency_ghz} GHz
* **Active Load**: {report.cpu.utilization} %
* **Thermals**: {report.cpu.temperature} °C

### Graphics (GPU)
* **Controller**: {report.gpu_model}

### Memory (RAM)
* **Configuration**: {report.ram.used_gb} GB used of {report.ram.total_gb} GB ({int(report.ram.percentage * 100)}%)

### Storage (SSD/HDD)
* **Utilization**: {report.disk.used_gb} GB used of {report.disk.total_gb} GB
* **S.M.A.R.T wear life**: {report.disk.health_percent}%
* **Drive Status**: {report.disk.status}

### Battery Status
* **Charge**: {report.battery.percentage}% ({"Charging" if report.battery.is_charging else "Discharging"})
* **Health Capacity**: {report.battery.health_percent}%
* **Estimated Time Remaining**: {report.battery.time_remaining_mins} minutes

### Network Configuration
* **Active Adapter**: {report.network_adapter}
* **IP Address**: {report.ip_address}

---

## Aegis Recommendations
{advice_str}
"""
