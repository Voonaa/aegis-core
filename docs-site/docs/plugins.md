# Plugin Development Guide

Aegis Core Platform features a dynamic runtime plugin system that allows developers to extend the diagnostic capabilities of the platform. Plugins are folder-based, validated at startup, and sandbox-executed based on declared permission models.

---

## Plugin Directory Layout

Plugins are located in the root `/plugins` folder:

```text
plugins/
└── latency_plugin/
    ├── manifest.json       # Metadata & permissions declarations
    └── main.py             # Entry script with lifecycle hooks
```

---

## 1. The Manifest Schema (`manifest.json`)

Every plugin must include a `manifest.json` file in its root directory. This manifest registers metadata and declares required permissions.

```json
{
  "name": "Network Latency Monitor",
  "version": "1.0.0",
  "author": "Aegis Core Team",
  "description": "Monitors ping times and network packet drops in real-time.",
  "permissions": ["network", "filesystem"],
  "entry_point": "main.py"
}
```

### Manifest Fields Description

| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `name` | `string` | ✅ | Human-readable plugin name. |
| `version` | `string` | ✅ | Semantic version string (e.g. `"1.2.0"`). |
| `author` | `string` | ✅ | Author name or organization. |
| `description` | `string` | ✅ | Brief explanation of plugin functions. |
| `permissions` | `array` | ✅ | List of permission strings. |
| `entry_point` | `string` | ✅ | Relative path to the execution python script. |

---

## 2. Permission Model

Aegis restricts plugin capabilities using a declarative permission model. The `PluginLoader` checks declared permission lists against system configurations at runtime:

| Permission | Boundary Description |
|:---|:---|
| `"filesystem"` | Allows reading and writing files to the local disk. |
| `"network"` | Allows initiating network connections and sockets. |
| `"registry"` | Allows querying Windows Registry trees. |
| `"admin"` | Requires Aegis to be executed with elevated Administrator privileges. |

> [!WARNING]
> **Admin Bypass Policy**:  
> Plugins requesting the `"admin"` permission will be skipped automatically with a log warning if the host Aegis process is running in standard user mode.

---

## 3. Lifecycle Hooks (`main.py`)

Aegis executes plugins inside strict lifecycle phases:

```text
Platform Bootstrapping
       │
       ▼
[Phase 1] initialize(container)
       │ -> Register custom services or configure state
       ▼
[Phase 2] start()
       │ -> Run background threads, pollers, or loops
       ▼
System Shutdown / Close
       │
       ▼
[Phase 3] dispose()
          -> Tear down threads, close file handles/sockets
```

### Hook Signatures

#### `initialize(container)`
Invoked during DI bootstrapping.
-   **Parameter**: `container` (`ServiceContainer`) — Allows fetching registered services (e.g. `event_bus` or `config`) or registering custom services.

#### `start()`
Invoked after platform bootstrapping completes. This is the entry point for starting background threads or event loops.

#### `dispose()`
Invoked when Aegis shuts down. Use this hook to terminate threads, release file handles, or close open sockets safely.

---

## Complete Example Plugin

Below is a complete, working plugin implementation that queries network latency periodically and publishes updates to the Aegis EventBus.

### manifest.json
```json
{
  "name": "Simple Latency Plugin",
  "version": "1.0.0",
  "author": "SDK Team",
  "description": "Monitors loopback ping times.",
  "permissions": ["network"],
  "entry_point": "main.py"
}
```

### main.py
```python
import time
import socket
import threading
from packages.core.constants import events

_event_bus = None
_thread = None
_stop_event = None

def ping_loop():
    """Background polling thread function."""
    print("[Simple Latency Plugin] Latency thread loop started.")
    while not _stop_event.is_set():
        try:
            start_time = time.perf_counter()
            # Perform a fast loopback connection check
            s = socket.create_connection(("127.0.0.1", 135), timeout=1.0)
            s.close()
            latency = (time.perf_counter() - start_time) * 1000.0
        except Exception:
            latency = -1.0 # Offline or unreachable
        
        # Publish latency updates to the EventBus
        if _event_bus:
            _event_bus.publish("NETWORK_LATENCY_CHANGED", {"ping_ms": latency})
            
        time.sleep(5.0)

def initialize(container):
    """Lifecycle Phase 1: Initialize service bindings."""
    global _event_bus
    _event_bus = container.get("event_bus")
    print("[Simple Latency Plugin] Initialized. Registered with EventBus.")

def start():
    """Lifecycle Phase 2: Start background tasks."""
    global _thread, _stop_event
    _stop_event = threading.Event()
    _thread = threading.Thread(target=ping_loop, daemon=True)
    _thread.start()
    print("[Simple Latency Plugin] Started loopback latency query thread.")

def dispose():
    """Lifecycle Phase 3: Tear down resources."""
    global _stop_event, _thread
    if _stop_event:
        _stop_event.set()
    if _thread:
        _thread.join(timeout=2.0)
    print("[Simple Latency Plugin] Teardown complete.")
```
