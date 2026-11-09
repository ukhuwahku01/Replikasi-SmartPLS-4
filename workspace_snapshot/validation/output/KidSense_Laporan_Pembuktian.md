# Pembuktian hasil KidSense

**Status: dapat digunakan dengan catatan (Share with caveats). Cakupan: parsial.**

Dihitung ulang pada 6 November 2026 WIB dari kelima file unggahan. Seluruh hasil numerik utama yang dapat dihitung dari CSV berhasil direplikasi. Lima berkas asli tidak diubah; workbook pembuktian ini dibuat terpisah. Bukti seleksi respons awal dan keluaran native SmartPLS tidak tersedia.

## Hasil yang terbukti dari CSV

CSV berisi **271 × 20** nilai integer 1–5, tanpa nilai kosong. Ada 10 baris jawaban seragam dan 7 pengulangan pola jawaban penuh. Pola identik tidak membuktikan responden ganda; tidak ada identitas atau timestamp dalam CSV.

| Jalur | Beta ulang | CI95 bootstrap dilaporkan dan direplikasi | p dua sisi aproksimasi normal |
|---|---:|---:|---:|
| AIR -> TR | 0.260379 | [0.137435; 0.383139] | 3.34e-05 |
| EXP -> TR | 0.293921 | [0.156871; 0.426766] | 1.83e-05 |
| PP -> TR | 0.315452 | [0.166742; 0.464030] | 3.54e-05 |
| TR -> AD | 0.687964 | [0.604991; 0.761237] | 3.01e-65 |

R² TR = **0,616399** dan AD = **0,473295**. Tiga asosiasi tidak langsung = **0,179132; 0,202207; 0,217019** dan interval bootstrap masing-masing tidak memuat nol. Hasil ini mendukung asosiasi dalam model, bukan hubungan sebab-akibat.

Lima konstruk: alpha standardized **0,840120–0,879011**, rho_C **0,892680–0,916747**, AVE **0,675347–0,733542**, loading **0,801232–0,859317**. Angka alpha workbook adalah versi standardized; versi raw juga disediakan agar definisinya jelas.

**HTMT:** semua 10 estimasi titik di bawah 0,90. Namun batas atas BC satu sisi 95% untuk **EXP–PP = 0,909878** dan **EXP–AD = 0,913699** tidak di bawah 0,90. Maka validitas diskriminan seluruh pasangan belum terbukti menurut kriteria yang ditetapkan file. Hanya EXP–PP memiliki estimasi titik di atas 0,85. Ambang titik dan ambang interval bukan pemeriksaan yang sama; tabel dua sisi juga tidak boleh dipertukarkan dengan satu sisi.

**Prediksi eksploratori:** 8/8 Q² analogue positif (**0,294313–0,473052**). PLS mengungguli LM pada **5/8 indikator menurut RMSE**, atau **6/8 menurut MAE**. AD memakai indikator TR yang diamati di data uji: hasilnya kondisional, bukan prediksi AD hanya dari AIR/EXP/PP. Ini bukan SmartPLS PLSpredict/CVPAT; selisih galat tidak menyatakan signifikansi statistik.

**Sensitivitas:** model n=271 dan model n=261 setelah membuang 10 jawaban seragam masing-masing cocok dengan angka skenario yang dilaporkan. Angka HTMT sensitivitas kedua kelompok cocok pada empat desimal. Kelompok D1/D2 n=228 dan irisan n=220 belum dapat diuji karena flag/keanggotaan baris tidak diberikan.

## Cakupan audit

Rasio berikut adalah jumlah unit dengan masalah tersisa dibanding inventaris yang disebutkan, bukan persentase keakuratan. Nol masalah teramati tidak membuktikan unit yang tidak terverifikasi. Data mentah tidak tersedia; ini membatasi kelengkapan audit.

### Kualitas dan kelengkapan artefak

| Kategori | Masalah teramati | Penilaian |
|---|---:|---|
| Kelengkapan paket unggahan | 0 / 5 file | Kelima file terbaca; asal dan penyaringan responden tidak dapat diuji penuh. |
| Kejelasan tabel reliabilitas | 1 / 1 tabel | Label alpha tidak menyebut standardized. Workbook pembuktian membedakan alpha standardized/raw. |
| Visual dan interaksi dashboard | N/A | Tidak ada dashboard yang ditinjau. |

### Ketepatan dan ketahanan analitis

