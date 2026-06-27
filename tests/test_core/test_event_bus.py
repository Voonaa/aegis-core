"""Unit tests for the EventBus publish-subscribe system."""

import pytest
from packages.core.event_bus import EventBus


@pytest.fixture
def bus() -> EventBus:
    """Returns a fresh EventBus instance for each test."""
    return EventBus()


def test_subscribe_and_receive(bus: EventBus) -> None:
    """Subscriber callback must be called when a matching event is published."""
    received = []

    def handler(value: str) -> None:
        received.append(value)

    bus.subscribe("test.event", handler)
    bus.publish("test.event", "hello")

    assert received == ["hello"]


def test_unsubscribe_stops_events(bus: EventBus) -> None:
    """After unsubscribing, the callback must not be called on subsequent publishes."""
    received = []

    def handler(value: str) -> None:
        received.append(value)

    bus.subscribe("test.event", handler)
    bus.unsubscribe("test.event", handler)
    bus.publish("test.event", "should_not_arrive")

    assert received == []


def test_multiple_subscribers(bus: EventBus) -> None:
    """All subscribers registered on the same event must each receive the payload."""
    log_a: list[str] = []
    log_b: list[str] = []

    bus.subscribe("shared.event", lambda v: log_a.append(v))
    bus.subscribe("shared.event", lambda v: log_b.append(v))
    bus.publish("shared.event", "broadcast")

    assert log_a == ["broadcast"]
    assert log_b == ["broadcast"]


def test_publish_no_subscribers(bus: EventBus) -> None:
    """Publishing an event with no subscribers must not raise any exception."""
    # Should complete without error
    bus.publish("ghost.event", "payload")


def test_subscriber_exception_isolated(bus: EventBus) -> None:
    """An exception in one subscriber must not prevent other subscribers from running."""
    called = []

    def bad_handler(*args: object) -> None:
        raise RuntimeError("Subscriber failure")

    def good_handler(*args: object) -> None:
        called.append(True)

    bus.subscribe("test.event", bad_handler)
    bus.subscribe("test.event", good_handler)
    bus.publish("test.event")  # Must not raise

    assert called == [True]


def test_duplicate_subscribe_ignored(bus: EventBus) -> None:
    """Subscribing the same callback twice must only register it once."""
    count = []

    def handler(*args: object) -> None:
        count.append(1)

    bus.subscribe("test.event", handler)
    bus.subscribe("test.event", handler)  # duplicate
    bus.publish("test.event")

    assert len(count) == 1
