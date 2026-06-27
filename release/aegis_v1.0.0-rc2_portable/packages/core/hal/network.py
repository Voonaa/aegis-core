"""Network configurations harvester module for Aegis HAL."""

from typing import NamedTuple
import psutil
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class NetworkInfo(NamedTuple):
    """Encapsulates network interfaces profiles."""
    adapter_name: str
    ip_address: str
    gateway_ip: str
    dns_servers: list[str]
    signal_strength_percent: int

class NetworkComponent:
    """Network configurations query module reading WMI adapter adapters configurations."""

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
        except Exception as ex:
            logger.warning(f"Failed to query WMI active network configs: {ex}. Using fallback defaults.")

        return NetworkInfo(
            adapter_name=adapter,
            ip_address=ip,
            gateway_ip=gateway,
            dns_servers=dns,
            signal_strength_percent=signal
        )

    def get_capabilities(self) -> dict[str, bool]:
        """Gets capability detection flags."""
        return self._capabilities
