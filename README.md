# Backup replikasi KidSense — SmartPLS 4

Backup berkas penelitian dan proses verifikasi yang dikerjakan dalam sesi ini, disiapkan pada **9 November 2026 (Asia/Jakarta)**. Paket memuat **188 berkas (18.234.550 byte)**, termasuk **12 unggahan asli**, data, ekspor native SmartPLS, hasil Python, skrip, sampel bootstrap, laporan, draf Word/PDF, gambar, pratinjau pemeriksaan, dan arsip historis.

Semua sumber dipertahankan **byte per byte**. Dua berkas cache Python `.pyc` tidak disertakan. Tidak ada direktori autentikasi, konfigurasi cloud, atau metadata Git mesin yang dimasukkan ke snapshot.

## Mulai dari hasil terbaru

- [Verifikasi bootstrap native M1 yang benar](workspace_snapshot/validation/native_M1_corrected/output/KidSense_M1_Native_Terverifikasi.xlsx)
- [Penjelasan hasil dan batas interpretasi M1](workspace_snapshot/validation/native_M1_corrected/output/KidSense_M1_Native_Hasil_Verifikasi.md)
- [Draf Word terklarifikasi, memakai hasil native M1](workspace_snapshot/validation/construct_review/output/KidSense_Draf_Terklarifikasi_dan_M1.docx)
- [Draf PDF](workspace_snapshot/validation/construct_review/output/KidSense_Draf_Terklarifikasi_dan_M1.pdf)
- [Tinjauan konstruk, item asli, dan perbandingan model](workspace_snapshot/validation/construct_review/output/KidSense_Tinjauan_Konstruk_dan_M1.xlsx)
- [Indeks laporan dan riwayat tahap analisis](REPORTS_INDEX.md)
- [Daftar 12 unggahan asli](ORIGINAL_UPLOADS.md)

## Status analisis yang perlu dipertahankan

**M0** adalah model awal AIR/EXP/PP → TR → AD. **M1** menambahkan AIR/EXP/PP → AD sebagai analisis sensitivitas posthoc; M0 tidak diganti secara otomatis. Bootstrap native M1 lengkap sudah diverifikasi: lima konstruk, tujuh jalur, 20 indikator, dan 271 observasi. Estimasi titik cocok dengan Python; interval bootstrap berasal dari native dan tidak dipaksa identik antarimplementasi.

Pada M1, AIR → AD langsung belum signifikan (p = 0,505143). EXP → AD, PP → AD, dan TR → AD memiliki CI percentile dua sisi 95% yang tidak memuat nol. Ketiga asosiasi tidak langsung melalui TR juga memiliki CI yang tidak memuat nol. Hasil ini tidak membuktikan kausalitas, dan bagian kovarians struktural skor M1 tersaturasi.

Batas atas HTMT BCa satu sisi untuk **EXP–PP (0,908139)** dan **EXP–AD (0,912789)** belum memenuhi kriteria < 0,90. Penambahan jalur tidak memperbaiki HTMT pada data dan pengelompokan item yang sama. Fit mixed dan composite tetap dibedakan dalam laporan.

**Hasil PLSpredict/CVPAT yang tersedia adalah untuk M0**, dengan Direct antecedents, 10 folds × 10 repetitions. Keunggulan keseluruhan atas regresi linear belum signifikan (p = 0,122338). Prediksi native M1 belum diserahkan. Jangan memindahkan hasil prediksi M0 ke M1.

Responden hanya menilai **deskripsi/gambar rancangan KidSense**. Konstruk mencakup persepsi dan niat adopsi hipotetis yang bersyarat, bukan penggunaan, akurasi AI, keamanan, atau adopsi aktual. Bukti seleksi respons awal 323 → 271 belum tersedia dalam data indikator ini.

## Struktur backup

```text
workspace_snapshot/
  attachments/          # seluruh unggahan, struktur UUID asli dipertahankan
  validation/           # seluruh tahap perhitungan, audit, dan hasil olahan
  smartpls4_native/     # input dan paket awal persiapan SmartPLS
BACKUP_MANIFEST.json    # path, ukuran, SHA-256 setiap berkas snapshot
SHA256SUMS              # daftar checksum lengkap
ORIGINAL_UPLOADS.md     # indeks unggahan asli
REPORTS_INDEX.md        # hasil terbaru dan penanda riwayat
 tools/                # utilitas snapshot dan pemeriksaan hash
```

Berkas berlabel “Final” pada tahap lama adalah final **untuk tahap tersebut**, bukan otomatis status M1 terbaru. Laporan lama yang menyatakan bootstrap M1 belum tersedia atau menunjukkan model tanpa TR disimpan sebagai riwayat audit. Gunakan indeks hasil terbaru di atas untuk status saat backup.

## Memeriksa dan memulihkan backup

Dari root repositori, jalankan:

```bash
python3 tools/verify_backup.py
```

Pemeriksaan memakai pustaka standar Python dan memverifikasi keberadaan, ukuran, dan SHA-256 seluruh 188 berkas. Pada mesin sumber, pemeriksaan tambahan dapat dilakukan dengan:

```bash
python3 tools/verify_backup.py --source-workspace /workspace
```

Unduh repositori melalui **Code → Download ZIP**, atau clone melalui Git, lalu pertahankan struktur direktori. Skrip analisis historis menggunakan path `/workspace/attachments`, `/workspace/validation`, dan `/workspace/smartpls4_native`; untuk menjalankannya di mesin lain, sesuaikan path atau pulihkan tiga direktori snapshot ke workspace yang sesuai. Tidak ada proses SmartPLS, lisensi, atau project native yang belum diunggah yang diasumsikan ikut tersimpan.

Jangan menjalankan skrip pembentuk snapshot untuk mengubah backup historis tanpa menyimpan versi sebelumnya. `make_snapshot.py` menolak menimpa berkas snapshot yang isinya sudah berbeda.
