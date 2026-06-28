# Sprint 5: BSOD Crash Analyzer & Packaging

## 1. Objectives
Implement the BSOD Minidump crash diagnostic engine. Create automated recommendation warnings for VM/virtualization conflicts and compile the application executable.

---

## 2. Target Files & Locations

### 1. `src/core/windows.py`
- Parse `C:\Windows\Minidump` crash files to retrieve bug check identifiers and target offending drivers.
- Match results to repair suggestions.

### 2. `src/ui/dashboard.py` (Modify)
- Perform BSOD scans on boot.
- Render conflict warnings if VMware is installed but Hyper-V is running.

### 3. `build_executable.py` (New Root Script)
- Package the toolkit into a standalone `Aegis.exe` executable using `PyInstaller`.
- Include Windows administration flags manifest definitions.

---

## 3. Verification Criteria
* Compile the application by running `python build_executable.py`.
* Ensure `dist/Aegis.exe` launches correctly and requests admin privileges.
* Mock a crash file and ensure the UI outputs diagnostic warnings.
