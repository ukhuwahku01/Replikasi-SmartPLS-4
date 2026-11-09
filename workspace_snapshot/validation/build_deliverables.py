from pathlib import Path
import json, hashlib, platform, importlib.metadata, zipfile, csv
import numpy as np, pandas as pd, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
BASE=Path(__file__).resolve().parent; ATT=BASE.parent/'attachments'; OUT=BASE/'output'; OUT.mkdir(exist_ok=True)
def load(name): return json.loads(next(ATT.rglob(name)).read_text())
original=load('KidSense_PLS_10000_results.json'); cvref=load('KidSense_CV_Prediction_Exploratory.json'); href=load('KidSense_HTMT_10000_validation.json')
point=json.loads((BASE/'pls_point_verification.json').read_text()); boot=json.loads((BASE/'pls_bootstrap_verification.json').read_text()); htmt=json.loads((BASE/'htmt/htmt_verification.json').read_text()); cv=json.loads((BASE/'prediction/prediction_validation.json').read_text()); hs=json.loads((BASE/'htmt/htmt_workbook_supplement.json').read_text())
d=pd.read_csv(next(ATT.rglob('*.csv')))
sources=[dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(ATT.rglob('*')) if p.is_file() and p.suffix in ['.json','.csv','.xlsx']]
checks=point['checks']+boot['checks']
for r,expected in zip(htmt['pairs'],href['pairs']):
 for k in ['HTMT+','percentile_CI95_lower','percentile_CI95_upper','percentile_upper95_one_sided','BC_upper95_one_sided','BC_upper97.5_two_sided']:
  e=expected['percentile_CI95_two_sided'][0 if k.endswith('lower') else 1] if k in ['percentile_CI95_lower','percentile_CI95_upper'] else expected[k]
  checks.append(dict(section='HTMT',label=r['pair'],metric=k,reported=e,recomputed=r[k],abs_diff=abs(e-r[k])))
for r,e in zip(cv['indicators'],cvref['indicators']):
 for a,b in [('RMSE_PLS_exploratory','RMSE_PLS_recalculated'),('RMSE_IA_mean','RMSE_mean_recalculated'),('RMSE_LM','RMSE_LM_recalculated'),('MAE_PLS_exploratory','MAE_PLS_recalculated'),('MAE_IA_mean','MAE_mean_recalculated'),('MAE_LM','MAE_LM_recalculated'),('Q2_predict_analogue','q2_recalculated')]:
  checks.append(dict(section='CV',label=r['indicator'],metric=a,reported=e[a],recomputed=r[b],abs_diff=abs(e[a]-r[b])))
