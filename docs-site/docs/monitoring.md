# Telemetry Monitoring

Aegis Core Platform continuously monitors system health using Windows Management Instrumentation (WMI), winreg handles, and psutil counters. The gathered telemetry is displayed in real-time widgets on the graphical dashboard and logged for historical trend analysis.

---

## Metric Breakdown

Aegis evaluates system health across five primary hardware categories:

### 1. Processor (CPU)
-   **Model Name**: Resolved from system registries (e.g., `Intel Core i7-13700H` or `AMD Ryzen 7 7840HS`).
-   **Utilization**: Average load percentage across all logical cores (0–100%).
-   **Temperature**: Read from active ACPI thermal zones in degrees Celsius (°C).
-   **Voltage & Power**: Real-time estimations of current CPU core voltage and wattage draw.

### 2. Memory (RAM)
-   **Used Space**: Active physical RAM allocations in gigabytes (GB).
-   **Total Capacity**: Installed physical RAM modules size (e.g., `16.0 GB`).
-   **Percentage**: Current memory footprint ratio (0–100%).

### 3. Graphics (GPU)
-   **Adapter Name**: Active discrete or integrated graphics processors.
-   **Core Load**: Processing cores utilization level.
-   **VRAM Allocation**: Active video memory usage vs total physical allocation.

### 4. Storage (SSD/HDD)
-   **Capacity Space**: Drive partition boundaries and usage percentages.
-   **S.M.A.R.T Integrity**: Wear-level percentage indicating write lifespan.
-   **Status Indicator**: Health states reported by the drive controller (`Healthy`, `Warning`, or `Critical`).

### 5. Battery
-   **Charge Level**: Current charge capacity percentage.
-   **AC Adapter status**: Indicates whether the system is running on battery power or plugged in (Charging).
-   **Health Rating**: Factory design capacity vs current full charge capacity.
-   **Time Remaining**: Estimated runtime remaining before battery depletion (in minutes).

---

## The Health Score

Aegis synthesizes all active telemetry points into a single **Health Score (0–100)** to give users an instant diagnostic overview. The rating is calculated as follows:

| Hardware Category | Evaluated Metric | Weighted Influence |
|:---|:---|:---:|
| **CPU Condition** | High load factor or temperature peaks (>85°C) | 25% |
| **RAM Footprint** | Memory starvation margins | 20% |
| **Storage Diagnostics** | SMART warnings or high sector errors | 25% |
| **Battery Wear** | Significant design capacity degradation | 15% |
| **GPU Utilization** | Processing load limits | 15% |

### Score Ratings:
-   **80 to 100**: ✅ **Excellent** (System is operational, thermals are stable, and resources are ample).
-   **50 to 79**: 🟡 **Warning** (Thermals are elevated, memory resources are congested, or storage indicates warning sectors).
-   **0 to 49**: 🔴 **Critical** (High thermal throttling, failing SMART states, or complete resource starvation).

---

## Dynamic Dashboard Views
When running the graphical application (`apps/desktop/main.py`), the Telemetry Monitoring dashboard displays:
-   **Dial Gauges**: Visual representations of current CPU and memory utilization.
-   **Historical Charts**: Interactive Matplotlib line graphs showing telemetry trends (CPU thermals, RAM load, etc.) over selected time frames (e.g. last 1 hour, 24 hours, or 7 days).
-   **Observation Logs**: System event alerts indicating anomalies (such as high CPU load or failing battery health).
