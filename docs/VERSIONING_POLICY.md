# Versioning & Release Management Policy: Aegis

This document defines the version schema, lifecycle milestones, and Git branch patterns required for the **Aegis Toolkit (Aegis)** repository.

---

## 1. Semantic Versioning Model (SemVer)
Aegis follows standard Semantic Versioning guidelines: `MAJOR.MINOR.PATCH`

* **`MAJOR`**: Major architectural updates, API breaks, or complete redesigns.
* **`MINOR`**: Additions of features, new utility modules, or sprint milestones.
* **`PATCH`**: Bug fixes, sensor read fallbacks adjustments, typo repairs, and optimization tweaks.

---

## 2. Product Development Lifecycles

```text
v0.x.x (Prototypes) ──> v1.x.x (Core Stable) ──> v2.x.x (Smart AI Core) ──> v3.x.x (Enterprise)
```

* **`v0.x.x` (Sprint 0 & 1)**: Internal prototypes. Core application UI frames, setting structures, logging engines, and mocks.
* **`v1.x.x` (Sprint 2 & 3 & 4)**: The Core utility release. Hardware monitoring polling dashboards, active system repair consoles, standard backups.
* **`v2.x.x` (Sprint 5 & Phase 2)**: The Smart Toolkit release. Adds event log parsing, local Windows BSOD Minidump diagnostic routines, and recommendations engines.
* **`v3.x.x` (Future Scope)**: The Enterprise release. Integrates dynamic third-party plugin JSON loaders, auto-update engines, and settings cloud synchronizers.
