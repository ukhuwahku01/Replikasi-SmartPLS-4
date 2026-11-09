# Hasil akhir replikasi KidSense di SmartPLS 4

**Status: dapat digunakan dengan catatan (Share with caveats).** Replikasi numerik selesai untuk ekspor yang tersedia: estimasi PLS, bootstrap jalur, HTMT satu sisi, serta PLSpredict/CVPAT. Ini tidak berarti seluruh model telah memenuhi validitas diskriminan, fit global, atau keunggulan prediksi terhadap regresi linear. Semua unggahan asli dipertahankan utuh.

## Prediksi native

File mencatat **SmartPLS 4.1.2.1**, **Direct antecedents**, **10 folds × 10 repetitions**, dan **Fixed seed**. Angka seed tidak diekspor. Data analisis tetap 271 responden dan 20 indikator; seluruh 5.420 nilainya cocok dengan CSV.

| Indikator | Q²_predict | RMSE PLS | RMSE LM | PLS lebih rendah? |
|---|---:|---:|---:|---|
| TR1 | 0.429694 | 0.741261 | 0.747146 | Ya |
| TR2 | 0.393986 | 0.793983 | 0.809530 | Ya |
| TR3 | 0.395881 | 0.770705 | 0.764487 | Tidak |
| TR4 | 0.474015 | 0.725451 | 0.749010 | Ya |
| AD1 | 0.307984 | 0.818698 | 0.828709 | Ya |
| AD2 | 0.363914 | 0.794019 | 0.800830 | Ya |
| AD3 | 0.294689 | 0.819193 | 0.818321 | Tidak |
| AD4 | 0.310104 | 0.809679 | 0.806461 | Tidak |

Semua **8/8 Q²_predict positif**, dengan rentang **0,294689–0,474015**. PLS memiliki RMSE lebih rendah daripada LM pada **5/8 indikator**; TR3, AD3, dan AD4 tidak. Berdasarkan MAE, PLS lebih rendah pada **7/8 indikator**; hanya AD4 tidak. Hasil Python sebelumnya memberi 5/8 menurut RMSE dan 6/8 menurut MAE; keputusan MAE untuk AD3 berubah pada run native.

Prediksi AD bersifat **kondisional pada TR yang diamati**. Hasil ini tidak mengukur prediksi AD hanya dari AIR, EXP, dan PP. Analisis dengan *Early antecedents* merupakan skenario berbeda dan belum dijalankan.

## CVPAT: apakah keunggulan prediksi signifikan?

| Pembanding | Unit | Average loss difference | p native | Keputusan pada α = 0,05 |
|---|---|---:|---:|---|
| IA | AD | -0.308517 | 1.13381e-07 | PLS lebih baik signifikan |
| IA | TR | -0.421841 | 8.27072e-11 | PLS lebih baik signifikan |
| IA | Overall | -0.365179 | 3.92504e-10 | PLS lebih baik signifikan |
| LM | AD | -0.005181 | 0.456418 | Keunggulan belum signifikan |
| LM | TR | -0.014719 | 0.159017 | Keunggulan belum signifikan |
| LM | Overall | -0.009950 | 0.122338 | Keunggulan belum signifikan |

Selisih loss negatif berarti loss PLS lebih rendah. **PLS lebih baik secara signifikan daripada prediksi rata-rata indikator (IA), tetapi keunggulan keseluruhan terhadap regresi linear (LM) belum signifikan pada α = 0,05.**

Mean squared loss keseluruhan adalah **0,615942 untuk PLS** dan **0,625892 untuk LM**. Pengurangannya sekitar **1,59%**, dengan **p CVPAT = 0,122338**. Hasil ini tidak membuktikan PLS dan LM setara; bukti pada run ini belum cukup untuk menyatakan keunggulan PLS.

Pada tingkat indikator, AD1 dan TR4 memiliki p < 0,05 terhadap LM tanpa penyesuaian multipel. Pemeriksaan tambahan Holm untuk delapan perbandingan indikator LM hanya mempertahankan AD1. Hasil per indikator tidak menggantikan kesimpulan *Overall*. Nilai p native dan koreksi tambahan disajikan terpisah dalam workbook.

## Bukti perhitungan ulang

- **21.680 galat indikator** cocok persis dengan observasi CSV dikurangi prediksi ekspor. Ada **2.710 prediksi per indikator**, berasal dari 271 responden yang diuji sepuluh kali, bukan 2.710 responden independen.
- RMSE dan MAE yang dihitung ulang dari galat cocok dengan ringkasan native hingga selisih < **2 × 10⁻¹⁵**. Rumus Q²_predict cocok hingga < **1,2 × 10⁻¹⁶**.
- Indeks kasus yang diekspor memungkinkan rekonstruksi **100 fold**. Setiap repetisi terdiri dari satu fold berisi 28 kasus dan sembilan fold berisi 27 kasus. Model dihitung ulang pada data training dan test yang sama. Selisih maksimum prediksi PLS adalah **2,97 × 10⁻⁹**, dan RMSE PLS **5,46 × 10⁻¹¹**. RMSE IA dan LM cocok hingga < **4 × 10⁻¹⁵**.
- Perbedaan kecil terhadap JSON Python sebelumnya dapat diterangkan oleh pembagian fold: penggunaan fold native mereproduksi hasil native tanpa mengetahui angka seed.
- Loss dan statistik t pada **22 baris CVPAT** direkonstruksi dari galat PLS dan benchmark IA/LM independen; selisih maksimum **3,74 × 10⁻¹⁴**. Nilai p native tetap dipertahankan. Cek numerik dengan distribusi t dan df = 270 menghasilkan keputusan pada α = 0,05 yang sama; selisih angka p maksimum **3,44 × 10⁻⁸**.

