"""Hardware monitoring telemetry service for Aegis Toolkit."""

import random
from typing import Any
from packages.core.models.telemetry import TelemetryReport, CPUInfo, RAMInfo, DiskInfo, BatteryInfo, OSInfo
from packages.core.container import ServiceContainer
from packages.core.event_bus import EventBus
import packages.core.constants.events as events
from packages.core.logger import get_subsystem_logger

# Import HAL components
from packages.core.hal.cpu import CPUComponent
from packages.core.hal.ram import RAMComponent
from packages.core.hal.storage import StorageComponent
from packages.core.hal.battery import BatteryComponent
from packages.core.hal.os_env import OSComponent
from packages.core.hal.gpu import GPUComponent
from packages.core.hal.network import NetworkComponent

logger = get_subsystem_logger("HARDWARE")

class HardwareService:
    """Queries HAL telemetry components or simulates metrics in Demo Mode."""

    def __init__(self, container: ServiceContainer, demo_mode: bool = False) -> None:
        """Initialize the Hardware Service.
        
        Args:
            container: Service container reference.
            demo_mode: True to force simulated data generation.
        """
        self.container = container
        self.event_bus: EventBus = container.get("event_bus")
        self.health_engine = container.get("health_engine")
        self.demo_mode = demo_mode
        self._active: bool = False

        # Initialize HAL components
        self.cpu_comp = CPUComponent()
        self.ram_comp = RAMComponent()
        self.storage_comp = StorageComponent()
        self.battery_comp = BatteryComponent()
        self.os_comp = OSComponent()
        self.gpu_comp = GPUComponent()
        self.net_comp = NetworkComponent()

        logger.info(f"Hardware Service initialized. Mode: {'DEMO / SIMULATION' if demo_mode else 'LIVE'}")

    def start(self, master_window: any) -> None:
        """Starts the periodic telemetry gathering loop.
        
        Args:
            master_window: The main application CTk window reference to run timers.
        """
        self._active = True
        logger.info("Starting telemetry gathering services loop.")
        self._poll_tick(master_window)

    def stop(self) -> None:
        """Stops the telemetry polling loop."""
        self._active = False
        logger.info("Stopping telemetry gathering loop.")

    def _poll_tick(self, master_window: any) -> None:
        """Runs a tick, parses payload report, publishes events, schedules next run.
        
        Args:
            master_window: Window reference.
        """
        if not self._active:
            return

        try:
            report = self.gather_telemetry()
            # Publish event via EventBus
            self.event_bus.publish(events.TELEMETRY_UPDATED, report)
        except Exception as ex:
            logger.error(f"Error gathered telemetry indices: {ex}", exc_info=True)

        # Schedule next tick in 1000ms using Tkinter native loop
        master_window.after(1000, lambda: self._poll_tick(master_window))

    def gather_telemetry(self) -> TelemetryReport:
        """Assembles metrics into a packaged TelemetryReport payload.
        
        Returns:
            The compiled TelemetryReport dataclass.
        """
        if self.demo_mode:
            return self._gather_simulated_telemetry()
        return self._gather_live_telemetry()

    def _gather_live_telemetry(self) -> TelemetryReport:
        """Fetches parameters using HAL component wrappers."""
        # 1. CPU Telemetry
        cpu_info = self.cpu_comp.query()

        # 2. RAM Telemetry
        ram_info = self.ram_comp.query()

        # 3. Disk Telemetry
        disk_info = self.storage_comp.query()

        # 4. Battery Telemetry
        bat_info = self.battery_comp.query()

        # 5. OS Telemetry
        os_info = self.os_comp.query()

        # 6. GPU & Network Telemetry
        gpu_info = self.gpu_comp.query()
        net_info = self.net_comp.query()

        # Compute Health Score using registered HealthEngine
        health_score = self.health_engine.calculate_score(
            cpu_util=cpu_info.utilization,
            cpu_temp=cpu_info.temperature,
            ram_percent=ram_info.percentage,
            disk_health=disk_info.health_percent,
            battery_health=bat_info.health_percent,
            virt_conflict=os_info.virtualization_conflict
        )

        return TelemetryReport(
            cpu=cpu_info, 
            ram=ram_info, 
            disk=disk_info, 
            battery=bat_info, 
            os=os_info,
            health_score=health_score,
            gpu_model=gpu_info.model_name,
            gpu_utilization=gpu_info.utilization,
            gpu_temperature=gpu_info.temperature,
            network_adapter=net_info.adapter_name,
            ip_address=net_info.ip_address,
            network_latency_ms=net_info.network_latency_ms
        )

    def _gather_simulated_telemetry(self) -> TelemetryReport:
        """Generates random simulated metrics."""
        cpu_util = round(random.uniform(8.0, 35.0), 1)
        cpu_temp = round(random.uniform(41.0, 52.0), 1)
        
        cpu_info = CPUInfo(
            utilization=cpu_util,
            temperature=cpu_temp,
            model_name=self.cpu_comp.cpu_name,
            frequency_ghz=3.3,
            voltage=1.12,
            power_draw_watts=round(random.uniform(6.5, 18.0), 1)
        )

        # Fluctuating RAM
        used_ram = round(random.uniform(6.8, 8.1), 2)
        ram_info = RAMInfo(
            used_gb=used_ram,
            total_gb=16.0,
            percentage=used_ram / 16.0
        )

        disk_info = DiskInfo(
            used_gb=84.2,
            total_gb=512.0,
            percentage=84.2 / 512.0,
            health_percent=96,
            status="Good",
            temperature=38.0,
            power_on_hours=1320,
            host_writes_gb=5420.2
        )

        # Changing battery level
        bat_info = BatteryInfo(
            percentage=92,
            is_charging=True,
            health_percent=92,
            time_remaining_mins=180,
            design_capacity_mwh=54000,
            current_capacity_mwh=51020,
            cycle_count=48
        )

        os_info = OSInfo(
            os_name="Windows 11 Pro (Simulation)",
            build_version="Build 26200",
            hyperv_active=True,
            virtualization_conflict=True
        )

        # Compute Health Score using registered HealthEngine
        health_score = self.health_engine.calculate_score(
            cpu_util=cpu_util,
            cpu_temp=cpu_temp,
            ram_percent=ram_info.percentage,
            disk_health=disk_info.health_percent,
            battery_health=bat_info.health_percent,
            virt_conflict=os_info.virtualization_conflict
        )

        return TelemetryReport(
            cpu=cpu_info, 
            ram=ram_info, 
            disk=disk_info, 
            battery=bat_info, 
            os=os_info,
            health_score=health_score,
            gpu_model="NVIDIA GeForce RTX 3050 Laptop (Simulated)",
            gpu_utilization=round(random.uniform(2.0, 15.0), 1),
            gpu_temperature=round(random.uniform(38.0, 48.0), 1),
            network_adapter="Intel(R) Wi-Fi 6E AX211 (Simulated)",
            ip_address="192.168.1.124",
            network_latency_ms=round(random.uniform(1.0, 8.0), 1)
        )
