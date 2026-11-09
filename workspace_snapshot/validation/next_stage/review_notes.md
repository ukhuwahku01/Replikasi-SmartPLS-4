# Batas interpretasi dan bahasa naskah KidSense

Catatan ini meninjau keluaran yang sudah diverifikasi; tidak memperkenalkan model revisi, penghapusan item, atau hasil baru. Nama konstruk tetap AIR, EXP, PP, TR, dan AD karena kepanjangan serta bunyi item belum diberikan.

## Kesimpulan mediasi yang boleh dan tidak boleh

Model yang tersedia hanya mengestimasi AIR/EXP/PP→TR→AD. Jalur langsung AIR→AD, EXP→AD, dan PP→AD tidak disertakan. Karena itu, efek langsung tersebut dibatasi nol oleh spesifikasi; efek langsungnya tidak diuji dan tidak dapat disebut tidak signifikan. **Label full mediation/mediasi penuh maupun partial mediation/mediasi parsial belum dapat ditetapkan.**

Menghitung VAF=100% dari model ini akan menghasilkan konsekuensi aritmetis karena total effect sama dengan indirect effect ketika direct effect ditiadakan; angka itu bukan bukti mediasi penuh. Signifikansi jalur menuju TR dan TR→AD saja juga bukan pengganti pengujian bootstrap efek tidak langsung, meskipun dalam berkas ini efek tidak langsung memang sudah memiliki CI bootstrap yang tidak memuat nol.

Bahasa naskah yang didukung:

> Dalam spesifikasi model yang diuji, AIR, EXP, dan PP memiliki asosiasi tidak langsung positif dengan AD melalui TR (β masing-masing 0,179132; 0,202207; dan 0,217019). Interval kepercayaan bootstrap percentile 95% dua sisi untuk ketiga asosiasi tidak langsung tidak memuat nol. Karena jalur langsung AIR/EXP/PP→AD tidak diestimasi, hasil ini tidak digunakan untuk mengklasifikasikan mediasi penuh atau parsial. Keluaran tersebut juga tidak menetapkan mekanisme kausal.

Jika teori memang menghendaki pengujian bentuk mediasi, pertimbangkan model tambahan dengan ketiga jalur langsung yang relevan, disertai bootstrap efek langsung, tidak langsung, dan total. Pisahkan sebagai analisis tambahan dan laporkan seluruh hasil, termasuk jika kesimpulan berubah. Penambahan jalur harus memiliki dasar substantif, bukan dilakukan sekadar untuk memperbaiki fit. Direct effect yang tidak signifikan dalam model tambahan pun tidak membuktikan bahwa efek populasi tepat nol; klaim ketiadaan efek membutuhkan definisi ukuran yang dianggap sepele dan rancangan pengujian yang sesuai. Pengujian mediasi statistik juga tidak mengatasi perancu, urutan waktu, atau keterbatasan desain yang belum dibuktikan.

## HTMT dan pengukuran

> Semua estimasi titik HTMT berada di bawah 0,90, tetapi validitas diskriminan belum terkonfirmasi untuk seluruh pasangan menurut kriteria batas atas bootstrap satu sisi 95% <0,90. Pada run native dengan metode terpilih BCa, batas atas untuk EXP–PP adalah 0,908139 dan EXP–AD adalah 0,912789; delapan pasangan lainnya memenuhi kriteria. Kriteria yang lebih longgar <1 dipenuhi seluruh pasangan, tetapi tidak digunakan sebagai pengganti ambang 0,90 yang sedang dinilai.

- Batas atas≥0,90 berarti bukti belum cukup untuk memenuhi kriteria tersebut; bukan pembuktian nilai HTMT populasi pasti≥0,90.
- EXP–PP=0,859510 juga melampaui ambang titik yang lebih ketat 0,85. Jangan mencampur ambang titik, interval satu sisi, dan interval dua sisi.
- Native BCa dan BC Python tanpa acceleration adalah metode berbeda; pertahankan label, jangan menyebut intervalnya identik.
- Alpha, rho_C, AVE dan loading yang memenuhi patokan tidak menghapus masalah diskriminan. rho_A native belum diverifikasi independen dan harus dibedakan dari hasil yang sudah dihitung ulang.

