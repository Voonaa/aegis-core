# Project Memory: Aegis Core Platform

This file is the single source of truth for the current state of development. **Every AI agent must read this file first** to avoid repeating work or deviating from the implementation status.

---

## 1. Project Overview
* **Project Name**: Aegis Core Platform
* **Current Version**: v1.0.0-rc2 (Release Candidate 3 - Release Engineering Complete)
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
* **Current Active Focus**: Dogfooding Stage (Stability trials & validation).

### File Registry Status
* `requirements.txt`: **[COMPLETED]** - Dependencies for Aegis.
* `pyproject.toml`: **[COMPLETED]** - Static checks configurations for ruff and mypy.
* `.gitignore`: **[COMPLETED]** - Exclusions.
* `CHANGELOG.md`: **[COMPLETED]** - Release tracking logs.
* `.github/workflows/ci.yml`: **[COMPLETED]** - Pipeline validation script.
* `docs/SRS.md` to `docs/VERSIONING_POLICY.md`: **[COMPLETED]** - Engineering foundation sheets.
* `apps/desktop/`: **[COMPLETED]** - Desktop UI wrapper (`main.py`, `app.py`, `ui/`, `config/`).
* `packages/core/`: **[COMPLETED]** - Core platform operational logic.
* `packages/sdk/`: **[COMPLETED]** - SDK wrapper entry points.
* `plugins/example_plugin/`: **[COMPLETED]** - Extensibility runtime demo example (`manifest.json`, `main.py`).
* `scripts/`: **[COMPLETED]** - Static checks (`lint.ps1`) and automated release pipeline (`release.ps1`).
* `tests/`: **[COMPLETED]** - Unit test suites.
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
│   └── release.ps1
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
│   │   │   └── telemetry.py
│   │   ├── plugins/
│   │   │   └── loader.py
│   │   └── services/
│   │       ├── hardware_service.py
│   │       ├── health_service.py
│   │       ├── maintenance_service.py
│   │       ├── privilege_service.py
│   │       ├── recommendation.py
│   │       ├── repair_service.py
│   │       └── report_service.py
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
        └── test_logger.py
```

---

## 4. Known Issues & Blockers
* **None**: RC3 release pipeline completed successfully.

---

## 5. Next Steps
* Initiate 2-week dogfood stability test runs prior to drafting v1.0.0-gold release tags.
