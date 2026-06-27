# Aegis SDK: Repair and Maintenance API

The `repair` SDK module exposes a thread-safe asynchronous pipeline to trigger Windows maintenance utilities (SFC, DISM, CHKDSK) and schedule optimization jobs.

## Namespace Reference

```python
from packages.sdk.repair import RepairSDK
```

## Methods List

### 1. `trigger_sfc_scan(callback=None)`
Schedules a System File Checker scan to run in the background.

* **Parameters**:
  - `callback`: `Callable[[str], None]` - (Optional) Logs progress output updates.
* **Returns**: `str` - Task Job ID string.

```python
def log_output(line):
    print(f"[SFC Progress] {line}")

job_id = RepairSDK.trigger_sfc_scan(callback=log_output)
print(f"Repair scan scheduled: {job_id}")
```

---

### 2. `trigger_dism_cleanup(callback=None)`
Schedules a Deployment Image Servicing and Management scan to cleanup component store.

* **Parameters**:
  - `callback`: `Callable[[str], None]` - (Optional) Logs progress output updates.
* **Returns**: `str` - Task Job ID string.

```python
job_id = RepairSDK.trigger_dism_cleanup()
```

---

### 3. `trigger_chkdsk(callback=None)`
Schedules a check disk scan on the primary volume.

* **Parameters**:
  - `callback`: `Callable[[str], None]` - (Optional) Logs progress output updates.
* **Returns**: `str` - Task Job ID string.

```python
job_id = RepairSDK.trigger_chkdsk()
```

---

### 4. `get_job_status(job_id)`
Queries the execution state of a background job task.

* **Parameters**:
  - `job_id`: `str` - Targeted job task ID.
* **Returns**: `dict` - Status dictionary containing `status` ("RUNNING", "COMPLETED", "FAILED") and `output` log strings.

```python
status = RepairSDK.get_job_status(job_id)
print(f"Current State: {status['status']}")
```
