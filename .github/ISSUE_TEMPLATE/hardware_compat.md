---
name: 💻 Hardware Compatibility Report
about: Report motherboards, bios, or WMI hardware telemetry issues on non-Advan hosts.
title: "[HW] <Motherboard / CPU Model>"
labels: hardware-compat
assignees: ''

---

**Hardware Description**
- Manufacturer: [e.g. ADVAN, ASUS, Lenovo]
- Product Model: [e.g. Workplus, Zenbook UX3402]
- CPU Model: [e.g. AMD Ryzen 7 7730U]
- RAM Size: [e.g. 16 GB]

**WMI / HAL Telemetry Status**
Please report if any HAL harvesters fail to gather data:
- [ ] CPU utilization & temp query
- [ ] GPU model & load
- [ ] Battery health & wear rate
- [ ] Disk status & write rates

**Telemetry Stats Diagnostics Output**
Paste the terminal output from the CLI command `telemetry stats` if available.
