# ADR-0003: Use WMI and pywin32 for Low-Level Windows Telemetry

## Status
Approved

## Context
While `psutil` handles general CPU and RAM metrics, AWUT needs access to lower-level, Windows-specific telemetry details. These include CPU thermal sensor data, BIOS versions, S.M.A.R.T drive failure predictions, and detailed battery state attributes (charge degradation values).

We evaluated the following approaches:
1. **`ctypes` & Native Win32 DLL wrappers**: Direct call of system kernel DLLs (e.g. `kernel32.dll`). This is highly performant but requires writing complex C-struct wrappers in Python, which is prone to memory leaks and system crashes if signatures change.
2. **Windows Management Instrumentation (WMI)**: A standardized Microsoft SQL-like query interface built into Windows. WMI exposes classes like `Win32_Battery` and `MSStorageDriver_FailurePredictStatus` that contain all required data.

## Decision
We will use **`wmi`** (backed by **`pywin32`** for COM interface access) to query Windows hardware telemetry metrics that are unavailable through standard python libraries.

## Consequences
* Python dependencies `wmi` and `pywin32` are added to `requirements.txt`.
* Because WMI queries can be slow, they must be called at lower frequencies (e.g., every 5-10 seconds) or run on background threads to prevent UI lag.
* Virtual machines or custom hardware may not expose certain WMI namespaces (like thermals). We must write robust exceptions wrapping to provide fallback configurations.
