# Aegis SDK: Plugin Extension API

Aegis Core Platform supports dynamic folder-based runtime extensions. Developers can write plugins inside the `plugins/` directory.

## Plugin Structure

Every plugin directory must contain exactly:
1. `manifest.json`: Metadata declarations.
2. `main.py`: Entry points lifecycle hook implementations.

```text
plugins/
└── custom_diagnostics/
    ├── manifest.json
    └── main.py
```

---

## 1. Manifest Specification (`manifest.json`)

Defines plugin identifiers and permissions.

```json
{
  "name": "Storage Diagnostics Extension",
  "version": "1.0.0",
  "author": "Platform Engineer",
  "description": "Performs custom SSD wear analytics.",
  "permissions": ["filesystem"],
  "entry_point": "main.py"
}
```

* **name**: Unique extension name label.
* **permissions**: Standard access control lists (`filesystem`, `network`). If a plugin attempts to use SDK elements outside of permissions, it is rejected by the DI container.

---

## 2. Lifecycles Implementation (`main.py`)

Aegis calls three lifecycle entry hooks inside plugins.

```python
def initialize(container):
    """Invoked when the plugin is loaded into the DI Container.
    
    Args:
        container: DI ServiceContainer reference to resolve system services.
    """
    event_bus = container.get("event_bus")
    print("Plugin registered successfully.")

def start():
    """Invoked when the platform bootstrap completes.
    
    Use this hook to start background threads, subscribe to events, 
    or initiate monitoring loops.
    """
    print("Plugin analytics loop active.")

def dispose():
    """Invoked when the platform or desktop UI shuts down.
    
    Use this hook to safely close open files, release sockets,
    and join background threads.
    """
    print("Plugin resources released.")
```
