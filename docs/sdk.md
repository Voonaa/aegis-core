# Aegis Core Platform — SDK Reference

> Aegis SDK menyediakan public API yang bersih dan stabil untuk mengintegrasikan kapabilitas diagnostik Aegis ke dalam aplikasi atau skrip eksternal.

---

## Overview

SDK terletak di `packages/sdk/` dan mengekspos tiga namespace utama:

| Namespace | Module | Deskripsi |
|:---|:---|:---|
| `HardwareSDK` | `packages.sdk.hardware` | Query snapshot hardware real-time |
| `RepairSDK` | `packages.sdk.repair` | Eksekusi job perbaikan sistem asinkron |
| `ReportSDK` | `packages.sdk.report` | Generate laporan diagnostik terformat |

---

## HardwareSDK

Mengambil snapshot telemetri hardware secara real-time dari HAL layer.

```python
from packages.sdk.hardware import HardwareSDK

sdk = HardwareSDK()
snapshot = sdk.get_snapshot()

print(snapshot.cpu.utilization)   # float: e.g. 23.4
print(snapshot.ram.percentage)    # float: e.g. 50.6
print(snapshot.battery.health)    # float: e.g. 94.3
print(snapshot.health_score)      # int:   e.g. 91
```

### `HardwareSDK.get_snapshot()` → `TelemetrySnapshot`

| Property | Type | Description |
|:---|:---|:---|
| `snapshot.cpu.utilization` | `float` | CPU load percentage (0–100) |
| `snapshot.cpu.temperature` | `float` | CPU die temperature in °C |
| `snapshot.cpu.model` | `str` | CPU model name string |
| `snapshot.cpu.core_count` | `int` | Number of logical cores |
| `snapshot.ram.used_gb` | `float` | RAM usage in GB |
| `snapshot.ram.total_gb` | `float` | Total RAM capacity in GB |
| `snapshot.ram.percentage` | `float` | RAM usage percentage (0–100) |
| `snapshot.disk.used_gb` | `float` | Disk usage in GB |
| `snapshot.disk.total_gb` | `float` | Total disk capacity in GB |
| `snapshot.disk.smart_status` | `str` | S.M.A.R.T status: `"Good"` / `"Warning"` / `"Critical"` |
| `snapshot.battery.percentage` | `float` | Battery charge percentage (0–100) |
| `snapshot.battery.is_charging` | `bool` | True if AC adapter connected |
| `snapshot.battery.health` | `float` | Battery health percentage (0–100) |
| `snapshot.gpu.vram_used_gb` | `float` | VRAM usage in GB |
| `snapshot.gpu.vram_total_gb` | `float` | Total VRAM in GB |
| `snapshot.gpu.load` | `float` | GPU load percentage (0–100) |
| `snapshot.health_score` | `int` | Computed health score (0–100) |
| `snapshot.timestamp` | `datetime` | Snapshot capture time (UTC) |

---

## RepairSDK

Mengeksekusi job perbaikan sistem secara asinkron tanpa memblokir thread utama.

```python
from packages.sdk.repair import RepairSDK

sdk = RepairSDK()

# Run System File Checker asynchronously
job = sdk.run_sfc()
print(job.status)   # "running" | "completed" | "failed"

# Run DISM image repair
job = sdk.run_dism()

# Run disk check (next boot scheduled)
job = sdk.run_chkdsk(drive="C:")
```

### Available Jobs

| Method | System Command | Description |
|:---|:---|:---|
| `run_sfc()` | `sfc /scannow` | Scans and repairs Windows system files |
| `run_dism()` | `DISM /RestoreHealth` | Repairs Windows image health |
| `run_chkdsk(drive)` | `chkdsk /f /r` | Schedules disk integrity check on next boot |

### `JobResult` Object

| Property | Type | Description |
|:---|:---|:---|
| `status` | `str` | `"running"`, `"completed"`, `"failed"` |
| `output` | `str` | Raw stdout/stderr text from the process |
| `exit_code` | `int` | Process exit code (0 = success) |
| `duration_ms` | `int` | Execution time in milliseconds |

---

## ReportSDK

Menghasilkan laporan diagnostik sistem dalam berbagai format.

```python
from packages.sdk.report import ReportSDK

sdk = ReportSDK()

# Generate a full diagnostic report
report = sdk.generate()

# Export in multiple formats
sdk.export(report, format="json",  path="output/report.json")
sdk.export(report, format="html",  path="output/report.html")
sdk.export(report, format="md",    path="output/report.md")
sdk.export(report, format="csv",   path="output/report.csv")
```

---

## Further Reading

- [Plugin System](plugins.md) — Extend Aegis with custom plugins using the SDK
- [CLI Reference](cli.md) — Headless diagnostics via command-line
- [Architecture](architecture.md) — Understand the internal service layer the SDK wraps
