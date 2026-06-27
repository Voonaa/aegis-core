# ADR-0006: Weighted Health Score Engine

## Status
Approved

## Context
To offer a clear diagnosis dashboard, Aegis Toolkit needs to calculate and show a general system **Health Score (0-100)**. This scoring must be mathematically consistent, predictable, and avoid arbitrary fluctuations.

## Decision
We will calculate the overall health index using a weighted linear combination of 5 system components (weighted at 20 points maximum each):

$$\text{Health Score} = S_{\text{Storage}} + S_{\text{Battery}} + S_{\text{Thermal}} + S_{\text{Memory}} + S_{\text{OS}}$$

### 1. Storage Pillar ($S_{\text{Storage}}$ - Max 20)
* Calculated directly from the SSD's S.M.A.R.T wear life indicator.
* Formula: `(SMART_Health_Percent / 100) * 20`

### 2. Battery Pillar ($S_{\text{Battery}}$ - Max 20)
* Measures battery degradation.
* Formula: `(Full_Charge_Capacity / Design_Capacity) * 20`
* *Fallback*: If the system is a desktop (no battery present), this component defaults to `20`.

### 3. Thermal Pillar ($S_{\text{Thermal}}$ - Max 20)
* Deducts points if temperatures exceed normal operating thresholds under idle states.
* Formula:
  - If Temp $\le 65^\circ\text{C}$: `20` points.
  - If Temp $> 65^\circ\text{C}$: Deduct `0.5` points per $1^\circ\text{C}$ over $65^\circ\text{C}$ (Min score: `0`).

### 4. Memory Allocation Pillar ($S_{\text{Memory}}$ - Max 20)
* Tracks memory starvation.
* Formula:
  - If RAM Usage $\le 80\%$: `20` points.
  - If RAM Usage $> 80\%$: Deduct `1.0` point per $1\%$ utilization over $80\%$ (Min score: `0`).

### 5. OS Integrity Pillar ($S_{\text{OS}}$ - Max 20)
* Evaluates operating system stability.
* Starts at `20`. Deducts `10` points if a BSOD dump is detected in `C:\Windows\Minidump` within the past 7 days. Deducts `10` points if critical system services (Windows Update, VSS) are disabled.

---

## Consequences
* High-frequency telemetry polling updates ($S_{\text{Thermal}}$ and $S_{\text{Memory}}$) are run inside the main loop every 1s, updating the dashboard instantly.
* Slow telemetry updates ($S_{\text{Storage}}$, $S_{\text{Battery}}$, $S_{\text{OS}}$) are cached and refreshed only on application start, or when a manual refresh is requested to minimize WMI query overhead.
