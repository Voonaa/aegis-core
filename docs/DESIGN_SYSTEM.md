# Design System & Styling Tokens: AWUT

This document describes the design tokens (spacing, typography, color palettes, and border radius variables) implemented within the **Advan Workplus Ultimate Toolkit (AWUT)** matching modern UI design guidelines.

---

## 1. Visual Color Palettes (Theme Tokens)

| Token Name | Light Value | Dark Value | Purpose |
| :--- | :--- | :--- | :--- |
| `BG_PRIMARY` | `#F3F4F6` | `#1A1A1A` | Main viewport backgrounds |
| `BG_SIDEBAR` | `#E5E7EB` | `#111827` | Navigation sidebar background |
| `BG_CARD` | `#FFFFFF` | `#1F2937` | Dashboard metric widgets background |
| `BORDER` | `#D1D5DB` | `#374151` | Dividers, boundaries, card borders |
| `TEXT_MAIN` | `#111827` | `#FFFFFF` | Primary headers and core values |
| `TEXT_MUTED` | `#4B5563` | `#9CA3AF` | Captions, descriptions, sub-labels |
| `ACCENT_BLUE` | `#2563EB` | `#3B82F6` | Selection states, focus, active actions |
| `STATUS_GOOD` | `#10B981` | `#10B981` | Green LED, successful run logs |
| `STATUS_WARN` | `#F59E0B` | `#FACC15` | Yellow LED, warnings, config recommendations |
| `STATUS_ERR` | `#EF4444` | `#EF4444` | Red LED, failures, BSOD alerts |

---

## 2. Layout Spacing Grid

AWUT layouts use a strictly enforced linear spacing scale. Padding and margins must only use the values below:

* **`SPACE_4`**: 4px (micro adjustment between text elements).
* **`SPACE_8`**: 8px (small spacing, internal grid elements padding).
* **`SPACE_12`**: 12px (intermediate layout padding).
* **`SPACE_16`**: 16px (standard card padding, grid margins).
* **`SPACE_24`**: 24px (large page margin offset).
* **`SPACE_32`**: 32px (container block separations).
* **`SPACE_48`**: 48px (major component sections spacing).

---

## 3. Typography Rules

The primary font family is set to **`Segoe UI`** (on Windows) or **`sans-serif`** fallbacks. Monospace operations use **`Consolas`**.

* **`FONT_TITLE`**: Size 24pt, Semi-Bold. Used for Main Header branding (Sidebar brand).
* **`FONT_HEADER`**: Size 18pt, Semi-Bold. Used for View page headings.
* **`FONT_SECTION`**: Size 14pt, Medium. Used for card section dividers.
* **`FONT_BODY`**: Size 12pt, Regular. Standard body text.
* **`FONT_CAPTION`**: Size 10pt, Regular. Used for sub-labels and small timestamps.

---

## 4. Border Radius Scale

* **`RADIUS_S` (4px)**: Standard buttons, progress bars.
* **`RADIUS_M` (8px)**: Entry inputs, small popovers.
* **`RADIUS_L` (12px)**: Cards, sidebar container components.
* **`RADIUS_FULL` (9999px)**: Circular buttons, status indicator LEDs.
