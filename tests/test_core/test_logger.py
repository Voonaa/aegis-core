"""Unit tests for the Aegis logging system."""

import logging
import pytest
from pathlib import Path
from packages.core.logger import setup_logging, get_subsystem_logger, SubsystemLoggerAdapter

def test_logger_setup(tmp_path: Path) -> None:
    """Verifies that the logging bootstrap configuration runs successfully."""
    # We test setup_logging by running it. Since it configures handlers, 
    # we verify we can retrieve a subsystem logger without errors.
    setup_logging(log_level_name="DEBUG")
    
    logger = get_subsystem_logger("SYSTEM")
    assert isinstance(logger, SubsystemLoggerAdapter)
    assert logger.subsystem == "SYSTEM"

def test_subsystem_injection() -> None:
    """Verifies logger adapter correctly injects subsystem keys into log parameters."""
    mock_logger = logging.getLogger("mock_test")
    adapter = SubsystemLoggerAdapter(mock_logger, "NETWORK")
    
    # Process method should add extra dictionary variables
    msg, kwargs = adapter.process("Test network event message", {})
    assert "extra" in kwargs
    assert kwargs["extra"]["subsystem"] == "NETWORK"
    assert msg == "Test network event message"
