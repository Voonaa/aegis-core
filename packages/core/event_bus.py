"""Observer pattern Event Bus for decoupling systems in Aegis Toolkit."""

from typing import Callable, Any
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class EventBus:
    """Centralized event publisher-subscriber communication bus."""

    def __init__(self) -> None:
        """Initialize the Event Bus."""
        self._subscribers: dict[str, list[Callable[..., None]]] = {}

    def subscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        """Subscribe to a specific event.
        
        Args:
            event_name: Unique event string identifier.
            callback: Function to run when the event publishes.
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        
        if callback not in self._subscribers[event_name]:
            self._subscribers[event_name].append(callback)
            logger.debug(f"EventBus: Registered subscriber for event '{event_name}'")

    def unsubscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        """Unsubscribe from a specific event.
        
        Args:
            event_name: Unique event string identifier.
            callback: Function to remove.
        """
        if event_name in self._subscribers:
            try:
                self._subscribers[event_name].remove(callback)
                logger.debug(f"EventBus: Removed subscriber from event '{event_name}'")
            except ValueError:
                pass

    def publish(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """Publish an event to all active subscribers.
        
        Args:
            event_name: Unique event string identifier.
            args: Positional arguments to pass to subscribers.
            kwargs: Keyword arguments to pass to subscribers.
        """
        if event_name not in self._subscribers or not self._subscribers[event_name]:
            return

        logger.debug(f"EventBus: Publishing event '{event_name}' to {len(self._subscribers[event_name])} subscribers")
        for callback in self._subscribers[event_name]:
            try:
                callback(*args, **kwargs)
            except Exception as ex:
                logger.error(f"EventBus: Error calling subscriber for event '{event_name}': {ex}", exc_info=True)
                # Avoid propagating subscriber failures to block publishers
