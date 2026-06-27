# Aegis Core Platform — Developer Setup Guide

Panduan onboarding bagi kontributor dan pengembang baru Aegis Core Platform. Dokumen ini menjelaskan tata cara penyiapan lingkungan kerja lokal, standarisasi pengujian, benchmarking, dan penjaminan kualitas kode.

---

## 🛠️ 1. Persiapan Lingkungan Kerja (Setup Environment)

### A. Clone Project
Clone repositori Aegis Core dari GitHub:
```bash
git clone https://github.com/Voonaa/aegis-core.git
cd aegis-core
```

### B. Membuat Virtual Environment (Venv)
Buat virtual environment Python untuk mengisolasi dependensi proyek:
```bash
python -m venv .venv
```
Aktifkan virtual environment:
- **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`
- **Windows (CMD)**: `.venv\Scripts\activate.bat`
- **Linux/macOS**: `source .venv/bin/activate`

### C. Install Dependencies
Instal dependensi runtime dan pustaka developer pendukung:
```bash
# Dependensi aplikasi utama
pip install -r requirements.txt

# Perkakas pengujian, linter, dan analisis statis
pip install -r requirements-dev.txt
```

---

## 🧪 2. Pengujian & Kualitas Kode

### A. Menjalankan Pytest
Pastikan semua unit pengujian lulus sebelum mengirimkan Pull Request (PR):
```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -v
```

### B. Cakupan Kode (Code Coverage)
Untuk menghasilkan visualisasi cakupan pengujian unit (dalam format Terminal, XML, dan HTML):
```powershell
$env:PYTHONPATH="."
python -m pytest tests/ --cov=packages --cov-report=term --cov-report=xml --cov-report=html
```
- Berkas `coverage.xml` digunakan oleh sistem CI/CD.
- Direktori `htmlcov/` berisi laporan interaktif HTML. Anda dapat membukanya via browser di `htmlcov/index.html`.

### C. Linter & Static Type Analysis
Aegis menggunakan `ruff` dan `mypy` untuk verifikasi struktur syntax dan type-safety:
```powershell
# Jalankan pengecekan ruff linter
ruff check packages/ apps/

# Jalankan pengecekan tipe data statis
mypy packages/ --ignore-missing-imports
```
Anda juga dapat menggunakan helper script lokal:
```powershell
./scripts/lint.ps1
```

---

## ⚡ 3. Pengukuran Performa (Benchmarking)

Naskah benchmark otomatis dapat dijalankan secara lokal untuk memverifikasi footprint memori dan latency bootstrap:
```bash
python scripts/benchmark.py
```
- Output eksekusi akan disimpan ke `reports/benchmark.json` dan `reports/benchmark.md`.
- Riwayat jangka panjang disimpan di `reports/history/`.

Untuk membandingkan performa run saat ini dengan pengujian historis sebelumnya:
```bash
python scripts/benchmark.py compare
```

---

## 📦 4. Release & Packaging

Untuk membuat paket rilis Aegis portable (`.zip` / `.exe` build sequence):
```powershell
./scripts/release.ps1
```
Naskah ini akan memverifikasi integritas, membuat metadata, dan membungkus aplikasi ke dalam direktori `release/`.

---

## 🔀 5. Git Flow & Review Policy

Kami menerapkan kebijakan alur kerja Git yang ketat untuk menjaga keandalan branch utama:

```
[develop] (Fitur & Hardening) ──> PR Review (TL approval) ──> Merge ke [main] (Rilis Resmi)
```

1. **Coding & Verification**: Lakukan coding di branch `develop`.
2. **Review Gate**: Pastikan pytest, lint, dan benchmark berjalan tanpa eror.
3. **TL Approval**: Berhenti dan tunggu verifikasi Technical Lead. **Dilarang keras melakukan commit atau memodifikasi CHANGELOG.md/PROJECT_MEMORY.md sebelum mendapat persetujuan.**
4. **Post-Approval**: Setelah status disetujui (Approved), perbarui CHANGELOG.md, lakukan `git commit`, dan lakukan `git push origin develop`.
