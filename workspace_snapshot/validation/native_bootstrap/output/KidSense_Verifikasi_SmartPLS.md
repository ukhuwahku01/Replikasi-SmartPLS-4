# Verifikasi ekspor bootstrap SmartPLS KidSense

**Dapat digunakan dengan catatan (Share with caveats). Cakupan parsial:** replikasi estimasi titik dan inferensi jalur selesai diperiksa; HTMT native satu sisi, prediksi native, dan penyaringan data mentah belum selesai. Berkas unggahan dipertahankan utuh.

Ekspor mencatat SmartPLS **4.1.2.1**, proyek KidSense_Replikasi, model KidSense_Model. Pengaturan: **10.000 bootstrap, Complete (slower), Percentile, Two-tailed, alpha 0,05, Fixed seed**. Angka seed tidak tercantum. Log menyatakan 10.000 sampel selesai dan All calculations done. Nilai per draw tidak disimpan.

## Hasil utama

Data asli271 × 20 dalam ekspor identik dengan CSV, termasuk urutan baris: **5.420 nilai cocok persis**. Header AIR1 di native memuat karakter BOM; normalisasi hanya dipakai untuk pemetaan nama. Ini tidak mengubah nilai data.

**62 estimasi titik** (17 beta/f²/VIF/R²/indirect, 35 loading/reliabilitas, 10 HTMT) cocok dengan Python dalam toleransi absolut1e-8. Selisih maksimum **4,80×10⁻¹⁰**. Pemeriksaan ini terpisah dari bootstrap; tidak menyatakan semua SE/CI sama.

| Jalur | beta native | SE native | t native | p native | CI95 percentile native |
|---|---:|---:|---:|---:|---|
| AIR -> TR | 0.260379 | 0.061570 | 4.2290 | 2.368e-05 | [0.139482; 0.380324] |
| EXP -> TR | 0.293921 | 0.068708 | 4.2778 | 1.905e-05 | [0.157908; 0.425392] |
| PP -> TR | 0.315452 | 0.076436 | 4.1270 | 3.705e-05 | [0.164208; 0.465164] |
| TR -> AD | 0.687964 | 0.040753 | 16.8813 | 5.684e-14 | [0.603460; 0.764247] |

Keempat jalur positif, semua p dilaporkan<0,001, dan CI95 percentile tidak memuat nol. t dihitung ulang sebagai|beta|/SE dan cocok. R² TR=0,6163994036 dan R² AD=0,4732948182.

| Asosiasi tidak langsung | beta native | CI95 percentile native | p native |
|---|---:|---|---:|
| AIR -> TR -> AD | 0.179132 | [0.095343; 0.266555] | 4.33e-05 |
| EXP -> TR -> AD | 0.202207 | [0.103184; 0.307668] | 0.0001153 |
| PP -> TR -> AD | 0.217019 | [0.113304; 0.322550] | 4.514e-05 |

Ketiga indirect sama dengan hasil kali koefisien jalur terkait; CI95 tidak memuat nol. Ini mendukung asosiasi tidak langsung pada model, bukan pembuktian kausal atau klaim full mediation. Tidak ada jalur langsung eksogen→AD pada model ini.

Bootstrap native dan Python tidak identik: selisih relatif SE keempat jalur maksimum1,889%; selisih batasCI jalur/indirect/R² maksimum0,004592. Perbedaan prosedur pembangkitan sampel dan implementasi mungkin berperan; ringkasan ini tidak mengisolasi penyebabnya. Seed numerik native tidak diketahui dan per-draw tidak disimpan. Nilai p native berbeda dari aproksimasi normal Python; konvensi numeriknya tidak dapat dipastikan dari ekspor; beberapa nilai sangat kecil mengulang 5,684341886080802e-14. Laporkan p<0,001 dalam narasi, bukan p=0, dan pertahankan nilai asli dalam tabel.

## Catatan yang membatasi kesimpulan

