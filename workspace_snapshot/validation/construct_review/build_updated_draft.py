from pathlib import Path
import json,hashlib,zipfile,re,os,math
import numpy as np,pandas as pd,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent;V=B.parent;O=B/'output';F=O/'figures';F.mkdir(parents=True,exist_ok=True)
U=json.loads((B/'definitions_and_items_user.json').read_text());Q=json.loads((B/'exploratory_M1/M1_exploratory_results.json').read_text());S=json.loads((V/'native_bootstrap/native_structural_verification.json').read_text());H=json.loads((V/'native_htmt_one_sided/verification.json').read_text());C=json.loads((V/'native_prediction/native_cvpat_verification.json').read_text())
N=json.loads((V/'native_M1_corrected/native_M1_verified.json').read_text())
M1={r['effect']:r for r in N['results']}
# Exploratory figure, distinct from native primary model.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
labels=['AIR -> AD','EXP -> AD','PP -> AD','TR -> AD'];yy=np.arange(4);rr=[M1[k] for k in labels]
fig,ax=plt.subplots(figsize=(9.2,4.5));est=np.array([r['estimate'] for r in rr]);lo=np.array([r['CI95_percentile_low'] for r in rr]);hi=np.array([r['CI95_percentile_high'] for r in rr])
ax.errorbar(est,yy,xerr=np.vstack([est-lo,hi-est]),fmt='o',ms=6,color='#245A81',ecolor='#245A81',capsize=4,lw=1.6);ax.axvline(0,color='#343A40',lw=1,ls='--');ax.set_yticks(yy,[x.replace(' -> ',' → ') for x in labels]);ax.invert_yaxis();ax.set_xlim(-.14,.6);ax.set_xlabel('Koefisien terstandardisasi dan CI95 percentile dua sisi');ax.set_title('M1 native SmartPLS: asosiasi langsung dengan AD',pad=12);ax.grid(axis='x',color='#E1E6EA',lw=.7);ax.set_axisbelow(True)
for r,y in zip(rr,yy):ax.text(1.02,y,f"{r['estimate']:.3f} [{r['CI95_percentile_low']:.3f}; {r['CI95_percentile_high']:.3f}]",transform=ax.get_yaxis_transform(),va='center',fontsize=9)
for side in ['top','right']:ax.spines[side].set_visible(False)
fig.subplots_adjust(left=.15,right=.73,bottom=.22,top=.84);fig.text(.15,.035,'Native M1: 10.000 bootstrap percentile dua sisi. Analisis sensitivitas posthoc.',fontsize=9,color='#343A40');fig.savefig(F/'M1_direct_AD_exploratory.png',dpi=220,bbox_inches='tight');fig.savefig(F/'M1_direct_AD_exploratory.svg',bbox_inches='tight');plt.close(fig)
# Updated review workbook.
w=openpyxl.Workbook();w.remove(w.active)
def tab(name,heads,rows):
 s=w.create_sheet(name);s.append(heads)
 for row in rows:s.append(list(row))
 s.freeze_panes='A2';s.auto_filter.ref=s.dimensions;s.row_dimensions[1].height=34
 for c in s[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='164B63');c.alignment=Alignment(wrap_text=True)
 for row in s.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(c.value,float):c.number_format='0.000000'
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='EEF4F7')
 for j,col in enumerate(s.columns,1):s.column_dimensions[get_column_letter(j)].width=min(88,max(16,max(len(str(c.value or '')) for c in col)+2))
 for row in s.iter_rows(min_row=2):
  lines=max(max(1,math.ceil(len(str(c.value or ''))/(s.column_dimensions[c.column_letter].width*.9))) for c in row)
  s.row_dimensions[row[0].row].height=min(240,lines*14+8)
 return s