for r in checks: r['tolerance']=1e-8; r['status']='COCOK' if r['abs_diff']<=1e-8 else 'SELISIH'
assert all(r['status']=='COCOK' for r in checks)
pd.DataFrame(checks).to_csv(OUT/'KidSense_Pembandingan_Semua_Angka.csv',index=False)
issues=[
 ('METADATA','Hash sumber berbeda','HTMT JSON dan CV JSON mencantumkan 5c517d0b...83fcc; SHA256 CSV aktual ab7e5333...216624. Angka tetap dapat direplikasi.','Simpan hash aktual CSV secara terpisah. Bila hash lama milik data mentah, beri label nama file dan sediakan file tersebut.'),
 ('BATAS KESIMPULAN','Dua pasangan HTMT belum memenuhi kriteria','Batas atas BC satu sisi 95%: EXP–PP 0.9098775164; EXP–AD 0.9136988925, keduanya >=0.90. Workbook asli telah menyatakan ini.','Jangan menyimpulkan validitas diskriminan seluruh konstruk telah terbukti; tinjau definisi/indikator dan estimasi ulang bila diperlukan.'),
 ('BELUM TERVERIFIKASI','Seleksi responden dan perhatian','323 respons awal, eksklusi 52, semua A1=Yes, B1–B4, D1/D2 n228, irisan n220, dan klaim timestamp unik tidak dapat diuji dari CSV 20 indikator.','Butuh data mentah, flag penyaringan dan pemetaan baris; bukan bukti bahwa klaim tersebut salah.'),
 ('LABEL METODE','Alpha menggunakan standardisasi','Seluruh alpha dalam workbook adalah standardized Cronbach alpha, bukan alpha berbasis kovarians item mentah; selisih maksimal raw vs standardized 0.00037235.','Labeli alpha sebagai standardized; kedua versi ada di sheet Reliabilitas.'),
 ('BATAS METODE','Python, bukan keluaran SmartPLS 4','Hasil mereplikasi PLS-PM Mode A, bootstrap serta CV eksploratori Python. Tidak ada hasil native SmartPLS atau CVPAT yang diuji.','Gunakan label metode yang tepat; ekspor resmi SmartPLS diperlukan bila mengklaim hasil software tersebut.'),
 ('BATAS PREDIKSI','Prediksi AD bersifat kondisional','AD diprediksi dengan indikator TR yang diamati dalam fold uji; bukan prediksi AD hanya dari AIR/EXP/PP.','Nyatakan kondisi penggunaan prediktor ini. Keunggulan galat tidak membuktikan signifikansi statistik.'),
 ('BATAS INFERENSI','Asosiasi bukan sebab-akibat','Empat jalur positif dan CI tidak memuat nol; desain dan keluaran ini tidak membuktikan efek kausal atau mediasi kausal.','Gunakan istilah asosiasi langsung/tidak langsung; hasil HTMT membatasi interpretasi konstruk.')]
summary=[
 ['Status','Dapat digunakan dengan catatan; pembuktian numerik selesai untuk data yang tersedia, audit asal/seleksi parsial.'],
 ['Tanggal','6 November 2026 (Asia/Jakarta)'],
 ['Data diperiksa','271 baris × 20 indikator; tidak ada nilai kosong; semua integer 1–5.'],
 ['Pemeriksaan angka',f'{len(checks)} perbandingan skalar cocok dengan toleransi absolut 1e-8; bukan persentase keakuratan penelitian.'],
 ['PLS utama','4 koefisien jalur, 2 R², 3 asosiasi tidak langsung, f²/VIF serta 10.000 bootstrap direplikasi.'],
 ['HTMT','10 estimasi dan 50 batas interval bootstrap cocok persis.'],
 ['Prediksi','10 repetisi × 10 fold: PLS, mean dan LM direplikasi; Q² positif 8/8; PLS lebih baik dari LM 5/8 RMSE dan 6/8 MAE.'],
 ['Sensitivitas','n271 dan tanpa 10 jawaban seragam n261 direplikasi; D1/D2 n228 serta irisan n220 belum dapat diuji.'],
 ['Berkas asli','Lima unggahan tidak diubah. Ini workbook pembuktian baru.'],
 ['Kesimpulan penting','Tidak cukup untuk menyatakan seluruh validitas diskriminan terpenuhi atau sebagai hasil native SmartPLS.']]
wb=openpyxl.Workbook(); wb.remove(wb.active)
def sheet(name,headers,rows):
 s=wb.create_sheet(name);s.append(list(headers))
 for r in rows: s.append(list(r))
 s.freeze_panes='A2';s.auto_filter.ref=s.dimensions
 for cell in s[1]:cell.font=Font(color='FFFFFF',bold=True);cell.fill=PatternFill('solid',fgColor='17365D');cell.alignment=Alignment(wrap_text=True,vertical='top')
 s.row_dimensions[1].height=32
 for row in s.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(vertical='top',wrap_text=True)
   if isinstance(c.value,float):c.number_format='0.0000000000'
  if row[0].row%2==0:
   for c in row:c.fill=PatternFill('solid',fgColor='EEF3F8')
 for j,col in enumerate(s.columns,1):
  mx=max(len(str(c.value or '')) for c in col);s.column_dimensions[get_column_letter(j)].width=min(65,max(14,mx+2))
 return s
