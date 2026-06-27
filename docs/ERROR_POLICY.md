# Error Management & Recovery Policy: Aegis

This document outlines exception handling models, error classifications, notification standards, and recovery protocols for the **Aegis Toolkit (Aegis)**.

---

## 1. Exception Handling Architecture

All operations interfacing with the operating system kernel or calling subprocesses must run inside `try-except-finally` blocks.

---

## 2. Specific Failure Recovery Scenarios

### 🔹 Subprocess Actions (DISM, SFC, Restore Point)
* **Failure Case**: Command exits with non-zero return code, or throws timeout exception.
* **Mitigation**:
  1. Capture the raw stderr data.
  2. Write details using `logger.error()`.
  3. Stop the active progress bar, changing its accent color to `#EF4444` (Danger red).
  4. Print troubleshooting directions inside the UI `ConsoleTerminal`.

### 🔹 WMI Hardware Diagnostics
* **Failure Case**: WMI querying raises COM exceptions (common when executing queries inside restricted environments).
* **Mitigation**:
  1. Log a warning description (`logger.warning`).
  2. Fall back instantly to querying data using native Python libraries (`psutil`).
  3. If fallbacks fail, set values on the Dashboard view components to `"N/A"` or `"Unavailable"`.

### 🔹 Device Profile Matching
* **Failure Case**: Host motherboard manufacturer cannot be parsed, or the matching JSON profile is corrupted.
* **Mitigation**:
  1. Log an error describing the failure.
  2. Gracefully fall back to loading the default profile configuration: `generic_windows.json`.

### 🔹 Startup Admin Validation
* **Failure Case**: Aegis is launched without elevated privileges (admin rights).
* **Mitigation**:
  1. Display a warning notification or console log warning.
  2. Continue executing in read-only mode, and lock commands that alter system status (like registry modifications or system file fixes). Show UAC shields on locked actions.
