# Sprint 3: Telemetry & Profile Engine

## 1. Objectives
Implement the BIOS hardware profiles mapping system and construct the weighted Health Score telemetry engine. Bind real-time telemetry metrics to the UI widgets dashboard.

---

## 2. Target Files & Locations

### 1. `src/core/profile.py`
- Query bios motherboard manufacture data using WMI (`Win32_ComputerSystem`).
- Map target string to profile registry config, loading appropriate profile (e.g. `config/profiles/advan_workplus.json`). Fallback to `generic_windows.json`.

### 2. `src/core/hardware.py`
- Expose functions to collect metrics (CPU usage, RAM loads, temperatures, battery degradations, S.M.A.R.T SSD health flags).
- Calculate overall weighted Health Score (0-100) based on ADR-0006.

### 3. `src/ui/widgets.py`
- Renders `MetricCard`, progress indicators, and LED status indicators.

### 4. `src/ui/dashboard.py` (Update)
- Initialize cards.
- Bind the 1.0 second hardware refresh telemetry polling loop (`.after(1000)` event ticks) to update values.
- Calculate and display the overall Health Score card with custom feedback.

---

## 3. Verification Criteria
* Booting the application must print recognized laptop profile configurations in the logs.
* CPU, RAM, and SSD charts must refresh every second without blocking UI responsiveness.
* Verify the computed Health Score updates dynamically when CPU/RAM loads change.
