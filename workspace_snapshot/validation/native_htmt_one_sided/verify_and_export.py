"""Verify a native SmartPLS one-tailed BCa HTMT export; preserve source files."""
from pathlib import Path
import json,hashlib,itertools
import numpy as np,pandas as pd,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
B=Path(__file__).resolve().parent;O=B/'output';O.mkdir(exist_ok=True)
N=Path('/workspace/attachments/666e1de7-a27b-4946-9db1-3c78729861ed/KidSense_HTMT_BCa_10000_OneTailed.xlsx')
P=Path('/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx')
C=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
J=Path('/workspace/attachments/d0bcb909-7b59-4061-ba39-2de66241055c/KidSense_HTMT_10000_validation.json')
w=openpyxl.load_workbook(N,data_only=True);s=w['Complete data set'];prev=openpyxl.load_workbook(P,data_only=True)['Complete data set'];ref=json.loads(J.read_text());d=pd.read_csv(C)
names=['AIR','EXP','PP','TR','AD'];order={n:i for i,n in enumerate(names)}
def pair(raw):return '-'.join(sorted(raw.split(' <-> '),key=order.get))
def direct_htmt(a,b):
 R=np.abs(d.corr().to_numpy());ga=[d.columns.get_loc(f'{a}{i}') for i in range(1,5)];gb=[d.columns.get_loc(f'{b}{i}') for i in range(1,5)];tri=np.triu_indices(4,1)
 return float(R[np.ix_(ga,gb)].mean()/np.sqrt(R[np.ix_(ga,ga)][tri].mean()*R[np.ix_(gb,gb)][tri].mean()))
settings={s.cell(r,2).value:s.cell(r,3).value for r in [678,679,680,681,682,683,689,690,691,692,693,694,695,696]}
assert int(settings['Samples'])==10000 and settings['Test type']=='One-tailed' and float(settings['Significance level'])==.05
assert settings['Confidence interval method']=='Bias-corrected and accelerated (BCa) bootstrap' and settings['Complexity']=='Complete (slower)'
assert s.cell(479,7).value=='95.0%' and s.cell(465,6).value=='95.0%'
# Prior native original-data block has already been mapped/verified against all 5420 CSV values.
diffs=[(r,c) for r in range(795,1072) for c in range(1,23) if s.cell(r,c).value!=prev.cell(r,c).value]
assert not diffs
ref={r['pair']:r for r in ref['pairs']};rows=[]
for r in range(480,490):
 label=pair(s.cell(r,2).value);p=ref[label];calc=direct_htmt(*label.split('-'));rr=r-14
 native=float(s.cell(r,3).value);u=float(s.cell(r,7).value);pct=float(s.cell(rr,6).value);lo=float(s.cell(r,6).value)
 assert lo<=u and native>=0 and abs(native-calc)<1e-12
 assert native==float(prev.cell(r,3).value)
 row={'pair':label,'HTMT_native':native,'HTMT_recomputed_CSV':calc,'point_abs_difference':abs(native-calc),'native_BCa_lower5':lo,'native_BCa_upper95':u,'native_PCT_upper95':pct,'BCa_upper95_below090':u<.9,'PCT_upper95_below090':pct<.9,'BCa_upper95_below085':u<.85,'point_below090':native<.9,'point_below085':native<.85,'Python_BC_upper95':p['BC_upper95_one_sided'],'Python_PCT_upper95':p['percentile_upper95_one_sided'],'delta_native_BCa_minus_Python_BC':u-p['BC_upper95_one_sided'],'classification_agrees_Python_BC090':(u<.9)==p['one_sided_BC_under090'],'native_source_BCa_upper95':f"'Complete data set'!G{r}",'native_source_PCT_upper95':f"'Complete data set'!F{rr}",'method_comparison':'Native selected BCa versus prior Python BC without acceleration; intervals are different methods.'}
 rows.append(row)
