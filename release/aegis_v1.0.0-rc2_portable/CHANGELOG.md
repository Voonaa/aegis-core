# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0-rc3] - 2026-06-27

### Added
- **Gold Sprint 1 (Real Hardware Integration)**: Disabled simulated Demo Mode by default and migrated the HAL harvesters to query real processor telemetry, NVMe SSD SMART records, ACPI battery capacity values, GPU engine performance, and gateway network round-trip ping latency.

## [1.0.0-rc2] - 2026-06-27

### Added
- **Distribution & Release Engineering (RC3)**: Developed automated PowerShell release pipeline script `scripts/release.ps1` that automates checks, compiles metadata configuration, and packages portable directories.
- **Build Metadata & About modal**: Implemented modal layout `AboutDialog` showing version, commit, Python runtime versions, architectures, and loaded profile specs.
- **Global Crash Trap excepthook**: Configured unhandled exceptions logger in `main.py` dumping details into `logs/crash/` logs on fatal events.
- **Visual Design Tokens (RC2)**: Integrated spacings, corner radii, and font tokens directly in `theme.json` loaded via `ThemeManager`.
- **UI Standardisation**: Refactored layout viewport pages to use design tokens, eliminating magic numbers.

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
