"""Example Aegis plugin module demonstrating lifecycle hook integrations."""

def initialize(container) -> None:
    """Invoked when the plugin is discovered and registered.
    
    Args:
        container: DI Service container reference.
    """
    # Fetch log subsystem to print status logs
    logger = container.get("theme") # Test DI queries
    print("[Plugin SDK] Extension initialized inside Service Container registry.")

def start() -> None:
    """Invoked when the initialization is complete."""
    print("[Plugin SDK] Extension start routine triggered.")

def dispose() -> None:
    """Invoked when the application exits and unloads active plugins."""
    print("[Plugin SDK] Extension teardown routine triggered.")