rows.sort(key=lambda r:tuple(order[n] for n in r['pair'].split('-')))
assert len(rows)==10 and sum(r['BCa_upper95_below090'] for r in rows)==8
meta={w['Navigation'].cell(r,2).value:w['Navigation'].cell(r,3).value for r in range(4,9)}
result={'source':N.name,'source_sha256':hashlib.sha256(N.read_bytes()).hexdigest(),'CSV_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'metadata':meta,'settings':settings,'data_same_as_previously_verified_271x20':True,'original_indicator_block_differences_vs_previous_native':0,'n':271,'indicators':20,'pairs':rows,'BCa_upper95_below090_count':8,'BCa_upper95_below085_count':sum(r['BCa_upper95_below085'] for r in rows),'PCT_upper95_below090_count':sum(r['PCT_upper95_below090'] for r in rows),'all_classifications_agree_with_Python_BC090':all(r['classification_agrees_Python_BC090'] for r in rows),'max_HTMT_abs_difference_vs_direct_CSV':max(r['point_abs_difference'] for r in rows),'scope':'Verified export settings, all10 HTMT point calculations from CSV, all10 bound classifications, and data continuity. Did not independently reconstruct native BCa bootstrap draws/acceleration; per-sample draws not saved.','limitations':['BCa native is not the BC method of prior Python; preserve separate method labels.','The displayed5% and95% columns are not a central two-sided95% interval. Only the upper95% bound is used for the one-sided criterion.','Fixed seed recorded, numeric seed not exposed.','Passing all upper bounds below1 is a different criterion from below0.90.','Do not use this one-tailed run to replace prior two-tailed path significance.','Native PLSpredict/CVPAT not included; raw response eligibility323→271 still outside scope.']}
(B/'verification.json').write_text(json.dumps(result,indent=2));pd.DataFrame(rows).to_csv(O/'KidSense_HTMT_OneTailed_BCa.csv',index=False)
out=openpyxl.Workbook();out.remove(out.active)
def tab(name,headers,values):
 t=out.create_sheet(name);t.append(headers)
 for row in values:t.append(list(row))
 t.freeze_panes='A2';t.auto_filter.ref=t.dimensions;t.row_dimensions[1].height=35
 for c in t[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='164B63');c.alignment=Alignment(wrap_text=True)
 for row in t.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(c.value,float):c.number_format='0.0000000000'
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='EEF4F7')
 for j,col in enumerate(t.columns,1):t.column_dimensions[get_column_letter(j)].width=min(72,max(15,max(len(str(c.value or '')) for c in col)+2))
 return t
summary=[['Kesimpulan','8/10 pasangan memenuhi batas atas BCa95 satu sisi <0,90; validitas diskriminan seluruh model belum terdukung pada kriteria ini.'],['EXP–PP','HTMT0,859509576; batas atas BCa 95=0,908138993, belum memenuhi<0,90.'],['EXP–AD','HTMT0,828421715; batas atas BCa 95=0,912789404, belum memenuhi<0,90.'],['Metode','Native SmartPLS 4.1.2.1, 10.000 bootstrap, BCa, One-tailed, alpha 0,05, Complete.'],['Konsistensi','Estimasi HTMT cocok dengan CSV; data mentah dalam ekspor sama dengan run native sebelumnya; keputusan<0,90 sama dengan PythonBC.'],['Perbedaan metode','Native BCa vs PythonBC; nilai interval tidak diharapkan identik.'],['Tahap selesai','PLS native dan bootstrap jalur dua sisi sudah diperiksa; pemeriksaan HTMT native satu sisi selesai.'],['Tahap berikutnya','Native PLSpredict/CVPAT belum tersedia; fit global terdahulu tetap perlu dicatat.'],['Berkas','Unggahan asli tidak diubah; ini workbook pembuktian baru.']]
tab('Ringkasan',['Bagian','Hasil'],summary)
fields=['pair','HTMT_native','HTMT_recomputed_CSV','point_abs_difference','native_BCa_upper95','native_PCT_upper95','BCa_upper95_below090','PCT_upper95_below090','BCa_upper95_below085','Python_BC_upper95','Python_PCT_upper95','delta_native_BCa_minus_Python_BC','classification_agrees_Python_BC090','native_source_BCa_upper95']
t=tab('HTMT_10_pasangan',fields,[[r[k] for k in fields] for r in rows])
for i,r in enumerate(rows,2):
 if not r['BCa_upper95_below090']:
  for c in t[i]:c.fill=PatternFill('solid',fgColor='FCE4D6')
