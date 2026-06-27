# Sprint 1 Prompt Blueprint

Feed this prompt to the AI when executing Sprint 1.

---

```markdown
We are ready to execute **Sprint 1: Boilerplate Infrastructure** for Aegis.

### 🎯 Objective:
Create the workspace configurations, default profiles, logging subsystem, and initialize a basic main CustomTkinter window.

### 📋 Files to Generate:

1. **`src/config/settings.json`**:
   - Store settings: app title ("Aegis Toolkit"), version, logging verbosity ("INFO"), default telemetry update speed (1000ms), and admin authorization requirements.

2. **`src/config/theme.json`**:
   - Map color hex codes for dark mode matching the design system in `docs/DESIGN_SYSTEM.md`.

3. **`src/core/logger.py`**:
   - Setup log rotate behavior writing to `logs/aegis.log`.
   - Implement SubsystemLoggerAdapter to inject subsystem labels automatically in standard format:
     `[TIMESTAMP] | [LEVEL] | [SUBSYSTEM] | [MESSAGE]`

4. **`src/app.py`**:
   - The main application launcher class `AegisApp` inheriting from `customtkinter.CTk`.
   - Setup properties: window size (1020x640), clean window title, and initialize logging and setting variables.

### 🛡 Implementation Rules:
- Strictly follow `docs/CODING_STANDARD.md` and `docs/LOGGING_POLICY.md`.
- Do NOT create files outside the Sprint 1 scope (no sidebar, telemetry polling, or repair logic yet).
- Provide a summary of the code and instructions on how to test it.
```
