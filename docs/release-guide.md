# Aegis Core Platform — Release Guide

> Panduan lengkap untuk membangun, mengemas, dan mempublikasikan rilis Aegis.

---

## Overview

Aegis menggunakan **automated release pipeline** berbasis PowerShell (`scripts/release.ps1`) yang diintegrasikan dengan **GitHub Actions** (`release.yml`) untuk menghasilkan distribusi biner yang reproducible.

---

## Release Outputs

| Output | Path | Description |
|:---|:---|:---|
| Portable directory | `reports/release/aegis_v{VERSION}_portable/` | Folder siap-pakai tanpa installer |
| ZIP archive | `reports/release/aegis_v{VERSION}_portable.zip` | Versi terkompresi dari portable |
| Windows Installer | `installer/Output/AegisSetup.exe` | Setup installer via Inno Setup |
| Checksum manifest | `reports/release/SHA256SUMS.txt` | SHA256 hash semua artifact |

---

## 1. Local Release Build

### Prerequisites

- Python virtual environment aktif dengan semua dependencies terinstall
- (Opsional) **Inno Setup Compiler** (`ISCC.exe`) di PATH untuk build installer

### Step 1: Jalankan Release Script

```powershell
.\\scripts\\release.ps1
```

Script ini secara otomatis:
1. ✅ Membaca versi dari `version.txt` (Single Source of Truth)
2. ✅ Menjalankan `ruff check` dan `mypy` (code compliance)
3. ✅ Menjalankan `pytest tests/` (unit test suite harus 100% pass)
4. ✅ Mengompilasi build metadata JSON (`build_metadata.json`):
   - Version string
   - Git commit hash
   - Python version
   - Build timestamp
5. ✅ Mengemas portable directory
6. ✅ Mengompresi ke `.zip` via `Compress-Archive`
7. ✅ Menghitung SHA256 checksum seluruh artifact → `SHA256SUMS.txt`
8. ✅ (Jika `ISCC.exe` terdeteksi) Mengompilasi `installer/aegis_setup.iss` → `AegisSetup.exe`

### Inno Setup (Opsional)

Jika Inno Setup Compiler **tidak tersedia**, script melanjutkan dengan warning (bukan error):

```text
⚠ Warning: ISCC.exe not found. Skipping installer build.
   Install Inno Setup from: https://jrsoftware.org/isdl.php
```

---

## 2. GitHub Actions Automated Release

### Trigger

Workflow `release.yml` dipicu secara otomatis saat tag `v*` di-push ke remote:

```powershell
# Buat annotated tag
git tag -a v1.0.1 -m "Release v1.0.1"

# Push tag ke GitHub
git push origin v1.0.1
```

### Workflow Steps

```text
On push: tag matching "v*"
      │
      ▼
1. Checkout code
      │
      ▼
2. Setup Python 3.12
      │
      ▼
3. Install dependencies
      │
      ▼
4. Install ISCC via fleskesvor/setup-iscc@v1
      │
      ▼
5. Run: scripts/release.ps1
      │
      ▼
6. Upload artifacts to GitHub Release (draft):
   ├── aegis_v*.zip
   ├── AegisSetup.exe
   └── SHA256SUMS.txt
```

### Publish the Release

Setelah workflow selesai:
1. Buka GitHub → **Releases**
2. Edit draft release yang dibuat otomatis
3. Tambahkan release notes dari `CHANGELOG.md`
4. Klik **Publish Release**

---

## 3. Versioning Policy

Aegis menggunakan **Semantic Versioning** (`MAJOR.MINOR.PATCH`):

| Increment | When |
|:---|:---|
| `MAJOR` | Breaking API changes |
| `MINOR` | New features (backward compatible) |
| `PATCH` | Bug fixes only |

**Single Source of Truth**: versi hanya diubah di `version.txt` di root repository. Script release, GitHub Actions, dan display versi di UI semuanya membaca dari file ini.

```text
version.txt
    │
    ├── release.ps1           (portable dir name, metadata)
    ├── release.yml           (GitHub Release tag)
    └── apps/desktop/app.py   (UI titlebar display)
```

---

## 4. Checksum Verification

Setelah mengunduh rilis, verifikasi checksum:

```powershell
# Verify a specific file
Get-FileHash aegis_v1.0.0_portable.zip -Algorithm SHA256
# Compare output with SHA256SUMS.txt
```

---

## Further Reading

- [Developer Guide](developer-guide.md) — Local development setup
- [Architecture](architecture.md) — System internals
- [Roadmap](roadmap.md) — Planned releases
