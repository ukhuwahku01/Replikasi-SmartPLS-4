# KidSense: paket pembuktian perhitungan

Baca `output/KidSense_Laporan_Pembuktian.md` dan `output/KidSense_Pembuktian_Hasil.xlsx`.
Semua unggahan asli ada di direktori `attachments` satu tingkat di atas `validation`.
Lima file asli dipertahankan byte per byte. Skrip hanya menulis hasil pembuktian terpisah.

Jalankan dari direktori `validation` dengan Python 3.12:

```bash
python3 -m pip install -r requirements-reproduction.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run_all.py
```

Dependensi tercatat sesuai versi pada mesin pembuktian. `run_all.py` tidak menginstal
paket, tidak mengakses jaringan, dan tidak menjalankan SmartPLS. Empat proses lokal
menghitung bootstrap PLS masing-masing 2.500 resampling; bootstrap HTMT 10.000 dijalankan
terpisah. Hasil eksploratori CV memakai sepuluh repetisi sepuluh fold.

Bukti utama: 199 perbandingan skalar cocok dengan toleransi absolut 1e-8. Periksa
`Pembandingan_angka` dan `Batasan` di Excel. Dua pasangan HTMT belum memenuhi
batas atas BC95 satu sisi <0,90. Hash yang dinyatakan pada JSON tidak sama dengan
hash CSV. Data mentah 323 respons/flag D1-D2 tidak tersedia, sehingga penyaringan
dan dua skenario sensitivitas terkait tidak dapat dibuktikan dari paket ini.
