# Component Library Specification: AWUT

This document outlines the standard UI components, structural styling variables, padding guidelines, and font rules designed for CustomTkinter widgets to ensure visual consistency.

---

## 1. Widget Anatomy & Specifications

### 🔹 Card Container (`MetricCard`)
A card-like container used to display telemetry info.
* **Base Widget**: `customtkinter.CTkFrame`
* **Border Radius**: 12px
* **Padding**: 16px (internal)
* **Colors**:
  - Background: `#1F2937` (Dark Slate)
  - Border Color: `#374151`
  - Hover Background: `#374151`
* **Layout Grid**:
  - Row 0: Label (Title) - 12pt regular, color `#9CA3AF`.
  - Row 1: Label (Large Value) - 22pt bold, color `#FFFFFF`.
  - Row 2: Status sub-label or mini progress bar.

### 🔹 Progress Bar Card (`ProgressBarCard`)
Used for RAM and SSD usage tracking.
* **Base Widget**: `MetricCard` with nested `customtkinter.CTkProgressBar`.
* **Progress Bar Height**: 8px
* **Border Radius**: 4px
* **Progress Colors**:
  - Normal (<80%): `#2563EB` (Primary blue)
  - Warning (80% - 90%): `#FACC15` (Warning yellow)
  - Critical (>90%): `#EF4444` (Danger red)

### 🔹 Status Indicator LED Badge (`StatusBadge`)
A visual badge demonstrating service statuses.
* **Base Component**: Horizontal layout frame containing a Canvas circle (diameter 12px) and a Label text.
* **LED Status Colors**:
  - Good/Active (🟢): `#22C55E`
  - Configured/Inactive (🟡): `#FACC15`
  - Error/Conflict (🔴): `#EF4444`
* **Spacing**: 8px margin between the LED dot and the label text.

---

## 2. Interactive Controls

### 🔹 Sidebar Button (`SidebarButton`)
* **Base Widget**: `customtkinter.CTkButton`
* **Dimensions**: Height 40px, Width 220px.
* **Border Radius**: 6px
* **Colors**:
  - Default: transparent
  - Hover: `#374151`
  - Selected: `#2563EB` (Primary blue)
* **Fonts**: Regular 14pt, alignment: `W` (West/Left aligned) with 12px leading indent.

### 🔹 Console Terminal Output Window (`ConsoleTerminal`)
* **Base Widget**: `customtkinter.CTkTextbox`
* **Colors**:
  - Background: `#0A0E17`
  - Text Foreground: `#E5E7EB`
  - Scrollbar: Custom dark style
* **Fonts**: `Consolas` or `Courier New`, 11pt, monospace.
* **Config**: Strict state `disabled` to prevent manual text entry. Automatic auto-scroll handling on append (`see(tkinter.END)`).
* **Tags**: Color tag definitions for logger outputs: `[INFO]` -> white, `[WARNING]` -> yellow, `[ERROR]` -> red.
