# Testing Strategy & Test Plan: Aegis

This document outlines the testing methodology, automated test coverage, mocking standards, and manual validation checklists for the **Aegis Toolkit (Aegis)**.

---

## 1. Automated Test Framework
* **Testing Tool**: `pytest`
* **Test Directory**: `tests/`
* **Coverage Target**: 80% coverage on core logic modules (`core/` and `modules/`).

---

## 2. Mocking Guidelines (OS Independence)
All Windows API or WMI hardware system hooks must be mocked out to enable test runs on Linux/macOS dev rigs or CI environments.

* **Standard mocks (`tests/conftest.py`)**:
  - Mock WMI namespace object queries.
  - Mock `psutil` telemetry metrics.
  - Mock subprocess calls executing PowerShell system commands.

---

## 3. Test Cases Directory Structure

* **`tests/test_core/`**:
  - `test_logger.py`: Verifies logger adapter formatting and file-based rotation triggers.
  - `test_profile.py`: Verifies matching BIOS vendor string to corresponding JSON profiles.
  - `test_health.py`: Verifies mathematical equations for the overall Health Score.
  - `test_powershell.py`: Verifies async script streaming.

* **`tests/test_ui/`**:
  - `test_console_router.py`: Verifies typing keyboard commands route to the correct execution callbacks (e.g. `aegis> status`).

---

## 4. Manual UI/UX Testing Checklist

| Test View | Action Trigger | Expected Behavior |
| :--- | :--- | :--- |
| **Global View** | Boot Application | Queries hardware details and displays the recognized Device Profile name (e.g. Advan Workplus) on the status bar |
| **Global View** | Type in Dev Console | `aegis> help` displays command descriptions in the terminal console |
| **Dashboard** | Temperature > 65C | Overall Health Score decreases dynamically by 0.5 points per 1C excess |
| **Maintenance** | Click Repair Action | Command executes asynchronously without blocking view resize actions |