summary=[['Status','Tinjauan isi selesai atas definisi dan12item; estimasi danbootstrap native M1 lengkap sudah diverifikasi. M0 tetap hasil awal; M1 adalah sensitivitas posthoc.'],['EXP','Explainability dioperasionalkan sebagai pemahaman yang dilaporkan orang tua, bukan kualitas teknis XAI yang diuji objektif.'],['PP','Persepsi perlindungan privasi anak, bukan bukti audit keamanan/privasi atau penerapan persetujuan aktual.'],['AD','Niat hipotetis dan kondisional: sistem tersedia, aman dan berfungsi sesuai rancangan; bukan adopsi/retensi aktual.'],['Penghapusan item','Tidak ada dasar isi yang cukup untuk menghapus item tertentu atau menggabungkan EXP/PP/AD.'],['M1 langsung','EXP→AD danPP→AD memiliki CI tidak memuat0; AIR→AD memuat0. CI nativepercentile dua sisi telah diperiksa; status analisis tetap posthoc.'],['M1 batas','Bagian kovarians struktural skor tersaturasi; kenaikanR2/fit tidak mengonfirmasi teori. Masalah HTMT tetap.'],['Paparan dikonfirmasi','Responden hanya menilai deskripsi/gambar rancangan; temuan adalah persepsi dan niat pada evaluasi konsep.'],['Informasi belum ada','Teks AIR/TR lengkap, sumber/adaptasi skala, materi stimulus persis dan protokol survei lengkap.']]
tab('Ringkasan',['Aspek','Kesimpulan'],summary)
tab('Definisi_peneliti',['Kode','Nama English asli','Definisi operasional peneliti','Batas interpretasi'],[[k,v['English'],v['definition'],v.get('scope','Persepsi/keyakinan yang dilaporkan, bukan kinerja teknis yang diukur.')] for k,v in U['constructs'].items()])
tab('Item_asli',['Kode','Pernyataan verbatim peneliti'],list(U['items'].items()))
review=[['EXP1–EXP4','Pemahaman alasan kategori, dasar peringatan, confidence/error, serta interpretasi alert.','Secara isi berbeda dari privasi dan niat; tidak mendukung penggabungan otomatis.'],['EXP3','Confidence dan kemungkinan kesalahan berada dalam satu item.','Periksa apakah responden memahami kedua aspek; bukan alasan otomatis menghapus data item.'],['PP1/PP4 vsPP2/PP3','Evaluasi umum berdampingan dengan aspek consent, storage/deletion.','Jelaskan persepsi umum yang mendasari semua item; cakupan beragam tidak otomatis membuktikan formatif.'],['AD1 vsAD2/AD3 vsAD4','Mencoba, rencana penggunaan, pemanfaatan fitur, keberlanjutan bersyarat.','Sesuai niat adopsi luas bila didefinisikan demikian; AD4 bukan retensi aktual.'],['PromptAD','Membayangkan sistem tersedia, memenuhi keamanan danfungsi.','Batasi generalisasi pada skenario itu. Dampak prompt/bias tidak diukur tanpa pembanding.'],['AIR/TR','Definisi ada; bunyi delapan item belum diberikan.','Tinjauan isi kedua skala belum menyeluruh.']]
tab('Review_isi',['Bagian','Observasi isi','Implikasi proporsional'],review)
keys=['kind','effect','estimate','bootstrap_SE','CI95_percentile_low','CI95_percentile_high','CI_excludes_zero','bootstrap_valid_count','status'];tab('M1_Python_eksploratori',keys,[[r[k] for k in keys] for r in Q['results']])
nativekeys=['kind','effect','estimate','bootstrap_SE','t','p','CI95_percentile_low','CI95_percentile_high','CI_excludes_zero','source_row'];tab('M1_native_terverifikasi',nativekeys,[[r[k] for k in nativekeys] for r in N['results']])
tab('M0_vs_M1',['Aspek','M0 terverifikasi native','M1 native eksploratori','Catatan'],[['Jalur→AD','TR saja','TR dan AIR/EXP/PP','Tiga jalur tambahan dimasukkan bersama, bukan dipilih berdasarkan p.'],['R2AD',S['r2']['AD']['O'],N['r2']['AD']['estimate'],'Perbandingan deskriptif; skor/bobot juga berubah.'],['R2TR',S['r2']['TR']['O'],N['r2']['TR']['estimate'],'Bukan F-test nested atas skor identik.'],['HTMT inferensial','2 pasangan belum memenuhi','Titik dan CI dua sisi tetap sama; BCa satu sisi sebelumnya tetap relevan','HTMT berbasis korelasi item; data dan pengelompokan item tidak berubah.'],['Status native','Sudah diverifikasi','Estimasi titik dan bootstrapM1 lengkap sudah diperiksa','Ekspor diperbaiki KidSense_M1_DenganTR_Bootstrap_10000.xlsx memuat5konstruk7jalur.'],['Saturasi kovarians struktural','Ada restriksi eksogen→AD','15 parameter untuk15 momen skor','Saturasi hanya bagian skor struktural; bukan seluruh model item.']])
protocol=[['1','Simpan model dan seluruh laporan M0 sebagai baseline.'],['2','Buat salinan model dengan nama KidSense_M1_Eksploratori; gunakan dataset271 dan20indikator yang sama.'],['3','Pertahankan AIR/EXP/PP→TR danTR→AD. Tambahkan sekaligus AIR→AD,EXP→AD,PP→AD. Jangan mengubah item/kasus.'],['4','PLS-SEM Path, Standardized, initial Default; catat semua pengaturan dan ekspor estimasi native M1.'],['5','Bootstrap10.000, Complete, Percentile, Two-tailed, alpha0,05, Fixed seed. Simpan/ekspor sebagai M1 terpisah.'],['6','Bandingkan direct dan specificindirect serta CI dengan tabel PythonM1. CI tidak wajib identik antarRNG.'],['7','Laporkan sebagai analisis sensitivitas posthoc. Jangan memilih M1 hanya karena R2/fit naik atau mengklaim HTMT telah selesai.'],['8','Jika M1 akan menjadi klaim utama, perlukan alasan teori serta validasi lebih lanjut; native prediksi M1 belum tersedia.']]
tab('Protokol_native_M1',['Tahap','Tindakan'],protocol)
tab('Batas_metode',['Topik','Catatan'],[['Definisi','Operasional dari peneliti; tidak diklaim kutipan teori atau skala teradopsi tervalidasi.'],['M0 mediasi','Tidak ada jalur langsung eksogen→AD yang diestimasi; tidak membuktikan full/partialmediation atau direct effects tepatnol.'],['M1 mediasi','Direct+indirect adalah asosiasi dalam modelposthoc, bukan bukti mediasi kausal. AIRdirect tidak signifikan bukan bukti nol.'],['M1 covariances','Semua momen skor dapat direproduksi oleh struktural lengkap. Ini membatasi penggunaan fit sebagai pengujian struktur.'],['Inferensi','Seluruh data sama; analisis posthoc perlu ditandai dan tidak dianggap konfirmasi independen.'],['Skenario','Paparan hanya deskripsi/gambar rancangan. AD adalah niat hipotetis dan kondisional; tidak diartikan sebagai adopsi aktual atau evaluasi prototipe fungsional.']])
w.save(O/'KidSense_Tinjauan_Konstruk_dan_M1.xlsx')
# Reader-facing document. Native M0 and exploratory M1 remain in distinct sections.
md='''# KidSense: klarifikasi konstruk dan analisis sensitivitas model

**Status: draf teknis untuk ditinjau.** Definisi dan item kini diselaraskan dengan keterangan peneliti. Model awal M0 tetap hasil utama yang telah diverifikasi native. M1 tetap analisis tambahan eksploratori. Estimasi titik serta bootstrap tujuh jalurnya telah diverifikasi native dari KidSense_M1_DenganTR_Bootstrap_10000.xlsx. Tabel dan gambar utama M1 berikut memakai hasil native; pembanding Python disimpan terpisah.

## Keputusan setelah membaca instrumen

EXP, PP, dan AD memiliki isi yang berbeda secara konseptual: pemahaman penjelasan, persepsi perlindungan privasi, dan niat adopsi. Tidak ada dasar isi yang cukup untuk menghapus item tertentu atau menggabungkan konstruk hanya karena batas atas HTMT EXP–PP dan EXP–AD belum memenuhi0,90. Perbedaan konseptual ini juga tidak menghapus keterbatasan diskriminan pada data yang tersedia.

Label asli **Explainability** dipertahankan, dengan penjelasan bahwa operasionalisasinya adalah pemahaman yang dilaporkan orang tua terhadap penjelasan. Ini bukan pengukuran objektif kemampuan XAI. AIR adalah perceived AI reliability, dan PP adalah perceived privacy protection; angka skala tidak membuktikan akurasi pengenalan emosi, keamanan aktual, atau audit privasi.

AD harus disebut **niat adopsi hipotetis dan kondisional**. Responden diminta membayangkan KidSense tersedia, memenuhi persyaratan keamanan, dan berfungsi sesuai rancangan. AD4 menambahkan kondisi pengalaman masa depan memenuhi harapan. Jadi hasil AD tidak diinterpretasikan sebagai perilaku penggunaan aktual, retensi yang sudah diamati, atau permintaan pasar tanpa syarat.

## Definisi operasional peneliti

Definisi berikut berasal dari cakupan indikator yang diberikan peneliti, bukan kutipan teori dari publikasi eksternal.

{{DEFINITIONS}}

## Tinjauan isi indikator

- **EXP1 dan EXP2:** alasan kategori emosi dan dasar peringatan adalah konteks informasi yang berdekatan, tetapi tidak identik secara otomatis. EXP4 menilai bantuan penjelasan untuk menafsirkan peringatan. Tidak ada isi privasi atau niat penggunaan yang dinyatakan langsung dalam item-item itu.
- **EXP3:** pemahaman tingkat keyakinan dan kemungkinan kesalahan AI tercakup dalam satu pernyataan. Pemeriksaan kognitif dapat menilai apakah kedua bagian dipahami konsisten; ini belum menjadi bukti bahwa item tersebut salah atau harus dihapus.
- **PP:** PP1/PP4 lebih global, sedangkan PP2/PP3 mencakup consent serta penyimpanan/penghapusan. Spesifikasi reflektif perlu dijelaskan sebagai manifestasi persepsi perlindungan umum. Keragaman aspek tidak cukup untuk menyimpulkan PP harus formatif atau mengganti model pengukuran pada data lama.
- **AD:** mencoba, rencana menggunakan, pemanfaatan peringatan, dan keberlanjutan bersyarat mencakup beberapa tahap niat. Definisi yang luas dapat mengakomodasi cakupan tersebut, tetapi naskah tidak boleh menyebutnya hanya initial adoption atau actual continuance tanpa pembatasan.
- **Prompt AD:** asumsi keamanan/fungsi harus ditulis dalam metode dan batas generalisasi. Prompt dapat membentuk konteks jawaban, tetapi tanpa kelompok pembanding, arah atau ukuran pengaruhnya tidak dapat ditentukan.
- **AIR dan TR:** nama serta definisinya tersedia; teks empat item masing-masing belum diberikan, sehingga tinjauan isi kedua skala belum menyeluruh.

## Draf metode dan hasil utama M0

Analisis melibatkan271observasi dan20indikator untuk AIR(Perceived AI Reliability), EXP(Explainability), PP(Perceived Privacy Protection), TR(Trust), dan AD(Adoption Intention). Responden menilai deskripsi dan gambar rancangan KidSense. Jawaban merefleksikan persepsi atas konsep yang disajikan dan niat penggunaan hipotetis, bukan evaluasi penggunaan prototipe fungsional. Dalam bagian AD, responden diminta membayangkan bahwa KidSense tersedia, memenuhi persyaratan keamanan, dan berfungsi sesuai rancangan. Asumsi dalam skenario tersebut tidak diperlakukan sebagai bukti keamanan atau kinerja aktual.

Estimasi native SmartPLS4.1.2.1 memakai pathweighting dan hasil terstandardisasi. Pengukuran reflektif disimpan dengan outerweightingAUTOMATIC; perhitungan independen ModeA mereproduksi estimasi titik. Bootstrap utama memakai10.000subsamples, two-tailedα0,05 dan percentileCI95%. HTMT dinilai terpisah dengan BCa satu sisi95% terhadap ambang0,90. Prediksi memakai Directantecedents,10folds×10repetitions danFixedseed; angka seed native tidak tercatat.

Dalam M0, AIR→TR β0,260379 CI95[0,139482;0,380324], EXP→TR β0,293921[0,157908;0,425392], PP→TR β0,315452[0,164208;0,465164], dan TR→AD β0,687964[0,603460;0,764247]. Keempat p native<0,001. R²TR0,616399 danAD0,473295. Semua tiga asosiasi tidak langsung melalui TR memiliki interval yang tidak memuat nol.

Hasil itu tidak menguji full/partialmediation: jalur langsung AIR/EXP/PP→AD tidak diestimasi pada model awal. Tidak adanya jalur dalam diagram bukan direct effects yang terbukti tidak signifikan. Asosiasi tersebut tidak menetapkan sebab-akibat.

Batas atasBCa95% HTMT EXP–PP0,908139 dan EXP–AD0,912789 belum memenuhi<0,90. Kriteria fit estimatedcompositemodel d_ULS dan d_G juga melewati batas bootstrap. Prediksi native memberi8Q²_predict positif; RMSEPLS lebih rendah dariLM pada5/8indikator danMAE pada7/8. CVPAT Overall signifikan terhadap benchmarkmean(IA), tetapi belum terhadapLM(p0,122338). Prediksi AD menggunakan TR yang diamati dan bersifat kondisional.

## Analisis tambahan M1 — native terverifikasi, tetap eksploratori

M1 mempertahankan seluruh271responden dan20indikator. Ketiga jalur langsung AIR→AD,EXP→AD,PP→AD ditambahkan bersama ke model awal untuk memeriksa sensitivitas pembatasan bahwa semua asosiasi dengan AD melalui TR. Jalur tidak dipilih satu per satu berdasarkan p. Ini analisis posthoc setelah hasil awal diketahui, bukan hipotesis konfirmatori baru.

M1 native memakai10.000bootstrap,Complete,Percentile,Two-tailed,alpha0,05,Fixedseed danSmartPLS4.1.2.1. Nilai seed numerik tidak diekspor. Sebanyak32estimasi titik identik dengan algoritma nativeM1 dan cocok denganPython hingga1,00411×10⁻¹⁰. Pembanding Python menggunakan empat stream NumPydefault_rng20261106–20261109; interval antarRNG tidak diharapkan identik. Seluruh keputusan CI utama sama.

{{M1_TABLE}}

![M1 native eksploratori](figures/M1_direct_AD_exploratory.png)

Gambar. Koefisien dan CI95percentile untuk empat prediktor AD pada M1. Interval berasal dari bootstrap native yang sudah diperbaiki. M1 tetap analisis sensitivitas posthoc.

Pada M1, EXP dan PP memiliki asosiasi langsung positif dengan AD serta CI yang tidak memuat nol; AIRdirect masih memuat nol. TR→AD tetap positif. Ketiga asosiasi tidak langsung melalui TR juga memiliki CI yang tidak memuat nol: AIR0,079954[0,032983;0,143367], EXP0,089052[0,035225;0,158803], danPP0,095297[0,037491;0,168760]. Ini pola asosiasi langsung/tidak langsung dalam model tambahan, bukan bukti mediasi kausal atau pembuktian efek AIR tepat nol.

R²AD M1=0,575904, dibanding0,473295 pada M0; R²TR M1=0,615656. Angka ini bersifat deskriptif karena jumlah parameter bertambah dan bobot komposit berubah. **Bagian kovarians struktural skor M1 tersaturasi:15parameter untuk15momen unik**. Hal itu tidak menyaturasi seluruh model indikator, tetapi berarti peningkatan fit kovarians skor tidak dapat dipakai mengonfirmasi teori yang ditambahkan.

Pada fit nativeM1, estimated dan saturated sama secara numerik. Composite estimated mempunyaiSRMR0,031026,d_ULS0,202144,d_G0,145440 di bawahHI95 masing-masing0,034508;0,250075;0,164052. Namun mixed estimated masih melewatiHI95 padaSRMR(0,049034>0,044696),d_ULS(0,504913>0,419530),dan d_G(0,275551>0,274682). Karena itu, perbaikan fitcomposite tidak diperlakukan sebagai bukti semua diagnostikfit lolos atau teori jalur baru terkonfirmasi.

AIRlangsung memiliki p0,505143 dan CI yang memuatnol. TotalasosiasiAIR memiliki p0,047521 danCIpercentile[0,002081;0,253714], tetapi correctedCI[−0,002360;0,249998] memuatnol. Total dan direct effects dibedakan; bila totalAIR dibahas, sensitivitas metodeinterval perlu dilaporkan.

Penambahan jalur tidak mengubah estimasi titik HTMT EXP–PP/EXP–AD karena HTMT berbasis korelasi item, sedangkan data serta pengelompokan indikator tetap sama. Tabel HTMT pada runM1 ini dua sisi2,5%/97,5% dan identik denganM0. Untuk kriteria batasatasBCa95 satu sisi tetap gunakan run khusus sebelumnya. Estimasi titik danbootstrap M1 kini selesai diverifikasi; filebootstrap lama tanpaTR tetap diarsipkan sebagai model lain. Prediksi M1 belum diuji. Hasil ini mendukung pemeriksaan sensitivitas yang transparan, bukan penggantian otomatis model utama.

## Protokol verifikasi native M1 yang terpisah

1. Pertahankan model dan ekspor M0. Buat salinan bernama **KidSense_M1_Eksploratori** dengan dataset271 dan20indikator yang sama.
2. Pertahankan empat jalur awal. Tambahkan AIR→AD, EXP→AD, dan PP→AD bersama-sama; jangan menghapus item atau kasus.
3. Jalankan PLS-SEM Path/Standardized dengan initialDefault; simpan pengaturan dan ekspor M1 terpisah.
4. Jalankan bootstrap10.000, Complete, Percentile, Two-tailed,α0,05, Fixedseed. Simpan sebagai **KidSense_M1_Bootstrap_10000.xlsx**.
5. Bandingkan direct serta specificindirect dan CI dengan tabel M1Python. Beri label sensitivitas posthoc; perbedaan RNG tidak membuat CI wajib identik.
6. Penggunaan M1 sebagai klaim utama memerlukan alasan teori dan validasi lebih lanjut. Kenaikan R²/fit saja tidak cukup. Native PLSpredict/CVPAT M1 belum dijalankan. Perbandingan M0–M1 perlu informasi prediktor danfold yang setara: Directantecedents M1 menambahkan informasiAD yang tidak dipakaiM0. Skenario Earlyantecedents pada kedua model dapat ditetapkan sebagai pembandingan tersendiri, dengan benchmark danfold yang dicatat.

## Draf pembahasan yang diperbarui

Temuan menunjukkan bahwa persepsi reliabilitas AI, pemahaman penjelasan, dan persepsi perlindungan privasi berasosiasi dengan trust pada rancangan KidSense. Trust berasosiasi dengan niat adopsi dalam skenario keamanan dan fungsi yang ditetapkan. Konsistensi komputasi lintas perhitungan mendukung ketepatan angka, tetapi tidak menghilangkan keterbatasan diskriminasi sebagian konstruk dan fit model.

Analisis tambahan mengindikasikan bahwa pembatasan semua asosiasi Explainability dan Perceived Privacy Protection terhadap AdoptionIntention melalui Trust patut ditinjau secara substantif. Namun, M1 adalah analisis posthoc pada sampel yang sama dengan kovarians struktural skor tersaturasi. Hasilnya tidak digunakan sebagai konfirmasi teori baru atau alasan menghapus konstruk. Isi item, sumber teori, dan data independen perlu menopang keputusan revisi.

Niat adopsi yang tinggi pada skenario hipotetis tidak setara dengan perilaku menggunakan KidSense. Demikian pula skor AIR dan PP tidak membuktikan kinerja teknis sistem atau perlindungan data yang sudah diaudit. Kesimpulan dibatasi pada persepsi dan niat orang tua setelah menilai deskripsi/gambar rancangan. Hasil ini membahas penerimaan konsep pada skenario yang diberikan; generalisasi ke pengalaman penggunaan dan adopsi aktual memerlukan pengujian lebih lanjut. Materi stimulus persis, protokol survei lengkap dan bukti penyaringan323→271 masih perlu dilengkapi.

## Item asli yang disediakan peneliti

{{ITEMS}}

## Jejak sumber dan batas

Nama dan definisi konstruk serta12item merupakan informasi yang diberikan peneliti, bukan kutipan dari literatur eksternal. Angka M0 berasal dari ekspor native yang sudah diverifikasi. Angka M1 pada tabel/gambar utama berasal dari ekspor native yang sudah diperbaiki. Pembanding Python tetap tersedia dan diberi label terpisah. Penilaian isi bukan pengganti validasi ahli atau studi kognitif. Format jurnal dan sumber/adaptasi skala belum ditetapkan dalam dokumen ini. Semua data serta model awal dipertahankan.
'''
# Fill tables and normalize reader-facing spacing without altering source items.
defs='\n\n'.join(f"**{k} — {r['English']}.** {r['definition']}" for k,r in U['constructs'].items())
table='| Jalur ke AD | β native M1 | p native | CI95 percentile native | Memuat nol? |\n|---|---:|---:|---|---|\n'
for k in labels:
 r=M1[k];table+=f"| {k} | {r['estimate']:.6f} | {r['p']:.6g} | [{r['CI95_percentile_low']:.6f}; {r['CI95_percentile_high']:.6f}] | {'Tidak' if r['CI_excludes_zero'] else 'Ya'} |\n"
