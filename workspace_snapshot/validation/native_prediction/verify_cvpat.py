"""Reconstruct native CVPAT loss and t statistics from prediction errors.
Reported native p-values are preserved; SciPy t(df=270) is a numerical cross-check.
"""
from pathlib import Path
import json,numpy as np,pandas as pd,openpyxl,hashlib
from scipy.stats import t as student_t
B=Path(__file__).resolve().parent;SRC=Path('/workspace/attachments/c7ccdeb6-0e70-4b07-a755-212a824125ff/KidSense_PLSpredict_10x10.xlsx')
s=openpyxl.load_workbook(SRC,data_only=True)['Complete data set']
PLS=np.load(B/'prediction/native_exported_PLS_errors.npz')['PLS'];err=np.load(B/'prediction/native_reconstructed_errors.npz');n=271
labels=['AD1','AD2','AD3','AD4','TR1','TR2','TR3','TR4'];rows=[]
for level,bench,start,end in [('construct','IA',70,72),('construct','LM',77,79),('indicator','IA',86,93),('indicator','LM',98,105)]:
 for rr in range(start,end+1):
  label=s.cell(rr,2).value
  ix=list(range(8)) if label=='Overall' else list(range(4)) if label=='AD' else list(range(4,8)) if label=='TR' else [labels.index(label)]
  a=(PLS[:,ix]**2).mean(axis=1);b=(err[bench][:,ix]**2).mean(axis=1);delta=a-b
  native=[float(s.cell(rr,c).value) for c in range(3,8)]
  # Native t is reproduced with pooled loss-difference population variance and effective N=271.
  calculated=[float(a.mean()),float(b.mean()),float(delta.mean()),float(abs(delta.mean())/np.sqrt(delta.var(ddof=0)/n))]
  recomputed_p=float(2*student_t.sf(calculated[3],n-1))
  r=dict(level=level,benchmark=bench,target=label,native_PLS_loss=native[0],recomputed_PLS_loss=calculated[0],native_benchmark_loss=native[1],recomputed_benchmark_loss=calculated[1],native_average_loss_difference=native[2],recomputed_average_loss_difference=calculated[2],native_t=native[3],recomputed_t=calculated[3],native_p=native[4],scipy_t270_two_sided_p_check=recomputed_p,p_abs_difference=abs(native[4]-recomputed_p),max_loss_or_t_abs_difference=max(abs(x-y) for x,y in zip(native[:4],calculated)),lower_loss_than_benchmark=bool(native[2]<0),significant_native_p_005=bool(native[4]<.05),better_and_significant_005=bool(native[2]<0 and native[4]<.05),source_row=rr,indicator_LM_Holm_p=None)
  assert abs(native[2]-(native[0]-native[1]))<1e-12
  assert (native[4]<.05)==(recomputed_p<.05)
  assert r['max_loss_or_t_abs_difference']<1e-10
  rows.append(r)
# Exploratory Holm adjustment across the eight LM indicator comparisons; native values preserved.
f=[r for r in rows if r['level']=='indicator' and r['benchmark']=='LM'];rank=sorted(range(8),key=lambda i:f[i]['native_p']);last=0
for k,i in enumerate(rank):
 last=max(last,(8-k)*f[i]['native_p']);f[i]['indicator_LM_Holm_p']=min(1,last)
result={'source':SRC.name,'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'n_respondents':271,'repetitions':10,'predictions_per_indicator':2710,'tests':rows,'max_loss_or_t_absolute_difference':max(r['max_loss_or_t_abs_difference'] for r in rows),'max_p_numeric_crosscheck_difference':max(r['p_abs_difference'] for r in rows),'overall_IA':next(r for r in rows if r['level']=='construct' and r['benchmark']=='IA' and r['target']=='Overall'),'overall_LM':next(r for r in rows if r['level']=='construct' and r['benchmark']=='LM' and r['target']=='Overall'),'indicator_IA_sig_count':sum(r['better_and_significant_005'] for r in rows if r['level']=='indicator' and r['benchmark']=='IA'),'indicator_LM_sig_unadjusted_count':sum(r['better_and_significant_005'] for r in f),'indicator_LM_sig_Holm_count':sum(r['lower_loss_than_benchmark'] and r['indicator_LM_Holm_p']<.05 for r in f),'method_notes':['Loss is squared original-unit indicator prediction error. Construct-level loss averages the four indicator losses; Overall averages all eight. These are not squared latent-score RMSE.','Native t is independently reproduced as abs(mean(delta))/sqrt(population_variance(delta)/271), pooling the 2710 repeated prediction rows while using effective respondent count271. The2710 rows are not2710 distinct respondents.','Native reported p-values are preserved. Numerical t-distribution check with df270 gives same decisions at alpha.05; small numeric differences are retained rather than replaced.','Holm across eight LM indicator tests is supplemental, not a change to the native output. Overall benchmark comparisons are the primary interpretation here.','These computations reproduce the native test output; they do not remove model fit, discriminant validity or data eligibility limitations.']}
(B/'native_cvpat_verification.json').write_text(json.dumps(result,indent=2));pd.DataFrame(rows).to_csv(B/'native_cvpat_comparison.csv',index=False)
print(json.dumps({k:v for k,v in result.items() if k not in ['tests','method_notes']},indent=2))
