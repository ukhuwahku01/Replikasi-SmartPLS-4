from pathlib import Path
import json,hashlib,re,zipfile
import numpy as np,pandas as pd,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches,Pt,Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
B=Path(__file__).resolve().parent;V=B.parent;O=B/'output';F=O/'figures';F.mkdir(parents=True,exist_ok=True)
S=json.loads((V/'native_bootstrap/native_structural_verification.json').read_text());M=json.loads((V/'native_bootstrap/measurement/native_measurement_verification.json').read_text());H=json.loads((V/'native_htmt_one_sided/verification.json').read_text());P=json.loads((V/'native_prediction/prediction/native_prediction_validation.json').read_text());C=json.loads((V/'native_prediction/native_cvpat_verification.json').read_text());D=json.loads((B/'measurement/measurement_diagnostics.json').read_text());R=json.loads((B/'structural/structural_restriction_diagnostics.json').read_text())
# Figures retain reviewed native values. Independent diagnostic outputs are separately labelled.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':13,'axes.labelsize':10,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(8.6,5.4));pairs=H['pairs'];yy=np.arange(len(pairs));points=np.array([r['HTMT_native'] for r in pairs]);upp=np.array([r['native_BCa_upper95'] for r in pairs]);colors=np.where(upp<.9,'#245A81','#B56528')
for y,p,u,c in zip(yy,points,upp,colors):ax.plot([p,u],[y,y],color=c,lw=1.8);ax.scatter(p,y,s=33,facecolors='white',edgecolors=c,zorder=3);ax.scatter(u,y,s=40,marker='D',color=c,zorder=3);ax.text(.964,y,f'{u:.3f}',ha='right',va='center',fontsize=9,color=c)
ax.axvline(.9,color='#343A40',ls='--',lw=1.2,label='Ambang 0,90');ax.set_yticks(yy,[r['pair'].replace('-','–') for r in pairs]);ax.invert_yaxis();ax.set_xlim(.67,.975);ax.set_xlabel('HTMT: estimasi titik dan batas atas satu sisi 95%');ax.set_title('Dua pasangan melampaui ambang batas atas HTMT',pad=30);ax.grid(axis='x',color='#E2E6E9',lw=.7);ax.set_axisbelow(True)
for x in ['top','right']:ax.spines[x].set_visible(False)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],marker='o',markerfacecolor='white',markeredgecolor='#245A81',color='none',label='Estimasi HTMT'),Line2D([0],[0],marker='D',color='none',markerfacecolor='#245A81',markeredgecolor='#245A81',label='Batas atas BCa 95%'),Line2D([0],[0],color='#343A40',ls='--',label='Ambang 0,90')],loc='upper center',bbox_to_anchor=(.5,1.03),ncol=3,frameon=False,fontsize=8)
fig.tight_layout();fig.savefig(F/'HTMT_native_upper95.png',dpi=220,bbox_inches='tight');fig.savefig(F/'HTMT_native_upper95.svg',bbox_inches='tight');plt.close(fig)
rows=sorted(P['indicators'],key=lambda r:(r['indicator'].startswith('AD'),r['indicator']));delta=np.array([r['RMSE_PLS']-r['RMSE_LM'] for r in rows]);fig,ax=plt.subplots(figsize=(8.6,4.9));yy=np.arange(8);cc=np.where(delta<0,'#245A81','#B56528');ax.barh(yy,delta,color=cc,height=.62);ax.axvline(0,color='#343A40',lw=1);ax.set_yticks(yy,[r['indicator'] for r in rows]);ax.invert_yaxis();ax.set_xlim(-.031,.013)
for y,v in zip(yy,delta):ax.text(v-.0005 if v<0 else v+.0005,y,f'{v:+.4f}',ha='right' if v<0 else 'left',va='center',fontsize=9)
ax.set_xlabel('RMSE PLS − RMSE LM (satuan indikator asli)');ax.set_title('PLS memiliki RMSE lebih rendah pada lima indikator');ax.grid(axis='x',color='#E2E6E9',lw=.7);ax.set_axisbelow(True)
for x in ['top','right']:ax.spines[x].set_visible(False)
fig.text(.12,.015,'Negatif: galat PLS lebih rendah. CVPAT Overall vs LM: p = 0,122338.',fontsize=9,color='#343A40');fig.tight_layout(rect=[0,.055,1,1]);fig.savefig(F/'RMSE_delta_native.png',dpi=220,bbox_inches='tight');fig.savefig(F/'RMSE_delta_native.svg',bbox_inches='tight');plt.close(fig)
# Tables for publication, retaining exact data in workbook.
wb=openpyxl.Workbook();wb.remove(wb.active)
def tab(name,heads,rows):
 t=wb.create_sheet(name);t.append(heads)
 for r in rows:t.append(list(r))
 t.freeze_panes='A2';t.auto_filter.ref=t.dimensions;t.row_dimensions[1].height=34
 for c in t[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='164B63');c.alignment=Alignment(wrap_text=True)
 for row in t.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(c.value,float):c.number_format='0.000000'
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='EEF4F7')
 for i,col in enumerate(t.columns,1):t.column_dimensions[get_column_letter(i)].width=min(78,max(15,max(len(str(c.value or '')) for c in col)+2))
 return t
