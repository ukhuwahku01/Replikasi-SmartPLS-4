# Audit kesesuaian tiga ekspor M1

**Status: butuh ekspor bootstrap ulang.** Estimasi titik M1 lengkap berhasil diverifikasi; inferensi bootstrap M1 lengkap belum tersedia. Berkas sumber dipertahankan utuh.

Identitas dibaca dari metadata dan matriks model, bukan nama berkas.

| File | Model dalam laporan | Konstruk | Indikator | Jalur | Sesuai M1 lengkap? |
|---|---|---:|---:|---:|---|
| KidSense_M1_Eksploratori.xlsx | Report (KidSense_M1_Eksploratori) | 5 | 20 | 7 | Ya |
| KidSense_M1_Algorithm.xlsx | Report (pls-sem) | 4 | 16 | 3 | Tidak: tanpa TR |
| KidSense_M1_Bootstrap_10000.xlsx | Report (pls-sem) | 4 | 16 | 3 | Tidak: tanpa TR |

## Hasil yang sudah terbukti

**KidSense_M1_Eksploratori.xlsx** memuat lima konstruk, 20 indikator, dan 7 jalur yang ditetapkan. Data 271 × 20 cocok persis dengan CSV. Tujuh beta,20 loadings, dua R², dan tiga specific indirect (32 perbandingan) cocok dengan Python M1; selisih maksimum **1,00411×10⁻¹⁰**.

| Jalur | Beta native M1 |
|---|---:|
| AIR -> AD | 0.045605 |
| AIR -> TR | 0.262996 |
| EXP -> AD | 0.337191 |
| EXP -> TR | 0.292923 |
| PP -> AD | 0.156463 |
| PP -> TR | 0.313463 |
| TR -> AD | 0.304012 |

R² AD = **0.575904** dan R² TR = **0.615656**. Tiga estimasi indirect melalui TR juga cocok. Ini membuktikan estimasi titik M1 tersedia native; tidak menyediakan interval bootstrap native bagi M1.

## Mengapa dua file lain tidak dapat digabungkan

**KidSense_M1_Algorithm.xlsx** dan **KidSense_M1_Bootstrap_10000.xlsx** mencatat model bernama **Report (pls-sem)**. Keduanya memuat AIR, EXP, PP, AD, dengan tiga jalur AIR/EXP/PP→AD; tidak ada TR maupun TR1–TR4 dalam model. Data yang diekspor adalah 271 × 16 nilai yang cocok dengan subset CSV, bukan data yang nilainya berubah.

Dua puluh estimasi asli pada algorithm dan bootstrap model empat konstruk cocok persis satu sama lain. Jadi masalah utamanya adalah **model yang berbeda**, bukan fluktuasi bootstrap. R² AD model tanpa TR=0,540860; nilai ini bukan R² M1 lengkap yang 0,575904.

Bootstrap model empat konstruk memang menyelesaikan 10.000 sampel dengan Complete, Percentile, Two-tailed, α = 0,05, Fixed seed. Tidak ada efek tidak langsung karena tidak ada rantai mediasi; mengubah Amount of results tidak akan memunculkan efek melalui TR pada model tersebut.

Misalnya, AIR→AD β 0,128194 dan p = 0,042186 pada file bootstrap adalah hasil model tanpa TR. Angka itu tidak dapat dipasangkan dengan beta M1 AIR→AD 0,045605 atau dipakai untuk menyatakan AIR signifikan setelah mengontrol TR. Interval Python M1 sebelumnya tetap berlabel Python; tidak ditempel sebagai interval native.

## Langkah koreksi

1. Kembali ke Workspace, lalu buka **KidSense_M1_Eksploratori** yang memuat **AIR, EXP, PP, TR, AD**.
2. Pastikan **20 indikator**,termasuk TR1–TR4,dan **7 jalur** ada: AIR/EXP/PP→TR;TR→AD;AIR/EXP/PP→AD.
3. Dari model aktif ini jalankan **Calculate→Bootstrapping**, dengan **10.000,Complete,Percentile,Two-tailed,α0,05,Fixedseed**.
4. Ekspor sebagai **KidSense_M1_DenganTR_Bootstrap_10000.xlsx**, lalu unggah. File algoritma M1 lengkap yang sudah cocok tidak perlu diganti.

M0 tetap dipertahankan sebagai model awal. M1 tetap analisis sensitivitas posthoc; verifikasi angka tidak membuktikan model substantif atau menyelesaikan HTMT. Model empat konstruk dapat disimpan sebagai keluaran berbeda apabila memang diperlukan, tetapi tidak dilaporkan sebagai M1 yang memuat TR.

## Cakupan audit

- Ketiga metadata, matriks inner/outer, pengelompokan item, dan data asli diperiksa.
- M1 lengkap: 32 estimasi titik dibandingkan independen; seluruhnya cocok dalam 1e-8.
- Dua model empat konstruk: 20 estimasi asli cocok satu sama lain; t=|beta|/SE bootstrap juga konsisten secara aritmetika.
- Terdapat **1/1 bootstrap yang diserahkan tidak cocok dengan target M1**. Ini masalah kesesuaian keluaran, bukan klaim semua angka di file salah.
- Bootstrap native untuk M1 lengkap, beserta CI, p, dan SE untuk ketujuh jalur serta indirect, masih memerlukan ekspor yang sesuai.

Sumber sel dan SHA256 ketiga unggahan tercatat pada workbook serta JSON audit. Tidak ada perubahan pada sumber atau penggabungan statistik dari model berbeda.
