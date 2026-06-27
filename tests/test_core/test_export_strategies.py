"""Unit tests for Strategy Pattern ExportService Context and concrete strategies."""

import json
import pytest
from pathlib import Path
from packages.core.services.export import ExportService
from packages.core.services.export.strategies import (
    CSVExportStrategy, JSONExportStrategy, MarkdownExportStrategy, HTMLExportStrategy
)


@pytest.fixture
def export_svc(tmp_path: Path) -> ExportService:
    """Returns an ExportService Context instance mapped to a temp directory."""
    service = ExportService()
    service.diagnostics_dir = tmp_path
    return service


def test_strategy_registration(export_svc: ExportService) -> None:
    """ExportService Context must initialize with csv, json, md, and html strategies registered."""
    assert "csv" in export_svc._strategies
    assert "json" in export_svc._strategies
    assert "md" in export_svc._strategies
    assert "html" in export_svc._strategies


def test_export_invalid_format_raises_value_error(export_svc: ExportService) -> None:
    """Exporting to an unregistered format strategy must raise ValueError."""
    with pytest.raises(ValueError):
        export_svc.export_data("pdf_native", [], "test.pdf")


def test_strategy_execution_writes_file(export_svc: ExportService) -> None:
    """Context export_data must resolve CSV/JSON strategies and write files successfully."""
    data = [
        {
            "id": 1,
            "timestamp": 1234567.0,
            "cpu_utilization": 15.0,
            "cpu_temperature": 40.0,
            "ram_percentage": 0.35,
            "disk_health_percent": 95,
            "battery_health_percent": 90,
            "network_latency_ms": 10.0,
            "health_score": 90,
            "active_power_plan": "Balanced"
        }
    ]

    csv_out = export_svc.export_data("csv", data, "test.csv")
    json_out = export_svc.export_data("json", data, "test.json")
    md_out = export_svc.export_data("md", data, "test.md")
    html_out = export_svc.export_data("html", data, "test.html")

    assert csv_out.exists()
    assert json_out.exists()
    assert md_out.exists()
    assert html_out.exists()

    # Confirm JSON parsing content matches original
    with open(json_out, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert parsed[0]["cpu_utilization"] == 15.0
    assert parsed[0]["active_power_plan"] == "Balanced"
