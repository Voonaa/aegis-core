"""Standard event identifier constants for Aegis Toolkit."""

# Telemetry events
TELEMETRY_UPDATED: str = "telemetry:updated"

# UI Navigation events
PAGE_CHANGED: str = "ui:page_changed"
NOTIFICATION_TRIGGERED: str = "ui:notification_triggered"

# Configuration / Profile events
PROFILE_LOADED: str = "config:profile_loaded"
CONFIG_RELOADED: str = "config:reloaded"

# Console commands events
COMMAND_EXECUTED: str = "console:command_executed"

# Job / Task manager events
JOB_STATUS_CHANGED: str = "job:status_changed"
JOB_PROGRESS_UPDATED: str = "job:progress_updated"
