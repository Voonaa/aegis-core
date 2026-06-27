# System Optimization

The Aegis Core Platform includes an optimization subsystem that allows users to modify active power profiles, CPU speed throttling settings, and Windows indexing parameters to fit active workloads. These adjustments are executed safely through a structured planning, validation, and backup rollback cycle.

---

## Power Profiles Overview

Aegis allows users to select between three preconfigured system presets:

### 1. ⚡ Performance Profile (Gaming & Heavy Workloads)
-   **Core Action**: Sets the active Windows power scheme to **High Performance** (Power Plan GUID: `8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c`).
-   **Tuning Details**: Min/Max CPU processor state set to 100% to prevent latency overhead during core clock shifts.
-   **Registry Tweaks**: Optimizes processor core parking thresholds and disables energy-saving network sleep modes.
-   **Result**: Maximum system throughput, at the cost of higher power draw and fan speeds.

### 2. ⚖️ Balanced Profile (General Use)
-   **Core Action**: Sets the active Windows power scheme to **Balanced** (Power Plan GUID: `381b4222-f694-41f0-9685-ff5bb260df2e`).
-   **Tuning Details**: Enables dynamic CPU scaling (Min: 5%, Max: 100%), allowing clocks to drop during idle times.
-   **Result**: Optimizes thermals and battery lifespan for everyday web browsing and office productivity.

### 3. 🔋 PowerSaver Profile (Extended Battery Life)
-   **Core Action**: Sets the active Windows power scheme to **Power Saver** (Power Plan GUID: `a1841308-3541-4fab-bc81-f71556f20b4a`).
-   **Tuning Details**: Caps the maximum processor state to 70% to limit power draw, slows down background Search indexers, and darkens display settings.
-   **Result**: Maximum battery runtime, suitable for travel or low-charge situations.

---

## Safe Execution Lifecycle

Aegis enforces a strict safety lifecycle when applying system tweaks:

```text
┌────────────────────────────────────────────────────────┐
│                   Pre-Check Query                      │
│      Validates current registry permissions & UAC      │
└───────────────────────────┬────────────────────────────┘
                            │ Approved
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Backup Generation                    │
│      RollbackEngine creates local JSON state recovery  │
└───────────────────────────┬────────────────────────────┘
                            │ Saved
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Execution Phase                      │
│     OptimizationExecutor applies powercfg directives    │
└───────────────────────────┬────────────────────────────┘
                            │ Applied
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Post-Apply Verification                │
│     OptimizationValidator checks telemetry delta changes│
└────────────────────────────────────────────────────────┘
```

1.  **Safety Verification (Pre-Check)**: The engine queries system configurations and UAC status. If registry alterations require admin credentials, it prompts for elevation.
2.  **Backups Creation**: The `RollbackEngine` records the active power plan GUID and system settings to a time-stamped JSON file inside `apps/desktop/config/backups/`.
3.  **Directives Application**: The `OptimizationExecutor` calls elevated processes to apply target tweaks.
4.  **Delta Validation**: The `OptimizationValidator` compares pre- and post-optimization telemetry snapshot deltas (such as changes in active power scheme and free RAM memory bytes) to confirm successful application.

---

## Restoring Configurations (Rollback)

If an optimization causes instability, you can reverse changes immediately:
-   **Via Graphical Interface**: Go to the **Settings** or **Optimization** page and click **Restore Settings**.
-   **Backup File Recovery**: Aegis will read the latest backup file in `apps/desktop/config/backups/restore_YYYYMMDD_HHMMSS.json`, parse the original values, and switch the active power plan back using `powercfg /setactive <GUID>`.
