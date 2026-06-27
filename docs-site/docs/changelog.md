# Changelog

All notable changes to the Aegis Core Platform project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-06-27

### Added
- **Release Experience Hardening (Epic 3 Polish)**: Boosted total project coverage to 70% by writing test suites for bootstrap process, command registry, privilege UAC checks, and report generators.
- **CI Dummy Installer Block**: Added strict validation in `ReleaseValidator` to reject dummy placeholder executables inside GitHub Actions environments.
- **Release Assets Inclusion**: Integrated `manifest.json`, `coverage.xml`, and benchmark reports into the standard build pipeline and release uploads.
- **Clean Index Enforcement**: Cleaned up the git cached index to ensure untracked report directories are ignored globally according to `.gitignore` specifications.

---

## [Gold-Portfolio-Sprint-1] - 2026-06-27

### Added
- **README Landing Page**: Refactored `README.md` from a 177-line technical document into a concise, professional landing page with hero subtitle, "Why Aegis?" section, "Core Technologies" table, structured screenshot gallery, and a contributors section crediting the project author.
- **Documentation Module — Architecture**: Updated `docs/ARCHITECTURE.md` with accurate v1.0.0 monorepo layout, five core design patterns (Dependency Injection, HAL, EventBus, Repository, Strategy), and a full system data flow diagram.
- **Documentation Module — CLI Reference**: Created `docs/cli.md` with full command reference table, example console output, supported export formats, and automation integration guidance.
- **Documentation Module — FAQ**: Created `docs/faq.md` covering installation, WMI permissions, Health Score explanation, telemetry storage, and development questions.
- **Professional Badges**: Added nine shields.io badges to README (CI, Release, Python, License, Windows, Tests, Coverage, MyPy, Ruff).

---

## [1.0.0] - 2026-06-27

### Added
- **Official Stable Production Release**: Promoted platform to stable v1.0.0 production edition incorporating full release validation diagnostics, parameterised Inno Setup installations, and dynamic GitHub Release CD integration workflows.

---

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

---

## [Gold-Sprint-6] - 2026-06-27

### Added
- **Bootstrap Service Registry**: Refactored inisialisasi service di `main.py` ke modular `bootstrap.py` (`bootstrap_services()`), membersihkan launcher shell hingga kurang dari 30 baris kode.
- **SQLite TelemetryRepository Layer**: Memisahkan domain akses database dari history service ke dalam `TelemetryRepository` murni di `packages/core/repositories/telemetry_repository.py`.
- **Strategy Pattern Exporters**: Merombak total export engine ke Strategy Pattern (`ExportStrategy`, `CSVExportStrategy`, `JSONExportStrategy`, `MarkdownExportStrategy`, `HTMLExportStrategy`) di dalam package dedicated `packages/core/services/export/`.
- **Trend Analysis Engine**: Meluncurkan `TrendAnalysisService` untuk menghitung gradien tren parameter hardware (suhu CPU/SSD, RAM) secara linier, memproyeksikan sisa masa pakai baterai (Degradation Forecast), dan membandingkan beban periodik (Yesterday vs. Today).
- **CLI Commands Expansion**: Memperbarui CLI command `telemetry stats` agar mencetak trend, anomaly warnings, dan perbandingan delta harian secara komprehensif.
