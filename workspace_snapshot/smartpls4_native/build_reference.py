from pathlib import Path
import json,hashlib,shutil,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
BASE=Path('/workspace/smartpls4_native');ATT=Path('/workspace/attachments')
def load(n):return json.loads(next(ATT.rglob(n)).read_text())
p=load('KidSense_PLS_10000_results.json');h=load('KidSense_HTMT_10000_validation.json');c=load('KidSense_CV_Prediction_Exploratory.json')
v=json.loads(Path('/workspace/validation/pls_point_verification.json').read_text())
src=next(ATT.rglob('KidSense_SmartPLS4_Input_271.csv'));dst=BASE/src.name;shutil.copyfile(src,dst)
sha=hashlib.sha256(dst.read_bytes()).hexdigest();assert sha==hashlib.sha256(src.read_bytes()).hexdigest()
w=openpyxl.Workbook();w.remove(w.active)
def sheet(name,headers,rows):
 s=w.create_sheet(name);s.append(headers)
 for row in rows:s.append(list(row))
 s.freeze_panes='A2';s.auto_filter.ref=s.dimensions
 for cc in s[1]:cc.font=Font(bold=True,color='FFFFFF');cc.fill=PatternFill('solid',fgColor='17365D');cc.alignment=Alignment(wrap_text=True)
 s.row_dimensions[1].height=32
 for row in s.iter_rows(min_row=2):
  for cc in row:
   cc.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(cc.value,float):cc.number_format='0.0000000000'
  if row[0].row%2==0:
   for cc in row:cc.fill=PatternFill('solid',fgColor='EEF3F8')
 for i,col in enumerate(s.columns,1):s.column_dimensions[get_column_letter(i)].width=min(72,max(14,max(len(str(x.value or '')) for x in col)+2))
 return s
sheet('START_HERE',['Field','Value'],[
 ['Status','PYTHON REFERENCE ONLY — no native SmartPLS 4 execution or exports yet.'],
 ['Purpose','Compare actual SmartPLS 4 exports against independently validated Python calculations; empty native fields must be filled only from genuine native exports.'],
 ['Input CSV','KidSense_SmartPLS4_Input_271.csv'],['SHA256 actual CSV',sha],['Dimensions','271 rows, 20 item columns, integer 1–5, no missing values.'],
 ['Model','AIR1–4→AIR, EXP1–4→EXP, PP1–4→PP, TR1–4→TR, AD1–4→AD, all reflective; AIR/EXP/PP→TR and TR→AD.'],
 ['Point reference','Custom Python PLS-PM Mode A, path weighting; not PLSc or covariance-based SEM.'],
 ['Bootstrap reference','10,000 resamples; four NumPy RNG streams seeds 20261106–20261109, 2,500 each. A native single RNG seed will not recreate identical resample draws.'],
 ['HTMT reference','HTMT+ absolute Pearson correlations; seed 20261105; percentile and bias-corrected BC (not BCa) intervals.'],
 ['CV reference','Exploratory 10×10-fold Python CV; not native SmartPLS PLSpredict or CVPAT. AD uses observed test TR indicators, making predictions conditional.'],
 ['Critical HTMT finding','One-sided BC upper95 >=0.90 for EXP–PP and EXP–AD; do not claim all construct pairs pass discriminant-validity inference.'],
 ['Source lineage','Hash recorded in HTMT/CV JSON differs from actual CSV hash. Raw 323 responses, exclusion flags, D1/D2 flags and timestamps not supplied.'],
 ['Native run record','Record app version/build, platform, license/trial status, all algorithm settings, random seed, date, sample count, convergence and exports. Do not record secret license keys.'],
 ['Note','Settings/checklist are proposed replication protocol, not evidence that SmartPLS has run.']])
HEAD=['Entity','Metric','Python reference value','Native SmartPLS 4 value','Native export file / cell','Comparison note']
def long(name,rows):
 s=sheet(name,HEAD,[[ent,met,val,None,None,note] for ent,met,val,note in rows]);s.column_dimensions['D'].width=25;s.column_dimensions['E'].width=32;return s
rows=[]
for r in p['paths']:
 for metric in ['beta','se','t','p','f2','VIF']:rows.append([r['path'],metric,r[metric],'p is normal two-sided approximation; bootstrap variation is expected across software/RNGs.' if metric in ['p','se','t'] else 'Compare equivalent settings and standardized estimates.'])
 for j,key in enumerate(['CI95 percentile lower','CI95 percentile upper']):rows.append([r['path'],key,r['ci95'][j],'Two-sided 95% percentile CI; not one-sided BC interval.'])
long('Paths',rows)
long('R2',[[r['construct'],key,val,'Bootstrap intervals may differ due to RNG/settings.'] for r in p['r2'] for key,val in [('R2',r['r2']),('CI95 percentile lower',r['ci95'][0]),('CI95 percentile upper',r['ci95'][1])]])
long('Indirect',[[r['effect'],key,val,'Specific indirect association; no direct exogenous→AD path in reference model. Association is not proof of causal mediation.'] for r in p['indirect'] for key,val in [('beta',r['beta']),('CI95 percentile lower',r['ci95'][0]),('CI95 percentile upper',r['ci95'][1])]])
rows=[]
for r in v['reliability']:
 for metric in ['alpha_standardized','alpha_raw','rho_C','AVE','loading_min','loading_max','mean']:rows.append([r['construct'],metric,r[metric],'Match raw vs standardized alpha definitions. Min/max loadings are only summaries; export all 20 loadings.'])
 rows.append([r['construct'],'rho_A',None,'Not available in Python reference; obtain from genuine native SmartPLS output. Do not invent.'])