ready=[['Replikasi numerik','Selesai','PLS, bootstrap jalur, HTMT dan prediksi native telah diperiksa.'],['Pelaporan hasil','Draf disiapkan','Nama konstruk lengkap dan isi kuesioner belum tersedia; singkatan dipertahankan.'],['Model pengukuran','Perlu peninjauan','Reliabilitas/AVE dan loading memadai secara deskriptif; HTMT inferensial EXP–PP serta EXP–AD belum memenuhi ambang0,90.'],['Spesifikasi struktural','Perlu peninjauan','Sisa asosiasi skor konstruk dengan AD setelah kontrol TR; ini diagnostik, bukan bukti jalur kausal.'],['Prediksi','Keunggulan terbatas','CVPAT signifikan terhadap IA; terhadap LM Overall p0,122338.'],['Revisi model','Belum ditetapkan','Memerlukan definisi konstruk, isi item, serta dasar teori. Model utama dan semua indikator dipertahankan.'],['Publikasi','Draf teknis untuk ditinjau','Belum merupakan naskah final atau mengikuti template jurnal tertentu.']]
tab('Kesiapan',['Aspek','Status','Bukti / kebutuhan'],ready)
rel=[]
for n in ['AIR','EXP','PP','TR','AD']:
 val={r['kind']:r['native'] for r in M['comparisons'] if r['entity']==n};ra=next(r['native_rho_A'] for r in M['rho_A_native_new'] if r['construct']==n);ld=[r['native'] for r in M['comparisons'] if r['kind']=='loading' and r['entity'].endswith('<- '+n)]
 # Field names vary; alpha/rho_c/AVE preserve exact JSON keys.
 rel.append([n,val,ra,min(ld),max(ld)])
print('Reliability kinds:',[r[1] for r in rel])
reliability=[]
for n,v,ra,lmin,lmax in rel:
 alpha=next(v[k] for k in v if 'alpha' in k.lower());rho=next(v[k] for k in v if 'rho' in k.lower());ave=next(v[k] for k in v if 'ave' in k.lower());reliability.append([n,alpha,ra,rho,ave,lmin,lmax])
