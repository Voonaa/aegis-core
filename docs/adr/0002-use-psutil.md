# ADR-0002: Use psutil for System Diagnostics & Telemetry

## Status
Approved

## Context
AWUT requires high-frequency (1.0 second intervals) hardware metrics polling on CPU utilization, physical RAM distribution, and storage partition occupancy to feed the dashboard charts and widgets.

We evaluated two approaches for retrieving these values:
1. **WMI Queries / PowerShell subprocesses**: Using `wmi` classes like `Win32_Processor` or spawning PowerShell tools like `Get-Counter`. While built-in, WMI calls take 50ms - 200ms to complete, causing unacceptable GUI stuttering and CPU usage overhead if called every second.
2. **`psutil` Library**: A cross-platform Python C-extension that queries OS telemetry APIs directly in C. Queries complete in microseconds with zero GUI lag and extremely low processor consumption.

## Decision
We will use **`psutil`** for all high-frequency diagnostic measurements (CPU usage %, RAM usage ratio, Disk storage capacity).

## Consequences
* `psutil` must be added as a dependency in `requirements.txt`.
* Because `psutil` utilizes compiled C-extensions, we must specify dynamic library parameters during PyInstaller compilation.
