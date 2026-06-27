"""Unit tests for the ProfileManager device detection and configuration loader."""

import json
import pytest
from pathlib import Path
from packages.core.profile_manager import ProfileManager


def _make_profile(tmp_path: Path, name: str, data: dict) -> Path:
    """Helper: writes a profile JSON file to tmp_path and returns its path."""
    f = tmp_path / f"{name}.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    return f


def test_detect_profile_returns_string(tmp_path: Path) -> None:
    """`detect_profile()` must return a non-empty string."""
    mgr = ProfileManager(profiles_dir=tmp_path)
    result = mgr.detect_profile()

    assert isinstance(result, str)
    assert len(result) > 0


def test_load_nonexistent_profile_does_not_crash(tmp_path: Path) -> None:
    """If no profile file exists, ProfileManager must fall back to empty dict without crashing."""
    mgr = ProfileManager(profiles_dir=tmp_path)

    # No file written — should fall back gracefully
    assert isinstance(mgr.profile_data, dict)


def test_load_valid_profile_populates_data(tmp_path: Path) -> None:
    """When a valid generic_windows.json exists, profile_data must be populated."""
    expected = {"profile_name": "Generic Windows", "max_cpu_temp": 85}
    _make_profile(tmp_path, "generic_windows", expected)

    mgr = ProfileManager(profiles_dir=tmp_path)
    mgr.profile_name = "generic_windows"
    # Reload using the helper directly
    mgr.profile_data = mgr._load_profile_file(tmp_path / "generic_windows.json")

    assert mgr.profile_data.get("profile_name") == "Generic Windows"
    assert mgr.profile_data.get("max_cpu_temp") == 85


def test_get_profile_name_returns_string(tmp_path: Path) -> None:
    """`get_profile_name()` must always return a string."""
    mgr = ProfileManager(profiles_dir=tmp_path)
    name = mgr.get_profile_name()

    assert isinstance(name, str)


def test_get_profile_data_returns_dict(tmp_path: Path) -> None:
    """`get_profile_data()` must always return a dict."""
    mgr = ProfileManager(profiles_dir=tmp_path)
    data = mgr.get_profile_data()

    assert isinstance(data, dict)


def test_corrupt_profile_falls_back_to_empty(tmp_path: Path) -> None:
    """A profile file with invalid JSON must fall back to empty dict without crashing."""
    bad_file = tmp_path / "generic_windows.json"
    bad_file.write_text("{ this is not valid json }", encoding="utf-8")

    mgr = ProfileManager(profiles_dir=tmp_path)
    result = mgr._load_profile_file(bad_file)

    assert result == {}
