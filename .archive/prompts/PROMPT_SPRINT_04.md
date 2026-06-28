# Sprint 4 Prompt Blueprint

Feed this prompt to the AI when executing Sprint 4.

---

```markdown
We are ready to execute **Sprint 4: Maintenance Subprocess Automation** for Aegis.

### 🎯 Objective:
Implement the PowerShell background subprocess manager and establish the Developer Console command router.

### 📋 Files to Generate/Modify:

1. **`src/core/powershell.py`**:
   - Asynchronous shell script runner capturing process stdout lines via generators.

2. **`src/modules/console_router.py`**:
   - Router module to match typed CLI commands (e.g. `repair sfc`, `status`, `help`) and trigger matching thread actions.

3. **`src/modules/repair/`**:
   - Repair wrappers executing SFC, DISM, Winsock resets, and drivers exporters.

4. **`src/ui/maintenance.py` (Modify)**:
   - Renders repair buttons and links them to thread execution processes, streaming outputs to the terminal window.

### 🛡 Implementation Rules:
- All execution tasks must run on a background thread.
- Handle UAC permissions exceptions and print errors directly to the terminal view.
```