## Fit global

> SRMR estimated composite sebesar 0,064091 berada di bawah patokan deskriptif 0,08. Namun, SRMR, d_ULS, dan d_G pada estimated composite melampaui batas bootstrap HI95 dan HI99. Dengan demikian, hasil fit tidak mendukung pernyataan bahwa seluruh kriteria kecocokan model telah terpenuhi, meskipun jalur yang diestimasi signifikan.

Saturated composite memiliki ketiga original discrepancy di bawah HI95/HI99, sedangkan estimated composite tidak. Perbedaan ini memotivasi pemeriksaan restriksi struktural, tetapi **tidak mengidentifikasi satu jalur hilang atau satu item sebagai penyebab** dan tidak membuktikan model pengukuran sepenuhnya benar. Tabel mixed dan composite menguji representasi berbeda dan tidak boleh digabung atau dipilih semata karena memberi keputusan yang menguntungkan.

## Prediksi dan CVPAT

> Pada skenario Direct antecedents, Q²_predict positif untuk seluruh delapan indikator. Loss prediksi PLS lebih rendah secara signifikan daripada benchmark indicator average secara keseluruhan (CVPAT p<0,001). Terhadap benchmark linear model, penurunan mean squared loss sekitar 1,59% belum signifikan secara keseluruhan (p=0,122338). Hasil ini tidak membuktikan kesetaraan PLS dan LM. Prediksi AD bersifat kondisional pada TR yang diamati dan tidak mewakili prediksi AD hanya dari AIR, EXP, dan PP.

- Perbandingan RMSE 5/8 dan MAE 7/8 indikator adalah deskriptif; bukan delapan uji keunggulan yang semuanya signifikan.
- Signifikansi AD1/TR4 tanpa koreksi tidak menggantikan Overall; tambahan Holm pada delapan perbandingan indikator LM hanya mempertahankan AD1.
- Q²_predict berbeda dari Q² berbasis blindfolding; jangan memindahkan interpretasinya tanpa menyebut prosedur.
- 2.710 prediksi per indikator berasal dari 271 orang yang diuji sepuluh kali; bukan 2.710 responden independen. Replikasi CVPAT menunjukkan kesesuaian angka software, bukan menghilangkan dependensi prediksi berulang atau menjamin generalisasi ke populasi baru.

## Indikator, responden, dan perubahan model

Tidak ada item yang dapat direkomendasikan dihapus secara substantif hanya dari label AIR1–AD4, loading, cross-loading, atau selisih HTMT. Bunyi item, definisi konstruk, reverse coding, cakupan konten, dan dasar teori perlu diperiksa terlebih dahulu. Loading yang baik tidak meniadakan tumpang tindih isi item. Jangan menggabungkan EXP/PP atau mengganti konstruk hanya karena korelasi tinggi.

Jika perubahan didukung teori/temuan pengodean yang sah: pertahankan model awal, dokumentasikan alasan setiap perubahan, laporkan analisis sensitivitas, hitung ulang seluruh hasil bergantung model, serta nyatakan sifat eksploratori bila perubahan dipilih setelah melihat hasil. Validasi pada data independen diperlukan untuk menilai kestabilan model hasil modifikasi. Hindari pemilihan berulang item/jalur sampai ambang atau p-value tertentu tercapai.

Pengecualian 10 pola jawaban seragam adalah analisis sensitivitas yang sudah diperiksa, bukan bukti otomatis bahwa responden tersebut tidak sah. Jangan mengganti sampel utama tanpa aturan kualitas yang dapat dibenarkan dan dilaporkan. Klaim 323→271, consent/flag D1D2 serta hash sumber mentah masih belum terverifikasi; angka yang dapat direplikasi tidak membuktikan kelayakan seleksi tersebut.

## Sumber yang ditinjau

- `/workspace/validation/native_prediction/output/KidSense_Laporan_Replikasi_Final.md`
- `/workspace/validation/native_bootstrap/native_model_fit.csv`
- `/workspace/validation/native_prediction/native_cvpat_verification.json`
- Audit independen HTMT satu sisi sebelumnya: `/workspace/validation/native_htmt_one_sided/independent/independent_one_sided_htmt.json`
