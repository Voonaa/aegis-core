"""Structured logging engine for Aegis Toolkit."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

# Define logging standard format
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | [%(subsystem)s] | %(message)s"
DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

class SubsystemLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter to inject subsystem values into log output formats."""

    def __init__(self, logger: logging.Logger, subsystem: str = "SYSTEM") -> None:
        """Initialize the logger adapter with a target subsystem."""
        super().__init__(logger, {"subsystem": subsystem})
        self.subsystem = subsystem

    def process(self, msg: str, kwargs: dict) -> tuple[str, dict]:
        """Inject the subsystem parameter into the extra arguments log dictionary."""
        extra = kwargs.setdefault("extra", {})
        extra["subsystem"] = self.subsystem
        return msg, kwargs

def setup_logging(log_level_name: str = "INFO") -> None:
    """Configures root rotating file logs and console standard outputs.
    
    Args:
        log_level_name: Target minimum severity log level string.
    """
    # Parse logging level
    level: int = getattr(logging, log_level_name.upper(), logging.INFO)

    # Determine absolute path paths
    project_root: Path = Path(__file__).resolve().parent.parent.parent
    log_dir: Path = project_root / "logs"
    
    # Dynamically create directories
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file: Path = log_dir / "aegis.log"

    # Fetch root logger
    root_logger: logging.Logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Formatter configuration
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # Rotating File Handler
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    root_logger.addHandler(file_handler)

    # Console stdout Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    root_logger.addHandler(console_handler)

    # Log initial bootstrap event using SYSTEM context
    adapter = SubsystemLoggerAdapter(root_logger, "SYSTEM")
    adapter.info(f"Logging system booted at level {log_level_name.upper()}. Log file: {log_file}")

def get_subsystem_logger(subsystem: str) -> SubsystemLoggerAdapter:
    """Returns a pre-configured logger adapter with a targeted subsystem tag.
    
    Args:
        subsystem: The targeted subsystem name (e.g. SYSTEM, USER, HARDWARE).
        
    Returns:
        SubsystemLoggerAdapter mapping subsystem context to messages.
    """
    # Retrieve base logger for the library
    logger = logging.getLogger("aegis")
    return SubsystemLoggerAdapter(logger, subsystem)
