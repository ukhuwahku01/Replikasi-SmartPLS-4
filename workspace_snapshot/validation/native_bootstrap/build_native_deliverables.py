from pathlib import Path
import json,hashlib,openpyxl,pandas as pd
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
B=Path(__file__).resolve().parent;O=B/'output';O.mkdir(exist_ok=True)
S=json.loads((B/'native_structural_verification.json').read_text());M=json.loads((B/'measurement/native_measurement_verification.json').read_text());H=json.loads((B/'htmt/native_htmt_audit.json').read_text())
ref=json.loads(Path('/workspace/attachments/fb78389c-5aaa-4cde-9053-ec03d7da31b6/KidSense_PLS_10000_results.json').read_text());by={p['path']:p for p in ref['paths']}
w=openpyxl.Workbook();w.remove(w.active)
def tab(name,heads,rows):
 t=w.create_sheet(name);t.append(heads)
 for r in rows:t.append(list(r))
 t.freeze_panes='A2';t.auto_filter.ref=t.dimensions
 for c in t[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='164B63');c.alignment=Alignment(wrap_text=True)
 t.row_dimensions[1].height=34
 for row in t.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(vertical='top',wrap_text=True)
   if isinstance(c.value,float):c.number_format='0.0000000000'
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='EFF5F7')
 for j,col in enumerate(t.columns,1):t.column_dimensions[get_column_letter(j)].width=min(72,max(15,max(len(str(c.value or '')) for c in col)+2))
 return t