1. **HTMT native satu sisi belum tersedia.** Tabel saat ini memiliki batas 2,5% dan 97,5% dua sisi. Native BC atas 97,5% untuk EXP–PP=0,916798 dan EXP–AD=0,926214; delapan pasangan lain di bawah0,90. Status ini hanya untuk batas 97,5%. Tidak dapat menghitung atau menetapkan secara tepat batas 95 satu sisi dari dua endpoint tersebut. Semua batas native<1 tidak berarti seluruhnya memenuhi kriteria <0,90.
2. **Hasil dekat ambang bergantung interval.** AIR–EXP dan EXP–TR percentile dua sisi native sekarang sedikit di bawah0,90, sedangkan Python sedikit di atas. TitikHTMT tetap sama. Pilih kriteria yang ditetapkan sejak awal dan jangan mengganti metode hanya agar lolos.
3. **Fit global perlu perhatian.** Estimated composite SRMR=0,064091<patokan deskriptif0,08, tetapi nilai ini>HI95bootstrap0,041905. d_ULS=0,862615>HI950,368764 dan d_G=0,190185>HI950,168519; semuanya juga melewati HI99 pada baris estimated composite. Jadi signifikansi jalur tidak membuktikan seluruh spesifikasi model sudah cocok. Tabel mixed dan saturated disimpan terpisah dalam workbook; jangan tertukar.
4. **rho_A baru tersedia dari native.** Rentang0,845098–0,880280; tidak ada pembandingPython awal dan belum dihitung ulang independen. Alpha standardized, rho_C, AVE dan20 loadings sudah dibandingkan.
5. **Cakupan sumber.** Kecocokan CSV271 tidak menyelesaikan asal hash data mentah, eksklusi 323→271 maupun kelompok D1D2. Tidak ada native PLSpredict/CVPAT dalam file ini.

## Cakupan pemeriksaan

Unit adalah komponen atau kelompok klaim yang disebutkan; rasio bukan persentase keakuratan. Nol masalah teramati tidak menandakan komponen yang belum diperiksa telah lolos.

### Kualitas dan kelengkapan artefak

| Kategori | Masalah teramati | Penilaian |
|---|---:|---|
| Kegunaan dan kelengkapan | 0 / 3 keluaran yang direncanakan terbukti salah | Bootstrap jalur diterima; HTMT satu sisi dan PLSpredict belum diserahkan. Kesimpulan keseluruhan tetap parsial. |
| Kejelasan analitis | 0 / 3 keluarga hasil utama | Jalur, indirect, R² diberi definisi dan interval jelas dalam hasil pemeriksaan. |
| Visual/interaksi dashboard | N/A | Tidak ada dashboard yang ditinjau. |

### Ketepatan dan ketahanan analitis

| Kategori | Masalah teramati | Penilaian |
|---|---:|---|
| Identitas input | 0 / 1 dataset analisis | 5.420 nilai dan urutan baris sama; tidak membuktikan seleksi sebelum CSV. |
| Akurasi estimasi titik | 0 / 62 nilai | Semua62 nilai dibandingkan; perbedaan<1e-8. |
| Keselarasan grafik | N/A | Tidak ada grafik yang dipakai untuk audit presisi penuh. |
| Kelengkapan sumber | 0 / 1 ekspor terbukti rusak | Native workbook terbaca, metadata dan lokasi sel dicatat; angka seed/per-draw tidak tersedia. |
| Konsistensi lintas berkas | 0 / 3 keluarga estimasi titik | Struktural, pengukuran, HTMT cocok; SE/CI tidak dipaksa identik. |
| Kontrol data | 0 / 3 pemeriksaan | Dimensi, pemetaan kolom dan seluruh nilai/urutan cocok. |
| Dukungan kesimpulan menyeluruh | 0 / 3 keluaran bootstrap terbukti salah | Jalur didukung; validitas diskriminan satu sisi dan prediksi masih belum lengkap. Fit menunjukkan batasan model, bukan bukti salah hitung. |

## Langkah berikutnya

Simpan run bootstrap jalur ini terpisah. Buat run HTMT 10.000 dengan one-tailed, alpha 0,05; pertahankan PLS Path/Standardized dan Fixed seed. Pilih opsi yang menghasilkan interval bias-corrected sesuai metode yang ditetapkan; catat nama opsi persis dan bedakan BC dari BCa. Pastikan header ekspor benar-benar menampilkan batas atas 95% satu sisi. Lalu jalankan PLSpredict 10 fold × 10 repetisi dan catat desain prediksi. Bandingkan hasil prediksi hanya jika informasi TR yang digunakan setara dengan skenario Python kondisional.

Tidak ada nilai native yang diubah dalam pemeriksaan ini. Workbook baru menyediakan estimasi native, pembandingPython, selisih, sumber baris dan batasan. Skrip sertaJSON audit disimpan bersama hasil.
