# Aegis Core Platform — Plugin System

> Panduan lengkap untuk membuat, mengkonfigurasi, dan mendistribusikan extension plugin untuk Aegis Core Platform.

---

## Overview

Aegis mendukung **dynamic runtime plugins** berbasis folder yang dimuat otomatis saat startup. Setiap plugin adalah folder mandiri di dalam direktori `plugins/` yang berisi sebuah manifest JSON dan entry script Python.

```text
plugins/
└── my_plugin/
    ├── manifest.json   ← Plugin metadata & permissions
    └── main.py         ← Lifecycle implementation
```

---

## 1. Manifest File (`manifest.json`)

Setiap plugin **wajib** menyertakan `manifest.json` di root folder-nya.

```json
{
  "name": "Network Latency Monitor",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "Monitors network latency and packet loss in real-time.",
  "permissions": ["filesystem", "network"],
  "entry_point": "main.py"
}
```

### Manifest Fields

| Field | Type | Required | Description |
|:---|:---|:---:|:---|
| `name` | `string` | ✅ | Human-readable plugin display name |
| `version` | `string` | ✅ | Semantic version string (e.g., `"1.0.0"`) |
| `author` | `string` | ✅ | Plugin author name or organization |
| `description` | `string` | ✅ | Short description of what the plugin does |
| `permissions` | `array` | ✅ | Required permissions (see Permission Model below) |
| `entry_point` | `string` | ✅ | Entry script filename (relative to plugin folder) |

---

## 2. Permission Model

Declare required permissions in `manifest.json`:

| Permission | Description |
|:---|:---|
| `"filesystem"` | Read/write access to local files |
| `"network"` | Network socket connections |
| `"registry"` | Windows Registry read access |
| `"admin"` | Elevated privilege operations |

> [!WARNING]
> Plugins requesting `"admin"` permission will only load when Aegis is launched as Administrator. Otherwise, the plugin is silently skipped with a warning logged.

---

## 3. Lifecycle Hooks (`main.py`)

Implement standard lifecycle functions in your entry script:

```python
def initialize(container):
    """
    Called when the plugin is loaded into the DI Container at startup.
    Use this to register services or fetch dependencies.
    
    Args:
        container: The Aegis ServiceContainer instance
    """
    print("Plugin registered.")

def start():
    """
    Called when platform bootstrap completes.
    Use this to start background threads or polling loops.
    """
    print("Plugin started.")

def dispose():
    """
    Called when the application shuts down (window close or SIGTERM).
    Use this to gracefully stop threads and release resources.
    """
    print("Plugin teardown complete.")
```

### Lifecycle Sequence

```text
Platform Startup
      │
      ▼
Plugin Loader scans plugins/ directory
      │
      ▼
manifest.json loaded & validated
      │
      ▼
Permission check (admin required?)
      │
      ▼
initialize(container)   ← DI registration phase
      │
      ▼
All services bootstrapped
      │
      ▼
start()                 ← Runtime activation
      │
      ▼
[Application Running]
      │
      ▼
dispose()               ← Graceful shutdown
```

---

## 4. Accessing Aegis Services via DI Container

Inside `initialize(container)`, you can retrieve any registered service:

```python
def initialize(container):
    hardware_service = container.get("hardware_service")
    event_bus        = container.get("event_bus")
    
    # Subscribe to telemetry updates
    event_bus.subscribe("telemetry.updated", on_telemetry_updated)

def on_telemetry_updated(snapshot):
    print(f"CPU: {snapshot.cpu.utilization:.1f}%")
```

### Available Services

| Key | Service | Description |
|:---|:---|:---|
| `"hardware_service"` | `HardwareService` | Polls and aggregates HAL telemetry |
| `"health_service"` | `HealthService` | Computes health score from snapshot |
| `"optimization_service"` | `OptimizationService` | Profile management & tuning |
| `"telemetry_service"` | `TelemetryService` | Historical data access |
| `"job_manager"` | `JobManager` | Async repair job executor |
| `"event_bus"` | `EventBus` | Publish/subscribe message broker |
| `"profile_mgr"` | `ProfileManager` | Hardware profile configuration |

---

## 5. Complete Plugin Example

Below is a complete working plugin that monitors CPU temperature and publishes alerts:

**`plugins/cpu_alert/manifest.json`**
```json
{
  "name": "CPU Temperature Alert",
  "version": "1.0.0",
  "author": "Aegis Community",
  "description": "Triggers alerts when CPU temperature exceeds 85°C.",
  "permissions": ["filesystem"],
  "entry_point": "main.py"
}
```

**`plugins/cpu_alert/main.py`**
```python
import threading
import time

_event_bus = None
_hardware  = None
_running   = False

def initialize(container):
    global _event_bus, _hardware
    _event_bus = container.get("event_bus")
    _hardware  = container.get("hardware_service")
    print("[CPU Alert] Plugin initialized.")

def start():
    global _running
    _running = True
    thread = threading.Thread(target=_monitor_loop, daemon=True)
    thread.start()

def dispose():
    global _running
    _running = False
    print("[CPU Alert] Plugin stopped.")

def _monitor_loop():
    while _running:
        snapshot = _hardware.get_snapshot()
        if snapshot.cpu.temperature > 85.0:
            _event_bus.publish("alert.cpu_overheat", {
                "temperature": snapshot.cpu.temperature,
                "threshold": 85.0,
            })
        time.sleep(5)
```

---

## Further Reading

- [SDK Reference](sdk.md) — Use HardwareSDK and RepairSDK within plugins
- [Architecture](architecture.md) — Understand the EventBus and DI Container internals
- [Developer Guide](developer-guide.md) — Testing and debugging plugins
