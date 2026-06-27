# Diagnostic Reporting

Aegis Core Platform includes a reporting service that compiles system diagnostics, active hardware settings, and anomaly reports into structured export files. Reports can be generated instantly via the GUI dashboard or headless CLI commands.

---

## Supported Export Formats

Aegis supports exporting system metrics to four different formats, depending on your needs:

| Format | Default Output Path | Primary Use Case |
|:---|:---|:---|
| **JSON** | `reports/diagnostics/system_report.json` | Programmatic analysis, integration with remote monitoring systems, or API payloads. |
| **Markdown** | `reports/diagnostics/system_report.md` | Human-readable system audits, developer logs, or documentation attachments. |
| **CSV** | `reports/export/telemetry.csv` | Relational data importing into Excel or Google Sheets for custom spreadsheet plotting. |
| **HTML** | `reports/export/telemetry.html` | Styled, print-ready diagnostics reports suitable for sharing with IT support teams. |

---

## Report Generation Logic

When a report is generated, the `ReportService` (`packages/core/services/report_service.py`) executes the following operations:

1.  **Poll Telemetry Snapshot**: Queries the `HardwareService` to gather live readings (CPU temperature, utilization, disk SMART health, RAM allocations).
2.  **Resolve Profile Overlays**: Fetches active hardware profile configurations (e.g. `advan_workplus.json`) via the `ProfileManager` to compare real hardware capabilities against target performance models.
3.  **Run Recommendation Rules**: Feeds the telemetry payload into the `RecommendationService`. Anomaly detection rules flag issues (such as high CPU temperatures, disk wear levels, or battery degradation).
4.  **Format Compilation**:
    -   **Markdown Compiler**: Formats raw telemetry metrics into clean tables, highlights issues with warning icons, and embeds action suggestions.
    -   **JSON Compiler**: Assembles a structured nested dictionary detailing system variables, graphics processors, storage lifespans, network adapters, and computed health scores.

---

## Generating Reports

### Via Graphical Desktop App
1. Go to the **Diagnostics** page.
2. Click **Generate System Report**.
3. Choose the export formats you want to generate.
4. Click the output paths links to view the generated files.

### Via Command-Line Interface (Headless)
Run the CLI launcher from your terminal to export historical logging tables:
```powershell
# Set path
$env:PYTHONPATH="."

# Export telemetry log database to structured JSON format
python -m packages.core.cli telemetry export json
```
All CLI-exported historical telemetry tables are written directly to `reports/export/`.
