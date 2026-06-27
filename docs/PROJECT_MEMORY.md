# Project Memory: Aegis Core Platform

This file is the single source of truth for the current state of development. **Every AI agent must read this file first** to avoid repeating work or deviating from the implementation status.

---

## 1. Project Overview
* **Project Name**: Aegis Core Platform
* **Current Version**: Gold-Sprint-4 (Modular Optimization Complete)
* **Vision**: An enterprise-grade modular Windows diagnostics and performance optimization engine. It splits into:
  - **Aegis Core (Engine)**: Subsystems containing HAL components, background Job threads, and WMI queries.
  - **Aegis Desktop (GUI)**: CustomTkinter layout dashboard.
  - **Aegis SDK (API)**: Clean public interface for extensions.
  - **Aegis Plugin API**: Third-party runtime extensions.

---

## 2. Current Development State
* **Completed Milestones**:
  - Sprint 0 (Engineering Foundation)
  - Sprint 1 (Boilerplate Infrastructure)
  - Sprint 2 (Application Shell & Telemetry Dashboard)
  - Sprint 3 (Core Hardware Platform & Diagnostic Reports)
  - Sprint 4 (Active System Management Platform)
  - Sprint 5 (Extensibility Platform & Aegis Core SDK)
  - RC1 (Monorepo Restructure, Static Checks & Hardening)
  - RC2 (UX & Design Tokens Layout Calibration)
  - RC3 (Distribution & Release Engineering Automation)
  - Gold Sprint 1 (Real Hardware Integration)
  - Gold Sprint 2 (Beautiful Dashboard Layout & Live Charts)
  - Gold Sprint 3 (Quality & Testing Hardening)
  - Gold Sprint 4 (Modular Optimization & Safe Profiles)
* **Current Active Focus**: Gold Sprint 5 (Enterprise Monitoring).

### File Registry Status
* `requirements.txt`: **[COMPLETED]** - Dependencies for Aegis.
* `requirements-dev.txt`: **[COMPLETED]** - Developer dependencies.
* `pyproject.toml`: **[COMPLETED]** - Static checks configurations for ruff and mypy.
* `.gitignore`: **[COMPLETED]** - Exclusions.
* `CHANGELOG.md`: **[COMPLETED]** - Release tracking logs.
* `.github/workflows/ci.yml`: **[COMPLETED]** - Pipeline validation script.
* `docs/SRS.md` to `docs/DEVELOPMENT_SETUP.md`: **[COMPLETED]** - Engineering and setup sheets.
* `apps/desktop/`: **[COMPLETED]** - Desktop UI wrapper (`main.py`, `app.py`, `ui/`, `config/`).
* `packages/core/`: **[COMPLETED]** - Core platform operational logic.
* `packages/sdk/`: **[COMPLETED]** - SDK wrapper entry points.
* `plugins/example_plugin/`: **[COMPLETED]** - Extensibility runtime demo example (`manifest.json`, `main.py`).
* `scripts/`: **[COMPLETED]** - Static checks (`lint.ps1`), release pipeline (`release.ps1`), and benchmarks (`benchmark.py`).
* `tests/`: **[COMPLETED]** - Unit test suites.
* `reports/`: **[COMPLETED]** - Unified folder containing benchmark SVG/JSONs, htmlcov reports, and diagnostics.
* `release/`: **[COMPLETED]** - Portable release outputs and checksum maps.

---

## 3. Directory Tree State

```text
Aegis/ (c:\tools Advan)
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── CHANGELOG.md
├── requirements.txt
├── pyproject.toml
├── scripts/
│   ├── lint.ps1
│   ├── release.ps1
│   └── benchmark.py
├── apps/
│   └── desktop/
│       ├── app.py
│       ├── main.py
│       ├── config/
│       │   ├── settings.json
│       │   ├── theme.json
│       │   └── build_metadata.json
│       └── ui/
│           ├── base_page.py
│           ├── sidebar.py
│           ├── console.py
│           ├── dashboard.py
│           ├── maintenance.py
│           ├── settings.py
│           └── widgets.py
├── packages/
│   ├── core/
│   │   ├── command_registry.py
│   │   ├── container.py
│   │   ├── event_bus.py
│   │   ├── health_engine.py
│   │   ├── jobs.py
│   │   ├── logger.py
│   │   ├── profile_manager.py
│   │   ├── constants/
│   │   │   ├── events.py
│   │   │   └── paths.py
│   │   ├── exceptions/
│   │   │   └── custom.py
│   │   ├── hal/
│   │   │   ├── battery.py
│   │   │   ├── cpu.py
│   │   │   ├── gpu.py
│   │   │   ├── network.py
│   │   │   ├── os_env.py
│   │   │   ├── ram.py
│   │   │   └── storage.py
│   │   ├── interfaces/
│   │   │   └── base.py
│   │   ├── models/
│   │   │   ├── telemetry.py
│   │   │   └── intelligence.py
│   │   ├── plugins/
│   │   │   └── loader.py
│   │   ├── services/
│   │   │   ├── hardware_service.py
│   │   │   ├── health_service.py
│   │   │   ├── maintenance_service.py
│   │   │   ├── privilege_service.py
│   │   │   ├── recommendation.py
│   │   │   ├── repair_service.py
│   │   │   ├── report_service.py
│   │   │   ├── windows_intelligence.py
│   │   │   └── optimization/
│   │   │       ├── __init__.py
│   │   │       ├── planner.py
│   │   │       ├── executor.py
│   │   │       ├── validator.py
│   │   │       └── rollback.py
│   └── sdk/
│       ├── __init__.py
│       ├── hardware.py
│       ├── repair.py
│       └── report.py
├── plugins/
│   └── example_plugin/
│       ├── main.py
│       └── manifest.json
├── release/
│   └── aegis_v1.0.0-rc2_portable/
│       ├── Aegis.bat
│       ├── CHANGELOG.md
│       ├── checksums.sha256
│       ├── pyproject.toml
│       ├── requirements.txt
│       ├── apps/
│       ├── packages/
│       └── plugins/
└── tests/
    ├── __init__.py
    └── test_core/
        ├── __init__.py
        ├── test_config.py
        ├── test_logger.py
        ├── test_container.py
        ├── test_event_bus.py
        ├── test_health_service.py
        ├── test_intelligence_model.py
        ├── test_jobs.py
        ├── test_performance.py
        ├── test_plugin_loader.py
        ├── test_profile_manager.py
        ├── test_recommendation.py
        ├── test_sdk.py
        ├── test_telemetry_models.py
        └── test_windows_intelligence.py
```

---

## 4. Known Issues & Blockers
* **None**: RC3 release pipeline completed successfully.

---

## 5. Next Steps
* Proceed to Gold Sprint 5 (Enterprise Monitoring: live charts, history data logging, CSV/JSON exporting).
