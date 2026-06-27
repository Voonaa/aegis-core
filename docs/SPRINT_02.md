# Sprint 2: UI View Routing & Shell

## 1. Objectives
Implement the application shell including the sidebar navigation panel, viewframe routing, and the embedded Developer Console CLI interface.

---

## 2. Target Files & Locations

### 1. `src/ui/theme.py`
Exposes design system variables loaded from `config/theme.json` as CTk visual configuration dictionaries.

### 2. `src/ui/sidebar.py`
The left navigation panel component. Displays the Aegis brand, version, and navigation triggers: `Dashboard`, `Maintenance`, `Settings`.

### 3. `src/ui/console.py`
The interactive CLI widget frame.
- Renders the scrollable `ConsoleTerminal` textbox.
- Renders the single-line input field `ConsoleInput` for CLI commands.
- Binds key `<Return>` to parse typed console actions.

### 4. `src/ui/dashboard.py`
Viewport containing placeholders for CPU card, RAM card, Disk card, temperatures, battery indicators, and performance graphs.

### 5. `src/ui/maintenance.py`
Page layout for repair actions and service execution buttons.

### 6. `src/ui/settings.py`
Settings configuration view.

### 7. `src/app.py` (Update)
Integrate the sidebar, main routing frame, page viewport, and the bottom Developer Console component into the layout.

---

## 3. Verification Criteria
* Run the application.
* Clicking sidebar navigation options must switch views smoothly.
* Typing into the developer console and pressing Enter must append the text to the log terminal screen.