tab('Pengaturan',['Pengaturan','Nilai'],list(settings.items())+list(meta.items()))
tab('Batasan',['Topik','Catatan'],[['Metode interval','Run dipilih BCa; tabel ekspor bernama Bias-corrected confidence intervals. BCa tidak disamakan dengan BC Python tanpa acceleration.'],['Header batas','5% dan 95% adalah dua batas yang ditampilkan dalam run satu sisi; gunakan batas atas 95% untuk kriteria. Jangan menyebut rentang5%–95% sebagai CI dua sisi 95%.'],['Rekonstruksi bootstrap','Native per-sample draws tidak tersimpan. Audit ini memverifikasi pengaturan dan klasifikasi interval dari ekspor; tidak mengklaim independen mereplikasi seluruh BCa native.'],['Keputusan','Tidak otomatis menghapus indikator atau mengubah konstruk agar ambang terpenuhi. Tinjau definisi teoritis dan isi item bila model perlu direvisi.'],['Kausalitas','Asosiasi jalur dan HTMT tidak membuktikan sebab-akibat.'],['Run jalur','Gunakan hasil two-tailed terdahulu untuk signifikansi jalur; jangan mengganti dengan run HTMT one-tailed.'],['Sumber dan kelayakan','Kecocokan271 baris tidak membuktikan penyaringan awal323→271 atau asal hash lama.']])
tab('Sumber',['Sumber','SHA256 / lokasi'],[['Native HTMT workbook',result['source_sha256']],['CSV271',result['CSV_sha256']],['BCa upper95','Complete data set!G480:G489'],['PCT upper95','Complete data set!F466:F475'],['Pengaturan','Complete data set!B689:C696']])
f=O/'KidSense_Verifikasi_HTMT_BCa_OneTailed.xlsx';out.save(f)
check=openpyxl.load_workbook(f,data_only=True);assert check['HTMT_10_pasangan'].max_row==11;assert sum(row[6] is True for row in list(check['HTMT_10_pasangan'].values)[1:])==8
text='''# Verifikasi HTMT native SmartPLS: satu sisi BCa

**Kesimpulan: 8 dari 10 pasangan memenuhi batas atas 95% <0,90.** Validitas diskriminan seluruh konstruk belum terdukung menurut kriteria ini. Pemeriksaan ekspor HTMT selesai; studi secara keseluruhan tetap memerlukan catatan fit global dan native prediction.

File mencatat SmartPLS 4.1.2.1, 10.000 bootstrap, Complete, BCa, one-tailed, alpha 0,05, Fixed seed. Header tabel terkoreksi memuat 5% dan 95%; nilai 95% pada kolom G dipakai sebagai batas atas satu sisi. Dua kolom tersebut bukan CI dua sisi 95%.

| Pasangan | HTMT | Batas atas BCa 95 native | Kriteria<0,90 |
|---|---:|---:|---|
'''
for r in rows:text+=f"| {r['pair']} | {r['HTMT_native']:.6f} | {r['native_BCa_upper95']:.6f} | {'Memenuhi' if r['BCa_upper95_below090'] else 'Belum memenuhi'} |\n"
text+='''
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
'''
(O/'KidSense_Hasil_HTMT_OneTailed.md').write_text(text)
print(json.dumps({k:v for k,v in result.items() if k not in ['pairs','limitations']},indent=2))
