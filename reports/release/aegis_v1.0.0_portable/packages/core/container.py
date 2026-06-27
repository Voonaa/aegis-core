"""Service Container (Dependency Injection Container) for Aegis Toolkit."""

from typing import Any
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class ServiceContainer:
    """Central registry mapping instances and services (Service Locator Pattern)."""

    _instance: "ServiceContainer | None" = None

    def __new__(cls) -> "ServiceContainer":
        """Enforces Singleton design pattern for the Container."""
        if cls._instance is None:
            cls._instance = super(ServiceContainer, cls).__new__(cls)
            cls._instance._services = {}
            logger.info("Service Container instance initialized.")
        return cls._instance

    def register(self, name: str, service_instance: Any) -> None:
        """Register a service instance under a unique identifier string.
        
        Args:
            name: Service registration key.
            service_instance: Instantiated object.
        """
        self._services[name] = service_instance
        logger.info(f"Service registered: '{name}' -> {type(service_instance).__name__}")

    def get(self, name: str) -> Any:
        """Fetch a registered service instance.
        
        Args:
            name: Service registration key.
            
        Returns:
            The registered service instance.
            
        Raises:
            KeyError: If the requested service is not registered.
        """
        if name not in self._services:
            logger.critical(f"ServiceContainer: Requested unregistered service: '{name}'")
            raise KeyError(f"Requested unregistered service: '{name}'")
        return self._services[name]

    def has(self, name: str) -> bool:
        """Checks if a service is registered.
        
        Args:
            name: Service registration key.
            
        Returns:
            True if registered, False otherwise.
        """
        return name in self._services
