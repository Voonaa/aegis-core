# Project Specification: Aegis Toolkit v1.0

## 1. Vision & Purpose
Aegis Toolkit (Aegis) is a professional Windows System Management Platform designed for advanced hardware telemetry, diagnostics, and repairs. Unlike standard single-device optimizers, Aegis features a dynamic Device Profile Engine that queries system BIOS details to adapt its optimization scripts specifically to the host laptop's manufacturer (e.g. Advan Workplus, ASUS TUF, HP Victus, Lenovo Legion).

Aegis is built to demonstrate enterprise-grade engineering principles including modular Clean Architecture, WMI telemetry integrations, thread-safe asynchronous GUI event loops, and an embedded keyboard-driven Developer Console.

---

## 2. Key Modules & Features

### ⚡ Device Profile & Performance Engine
* **Dynamic Profiles Detection**: Auto-detects manufacturer on start. Activates profile overlays containing settings for custom power plans, fan controllers (if available), and relevant system service tweaks.
* **Performance Presets**:
  - **Daily Mode**: Optimizes settings for regular work, prioritizing low thermals.
  - **Developer Mode**: configures environment paths, enables docker/virtualization priorities.
  - **Gaming Mode**: Stops unnecessary background services, clears standby lists.
  - **AI Mode**: Configures configurations for local LLM inference engines.

### 🛠 Windows Repair & System Actions
* **Background SFC & DISM**: Performs background system repair scans inside a dedicated worker thread.
* **Virtualization Conflicts Manager**: Toggles Hyper-V configuration parameters to prevent running issues with VMware/VirtualBox virtualization.
* **Network & DNS Resolvers**: Resets socket APIs, flushes DNS records, tests connections.

### 📊 Health Score Telemetry Engine
* **Pillar Scorer**: Gathers telemetry for SSD (SMART status), Battery (wear cycles), Thermals, Memory allocations, and OS logs.
* **Overall Health Index (0-100)**: Displays a combined overall score indicating system health alongside recommended optimizations.

### 💻 Developer Console (CLI inside GUI)
* **CLI Input Box**: Located at the bottom of the dashboard viewport. Exposes keyboard-driven commands (`aegis> repair windows`, `aegis> status`, etc.).

---

## 3. UI Layout Wireframe

```text
+------------------------------------------------------------------------+
|  🛡 AEGIS TOOLKIT v1.0                                       [ - ] [ X ]|
+------------------------------------------------------------------------+
| 🏠 Dashboard      |  System: Advan Workplus   Health: [ 96 / 100 ]     |
| ⚡ Performance    |  +---------------------+  +---------------------+  |
| 🛠 Maintenance    |  | CPU: Ryzen 5 6600H  |  | SSD Health: 84%     |  |
| 📊 Monitoring     |  | Util: 18%  43°C     |  | Good - S.M.A.R.T    |  |
| 🎮 Gaming         |  +---------------------+  +---------------------+  |
| 💻 Developer      |                                                    |
| 🖥 Drivers         |  [ CPU & Memory Performance Analytics Graph ]      |
| 💾 Backup         |  +-----------------------------------------------+ |
| ⚙ Settings       |  | (Live Matplotlib CPU/RAM trend lines)          | |
|                   |  +-----------------------------------------------+ |
+-------------------+----------------------------------------------------+
| aegis> repair network                                                  |
+------------------------------------------------------------------------+
| Status: Routing CLI command...                                         |
+------------------------------------------------------------------------+
```
