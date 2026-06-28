# Sprint 4: Maintenance Subprocess Automation

## 1. Objectives
Implement the PowerShell background execution system and the CLI command router for the Developer Console. Connect execution threads to print stdout records to the terminal logs view.

---

## 2. Target Files & Locations

### 1. `src/core/powershell.py`
High-level execution utility. Spawns processes securely, capture stdout line-by-line using generator wrappers.

### 2. `src/modules/console_router.py`
- Command router that parses typed strings from the Developer Console input (e.g. `repair sfc`, `profile load advan`).
- Maps matches to call execution threads.

### 3. `src/modules/repair/`
Contains modular Python wrappers for calling Windows SFC scans, DISM integrity fixes, network resets, and drivers exporters.

### 4. `src/ui/maintenance.py` (Modify)
- Renders button triggers for system repair commands.
- Toggles buttons to `disabled` when an action starts, unlocking them on process completion.
- Streams stdout lines directly to the log terminal screen.

---

## 3. Verification Criteria
* Typing `repair network` in the CLI input box must launch DNS flush scripts and print logs.
* Action buttons must run repairs inside background threads without freezing UI controls.
* All repair tasks must log process codes into `logs/aegis.log`.
