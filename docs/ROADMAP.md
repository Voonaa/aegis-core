# Aegis Core Platform — Roadmap

> Dokumen ini mencatat history milestone pengembangan Aegis Core Platform dan rencana jangka panjang.

---

## Sprint History (Completed)

| Milestone | Status | Focus Area |
|:---|:---:|:---|
| Sprint 0 — Engineering Foundation | Done | SRS, ADRs, component libraries, design system |
| Sprint 1 — Boilerplate Infrastructure | Done | Monorepo structure, dependency setup, config templates |
| Sprint 2 — Application Shell & Telemetry Dashboard | Done | Sidebar nav, viewport router, dashboard widgets |
| Sprint 3 — Core Hardware Platform & Diagnostic Reports | Done | HAL (CPU/RAM/Disk/Battery), WMI queries, health scoring |
| Sprint 4 — Active System Management | Done | Async job manager, SFC/DISM/CHKDSK runners |
| Sprint 5 — Extensibility Platform & Aegis Core SDK | Done | Plugin loader, DI container, SDK public API |
| RC 1 — Monorepo Restructure & Hardening | Done | Ruff, MyPy, Pytest, test coverage, monorepo layout |
| RC 2 — UX & Design Tokens Calibration | Done | Theme system, typography, layout polish |
| RC 3 — Distribution & Release Engineering | Done | release.ps1, Inno Setup, SHA256, portable build |
| Gold Sprint 1 — Real Hardware Integration | Done | Live WMI polling, psutil integration, HAL accuracy |
| Gold Sprint 2 — Beautiful Dashboard & Live Charts | Done | Matplotlib charts, health trend lines, animated metrics |
| Gold Sprint 3 — Quality & Testing Hardening | Done | 99 unit tests, mocking WMI, 80%+ coverage |
| Gold Sprint 4 — Modular Optimization & Safe Profiles | Done | Performance/Balanced/PowerSaver profiles |
| Gold Sprint 5 — Enterprise Monitoring & Observability | Done | Export pipeline, multi-format reports, event logging |
| Gold Sprint 6 — Analytics & Historical Dashboard | Done | SQLite telemetry, historical charts, time-range filters |
| v1.0.0-rc4 — Release Candidate 4 | Done | Installer hardening, GitHub Actions, API docs |
| **v1.0.0 Stable** | **Released** | Official production-ready release — 2026-06-27 |

---

## Current Phase: v1.0 Gold — Portfolio Edition

Focus: Meningkatkan kualitas repository agar setara dengan project open source enterprise-grade.

| Epic | Status | Deliverable |
|:---|:---:|:---|
| Epic 1 — Repository Branding & Documentation | In Progress | README landing page, 8 docs files |

---

## Future Considerations (Post v1.0)

> Items berikut belum disetujui dan bukan bagian dari scope v1.0.0.

| Feature | Estimated Effort |
|:---|:---:|
| v1.1 — GPU Temperature Monitoring | Small |
| v1.1 — Notification Tray Icon | Medium |
| v1.2 — Plugin Marketplace | Large |
| v2.0 — Multi-machine Dashboard | XL |

---

## Versioning Policy

Aegis follows [Semantic Versioning](https://semver.org/):

- `MAJOR` — Breaking changes
- `MINOR` — New features (backward compatible)
- `PATCH` — Bug fixes only

The version string is managed exclusively in `version.txt` as the Single Source of Truth.

---

## Further Reading

- [Changelog](../CHANGELOG.md) — Detailed per-release change log
- [Release Guide](release-guide.md) — How to build and publish a release
- [Architecture](architecture.md) — Technical platform design
