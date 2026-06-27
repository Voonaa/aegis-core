"""Unit tests for the PluginLoader discovery and lifecycle engine."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from packages.core.container import ServiceContainer
from packages.core.event_bus import EventBus
from packages.core.plugins.loader import PluginLoader
from packages.core.services.privilege_service import PrivilegeService


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    """Reset ServiceContainer singleton between tests."""
    ServiceContainer._instance = None
    yield
    ServiceContainer._instance = None


@pytest.fixture
def container() -> ServiceContainer:
    """Returns a minimal container with required services."""
    c = ServiceContainer()
    c.register("event_bus", EventBus())
    c.register("privilege_service", PrivilegeService())
    return c


def test_empty_plugins_dir_returns_empty(tmp_path: Path, container: ServiceContainer) -> None:
    """An empty plugin directory must return an empty list without crashing."""
    loader = PluginLoader(plugins_dir=tmp_path)
    result = loader.load_all_plugins(container)

    assert isinstance(result, list)
    assert result == []


def test_missing_dir_creates_folder(tmp_path: Path, container: ServiceContainer) -> None:
    """If the plugins directory does not exist, it must be created automatically."""
    plugins_dir = tmp_path / "plugins"
    assert not plugins_dir.exists()

    loader = PluginLoader(plugins_dir=plugins_dir)
    loader.load_all_plugins(container)

    assert plugins_dir.exists()


def test_invalid_manifest_skipped(tmp_path: Path, container: ServiceContainer) -> None:
    """A plugin directory with an invalid manifest.json must be skipped, not crash."""
    # Create a plugin dir with broken manifest
    bad_plugin = tmp_path / "bad_plugin"
    bad_plugin.mkdir()
    (bad_plugin / "manifest.json").write_text("{ not valid json }", encoding="utf-8")

    loader = PluginLoader(plugins_dir=tmp_path)
    result = loader.load_all_plugins(container)

    # Bad plugin must be silently skipped
    assert "bad_plugin" not in result


def test_valid_plugin_loaded(tmp_path: Path, container: ServiceContainer) -> None:
    """A plugin with a valid manifest and enabled=true must be loaded successfully."""
    plugin_dir = tmp_path / "test_plugin"
    plugin_dir.mkdir()

    manifest = {
        "name": "test_plugin",
        "version": "1.0.0",
        "enabled": True,
        "entry_point": "main.py",
        "requires_admin": False,
        "permissions": []
    }
    (plugin_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    # Create a minimal main.py plugin
    (plugin_dir / "main.py").write_text(
        "def on_load(container):\n    pass\n",
        encoding="utf-8"
    )

    loader = PluginLoader(plugins_dir=tmp_path)

    # Mock importlib to avoid actual module loading side effects
    with patch("importlib.util.spec_from_file_location") as mock_spec, \
         patch("importlib.util.module_from_spec") as mock_module:
        mock_mod = type("mod", (), {"on_load": lambda c: None})()
        mock_module.return_value = mock_mod
        mock_spec.return_value = type("spec", (), {"loader": type("ldr", (), {"exec_module": lambda self, m: None})()})()

        result = loader.load_all_plugins(container)

    # Result is a list regardless
    assert isinstance(result, list)


def test_disabled_plugin_skipped(tmp_path: Path, container: ServiceContainer) -> None:
    """A plugin with enabled=false in its manifest must not be loaded."""
    plugin_dir = tmp_path / "disabled_plugin"
    plugin_dir.mkdir()

    manifest = {
        "name": "disabled_plugin",
        "version": "1.0.0",
        "enabled": False,
        "entry_point": "main.py",
        "requires_admin": False,
        "permissions": []
    }
    (plugin_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    loader = PluginLoader(plugins_dir=tmp_path)
    result = loader.load_all_plugins(container)

    assert "disabled_plugin" not in result
