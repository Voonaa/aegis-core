# Software Requirements Specification (SRS): Aegis Toolkit

This document defines the functional and non-functional requirements for the **Aegis Toolkit (Aegis)**, a multi-profile Windows System Management Platform.

---

## 1. Introduction
Aegis Toolkit is a desktop management application designed to query hardware configurations, perform system diagnostic checks, execute system repairs, and manage performance profiles on Windows 10/11 machines. Unlike single-device optimizers, Aegis dynamically adapts its optimization logic based on the host computer's manufacturer and model.

---

## 2. Functional Requirements (FR)

### 🔹 Device Profiling & Hardware Telemetry
* **`FR-001`**: The system **shall** query BIOS and system properties on startup via WMI (`Win32_ComputerSystem` and `Win32_BIOS`) to extract system manufacturer and model fields.
* **`FR-002`**: The system **shall** map the detected manufacturer to a dynamic Device Profile configuration. Profiles include:
  - `Advan Workplus`
  - `ASUS TUF`
  - `Lenovo Legion`
  - `HP Victus`
  - `Generic Windows Device` (Fallback)
* **`FR-003`**: The system **shall** retrieve real-time CPU model naming and dynamic processor core utilization statistics using `psutil`.
* **`FR-004`**: The system **shall** retrieve total physical RAM capacities and real-time utilization rates.
* **`FR-005`**: The system **shall** retrieve SSD details, partition capacities, and S.M.A.R.T health scores.
* **`FR-006`**: The system **shall** monitor battery statistics: current percentage capacity, charging status, and calculated battery degradation metrics.
* **`FR-007`**: The system **shall** query motherboard thermal zones to extract real-time CPU core temperatures.

### 🔹 Health Score & Recommendation Engine
* **`FR-008`**: The system **shall** compute an overall **Health Score (0-100)** on startup. Scoring weights: SSD Health (20%), Battery Health (20%), Driver Integrity (20%), OS integrity (20%), Temperature states (20%).
* **`FR-009`**: The system **shall** display dynamic warning cards recommending configurations if conflicts are caught. E.g. *If VMware is detected while Hyper-V is running, generate a Conflict Card.*

### 🔹 Maintenance & Repairs
* **`FR-010`**: The system **shall** run Windows repair tools (SFC, DISM, CHKDSK) in separate background threads, allowing concurrent execution without blocking UI controls.
* **`FR-011`**: The system **shall** display real-time terminal stdout and log records inside an embedded read-only textbox GUI widget.
* **`FR-012`**: The system **shall** offer options to run system driver exports, registry configuration backups, and WiFi password dumps.

### 🔹 Developer Console (Embedded CLI)
* **`FR-013`**: The system **shall** render a CLI textbox area (Developer Console) inside the GUI shell.
* **`FR-014`**: The system **shall** parse and execute specific text commands entered by the user (e.g. `aegis> repair windows`, `aegis> disable hyper-v`, `aegis> status`).

---

## 3. Non-Functional Requirements (NFR)

* **`NFR-001` (Telemetry Polling)**: Hardware polling loops and GUI widgets updates must occur every **1000ms** without causing user-interaction stuttering.
* **`NFR-002` (Memory Allocation)**: Application memory utilization must remain under **150MB** during idle background system telemetry polling.
* **`NFR-003` (Startup Latency)**: Cold boot and interface rendering must complete in under **2.0 seconds** on standard NVMe SSD systems.
* **`NFR-004` (Responsiveness)**: The GUI must not freeze or lock during heavy operations (e.g., driver backups). Any task exceeding 100ms execution times must run in a separate thread.
* **`NFR-005` (Security & Elevation)**: The app shall run in user mode on startup and only request UAC Administrator permission elevation when write tasks (Registry editing, SFC scans) are triggered.
* **`NFR-006` (Maintainability)**: Core logic components and visual interfaces must be decoupled. Automation logic must load modularly.
* **`NFR-007` (Compatibility)**: The system must run as a compiled executable on Windows 10/11 (x64 architectures).