Loss konstruk dalam CVPAT adalah rata-rata loss empat indikator, dan *Overall* adalah rata-rata delapan indikator. Angka tersebut berbeda dari kuadrat RMSE skor laten pada tabel PLSpredict LV. Rekonstruksi t native menggunakan `|mean(delta)| / sqrt(var_population(delta) / 271)` atas baris prediksi berulang. Skrip, galat, dan indeks fold disimpan sebagai bukti; rumus ini mereproduksi keluaran software, bukan menghilangkan keterbatasan rancangan penelitian.

## Kesimpulan seluruh replikasi

1. **Estimasi dan inferensi jalur berhasil direplikasi.** Sebanyak 62 estimasi titik lintas hasil struktural, pengukuran, dan HTMT cocok hingga selisih < 5 × 10⁻¹⁰. Empat jalur dan tiga asosiasi tidak langsung positif, dengan CI 95% dua sisi tidak memuat nol. R² TR = **0,616399** dan AD = **0,473295**. Ini mendukung asosiasi dalam model, bukan kausalitas atau mediasi kausal.
2. **Validitas diskriminan belum terpenuhi untuk seluruh pasangan.** Pada HTMT native BCa satu sisi, 8/10 pasangan memenuhi batas atas 95% < 0,90. **EXP–PP = 0,908139** dan **EXP–AD = 0,912789** belum memenuhi. Metode BC Python tanpa acceleration tetap dibedakan dari BCa native.
3. **Fit global masih memerlukan perhatian.** Pada estimated composite model, d_ULS = **0,862615** > HI95 **0,368764**, dan d_G = **0,190185** > HI95 **0,168519**; keduanya juga melewati HI99. SRMR = **0,064091** berada di bawah patokan deskriptif 0,08, tetapi di atas batas bootstrap HI95. Jangan menyatakan seluruh fit memadai hanya berdasarkan SRMR atau jalur yang signifikan.
4. **Keunggulan prediksi terhadap LM belum signifikan secara keseluruhan.** Keunggulan terhadap IA terdukung, sedangkan CVPAT Overall terhadap LM memberi p = **0,122338**.
5. **Asal dan penyaringan data tetap terbatas.** Kecocokan 271 baris analisis tidak membuktikan seleksi awal 323 → 271, consent, flag D1/D2, atau identitas hash data mentah yang tidak disediakan. Nilai rho_A native tersedia, tetapi belum direplikasi secara independen.

## Cakupan pemeriksaan

Rasio di bawah menyatakan unit dengan masalah perhitungan teramati dibanding inventaris yang disebutkan, bukan persentase validitas penelitian. Nol masalah teramati tidak menghapus keterbatasan metodologis.

### Kualitas dan kelengkapan artefak

| Kategori | Masalah teramati | Penilaian |
|---|---:|---|
| Kelengkapan run native yang diminta | 0 / 3 run | Bootstrap jalur, HTMT satu sisi, dan PLSpredict/CVPAT telah diperiksa. Bukti seleksi data mentah berada di luar cakupan. |
| Kejelasan kesimpulan | 0 / 3 keluarga hasil | Asosiasi, validitas diskriminan, dan prediksi diberi batas yang berbeda; tidak ada klaim seluruh model valid. |
| Visual dan interaksi dashboard | N/A | Tidak ada dashboard yang ditinjau. |

### Ketepatan dan ketahanan analitis

| Kategori | Masalah teramati | Penilaian |
|---|---:|---|
| Identitas data analisis | 0 / 1 dataset | Seluruh 5.420 nilai dan urutan baris cocok dengan CSV. |
| Estimasi titik | 0 / 62 nilai | Perbandingan struktural, pengukuran, dan HTMT selesai; rho_A tidak termasuk perbandingan independen ini. |
| Ringkasan PLSpredict | 0 / 8 indikator | Galat, RMSE, MAE, Q², serta hasil penghitungan ulang model diverifikasi. |
| CVPAT | 0 / 22 baris | Loss dan t direkonstruksi; nilai p native dipertahankan dan keputusan 0,05 sama dengan cek numerik. |
| Konsistensi pengaturan | 0 / 3 run | Jalur dua sisi, HTMT BCa satu sisi, dan prediksi Direct antecedents dibedakan. |
| Keselarasan grafik | N/A | Audit presisi memakai angka dan galat prediksi, bukan grafik. |
| Kontrol data | 0 / 3 pemeriksaan | Dimensi, nilai/urutan CSV, serta frekuensi sepuluh prediksi per kasus sesuai. |
| Dukungan kesimpulan | 0 / 3 keluarga hasil salah hitung | Batasan HTMT, fit, dan CVPAT terhadap LM adalah temuan analitis yang dipertahankan. |

## Tindak lanjut

- Tinjau definisi dan isi item EXP, PP, dan AD untuk dua pasangan HTMT yang belum memenuhi kriteria. Tidak ada indikator dihapus atau data diubah agar ambang terpenuhi.
- Selidiki keterbatasan fit berdasarkan teori dan spesifikasi yang ditetapkan; hindari menambahkan jalur hanya untuk mengejar angka fit.
- Laporkan keunggulan terhadap IA serta hasil CVPAT terhadap LM yang belum signifikan. Pertahankan keterangan bahwa prediksi AD memerlukan TR yang diamati.
- Sediakan data mentah serta aturan dan pemetaan penyaringan bila ingin membuktikan seleksi 323 → 271.

Workbook akhir menghimpun keluaran native, pembanding Python, perbedaan angka, lokasi sumber, dan batasan. Bukti mesin berupa CSV/JSON, skrip rekonstruksi, galat, indeks fold, dan hash sumber disimpan terpisah. Tidak ada berkas native unggahan yang diubah.
