"""Fill the actual uploaded JADS Word template with the source-backed draft.

Source datasets and template are read-only. Tables are built from verified JSON.
"""
from pathlib import Path
from copy import deepcopy
import os, re, json, hashlib, csv
os.environ.setdefault('MPLCONFIGDIR', '/tmp/kidsense_mpl_cache')
os.environ.setdefault('XDG_CACHE_HOME', '/tmp/kidsense_xdg')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
FIG = ROOT / 'figures'
V = ROOT.parent / 'validation'
TEMPLATE = ROOT.parent / 'attachments/2f82fc2f-7333-4b16-932a-c23db07d7717/JADS-template.docx'
for p in [OUT, FIG]: p.mkdir(parents=True, exist_ok=True)
read = lambda p: json.loads(Path(p).read_text())
M0 = read(V / 'native_bootstrap/native_structural_verification.json')
M1 = read(V / 'native_M1_corrected/native_M1_verified.json')
HT = read(V / 'native_htmt_one_sided/verification.json')
PR = read(V / 'native_prediction/prediction/native_prediction_validation.json')
CV = read(V / 'native_prediction/native_cvpat_verification.json')
DIAG = read(ROOT / 'review/structural_diagnostics.json')
ITEMS = read(V / 'construct_review/definitions_and_items_user.json')
MEAS = list(csv.DictReader((ROOT / 'review/measurement_descriptives_M0.csv').open()))
REFS = read(ROOT / 'references.json')
TITLE = 'Parental trust and conditional adoption intention toward KidSense: A PLS-SEM concept evaluation with computational revalidation'
ABSTRACT = (
    'Understanding parental acceptance of a proposed AI system requires distinguishing concept-based perceptions from experience with a functioning product. '
    'This study examines Perceived AI Reliability, Explainability, Perceived Privacy Protection, Trust, and Adoption Intention using 271 questionnaire records and 20 indicators. '
    'Respondents evaluated descriptions and images of the KidSense design; intention was conditional on its assumed availability, security, and functioning. '
    'The original model (M0) was assessed in SmartPLS 4 using 10,000 bootstrap resamples, separate one-sided BCa HTMT bounds, and 10-fold cross-validation repeated 10 times. '
    'Independent computations checked native estimates and prediction outputs. '
    'All four M0 paths were positive (p < 0.001); Trust was associated with intention (β = 0.688), with R² = 0.616 for Trust and 0.473 for intention. '
    'Although reliability and convergent summaries were favorable, the HTMT upper bounds exceeded 0.90 for Explainability–Privacy Protection and Explainability–Adoption Intention. '
    'All eight endogenous indicators had positive Q²predict, but CVPAT did not establish overall superiority over the linear-model benchmark (p = 0.122). '
    'A post hoc model (M1) added three direct paths to intention, increasing in-sample R² to 0.576; Explainability and Privacy Protection had positive direct associations, while the reliability direct path was not supported. '
    'The results provide numerically traceable evidence about conditional concept acceptance, with unresolved measurement and specification limitations. '
    'They do not establish causal mediation, actual adoption, or implemented-system performance.'
)
KEYWORDS = 'KidSense, parental trust, adoption intention, explainability, perceived privacy protection, PLS-SEM'

# Figures are original scientific diagrams/plots made from the recorded models.
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(figsize=(9.0, 3.7))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
nodes = {'AIR': (.14, .80), 'EXP': (.14, .49), 'PP': (.14, .18), 'TR': (.55, .49), 'AD': (.88, .49)}
labels = {'AIR': 'AIR\nPerceived AI\nReliability', 'EXP': 'EXP\nExplainability', 'PP': 'PP\nPerceived Privacy\nProtection', 'TR': 'TR\nTrust', 'AD': 'AD\nAdoption\nIntention'}
w, h = .205, .205
for name, (x, y) in nodes.items():
    rect = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle='round,pad=0.008,rounding_size=0.01', linewidth=1, edgecolor='#223648', facecolor='#f3f6f8', zorder=4)
    ax.add_patch(rect); ax.text(x, y, labels[name], ha='center', va='center', fontsize=10, zorder=5)
