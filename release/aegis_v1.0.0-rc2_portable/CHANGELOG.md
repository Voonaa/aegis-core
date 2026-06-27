# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0-rc2] - 2026-06-27

### Added
- **Visual Design Tokens**: Integrated layout spacings, corner radii, and typography scales parameters directly into `theme.json` loaded dynamically via `ThemeManager`.
- **UI Standardisation**: Refactored `app.py`, `dashboard.py`, `maintenance.py`, `settings.py`, and `widgets.py` elements, replacing static values with theme tokens.
- **Accessability Contours**: Hardened font sizes and colors contrast bounds inside active layout pages.

---

## [1.0.0-rc1] - 2026-06-27

### Added
- **Monorepo Restructuring**: Reorganized directory layouts to separate apps (`apps/desktop/`), core platform packages (`packages/core/`), and API wrappers (`packages/sdk/`).
- **Static Code Analysis**: Configured `pyproject.toml` with strict rules for `ruff` and `mypy`. Created `scripts/lint.ps1` helper validation checks script.
- **Path Resolution Hardening**: Re-mapped configuration path references in `ThemeManager` and `main.py` using relative pathing rules.
- **Unit Test Coverage Verification**: Verified all unit tests successfully compile and execute on the new monorepo layout structure.

---

## [0.3.0-alpha] - 2026-06-27

### Added
- **Sprint 4.1 (Privilege & Job Manager)**: Created `PrivilegeService` with UAC Admin detection and execution elevation triggers. Created asynchronous `JobManager` coordinating background thread pools to prevent GUI freezing.
- **Sprint 4.2 (Repair Engines)**: Created `RepairService` executing elevated DISM, SFC, and CHKDSK subprocesses.
- **Subprocess Progress Parser**: Developed stdout regex parsers that dynamically map SFC and DISM percentage logs to EventBus updates.
- **CLI Commands integration**: Connected console triggers `repair sfc`, `repair dism`, and `repair chkdsk` to live background jobs.
- **Sprint 4.3 (Maintenance Actions)**: Created `MaintenanceService` supporting temporary files cleaning, DNS resolver cache flushing, and DISM component store cleanup.
- **UX Progress UI**: Re-routed `MaintenancePage` buttons to run background jobs and display progress bar status cards in the UI shell.

---

## [0.2.0-alpha] - 2026-06-27

### Added
- **Sprint 3.1 (Hardware Abstraction Layer)**: Created modular HAL package separating CPU, RAM, Storage, Battery, OS, GPU, and Network inspections.
- **Windows Registry & WMI Inspections**: Implemented winreg and WMI queries to fetch Windows OS current builds, active gateway IPs, DNS address search orders, and nested virtualization statuses.
- **Dynamic Motherboard Profile Matching**: Updated `ProfileManager` to dynamically detect motherboard manufacturer and load laptop config files (e.g. `advan_workplus.json`).
- **Sprint 3.2 (Report Exporter)**: Created `ReportService` yielding MD and JSON system diagnostics files inside `temp/`. Added CLI command `report` to Developer Console.
- **Extended Page Lifecycles**: Integrated `on_enter()`, `on_leave()`, `on_resume()`, and `on_pause()` hooks in `BasePage` to manage telemetry timers.

---

## [0.1.0-alpha] - 2026-06-27

### Added
- **Project Structure**: Built complete modular structure under `src/` and `docs/`.
- **Engineering Foundation (Sprint 0)**: Formulated SRS, Feature Matrix, Component Library, Design Tokens, test plan, version policy, logging policy, and ADRs (ADR-0001 to ADR-0007).
- **Subsystem Logging**: Implemented `SubsystemLoggerAdapter` in `src/core/logger.py` printing formatted logs to `logs/aegis.log`.
- **Configuration & Styling**: Created `src/config/settings.json` and `src/config/theme.json` to handle visual presets and settings configurations.
- **GUI Application Shell**: Created main launcher class `AegisApp` in `src/app.py` displaying left sidebar, router frame, and console inputs.
- **Developer Console**: Created interactive CLI inputs console `src/ui/console.py` rendering terminal screens inside the GUI.
- **Visual Viewports**: Added layout placeholders for `DashboardPage`, `MaintenancePage`, and `SettingsPage` with reusable widget metrics in `src/ui/widgets.py`.
- **CI/CD Automation**: Configured `.github/workflows/ci.yml` runner pipeline executing lint and test verification scripts.
- **Unit Testing**: Added test coverage classes under `tests/test_core/` for logging and configurations.
