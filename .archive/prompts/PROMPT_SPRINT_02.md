# Sprint 2 Prompt Blueprint

Feed this prompt to the AI when executing Sprint 2.

---

```markdown
We are ready to execute **Sprint 2: UI View Routing & Shell** for Aegis.

### 🎯 Objective:
Build the UI frame layout routing mechanism, navigation sidebar, and the bottom-embedded Developer Console.

### 📋 Files to Generate/Modify:

1. **`src/ui/theme.py`**:
   - Class to parse and supply styling parameters from `config/theme.json` to CustomTkinter components.

2. **`src/ui/sidebar.py`**:
   - Sidebar panel class inheriting from `customtkinter.CTkFrame`.
   - Setup navigation controls (Dashboard, Maintenance, Settings) with active state indicators.

3. **`src/ui/console.py`**:
   - Renders the scrollable read-only log console (`ConsoleTerminal`) and command input entry field (`ConsoleInput`).
   - Catch Enter/Return key events to process console inputs.

4. **`src/ui/dashboard.py`**, **`src/ui/maintenance.py`**, **`src/ui/settings.py`**:
   - Basic frame layout shells for active view ports.

5. **`src/app.py` (Modify)**:
   - Integrate the Sidebar on the left, the Viewport container on the upper right, and the Developer Console on the bottom right.
   - Bind routing calls.

### 🛡 Implementation Rules:
- Enforce the separation of concern: no system API calls in UI components.
- Style parameters must read from theme config.
```