for name in ['AIR', 'EXP', 'PP']:
    x,y=nodes[name]
    ax.add_patch(FancyArrowPatch((x+w/2+.01,y), (nodes['TR'][0]-w/2-.012,nodes['TR'][1]), arrowstyle='-|>', mutation_scale=13, linewidth=1.3, color='#202020', zorder=3))
ax.add_patch(FancyArrowPatch((.55+w/2+.01,.49),(.88-w/2-.012,.49),arrowstyle='-|>',mutation_scale=13,linewidth=1.3,color='#202020',zorder=3))
for name, rad in [('AIR', -.28), ('EXP', -.47), ('PP', .27)]:
    x,y=nodes[name]
    end_y = .49 + (.105 if name in ['AIR','EXP'] else -.105)
    end_x = .88 if name != 'EXP' else .84
    ax.add_patch(FancyArrowPatch((x+w/2+.01,y+.035 if name!='PP' else y-.035), (end_x,end_y), connectionstyle=f'arc3,rad={rad}', arrowstyle='-|>', mutation_scale=12, linewidth=1.1, linestyle=(0,(5,3)), color='#315e83', zorder=2))
ax.legend(handles=[Line2D([0],[0],color='#202020',label='M0 paths (also retained in M1)'),Line2D([0],[0],color='#315e83',ls='--',label='Additional paths in exploratory M1')],loc='lower center',bbox_to_anchor=(.5,-.07),ncol=2,frameon=False,fontsize=9)
fig.tight_layout(pad=.5)
for ext in ['png','svg']: fig.savefig(FIG/f'model_specifications.{ext}',dpi=300,bbox_inches='tight')
plt.close(fig)

fig,ax=plt.subplots(figsize=(7.6,2.8))
effects=['AIR -> AD','EXP -> AD','PP -> AD','TR -> AD']
for i,k in enumerate(effects):
    d=M1['paths'][k]; x=d['estimate']; lo=d['CI95_percentile_low']; hi=d['CI95_percentile_high']
    ax.errorbar(x,3-i,xerr=np.array([[x-lo],[hi-x]]),fmt='o',color='#315e83' if k!='AIR -> AD' else '#5b5b5b',capsize=4,lw=1.8,markersize=6)
ax.axvline(0,color='#777777',lw=.8,ls='--')
ax.set_yticks(range(4),[x.replace(' -> ',' → ') for x in effects[::-1]])
ax.set_xlabel('Standardized path coefficient (95% percentile bootstrap interval)')
ax.set_xlim(-.13,.57);ax.set_ylim(-.55,3.55);ax.grid(axis='x',alpha=.15);ax.spines['left'].set_visible(False)
fig.tight_layout(pad=.7)
for ext in ['png','svg']:fig.savefig(FIG/f'M1_paths_to_intention.{ext}',dpi=300,bbox_inches='tight')
plt.close(fig)

def f(x,n=3): return f'{float(x):.{n}f}'.replace('-', '−')
def pv(x): return '<0.001' if x < .001 else f(x,6)
def ar(s): return s.replace(' -> ',' → ')
def ci(a,b): return f'[{f(a)}, {f(b)}]'
tables={}
def tab(key,title,headers,rows,note,widths):
    tables[key]={'title':title,'headers':headers,'rows':rows,'note':note,'widths_cm':widths}

tab('constructs','Table 1. Operational scope of the five constructs',
    ['Code / indicators','Construct','Operational scope in concept evaluation'],[
    ['AIR / AIR1–AIR4','Perceived AI Reliability','Expected consistency and appropriateness of detections and notifications, and stable functioning during digital play.'],
    ['EXP / EXP1–EXP4','Explainability','Reported understanding of described reasons, warning information, prediction confidence and possible errors, and interpretation of alerts.'],
    ['PP / PP1–PP4','Perceived Privacy Protection','Perceived adequacy of proposed controls for camera/microphone permission, storage, deletion, and child-data protection.'],
    ['TR / TR1–TR4','Trust','Confidence that the proposed system would serve the child’s interests and responsibly provide initial emotion-related information.'],
    ['AD / AD1–AD4','Adoption Intention','Conditional intentions to try and use KidSense and its warning features, including prospective continuation if experience meets expectations.']],
    'Four reflective indicators per construct. Definitions describe the researcher-specified instrument; they do not establish objective AI capability, audited safeguards, or actual behavior.',[3.0,4.0,11.3])
