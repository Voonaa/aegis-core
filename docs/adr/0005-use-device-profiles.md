# ADR-0005: Use Dynamic JSON Device Profiles

## Status
Approved

## Context
Aegis Toolkit must adjust its system optimization actions, background service toggles, and performance adjustments dynamically depending on the host computer hardware. Hardcoding check-lists or values inside Python source modules for Asus TUF, Lenovo Legion, HP Victus, or Advan Workplus is highly fragile and makes support for new systems very difficult.

We evaluated two options:
1. **Dynamic Class Inheritance**: Write custom Python adapter classes for every laptop model (e.g., `class AdvanWorkplusProfile(BaseProfile)`). This allows custom execution blocks but requires recompiling the executable for any profile updates.
2. **JSON Profile Assets**: Define device profiles in standalone JSON files (e.g., `config/profiles/advan_workplus.json`) mapping WMI vendor strings to configurations (e.g., target power plan GUID, performance services check-lists, relevant driver warnings).

## Decision
We will use **JSON Profile Assets** loaded dynamically at startup based on bios vendor properties queried via WMI (`Win32_ComputerSystem`).

On startup, Aegis will run:
```python
manufacturer = wmi.Win32_ComputerSystem()[0].Manufacturer
model = wmi.Win32_ComputerSystem()[0].Model
# Match against profile registry keys and load config/profiles/<profile_name>.json
```
If no profile is matched, load `generic_windows.json`.

## Consequences
* Simplifies addition of new laptop models; users or developers can support a new device by dropping a new JSON file into the profile folder without changing source code.
* Requires a schema validation checker to verify JSON profiles formats during initialization.