summary=[['Status','Replikasi estimasi titik berhasil; inferensi jalur didukung. Pemeriksaan model secara keseluruhan masih memerlukan catatan.'],['Data','271 × 20 nilai asli, seluruh 5.420 nilai dan urutan baris cocok dengan CSV.'],['Kecocokan estimasi titik','62 pembandingan: 17 struktural + 35 pengukuran + 10 HTMT; semua selisih absolut <1e-8.'],['Selisih maksimum titik',max(S['max_point_abs_difference'],M['max_abs_numeric_difference'],H['max_abs_point_difference'])],['Bootstrap','10.000, Complete (slower), Percentile, Two-tailed, alpha 0,05; Fixed seed, angka seed tidak tercatat.'],['Jalur','4/4 positif; semua p native <0,001 dan percentile CI95 tidak memuat nol.'],['Indirect','3/3 positif; semua p native <0,001 dan percentile CI95 tidak memuat nol.'],['R2','TR=0,6163994036; AD=0,4732948182.'],['Beda bootstrap','SE dan CI berbeda dari Python. Maksimum selisih relatif SE empat jalur 1,889%; bukan kegagalan replikasi estimasi titik.'],['HTMT','Run ini dua sisi (2,5%–97,5%). Batas BC97,5 native EXP–PP=0,916798 dan EXP–AD=0,926214; batas BC satu sisi95 belum tersedia.'],['Model fit','Estimated composite: d_ULS=0,862615 > HI95=0,368764; d_G=0,190185 > HI95=0,168519. Tidak mendukung klaim seluruh kriteria fit terpenuhi.'],['Belum ada','Native HTMT one-sided95, PLSpredict/CVPAT, bukti penyaringan data mentah323→271, draw bootstrap per sampel.'],['Sumber','Ekspor native SmartPLS 4.1.2.1; waktu dalam file Nov6 2026 1:03:21AM, zona tidak dinyatakan dalam file.'],['Berkas asli','Unggahan tidak diubah. Ini hasil pemeriksaan baru.']]
tab('Ringkasan',['Bagian','Hasil'],summary)
tab('Jalur_native',['Jalur','Beta SmartPLS','SE SmartPLS','t SmartPLS','p SmartPLS dilaporkan','CI95 pct bawah','CI95 pct atas','Beta Python','SE Python','CI95 Python bawah','CI95 Python atas','Delta beta','Delta SE relatif','Baris sumber'],[[k,p['O'],p['SE'],p['t'],p['p'],*p['ci95_percentile'],by[k]['beta'],by[k]['se'],*by[k]['ci95'],p['O']-by[k]['beta'],p['SE_relative_difference_vs_Python'],p['excel_row']] for k,p in S['paths'].items()])
tab('Indirect_native',['Asosiasi','Beta SmartPLS','SE','t','p dilaporkan','CI95 pct bawah','CI95 pct atas','Hasil kali beta jalur','Selisih hasil kali','Baris sumber'],[[k,p['O'],p['SE'],p['t'],p['p'],*p['ci95_percentile'],p['product_of_paths'],p['product_absolute_error'],p['excel_row']] for k,p in S['indirect'].items()])
tab('R2_native',['Konstruk','R2','CI95 pct bawah','CI95 pct atas','Baris sumber'],[[k,p['O'],*p['ci95_percentile'],p['excel_row']] for k,p in S['r2'].items()])
keys=['group','label','metric','Python','SmartPLS','signed_difference','absolute_difference','comparison_kind','source_row','status'];tab('Banding_struktural',keys,[[r[k] for k in keys] for r in S['comparison']])
keys=['kind','entity','native','reference','abs_difference','native_cell','reference_method'];tab('Banding_pengukuran',keys,[[r[k] for k in keys] for r in M['comparisons']])
tab('rho_A_native',['Konstruk','rho_A native','Sel sumber','Status pembanding'],[[r['construct'],r['native_rho_A'],r['native_cell'],'Belum dihitung independen; tidak ada pada Python awal'] for r in M['rho_A_native_new']])
tab('HTMT_dua_sisi',['Pasangan','HTMT native','HTMT Python','Delta titik','PCT native bawah2.5','PCT native atas97.5','BC native bawah2.5','BC native atas97.5','PCT Python atas97.5','BC Python atas97.5','BC native97.5 <0.90','BC native atas95 satu sisi','Status batas satu sisi95'],[[r['pair'],r['native_percentile']['point'],r['prior_python_point'],r['point_difference_native_minus_python'],r['native_percentile']['lower_025'],r['native_percentile']['upper_975'],r['native_BC']['lower_025'],r['native_BC']['upper_975'],r['prior_python_percentile_two_sided'][1],r['prior_python_BC_two_sided_upper_975'],r['native_BC_upper_975_below_090'],None,'BELUM DIEKSPOR; jangan isi dengan nilai Python'] for r in H['pairs']])
keys=['metric','model','original','HI95','HI99','original_below_HI95','original_below_HI99','source_row'];tab('Fit_native',keys,[[r[k] for k in keys] for r in S['fit']])
tab('Pengaturan',['Pengaturan','Nilai native'],list(S['settings'].items())+list(S['metadata'].items())+[[f'Outer weighting {k}',v] for k,v in M['native_construct_outer_weighting_modes'].items()])
limits=[['Estimasi vs bootstrap','Estimasi titik cocok; SE, t, p dan CI native tidak identik dengan Python. Perbedaan RNG/resampling dan implementasi mungkin berperan; penyebab tepat tidak dapat diisolasi dari ringkasan.'],['p sangat kecil','Beberapa nilai p native mengulang 5,684341886080802e-14. Pertahankan angka ekspor, laporkan p<0,001 dalam narasi; tidak menulis p=0. P-value normal Python berbeda dan tidak diperlakukan identik.'],['HTMT','Kriteria batas atas<1 berbeda dari<0,90. Dua batas atas97,5 yang melewati0,90 tidak cukup menentukan apakah batas 95 satu sisi juga melewati0,90.'],['Mode pengukuran','Native mencatat AUTOMATIC; 20 link reflektif dan hasilnya cocok dengan kalkulasi ModeA independen.'],['rho_A','Angka baru dari native tersedia; tidak diklaim sudah direplikasi independen.'],['Efek kausal','Signifikansi jalur dan indirect mendukung asosiasi dalam model; tidak menetapkan sebab-akibat atau mediasi kausal.'],['Fit','SRMR estimated composite0,064091<0,08 tetapi melebihi HI95/HI99 bootstrap. d_ULS dan d_G estimated juga melewati HI95/HI99; hindari klaim semua fit baik.'],['Seleksi data','Kecocokan 271 baris analisis tidak membuktikan aturan eksklusi323→271, consent atau D1D2.'],['Sampel bootstrap','Save results per sample=No; tidak dapat membandingkan seluruh draw native dengan Python.'],['PLSpredict','Belum ada hasil prediksi native pada workbook ini.']]
tab('Batasan',['Topik','Catatan'],limits)
tab('Sumber',['Sumber','SHA256 / catatan'],[['KidSense_Bootstrap_10000.xlsx',S['source_sha256']],['CSV271',M['input_CSV_sha256']],['Sheet sumber','Complete data set; baris sumber tertera pada tabel hasil'],['Pembanding','Python yang sudah dihitung ulang dari CSV pada pemeriksaan sebelumnya; bootstrap10.000 berbeda stream']])
file=O/'KidSense_Verifikasi_SmartPLS_vs_Python.xlsx';w.save(file)
rr=openpyxl.load_workbook(file,data_only=True);assert rr['Jalur_native'].max_row==5;assert rr['Indirect_native'].max_row==4;assert rr['HTMT_dua_sisi'].max_row==11
assert not [(ss.title,c.coordinate) for ss in rr for row in ss for c in row if c.data_type=='e']
md='''# Verifikasi ekspor bootstrap SmartPLS KidSense

**Dapat digunakan dengan catatan (Share with caveats). Cakupan parsial:** replikasi estimasi titik dan inferensi jalur selesai diperiksa; HTMT native satu sisi, prediksi native, dan penyaringan data mentah belum selesai. Berkas unggahan dipertahankan utuh.

Ekspor mencatat SmartPLS **4.1.2.1**, proyek KidSense_Replikasi, model KidSense_Model. Pengaturan: **10.000 bootstrap, Complete (slower), Percentile, Two-tailed, alpha 0,05, Fixed seed**. Angka seed tidak tercantum. Log menyatakan 10.000 sampel selesai dan All calculations done. Nilai per draw tidak disimpan.

## Hasil utama

Data asli271 × 20 dalam ekspor identik dengan CSV, termasuk urutan baris: **5.420 nilai cocok persis**. Header AIR1 di native memuat karakter BOM; normalisasi hanya dipakai untuk pemetaan nama. Ini tidak mengubah nilai data.

**62 estimasi titik** (17 beta/f²/VIF/R²/indirect, 35 loading/reliabilitas, 10 HTMT) cocok dengan Python dalam toleransi absolut1e-8. Selisih maksimum **4,80×10⁻¹⁰**. Pemeriksaan ini terpisah dari bootstrap; tidak menyatakan semua SE/CI sama.

| Jalur | beta native | SE native | t native | p native | CI95 percentile native |
|---|---:|---:|---:|---:|---|
'''
for k,p in S['paths'].items():md+=f"| {k} | {p['O']:.6f} | {p['SE']:.6f} | {p['t']:.4f} | {p['p']:.4g} | [{p['ci95_percentile'][0]:.6f}; {p['ci95_percentile'][1]:.6f}] |\n"
md+='''
Keempat jalur positif, semua p dilaporkan<0,001, dan CI95 percentile tidak memuat nol. t dihitung ulang sebagai|beta|/SE dan cocok. R² TR=0,6163994036 dan R² AD=0,4732948182.

| Asosiasi tidak langsung | beta native | CI95 percentile native | p native |
|---|---:|---|---:|
'''
for k,p in S['indirect'].items():md+=f"| {k} | {p['O']:.6f} | [{p['ci95_percentile'][0]:.6f}; {p['ci95_percentile'][1]:.6f}] | {p['p']:.4g} |\n"
md+='''
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
'''
(O/'KidSense_Verifikasi_SmartPLS.md').write_text(md)
manifest={'native_file':S['source_file'],'native_sha256':S['source_sha256'],'CSV_sha256':M['input_CSV_sha256'],'point_comparisons':62,'max_point_abs_difference':max(S['max_point_abs_difference'],M['max_abs_numeric_difference'],H['max_abs_point_difference']),'settings':S['settings'],'next_required':['Native one-sided95 BC HTMT','Native PLSpredict'],'original_modified':False}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(file);print('Original input untouched,62 point values compared; new workbook reopened and checked.')
