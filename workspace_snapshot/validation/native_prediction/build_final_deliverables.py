from pathlib import Path
import json,hashlib,openpyxl,pandas as pd,numpy as np,zipfile
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
B=Path(__file__).resolve().parent;V=B.parent;O=B/'output';O.mkdir(exist_ok=True)
P=json.loads((B/'prediction/native_prediction_validation.json').read_text());D=json.loads((B/'data_integrity/native_prediction_data_integrity.json').read_text());C=json.loads((B/'native_cvpat_verification.json').read_text());S=json.loads((V/'native_bootstrap/native_structural_verification.json').read_text());M=json.loads((V/'native_bootstrap/measurement/native_measurement_verification.json').read_text());H=json.loads((V/'native_htmt_one_sided/verification.json').read_text())
w=openpyxl.Workbook();w.remove(w.active)
def sheet(name,headers,rows):
 s=w.create_sheet(name);s.append(list(headers))
 for row in rows:s.append(list(row))
 s.freeze_panes='A2';s.auto_filter.ref=s.dimensions;s.row_dimensions[1].height=36
 for c in s[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='164B63');c.alignment=Alignment(wrap_text=True)
 for row in s.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(c.value,float):c.number_format='0.0000000000'
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='EEF4F7')
 for i,col in enumerate(s.columns,1):s.column_dimensions[get_column_letter(i)].width=min(76,max(15,max(len(str(c.value or '')) for c in col)+2))
 return s
