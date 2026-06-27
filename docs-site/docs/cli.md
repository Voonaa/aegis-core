# CLI Reference Guide

Aegis Core Platform includes a robust command-line interface (CLI) module for headless execution, automated scheduling, and system diagnostics without launching the desktop GUI application.

---

## Environment Preparation

Before executing any CLI commands, ensure the project root is registered in your shell's `PYTHONPATH` so nested modules can be resolved correctly:

```powershell
# Windows PowerShell
$env:PYTHONPATH="."
```

---

## Command Catalog

### 1. `telemetry stats`

#### Description
Queries the active Hardware Abstraction Layer (HAL) to collect real-time system metrics (CPU utilization, core counts, RAM usage, storage SMART diagnostics, battery levels, GPU usage) and computes the current system health score.

#### Syntax
```powershell
python -m packages.core.cli telemetry stats
```

#### Example Command
```powershell
python -m packages.core.cli telemetry stats
```

#### Expected Output
```text
============================================================
  AEGIS CORE — SYSTEM TELEMETRY SNAPSHOT
============================================================
  CPU         :  14.2%  (16 cores)  |  Temp: 54.8°C
  RAM         :  6.4 GB / 16.0 GB   |  40.0%
  Disk        :  180 GB / 476 GB    |  37.8%  (SMART: Healthy)
  Battery     :  98%  (Charging)    |  Health: 96.5%
  GPU         :  1.2 GB / 6.0 GB    |  Load: 8.5%
------------------------------------------------------------
  HEALTH SCORE: 94 / 100  ✅  Excellent
============================================================
```

---

### 2. `telemetry export`

#### Description
Exports the historical database log records from the local SQLite repository into your choice of structured file format.

#### Syntax
```powershell
python -m packages.core.cli telemetry export <format>
```

#### Acceptable Formats
-   `csv` — Flat comma-separated records, written to `reports/export/telemetry.csv`.
-   `json` — Structured JSON array, written to `reports/export/telemetry.json`.
-   `md` — Formatted Markdown table, written to `reports/export/telemetry.md`.
-   `html` — Styled, print-ready HTML page, written to `reports/export/telemetry.html`.

#### Example Command
```powershell
python -m packages.core.cli telemetry export json
```

#### Expected Output
```text
[+] Telemetry database export completed successfully.
    Target File: C:\tools Advan\reports\export\telemetry.json
    Exported 348 logging records.
```

---

### 3. `telemetry clean`

#### Description
Clears all historical logs from the local SQLite database. This action permanently deletes historical records and **cannot** be undone.

#### Syntax
```powershell
python -m packages.core.cli telemetry clean
```

#### Example Command
```powershell
python -m packages.core.cli telemetry clean
```

#### Expected Output
```text
Warning: This will permanently delete all telemetry history.
Type 'yes' to confirm: yes
✅ Telemetry database cleared successfully.
```

---

### 4. `help`

#### Description
Displays a list of available command catalog operations, default parameters, and syntax rules.

#### Syntax
```powershell
python -m packages.core.cli help
```

#### Example Command
```powershell
python -m packages.core.cli help
```

#### Expected Output
```text
============================================================
  AEGIS CORE COMMAND LINE INTERFACE (CLI)
============================================================
  Usage: python -m packages.core.cli <command> [args]

  Available Commands:
    telemetry stats           Display real-time system diagnostics.
    telemetry export <fmt>    Export telemetry history database records.
                              Supported formats: csv, json, md, html
    telemetry clean           Clear all local database log history.
    help                      Display this help instruction screen.
============================================================
```

---

## Automation Integration

You can integrate Aegis CLI commands into Windows Task Scheduler for headless automation:
-   **Task Trigger**: Run every 6 hours or on system boot.
-   **Action Command**:
    -   Program/script: `python`
    -   Arguments: `-m packages.core.cli telemetry export csv`
    -   Start in: `C:\tools Advan` (or your absolute installation directory)
