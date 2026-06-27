# ADR-0007: Embedded Developer Console (CLI inside GUI)

## Status
Approved

## Context
Aegis Toolkit is designed as a platform for both typical users (who prefer graphical buttons) and system administrators/developers (who prefer keyboard interfaces). Adding keyboard interfaces enhances diagnostic speeds and adds a professional terminal look to the application.

We evaluated two options:
1. **Dual Executables**: Ship a separate CLI binary (`aegis.exe`) and GUI binary (`aegis-gui.exe`). This increases compiled asset size and complicates communication channels between processes.
2. **Embedded CLI Console**: Create an interactive shell text field inside the GUI itself. Typing commands executes backend module functions and prints log outputs directly to the embedded terminal screen.

## Decision
We will build an **Embedded Developer Console** at the bottom of the UI frame. 

It consists of:
* A read-only text terminal widget (`ConsoleTerminal`).
* A text input entry widget (`ConsoleInput`) where users type CLI commands.

### Supported CLI Syntax:
- `aegis> help` : List all available console automation codes.
- `aegis> profile <profile_name>` : Manually load and enforce a system profile.
- `aegis> repair <sfc | dism | network>` : Run background diagnostic tasks.
- `aegis> status` : Print dynamic telemetry JSON report.
- `aegis> clear` : Clear console log screen buffer.

## Consequences
* Keyboard events must bind the `Return` / `Enter` key to command parser evaluations.
* Commands run asynchronously using Python's `threading` modules to keep UI animations responsive.
* All stdout outputs from executing tasks are routed to both `logs/aegis.log` and the UI `ConsoleTerminal`.
