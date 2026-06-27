"""Decoupled file format strategies for Strategy Pattern export module."""

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

class ExportStrategy(ABC):
    """Abstract Strategy interface for exporting telemetry history lists."""

    @abstractmethod
    def export(self, data: list[dict], dest: Path) -> Path:
        """Processes and writes telemetry rows array to destination path.
        
        Args:
            data: Telemetry history dictionary rows list.
            dest: Target destination file path.
            
        Returns:
            The output Path object.
        """
        pass


class CSVExportStrategy(ExportStrategy):
    """CSV output generator implementation strategy."""

    def export(self, data: list[dict], dest: Path) -> Path:
        if not data:
            headers = ["id", "timestamp", "cpu_utilization", "cpu_temperature", "ram_percentage", 
                       "disk_health_percent", "battery_health_percent", "network_latency_ms", 
                       "health_score", "active_power_plan"]
            with open(dest, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
            return dest

        headers = list(data[0].keys())
        with open(dest, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in data:
                row_copy = dict(row)
                if "timestamp" in row_copy:
                    row_copy["timestamp"] = datetime.fromtimestamp(row_copy["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow(row_copy)
        return dest


class JSONExportStrategy(ExportStrategy):
    """JSON output generator implementation strategy."""

    def export(self, data: list[dict], dest: Path) -> Path:
        formatted_data = []
        for row in data:
            row_copy = dict(row)
            if "timestamp" in row_copy:
                row_copy["timestamp_raw"] = row_copy["timestamp"]
                row_copy["timestamp"] = datetime.fromtimestamp(row_copy["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            formatted_data.append(row_copy)

        with open(dest, "w", encoding="utf-8") as f:
            json.dump(formatted_data, f, indent=2)
        return dest


class MarkdownExportStrategy(ExportStrategy):
    """Markdown tabular output generator implementation strategy."""

    def export(self, data: list[dict], dest: Path) -> Path:
        lines = [
            "# Aegis Telemetry History Diagnostics Report",
            "",
            f"**Report Generated**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
            "",
            "| ID | Timestamp | CPU (%) | Temp (°C) | RAM (%) | Disk Health | Battery | Ping (ms) | Health Score | Active Plan |",
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
        ]

        for row in data:
            pretty_time = datetime.fromtimestamp(row.get("timestamp", 0.0)).strftime("%Y-%m-%d %H:%M:%S")
            lines.append(
                f"| {row.get('id', '-')} "
                f"| {pretty_time} "
                f"| {row.get('cpu_utilization', 0.0):.1f}% "
                f"| {row.get('cpu_temperature', 0.0):.1f}°C "
                f"| {row.get('ram_percentage', 0.0)*100.0:.1f}% "
                f"| {row.get('disk_health_percent', 0)}% "
                f"| {row.get('battery_health_percent', 0)}% "
                f"| {row.get('network_latency_ms', 0.0):.1f} ms "
                f"| {row.get('health_score', 0)}/100 "
                f"| {row.get('active_power_plan', 'Balanced')} |"
            )

        with open(dest, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return dest


class HTMLExportStrategy(ExportStrategy):
    """Print-to-PDF ready HTML output generator implementation strategy."""

    def export(self, data: list[dict], dest: Path) -> Path:
        table_rows = []
        for row in data:
            pretty_time = datetime.fromtimestamp(row.get("timestamp", 0.0)).strftime("%Y-%m-%d %H:%M:%S")
            table_rows.append(f"""
            <tr>
                <td>{row.get('id')}</td>
                <td>{pretty_time}</td>
                <td>{row.get('cpu_utilization'):.1f}%</td>
                <td>{row.get('cpu_temperature'):.1f}°C</td>
                <td>{row.get('ram_percentage')*100.0:.1f}%</td>
                <td>{row.get('disk_health_percent')}%</td>
                <td>{row.get('battery_health_percent')}%</td>
                <td>{row.get('network_latency_ms'):.1f} ms</td>
                <td class="health-score">{row.get('health_score')}/100</td>
                <td>{row.get('active_power_plan')}</td>
            </tr>""")

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Aegis Telemetry Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ffffff;
            color: #1f2937;
            margin: 40px;
        }}
        h1 {{
            color: #111827;
            font-size: 24px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
        }}
        .meta {{
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-bottom: 40px;
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f9fafb;
            font-weight: bold;
            color: #374151;
        }}
        tr:nth-child(even) {{
            background-color: #f9fafb;
        }}
        .health-score {{
            font-weight: bold;
            color: #10b981;
        }}
        @media print {{
            body {{
                margin: 20px;
            }}
            table {{
                page-break-inside: auto;
            }}
            tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}
        }}
    </style>
</head>
<body>
    <h1>Aegis Observability Diagnostics</h1>
    <div class="meta">
        <strong>Report Type</strong>: Telemetry Historical Log Export <br>
        <strong>Generated</strong>: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} <br>
        <strong>Target Records</strong>: {len(data)}
    </div>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>CPU Util</th>
                <th>CPU Temp</th>
                <th>RAM</th>
                <th>Disk Health</th>
                <th>Battery</th>
                <th>Network Ping</th>
                <th>Health Score</th>
                <th>Active plan</th>
            </tr>
        </thead>
        <tbody>
            {"".join(table_rows)}
        </tbody>
    </table>
</body>
</html>"""

        with open(dest, "w", encoding="utf-8") as f:
            f.write(html_content)
        return dest