sheet('Ringkasan',['Bagian','Hasil'],summary)
sheet('Jalur',['Jalur','Beta hasil ulang','SE bootstrap ulang','t beta/SE','p normal dua sisi','CI95 bawah','CI95 atas','f2','VIF'],[[p['path'],point['point_beta'][i],next(r['recomputed'] for r in boot['checks'] if r['section']=='paths' and r['label']==p['path'] and r['metric']=='se'),p['t'],p['p'],*p['ci95'],p['f2'],p['VIF']] for i,p in enumerate(original['paths'])])
sheet('R2',['Konstruk','R2 hasil ulang','CI95 bawah','CI95 atas'],[[p['construct'],point['r2'][i],*p['ci95']] for i,p in enumerate(original['r2'])])
sheet('Mediasi',['Asosiasi tidak langsung','Beta hasil ulang','CI95 bawah','CI95 atas'],[[p['effect'],point['point_beta'][i]*point['point_beta'][3],*p['ci95']] for i,p in enumerate(original['indirect'])])
sheet('Reliabilitas',['Konstruk','Alpha standardized','Alpha raw','rho_C','AVE','Loading min','Loading max','Rata-rata Likert'],[[r[k] for k in ['construct','alpha_standardized','alpha_raw','rho_C','AVE','loading_min','loading_max','mean']] for r in point['reliability']])
sheet('HTMT',['Pasangan','HTMT+ ulang','BC atas95 satu sisi','Percentile atas95 satu sisi','CI95 pct bawah','CI95 pct atas','BC atas97.5 dua sisi','BC95 <0.90','Point <0.85'],[[r['pair'],r['HTMT+'],r['BC_upper95_one_sided'],r['percentile_upper95_one_sided'],r['percentile_CI95_lower'],r['percentile_CI95_upper'],r['BC_upper97.5_two_sided'],'MEMENUHI' if r['one_sided_BC_under090'] else 'BELUM MEMENUHI','YA' if r['point_below_085'] else 'TIDAK'] for r in htmt['pairs']])
sheet('Prediksi_CV',['Indikator','RMSE PLS','RMSE mean','RMSE LM','MAE PLS','MAE mean','MAE LM','Q2 analogue','PLS < LM RMSE','PLS < LM MAE'],[[r[k] for k in ['indicator','RMSE_PLS_recalculated','RMSE_mean_recalculated','RMSE_LM_recalculated','MAE_PLS_recalculated','MAE_mean_recalculated','MAE_LM_recalculated','q2_recalculated','beats_LM_RMSE','beats_LM_MAE']] for r in cv['indicators']])
keys=['section','label','metric','reported','recomputed','abs_diff','tolerance','status'];sheet('Pembandingan_angka',keys,[[r[k] for k in keys] for r in checks])
sheet('Sensitivitas',['Skenario','n','AIR→TR','EXP→TR','PP→TR','TR→AD','R2 TR','R2 AD','Status'],[['Utama',271,*point['point_beta'],*point['r2'],'COCOK'],['Tanpa jawaban seragam',261,*point['sensitivity_beta'],*point['sensitivity_r2'],'COCOK'],['Lolos D1/D2',228,None,None,None,None,None,None,'BELUM DAPAT DIVERIFIKASI'],['Lolos D1/D2 dan tanpa seragam',220,None,None,None,None,None,None,'BELUM DAPAT DIVERIFIKASI']])
sheet('Batasan',['Kategori','Temuan','Bukti / batasan','Tindak lanjut'],issues)
sheet('Sumber',['File','SHA256 aktual','Ukuran byte'],[[r['file'],r['sha256'],r['bytes']] for r in sources])
sheet('Data271',d.columns,d.itertuples(index=False,name=None))
workbook=OUT/'KidSense_Pembuktian_Hasil.xlsx';wb.save(workbook)
# Reopen and verify core numbers and no error cells.
ww=openpyxl.load_workbook(workbook,data_only=True);assert ww['Data271'].max_row==272;assert ww['Pembandingan_angka'].max_row==len(checks)+1
assert not [(s.title,c.coordinate) for s in ww for row in s for c in row if c.data_type=='e']
versions={k:importlib.metadata.version(k) for k in ['numpy','pandas','scipy','openpyxl','scikit-learn']}; versions['Python']=platform.python_version()
manifest={'date_timezone':'2026-11-06 Asia/Jakarta','files':sources,'versions':versions,'scalar_comparisons':len(checks),'max_abs_difference':max(r['abs_diff'] for r in checks),'tolerance_absolute':1e-8,'original_files_modified':False,'bootstrap_resamples_PLS':10000,'bootstrap_resamples_HTMT':10000,'coverage':'Numerical replication complete where inputs exist; source selection/eligibility and native SmartPLS execution unverified.'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
md=f'''# Pembuktian hasil KidSense

**Status: dapat digunakan dengan catatan (Share with caveats). Cakupan: parsial.**

Dihitung ulang pada 6 November 2026 WIB dari kelima file unggahan. Seluruh hasil numerik utama yang dapat dihitung dari CSV berhasil direplikasi. Lima berkas asli tidak diubah; workbook pembuktian ini dibuat terpisah. Bukti seleksi respons awal dan keluaran native SmartPLS tidak tersedia.

## Hasil yang terbukti dari CSV

CSV berisi **271 × 20** nilai integer 1–5, tanpa nilai kosong. Ada 10 baris jawaban seragam dan 7 pengulangan pola jawaban penuh. Pola identik tidak membuktikan responden ganda; tidak ada identitas atau timestamp dalam CSV.

| Jalur | Beta ulang | CI95 bootstrap dilaporkan dan direplikasi | p dua sisi aproksimasi normal |
|---|---:|---:|---:|
'''
for p,b in zip(original['paths'],point['point_beta']):md+=f"| {p['path']} | {b:.6f} | [{p['ci95'][0]:.6f}; {p['ci95'][1]:.6f}] | {p['p']:.3g} |\n"
md+='''
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
| Perhitungan angka | 0 / '''+str(len(checks))+''' perbandingan skalar | Semua angka yang dibandingkan independen cocok dalam toleransi absolut 1e-8. Ini tidak meliputi klaim penyaringan yang tidak memiliki input. |
| Keselarasan grafik | N/A | Tidak ada grafik dalam artefak sumber. |
| Kelengkapan data untuk penyaringan | 0 / 4 skenario terbukti salah | Dua skenario direplikasi; dua skenario D1/D2 belum dapat diverifikasi, bukan dianggap lolos. |
| Konsistensi lintas berkas | 0 / 4 bagian bersama | HTMT, Structural, Indirect dan Exploratory CV workbook konsisten dengan JSON; hash sumber dinilai terpisah. |
| Kontrol kualitas input | 0 / 3 pemeriksaan | Dimensi 271×20, tanpa missing, integer 1–5 terkonfirmasi. |
| Dukungan kesimpulan numerik | 0 / 3 keluarga hasil | Hasil PLS, HTMT dan CV cocok dengan kualifikasi pada workbook; tidak menjustifikasi klaim seluruh diskriminan lolos, kausalitas atau native SmartPLS. |

## Masalah prioritas dan penanganan

1. **Identitas hash sumber belum cocok.** CSV aktual SHA256 `'''+hashlib.sha256(next(ATT.rglob('*.csv')).read_bytes()).hexdigest()+'''`; HTMT/CV JSON mencantumkan `5c517d0bcc99f0ce5e909af11da5a4fca1f0c23bb8c4e9060f7cf620def83fcc`. **Usulan:** pisahkan hash file mentah dan CSV analisis dengan nama file masing-masing. Kecocokan perhitungan membuktikan angka dapat diperoleh dari CSV; bukan pembuktian rantai asal data.
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
'''
(OUT/'KidSense_Laporan_Pembuktian.md').write_text(md)
print(json.dumps({'workbook':str(workbook),'scalar_checks':len(checks),'max_diff':max(r['abs_diff'] for r in checks),'sheets':wb.sheetnames,'versions':versions},indent=2))
