"""GPU telemetry harvester module for Aegis HAL."""

from typing import NamedTuple
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("HARDWARE")

class GPUInfo(NamedTuple):
    """Encapsulates GPU controller parameters."""
    model_name: str
    driver_version: str
    temperature: float
    adapter_ram_mb: int

class GPUComponent:
    """GPU telemetry module querying WMI video controllers namespaces."""

    def __init__(self) -> None:
        """Initialize the GPU Component."""
        self._capabilities = {
            "gpu_polling": True,
            "temp_polling": False
        }

    def query(self) -> GPUInfo:
        """Queries WMI controllers.
        
        Returns:
            GPUInfo tuple mapping.
        """
        model = "AMD Radeon Graphics"
        driver = "31.0.12028.2"
        vram = 2048
        temp = 0.0

        try:
            import wmi
            w = wmi.WMI()
            controllers = w.Win32_VideoController()
            if controllers and len(controllers) > 0:
                gpu = controllers[0]
                model = getattr(gpu, "Name", model)
                driver = getattr(gpu, "DriverVersion", driver)
                # AdapterRAM is returned in bytes, convert to MB
                bytes_ram = getattr(gpu, "AdapterRAM", 0)
                if bytes_ram:
                    vram = int(bytes_ram // (1024 ** 2))
        except Exception as ex:
            logger.warning(f"GPU WMI video controller query failed: {ex}. Using default placeholders.")

        return GPUInfo(
            model_name=model,
            driver_version=driver,
            temperature=temp,
            adapter_ram_mb=vram
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