rows=[]
for d in MEAS:
    g=lambda k:float(d[k])
    rows.append([d['construct'],f"{f(g('raw_item_average_mean'))} ({f(g('raw_item_average_SD_sample'))})",f"{f(g('loading_min_native_M0'))}–{f(g('loading_max_native_M0'))}",f(g('alpha_standardized_native_M0')),f(g('rho_A_native_M0')),f(g('rho_C_native_M0')),f(g('AVE_native_M0'))])
tab('measurement','Table 2. Descriptive and native M0 measurement summaries (n = 271)',
    ['Construct','Mean (SD)','Loading range','Alpha','rho_A','rho_C','AVE'],rows,
    'Mean and sample SD refer to unweighted four-item averages in the original 1–5 units. Alpha is standardized; loadings, rho_A, rho_C, and AVE are native M0 outputs. rho_A was not independently recomputed.',[2.0,3.0,3.3,2.2,2.2,2.2,3.4])
tab('htmt','Table 3. Native HTMT and one-sided BCa 95% upper bounds',
    ['Construct pair','HTMT','Upper 95% bound','Upper bound < 0.90?'],
    [[ar(d['pair']).replace('-','–'),f(d['HTMT_native']),f(d['native_BCa_upper95']),'Yes' if d['BCa_upper95_below090'] else 'No'] for d in HT['pairs']],
    'Dedicated native BCa bootstrap: 10,000 resamples, one-tailed α = 0.05. Decisions use unrounded bounds. The 0.90 criterion was not established for EXP–PP or EXP–AD; all point estimates alone were below 0.90.',[5.2,3.5,4.8,4.8])
rows=[]
for kind in ['paths','indirect']:
    for k,d in M0[kind].items():rows.append([ar(k),'Path' if kind=='paths' else 'Indirect',f(d['O']),f(d['SE']),f(d['t']),ci(*d['ci95_percentile']),pv(d['p'])])
tab('m0','Table 4. Original M0 structural paths and specific indirect effects',
    ['Association','Type','β','SE','t','95% percentile CI','p'],rows,
    'Native SmartPLS, 10,000 resamples, two-tailed α = 0.05; standardized coefficients. M0 does not estimate direct AIR/EXP/PP → AD paths. Significant products are not evidence of full or causal mediation.',[4.6,1.8,1.5,1.5,1.5,4.5,2.9])
rows=[]
for name,data in [('M0',M0),('M1',M1)]:
    for typ in ['composite','mixed']:
        vals=[next(d for d in data['fit'] if d['model']==f'Estimated {typ} model' and d['metric']==met) for met in ['SRMR','d_ULS','d_G']]
        rows.append([name,typ.title()]+[f"{f(d['original'],4)} / {f(d['HI95'],4)}" for d in vals]+['Yes' if all(d['original']<d['HI95'] for d in vals) else 'No'])
tab('fit','Table 5. Estimated-model discrepancies compared with native HI95 bounds',
    ['Model','Type','SRMR / HI95','d_ULS / HI95','d_G / HI95','All < HI95?'],rows,
    'Each cell shows the original discrepancy / its native 95th-percentile bootstrap reference bound. Composite and mixed-model outputs are distinguished. M1 is saturated only in its structural covariance specification; favorable composite comparisons do not independently confirm its paths.',[1.2,2.5,4.0,4.0,4.0,2.6])
rows=[]
for kind in ['paths','indirect']:
    for k,d in M1[kind].items():rows.append([ar(k),'Path' if kind=='paths' else 'Indirect',f(d['estimate']),f(d['bootstrap_SE']),ci(d['CI95_percentile_low'],d['CI95_percentile_high']),pv(d['p'])])
tab('m1','Table 6. Corrected native M1 exploratory paths and indirect effects',
    ['Association','Type','β','SE','95% percentile CI','p'],rows,
    'Corrected five-construct, seven-path model containing TR; same 271 records and 20 items as M0. Native 10,000-resample percentile bootstrap, two-tailed α = 0.05. Nominal inference is exploratory, with no multiplicity correction for model development.',[4.7,1.8,1.7,1.7,5.0,3.4])
