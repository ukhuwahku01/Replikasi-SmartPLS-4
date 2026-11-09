from pathlib import Path
import json,math
import pandas as pd,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
B=Path(__file__).resolve().parent;O=B/'output';J=json.loads((B/'native_M1_verified.json').read_text());comp=pd.read_csv(B/'integrity/corrected_M1_point_comparisons.csv')
w=openpyxl.Workbook();w.remove(w.active)
def tab(name,heads,values):
 s=w.create_sheet(name);s.append(heads)
 for r in values:s.append(list(r))
 s.freeze_panes='A2';s.auto_filter.ref=s.dimensions;s.row_dimensions[1].height=35
 for c in s[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='164B63');c.alignment=Alignment(wrap_text=True)
 for row in s.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(c.value,float):c.number_format='0.0000000000'
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='EEF4F7')
 for i,col in enumerate(s.columns,1):s.column_dimensions[get_column_letter(i)].width=min(78,max(15,max(len(str(c.value or '')) for c in col)+2))
 for row in s.iter_rows(min_row=2):s.row_dimensions[row[0].row].height=min(240,14*max(max(1,math.ceil(len(str(c.value or ''))/(s.column_dimensions[c.column_letter].width*.9))) for c in row)+8)
 return s
summary=[['Status','Ekspor yang diperbaiki sesuai M1:5konstruk7jalur20indikator; penghitungan native bootstrap M1 kini dapat diperiksa.'],['Input','271×20 nilai dan urutan kasus identik dengan CSV asli.'],['Pengaturan','10.000,Complete,Percentile,Two-tailed,alpha0,05,Fixedseed.'],['Estimasi titik','32estimasi identik dengan algoritma native M1 sebelumnya dan cocok denganPython hingga1,00411e-10.'],['AD langsung','AIR belum signifikan(p0,505143); EXP(p0,000771),PP(p0,027921),TR(p0,00006969) signifikan pada taraf nominal0,05.'],['Indirect','Ketiga asosiasi melaluiTR memilikiCI95percentile tidak memuat0; psekitar0,005.'],['R2','AD0,575904;TR0,615656.'],['AIRtotal','Total p0,047521 denganCIpercentile tidak memuat0, tetapiCIcorrected memuat0; jangan menyamakan dengan efek langsungAIR.'],['Batas','M1posthoc; tidak membuktikan kausalitas atau validasi teori. HTMT belum terselesaikan; prediksi M1 belum diuji.'],['Perbaikan ekspor','Bootstrap sebelumnya tanpaTR tetap keluaran model lain dan tidak dipakai sebagai hasil M1.']]
tab('Ringkasan',['Aspek','Hasil'],summary)
fields=['effect','estimate','bootstrap_SE','t','p','CI95_percentile_low','CI95_percentile_high','CI_excludes_zero','source_row']
for name,rows in [('Jalur_native',J['paths'].values()),('Indirect_native',J['indirect'].values()),('Total_native',J['totals'].values()),('R2_native',J['r2'].values())]:tab(name,fields,[[r[k] for k in fields] for r in rows])
fields=['effect','CI95_percentile_low','CI95_percentile_high','BC_CI95_low','BC_CI95_high'];tab('Sensitivitas_interval',fields,[[r.get(k) for k in fields] for r in J['results'] if r['kind']!='r2'])
tab('32_estimasi_titik',list(comp.columns),comp.itertuples(index=False,name=None))
fields=['kind','effect','metric','native','Python_M1','abs_difference','comparison_type','source_row'];tab('Banding_bootstrap_Python',fields,[[r[k] for k in fields] for r in J['comparisons']])
fields=['metric','model','original','HI95','HI99','belowHI95','belowHI99','source_row'];tab('Fit_mixed_composite',fields,[[r[k] for k in fields] for r in J['fit']])
tab('Pengaturan',['Pengaturan','Nilai'],list(J['settings'].items())+list(J['metadata'].items()))
limits=[['Saturasi','Saturated/estimated fit sama karena struktur skor rekursif lengkap. Tidak mengonfirmasi jalur baru atau membuat seluruh model item tersaturasi.'],['Fit mixed vscomposite','Composite estimated berada di bawahHI95; mixed masih melewati beberapaHI95/HI99. Jangan menyatakan semua fit lolos hanya dariSRMR<0,08.'],['HTMT','HTMT current dua sisi identik denganM0. BatasBCa satu sisi95 sebelumnya tetap: EXP–PP0,908139 danEXP–AD0,912789.'],['M1prediksi','Belum ada PLSpredict/CVPATnativeM1. Hasil prediksiM0 tidak dipindahkan keM1.'],['Pembandingan prediksi','Jika membandingkan M0danM1, gunakan informasi prediktor yang setara danfold setara. Directantecedents M1 memberi AD lebih banyak informasi daripada M0.'],['Desain studi','Persepsi orang tua dari deskripsi/gambar; AD adalah niat hipotetis bersyarat. Tidak menyatakan pengalaman/adopsi aktual.'],['Mediasi','Laporkan asosiasi langsung/tidak langsung. AIRdirect tidak signifikan bukan bukti efek tepatnol atau mediasi kausal penuh.'],['p danbootstrap','p native dipertahankan; keputusan utama memakaiCIpercentile dua sisi yang dipilih. Tidak memilih interval hanya agar signifikan.']]
tab('Batas_dan_tindak_lanjut',['Topik','Catatan'],limits)
tab('Sumber',['File','SHA256','Lokasi'],[[J['source'],J['source_sha256'],'Complete data set:paths12–18,CI23–29,indirect75–77,CI82–84'],['Model asli','KidSense_M1_Eksploratori','Matriks inner/outer dan dataset271×20 telah diperiksa']])
f=O/'KidSense_M1_Native_Terverifikasi.xlsx';w.save(f)
md='''# Verifikasi bootstrap native M1 lengkap

**Status: perhitungan native M1 sesuai dan terverifikasi dalam cakupan ekspor.** Model tetap analisis sensitivitas posthoc; hasil ini tidak menghapus keterbatasan validitas konstruk, kausalitas, atau prediksi yang belum diuji.

Ekspor mencatat **KidSense_M1_Eksploratori**, SmartPLS4.1.2.1, lima konstruk,AIR/EXP/PP/TR/AD,20indikator reflektif,dan7jalur. Seluruh271×20nilai dan urutan kasus cocok denganCSV. Bootstrap memakai10.000,Complete,Percentile,Two-tailed,alpha0,05,Fixedseed. Nilai seed tidak tercatat dan per-sample results tidak disimpan.

Tiga puluh dua estimasi titik(7jalur,20loadings,2R²,3indirect) identik dengan algoritma native M1 yang benar. Perbandingan terhadapPythonM1 menunjukkan selisih maksimum1,00411×10⁻¹⁰. Semua keputusan CI utama sesuai denganPython; nilaiSE danCI tidak dipaksa identik antarRNG.

## Hasil jalur native

| Jalur | beta | SE | p native | CI95percentile |
|---|---:|---:|---:|---|
'''
for k,r in J['paths'].items():md+=f"| {k} | {r['estimate']:.6f} | {r['bootstrap_SE']:.6f} | {r['p']:.6g} | [{r['CI95_percentile_low']:.6f}; {r['CI95_percentile_high']:.6f}] |\n"
md+='''
AIR→AD langsung belum signifikan padaα0,05. EXP→AD,PP→AD,TR→AD,dan ketiga jalur menujuTR signifikan secara nominal. NonsignifikansiAIRdirect tidak membuktikan efek populasi tepatnol.

## Asosiasi tidak langsung

| Asosiasi melaluiTR | beta | p native | CI95percentile |
|---|---:|---:|---|
'''
for k,r in J['indirect'].items():md+=f"| {k} | {r['estimate']:.6f} | {r['p']:.6g} | [{r['CI95_percentile_low']:.6f}; {r['CI95_percentile_high']:.6f}] |\n"
md+='''
Ketiga CI tidak memuat nol. Secara statistik, terdapat dukungan bagi asosiasi tidak langsung melaluiTR dalam M1. UntukEXP/PP, asosiasi langsung dan tidak langsung sama-sama positif. Pola ini tidak membuktikan mediasi kausal, karena model bersifat posthoc pada data persepsi yang sama.

R²AD=0,575904 (CI95percentile0,460257–0,694855) danR²TR=0,615656(0,531243–0,701116). DibandingM0, R²AD meningkat secara deskriptif dari0,473295; jumlah parameter serta bobot komposit berubah, sehingga ini bukan bukti perbaikan model independen atau F-test nested dengan skor identik.

TotalasosiasiAIR→AD=0,125558,p0,047521,CIpercentile[0,002081;0,253714],sedangkan correctedCI[−0,002360;0,249998] memuatnol. Laporkan sensitivitas ini bila membahas totalAIR. Jangan menggabungkannya dengan efek langsungAIR0,045605,p0,505143 atau memilih interval yang paling mendukung.

## Fit dan batas interpretasi

Estimated dan saturated mempunyai SRMR,d_ULS,d_G yang sama secara numerik pada M1, sesuai saturasi bagian struktural skor. Ini bukan pengujian independen teori tambahan atau saturasi seluruh model indikator.

- **Composite estimated:**SRMR0,031026<HI950,034508;d_ULS0,202144<0,250075;d_G0,145440<0,164052.
- **Mixed estimated:**SRMR0,049034>HI950,044696;d_ULS0,504913>0,419530;d_G0,275551>0,274682. SRMRdan d_ULS juga melewatiHI99;d_G tidak melewatiHI99. Karena itu jangan menyatakan seluruhdiagnostikfit lolos.

HTMT pada file ini adalah dua sisi(2,5%/97,5%). Semua estimasi serta batasHTMT sama dengan runM0 dua sisi, sehingga penambahan jalur tidak mengubahnya. Kriteria nativeBCa satu sisi95% sebelumnya tetap belum terpenuhi untukEXP–PP(0,908139) danEXP–AD(0,912789).

M1nativePLSpredict/CVPAT belum tersedia. Hasil prediksiM0 tidak menjadi hasilM1. Untuk perbandingan model yang sepadan, informasi prediktor serta pembagianfold harus setara; Directantecedents M1 menggunakan lebih banyak anteseden langsungAD daripadaM0.

Penelitian tetap survei persepsi atas deskripsi/gambar rancangan. AD adalah niat hipotetis dan kondisional; hasil ini tidak membuktikan adopsi aktual, kinerjaAI, auditprivasi, atau kausalitas. M0dipertahankan sebagai baseline, M1sebagai analisis sensitivitas yang diberi label transparan.

## Cakupan pemeriksaan dan penyelesaian masalah ekspor

- Identitas model,7jalur,20indikator reflektif,271baris,dan semua5.420nilai diverifikasi.
- Seluruh32estimasi titik dibandingkan terhadap algoritma nativeM1 danPythonM1;15estimasi struktural/total/R² juga dibandingkan denganSE/CI bootstrapPython secara terpisah.
- Rasio t dihitung ulang dari|beta|/SE; indirect dari hasil kali koefisien terkait; total dari direct+indirect. Tidak ditemukan ketidaksesuaian aritmetika.
- Nativep dipertahankan dan tidak diklaim identik dengan pendekatanSciPy. Per-draw bootstrap native tidak dapat direkonstruksi dari ekspor karena tidak disimpan.
- Filebootstrap sebelumnya yang tanpaTR tetap keluaran model empat konstruk yang berbeda. Masalah itu kini terselesaikan oleh ekspor baru ini; statistik dari keduanya tidak digabung.

Sumber sel serta hash file ada di workbook,CSVdanJSON. Berkas unggahan asli tidak diubah. Verifikasi komputasi selesai; justifikasi model dan generalisasi tetap memerlukan batasan yang disebutkan.
'''
replace={'SmartPLS4.1.2.1':'SmartPLS 4.1.2.1','konstruk,AIR/EXP/PP/TR/AD,20indikator reflektif,dan7jalur':'konstruk (AIR, EXP, PP, TR, AD), 20 indikator reflektif, dan 7 jalur','Seluruh271×20nilai':'Seluruh 271 × 20 nilai','denganCSV':'dengan CSV','memakai10.000,Complete,Percentile,Two-tailed,alpha0,05,Fixedseed':'memakai 10.000, Complete, Percentile, Two-tailed, α = 0,05, Fixed seed','titik(7jalur,20loadings,2R²,3indirect)':'titik (7 jalur, 20 loadings, 2 R², 3 indirect)','terhadapPythonM1':'terhadap Python M1','maksimum1,00411':'maksimum 1,00411','denganPython':'dengan Python','nilaiSE danCI':'nilai SE dan CI','antarRNG':'antar RNG','CI95percentile':'CI95 percentile','padaα0,05':'pada α = 0,05','EXP→AD,PP→AD,TR→AD,dan':'EXP→AD, PP→AD, TR→AD, dan','menujuTR':'menuju TR','NonsignifikansiAIRdirect':'Nonsignifikansi AIR direct','tepatnol':'tepat nol','melaluiTR':'melalui TR','UntukEXP/PP':'Untuk EXP/PP','R²AD':'R² AD','danR²TR':'dan R² TR','DibandingM0':'Dibanding M0','dari0,':'dari 0,','TotalasosiasiAIR':'Total asosiasi AIR','p0,':'p = 0,','memuatnol':'memuat nol','totalAIR':'total AIR','langsungAIR0,':'langsung AIR 0,','SRMR,d_ULS,d_G':'SRMR, d_ULS, d_G','estimated:**SRMR':'estimated:** SRMR','HI950,':'HI95 0,',';d_ULS':'; d_ULS',';d_G':'; d_G','SRMRdan':'SRMR dan','melewatiHI99':'melewati HI99','seluruhdiagnostikfit':'seluruh diagnostik fit','batasHTMT':'batas HTMT','runM0':'run M0','nativeBCa satu sisi95%':'native BCa satu sisi 95%','untukEXP–PP':'untuk EXP–PP','danEXP–AD':'dan EXP–AD','M1nativePLSpredict/CVPAT':'M1 native PLSpredict/CVPAT','prediksiM0':'prediksi M0','hasilM1':'hasil M1','pembagianfold':'pembagian fold','Directantecedents':'Direct antecedents','langsungAD':'langsung AD','daripadaM0':'daripada M0','kinerjaAI, auditprivasi':'kinerja AI, audit privasi','M0dipertahankan':'M0 dipertahankan','M1sebagai':'M1 sebagai','model,7jalur,20indikator reflektif,271baris,dan semua5.420nilai':'model, 7 jalur, 20 indikator reflektif, 271 baris, dan semua 5.420 nilai','Seluruh32estimasi':'Seluruh 32 estimasi','nativeM1 danPythonM1;15estimasi':'native M1 dan Python M1; 15 estimasi','denganSE/CI bootstrapPython':'dengan SE/CI bootstrap Python','dari|beta|/SE':'dari |beta|/SE','Nativep':'Native p','Filebootstrap':'File bootstrap','tanpaTR':'tanpa TR','workbook,CSVdanJSON':'workbook, CSV, dan JSON'}
for a,b in replace.items():md=md.replace(a,b)
(O/'KidSense_M1_Native_Hasil_Verifikasi.md').write_text(md)
print('Verified native M1 workbook and report saved.')
