# Structured Logging Policy: Aegis

This document outlines the log formatting standards, subsystem classifications, and rotating file rules enforced in the **Aegis Toolkit (Aegis)** logging engine.

---

## 1. Log Format & Layout

Every log entry must be structured cleanly to allow easy parsing and log-viewer filtering. 
The standard format string:

```text
%(asctime)s | %(levelname)-8s | [%(subsystem)s] | %(message)s
```

---

## 2. Subsystem Definitions

To filter log events, developers must direct logs using one of the following subsystem identifiers:

1. **`SYSTEM`**: Logged during startup operations, config loads, theme evaluations, page routing events, and app shutdown sequences.
2. **`USER`**: Logged on UI interactions (clicks, keyboard focus changes, setting slider updates).
3. **`NETWORK`**: Logged during network status telemetry polls and socket reset automation actions.
4. **`HARDWARE`**: Telemetry sensor read actions (CPU utilization, RAM consumption metrics, disk capacity metrics, smart readings).
5. **`PLUGIN`**: Diagnostic logs tracing dynamic plugin load states and third-party-manifest parser operations.
6. **`UPDATE`**: Application update checks, version comparisons, and file downloads.
7. **`PERFORMANCE`**: Metrics regarding optimizations (gaming plan, developer mode toggles, RAM cleanup operations, profile switches).

---

## 3. Code Implementation

The `core/logger.py` file must implement a subclass of `logging.LoggerAdapter` to inject subsystem labels:

```python
import logging

class SubsystemLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.setdefault('extra', {})
        extra['subsystem'] = self.extra.get('subsystem', 'SYSTEM')
        return msg, kwargs
```

---

## 4. File Rotation Policy
* **Log Location**: Write to `logs/aegis.log` relative to root directory.
* **Rotation Mode**: Use `logging.handlers.RotatingFileHandler`.
* **Rotation Parameters**:
  - Max File Size: `5MB`
  - Backup Count: `5` files
  - Encoding: `utf-8`
