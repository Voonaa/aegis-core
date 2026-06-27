# Supported Hardware Matrix

Aegis Core Platform maps real-time telemetry variables through the Hardware Abstraction Layer (HAL) by querying Windows Management Instrumentation (WMI) and host OS APIs.

## Tested Laptops & Hardware Profiles

| Manufacturer | Laptop Model | CPU Type | GPU Model | Telemetry Support Status |
| :--- | :--- | :--- | :--- | :---: |
| **ADVAN** | **Workplus** | AMD Ryzen 7 7730U | AMD Radeon Graphics | ✅ Full Telemetry + Temp Support |
| **ADVAN** | **Workpro** | Intel Core i5-1035G1 | Intel UHD Graphics | ✅ Full Telemetry |
| **ASUS** | **Zenbook 14** | Intel Core i7-1360P | Intel Iris Xe | ✅ Full Telemetry |
| **Lenovo** | **ThinkPad L14** | AMD Ryzen 5 Pro 5650U | AMD Radeon Graphics | ✅ Full Telemetry |
| **HP** | **ProBook 440 G9**| Intel Core i5-1235U | Intel Iris Xe | ✅ Full Telemetry |

## Telemetry Metrics Capture Matrix

- **CPU**:
  - Load Utilization: Captured via WMI query `Win32_Processor`.
  - CPU Temperature: Derived via `MSAcpi_ThermalZoneTemperature` (Requires Elevated Administrator privileges on select motherboards).
- **RAM**:
  - Memory Usage/Totals: Captured via WMI `Win32_OperatingSystem` & `psutil`.
- **Storage**:
  - Disk Health Status: Derived from S.M.A.R.T attributes mapped via `MSStorageDriver_FailurePredictStatus` WMI class.
  - Temperature: Derived via `MSStorageDriver_FailurePredictData` or NVMe SMART attributes.
- **Battery**:
  - Charge & Health Rates: Captured via WMI `Win32_Battery` and `BatteryStatus` classes.
