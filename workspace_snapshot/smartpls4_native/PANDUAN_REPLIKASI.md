# Replikasi KidSense langsung di SmartPLS 4

Status: BELUM DIJALANKAN DI SMARTPLS. Paket ini berisi data, spesifikasi model dan pembanding Python; tidak berisi hasil native maupun berkas project SmartPLS yang direkayasa.

## Prasyarat yang belum terpenuhi

SmartPLS 4 belum ditemukan dalam lingkungan cloud. Pengguna menyatakan belum mempunyai aplikasi/lisensi atau trial aktif. Permintaan ke https://www.smartpls.com/downloads/ menghasilkan kegagalan CONNECT proxy HTTP 403. Tidak ada alat kendali desktop yang tersedia dalam sesi agen ini. Dukungan OS dan distribusi aplikasi belum diverifikasi melalui situs resmi.

Draf konfigurasi jaringan telah ditambah `smartpls.com` dan `www.smartpls.com`, mempertahankan preset package_managers. Status penyimpanan: saved; requires_publish=true. Tinjau dan simpan di pengaturan lingkungan, lalu publish agar konfigurasi tersebut dapat digunakan. Draf ini tidak memasang aplikasi, tidak mengaktifkan lisensi, tidak membuktikan kompatibilitas OS dan belum mengubah jaringan mesin saat ini. Domain tambahan untuk unduhan/aktivasi hanya dapat ditentukan dari petunjuk resmi atau respons aktual berikutnya.

Pemasangan resmi di komputer yang didukung vendor serta aktivasi lisensi/trial yang mendukung 271 observasi diperlukan untuk pelaksanaan lokal. Periksa dukungan platform, kapasitas, dan persyaratan lisensi pada situs resmi. Tidak ada pendaftaran akun, pembelian, atau aktivasi yang dilakukan oleh agen.

## Input dan diagram

Impor `KidSense_SmartPLS4_Input_271.csv` tanpa perubahan. Harus terbaca 271 baris dan 20 kolom numerik, semua nilai integer 1–5, tanpa missing. SHA256 byte file:

`ab7e5333f80e50f89dcf90d885556f5b60bb30848052153e77325500af216624`

Buat lima konstruk reflektif, masing-masing empat indikator:

| Konstruk | Indikator |
|---|---|
| AIR | AIR1, AIR2, AIR3, AIR4 |
| EXP | EXP1, EXP2, EXP3, EXP4 |
| PP | PP1, PP2, PP3, PP4 |
| TR | TR1, TR2, TR3, TR4 |
| AD | AD1, AD2, AD3, AD4 |

Hubungan struktural: AIR→TR; EXP→TR; PP→TR; TR→AD. Hubungan pengukuran reflektif mengarah dari konstruk menuju indikatornya. Pertahankan semua 20 indikator tanpa penghapusan, reverse coding, atau penyaringan baru pada model utama. Tidak ada jalur langsung AIR/EXP/PP→AD dalam model pembanding.

## Pengaturan pelaksanaan

Nama menu dapat berbeda menurut build SmartPLS. Pengaturan ini menurunkan spesifikasi dari workbook pengguna dan perhitungan pembanding; petunjuk versi terbaru vendor belum berhasil diakses.

