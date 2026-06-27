# Getting Started

## What is Aegis?

**Aegis Core Platform** is a professional diagnostic utility and optimization suite designed specifically for Microsoft Windows environments. It bridges the gap between raw hardware telemetry and active system administration by providing an extensible, secure, and modern monorepo platform.

Whether you are a developer looking to integrate telemetry into your app, an IT administrator seeking automated diagnostics pipelines, or a power user trying to squeeze every bit of performance out of your hardware, Aegis provides the tools you need.

---

## Core Operational Layers

Aegis is architected into four distinct modules, ensuring a complete separation of concerns:

```text
┌────────────────────────────────────────────────────────┐
│                   Aegis Desktop UI                     │
│                (CustomTkinter Interface)               │
└───────────────────────────┬────────────────────────────┘
                            │ Consumes
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Aegis SDK / APIs                     │
│         (HardwareSDK, RepairSDK, ReportSDK)            │
└───────────────────────────┬────────────────────────────┘
                            │ Calls
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Aegis Core Engine                    │
│      (DI Container, Event Bus, SQLite Storage)         │
└───────────────────────────┬────────────────────────────┘
                            │ Interfaces
                            ▼
┌────────────────────────────────────────────────────────┐
│             Hardware Abstraction Layer (HAL)           │
│        (WMI queries, psutil loops, winreg hooks)       │
└────────────────────────────────────────────────────────┘
```

1.  **Presentation Layer (`apps/desktop/`)**: A sleek graphical user interface utilizing CustomTkinter dark-mode design tokens, featuring real-time interactive widgets and Matplotlib historical trends.
2.  **SDK Interface (`packages/sdk/`)**: Clean public interfaces exposing telemetry parameters, system repair handles, and PDF/HTML generator models.
3.  **Core Services (`packages/core/`)**: The logical engine managing events, background task queues, recommendations rules, and sqlite relational databases.
4.  **Hardware Abstraction Layer (`packages/core/hal/`)**: Low-level query providers isolating Windows Management Instrumentation (WMI), winreg registry handles, and OS-specific functions from the upper application layers.

---

## Next Steps

To begin using or developing with Aegis, check out the following pages:

-   Go to [💾 Installation](installation.md) to set up your environment or download release binaries.
-   Explore [🏗 Architecture](architecture.md) to understand design patterns and structural layouts.
-   Check out [💻 CLI Reference](cli.md) to query hardware parameters directly from your shell scripts.
