# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0-final] - 2026-06-27

### Added
- **Release Experience Hardening (Epic 3 Polish)**: Boosted total project coverage to 70% by writing test suites for bootstrap process, command registry, privilege UAC checks, and report generators.
- **CI Dummy Installer Block**: Added strict validation in `ReleaseValidator` to reject dummy placeholder executables inside GitHub Actions environments.
- **Release Assets Inclusion**: Integrated `manifest.json`, `coverage.xml`, and benchmark reports into the standard build pipeline and release uploads.
- **Clean Index Enforcement**: Cleaned up the git cached index to ensure untracked report directories are ignored globally according to `.gitignore` specifications.
- **Aegis Documentation Website (Epic 4)**: Created Material for MkDocs static site layout inside `docs-site/` complete with 16 pages, Gantt roadmaps, custom footers, multi-tier sequence diagrams, and detailed FAQ list of 30 items.

## [Gold-Portfolio-Sprint-1] - 2026-06-27

### Added
- **README Landing Page**: Refactored `README.md` from a 177-line technical document into a concise, professional landing page with hero subtitle, "Why Aegis?" section, "Core Technologies" table, structured screenshot gallery, and a contributors section crediting the project author.
- **Documentation Module — Architecture**: Updated `docs/ARCHITECTURE.md` with accurate v1.0.0 monorepo layout, five core design patterns (Dependency Injection, HAL, EventBus, Repository, Strategy), and a full system data flow diagram.
- **Documentation Module — CLI Reference**: Created `docs/cli.md` with full command reference table, example console output, supported export formats, and automation integration guidance.
- **Documentation Module — SDK Reference**: Created `docs/sdk.md` documenting all three public SDK namespaces (`HardwareSDK`, `RepairSDK`, `ReportSDK`) with method signatures, property tables, and usage examples.
- **Documentation Module — Plugin System**: Created `docs/plugins.md` with manifest JSON specification, permission model, lifecycle hook sequence diagram, DI container integration guide, and a complete working plugin example.
- **Documentation Module — Developer Guide**: Created `docs/developer-guide.md` covering prerequisites, virtual environment setup, test execution, static analysis commands, naming conventions, git workflow, and debugging tips.
- **Documentation Module — Release Guide**: Created `docs/release-guide.md` documenting `release.ps1` pipeline steps, GitHub Actions release workflow, SSOT versioning policy, and checksum verification.
- **Documentation Module — Roadmap**: Updated `docs/ROADMAP.md` with complete sprint history table from Sprint 0 through v1.0.0 Stable, current Gold Phase status, and future considerations.
- **Documentation Module — FAQ**: Created `docs/faq.md` covering installation, WMI permissions, Health Score explanation, telemetry storage, and development questions.
- **Professional Badges**: Added nine shields.io badges to README (CI, Release, Python, License, Windows, Tests, Coverage, MyPy, Ruff).

## [1.0.0] - 2026-06-27

### Added
- **Official Stable Production Release**: Promoted platform to stable v1.0.0 production edition incorporating full release validation diagnostics, parameterised Inno Setup installations, and dynamic GitHub Release CD integration workflows.

## [1.0.0-rc4] - 2026-06-27

### Added
- **Inno Setup Runner Hardening**: Integrated `fleskesvor/setup-iscc` action inside GitHub workflows to ensure deterministic compiler availability on virtual machine builds.
- **Aegis CLI & Release Roadmap Docs**: Documented CLI module commands reference table and visual roadmap stages in primary README.md.
- **GitHub Release Automation Workflow**: Created `.github/workflows/release.yml` triggering automated ZIP builds, EXE compilations via ISCC, and softprops draft release publications on tag push.
- **SDK API Documentation Pages**: Documented developers API modules at `docs/api/hardware.md`, `docs/api/repair.md`, and `docs/api/plugin.md`.
- **Release Compression Automation**: Built dynamic Compress-Archive zip creation inside `release.ps1` to yield portable `.zip` archives.
- **UI Screenshots Automation**: Added a dynamic screenshot capture loop (`--capture-screenshots`) inside the desktop Tkinter main loop to automatically save client area page frames to `docs/assets/`.
- **Inno Setup Script Configuration**: Created `installer/aegis_setup.iss` to package unified setup executables.
- **Dependency Resolution Fix**: Resolved duplicate parent path concatenations in main.py boot config and unified the DI ServiceContainer profile key mapping to `"profile_mgr"`.
- **Production Release Package**: Created the automated pipeline to compile build metadata (version, commit hash, Python version) and assemble the portable directory (`reports/release/aegis_v1.0.0_portable/`) complete with verification manifests (`checksums.sha256`) and an Authenticode code-signing certificate verification step.
- **GitHub Community Guidelines**: Configured issue report templates (`bug_report.md`, `feature_request.md`, `hardware_compat.md`) and a standard Pull Request merge checklist.
- **Repository Safety Documents**: Established root policy documents: `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SUPPORTED_HARDWARE.md` outlining local dev setups, WMI queries, and private vulnerability disclosure procedures.

