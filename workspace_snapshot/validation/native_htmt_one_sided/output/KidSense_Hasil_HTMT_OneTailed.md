# Verifikasi HTMT native SmartPLS: satu sisi BCa

**Kesimpulan: 8 dari 10 pasangan memenuhi batas atas 95% <0,90.** Validitas diskriminan seluruh konstruk belum terdukung menurut kriteria ini. Pemeriksaan ekspor HTMT selesai; studi secara keseluruhan tetap memerlukan catatan fit global dan native prediction.

File mencatat SmartPLS 4.1.2.1, 10.000 bootstrap, Complete, BCa, one-tailed, alpha 0,05, Fixed seed. Header tabel terkoreksi memuat 5% dan 95%; nilai 95% pada kolom G dipakai sebagai batas atas satu sisi. Dua kolom tersebut bukan CI dua sisi 95%.

| Pasangan | HTMT | Batas atas BCa 95 native | Kriteria<0,90 |
|---|---:|---:|---|
| AIR-EXP | 0.832934 | 0.887517 | Memenuhi |
| AIR-PP | 0.819739 | 0.873538 | Memenuhi |
| AIR-TR | 0.805097 | 0.860777 | Memenuhi |
| AIR-AD | 0.709041 | 0.793659 | Memenuhi |
| EXP-PP | 0.859510 | 0.908139 | Belum memenuhi |
| EXP-TR | 0.830228 | 0.886612 | Memenuhi |
| EXP-AD | 0.828422 | 0.912789 | Belum memenuhi |
| PP-TR | 0.822669 | 0.879041 | Memenuhi |
| PP-AD | 0.759295 | 0.830131 | Memenuhi |
| TR-AD | 0.802582 | 0.865819 | Memenuhi |

**EXP–PP** dan **EXP–AD** belum memenuhi. Seluruh estimasi titik berada <0,90, tetapi kriteria yang ditetapkan menggunakan batas atas 95%, sehingga estimasi titik saja belum cukup. Hanya AIR–AD dan PP–AD mempunyai batas atas BCa 95<0,85. Seluruh batas atas<1 adalah kriteria berbeda dari<0,90.

Kesimpulan<0,90 sama dengan hasil Python sebelumnya. Namun native memilih BCa (bias-corrected and accelerated), sedangkan Python awal memakai BC tanpa acceleration; intervalnya tetap diberi label terpisah. Native atas95 EXP–PP=0,908138993 dan EXP–AD=0,912789404; Python BC=0,909877516 dan 0,913698892. Perbedaan ini tidak diartikan sebagai salah hitung atau sebagai replikasi identik dari metode interval.

Kesepuluh estimasi HTMT dihitung ulang langsung dari korelasi Pearson absolut CSV dan cocok dalam 1,4e-15. Semua klasifikasi batas dibanding ambang dihitung ulang. Blok data asli dalam ekspor identik dengan ekspor native terdahulu yang telah diperiksa terhadap 5.420 nilai CSV. Model dan estimasi titik HTMT tidak berubah. Dibanding run sebelumnya, pengaturan metode interval dan arah uji berubah; bootstrap means sama, konsisten dengan Fixed seed tetapi tidak membuktikan seluruh draw sama karena tidak diekspor.

## Cakupan dan keterbatasan

- Diverifikasi: metadata, 10.000 sampel selesai pada log, pengaturan BCa/satu sisi, header95%, seluruh 10 estimasi dan klasifikasi ambang, serta kontinuitas data 271 × 20.
- Tidak direkonstruksi secara independen: semua draw native, koreksi acceleration/jackknife native, atau angka seed numerik yang tidak dicantumkan. Per-sample results=No.
- Pengujian jalur tetap mengacu pada hasil two-tailed sebelumnya. Jangan mengganti p-value hipotesis dengan keluaran run HTMT ini.
- Fit global yang melewati batas bootstrap pada run sebelumnya tetap menjadi catatan; hasil HTMT ini tidak meniadakannya.
- Data mentah 323 respons/flag penyaringan belum tersedia. Native PLSpredict/CVPAT belum diserahkan.

## Implikasi dan langkah berikutnya

Laporan penelitian perlu menyebut dua pasangan yang belum memenuhi validitas diskriminan. Tinjau definisi dan isi item EXP/PP/AD sebelum mengusulkan revisi model; tidak ada indikator yang dihapus atau data yang diubah dalam pemeriksaan ini.

Lanjutkan PLSpredict 10 fold × 10 repetisi untuk memperoleh bukti prediksi native. Hasil prediksi tidak menggantikan pemeriksaan diskriminan dan fit model. Simpan pengaturan prediksi dan jenis informasi TR yang digunakan untuk AD agar perbandingan dengan Python kondisional tetap sepadan.

Berkas unggahan tidak diubah. Workbook pembuktian menampilkan pasangan, estimasi, batas atas, ambang, hasil Python berlabel BC, dan lokasi sel sumber. CSV dan JSON menyimpan angka presisi penuh serta catatan audit.
