# Aegis Core Platform — Architecture

> Dokumen ini menjelaskan arsitektur teknis platform Aegis Core Platform v1.0.0.

---

## Monorepo Structure

Aegis dibangun sebagai **decoupled monorepo** yang memisahkan core engine, desktop GUI, SDK publik, dan plugin extension secara tegas.

```text
aegis-core/
├── apps/
│   └── desktop/            # CustomTkinter GUI presentation layer
│       ├── main.py          # Entry point & bootstrap orchestrator
│       ├── app.py           # AegisApp window class
│       ├── ui/              # Page views (dashboard, monitor, maintenance, report, settings)
│       └── config/          # Runtime config (settings.json, theme.json, profiles/)
├── packages/
│   ├── core/               # Business logic & platform services
│   │   ├── hal/            # Hardware Abstraction Layer (CPU, RAM, GPU, Disk, Battery)
│   │   ├── services/       # Service layer (health, optimization, telemetry, export)
│   │   ├── repositories/   # Data access layer (TelemetryRepository -> SQLite)
│   │   ├── models/         # Domain data models (TelemetrySnapshot, IntelligenceScore)
│   │   ├── plugins/        # Plugin loader & lifecycle manager
│   │   ├── bootstrap.py    # Dependency Injection container registration
│   │   ├── container.py    # DI ServiceContainer
│   │   └── event_bus.py    # Decoupled publish/subscribe event system
│   └── sdk/                # Public API surface for external consumers
│       ├── hardware.py     # HardwareSDK entry point
│       ├── repair.py       # RepairSDK entry point
│       └── report.py       # ReportSDK entry point
├── plugins/                # Runtime extension manifests
├── scripts/                # Release automation & quality tooling
├── tests/                  # Unit test suites (99 tests)
├── installer/              # Inno Setup configuration
├── docs/                   # Documentation
└── version.txt             # Single Source of Truth for version string
```

---

## Core Design Patterns

### 1. Dependency Injection (DI)

Semua service diregistrasi melalui `bootstrap_services()` di `packages/core/bootstrap.py` dan dikonsumsi melalui `ServiceContainer`:

```python
container = ServiceContainer()
bootstrap_services(container, config, profiles_dir)

hardware = container.get("hardware_service")
health   = container.get("health_service")
```

---

### 2. Hardware Abstraction Layer (HAL)

HAL mengisolasi semua query WMI/psutil dari business logic:

```text
WMI / WinReg / psutil
        |
        v
  HAL Components
  +-- CpuHAL     -> utilization, temp, model, cores
  +-- RamHAL     -> used_gb, total_gb, percentage
  +-- StorageHAL -> used_gb, total_gb, wear_level, SMART status
  +-- BatteryHAL -> percentage, is_charging, health_percent
  +-- GpuHAL     -> vram_used, vram_total, gpu_load
```

---

### 3. Event Bus (Publish/Subscribe)

Komponen berkomunikasi secara decoupled melalui `EventBus`:

```python
event_bus.subscribe("telemetry.updated", handler_fn)
event_bus.publish("telemetry.updated", snapshot)
```

---

### 4. Repository Pattern

Akses data SQLite diisolasi di layer repository:

```text
Service Layer -> TelemetryRepository -> SQLite Database (telemetry.db)
```

---

### 5. Strategy Pattern (Export)

```text
ExportService
+-- CSVExportStrategy
+-- JSONExportStrategy
+-- MarkdownExportStrategy
+-- HTMLExportStrategy
```

---

## System Data Flow

```text
Hardware (WMI / WinReg / psutil)
        |
        v
HAL Telemetry Components
        |
        v
TelemetrySnapshot (Domain Model)
        |
        +---> HealthEngine -> HealthScore -> RecommendationEngine
        |
        +---> TelemetryRepository -> SQLite (history)
        |
        +---> EventBus -> "telemetry.updated"
                              |
                              v
                      GUI Desktop Viewports
                      (Dashboard, Monitor, Report)
```

---

## Further Reading

- [Developer Guide](developer-guide.md) — Setup environment dan cara berkontribusi
- [SDK Reference](sdk.md) — API publik untuk integrasi eksternal
- [Plugin System](plugins.md) — Cara menulis extension plugins