| Kategori | Masalah teramati | Penilaian |
|---|---:|---|
| Identitas sumber CSV | 2 / 2 deklarasi hash | Hash pada HTMT JSON dan CV JSON berbeda dari byte CSV unggahan. |
| Perhitungan angka | 0 / 199 perbandingan skalar | Semua angka yang dibandingkan independen cocok dalam toleransi absolut 1e-8. Ini tidak meliputi klaim penyaringan yang tidak memiliki input. |
| Keselarasan grafik | N/A | Tidak ada grafik dalam artefak sumber. |
| Kelengkapan data untuk penyaringan | 0 / 4 skenario terbukti salah | Dua skenario direplikasi; dua skenario D1/D2 belum dapat diverifikasi, bukan dianggap lolos. |
| Konsistensi lintas berkas | 0 / 4 bagian bersama | HTMT, Structural, Indirect dan Exploratory CV workbook konsisten dengan JSON; hash sumber dinilai terpisah. |
| Kontrol kualitas input | 0 / 3 pemeriksaan | Dimensi 271×20, tanpa missing, integer 1–5 terkonfirmasi. |
| Dukungan kesimpulan numerik | 0 / 3 keluarga hasil | Hasil PLS, HTMT dan CV cocok dengan kualifikasi pada workbook; tidak menjustifikasi klaim seluruh diskriminan lolos, kausalitas atau native SmartPLS. |

## Masalah prioritas dan penanganan

1. **Identitas hash sumber belum cocok.** CSV aktual SHA256 `ab7e5333f80e50f89dcf90d885556f5b60bb30848052153e77325500af216624`; HTMT/CV JSON mencantumkan `5c517d0bcc99f0ce5e909af11da5a4fca1f0c23bb8c4e9060f7cf620def83fcc`. **Usulan:** pisahkan hash file mentah dan CSV analisis dengan nama file masing-masing. Kecocokan perhitungan membuktikan angka dapat diperoleh dari CSV; bukan pembuktian rantai asal data.
2. **Bukti penyaringan belum tersedia.** Klaim 323 respons, 52 eksklusi, consent/inclusion B1–B4, D1/D2 dan timestamp belum dapat diperiksa. **Perlu input:** data mentah dan pemetaan ke 271 baris. Tidak ada hasil yang diada-adakan untuk kelompok yang tidak tersedia.
3. **Batasan validitas dan metode harus dipertahankan.** Dua pasangan HTMT belum memenuhi uji batas 0,90, prediksi AD kondisional, dan file menyatakan Python. **Ditangani:** seluruh catatan tersebut dibawa ke workbook pembuktian. Tidak ada angka sumber diubah untuk membuat hasil tampak lolos.
4. **Definisi alpha perlu diperjelas.** **Ditangani dalam salinan pembuktian:** alpha standardized dan raw ditampilkan terpisah. Berkas asli tidak disentuh.

## Jejak perhitungan yang dapat diulang

- PLS-PM Mode A reflektif, path weighting, lima blok masing-masing empat indikator, jalur AIR/EXP/PP→TR dan TR→AD. Skor dinormalisasi; konvergensi perubahan maksimum bobot <1e-12.
- PLS bootstrap: 10.000 resampling baris, empat stream NumPy default_rng dengan seed 20261106–20261109, masing-masing 2.500. SE memakai ddof=1; CI percentile 2,5%/97,5%. t=|beta|/SE; p=2×normal.sf(t), bukan p empiris bootstrap.
- HTMT+: rerata korelasi Pearson absolut lintas blok dibagi akar hasil kali rerata korelasi absolut dalam blok. Bootstrap 10.000, seed 20261105; interval percentile dan BC, bukan BCa.
- CV: KFold 10 fold acak, seed 20261105+repetisi, sepuluh repetisi; normalisasi/fitting hanya training. Galat digabung pada satuan item asli. LM memakai 12 indikator AIR/EXP/PP untuk TR dan empat indikator TR teramati untuk AD. Q² analogue=1−RMSE_PLS²/RMSE_mean².

Selisih maksimum PLS titik/reliabilitas <6e-13; bootstrap PLS <5e-11; HTMT beserta 50 batas interval **0,0**; PLS CV RMSE <5e-14. Selisih sangat kecil pada PLS berasal dari numerik/konvergensi, tidak mengubah angka yang dilaporkan atau kesimpulan.

Versi perangkat lunak dan hash semua file ada di `manifest.json`; data sumber, skrip, hasil pembanding dan sampel bootstrap ada dalam paket ZIP. Lembar `Pembandingan_angka` menampilkan nilai dilaporkan, hitung ulang, selisih, toleransi dan status per angka. Lembar ringkasan menegaskan bagian yang belum terverifikasi.
