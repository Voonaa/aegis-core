# Sprint 5 Prompt Blueprint

Feed this prompt to the AI when executing Sprint 5.

---

```markdown
We are ready to execute **Sprint 5: BSOD Crash Analyzer & Packaging** for Aegis.

### 🎯 Objective:
Implement BSOD crash dump parsing routines, automated VM virtualization warning triggers, and configure PyInstaller packaging parameters.

### 📋 Files to Generate/Modify:

1. **`src/core/windows.py`**:
   - Diagnostic logic querying Event logs or minidump crash files (`C:\Windows\Minidump`). Parse failing driver names (e.g. `nvlddmkm.sys`) and return resolutions suggestions.

2. **`src/ui/dashboard.py` (Modify)**:
   - Include diagnostic checks on startup. Render warning cards if virtualization configs conflict (Hyper-V enabled with VMware installed).

3. **`build_executable.py` (New Root Script)**:
   - Configure PyInstaller settings to pack the workspace files into a single, UAC-elevated standalone `Aegis.exe` executable.

### 🛡 Implementation Rules:
- Gracefully handle empty or inaccessible Minidump files.
- Ensure all packaging paths map dynamically.
```