rows=[]
for construct in ['TR','AD']:
    for d in sorted([x for x in PR['indicators'] if x['indicator'].startswith(construct)],key=lambda x:x['indicator']):
        rows.append([d['indicator'],f(d['Q2']),f(d['RMSE_PLS']),f(d['RMSE_LM']),f(d['RMSE_IA']),f(d['MAE_PLS']),f(d['MAE_LM'])])
tab('predict','Table 7. Native M0 held-out indicator prediction summaries',
    ['Indicator','Q²predict','RMSE PLS','RMSE LM','RMSE IA','MAE PLS','MAE LM'],rows,
    '10 folds × 10 repetitions, n = 271, 2,710 predictions per indicator. Direct antecedents: AD predictions are conditional on observed TR. Lower error is better. PLS RMSE beats LM for 5/8 indicators; PLS MAE beats LM for 7/8. Comparisons use unrounded values.',[1.8,2.4,2.8,2.8,2.8,2.8,2.9])
rows=[]
for benchmark in ['IA','LM']:
    for target in ['TR','AD','Overall']:
        d=next(x for x in CV['tests'] if x['benchmark']==benchmark and x['target']==target and x['level']=='construct')
        rows.append([benchmark,target,f(d['native_PLS_loss'],6),f(d['native_benchmark_loss'],6),f(d['native_average_loss_difference'],6),f(d['native_t']),pv(d['native_p'])])
tab('cvpat','Table 8. Native M0 CVPAT loss comparisons',
    ['Benchmark','Target','PLS loss','Benchmark loss','Difference','t','p'],rows,
    'Squared indicator prediction errors averaged within each target. Difference = PLS minus benchmark; negative favors PLS. Native p-values retained. Overall LM p = 0.122338 does not establish PLS superiority or equivalence.',[2.3,1.8,2.7,3.3,3.1,2.2,2.9])
tab('items','Table A1. Researcher-supplied original EXP, PP, and AD items',
    ['Item','Original Indonesian statement'],[[k,v] for k,v in ITEMS['items'].items()],
    'Verbatim text as supplied. AIR and TR item wording and the response anchors remain to be supplied; they were not invented for this draft.',[1.9,16.4])
rows=[]
S=DIAG['n261_uniform_answer_sensitivity']
for d in S['path_results']:rows.append([ar(d['path']),f(d['M0_n271_native_beta']),f(d['sensitivity_n261_Python_beta']),f(d['delta_sensitivity_minus_main'])])
for d in S['r2_results']:rows.append(['R² '+d['construct'],f(d['M0_n271_native_r2']),f(d['sensitivity_n261_Python_r2']),f(d['delta_sensitivity_minus_main'])])
tab('sensitivity','Table B1. Sensitivity excluding ten all-item-uniform response records',
    ['M0 quantity','Primary n = 271 (native)','Sensitivity n = 261 (Python)','Difference'],rows,
    'Point estimates only. No n = 261 bootstrap confidence intervals or significance decisions are claimed. A uniform response pattern alone does not establish invalid participation. Differences combine the labeled sample change with numerically matched point-estimation implementations.',[4.0,4.4,5.5,4.4])

doc=Document(TEMPLATE)
# Keep the uploaded section, theme, styles, headers, footers and page fields.
prototypes={k:deepcopy(doc.paragraphs[i]._p) for k,i in [('title',0),('authors',1),('affiliation',2),('dates',4),('abstract_heading',5),('abstract',6),('keywords',7),('h1',8),('h2',11),('body',9),('caption',56),('figure_caption',60),('references_heading',78)]}
for el in list(doc._element.body):
    if el.tag!=qn('w:sectPr'):doc._element.body.remove(el)
doc.core_properties.title=TITLE
doc.core_properties.subject='Draft concept-evaluation study; native SmartPLS replication'
doc.core_properties.author='Ratih Titi Komala Sari; Widowati; Adi Wibowo'
doc.core_properties.keywords=KEYWORDS
doc.core_properties.comments='Draft prepared from the actual uploaded JADS template. Unprovided study metadata are explicitly marked.'

for sec in doc.sections:
    for header in [sec.header,sec.first_page_header]:
        for table in header.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        if 'Vol.' in p.text:
                            p.text='Draft manuscript — volume, issue and pages to be assigned'
                            for r in p.runs:r.font.name='Arial';r.font.size=Pt(8)
    # Remove unused template example hyperlinks and footnote claims from the body.

