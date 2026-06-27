"""Custom exception categories for Aegis Toolkit."""

class AegisError(Exception):
    """Base class for all Aegis Toolkit exceptions."""
    pass

class ConfigurationError(AegisError):
    """Raised when configuration parsing or validation checks fail."""
    pass

class PluginError(AegisError):
    """Raised when third-party dynamic plugins loading fails."""
    pass

class HealthError(AegisError):
    """Raised when Health Engine scoring calculations fail."""
    pass

class RepairError(AegisError):
    """Raised when Windows OS integrity repairs subprocess fails."""
    pass

class HardwareError(AegisError):
    """Raised when querying lower-level motherboard telemetry or WMI logs fails."""
    pass