summary=[['Kesimpulan','Replikasi numerik native SmartPLS selesai untuk estimasi, bootstrap jalur, HTMT dan prediksi. Interpretasi model tetap memerlukan catatan.'],['Native PLSpredict','Direct antecedents; 10 folds × 10 repetitions; Fixed seed (angka seed tidak diekspor).'],['Q2_predict','8/8 positif; 0,294688580–0,474014919.'],['PLS vs LM RMSE','Lebih rendah pada 5/8 indikator. TR3, AD3 dan AD4 tidak lebih rendah.'],['PLS vs LM MAE','Lebih rendah pada 7/8 indikator; hanya AD4 tidak lebih rendah. Python lama 6/8; AD3 kini berubah.'],['CVPAT vs rata-rata indikator','Overall loss difference −0,365178844; p=3,925038e-10. PLS lebih baik secara signifikan dari IA.'],['CVPAT vs regresi linear','Overall loss difference −0,009950396; p=0,122338055. Keunggulan keseluruhan terhadap LM belum signifikan pada 0,05.'],['Verifikasi prediksi','21.680 galat indikator sama persis dengan observasi−prediksi. RMSE/MAE dihitung ulang cocok<2e-15. Fold native direkonstruksi dan model dihitung ulang; RMSE PLS cocok<5,5e-11.'],['Verifikasi CVPAT','22 tabel-baris uji: loss dan statistik t dihitung ulang, selisih maksimum3,8e-14; p native dipertahankan.'],['PLS struktural','62 estimasi titik lintas struktural/pengukuran/HTMT cocok<5e-10; empat jalur dan tiga indirect memiliki CI dua sisi tidak memuat nol.'],['HTMT','8/10 memenuhi batas atas BCa 95< 0,90; EXP–PP=0,908138993 dan EXP–AD=0,912789404 belum memenuhi.'],['Fit global','Estimated composite d_ULS dan d_G melampaui batas bootstrap95%/99% pada run sebelumnya; jangan mengklaim semua fit memadai.'],['Data','271 responden; 20 indikator; 5.420 nilai cocok. 2.710 prediksi per indikator adalah pengulangan 271 responden, bukan responden baru.'],['Batas prediksi','AD diprediksi dengan TR yang diamati (Direct antecedents), bukan hanya dari AIR/EXP/PP.'],['Belum diverifikasi','Seleksi awal 323 → 271, asal hash mentah lama, dan validitas/kausalitas substansial tidak dibuktikan oleh kecocokan perhitungan.'],['Berkas','Berkas sumber tidak diubah. Workbook ini adalah kompilasi hasil verifikasi, bukan ekspor asli SmartPLS.']]
sheet('Ringkasan_Final',['Bagian','Hasil'],summary)
fields=['indicator','Q2','RMSE_PLS','RMSE_LM','RMSE_IA','MAE_PLS','MAE_LM','MAE_IA','beats_LM_RMSE_native','beats_LM_MAE_native']
sheet('PLSpredict_native',fields,[[r[k] for k in fields] for r in P['indicators']])
fields=['indicator','RMSE_PLS','RMSE_PLS_custom','RMSE_PLS_native_minus_custom','MAE_PLS','MAE_PLS_custom','MAE_PLS_native_minus_custom','Q2','Q2_custom','Q2_native_minus_custom']
sheet('Prediksi_vs_Python_lama',fields,[[r[k] for k in fields] for r in P['indicators']])
fields=['indicator','PLS_RMSE_from_native_errors','RMSE_PLS','PLS_RMSE_error_summary_delta','PLS_MAE_from_native_errors','MAE_PLS','PLS_MAE_error_summary_delta','RMSE_PLS_independent_refit','RMSE_IA_independent_refit','RMSE_LM_independent_refit','Q2_independent_refit']
sheet('Prediksi_hitung_ulang',fields,[[r[k] for k in fields] for r in P['indicators']])
fields=['level','benchmark','target','native_PLS_loss','native_benchmark_loss','native_average_loss_difference','native_t','native_p','better_and_significant_005','source_row']
sheet('CVPAT_Konstruk',fields,[[r[k] for k in fields] for r in C['tests'] if r['level']=='construct'])
fields+=['indicator_LM_Holm_p']
sheet('CVPAT_Indikator',fields,[[r[k] for k in fields] for r in C['tests'] if r['level']=='indicator'])
fields=['level','benchmark','target','native_PLS_loss','recomputed_PLS_loss','native_benchmark_loss','recomputed_benchmark_loss','native_average_loss_difference','recomputed_average_loss_difference','native_t','recomputed_t','max_loss_or_t_abs_difference','native_p','scipy_t270_two_sided_p_check','p_abs_difference']
sheet('CVPAT_hitung_ulang',fields,[[r[k] for k in fields] for r in C['tests']])
sheet('Jalur_2_sisi',['Jalur','Beta','SE','t','p native','CI95 pct bawah','CI95 pct atas','Baris sumber'],[[k,r['O'],r['SE'],r['t'],r['p'],*r['ci95_percentile'],r['excel_row']] for k,r in S['paths'].items()])
sheet('Indirect_2_sisi',['Asosiasi','Beta','SE','t','p native','CI95 pct bawah','CI95 pct atas'],[[k,r['O'],r['SE'],r['t'],r['p'],*r['ci95_percentile']] for k,r in S['indirect'].items()])
sheet('R2',['Konstruk','R2','CI95 pct bawah','CI95 pct atas'],[[k,r['O'],*r['ci95_percentile']] for k,r in S['r2'].items()])
fields=['kind','entity','native','reference','abs_difference','native_cell']
sheet('Pengukuran_vs_Python',fields,[[r[k] for k in fields] for r in M['comparisons']])
sheet('rho_A_native',['Konstruk','rho_A','Status'],[[r['construct'],r['native_rho_A'],'Nilai native baru; belum direplikasi independen'] for r in M['rho_A_native_new']])
fields=['pair','HTMT_native','native_BCa_upper95','native_PCT_upper95','BCa_upper95_below090','Python_BC_upper95','classification_agrees_Python_BC090','native_source_BCa_upper95']
sheet('HTMT_BCa_1_sisi',fields,[[r[k] for k in fields] for r in H['pairs']])
fields=['metric','model','original','HI95','HI99','original_below_HI95','original_below_HI99','source_row']
sheet('Fit_native',fields,[[r[k] for k in fields] for r in S['fit']])
settings=D['settings'];print('Settings type',type(settings).__name__)
if isinstance(settings,dict):settings=list(settings.items())
else:settings=[[r.get('setting',r.get('name',str(r))),r.get('value')] for r in settings]
sheet('Pengaturan_prediksi',['Pengaturan','Nilai'],settings+list(D['metadata'].items()))
notes=[['Prediksi','Nilai RMSE/MAE ada dalam satuan indikator asli. Q²predict=1−RMSE_PLS²/RMSE_IA². Semua nilai prediksi asli dipertahankan.'],['Fold asli','Indeks kasus diekspor pada setiap galat/prediksi. Setiap271 baris adalah satu repetisi; fold pertama 28 kasus, sembilan fold berikutnya 27. Refit pada train/test tersebut mereproduksi prediksi native.'],['CVPAT loss','Loss adalah kuadrat galat indikator. Loss konstruk adalah rata-rata empat indikator; Overall rata-rata delapan indikator. Ini berbeda dari kuadratRMSE latent-score PLSpredict.'],['CVPAT t','Loss difference2.710 baris direkonstruksi. Statistik native cocok dengan|mean(delta)|/sqrt(var_population(delta)/271). Jumlah efektif menggunakan271 responden.'],['CVPAT p','Nilai p native dipertahankan. Cek numerik scipy t(df270) memberikan keputusan0,05 sama; selisih maksimum p3,5e-8 tidak diganti atau dianggap perbedaan inferensi.'],['Uji indikator','AD1 dan TR4 signifikan vsLM pada 0,05 tanpa penyesuaian. Holm delapan perbandingan indikator LM tambahan hanya menyisakan AD1. Kesimpulan utama memakai Overall, bukan memilih indikator signifikan.'],['RNG','Fixed seed tidak mengekspor angka/algoritma RNG. Fold asli diperoleh dari indeks yang diekspor, bukan menebak seed.'],['Hipotesis','Signifikansi jalur tetap mengacu pada run dua sisi. HTMT mengacu pada runBCa satu sisi. Python lama BC tanpa acceleration tetap berlabel berbeda.'],['Interpretasi','Keunggulan terhadap prediksi mean tidak membuktikan keunggulan signifikan terhadap regresi linear. CVPAT tidak membuktikan model sudah valid secara kausal atau diskriminan.'],['Pelestarian','Semua unggahan asli tetap utuh; ini ringkasan audit terpisah.']]
sheet('Metode_dan_batasan',['Topik','Catatan'],notes)
sources=[['Native PLSpredict10x10',C['source_sha256'],'Complete data set!B12:I19;B70:G79;B86:G105'],['Native bootstrap dua sisi',S['source_sha256'],'Complete data set!B12:G31;B66:G82'],['Native HTMTBCa satu sisi',H['source_sha256'],'Complete data set!B480:G489'],['CSV271',D['csv_sha256'],'271×20 nilai asli']]
sheet('Sumber',['Sumber','SHA256','Lokasi relevan'],sources)
f=O/'KidSense_Replikasi_SmartPLS4_Final.xlsx';w.save(f)
ww=openpyxl.load_workbook(f,data_only=True);assert ww['PLSpredict_native'].max_row==9;assert ww['CVPAT_Konstruk'].max_row==7;assert ww['CVPAT_Indikator'].max_row==17
assert not [(ss.title,c.coordinate) for ss in ww for row in ss for c in row if c.data_type=='e']
manifest={'files':[{'source':r[0],'sha256':r[1]} for r in sources],'native_prediction_settings':D['settings'],'verification':{'indicator_error_values_exact':21680,'native_fold_refit_max_PLS_RMSE_diff':P['max_refitted_PLS_RMSE_difference'],'CVPAT_loss_t_max_abs_diff':C['max_loss_or_t_absolute_difference'],'CVPAT_p_check_max_abs_diff':C['max_p_numeric_crosscheck_difference']},'overall_status':'Numerical replication complete within available exports; interpretive caveats retained.','original_source_files_modified':False}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
# Persist reader-facing result and final scoped validation handoff.
md=(B/'report_template.md').read_text()
pred_table='| Indikator | Q²_predict | RMSE PLS | RMSE LM | PLS lebih rendah? |\n|---|---:|---:|---:|---|\n'
for r in sorted(P['indicators'],key=lambda r:(r['indicator'].startswith('AD'),r['indicator'])):
 pred_table+=f"| {r['indicator']} | {r['Q2']:.6f} | {r['RMSE_PLS']:.6f} | {r['RMSE_LM']:.6f} | {'Ya' if r['beats_LM_RMSE_native'] else 'Tidak'} |\n"
cv_table='| Pembanding | Unit | Average loss difference | p native | Keputusan pada α = 0,05 |\n|---|---|---:|---:|---|\n'
for r in C['tests']:
 if r['level']=='construct':cv_table+=f"| {r['benchmark']} | {r['target']} | {r['native_average_loss_difference']:.6f} | {r['native_p']:.6g} | {'PLS lebih baik signifikan' if r['better_and_significant_005'] else 'Keunggulan belum signifikan'} |\n"
md=md.replace('{{PREDICTION_TABLE}}',pred_table.rstrip()).replace('{{CVPAT_TABLE}}',cv_table.rstrip())
(O/'KidSense_Laporan_Replikasi_Final.md').write_text(md)
print(json.dumps({'workbook':str(f),'sheets':w.sheetnames,'overall_CVPAT_LM_p':C['overall_LM']['native_p'],'prediction_RMSE_wins':P['RMSE_wins_LM_native'],'prediction_MAE_wins':P['MAE_wins_LM_native']},indent=2))