def strip_num(p):
    pr=p._p.get_or_add_pPr()
    for tag in ['numPr','sectPr','pageBreakBefore']:
        for e in list(pr.findall(qn('w:'+tag))):pr.remove(e)

def runtext(p,text,size=10,bold=False,italic=False,color='000000'):
    # Explicit yellow markers make missing factual information visible in Word.
    parts=re.split(r'(\[TO BE COMPLETED:.*?\])',text)
    for part in parts:
        if not part:continue
        r=p.add_run(part);r.font.name='Times New Roman';r.font.size=Pt(size)
        r.font.bold=bold;r.font.italic=italic;r.font.color.rgb=RGBColor.from_string(color)
        if part.startswith('[TO BE COMPLETED:'):
            from docx.enum.text import WD_COLOR_INDEX
            r.font.highlight_color=WD_COLOR_INDEX.YELLOW
        rf=r._element.get_or_add_rPr().get_or_add_rFonts()
        for a in ['ascii','hAnsi','eastAsia','cs']:rf.set(qn('w:'+a),'Times New Roman')
        lang=OxmlElement('w:lang');lang.set(qn('w:val'),'en-US');r._element.get_or_add_rPr().append(lang)

def para(text,kind='body',size=10,bold=False,italic=False,color='000000'):
    from docx.text.paragraph import Paragraph
    el=deepcopy(prototypes[kind])
    for c in list(el):
        if c.tag!=qn('w:pPr'):el.remove(c)
    doc._element.body.insert(len(doc._element.body)-1,el)
    p=Paragraph(el,doc._body);strip_num(p)
    runtext(p,text,size,bold,italic,color)
    p.paragraph_format.widow_control=True
    return p

def body(text):
    p=para(text)
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing=1.1
    p.paragraph_format.space_after=Pt(6)
    p.paragraph_format.space_before=Pt(0)
    p.paragraph_format.keep_with_next=False
    return p

def heading(text,level):
    kind='references_heading' if text=='References' else ('h1' if level==1 else 'h2')
    p=para(text,kind,size=(10 if text=='References' else (11 if level==1 else 13)),bold=level==1,color='000000' if level==1 else '2E74B5')
    p.paragraph_format.keep_with_next=True;p.paragraph_format.keep_together=True
    p.paragraph_format.space_before=Pt(10 if level==1 else 6)
    p.paragraph_format.space_after=Pt(7 if level==1 else 3)
    p.paragraph_format.line_spacing=1
    p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    # Explicitly suppress inherited sample heading borders.
    pr=p._p.get_or_add_pPr();b=pr.find(qn('w:pBdr'))
    if b is not None:pr.remove(b)
    b=OxmlElement('w:pBdr')
    for edge in ['top','left','bottom','right','between']:
        e=OxmlElement('w:'+edge);e.set(qn('w:val'),'nil');b.append(e)
    pr.append(b)
    return p

front=para(TITLE,'title',17)
front.paragraph_format.keep_with_next=True
front=para('Ratih Titi Komala Sari¹,*, Widowati², Adi Wibowo³','authors',11)
front.paragraph_format.keep_with_next=True
for txt in [
    '¹ Doctoral Program of Information Systems, Postgraduate School, Diponegoro University, Semarang, Indonesia',
    '² Mathematics Department, Faculty of Mathematics and Sciences, Diponegoro University, Semarang, Indonesia',
    '³ Informatics Department, Faculty of Mathematics and Sciences, Diponegoro University, Semarang, Indonesia']:
    p=para(txt,'affiliation',9,italic=True)
    p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(3)
    p.paragraph_format.line_spacing=1
p=para('* Corresponding author: ratihtiti@students.undip.ac.id','affiliation',9)
p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(8)
p=para('(Received: to be assigned; Revised: to be assigned; Accepted: to be assigned; Available online: to be assigned)','dates',8)
p.paragraph_format.space_after=Pt(3)
para('Abstract','abstract_heading',9,bold=True)
p=para(ABSTRACT,'abstract',9)
p.paragraph_format.line_spacing=Pt(11);p.paragraph_format.space_after=Pt(12)
para('Keywords: '+KEYWORDS,'keywords',8,italic=True)

