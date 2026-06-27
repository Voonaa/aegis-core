"""Unit tests for the ServiceContainer dependency injection container."""

import pytest
from packages.core.container import ServiceContainer


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    """Reset the ServiceContainer singleton between tests to ensure isolation."""
    ServiceContainer._instance = None
    yield
    ServiceContainer._instance = None


def test_register_and_get() -> None:
    """A registered service must be retrievable by the same key."""
    container = ServiceContainer()
    container.register("my_service", "service_value")

    result = container.get("my_service")
    assert result == "service_value"


def test_get_unregistered_raises_keyerror() -> None:
    """Requesting an unregistered service must raise KeyError."""
    container = ServiceContainer()

    with pytest.raises(KeyError):
        container.get("nonexistent_service")


def test_has_returns_true_when_registered() -> None:
    """`has()` must return True for a registered key."""
    container = ServiceContainer()
    container.register("exists", object())

    assert container.has("exists") is True


def test_has_returns_false_when_not_registered() -> None:
    """`has()` must return False for an unregistered key."""
    container = ServiceContainer()

    assert container.has("missing") is False


def test_overwrite_service() -> None:
    """Re-registering an existing key must overwrite the previous value."""
    container = ServiceContainer()
    container.register("key", "first")
    container.register("key", "second")

    assert container.get("key") == "second"


def test_singleton_pattern() -> None:
    """Two calls to ServiceContainer() must return the same instance."""
    a = ServiceContainer()
    b = ServiceContainer()

    assert a is b


def test_register_multiple_services() -> None:
    """Multiple distinct services can be registered and retrieved independently."""
    container = ServiceContainer()
    container.register("alpha", 1)
    container.register("beta", 2)
    container.register("gamma", 3)

    assert container.get("alpha") == 1
    assert container.get("beta") == 2
    assert container.get("gamma") == 3
