"""Telemetry data models using Python dataclasses for Aegis Toolkit."""

from dataclasses import dataclass

@dataclass(frozen=True)
class CPUInfo:
    """CPU hardware telemetry variables."""
    utilization: float
    temperature: float
    model_name: str
    frequency_ghz: float


@dataclass(frozen=True)
class RAMInfo:
    """RAM telemetry distribution."""
    used_gb: float
    total_gb: float
    percentage: float


@dataclass(frozen=True)
class DiskInfo:
    """Storage partition parameters and S.M.A.R.T integrity fields."""
    used_gb: float
    total_gb: float
    percentage: float
    health_percent: int
    status: str


@dataclass(frozen=True)
class BatteryInfo:
    """Battery diagnostic parameters."""
    percentage: int
    is_charging: bool
    health_percent: int
    time_remaining_mins: int


@dataclass(frozen=True)
class OSInfo:
    """Windows kernel parameters and system settings flags."""
    os_name: str
    build_version: str
    hyperv_active: bool
    virtualization_conflict: bool


@dataclass(frozen=True)
class TelemetryReport:
    """Master telemetry payload packaging component metrics."""
    cpu: CPUInfo
    ram: RAMInfo
    disk: DiskInfo
    battery: BatteryInfo
    os: OSInfo
    health_score: int
    gpu_model: str
    network_adapter: str
    ip_address: str