## [Gold-Sprint-6] - 2026-06-27

### Added
- **Bootstrap Service Registry**: Refactored inisialisasi service di `main.py` ke modular `bootstrap.py` (`bootstrap_services()`), membersihkan launcher shell hingga kurang dari 30 baris kode.
- **SQLite TelemetryRepository Layer**: Memisahkan domain akses database dari history service ke dalam `TelemetryRepository` murni di `packages/core/repositories/telemetry_repository.py`.
- **Strategy Pattern Exporters**: Merombak total export engine ke Strategy Pattern (`ExportStrategy`, `CSVExportStrategy`, `JSONExportStrategy`, `MarkdownExportStrategy`, `HTMLExportStrategy`) di dalam package dedicated `packages/core/services/export/`.
- **Trend Analysis Engine**: Meluncurkan `TrendAnalysisService` untuk menghitung gradien tren parameter hardware (suhu CPU/SSD, RAM) secara linier, memproyeksikan sisa masa pakai baterai (Degradation Forecast), dan membandingkan beban periodik (Yesterday vs. Today).
- **CLI Commands Expansion**: Memperbarui CLI command `telemetry stats` agar mencetak trend, anomaly warnings, dan perbandingan delta harian secara komprehensif.

## [Gold-Sprint-5] - 2026-06-27

### Added
- **SQLite Telemetry Logging**: Developed a localized relational logging database service (`TelemetryHistoryService`) under `packages/core/services/` targeting telemetry log entries, featuring active power plan GUID tracking, SQLite indexes, and query metrics.
- **7-Day Rolling History**: Implemented automatic database vacuuming to delete log rows older than 7 days, maintaining a lightweight file size limit footprint.
- **Multi-Format Export Engine**: Created `ExportService` supporting batch formatting of database history arrays to CSV, JSON logs, Markdown diagnostics tables, and print-friendly HTML templates.
- **CLI telemetry commands**: Added console directives (`telemetry stats` and `telemetry export <csv|json|md|html>`) that render 7-day stats averages (CPU, temp, RAM peak, latency) and export logs directly to the `reports/diagnostics/` folder.

## [Gold-Sprint-4] - 2026-06-27

### Added
- **Modular Optimization Engine**: Re-architected system optimization logic into a highly decoupled package (`packages/core/services/optimization/`) containing `planner.py` (OptimizationPlanner), `executor.py` (OptimizationExecutor), `validator.py` (OptimizationValidator), and `rollback.py` (RollbackEngine), unified behind a single `OptimizationService` facade wrapper.
- **Safe Profiles**: Replaced custom registry modifications with documented system operations (active power plan switching, DNS resolver flush, temp cleanup). Re-defined modes to professional tiers: `PERFORMANCE` (with `GAMING` & `RENDERING` presets), `BALANCED`, and `POWER_SAVER`.
- **System Restores & Backups**: Configured safe rollback verification that checks for Windows restore point capability, triggers async Checkpoint-Computer commands, and generates local JSON backups detailing structured changes lists with system metadata.
- **Diagnostics Reporting**: Consolidated all diagnostics reports (Health, Optimization validation, Repair jobs) under the unified directory `reports/diagnostics/`.
- **Benchmark Graphing & Cold Booting**: Expanded the benchmark utility (`benchmark.py`) to measure Cold Start vs. Warm Start latencies and render 5 distinct performance history trend charts in SVG format.

## [Gold-Sprint-3] - 2026-06-27

### Added
- **Test Suite Expansion**: Expanded unit test coverage from 4 tests to 80 tests, covering EventBus, DI Container, Health Engine, Recommendation rules, JobManager, PluginLoader, WindowsIntelligence, and Telemetry models.
- **Performance Regression Gate**: Added automated execution latency validation (`test_performance.py`) asserting critical engine thresholds (Health < 10ms, Recommendation < 5ms, HAL CPU mocked < 100ms).
- **Upgraded Benchmark Engine**: Developed robust local profiling script `scripts/benchmark.py` that records startup metrics, generates automated JSON/Markdown reports, and supports comparison audits via CLI (`benchmark.py compare`).
- **CI/CD Quality Artifacts**: Configured GitHub Actions to produce code coverage HTML reports and upload code quality artifacts (coverage.xml, HTML results, benchmark metrics).
- **HAL Sensor Accuracy**: Standardized CPU WMI voltage fallback representation (`0.0 (WMI Unavailable)`), calibrated battery capacity health calculations, stabilized GPU engine polling states, and introduced ping gateway socket timeouts.
- **Developer Onboarding Guidelines**: Established `requirements-dev.txt` for developer tooling standardization and documented the complete setup pipeline in `docs/DEVELOPMENT_SETUP.md`.

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
