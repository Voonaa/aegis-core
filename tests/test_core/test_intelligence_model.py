"""Unit tests for the IntelligenceAlert data model."""

import pytest
from packages.core.models.intelligence import IntelligenceAlert


def test_alert_creation_with_all_fields() -> None:
    """IntelligenceAlert must be constructable with all required fields."""
    alert = IntelligenceAlert(
        title="Test Alert",
        message="This is a test message.",
        severity="WARNING",
        category="SECURITY",
        action="Take corrective action."
    )

    assert alert.title == "Test Alert"
    assert alert.message == "This is a test message."
    assert alert.severity == "WARNING"
    assert alert.category == "SECURITY"
    assert alert.action == "Take corrective action."


def test_alert_default_action_is_empty_string() -> None:
    """The `action` field must default to an empty string when not provided."""
    alert = IntelligenceAlert(
        title="No Action Alert",
        message="No action needed.",
        severity="INFO",
        category="SYSTEM",
    )

    assert alert.action == ""


def test_alert_is_frozen_immutable() -> None:
    """IntelligenceAlert is a frozen dataclass and must not be mutable after creation."""
    alert = IntelligenceAlert(
        title="Immutable Alert",
        message="Cannot change me.",
        severity="INFO",
        category="SYSTEM",
    )

    with pytest.raises((AttributeError, TypeError)):
        alert.title = "Modified"  # type: ignore[misc]


def test_alert_equality_by_value() -> None:
    """Two IntelligenceAlert instances with identical fields must compare as equal."""
    a = IntelligenceAlert(title="A", message="M", severity="INFO", category="SYSTEM")
    b = IntelligenceAlert(title="A", message="M", severity="INFO", category="SYSTEM")

    assert a == b


def test_alert_repr_contains_title() -> None:
    """The repr of an IntelligenceAlert must include the title for debuggability."""
    alert = IntelligenceAlert(
        title="Debug Alert",
        message="Check me.",
        severity="WARNING",
        category="PERFORMANCE",
    )

    assert "Debug Alert" in repr(alert)
