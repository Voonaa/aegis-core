# Sprint 1: Boilerplate Infrastructure

## 1. Objectives
Create the project folder structure, configure target packages, implement JSON configuration managers, initialize the subsystem logging engine, and generate a basic CustomTkinter window.

---

## 2. Target Files & Locations

### 1. `src/config/settings.json`
Configuration store containing application values.
```json
{
  "app_name": "Aegis Toolkit",
  "version": "0.1.0",
  "log_level": "INFO",
  "telemetry_interval_ms": 1000,
  "admin_required": true
}
```

### 2. `src/config/theme.json`
Visual design tokens matching VSCode/Fluent style.
```json
{
  "theme_mode": "dark",
  "colors": {
    "bg_primary": "#1A1A1A",
    "bg_sidebar": "#111827",
    "accent_primary": "#2563EB",
    "text_primary": "#FFFFFF",
    "status_success": "#22C55E",
    "status_warning": "#FACC15",
    "status_danger": "#EF4444"
  }
}
```

### 3. `src/core/logger.py`
Configure custom SubsystemLoggerAdapter writing outputs to `logs/aegis.log`. Log entries must format as:
`[TIMESTAMP] | [LEVEL] | [SUBSYSTEM] | [MESSAGE]`

### 4. `src/app.py`
The main entry point launcher class `AegisApp` inheriting from `customtkinter.CTk`.
- Load configuration files.
- Boot the subsystem logger.
- Initialize the dark mode GUI context, size dimensions (1020x640), and test window boot.

---

## 3. Verification Criteria
* Run `python src/app.py`.
* Ensure a dark mode window loads without warnings.
* Verify `logs/aegis.log` is created and writes startup logs correctly.
