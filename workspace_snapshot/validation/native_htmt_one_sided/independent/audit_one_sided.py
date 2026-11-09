#!/usr/bin/env python3
"""Read and audit native one-tailed selected-BCa HTMT output, preserving methods.
This validates exported bounds and comparisons, not SmartPLS BCa internals/draws.
"""
from pathlib import Path
import hashlib,json,math
from openpyxl import load_workbook
OUT=Path('/workspace/validation/native_htmt_one_sided/independent')
NEW=Path('/workspace/attachments/666e1de7-a27b-4946-9db1-3c78729861ed/KidSense_HTMT_BCa_10000_OneTailed.xlsx')
OLD=Path('/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx')
PYTHON=Path('/workspace/attachments/d0bcb909-7b59-4061-ba39-2de66241055c/KidSense_HTMT_10000_validation.json')
ORDER=['AIR','EXP','PP','TR','AD']
def norm(s):return '-'.join(sorted((a.strip() for a in s.split('<->')),key=ORDER.index))
def read(path):
 s=load_workbook(path,data_only=True)['Complete data set']
 def table(first,last,corrected=False):
  return {norm(s.cell(i,2).value):{'source_row':i,'label':s.cell(i,2).value,'point':s.cell(i,3).value,'mean':s.cell(i,4).value,'lower':s.cell(i,6 if corrected else 5).value,'upper':s.cell(i,7 if corrected else 6).value,**({'bias':s.cell(i,5).value} if corrected else {})} for i in range(first,last+1)}
 settings={s.cell(i,2).value:s.cell(i,3).value for i in range(668,708) if s.cell(i,2).value and s.cell(i,3).value is not None}
 headers={'percentile':[s.cell(465,j).value for j in range(2,7)],'corrected':[s.cell(479,j).value for j in range(2,8)]}
 logs=[{'row':i,'text':s.cell(i,2).value} for i in range(713,750) if s.cell(i,2).value]
 return s,table(466,475),table(480,489,True),settings,headers,logs

def main():
 ns,npct,nbc,settings,headers,logs=read(NEW); os,opct,obc,oldsettings,_,_=read(OLD)
 refs={p['pair']:p for p in json.loads(PYTHON.read_text())['pairs']}
 pairs=[];anomalies=[]
 for name,r in refs.items():
  p=npct[name];c=nbc[name]
  for method,t in [('percentile',p),('corrected',c)]:
   if not all(math.isfinite(t[k]) for k in ['point','mean','lower','upper']):anomalies.append(f'{name} {method}: nonfinite value')
   if not(0<t['lower']<t['point']<t['upper']):anomalies.append(f'{name} {method}: point/order/sign anomaly')
   if method=='corrected' and abs((t['mean']-t['point'])-t['bias'])>1e-14:anomalies.append(f'{name}: reported bias not mean-minus-point')
  comparisons={'point_native_minus_python':p['point']-r['HTMT+'],'point_new_minus_oldnative':p['point']-opct[name]['point'],'mean_new_minus_oldnative':p['mean']-opct[name]['mean'],'percentile_upper95_native_minus_python':p['upper']-r['percentile_upper95_one_sided'],'corrected_upper95_native_selected_BCa_minus_python_BC':c['upper']-r['BC_upper95_one_sided'],'percentile_upper95_not_above_prior_upper975':p['upper']<=opct[name]['upper'],'corrected_upper95_not_above_prior_upper975':c['upper']<=obc[name]['upper']}
  pairs.append({'pair':name,'percentile_one_sided':p,'corrected_one_sided_selected_BCa':c,'point_below_090':p['point']<.9,'point_below_085':p['point']<.85,**{f'{m}_upper95_below_{key}':t['upper']<thr for m,t in [('percentile',p),('corrected',c)] for key,thr in [('090',.9),('085',.85),('1',1)]},'comparisons':comparisons})
 counts={f'{m}_upper95_below_{key}':sum(p[f'{m}_upper95_below_{key}'] for p in pairs) for m in ['percentile','corrected'] for key in ['090','085','1']}
 result={'source':str(NEW),'sha256':hashlib.sha256(NEW.read_bytes()).hexdigest(),'settings':settings,'header_rows':headers,'execution_log':logs,'pairs':pairs,'counts':counts,'anomalies':anomalies,'max_abs_point_difference_vs_python':max(abs(p['comparisons']['point_native_minus_python']) for p in pairs),'max_abs_point_difference_vs_prior_native':max(abs(p['comparisons']['point_new_minus_oldnative']) for p in pairs),'max_abs_sample_mean_difference_vs_prior_native':max(abs(p['comparisons']['mean_new_minus_oldnative']) for p in pairs),'max_abs_percentile_upper95_difference_vs_python':max(abs(p['comparisons']['percentile_upper95_native_minus_python']) for p in pairs),'max_abs_corrected_upper95_difference_vs_python_BC':max(abs(p['comparisons']['corrected_upper95_native_selected_BCa_minus_python_BC']) for p in pairs),'limitations':['Method setting explicitly says Bias-corrected and accelerated (BCa) bootstrap; table title says Bias-corrected confidence intervals. Preserve both facts. Do not call these numerically equivalent to prior Python BC without acceleration.','One-tailed alpha .05 setting and 5%/95% endpoint headers directly support using the exported upper95 endpoint for one-sided inference. The pair of displayed endpoints is not a two-sided95% interval.','The numeric seed and per-draw results are absent; full equivalence of resampled draws and BCa internals is not independently checked.','Identical original points and sample means across native exports are consistency evidence, not proof of identical bootstrap draws.','A corrected upper95>=.90 means the specified .90 discriminant-validity criterion is not established; it does not prove HTMT population value>.90.','All upper95<1 supports the weaker <1 criterion only, not universal success at .90.']}
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'independent_one_sided_htmt.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k not in ['pairs','execution_log']},indent=2))
 print('\nPAIR| POINT|PCT_UPPER95|CORRECTED_UPPER95|PCT_PASS.9|CORRECTED_PASS.9|CORRECTED_PASS.85')
 for p in pairs:print(p['pair'],p['percentile_one_sided']['point'],p['percentile_one_sided']['upper'],p['corrected_one_sided_selected_BCa']['upper'],p['percentile_upper95_below_090'],p['corrected_upper95_below_090'],p['corrected_upper95_below_085'])
if __name__=='__main__':main()