manuscript=(ROOT/'manuscript.md').read_text()
citation_order=[]
def replacecite(m):
    key=m.group(1)
    if key not in REFS:raise ValueError('Missing reference '+key)
    if key not in citation_order:citation_order.append(key)
    return '['+str(citation_order.index(key)+1)+']'
# Resolve in reading order before reference generation.
resolved=re.sub(r'\{\{(\w+)\}\}',replacecite,manuscript)

def bordercell(cell):
    pr=cell._tc.get_or_add_tcPr();m=pr.find(qn('w:tcMar'))
    if m is None:m=OxmlElement('w:tcMar');pr.append(m)
    for edge in ['top','bottom','left','right']:
        el=OxmlElement('w:'+edge);el.set(qn('w:w'),'60');el.set(qn('w:type'),'dxa');m.append(el)

def table(key):
    info=tables[key]
    cap=para(info['title'],'caption',10)
    cap.paragraph_format.keep_with_next=True;cap.paragraph_format.space_before=Pt(6);cap.paragraph_format.space_after=Pt(6)
    cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
    t=doc.add_table(rows=1,cols=len(info['headers']));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    t._tbl.tblPr.append(OxmlElement('w:tblBorders'))
    borders=t._tbl.tblPr.find(qn('w:tblBorders'))
    for edge in ['top','bottom','insideH']:
        e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4' if edge=='insideH' else '8');e.set(qn('w:color'),'A5A5A5' if edge=='insideH' else '303030');borders.append(e)
    t._tbl.tblPr.find(qn('w:tblW')).set(qn('w:w'),str(int(Cm(18.3).twips)))
    t._tbl.tblPr.find(qn('w:tblW')).set(qn('w:type'),'dxa')
    for col,width in zip(t.columns,info['widths_cm']):col.width=Cm(width)
    display_rows=[(info['headers'],True)]+[(r,False) for r in info['rows']]
    for row_index,(vals,ishead) in enumerate(display_rows):
        row=t.rows[0] if ishead else t.add_row()
        pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
        if ishead:pr.append(OxmlElement('w:tblHeader'))
        for j,(cell,txt,width) in enumerate(zip(row.cells,vals,info['widths_cm'])):
            cell.width=Cm(width);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER;bordercell(cell)
            p=cell.paragraphs[0];p.style=doc.styles['table copy']
            p.paragraph_format.space_before=Pt(1);p.paragraph_format.space_after=Pt(1);p.paragraph_format.line_spacing=1
            # Every table is shorter than one page. Keep all its rows together;
            # this also avoids a LibreOffice pagination defect dropping rows.
            p.paragraph_format.keep_with_next=True
            p.alignment=WD_ALIGN_PARAGRAPH.LEFT if j==0 or key in ['constructs','items'] else WD_ALIGN_PARAGRAPH.CENTER
            runtext(p,str(txt),8.5 if key not in ['items','constructs'] else 9,bold=ishead)
            if ishead:
                shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EDEFF1');cell._tc.get_or_add_tcPr().append(shade)
    p=para('Note. '+info['note'],'body',8)
    p.paragraph_format.line_spacing=1;p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(7)
    p.paragraph_format.keep_with_next=False

def figure(key):
    cfg={
        'model':('model_specifications.png','Figure 1. Original M0 paths (solid) and additional exploratory M1 paths (dashed). Each construct has four reflective indicators. The three exogenous constructs are permitted to covary; covariances and measurement links are omitted for clarity. The diagram denotes statistical specifications, not established causal effects.'),
        'forest':('M1_paths_to_intention.png','Figure 2. Corrected native M1 paths into Adoption Intention, with 95% percentile bootstrap intervals (10,000 resamples). The AIR interval crosses zero. All estimates are exploratory, based on the same concept-evaluation sample; they do not resolve the HTMT limitations.')}
    file,caption=cfg[key]
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True
    p.paragraph_format.space_before=Pt(4);p.paragraph_format.space_after=Pt(2)
    p.add_run().add_picture(str(FIG/file),width=Cm(17.2 if key=='model' else 15.9))
    c=para(caption,'figure_caption',9)
    c.paragraph_format.space_before=Pt(2);c.paragraph_format.space_after=Pt(9);c.paragraph_format.line_spacing=1
    c.paragraph_format.keep_with_next=False

