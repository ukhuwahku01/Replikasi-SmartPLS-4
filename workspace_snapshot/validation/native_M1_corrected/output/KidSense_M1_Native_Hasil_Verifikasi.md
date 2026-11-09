# Verifikasi bootstrap native M1 lengkap

**Status: perhitungan native M1 sesuai dan terverifikasi dalam cakupan ekspor.** Model tetap analisis sensitivitas posthoc; hasil ini tidak menghapus keterbatasan validitas konstruk, kausalitas, atau prediksi yang belum diuji.

Ekspor mencatat **KidSense_M1_Eksploratori**, SmartPLS 4.1.2.1, lima konstruk (AIR, EXP, PP, TR, AD), 20 indikator reflektif, dan 7 jalur. Seluruh 271 × 20 nilai dan urutan kasus cocok dengan CSV. Bootstrap memakai 10.000, Complete, Percentile, Two-tailed, α = 0,05, Fixed seed. Nilai seed tidak tercatat dan per-sample results tidak disimpan.

Tiga puluh dua estimasi titik (7 jalur, 20 loadings, 2 R², 3 indirect) identik dengan algoritma native M1 yang benar. Perbandingan terhadap Python M1 menunjukkan selisih maksimum 1,00411×10⁻¹⁰. Semua keputusan CI utama sesuai dengan Python; nilai SE dan CI tidak dipaksa identik antar RNG.

## Hasil jalur native

| Jalur | beta | SE | p native | CI95 percentile |
|---|---:|---:|---:|---|
| AIR -> AD | 0.045605 | 0.068430 | 0.505143 | [-0.087686; 0.180170] |
| AIR -> TR | 0.262996 | 0.061725 | 2.05604e-05 | [0.141933; 0.383128] |
| EXP -> AD | 0.337191 | 0.100236 | 0.000771185 | [0.127204; 0.517708] |
| EXP -> TR | 0.292923 | 0.068955 | 2.17624e-05 | [0.156110; 0.425043] |
| PP -> AD | 0.156463 | 0.071161 | 0.027921 | [0.017163; 0.296779] |
| PP -> TR | 0.313463 | 0.076747 | 4.45394e-05 | [0.162077; 0.464231] |
| TR -> AD | 0.304012 | 0.076404 | 6.96902e-05 | [0.156881; 0.459000] |

AIR→AD langsung belum signifikan pada α = 0,05. EXP→AD, PP→AD, TR→AD, dan ketiga jalur menuju TR signifikan secara nominal. Nonsignifikansi AIR direct tidak membuktikan efek populasi tepat nol.

## Asosiasi tidak langsung

| Asosiasi melalui TR | beta | p native | CI95 percentile |
|---|---:|---:|---|
| AIR -> TR -> AD | 0.079954 | 0.00515335 | [0.032983; 0.143367] |
| EXP -> TR -> AD | 0.089052 | 0.00514052 | [0.035225; 0.158803] |
| PP -> TR -> AD | 0.095297 | 0.00481345 | [0.037491; 0.168760] |

Ketiga CI tidak memuat nol. Secara statistik, terdapat dukungan bagi asosiasi tidak langsung melalui TR dalam M1. Untuk EXP/PP, asosiasi langsung dan tidak langsung sama-sama positif. Pola ini tidak membuktikan mediasi kausal, karena model bersifat posthoc pada data persepsi yang sama.

R² AD=0,575904 (CI95 percentile0,460257–0,694855) dan R² TR=0,615656(0,531243–0,701116). Dibanding M0, R² AD meningkat secara deskriptif dari 0,473295; jumlah parameter serta bobot komposit berubah, sehingga ini bukan bukti perbaikan model independen atau F-test nested dengan skor identik.

Total asosiasi AIR→AD=0,125558,p = 0,047521,CIpercentile[0,002081;0,253714],sedangkan correctedCI[−0,002360;0,249998] memuat nol. Laporkan sensitivitas ini bila membahas total AIR. Jangan menggabungkannya dengan efek langsung AIR 0,045605,p = 0,505143 atau memilih interval yang paling mendukung.

## Fit dan batas interpretasi

Estimated dan saturated mempunyai SRMR, d_ULS, d_G yang sama secara numerik pada M1, sesuai saturasi bagian struktural skor. Ini bukan pengujian independen teori tambahan atau saturasi seluruh model indikator.

- **Composite estimated:** SRMR0,031026<HI95 0,034508; d_ULS0,202144<0,250075; d_G0,145440<0,164052.
- **Mixed estimated:** SRMR0,049034>HI95 0,044696; d_ULS0,504913>0,419530; d_G0,275551>0,274682. SRMR dan d_ULS juga melewati HI99; d_G tidak melewati HI99. Karena itu jangan menyatakan seluruh diagnostik fit lolos.

HTMT pada file ini adalah dua sisi(2,5%/97,5%). Semua estimasi serta batas HTMT sama dengan run M0 dua sisi, sehingga penambahan jalur tidak mengubahnya. Kriteria native BCa satu sisi 95% sebelumnya tetap belum terpenuhi untuk EXP–PP(0,908139) dan EXP–AD(0,912789).

M1 native PLSpredict/CVPAT belum tersedia. Hasil prediksi M0 tidak menjadi hasil M1. Untuk perbandingan model yang sepadan, informasi prediktor serta pembagian fold harus setara; Direct antecedents M1 menggunakan lebih banyak anteseden langsung AD daripada M0.

Penelitian tetap survei persepsi atas deskripsi/gambar rancangan. AD adalah niat hipotetis dan kondisional; hasil ini tidak membuktikan adopsi aktual, kinerja AI, audit privasi, atau kausalitas. M0 dipertahankan sebagai baseline, M1 sebagai analisis sensitivitas yang diberi label transparan.

## Cakupan pemeriksaan dan penyelesaian masalah ekspor

- Identitas model, 7 jalur, 20 indikator reflektif, 271 baris, dan semua 5.420 nilai diverifikasi.
- Seluruh 32 estimasi titik dibandingkan terhadap algoritma native M1 dan Python M1; 15 estimasi struktural/total/R² juga dibandingkan dengan SE/CI bootstrap Python secara terpisah.
- Rasio t dihitung ulang dari |beta|/SE; indirect dari hasil kali koefisien terkait; total dari direct+indirect. Tidak ditemukan ketidaksesuaian aritmetika.
- Native p dipertahankan dan tidak diklaim identik dengan pendekatanSciPy. Per-draw bootstrap native tidak dapat direkonstruksi dari ekspor karena tidak disimpan.
- File bootstrap sebelumnya yang tanpa TR tetap keluaran model empat konstruk yang berbeda. Masalah itu kini terselesaikan oleh ekspor baru ini; statistik dari keduanya tidak digabung.

Sumber sel serta hash file ada di workbook, CSV, dan JSON. Berkas unggahan asli tidak diubah. Verifikasi komputasi selesai; justifikasi model dan generalisasi tetap memerlukan batasan yang disebutkan.
