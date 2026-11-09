from pathlib import Path
import json,math,hashlib
import pandas as pd,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
B=Path(__file__).resolve().parent;O=B/'output';O.mkdir(exist_ok=True)
J=json.loads((B/'export_audit.json').read_text());pts=pd.read_csv(B/'integrity/correct_M1_native_vs_python_points.csv');cross=pd.read_csv(B/'integrity/four_construct_algorithm_vs_bootstrap.csv');files=J['files'];good=next(r for r in files if r['correct_M1_structure']);bad=next(r for r in files if r['file']=='KidSense_M1_Bootstrap_10000.xlsx')
w=openpyxl.Workbook();w.remove(w.active)
def tab(name,heads,rows):
 s=w.create_sheet(name);s.append(list(heads))
 for row in rows:s.append(list(row))
 s.freeze_panes='A2';s.auto_filter.ref=s.dimensions;s.row_dimensions[1].height=35
 for c in s[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='164B63');c.alignment=Alignment(wrap_text=True)
 for row in s.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(c.value,float):c.number_format='0.0000000000'
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='EEF4F7')
 for i,col in enumerate(s.columns,1):s.column_dimensions[get_column_letter(i)].width=min(78,max(15,max(len(str(c.value or '')) for c in col)+2))
 for row in s.iter_rows(min_row=2):
  n=max(max(1,math.ceil(len(str(c.value or ''))/(s.column_dimensions[c.column_letter].width*.9))) for c in row);s.row_dimensions[row[0].row].height=min(240,14*n+8)
 return s
