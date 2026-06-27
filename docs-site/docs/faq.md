# Frequently Asked Questions (FAQ)

Find answers to common questions about installing, using, and developing for the Aegis Core Platform.

---

## Installation & Setup

### 1. What Windows versions are supported?
Aegis is designed for **Windows 10** and **Windows 11**. It relies on Windows Management Instrumentation (WMI), winreg registry keys, and power scheme configurations (`powercfg`), which are exclusive to Microsoft Windows.

### 2. Can I run Aegis on Linux or macOS?
**No**. Running Aegis on Linux, macOS, or other UNIX-based operating systems is not supported due to its deep integration with Windows-specific APIs.

### 3. Which Python versions are compatible?
Aegis is officially tested and supported on **Python 3.11**, **3.12**, and **3.14** (experimental). Python 3.10 and earlier versions are not supported because Aegis uses modern syntax features like structural pattern matching (`match/case`) and PEP 585 type hinting.

### 4. Why do I see a `ModuleNotFoundError: No module named 'packages'` error?
This happens when python cannot resolve nested monorepo packages. To fix it, add the project root directory to your system `PYTHONPATH` before launching the application:
```powershell
$env:PYTHONPATH = "."
python apps/desktop/main.py
```

### 5. Why does Aegis require Administrator privileges?
Several core features require elevated privileges (UAC):
-   **WMI queries** targeting CPU socket thermals (`MSAcpi_ThermalZoneTemperature`) require admin rights.
-   **System repair runners** (`sfc /scannow`, `DISM /RestoreHealth`) require administrator access.
-   **Power profile modifications** (`powercfg` schemes switches) require admin privileges.

---

## Telemetry & Diagnostics

### 6. How is the Health Score calculated?
The **Health Score** is a weighted rating from 0 to 100 calculated from five telemetry metrics:
-   **CPU Performance** (utilization averages & thermals): 25%
-   **Memory Overhead** (RAM consumption): 20%
-   **Storage Integrity** (SMART health flags & partition spaces): 25%
-   **Battery Condition** (charge retention & wear index): 15%
-   **GPU Utilization** (GPU core load metrics): 15%

### 7. What do the Health Score colors mean?
-   🟢 **Excellent (80–100)**: System is operating stably within safe margins.
-   🟡 **Warning (50–79)**: Resource usage is high, or minor hardware warnings are present.
-   🔴 **Critical (0–49)**: Severe resource exhaustion, high thermal throttling, or drive SMART failures.

### 8. Where are the telemetry logs stored?
Telemetry logs are stored in a local SQLite database file at:
`apps/desktop/config/telemetry_history.db`

### 9. How long is the telemetry log history kept?
Aegis keeps a **7-day rolling history**. During startup, a background clean-up service runs `telemetry_history_service.clean_old_records(days=7)` to automatically prune records older than 7 days, keeping the database file lightweight.

### 10. Can I export the logged telemetry data?
**Yes**. You can export telemetry logs using the GUI's Diagnostics page or the headless CLI. Aegis supports exporting logs to **CSV**, **JSON**, **Markdown**, and **HTML** formats, saving files directly to `reports/export/`.

---

## Performance Optimization

### 11. What changes does the Performance Profile apply?
The **Performance Profile** switches the active Windows power plan GUID to **High Performance**, sets both minimum and maximum CPU processor states to 100% to prevent latency overhead during core clock shifts, and optimizes processor core parking thresholds.

### 12. What does the PowerSaver Profile do?
The **PowerSaver Profile** switches the active Windows power plan GUID to **Power Saver**, caps the maximum CPU state to 70%, throttles background Search indexers, and adjusts screen brightness to extend battery life.

### 13. Is changing power profiles safe for my hardware?
**Yes**. Aegis only switches between standard Windows power schemes and safety-validated registries configurations. It does not perform hardware overclocking or voltage modifications.

### 14. How can I undo optimization tweaks?
Aegis automatically creates backup checkpoints. You can revert changes anytime by clicking **Restore Settings** in the GUI, which restores settings from the latest JSON backup file inside `apps/desktop/config/backups/`.

