# Feature Matrix: Aegis Toolkit

This matrix maps functional features across the planned version releases of the **Aegis Toolkit (Aegis)** platform.

| Feature Area | Specific Function | v1.0 (Alpha/Core) | v2.0 (Smart Telemetry) | v3.0 (AI Diagnostic) | v4.0 (Enterprise) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **GUI Framework** | Multi-frame Routing & Sidebar | ✅ | ✅ | ✅ | ✅ |
| | Developer Console (Embedded CLI) | ✅ | ✅ | ✅ | ✅ |
| **System Telemetry** | High-Freq CPU, RAM, Disk Polling | ✅ | ✅ | ✅ | ✅ |
| | S.M.A.R.T SSD Health & Battery stats | ❌ | ✅ | ✅ | ✅ |
| **Device Profiling** | WMI Manufacturer / Model queries | ✅ | ✅ | ✅ | ✅ |
| | Custom profile adjustments (JSON specs)| ❌ | ✅ | ✅ | ✅ |
| **Health Engine** | Basic telemetry scoring (CPU/RAM/Temp)| ❌ | ✅ | ✅ | ✅ |
| | Weighted health score (SSD/Battery/OS) | ❌ | ✅ | ✅ | ✅ |
| **System Repairs** | Background SFC & DISM executing | ✅ | ✅ | ✅ | ✅ |
| | Asynchronous GUI logging console | ✅ | ✅ | ✅ | ✅ |
| **Backup Utilities** | Registry & Wi-Fi profile exporter | ✅ | ✅ | ✅ | ✅ |
| | Driver backups & restoration | ❌ | ✅ | ✅ | ✅ |
| **AI Diagnosis** | Conflict detection (VMware vs Hyper-V) | ❌ | ❌ | ✅ | ✅ |
| | BSOD Minidump crash parser | ❌ | ❌ | ✅ | ✅ |
| **Extensibility** | Dynamic JSON plugin configurations | ❌ | ❌ | ❌ | ✅ |
| | Cloud configuration synchronizer | ❌ | ❌ | ❌ | ✅ |
