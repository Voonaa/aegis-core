# Aegis Core Platform — CLI Reference

> Aegis Core Platform menyertakan command-line interface (CLI) untuk eksekusi headless dan diagnostik otomatis.

---

## Usage

Jalankan CLI menggunakan module launcher dengan menyetel `PYTHONPATH` terlebih dahulu:

```powershell
# Windows PowerShell
$env:PYTHONPATH="."
python -m packages.core.cli <command>
```

---

## Command Reference

### `telemetry stats`

Menampilkan snapshot diagnostik hardware secara real-time di console: CPU load, RAM usage, Disk usage, Battery health, dan Health Score.

```powershell
python -m packages.core.cli telemetry stats
```

**Example Output:**

```text
============================================================
  AEGIS CORE — SYSTEM TELEMETRY SNAPSHOT
============================================================
  CPU         :  23.4%  (12 cores)  |  Temp: 61.2°C
  RAM         :  8.1 GB / 16.0 GB   |  50.6%
  Disk        :  234 GB / 512 GB    |  45.7%  (SMART: Good)
  Battery     :  87%  (Charging)    |  Health: 94.3%
  GPU         :  2.1 GB / 8.0 GB    |  Load: 12.0%
------------------------------------------------------------
  HEALTH SCORE: 91 / 100  ✅  Excellent
============================================================
```

---

### `telemetry export <format>`

Mengekspor seluruh data telemetri historis dari database ke file output.

```powershell
python -m packages.core.cli telemetry export <format>
```

**Supported Formats:**

| Format | File Output | Description |
|:---|:---|:---|
| `csv` | `reports/export/telemetry.csv` | Flat comma-separated values |
| `json` | `reports/export/telemetry.json` | Structured JSON array |
| `md` | `reports/export/telemetry.md` | Markdown table format |
| `html` | `reports/export/telemetry.html` | Styled HTML report |

**Example:**
```powershell
python -m packages.core.cli telemetry export json
```

---

### `telemetry clean`

Menghapus seluruh rekaman data telemetri historis dari database SQLite. Operasi ini **tidak dapat di-undo**.

```powershell
python -m packages.core.cli telemetry clean
```

**Confirmation Prompt:**
```text
Warning: This will permanently delete all telemetry history.
Type 'yes' to confirm: yes
✅ Telemetry database cleared successfully.
```

---

### `help`

Menampilkan daftar semua perintah CLI yang tersedia beserta panduan sintaks konfigurasi.

```powershell
python -m packages.core.cli help
```

---

## Advanced: Automated Diagnostics

CLI dapat diintegrasikan dalam script otomasi atau task scheduler Windows:

```powershell
# Contoh: Export harian ke JSON via Task Scheduler
$env:PYTHONPATH="C:\path\to\aegis-core"
python -m packages.core.cli telemetry export json
```

---

## Further Reading

- [Developer Guide](developer-guide.md) — Setup PYTHONPATH dan virtual environment
- [Architecture](architecture.md) — Cara kerja internal platform
