# Aegis SDK: Hardware Telemetry API

The `hardware` SDK module exposes a clean public interface to query real-time system metrics harvested from Windows Management Instrumentation (WMI) and host OS APIs.

## Namespace Reference

```python
from packages.sdk.hardware import HardwareSDK
```

## Methods List

### 1. `get_cpu_info()`
Retrieves active CPU physical metrics.

* **Returns**: `CPUInfo` (Frozen dataclass)
* **Fields**:
  - `utilization`: `float` - Overall CPU usage (%).
  - `temperature`: `float` - Core package temperature (°C).
  - `model`: `str` - Processor descriptor name.
  - `base_speed_ghz`: `float` - Clock speed frequency.
  - `cores_physical`: `int` - Count of physical cores.
  - `cores_logical`: `int` - Count of logical threads.

```python
cpu = HardwareSDK.get_cpu_info()
print(f"CPU Load: {cpu.utilization}% Temp: {cpu.temperature} C")
```

---

### 2. `get_ram_info()`
Retrieves physical volatile memory sizes.

* **Returns**: `RAMInfo` (Frozen dataclass)
* **Fields**:
  - `used_gb`: `float` - Active memory allocation (GB).
  - `total_gb`: `float` - Maximum hardware RAM size (GB).
  - `percentage`: `float` - Current allocation percentage (0.0 to 1.0).

```python
ram = HardwareSDK.get_ram_info()
print(f"RAM Allocation: {ram.percentage * 100:.1f}%")
```

---

### 3. `get_disk_info()`
Retrieves the boot disk SMART diagnostic values.

* **Returns**: `DiskInfo` (Frozen dataclass)
* **Fields**:
  - `used_gb`: `float` - Storage utilization (GB).
  - `total_gb`: `float` - Maximum capacity size (GB).
  - `wear_level_percent`: `int` - Calculated drive health rate (0 to 100).
  - `status`: `str` - SMART prediction status ("OK" or "PREDICT_FAILURE").

```python
disk = HardwareSDK.get_disk_info()
if disk.status != "OK":
    print("WARNING: Storage degradation predicted!")
```

---

### 4. `get_battery_info()`
Retrieves details of battery health and charge capacity.

* **Returns**: `BatteryInfo` (Frozen dataclass)
* **Fields**:
  - `percentage`: `int` - Current charge percentage (0 to 100).
  - `is_charging`: `bool` - Power adapter attachment state.
  - `health_percent`: `int` - Wear degradation rate (0 to 100).

```python
bat = HardwareSDK.get_battery_info()
print(f"Battery Wear Level: {100 - bat.health_percent}%")
```
