# User Interface Specification: AWUT

This document describes the layout grids, coordinates, responsive parameters, and frame relationships of the **Advan Workplus Ultimate Toolkit (AWUT)** desktop application.

---

## 1. Global Shell Structure
AWUT is designed around a responsive grid structure using CustomTkinter. The layout is divided into a left navigation sidebar and a right viewport.

```text
+-----------------------------------------------------------------------+
|  AW Logo | Titlebar Brand Area                             [ - ] [ X ]|
+----------+------------------------------------------------------------+
|          |                                                            |
|          | Viewport Area (Page Frame Container)                       |
|          |                                                            |
|          | +--------------------------------------------------------+ |
| Sidebar  | |                                                        | |
| Frame    | | Active Page Frame (Dashboard / Maintenance / etc.)     | |
|          | |                                                        | |
|          | +--------------------------------------------------------+ |
|          |                                                            |
+----------+------------------------------------------------------------+
| Version  | Status Indicator Bar                                       |
+-----------------------------------------------------------------------+
```

### Dimensions & Grid Grid Weight
* **Window Size (Default)**: 1020px width x 640px height.
* **Window Size (Minimum)**: 800px width x 500px height.
* **Columns Layout**:
  - Column 0 (Sidebar): Width 240px (non-resizable, `weight=0`).
  - Column 1 (Viewport): Flex-grow (`weight=1`).
* **Rows Layout**:
  - Row 0 (Page Contents): Flex-grow (`weight=1`).
  - Row 1 (Statusbar): Height 24px (non-resizable, `weight=0`).

---

## 2. Page Specific Layouts

### 🏠 Dashboard Page
The Dashboard page uses a two-column grid. Column 0 contains the hardware telemetry cards, and Column 1 contains status indicator badges and performance trend graphs.

```text
+----------------------------------------------------------------------+
|  [ CPU: Ryzen 5 6600H ]      [ RAM: 7.2 / 16.0 GB ]                  |
|  Usage: 18%  Temp: 43°C      Usage Bar: [========----]               |
+----------------------------------------------------------------------+
|  [ SSD: 512GB NVMe ]         [ Battery Status ]                      |
|  Health: 84% - Good          Capacity: 92% - Charging                |
+----------------------------------------------------------------------+
|  [ Performance Analytics Graph ]                                      |
|  +----------------------------------------------------------------+  |
|  | (Live Matplotlib CPU/RAM trend line chart)                      |  |
|  +----------------------------------------------------------------+  |
+----------------------------------------------------------------------+
|  🔴 Hyper-V Conflict Alert Card (Only visible when VMware is running) |
+----------------------------------------------------------------------+
```

### 🛠 Maintenance & Repair Page
The Maintenance page contains action triggers and a simulated terminal console.

```text
+----------------------------------------------------------------------+
| Windows Integrity:    [ Run SFC Scan ]        [ Run DISM Restore ]    |
| Storage Maintenance:  [ Run CHKDSK ]          [ Optimize SSD ]        |
| Network Automation:   [ Flush DNS Cache]      [ Reset TCP/IP Stack ]  |
+----------------------------------------------------------------------+
| Live Action Terminal Console:                                        |
| +------------------------------------------------------------------+ |
| | [2026-06-27 10:49:15] [INFO] Launching SFC Integrity Scan...      | |
| | [2026-06-27 10:49:20] [INFO] Progress: 14% completed.             | |
| |                                                                  | |
| +------------------------------------------------------------------+ |
+----------------------------------------------------------------------+
```

### ⚙ Settings Page
Simple form panel to handle configurations.
- **Subsystem Toggles**: Logging Level Combo-box (DEBUG, INFO, ERROR), Telemetry Tick rate dropdown (1s, 2s, 5s).
- **Paths Directory Display**: Displays values of `APPDATA`, `logs/`, `backup/` folders.
- **Restore Options**: Trigger button to create restore point.