tab('Tabel_Pengukuran',['Konstruk','Alpha standardized','rho_A native','rho_C','AVE','Loading min','Loading max'],reliability)
tab('Tabel_Jalur',['Jalur','Beta','SE native','t native','p native','CI95 percentile bawah','CI95 percentile atas'],[[k,r['O'],r['SE'],r['t'],r['p'],*r['ci95_percentile']] for k,r in S['paths'].items()])
tab('Tabel_Indirect',['Asosiasi tidak langsung','Beta','p native','CI95 bawah','CI95 atas','Batas interpretasi'],[[k,r['O'],r['p'],*r['ci95_percentile'],'Asosiasi tidak langsung; bukan uji mediasi penuh/parsial'] for k,r in S['indirect'].items()])
tab('Tabel_HTMT',['Pasangan','HTMT','Batas atas BCa95 native','Memenuhi <0.90'],[[r['pair'],r['HTMT_native'],r['native_BCa_upper95'],r['BCa_upper95_below090']] for r in H['pairs']])
tab('Tabel_Prediksi',['Indikator','Q2_predict','RMSE PLS','RMSE LM','MAE PLS','MAE LM'],[[r[k] for k in ['indicator','Q2','RMSE_PLS','RMSE_LM','MAE_PLS','MAE_LM']] for r in rows])
tab('Tabel_CVPAT',['Benchmark','Unit','Loss PLS','Loss benchmark','Selisih','p native'],[[r[k] for k in ['benchmark','target','native_PLS_loss','native_benchmark_loss','native_average_loss_difference','native_p']] for r in C['tests'] if r['level']=='construct'])
cl=D['crossloadings'];keys=['indicator','assigned_construct']+[f'corr_{n}' for n in ['AIR','EXP','PP','TR','AD']]+['highest_other_construct','own_minus_highest_other_abs'];tab('Crossloading_diagnostik',keys,[[r[k] for k in keys] for r in cl])
tab('FL_deskriptif',['Pasangan','Korelasi skor','sqrtAVE A','sqrtAVE B','Memenuhi deskriptif','Catatan'],[[r['pair'],r['latent_corr'],r['sqrtAVE_a'],r['sqrtAVE_b'],r['passes_descriptive_FL'],'Tidak menggantikan HTMT inferensial'] for r in D['fornell_larcker_pairs']])
keys=['construct','observed_corr_X_AD','implied_corr_X_AD_under_restricted_model','observed_minus_implied','partial_corr_X_AD_controlling_only_TR'];tab('Restriksi_AD_diagnostik',keys,[[r[k] for k in keys] for r in R['diagnostics']])
keys=['construct_pair','item_a','item_b','pearson_r'];tab('Korelasi_item_tinjauan',keys,[[r[k] for k in keys] for r in D['highest_cross_item_pairs']])
plan=[['Pertahankan model utama','Simpan M0 sebagai hasil asli yang sudah diverifikasi.','Tidak ada data atau indikator yang diubah.'],['Tinjau isi konstruk','Periksa definisi EXP, PP, AD dan item terkait kesamaan konsep/frasa/konteks.','Definisi konstruk dan teks kuesioner diperlukan.'],['Tinjau hubungan langsung','Evaluasi apakah teori memang mendukung efek langsung konstruk awal terhadap AD, di samping TR.','Korelasi parsial tidak cukup untuk menetapkan jalur baru.'],['Jika revisi didukung','Nyatakan model alternatif dan alasan substantif sebelum menghitungnya; simpan sebagai analisis tambahan.','Jangan menimpa M0; bedakan eksploratori dari konfirmatori.'],['Evaluasi ulang','Estimasi pengukuran, HTMT, fit, bootstrap direct/indirect, dan prediksi untuk spesifikasi yang dibenarkan.','Model yang dipilih dengan data yang sama tetap membutuhkan validasi lebih lanjut.'],['Laporkan lengkap','Sertakan keputusan HTMT dan CVPAT yang belum mendukung klaim kuat.','Jangan mengubah ambang atau memilih metrik hanya agar hasil tampak lolos.']]
tab('Rencana_tindak_lanjut',['Tahap','Tindakan','Batas / prasyarat'],plan)
wb.save(O/'KidSense_Tahap_Lanjut_Diagnostik.xlsx')
# Narrative: technically reviewable, with abbreviations and no invented questionnaire concepts.
text='''# Draf hasil dan peninjauan model KidSense

**Status: draf teknis untuk ditinjau.** Hasil numerik dapat dilaporkan, tetapi naskah belum dapat menyatakan bahwa seluruh konstruk terpisah secara diskriminan, seluruh fit memadai, atau PLS mengungguli regresi linear secara signifikan. Kepanjangan konstruk dan teks kuesioner belum tersedia; singkatan AIR, EXP, PP, TR, dan AD dipertahankan.

## Ringkasan keputusan

Replikasi SmartPLS selesai. Tahap berikutnya adalah meninjau dasar pengukuran dan spesifikasi model sebelum memperkuat kesimpulan atau merevisi model. EXP–PP dan EXP–AD belum memenuhi kriteria HTMT batas atas95%<0,90. Prediksi mengungguli benchmark rata-rata indikator, tetapi belum menunjukkan keunggulan keseluruhan yang signifikan atas regresi linear. Diagnostik baru menunjukkan seluruh20 indikator memiliki loading tertinggi pada konstruk asalnya, sementara asosiasi EXP–AD masih tersisa setelah kontrol TR saja.

## Draf bagian metode analisis

Analisis menggunakan 271 observasi dan20 indikator yang membentuk lima konstruk reflektif. Model memuat jalur AIR→TR, EXP→TR, PP→TR, serta TR→AD. Estimasi native dilakukan dengan SmartPLS4.1.2.1, path weighting, hasil terstandardisasi, initial weight1, maksimum3000 iterasi dan stopping criterion10⁻⁷. Pengaturan outer weighting tercatat AUTOMATIC; perhitungan independen ModeA mereproduksi estimasi titiknya.

Inferensi jalur dan asosiasi tidak langsung menggunakan10.000bootstrap, uji dua sisi padaα0,05, serta interval percentile95%. Validitas diskriminan dinilai menggunakan HTMT dan batas atas BCa95% satu sisi terhadap ambang0,90. BCa native dibedakan dari BC tanpaacceleration pada perhitunganPython sebelumnya. Prediksi diuji dengan PLSpredict/CVPAT,10folds×10repetitions, Directantecedents, danFixedseed. Angka seed native tidak diekspor. Untuk AD, informasiTR yang diamati digunakan sebagai anteseden langsung, sehingga hasil prediksi bersifat kondisional.

Bagian metode mengenai rekrutmen, persetujuan, kriteria inklusi dan eksklusi323→271 harus diisi dari bukti sumber yang belum tersedia. DataCSV271 tidak memuat flag tersebut.

## Draf hasil pengukuran

Loading indikator berada pada rentang0,801232–0,859317. Alpha standardized berada pada0,840120–0,879011, rho_C0,892680–0,916747, dan AVE0,675347–0,733542. Nilai rho_A native berada pada0,845098–0,880280; nilai ini belum dihitung ulang secara independen. Temuan tersebut mendukung konsistensi internal dan konvergensi secara deskriptif, dengan validitas diskriminan yang masih memerlukan catatan.

Seluruh estimasi titik HTMT berada di bawah0,90. Namun, batas atasBCa95% untuk EXP–PP sebesar0,908139 dan EXP–AD sebesar0,912789 tidak memenuhi kriteria<0,90. Delapan pasangan lainnya memenuhi. Karena itu, validitas diskriminan belum terdukung untuk seluruh pasangan menurut kriteria yang ditetapkan. Ini bukan bukti bahwa HTMT populasi kedua pasangan pasti lebih dari0,90; interval yang tersedia belum cukup menetapkannya di bawah ambang.

![Estimasi HTMT dan batas atas satu sisi](figures/HTMT_native_upper95.png)

Gambar1. Lingkaran menunjukkan estimasi HTMT dan wajik menunjukkan batas atasBCa95% satu sisi; garis penghubung bukan interval dua sisi. Data berasal dari ekspor native HTMT.

## Draf hasil struktural

Keempat asosiasi langsung positif dan memiliki interval bootstrap95% dua sisi yang tidak memuat nol: AIR→TR β0,260379 [0,139482;0,380324], EXP→TR β0,293921 [0,157908;0,425392], PP→TR β0,315452 [0,164208;0,465164], serta TR→AD β0,687964 [0,603460;0,764247]. Semua p native<0,001. R²TR=0,616399 dan R²AD=0,473295.

Asosiasi tidak langsung AIR→TR→AD sebesar0,179132 [0,095343;0,266555], EXP→TR→AD sebesar0,202207 [0,103184;0,307668], dan PP→TR→AD sebesar0,217019 [0,113304;0,322550]. Ketiga interval tidak memuat nol. Hasil ini mendukung asosiasi tidak langsung dalam model, bukan pembuktian sebab-akibat. Model tidak mengestimasi jalur langsung AIR/EXP/PP→AD, sehingga hasilnya belum dapat diklasifikasikan sebagai mediasi penuh atau parsial.

## Draf hasil prediksi

Seluruh delapan Q²_predict positif, dengan rentang0,294689–0,474015. PLS memiliki RMSE lebih rendah daripada LM pada5/8 indikator, dan MAE lebih rendah pada7/8 indikator. CVPAT Overall menunjukkan loss lebih rendah signifikan dibanding rata-rata indikator (selisih−0,365179; p3,925×10⁻¹⁰), tetapi keunggulan terhadap LM belum signifikan (selisih−0,009950; p0,122338). Tidak menolak hipotesis terhadap LM tidak membuktikan kedua model setara.

![Selisih RMSE native](figures/RMSE_delta_native.png)

Gambar2. Selisih negatif menunjukkan RMSE PLS lebih rendah daripada LM. Perbandingan perindikator tidak menggantikan hasil CVPAT Overall.

## Fit dan diagnostik baru

Pada estimatedcompositemodel, d_ULS0,862615 melewati HI950,368764 dan d_G0,190185 melewati HI950,168519. SRMR0,064091 berada di bawah patokan deskriptif0,08, tetapi melewati batas bootstrap HI95. Sebaliknya, saturatedcompositemodel berada di bawah batas bootstrap terkait. Perbedaan ini memberi alasan meninjau pembatasan struktur; tidak menunjukkan dengan pasti jalur atau item mana yang perlu diubah, dan tidak membuktikan seluruh pengukuran sudah benar.

Diagnostik tambahan dihitung diPython dari model awal yang estimasi titiknya cocok dengan native. Seluruh20 indikator memiliki loading tertinggi pada konstruk asalnya; margin minimum terhadap crossloading tertinggi lainnya0,190707. Seluruh10 pasangan memenuhi Fornell–Larcker secara deskriptif. Kedua pemeriksaan tersebut tidak menggantikan HTMT inferensial yang telah ditetapkan.

Berdasarkan skor komposit, korelasi EXP–AD teramati0,701494, sedangkan implikasi pembatasan EXP→TR→AD adalah0,489623; selisih0,211870. Korelasi parsial EXP–AD setelah mengontrol TR saja sebesar0,415575. Nilai yang setara untuk AIR dan PP adalah0,247018 dan0,319697. Ini adalah sisa asosiasi linear pada sampel yang sama, bukan koefisien jalur langsung yang dikontrol simultan atau bukti kausal.

Korelasi antaritem tertinggi pada dua pasangan yang perlu ditinjau antara lain EXP2–PP4 (r0,602603), EXP3–PP4 (r0,569708), dan EXP4–AD3 (r0,532271). Angka ini hanya memprioritaskan pemeriksaan isi item; tanpa teks item, kesamaan makna atau sumber overlap belum dapat ditentukan.

## Draf pembahasan yang proporsional

Model menunjukkan asosiasi positif dengan TR dan hubungan positif TR dengan AD. Replikasi numerik lintas perhitungan memberi dukungan terhadap ketepatan hasil komputasi. Namun, inferensi substantif dibatasi oleh ketidakpastian diskriminasi EXP terhadap PP/AD dan fit spesifikasi yang belum seluruhnya memadai. Temuan prediksi juga menunjukkan manfaat terhadap benchmark sederhana, dengan keunggulan keseluruhan atas regresi linear yang belum signifikan. Karena itu, kontribusi model perlu dijelaskan melalui teori serta pola asosiasi yang teramati, tanpa mengklaim superioritas prediktif yang belum didukung atau sebab-akibat.

## Rencana sebelum revisi atau finalisasi naskah

1. Lengkapi definisi AIR, EXP, PP, TR, AD serta teks itemEXP1–EXP4, PP1–PP4 dan AD1–AD4. Gunakan untuk menilai pembedaan konsep dan isi pengukuran.
2. Pertahankan model awal sebagai hasil utama yang telah diverifikasi. Tidak ada indikator atau kasus yang dihapus.
3. Bila teori mendukung jalur tambahan, tetapkan alasan serta model alternatif sebelum estimasi dan laporkan sebagai analisis tambahan. Menambah semua jalur langsung dapat melonggarkan pembatasan model secara mekanis; perbaikan fit saja tidak membuktikan model lebih benar.
4. Bila revisi pengukuran didukung isi item dan teori, laporkan alasan secara transparan. Modifikasi berbasis data yang sama bersifat eksploratori dan perlu validasi lebih lanjut.
5. Ulangi pemeriksaan relevan pada model alternatif yang dibenarkan: loadings/reliabilitas, HTMT, direct/indirect, fit, dan prediksi. Jangan mengganti ambang atau memilih metrik untuk menyembunyikan hasil yang tidak mendukung.
6. Isi bukti penyaringan data323→271 dari sumber asli. Terapkan template jurnal dan rincian naskah setelah informasi tersebut tersedia.

## Sumber dan cakupan

Tabel native berasal dari tiga ekspor pengguna: bootstrap jalur dua sisi, HTMT BCa satu sisi, dan PLSpredict10×10. Diagnostik crossloading, Fornell–Larcker, korelasi antaritem, dan restriksi skor komposit merupakan perhitunganPython tambahan yang diberi label eksploratori. Semua angka presisi penuh dan sumber sel ada dalam workbook serta JSON diagnostik. Tidak ada hasil native yang diubah dan tidak ada keputusan revisi model yang diterapkan.
'''
# Improve readability of intentionally compact metric strings in draft; numeric values remain unchanged.
repl={'seluruh20':'seluruh 20','Seluruh20':'Seluruh 20','dan20':'dan 20','SmartPLS4.1.2.1':'SmartPLS 4.1.2.1','weight1':'weight 1','maksimum3000':'maksimum 3000','criterion10⁻⁷':'criterion 10⁻⁷','ModeA':'Mode A','menggunakan10.000bootstrap':'menggunakan 10.000 bootstrap','padaα0,05':'pada α 0,05','percentile95%':'percentile 95%','BCa95%':'BCa 95%','ambang0,90':'ambang 0,90','tanpaacceleration':'tanpa acceleration','perhitunganPython':'perhitungan Python','10folds×10repetitions':'10 folds × 10 repetitions','Directantecedents':'Direct antecedents','danFixedseed':'dan Fixed seed','informasiTR':'informasi TR','eksklusi323→271':'eksklusi 323 → 271','DataCSV271':'Data CSV 271','rentang0,':'rentang 0,','pada0,':'pada 0,','rho_C0,':'rho_C 0,','AVE0,':'AVE 0,','bawah0,':'bawah 0,','sebesar0,':'sebesar 0,','kriteria<':'kriteria <','dari0,':'dari 0,','Gambar1':'Gambar 1','Gambar2':'Gambar 2','atasBCa':'atas BCa','bootstrap95%':'bootstrap 95%','β0,':'β 0,','p native<':'p native <','R²TR':'R² TR','R²AD':'R² AD','pada5/8':'pada 5/8','pada7/8':'pada 7/8','selisih−':'selisih −','p3,925':'p = 3,925','p0,122338':'p = 0,122338','perindikator':'per indikator','estimatedcompositemodel':'estimated composite model','saturatedcompositemodel':'saturated composite model','d_ULS0,':'d_ULS 0,','HI950,':'HI95 0,','d_G0,':'d_G 0,','SRMR0,':'SRMR 0,','diPython':'di Python','lainnya0,':'lainnya 0,','Seluruh10':'Seluruh 10','teramati0,':'teramati 0,','adalah0,':'adalah 0,','selisih0,':'selisih 0,','r0,':'r = 0,','itemEXP':'item EXP','data323→271':'data 323 → 271','PLSpredict10×10':'PLSpredict 10 × 10','atas95%':'atas 95%','seluruh20':'seluruh 20','Seluruh20':'Seluruh 20','di bawah0,90':'di bawah 0,90','TR saja sebesar0,':'TR saja sebesar 0,','perhitunganPython':'perhitungan Python'}
for a,b in repl.items():text=text.replace(a,b)
text+='\nSitasi software sebagaimana tercantum dalam ekspor: Ringle, C. M., Wende, S., dan Becker, J.-M. (2024). SmartPLS 4. Bönningstedt: SmartPLS. https://www.smartpls.com.\n'
(O/'KidSense_Draf_Hasil_dan_Peninjauan_Model.md').write_text(text)
# Editable Word draft with figures and key manuscript tables.
doc=Document();sec=doc.sections[0];sec.top_margin=Cm(2);sec.bottom_margin=Cm(2);sec.left_margin=Cm(2.2);sec.right_margin=Cm(2.2)
styles=doc.styles
for name in ['Normal','Body Text']:styles[name].font.name='Calibri';styles[name].font.size=Pt(10.5)
styles['Normal'].paragraph_format.space_after=Pt(6)
for n in ['Title','Heading 1','Heading 2']:styles[n].font.name='Calibri';styles[n].font.color.rgb=__import__('docx').shared.RGBColor.from_string('164B63')
# Footer page number.
p=sec.footer.paragraphs[0];p.alignment=2;run=p.add_run('KidSense — draf teknis | ');run.font.size=Pt(8);fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');p._p.append(fld)
for line in text.splitlines():
 line=line.strip()
 if not line:continue
 if line.startswith('# '):doc.add_heading(line[2:],0)
 elif line.startswith('## '):doc.add_heading(line[3:],1)
 elif line.startswith('!['):
  path=re.search(r'\]\((.+)\)',line).group(1);doc.add_picture(str(O/path),width=Cm(16));doc.paragraphs[-1].paragraph_format.keep_with_next=True
 elif re.match(r'^\d+\. ',line):doc.add_paragraph(re.sub(r'^\d+\. ','',line),style='List Number')
 else:doc.add_paragraph(line.replace('**',''))