summary=[['Status','Estimasi titik M1 terverifikasi; bootstrap native M1 lengkap belum tersedia. Dua file lainnya memakai model berbeda tanpaTR.'],['M1 lengkap','KidSense_M1_Eksploratori.xlsx:5konstruk20indikator7jalur, termasukTR;32perbandingan titik cocok denganPythonM1.'],['Presisi',float(pts['abs_difference'].max())],['Dua file berbeda','KidSense_M1_Algorithm.xlsx danKidSense_M1_Bootstrap_10000.xlsx mencatat modelReport(pls-sem),4konstruk16indikator3jalur tanpaTR.'],['Bootstrap','10.000,Complete,Percentile,Two-tailed,alpha0,05,Fixedseed benar; tetapi pengaturan itu dijalankan pada model tanpaTR.'],['Efek tidak langsung','Kosong karena tidak adaTR atau rantai mediasi pada model4konstruk. Bukan disebabkan Amountofresults.'],['Batas klaim','pAIR→AD0,042186 danCI pada filebootstrap berlaku untuk modeltanpaTR; tidak menjadi inferensiM1 lengkap.'],['Tindakan','Ulangi hanya bootstrap dari model5konstruk7jalur yang benar; ekspor dengan namaKidSense_M1_DenganTR_Bootstrap_10000.xlsx.'],['Pelestarian','Semua unggahan tetap utuh; angka antar model tidak digabung atau diubah.']]
tab('Ringkasan',['Aspek','Hasil'],summary)
tab('Identitas_3_file',['File','Model dalam ekspor','Konstruk','Jumlah konstruk','Indikator dalam model','Jalur','AdaTR','SesuaiM1','R2AD','R2TR','Waktu tercatat'],[[r['file'],r['metadata']['Model'],', '.join(r['constructs']),r['n_constructs'],r['n_items_in_model'],r['n_paths'],r['contains_TR'],r['correct_M1_structure'],r['R2'].get('AD'),r['R2'].get('TR'),r['metadata']['Calculated']] for r in files])
tab('M1_titik_vs_Python',list(pts.columns),pts.itertuples(index=False,name=None))
tab('M1_jalur_native',['Jalur','Beta native','Baris sumber','Status CI native'],[[k,r['estimate'],r['row'],'Belum tersedia dari M1 lengkap'] for k,r in good['paths'].items()])
tab('M1_R2_native',['Konstruk','R2native','Status'],[[k,v,'Model5konstruk denganTR'] for k,v in good['R2'].items()])
tab('Bootstrap_tanpa_TR',['Jalur modeltanpaTR','Beta','SE','t','p','CI95percentile bawah','CI95percentile atas','Status'],[[k,r['estimate'],r['SE'],r['t'],r['p'],r['CI_low'],r['CI_high'],'Bukan inferensiM1 lengkap'] for k,r in bad['paths'].items()])
tab('Cocok_model_4konstruk',list(cross.columns),cross.itertuples(index=False,name=None))
tab('Pengaturan_bootstrap',['Pengaturan','Nilai'],list(bad['settings'].items()))
tab('Sumber',['File','SHA256','Pemeriksaan struktur'],[[r['file'],r['sha256'],'Complete data set / Inner model dan Outer model'] for r in files])
steps=[['1','Kembali keWorkspace dan buka model bernamaKidSense_M1_Eksploratori, bukan laporan(modelpls-sem).'],['2','Pastikan lingkaranAIR,EXP,PP,TR,AD ada; TR1–TR4 tetap terpasang;5konstruk20indikator7jalur.'],['3','Pertahankan AIR/EXP/PP→TR danTR→AD; ketiga jalur tambahan AIR/EXP/PP→AD tetap ada.'],['4','Dari model aktif ini jalankan Calculate→Bootstrapping:10.000,Complete,Percentile,Two-tailed,alpha0,05,Fixedseed.'],['5','Ekspor sebagaiKidSense_M1_DenganTR_Bootstrap_10000.xlsx danunggah. Estimasi algoritma M1 lengkap yang sudah ada tidak perlu diganti.']]
tab('Langkah_ekspor_ulang',['Tahap','Tindakan'],steps)
w.save(O/'KidSense_M1_Pemeriksaan_Kesesuaian_Ekspor.xlsx')
md='''# Audit kesesuaian tiga ekspor M1

**Status: butuh ekspor bootstrap ulang.** Estimasi titik M1 lengkap berhasil diverifikasi; inferensi bootstrap M1 lengkap belum tersedia. Berkas sumber dipertahankan utuh.

Identitas dibaca dari metadata dan matriks model, bukan nama berkas.

| File | Model dalam laporan | Konstruk | Indikator | Jalur | Sesuai M1 lengkap? |
|---|---|---:|---:|---:|---|
'''
for r in files:md+=f"| {r['file']} | {r['metadata']['Model']} | {r['n_constructs']} | {r['n_items_in_model']} | {r['n_paths']} | {'Ya' if r['correct_M1_structure'] else 'Tidak: tanpa TR'} |\n"
md+='''
## Hasil yang sudah terbukti

**KidSense_M1_Eksploratori.xlsx** memuat lima konstruk,20indikator,dan7jalur yang ditetapkan. Data271×20 cocok persis dengan CSV. Tujuh beta,20loadings,duaR²,dan tiga specificindirect (32perbandingan) cocok dengan PythonM1; selisih maksimum **1,00411×10⁻¹⁰**.

| Jalur | Beta native M1 |
|---|---:|
'''
for k,r in good['paths'].items():md+=f"| {k} | {r['estimate']:.6f} |\n"
md+=f"\nR² AD = **{good['R2']['AD']:.6f}** dan R² TR = **{good['R2']['TR']:.6f}**. Tiga estimasi indirect melalui TR juga cocok. Ini membuktikan estimasi titik M1 tersedia native; tidak menyediakan interval bootstrap native bagi M1.\n"
md+='''
## Mengapa dua file lain tidak dapat digabungkan

**KidSense_M1_Algorithm.xlsx** dan **KidSense_M1_Bootstrap_10000.xlsx** mencatat model bernama **Report(pls-sem)**. Keduanya memuat AIR,EXP,PP,AD, dengan tiga jalur AIR/EXP/PP→AD; tidak ada TR maupun TR1–TR4 dalam model. Data yang diekspor adalah271×16nilai yang cocok dengan subsetCSV, bukan data yang nilainya berubah.

Dua puluh estimasi asli pada algorithm dan bootstrap model empat konstruk cocok persis satu sama lain. Jadi masalah utamanya adalah **model yang berbeda**, bukan fluktuasi bootstrap. R² AD model tanpaTR=0,540860; nilai ini bukan R² M1 lengkap yang0,575904.

Bootstrap model empat konstruk memang menyelesaikan10.000sampel denganComplete,Percentile,Two-tailed,α0,05,Fixedseed. Tidak ada efek tidak langsung karena tidak ada rantai mediasi; mengubah Amountofresults tidak akan memunculkan efek melaluiTR pada model tersebut.

Misalnya, AIR→ADβ0,128194 danp0,042186 pada filebootstrap adalah hasil modeltanpaTR. Angka itu tidak dapat dipasangkan dengan betaM1AIR→AD0,045605 atau dipakai untuk menyatakan AIR signifikan setelah mengontrolTR. Interval PythonM1 sebelumnya tetap berlabel Python; tidak ditempel sebagai intervalnative.

## Langkah koreksi

1. Kembali keWorkspace, lalu buka **KidSense_M1_Eksploratori** yang memuat **AIR,EXP,PP,TR,AD**.
2. Pastikan **20indikator**,termasukTR1–TR4,dan **7jalur** ada: AIR/EXP/PP→TR;TR→AD;AIR/EXP/PP→AD.
3. Dari model aktif ini jalankan **Calculate→Bootstrapping**, dengan **10.000,Complete,Percentile,Two-tailed,α0,05,Fixedseed**.
4. Ekspor sebagai **KidSense_M1_DenganTR_Bootstrap_10000.xlsx**, lalu unggah. File algoritma M1 lengkap yang sudah cocok tidak perlu diganti.

M0 tetap dipertahankan sebagai model awal. M1 tetap analisis sensitivitas posthoc; verifikasi angka tidak membuktikan model substantif atau menyelesaikan HTMT. Model empat konstruk dapat disimpan sebagai keluaran berbeda apabila memang diperlukan, tetapi tidak dilaporkan sebagai M1 yang memuatTR.

## Cakupan audit

- Ketiga metadata,matriks inner/outer,pengelompokan item,dan data asli diperiksa.
- M1 lengkap:32estimasi titik dibandingkan independen; seluruhnya cocok dalam1e-8.
- Dua model empat konstruk:20estimasi asli cocok satu sama lain; t=|beta|/SE bootstrap juga konsisten secara aritmetika.
- Terdapat **1/1 bootstrap yang diserahkan tidak cocok dengan target M1**. Ini masalah kesesuaian keluaran, bukan klaim semua angka di file salah.
- Bootstrap native untuk M1 lengkap,besertaCI,p dan SE untuk ketujuh jalur serta indirect,masih memerlukan ekspor yang sesuai.

Sumber sel dan SHA256 ketiga unggahan tercatat pada workbook serta JSON audit. Tidak ada perubahan pada sumber atau penggabungan statistik dari model berbeda.
'''
replace={'lima konstruk,20indikator,dan7jalur':'lima konstruk, 20 indikator, dan 7 jalur','Data271×20':'Data 271 × 20','20loadings,duaR²,dan':'20 loadings, dua R², dan','specificindirect (32perbandingan)':'specific indirect (32 perbandingan)','PythonM1':'Python M1','Report(pls-sem)':'Report (pls-sem)','AIR,EXP,PP,AD':'AIR, EXP, PP, AD','adalah271×16nilai':'adalah 271 × 16 nilai','subsetCSV':'subset CSV','tanpaTR':'tanpa TR','yang0,575904':'yang 0,575904','menyelesaikan10.000sampel':'menyelesaikan 10.000 sampel','denganComplete,Percentile,Two-tailed,α0,05,Fixedseed':'dengan Complete, Percentile, Two-tailed, α = 0,05, Fixed seed','Amountofresults':'Amount of results','melaluiTR':'melalui TR','AIR→ADβ0,':'AIR→AD β 0,','danp0,':'dan p = 0,','filebootstrap':'file bootstrap','modeltanpa':'model tanpa','betaM1AIR→AD0,':'beta M1 AIR→AD 0,','mengontrolTR':'mengontrol TR','intervalnative':'interval native','keWorkspace':'ke Workspace','AIR,EXP,PP,TR,AD':'AIR, EXP, PP, TR, AD','20indikator':'20 indikator','termasukTR1':'termasuk TR1','dan **7jalur**':'dan **7 jalur**','memuatTR':'memuat TR','metadata,matriks':'metadata, matriks','inner/outer,pengelompokan item,dan':'inner/outer, pengelompokan item, dan','lengkap:32estimasi':'lengkap: 32 estimasi','dalam1e-8':'dalam 1e-8','konstruk:20estimasi':'konstruk: 20 estimasi','lengkap,besertaCI,p dan SE':'lengkap, beserta CI, p, dan SE','indirect,masih':'indirect, masih'}
for a,b in replace.items():md=md.replace(a,b)
(O/'KidSense_M1_Status_Verifikasi.md').write_text(md)
print('Audit handoff saved;32M1 point comparisons, bootstrap mismatch retained explicitly.')