items='\n\n'.join(f"**{k}.** {v}" for k,v in U['items'].items())
md=md.replace('{{DEFINITIONS}}',defs).replace('{{M1_TABLE}}',table.rstrip()).replace('{{ITEMS}}',items)
replacements={'memenuhi0,90':'memenuhi 0,90','melibatkan271observasi dan20indikator':'melibatkan 271 observasi dan 20 indikator','AIR(Perceived':'AIR (Perceived','EXP(Explainability)':'EXP (Explainability)','PP(Perceived':'PP (Perceived','TR(Trust)':'TR (Trust)','AD(Adoption':'AD (Adoption','SmartPLS4.1.2.1':'SmartPLS 4.1.2.1','pathweighting':'path weighting','outerweightingAUTOMATIC':'outer weighting AUTOMATIC','ModeA':'Mode A','memakai10.000subsamples':'memakai 10.000 subsamples','two-tailedα':'two-tailed α','percentileCI95%':'percentile CI 95%','satu sisi95%':'satu sisi 95%','ambang0,90':'ambang 0,90','Directantecedents':'Direct antecedents','10folds×10repetitions':'10 folds × 10 repetitions','danFixedseed':'dan Fixed seed','β0,':'β 0,','CI95[':'CI95 [','p native<':'p native <','R²TR0,':'R² TR 0,','danAD0,':'dan AD 0,','full/partialmediation':'mediasi penuh/parsial','atasBCa95%':'atas BCa 95%','EXP–PP0,':'EXP–PP 0,','EXP–AD0,':'EXP–AD 0,','memenuhi<':'memenuhi <','estimatedcompositemodel':'estimated composite model','memberi8Q²_predict':'memberi 8 Q²_predict','RMSEPLS':'RMSE PLS','dariLM':'dari LM','pada5/8indikator':'pada 5/8 indikator','danMAE pada7/8':'dan MAE pada 7/8','benchmarkmean(IA)':'benchmark mean (IA)','terhadapLM(p0,122338)':'terhadap LM (p = 0,122338)','seluruh271responden dan20indikator':'seluruh 271 responden dan 20 indikator','dengan10.000bootstrap':'dengan 10.000 bootstrap','NumPydefault_rng seed20261106':'NumPy default_rng seed 20261106','masing-masing2500':'masing-masing 2500','CIpercentile dua sisi95%':'CI percentile dua sisi 95%','CI95percentile':'CI95 percentile','AIRdirect':'AIR direct','AIR0,':'AIR 0,','EXP0,':'EXP 0,','danPP0,':'dan PP 0,','R²AD':'R² AD','dibanding0,':'dibanding 0,','R²TR':'R² TR','tersaturasi:15parameter untuk15momen':'tersaturasi: 15 parameter untuk 15 momen','dataset271 dan20indikator':'dataset 271 dan 20 indikator','initialDefault':'initial Default','bootstrap10.000':'bootstrap 10.000','Two-tailed,α':'Two-tailed, α','Fixedseed':'Fixed seed','specificindirect':'specific indirect','M1Python':'M1 Python','AdoptionIntention':'Adoption Intention','penyaringan323→271':'penyaringan 323 → 271','serta12item':'serta 12 item','perhitunganPython':'perhitungan Python','hasilSmartPLS':'hasil SmartPLS'}
for a,b in replacements.items():md=md.replace(a,b)
(O/'KidSense_Draf_Terklarifikasi_dan_M1.md').write_text(md)
# Editable Word; retain separate status and method labels.
doc=Document();s=doc.sections[0];s.top_margin=Cm(2);s.bottom_margin=Cm(2);s.left_margin=Cm(2.2);s.right_margin=Cm(2.2)
doc.styles['Normal'].font.name='Calibri';doc.styles['Normal'].font.size=Pt(10.5);doc.styles['Normal'].paragraph_format.space_after=Pt(6)
for n in ['Title','Heading 1','Heading 2']:doc.styles[n].font.name='Calibri';doc.styles[n].font.color.rgb=RGBColor.from_string('164B63')
p=s.footer.paragraphs[0];p.alignment=2;r=p.add_run('KidSense — draf dan analisis eksploratori | ');r.font.size=Pt(8);fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');p._p.append(fld)
lines=md.splitlines();i=0
while i<len(lines):
 line=lines[i].strip();i+=1
 if not line:continue
 if line.startswith('# '):doc.add_heading(line[2:],0)
 elif line.startswith('## '):doc.add_heading(line[3:],1)
 elif line.startswith('!['):path=re.search(r'\]\((.+)\)',line).group(1);doc.add_picture(str(O/path),width=Cm(16));doc.paragraphs[-1].paragraph_format.keep_with_next=True
 elif line.startswith('|'):
  heads=[x.strip() for x in line.strip('|').split('|')];t=doc.add_table(rows=1,cols=len(heads));t.style='Light Shading Accent 1'
  for c,h in zip(t.rows[0].cells,heads):c.text=h
  if i<len(lines) and re.match(r'^\|[-| :]+\|$',lines[i].strip()):i+=1
  while i<len(lines) and lines[i].strip().startswith('|'):
   vals=[x.strip() for x in lines[i].strip().strip('|').split('|')];i+=1
   for c,v in zip(t.add_row().cells,vals):c.text=v
  for row in t.rows:
   for cell in row.cells:
    for p in cell.paragraphs:
     for r in p.runs:r.font.size=Pt(9)
 elif line.startswith('- '):doc.add_paragraph(line[2:].replace('**',''),style='List Bullet')
 elif re.match(r'^\d+\. ',line):doc.add_paragraph(re.sub(r'^\d+\. ','',line).replace('**',''),style='List Number')
 else:doc.add_paragraph(line.replace('**',''))
doc.save(O/'KidSense_Draf_Terklarifikasi_dan_M1.docx')
manifest={'definitions_source':'Exact user message; saved verbatim definitions/items in definitions_and_items_user.json','native_M0_primary_preserved':True,'M1_status':'Posthoc exploratory M1;corrected native7path bootstrap andpoint estimates verified;not primary replacement','M1_native_source':N['source'],'M1_native_source_sha256':N['source_sha256'],'M1_bootstraps':10000,'M1_CSV_sha256':Q['source_sha256'],'M1_structural_saturation':Q['structural_saturation'],'exposure_context':'Confirmed by user: descriptions/images design only; conceptual survey, not functional prototype use','original_items_and_cases_modified':False}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Outputs',[(p.name,p.stat().st_size) for p in O.iterdir() if p.is_file()])
