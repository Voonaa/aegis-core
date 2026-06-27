"""Network configurations harvester module for Aegis HAL."""

import psutil
import subprocess
import re
from typing import NamedTuple
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class NetworkInfo(NamedTuple):
    """Encapsulates network interfaces profiles."""
    adapter_name: str
    ip_address: str
    gateway_ip: str
    dns_servers: list[str]
    signal_strength_percent: int
    network_latency_ms: float


class NetworkComponent:
    """Network configurations query module reading WMI adapter configurations."""

    def __init__(self) -> None:
        """Initialize the Network Component."""
        self._capabilities = {
            "network_polling": True,
            "signal_polling": False
        }

    def query(self) -> NetworkInfo:
        """Queries network adapters configs.
        
        Returns:
            NetworkInfo metrics mapping.
        """
        adapter = "Wi-Fi Adapter"
        ip = "192.168.1.100"
        gateway = "192.168.1.1"
        dns = ["8.8.8.8", "1.1.1.1"]
        signal = 88
        latency = 2.0

        try:
            import wmi
            w = wmi.WMI()
            configs = w.Win32_NetworkAdapterConfiguration(IPEnabled=True)
            if configs and len(configs) > 0:
                conf = configs[0]
                adapter = getattr(conf, "Description", adapter)
                
                # Check IP Addresses
                ips = getattr(conf, "IPAddress", None)
                if ips and len(ips) > 0:
                    ip = ips[0]

                # Check Gateway IP
                gateways = getattr(conf, "DefaultIPGateway", None)
                if gateways and len(gateways) > 0:
                    gateway = gateways[0]

                # Check DNS search orders
                dns_search = getattr(conf, "DNSServerSearchOrder", None)
                if dns_search:
                    dns = list(dns_search)

            # Measure ping latency to gateway
            # timeout=2s ensures this never blocks the telemetry polling loop,
            # even if the gateway is unreachable or behind a firewall.
            if gateway:
                try:
                    out = subprocess.run(
                        ["ping", "-n", "1", "-w", "500", gateway],
                        capture_output=True,
                        text=True,
                        timeout=2,
                        creationflags=0x08000000  # CREATE_NO_WINDOW
                    )
                    if out.returncode == 0:
                        match = re.search(r"time[=<](\d+)ms", out.stdout)
                        if match:
                            latency = float(match.group(1))
                            logger.debug(f"Gateway ping latency: {latency} ms to {gateway}")
                except subprocess.TimeoutExpired:
                    logger.debug(f"Gateway ping timed out after 2s. Latency marked as unavailable.")
                    latency = -1.0
                except Exception as ex:
                    logger.debug(f"Gateway ping failed: {ex}")

        except Exception as ex:
            logger.warning(f"Failed to query WMI active network configs: {ex}. Using fallback defaults.")

        return NetworkInfo(
            adapter_name=adapter,
            ip_address=ip,
            gateway_ip=gateway,
            dns_servers=dns,
            signal_strength_percent=signal,
            network_latency_ms=latency
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