1. **Catat provenance.** Versi/build SmartPLS, OS, waktu pelaksanaan, hash CSV dan n=271. Isi sheet Run_Record di `expected_reference.xlsx`.
2. **Jalankan PLS-SEM.** Pengukuran reflektif Mode A; path weighting; skor/estimasi terstandardisasi. Catat nilai pengaturan iterasi maksimum, stopping criterion, initial weights, dan penanganan data yang benar-benar tampil. Pembanding Python menggunakan toleransi bobot 1e-12; perbedaan toleransi/default harus dilaporkan saat membandingkan native.
3. **Ekspor estimasi utama.** Semua 20 outer loadings dan weights, alpha (catat definisi raw/standardized), rho_A, rho_C, AVE, HTMT, path coefficients, inner VIF, R², adjusted R², dan f². Python belum menyediakan rho_A sebagai pembanding; kolomnya sengaja kosong.
4. **Bootstrap jalur dan indirect.** 10.000 subsamples, confidence level 95%, two-tailed, interval percentile. Gunakan fixed seed (misalnya 20261106) dan catat nilai sebenarnya beserta opsi sign changes/hasil yang diminta. Simpan estimasi, bootstrap mean, SE/STDEV, t, p dan kedua batas CI. Ekspor CI R² bila tersedia.
5. **Bootstrap HTMT.** Buat hasil terpisah dengan 10.000 subsamples, one-tailed 5%, bias-corrected upper bound 95% jika opsi tersebut tersedia. Catat nama metode interval tepatnya: percentile, BC, dan BCa tidak boleh dipertukarkan. Jika build tidak menyediakan BC yang sama, tandai hasil sebagai metode berbeda. Kriteria penelitian yang ditetapkan adalah batas atas <0,90, bukan hanya estimasi titik <0,90. Ekspor juga CI percentile untuk pembandingan apabila tersedia.
6. **PLSpredict.** Gunakan 10 folds × 10 repetitions apabila didukung versi/lisensi; catat seed, opsi prediksi, standardisasi dan cara agregasi galat. Ekspor indikator Q²_predict, PLS RMSE/MAE, LM RMSE/MAE serta benchmark mean jika tersedia. Catat apakah AD menggunakan TR yang diamati atau prediksi TR. Pembanding Python menggunakan TR teramati, sehingga AD bersifat kondisional. Hasil PLSpredict dengan desain prediksi berbeda harus dilaporkan sebagai analisis berbeda.
7. **CVPAT, bila diperlukan dan tersedia.** Simpan keluaran native sebagai analisis tambahan. Tidak ada keluaran CVPAT dalam file Python sebelumnya.
8. **Simpan hasil asli.** Simpan project/model SmartPLS, laporan lengkap Excel/HTML yang disediakan aplikasi, serta pengaturan setiap run. Jangan mengganti label pembanding Python menjadi hasil SmartPLS.
9. **Isi perbandingan.** Dalam `expected_reference.xlsx`, isi kolom Native SmartPLS 4 value dan lokasi file/sel ekspor. Kolom native sekarang semuanya kosong. Nilai R² sekitar TR=0,616399 dan AD=0,473295 serta beta sekitar 0,260379; 0,293921; 0,315452; 0,687964 menjadi pemeriksaan kesetaraan model, bukan nilai yang harus dipaksakan.
10. **Evaluasi perbedaan.** Estimasi titik seharusnya dekat bila estimator, model, data dan standardisasi sepadan. Bootstrap tidak wajib identik: Python memakai empat stream seed 20261106–20261109 dengan 2.500 sampel per stream, sedangkan SmartPLS mungkin memakai RNG/resampling berbeda. Seed numerik sama tidak menjamin sampel sama. Selidiki perbedaan metodologis sebelum menilai suatu angka salah.

## Batas kesimpulan pembanding

- Nilai HTMT dan CI Python menunjukkan EXP–PP serta EXP–AD belum memenuhi batas atas BC95 satu sisi <0,90. Jangan menghapus indikator hanya agar ambang terlampaui.
- Python mengalahkan LM 5/8 indikator menurut RMSE dan 6/8 menurut MAE. Ini tidak membuktikan signifikansi prediktif; native CVPAT belum tersedia.
- CSV tidak memuat data mentah 323 respons, timestamp maupun flag A1/B1–B4/D1–D2. Penyaringan dan kelompok D1/D2 belum dapat dibuktikan.
- Dua JSON pengguna mencantumkan hash yang berbeda dari hash byte CSV; sumber hash lama belum diketahui.
- Hasil mendukung asosiasi dalam model. Kausalitas tidak ditetapkan oleh replikasi software.

Sesudah ekspor native tersedia, file itu dapat diperiksa terhadap workbook pembanding untuk menentukan kecocokan model, estimasi titik, inferensi, dan prediksi yang benar-benar sepadan.
