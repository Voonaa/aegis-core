# Aegis Core Platform — FAQ

> Pertanyaan umum seputar instalasi, penggunaan, dan pengembangan Aegis Core Platform.

---

## Installation & Setup

### Q: Sistem operasi apa yang didukung?

Aegis dirancang khusus untuk **Windows 10 dan Windows 11**. Platform menggunakan WMI (Windows Management Instrumentation) dan WinReg yang merupakan API eksklusif Windows.

Menggunakan Aegis di Linux atau macOS **tidak didukung**.

---

### Q: Versi Python apa yang kompatibel?

Aegis diuji di:
- Python **3.11** ✅
- Python **3.12** ✅
- Python **3.14** ✅ (experimental)

Python 3.10 ke bawah **tidak didukung** karena menggunakan syntax terbaru (`match/case`, type hints modern).

---

### Q: Kenapa terjadi `ModuleNotFoundError` saat menjalankan aplikasi?

```text
ModuleNotFoundError: No module named 'packages'
```

**Solusi**: Set `PYTHONPATH` ke root directory proyek sebelum menjalankan:

```powershell
$env:PYTHONPATH = "."
python apps/desktop/main.py
```

Ini diperlukan karena Aegis menggunakan monorepo layout di mana modul berada di `packages/`, bukan di root.

---

### Q: Kenapa aplikasi harus dijalankan sebagai Administrator?

Beberapa query hardware membutuhkan elevated privilege:
- **WMI queries** untuk thermal zone (CPU temperature) memerlukan admin access
- **SFC dan DISM** repair jobs memerlukan admin access

Untuk fitur penuh, jalankan terminal atau IDE sebagai **Run as Administrator**.

---

## Usage

### Q: Apa perbedaan antara Portable dan Installer?

| Aspek | Portable | Installer (Setup) |
|:---|:---|:---|
| Instalasi | Tidak perlu | Perlu dijalankan sekali |
| Registry | Tidak mengubah | Membuat uninstall entry |
| Lokasi | Di mana saja | `Program Files\Aegis` |
| Cocok untuk | USB drive, testing | Penggunaan jangka panjang |

Download keduanya dari [GitHub Releases](https://github.com/Voonaa/aegis-core/releases).

---

### Q: Bagaimana cara memperbarui Aegis?

Aegis belum memiliki auto-updater. Untuk memperbarui:
1. Kunjungi halaman [GitHub Releases](https://github.com/Voonaa/aegis-core/releases)
2. Unduh versi terbaru
3. Gantikan folder portable lama, atau jalankan installer baru

---

### Q: Apa itu Health Score?

**Health Score** adalah nilai 0–100 yang merepresentasikan kondisi sistem secara keseluruhan, dihitung dari:

| Komponen | Bobot |
|:---|:---:|
| CPU temperature & load | 25% |
| RAM usage | 20% |
| Disk health (SMART) | 25% |
| Battery health | 15% |
| GPU load | 15% |

Skor di atas **80** = Excellent. Di bawah **50** = perlu perhatian.

---

### Q: Di mana data telemetri disimpan?

Data historis disimpan dalam database SQLite lokal:

```text
apps/desktop/config/telemetry.db
```

Database ini hanya tersimpan di mesin lokal dan tidak dikirimkan ke server manapun.

---

## Development

### Q: Bagaimana cara menulis plugin untuk Aegis?

Baca panduan lengkap di [Plugin System](plugins.md).

---

### Q: Bagaimana cara menggunakan Aegis SDK dari kode eksternal?

Baca panduan lengkap di [SDK Reference](sdk.md).

---

### Q: Apakah Aegis mendukung mock WMI di tests?

Ya. Test suite menggunakan `unittest.mock.patch` untuk mengisolasi WMI calls sehingga tests dapat berjalan tanpa admin privilege atau hardware fisik.

---

### Q: Bagaimana cara melaporkan bug atau security issue?

- **Bug**: Buka [GitHub Issue](https://github.com/Voonaa/aegis-core/issues) menggunakan template `bug_report.md`
- **Security**: Lihat [SECURITY.md](../SECURITY.md) untuk prosedur private disclosure

---

## Further Reading

- [Developer Guide](developer-guide.md) — Setup lengkap environment development
- [Architecture](architecture.md) — Desain teknis internal platform
- [Release Guide](release-guide.md) — Cara build dan publish rilis