sectionnum=0;subnum=0
for block in re.split(r'\n\s*\n',resolved.strip()):
    if block.startswith('# '):
        text=block[2:].strip();subnum=0
        if text.startswith('Appendix') or text=='References':label=text
        else:sectionnum+=1;label=f'{sectionnum}. '+text
        heading(label,1)
    elif block.startswith('## '):
        subnum+=1;heading(f'{sectionnum}.{subnum}. '+block[3:].strip(),2)
    elif re.fullmatch(r'\[\[TABLE:(\w+)\]\]',block):table(re.fullmatch(r'\[\[TABLE:(\w+)\]\]',block).group(1))
    elif re.fullmatch(r'\[\[FIG:(\w+)\]\]',block):figure(re.fullmatch(r'\[\[FIG:(\w+)\]\]',block).group(1))
    elif block=='[[REFERENCES]]':
        for i,k in enumerate(citation_order,1):
            p=doc.add_paragraph(style='references')
            ref=REFS[k]
            # Journal template allows et al. for six or more authors; all names remain traceable in the source list.
            runtext(p,f'[{i}] '+ref,10)
            p.paragraph_format.keep_together=True;p.paragraph_format.keep_with_next=False
            p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(6)
            p.paragraph_format.left_indent=Cm(.5);p.paragraph_format.first_line_indent=Cm(-.5)
    else:body(block.replace('\n',' '))

path=OUT/'KidSense_JADS_Draft_Paper.docx'
doc.save(path)
# The old template's orphaned footnote text contains fictitious sample DOI/rights.
# Remove obsolete footnote entries (their references were removed with sample body).
import zipfile
from lxml import etree
temp=path.with_suffix('.tmp.docx')
with zipfile.ZipFile(path) as src,zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as dst:
    for zi in src.infolist():
        data=src.read(zi.filename)
        if zi.filename=='word/footnotes.xml':
            tree=etree.fromstring(data)
            for el in list(tree):
                if int(el.get(qn('w:id'),'0'))>0:tree.remove(el)
            data=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
        dst.writestr(zi,data)
temp.replace(path)

md=resolved.replace('[[REFERENCES]]','\n\n'.join(f'[{i}] {REFS[k]}' for i,k in enumerate(citation_order,1)))
for key,t in tables.items():
    rows=[t['headers'],['---']*len(t['headers'])]+t['rows']
    mdt='\n'.join('| '+' | '.join(str(c) for c in row)+' |' for row in rows)
    md=md.replace('[[TABLE:'+key+']]','**'+t['title']+'**\n\n'+mdt+'\n\nNote. '+t['note'])
md=md.replace('[[FIG:model]]','![Figure 1. Original and exploratory model specifications](../figures/model_specifications.png)')
md=md.replace('[[FIG:forest]]','![Figure 2. Exploratory native M1 paths into intention](../figures/M1_paths_to_intention.png)')
(OUT/'KidSense_JADS_Draft_Paper.md').write_text('# '+TITLE+'\n\nRatih Titi Komala Sari; Widowati; Adi Wibowo\n\nCorresponding author: ratihtiti@students.undip.ac.id\n\n## Abstract\n\n'+ABSTRACT+'\n\nKeywords: '+KEYWORDS+'\n\n'+md)
(OUT/'paper_tables_full_precision_sources.json').write_text(json.dumps({'tables_display':tables,'source_paths':{'M0':str(V/'native_bootstrap/native_structural_verification.json'),'M1':str(V/'native_M1_corrected/native_M1_verified.json'),'HTMT':str(V/'native_htmt_one_sided/verification.json'),'prediction':str(V/'native_prediction/prediction/native_prediction_validation.json'),'CVPAT':str(V/'native_prediction/native_cvpat_verification.json'),'measurement':str(ROOT/'review/measurement_descriptives_M0.csv'),'structural_diagnostics':str(ROOT/'review/structural_diagnostics.json')},'references_in_order':citation_order},ensure_ascii=False,indent=2))
print(json.dumps({'docx':str(path),'abstract_words':len(ABSTRACT.split()),'main_md_words':len(manuscript.split()),'references_used':len(citation_order),'tables':len(tables),'figures':2,'template_sha256':hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()},indent=2))
