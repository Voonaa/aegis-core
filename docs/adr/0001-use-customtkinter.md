# ADR-0001: Use CustomTkinter for Desktop GUI

## Status
Approved

## Context
AWUT requires a desktop graphical interface to display system metrics and trigger automation scripts. The interface must look modern, professional (Windows 11 Fluent style), and run efficiently on target laptops.

We evaluated three potential GUI libraries:
1. **Tkinter (Standard library)**: Highly lightweight and built-in, but looks outdated (2000s era) and lacks modern widgets (e.g. rounded frames, switches, sliders).
2. **PyQt / PySide (Qt bindings)**: Extremely powerful and native UI rendering, but introduces large executable sizes, complex licensing rules, and a steep learning curve.
3. **CustomTkinter**: A wrapper extension of native Tkinter that implements modern dark themes, rounded corners, custom progress bars, and high DPI scaling.

## Decision
We will use **CustomTkinter** for the desktop GUI layer. 

This enables us to achieve a modern VSCode-like dark theme layout out-of-the-box while maintaining the lightweight footprint of standard Tkinter event loops.

## Consequences
* All UI layouts must be designed using `customtkinter` classes (e.g. `CTkFrame`, `CTkButton`, `CTkTextbox`) instead of raw `tkinter`.
* Custom packaging rules using `PyInstaller` must include CustomTkinter assets.
* We must strictly decouple UI layout frames from system tasks to prevent blocking the GUI thread.
