"""Core Interface protocols for Dependency Injection in Aegis Toolkit."""

from typing import Protocol, Any, Callable
from pathlib import Path

class IService(Protocol):
    """Base Protocol for all application service structures."""
    def start(self) -> None:
        """Starts the service execution loop."""
        ...
    def stop(self) -> None:
        """Stops the service execution loop."""
        ...


class IConfigManager(Protocol):
    """Protocol for Configuration reading and writing."""
    def reload(self) -> None:
        ...
    def save(self) -> None:
        ...
    def get(self, key: str, default: Any = None) -> Any:
        ...
    def set(self, key: str, value: Any) -> None:
        ...


class IThemeManager(Protocol):
    """Protocol for Style Theme loaders."""
    def get_color(self, token_name: str) -> str:
        ...
    @property
    def theme_mode(self) -> str:
        ...


class IEventBus(Protocol):
    """Protocol for Event Bus observers."""
    def subscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        ...
    def unsubscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        ...
    def publish(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        ...


class IHealthEngine(Protocol):
    """Protocol for scoring calculators."""
    def calculate_score(self) -> int:
        ...


class IProfileManager(Protocol):
    """Protocol for Dynamic Profiling loaders."""
    def detect_profile(self) -> str:
        ...
