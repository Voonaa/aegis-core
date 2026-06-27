# Coding Standards & Quality Guidelines: Aegis

This document outlines the strict quality guidelines and code conventions required for the **Aegis Toolkit (Aegis)** codebase.

---

## 1. Syntax & Typing Rules

* **Python Version**: Strict target of Python 3.12+.
* **Type Hints**: Type annotations are mandatory for all public functions, methods, parameters, and class variables.
* **PEP 8 Compliance**: Code must follow standard PEP 8 formatting rules (indentation using 4 spaces, clean variable naming).
* **Docstrings**: All functions, methods, and classes must have descriptive docstrings explaining their purpose, arguments, and return types. Use Google style.

---

## 2. Directory Rules & Packages

* **Modular Imports**: Every subdirectory inside `core/`, `ui/`, and `modules/` must contain an `__init__.py` file to define a clean public API for that package.
* **No Circular Imports**: Do not import UI components inside Core or Automation modules. Use event-based mechanisms or callbacks to send notifications back to the UI.
* **Path Management**: Never use hardcoded Windows path strings or `os.path`. Use Python's `pathlib.Path` exclusively.

---

## 3. Structural Rules & Clean Code Patterns

* **Composition over Inheritance**: Use composition to share logic between helper utility classes rather than deeply nested inheritance trees.
* **UI Components**: Every page element must inherit from `customtkinter.CTkFrame`.
* **Zero Global Variables**: Global variables are strictly prohibited. Application state must reside inside an instantiated context manager or configuration class.
* **No Magic Numbers**: Avoid arbitrary numerical configurations. UI sizing, polling delays, and system timeout integers must be declared as constants.
* **Error Handling**: All system automation code must be wrapped inside `try-except` blocks. Never silence exceptions; always log the traceback using the system logger.
* **Logging Standard**: Use Python's standard `logging` library. Use SubsystemLoggerAdapter to tag subsystem contexts automatically.
