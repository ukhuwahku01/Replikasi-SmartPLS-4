"""Audit native SmartPLS bootstrap export against previously verified Python.
Uploaded artifacts are evidence; no source files or source methods are edited.
"""
from pathlib import Path
import json,hashlib,math,sys
import numpy as np,pandas as pd,openpyxl
from scipy.stats import norm
BASE=Path(__file__).resolve().parent
SOURCE=Path('/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx')
PYREF=Path('/workspace/attachments/fb78389c-5aaa-4cde-9053-ec03d7da31b6/KidSense_PLS_10000_results.json')
w=openpyxl.load_workbook(SOURCE,data_only=True);s=w['Complete data set'];ref=json.loads(PYREF.read_text())
def rows(first,last):
 return {str(s.cell(r,2).value).replace('\ufeff',''):dict(O=s.cell(r,3).value,M=s.cell(r,4).value,SE=s.cell(r,5).value,t=s.cell(r,6).value,p=s.cell(r,7).value,excel_row=r) for r in range(first,last+1)}
def ci(first,last,bc=False):
 return {str(s.cell(r,2).value).replace('\ufeff',''):[s.cell(r,6 if bc else 5).value,s.cell(r,7 if bc else 6).value] for r in range(first,last+1)}
paths=rows(12,15);pathci=ci(20,23);bc=ci(28,31,True);f2=rows(324,327)
vif={str(s.cell(r,2).value):s.cell(r,3).value for r in range(620,624)}
ind=rows(66,68);indci=ci(73,75);r2=rows(284,285);r2ci=ci(290,291)
comparisons=[]
def check(group,label,metric,a,b,kind='point',location=None):
 comparisons.append(dict(group=group,label=label,metric=metric,Python=b,SmartPLS=a,signed_difference=a-b,absolute_difference=abs(a-b),comparison_kind=kind,source_row=location,status=('COCOK (<1e-8)' if abs(a-b)<1e-8 else 'BERBEDA: resampling/konvensi' if kind=='bootstrap' else 'PERIKSA')))
for p in ref['paths']:
 label=p['path'];r=paths[label]
 for k,a,b in [('beta',r['O'],p['beta']),('f2',f2[label]['O'],p['f2']),('VIF',vif[label],p['VIF'])]:check('paths',label,k,a,b,location=r['excel_row'])
 for k,a,b in [('SE',r['SE'],p['se']),('t',r['t'],p['t']),('p_reported',r['p'],p['p']),('CI95_low',pathci[label][0],p['ci95'][0]),('CI95_high',pathci[label][1],p['ci95'][1])]:check('paths',label,k,a,b,'bootstrap',r['excel_row'])
 r['ci95_percentile']=pathci[label];r['ci95_bias_corrected']=bc[label]
 r['t_independent_beta_over_SE']=abs(r['O'])/r['SE'];r['t_arithmetic_abs_error']=abs(r['t']-r['t_independent_beta_over_SE'])
 r['p_normal_recomputed']=float(2*norm.sf(r['t']));r['SE_relative_difference_vs_Python']=(r['SE']-p['se'])/p['se']
 r['significant_005_reported_p']=bool(r['p']<.05);r['CI_excludes_zero']=bool(pathci[label][0]*pathci[label][1]>0)
for p in ref['indirect']:
 label=p['effect'];r=ind[label];check('indirect',label,'beta',r['O'],p['beta'],location=r['excel_row'])
 for j,k in enumerate(['CI95_low','CI95_high']):check('indirect',label,k,indci[label][j],p['ci95'][j],'bootstrap',r['excel_row'])
 a=label.split(' -> ')[0];r['product_of_paths']=paths[a+' -> TR']['O']*paths['TR -> AD']['O'];r['product_absolute_error']=abs(r['product_of_paths']-r['O']);r['ci95_percentile']=indci[label]
 r['t_arithmetic_abs_error']=abs(r['t']-abs(r['O'])/r['SE'])
 r['significant_005_reported_p']=bool(r['p']<.05);r['CI_excludes_zero']=bool(indci[label][0]*indci[label][1]>0)
for p in ref['r2']:
 label=p['construct'];r=r2[label];check('r2',label,'R2',r['O'],p['r2'],location=r['excel_row'])
 for j,k in enumerate(['CI95_low','CI95_high']):check('r2',label,k,r2ci[label][j],p['ci95'][j],'bootstrap',r['excel_row'])
 r['ci95_percentile']=r2ci[label]
settings={str(s.cell(r,2).value):s.cell(r,3).value for r in [678,679,680,681,682,683,689,690,691,692,693,694,695,696]}
assert int(settings['Samples'])==10000 and settings['Complexity']=='Complete (slower)' and settings['Confidence interval method']=='Percentile bootstrap' and settings['Test type']=='Two-tailed'
assert float(settings['Significance level'])==.05 and settings['Weighting scheme']=='Path' and settings['Type of results']=='Standardized'
assert all(r['t_arithmetic_abs_error']<1e-10 for r in list(paths.values())+list(ind.values()))
assert all(r['product_absolute_error']<1e-12 for r in ind.values())
assert all(c['absolute_difference']<1e-8 for c in comparisons if c['comparison_kind']=='point')
fits=[]
for section,start in [('SRMR',640),('d_ULS',650),('d_G',660)]:
 for rr in range(start,start+4):
  model=s.cell(rr,2).value;a=s.cell(rr,3).value;hi95=s.cell(rr,5).value;hi99=s.cell(rr,6).value
  fits.append(dict(metric=section,model=model,original=a,HI95=hi95,HI99=hi99,original_below_HI95=a<hi95,original_below_HI99=a<hi99,source_row=rr))
meta={str(w['Navigation'].cell(r,2).value):w['Navigation'].cell(r,3).value for r in range(4,9)}
point=[c for c in comparisons if c['comparison_kind']=='point'];bootstrap=[c for c in comparisons if c['comparison_kind']=='bootstrap']
result={'source_file':SOURCE.name,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'metadata':meta,'settings':settings,'paths':paths,'indirect':ind,'r2':r2,'comparison':comparisons,'fit':fits,'point_comparisons':len(point),'max_point_abs_difference':max(c['absolute_difference'] for c in point),'max_SE_relative_difference':max(abs(p['SE_relative_difference_vs_Python']) for p in paths.values()),'max_CI_boundary_difference':max(c['absolute_difference'] for c in bootstrap if 'CI95' in c['metric']),'execution_log_complete':s.cell(747,2).value=='All calculations done.','limitations':['Bootstrapping data per sample were not saved; native draws cannot be reproduced or compared row-by-row from this export.','Only Fixed seed is recorded; no numeric seed value is exposed. Do not claim this was seed 20261106.','Native and Python bootstrap SE/intervals differ; RNG/resampling/implementation differences are plausible, but the exact source is not identifiable from saved output.','Native reported p values differ from Python normal approximation; some very small exported p values repeat at 5.684341886080802e-14. Preserve software-reported values; use p<0.001 in the prose.','HTMT intervals in this run are two-sided 2.5%/97.5%; target one-sided BC upper95 is not present.','No PLSpredict or CVPAT native execution is included in this workbook.']}
(BASE/'native_structural_verification.json').write_text(json.dumps(result,indent=2))
pd.DataFrame(comparisons).to_csv(BASE/'native_vs_python_structural.csv',index=False)
pd.DataFrame(fits).to_csv(BASE/'native_model_fit.csv',index=False)
print(json.dumps({k:v for k,v in result.items() if k not in ['comparison','fit','limitations']},indent=2))