---

## Architecture & Development

### 15. What design patterns are used in the codebase?
Aegis is built around five main design patterns:
-   **Dependency Injection (DI)**: Manages service instances using a central `ServiceContainer`.
-   **Hardware Abstraction Layer (HAL)**: Decouples low-level queries from business logic.
-   **Event Bus**: Enables loose communication between modules using pub/sub events.
-   **Repository Pattern**: Handles database access via the `TelemetryRepository` wrapper.
-   **Strategy Pattern**: Dynamically selects formatting engines for CSV, JSON, MD, and HTML exports.

### 16. How do I add a custom plugin?
Create a new directory inside the root `plugins/` folder containing a valid `manifest.json` (defining entry points, metadata, and permissions) and a `main.py` entry script that implements lifecycle hooks (`initialize`, `start`, `dispose`). See the [🔌 Plugin Development Guide](plugins.md) for details.

### 17. How does the plugin permission sandbox work?
Aegis restricts plugin capabilities by evaluating declared permission keys (`network`, `filesystem`, `registry`, `admin`) inside `manifest.json`. Plugins requesting administrative access are skipped if the host process is not running with elevated privileges.

### 18. Where can I find the public API functions?
The public API is located in `packages/sdk/` and exposes:
-   `HardwareSDK` (`packages.sdk.hardware`) for querying real-time telemetry.
-   `RepairSDK` (`packages.sdk.repair`) for executing system repairs.
-   `ReportSDK` (`packages.sdk.report`) for compiling diagnostics reports.

### 19. How do I run unit tests?
First, ensure you have set `PYTHONPATH`. Then run pytest:
```powershell
$env:PYTHONPATH = "."
pytest tests/ -v
```

### 20. How do I compile a release build?
Run the release pipeline script:
```powershell
.\scripts\release.ps1
```
This runs style checks, executes the test suite, generates metadata, and uses the Inno Setup Compiler (`ISCC.exe`) to build the installer binary.

---

## Polishing & Customizations (Expanded Q&As)

### 21. How can I customize the GUI theme or color schemes?
Theme values are defined inside `apps/desktop/config/theme.json`. You can modify UI element coordinates, color arrays (using HSL or Hex codes), and default fonts to customize the dashboard.

### 22. Where are config parameters and backup overrides written?
Under default source runs, they are resolved to `apps/desktop/config/`. Under portable binary distributions, they are resolved relative to the launch directory.

### 23. Are local telemetry history logs encrypted?
No. Local SQLite files are stored as plain SQL database files to maximize query execution speeds. Access security is maintained by Windows OS standard file system permissions boundary limits.

### 24. Why does Aegis use SQLite instead of other DBMS?
SQLite requires zero configuration, stores data in a single file, runs completely in-process, and has a very small memory footprint, making it ideal for client-side applications.

### 25. How is the Trend Analysis calculation resolved?
The `TrendAnalysisService` calculates telemetry changes by performing standard linear regression slope calculations across database log metrics over selected time ranges.

### 26. Can I reload plugins dynamically while Aegis is running?
No. Plugins are loaded and initialized once during startup to prevent DI container conflicts and ensure thread safety.

### 27. What is the average CPU/RAM overhead of Aegis?
Under idle state polling, the desktop app consumes approximately **34 MB** of RAM and less than **1%** CPU utilization.

### 28. Under what license is Aegis Core Platform released?
Aegis is officially released under the permissive **MIT License**. You are free to modify, distribute, and consume the codebase for personal or commercial projects.

### 29. How should I report security vulnerabilities?
If you discover a security vulnerability, please submit details privately by emailing the maintainers listed in `SECURITY.md` instead of opening a public issue tracker.

### 30. How can I contribute to the repository?
You can contribute by submitting pull requests. Please ensure your branch follows the Git Flow rules, and all changes pass `lint.ps1` with unit test coverages remaining above **70%**.