# Supplement with exact, compact tables.
doc.add_page_break();doc.add_heading('Tabel pelaporan utama',1)
def word_table(title,heads,values):
 doc.add_heading(title,2);t=doc.add_table(rows=1,cols=len(heads));t.style='Light Shading Accent 1'
 for c,h in zip(t.rows[0].cells,heads):c.text=h
 for row in values:
  cells=t.add_row().cells
  for c,v in zip(cells,row):c.text=str(v)
 for row in t.rows:
  for cell in row.cells:
   for p in cell.paragraphs:
    for r in p.runs:r.font.size=Pt(8.5)
 return t
word_table('Pengukuran',['Konstruk','α std.','rho_A','rho_C','AVE','Loading'],[[r[0],*[f'{v:.3f}' for v in r[1:5]],f'{r[5]:.3f}–{r[6]:.3f}'] for r in reliability])
word_table('Jalur struktural',['Jalur','β','SE','CI95 percentile','p'],[[k.replace(' -> ','→'),f"{r['O']:.3f}",f"{r['SE']:.3f}",f"{r['ci95_percentile'][0]:.3f}–{r['ci95_percentile'][1]:.3f}",'<0,001'] for k,r in S['paths'].items()])
word_table('HTMT',['Pasangan','HTMT','Atas BCa95','<0,90'],[[r['pair'],f"{r['HTMT_native']:.3f}",f"{r['native_BCa_upper95']:.3f}",'Ya' if r['BCa_upper95_below090'] else 'Belum'] for r in H['pairs']])
doc.save(O/'KidSense_Draf_Hasil_dan_Peninjauan_Model.docx')
# Input/source manifest and coverage of new diagnostics.
manifest={'stage':'Model adequacy diagnostics and manuscript results draft','native_sources':[{'file':S['source_file'],'sha256':S['source_sha256']},{'file':H['source'],'sha256':H['source_sha256']},{'file':C['source'],'sha256':C['source_sha256']}],'new_diagnostics':['Crossloadings and Fornell-Larcker descriptive check','Cross-construct item correlations for EXP-PP and EXP-AD','Composite-score restriction gaps and partial correlations controlling only TR'],'original_model_modified':False,'theory_input_missing':['Full construct names','Definitions and item wording for EXP/PP/AD'],'journal_template_applied':False,'own_loadings_highest':D['crossloadings_own_highest_count'],'FL_pairs_pass_descriptive':sum(r['passes_descriptive_FL'] for r in D['fornell_larcker_pairs'])}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Created:',[p.name for p in O.iterdir()]);print('DOCX tables',len(doc.tables),'paragraphs',len(doc.paragraphs))
