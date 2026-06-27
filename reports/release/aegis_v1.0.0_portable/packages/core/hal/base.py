"""Base interfaces and capabilities protocols for the Hardware Abstraction Layer."""

from typing import Protocol, Any

class IHalComponent(Protocol):
    """Protocol defining standard methods for all HAL components."""

    def query(self) -> Any:
        """Queries OS APIs and returns the mapped hardware data structure."""
        ...

    def get_capabilities(self) -> dict[str, bool]:
        """Returns capability detection flags (feature support statuses)."""
        ...
