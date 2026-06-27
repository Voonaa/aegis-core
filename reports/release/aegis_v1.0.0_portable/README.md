# 🛡 Aegis Core Platform

[![CI Pipeline Status](https://github.com/Voonaa/aegis-core/actions/workflows/ci.yml/badge.svg)](https://github.com/Voonaa/aegis-core/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **One Click. One Platform. Total Control.**
> An enterprise-grade, modular Windows Diagnostics & System Management Platform engineered to analyze telemetry, run async repair jobs, and dynamically score host health.

---

## 🏛 Platform Architecture

Aegis is engineered as a decoupled monorepo, cleanly isolating core systems, desktop representations, and dynamic extension plugins.

```text
Aegis Core Platform (Monorepo)
├── apps/
│   └── desktop/           # CustomTkinter GUI presentation layer
├── packages/
│   ├── core/              # HAL engines, dependency injection, and event buses
│   └── sdk/               # Public API entry point wrapper classes
├── plugins/               # External runtime manifest extensions
├── scripts/               # Quality linter and automated release tools
└── tests/                 # Unit test coverage files
```

### Decoupled Subsystem Pipeline
```text
Hardware (WMI / WinReg) -> HAL Telemetry -> Health Scoring -> Recommendation Engine
                                                                    │
GUI Desktop Viewports <------ EventBus <------ JobManager <─────────┘
```

---

## 🚀 Key Features

* **Hardware Abstraction Layer (HAL)**: Dynamic polling of CPU loads, RAM capacities, SSD SMART health parameters, battery degradation metrics, and active virtualisation hypervisor environments.
* **Asynchronous Job Manager**: Asynchronous, thread-safe background process scheduler executing SFC, DISM, and CHKDSK utilities without freezing the main visual window.
* **Rules-Based Recommendation Engine**: Real-time evaluation of host hardware parameters against threshold guidelines to suggest context-aware system optimization advices.
* **Extensibility Plugin SDK**: Dynamic folder-based runtime extensions loading custom manifes JSONs, verifying admin access boundaries, and triggering standard lifecycle hooks (`initialize`, `start`, `dispose`).
* **Design Tokens styling**: Fully customizable aesthetic parameters (`theme.json`) regulating sizes, typography font weights, margins, and corners dynamically.

---

## 🛠 Quick Start Guide

### Prerequisites
* **Windows OS** (Recommended: Windows 10/11)
* **Python 3.11+** installed and added to PATH.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Voonaa/aegis-core.git
   cd aegis-core
   ```
2. Install system dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution
Launch the Aegis Desktop UI wrapper:
```bash
$env:PYTHONPATH="."
python apps/desktop/main.py
```

---

## 🔌 Writing Plugins (Aegis Plugin SDK)

Dynamic plugin folders reside inside the `plugins/` directory. Each extension plugin must contain:
1. A manifest file: `manifest.json`
2. An entry script: `main.py`

### 1. Manifes Setup (`manifest.json`)
```json
{
  "name": "Network Latency Extension",
  "version": "1.0.0",
  "author": "System Administrator",
  "description": "Performs latency verification diagnostics.",
  "permissions": ["filesystem"],
  "entry_point": "main.py"
}
```

### 2. Lifecycles Implementation (`main.py`)
```python
def initialize(container):
    """Invoked when the plugin is loaded into the DI Container."""
    print("Network extension registered.")

def start():
    """Invoked when the platform bootstrap completes."""
    print("Network diagnostics active.")

def dispose():
    """Invoked when the app shuts down."""
    print("Network extension teardown.")
```

---

## 📦 Automated Release Pipeline

Aegis includes automated packaging and release compilation tools. Running the release script verifies code compliance, runs unit tests, and packages a portable distribution folder containing calculated checksums:

```powershell
# Run the release pipeline script
.\scripts\release.ps1
```

The output folder is compiled under:
`release/aegis_v1.0.0-rc2_portable/`

---

## 🛡 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
