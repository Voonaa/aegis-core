# Sprint 3 Prompt Blueprint

Feed this prompt to the AI when executing Sprint 3.

---

```markdown
We are ready to execute **Sprint 3: Telemetry & Profile Engine** for Aegis.

### 🎯 Objective:
Create the WMI device profiles matcher and construct the weighted Health Score telemetry engine. Bind real-time data ticks to the UI dashboard widgets.

### 📋 Files to Generate/Modify:

1. **`src/core/profile.py`**:
   - Query manufacturer and product identifiers via WMI. Load matching profiles config from `config/profiles/` (or default to `generic_windows.json`).

2. **`src/core/hardware.py`**:
   - Telemetry querying for CPU usage %, RAM utilization, temperatures, battery status, and S.M.A.R.T SSD indicators.
   - Implement the weighted Health Score calculation (0-100) based on ADR-0006.

3. **`src/ui/widgets.py`**:
   - UI widgets: `MetricCard`, progress indicators, and status indicators.

4. **`src/ui/dashboard.py` (Modify)**:
   - Construct telemetry cards.
   - Initialize the 1.0 second hardware polling loop (`.after(1000)`) updating dashboard elements.
   - Display the computed overall Health Score card.

### 🛡 Implementation Rules:
- Telemetry polls must run asynchronously or be extremely lightweight to prevent GUI lag.
- Check parameters against bounds to handle virtualized or generic PC hardware without failures.
```
