# ADR-0004: Use JSON for Configuration and Themes

## Status
Approved

## Context
AWUT requires persistent, human-readable config systems to store application configurations (telemetry intervals, logging level) and visual configurations (colors, theme configurations).

We evaluated the following formats:
1. **SQLite Database**: High overhead and binary format. Overkill for simple configurations.
2. **INI (`configparser`)**: Simple and built-in, but struggles to represent nested styling objects or array collections.
3. **YAML**: Clean syntax, but requires importing external packages (like `PyYAML`), complicating the build system.
4. **JSON (JavaScript Object Notation)**: Native to Python via the `json` module, easily represents nested key-value pairs, human-readable, and maps 1-to-1 with Python dictionaries.

## Decision
We will use **JSON** files (`settings.json` and `theme.json`) located in `src/config/` for all application parameters and GUI design configurations.

## Consequences
* All settings and design system colors can be read and written using standard Python dictionary methods.
* We must write wrapper handlers in `core/helper.py` to recreate default JSON configs if the files are deleted or corrupted.
