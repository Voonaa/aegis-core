# Development Roadmap: Aegis Toolkit

This document outlines the step-by-step product-based roadmap for the **Aegis Toolkit (Aegis)** platform. Development follows an Agile methodology organized across release milestones.

---

## 📅 Release Milestones Gantt

```mermaid
gantt
    title Aegis Toolkit Product Roadmap
    dateFormat  YYYY-MM-DD
    section Phase Alpha
    Sprint 0: Engineering Foundation   :completed, s0, 2026-06-27, 1d
    Sprint 1: Core Setup               :active, s1, after s0, 3d
    Sprint 2: UI View Routing & Shell  : s2, after s1, 4d
    section Phase Beta
    Sprint 3: Telemetry & Profile Engine: s3, after s2, 5d
    Sprint 4: Maintenance Subprocess    : s4, after s3, 5d
    section Phase RC
    Sprint 5: BSOD Crash Analyzer      : s5, after s4, 5d
    Sprint 6: Packaging & Installer    : s6, after s5, 3d
    section Phase Stable
    v1.0.0 Stable Release              : milestone, after s6, 1d
    section Phase Enterprise
    v2.0.0 Plugins & Cloud Engine       : s7, after v1.0.0, 10d
```

### 🔹 Phase Alpha (Core Architecture)
* **Sprint 0: Engineering Foundation** (Status: **COMPLETED**)
  - Formulate SRS, component libraries, Design tokens, test specifications, and ADRs.
* **Sprint 1: Boilerplate Infrastructure**
  - Create directory structures, dependency setups, default JSON config templates, Subsystem logger.
* **Sprint 2: UI View Routing & Shell**
  - Build left navigation sidebar, viewport router, empty page views, and the embedded Developer Console.

### 🔹 Phase Beta (System Integration)
* **Sprint 3: Telemetry & Profile Engine**
  - Build WMI motherboard vendor detection, profile configurations JSON loads, and real-time dashboard widget binders. Calculate weighted Health Score.
* **Sprint 4: Maintenance Subprocess Automation**
  - Establish PowerShell async runner, thread executors, background status console updates, and environment variables exporters.

### 🔹 Phase RC (Testing & Packaging)
* **Sprint 5: BSOD Crash Analyzer (AI Recommendation)**
  - Implement Event Viewer and crash dump reader logic inside `core/windows.py`. Compute warning banners on conflict events.
* **Sprint 6: Distributables Build**
  - Packaging the complete app using `PyInstaller` with admin manifests, setting up desktop shortcuts and uninstallers.

### 🔹 Phase Stable (Product Delivery)
* Compile release candidates, complete manual test suites, and tag the v1.0.0 repository stable branch.

### 🔹 Phase Enterprise (Future Scale)
* JSON-driven plugins loads, settings cloud configuration synchronization, and automated updates checking.