long('Reliability',rows)
rows=[]
for r in h['pairs']:
 for metric in ['HTMT+','percentile_upper95_one_sided','BC_upper95_one_sided','BC_upper97.5_two_sided']:rows.append([r['pair'],metric,r[metric],'Discriminant criterion in source: BC upper95 ONE-SIDED <0.90. BC is not BCa; verify software interval method.'])
 for j,metric in enumerate(['percentile CI95 TWO-SIDED lower','percentile CI95 TWO-SIDED upper']):rows.append([r['pair'],metric,r['percentile_CI95_two_sided'][j],'Do not compare directly with a one-sided upper95 boundary.'])
long('HTMT',rows)
rows=[]
for r in c['indicators']:
 for metric in ['RMSE_PLS_exploratory','RMSE_IA_mean','RMSE_LM','MAE_PLS_exploratory','MAE_IA_mean','MAE_LM','Q2_predict_analogue']:
  rows.append([r['indicator'],metric,r[metric],'Exploratory Python CV; native predictions may differ in folds, weighting, and prediction design. AD reference is conditional on observed TR.'])
long('Prediction',rows)
check=[
 ['Before calculation','Record SmartPLS version/build, platform, license/trial availability and sample n=271; preserve input checksum.'],
 ['Model','Export model diagram/project with five reflective four-item blocks and four paths AIR/EXP/PP→TR; TR→AD only.'],
 ['Algorithm','Export algorithm settings, convergence status, outer weights, all 20 loadings, latent scores if available, reliability alpha/rho_A/rho_C/AVE.'],
 ['Structural','Export standardized beta, R²/adjusted R², inner VIF, f², total and specific indirect effects.'],
 ['Bootstrap paths','Use 10,000 resamples; record seed, sign-change settings and all options. Export SE/t/p and TWO-SIDED 95% PERCENTILE CIs.'],
 ['Bootstrap HTMT','Use 10,000 resamples; export HTMT point values and ONE-SIDED 95% BIAS-CORRECTED upper limits, cutoff 0.90. Verify exact interval naming in your version.'],
 ['HTMT interpretation','Check EXP–PP and EXP–AD; assess point cutoff separately from inferential upper bound. Do not substitute two-sided or BCa intervals.'],
 ['Prediction','Run native PLSpredict with 10 folds × 10 repetitions where available. Export Q²predict, PLS and LM RMSE/MAE at indicator level; save settings and fold/seed controls.'],
 ['CVPAT','Only report CVPAT if it was actually executed; export loss differences and statistical tests separately. No reference CVPAT result is available.'],
 ['Comparison','Enter native numbers only from genuine exports; record source file/cell, algorithm/CI differences and Monte Carlo variation rather than forcing a numerical match.'],
 ['Final package','Retain original input CSV, native project file, all native exports, screenshots/settings and difference log. Do not overwrite Python reference columns.']]
sheet('Export_Checklist',['Stage','Required native evidence'],check)
sheet('Run_Record',['Field','Native run value'],[[k,None] for k in ['SmartPLS version/build','Platform','Execution date/time/timezone','License/trial usable (no key)','Sample n','Input SHA256','Weighting scheme','Mode A / reflective','PLS vs PLSc','Max iterations','Stop criterion','Bootstrap repetitions','Bootstrap seed','Sign-change settings','Path CI method/sidedness/alpha','HTMT CI method/sidedness/alpha','PLSpredict folds/repetitions','PLSpredict seed/fold method','Prediction design for AD','Convergence status','Native project file','Native export directory']])
file=BASE/'expected_reference.xlsx';w.save(file)
# Verify no native cells contain numbers, formulas or fabricated evidence.
r=openpyxl.load_workbook(file,data_only=False)
for name in ['Paths','R2','Indirect','Reliability','HTMT','Prediction']:
 for row in r[name].iter_rows(min_row=2):assert row[3].value is None and row[4].value is None
for row in r['Run_Record'].iter_rows(min_row=2):assert row[1].value is None
manifest={'status':'prepared_reference_only_native_execution_not_performed','input_file':dst.name,'input_sha256':sha,'input_bytes':dst.stat().st_size,'input_rows':271,'input_columns':20,'original_csv_copied_byte_identical':True,'native_smartpls4_results_present':False,'native_value_fields_empty':True,'reference_workbook':file.name,'reference_workbook_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'source_references':[{'file':q.name,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in ATT.rglob('*') if q.is_file() and q.suffix in ['.csv','.json','.xlsx']],'limitations':['No installed SmartPLS execution or native project file has been generated.','Bootstrap resampling seeds/RNGs and native prediction design may differ from Python.','Original raw 323-response file and eligibility/attention flags are absent.','rho_A reference values are intentionally blank.']}
(BASE/'reference_manifest.json').write_text(json.dumps(manifest,indent=2))
print(file, file.stat().st_size, 'bytes; sheets:',r.sheetnames)
print('Native fields blank verified; CSV copied byte-identical:',sha)
