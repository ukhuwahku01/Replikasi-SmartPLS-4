"""Audit corrected native seven-path M1; separate points from resampling precision."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,openpyxl
B=Path(__file__).resolve().parent;O=B/'output';O.mkdir(exist_ok=True)
N=Path('/workspace/attachments/510e4ab6-8e13-4421-bf7e-f75ae9606f06/KidSense_M1_DenganTR_Bootstrap_10000.xlsx');P=Path('/workspace/validation/construct_review/exploratory_M1/M1_exploratory_results.json');ref=json.loads(P.read_text());reference={r['effect']:r for r in ref['results']}
w=openpyxl.load_workbook(N,data_only=True);s=w['Complete data set'];meta={w['Navigation'].cell(r,2).value:w['Navigation'].cell(r,3).value for r in range(4,9)}
def means(first,last):
 return {s.cell(r,2).value:{'estimate':s.cell(r,3).value,'bootstrap_mean':s.cell(r,4).value,'bootstrap_SE':s.cell(r,5).value,'t':s.cell(r,6).value,'p':s.cell(r,7).value,'source_row':r} for r in range(first,last+1)}
def bounds(first,last,bc=False):return {s.cell(r,2).value:[s.cell(r,6 if bc else 5).value,s.cell(r,7 if bc else 6).value] for r in range(first,last+1)}
settings={s.cell(r,2).value:s.cell(r,3).value for r in [702,703,704,705,706,707,713,714,715,716,717,718,719,720]}
assert int(settings['Samples'])==10000 and settings['Complexity']=='Complete (slower)' and settings['Confidence interval method']=='Percentile bootstrap' and settings['Test type']=='Two-tailed' and float(settings['Significance level'])==.05
assert s.cell(771,2).value=='All calculations done.'
paths=means(12,18);indirect=means(75,77);totals=means(98,104);r2=means(293,294)
ci_path=bounds(23,29);ci_ind=bounds(82,84);ci_total=bounds(109,115);ci_r2=bounds(299,300)
bc_path=bounds(34,40,True);bc_ind=bounds(89,91,True);bc_total=bounds(120,126,True)
assert set(paths)==set(ref['M1_paths'])
rows=[];comparison=[]
def add(kind,effect,row,ci,ref_label=None,bc=None):
 label=ref_label or effect;py=reference[label];r=dict(kind=kind,effect=effect,**row,CI95_percentile_low=ci[0],CI95_percentile_high=ci[1],CI_excludes_zero=bool(ci[0]>0 or ci[1]<0),status='NATIVE SmartPLS M1 corrected seven-path model')
 if bc:r['BC_CI95_low'],r['BC_CI95_high']=bc
 if kind!='r2':assert abs(r['t']-abs(r['estimate'])/r['bootstrap_SE'])<1e-10
 for name,a,b,typ in [('estimate',r['estimate'],py['estimate'],'point'),('SE',r['bootstrap_SE'],py['bootstrap_SE'],'bootstrap'),('CI95_low',ci[0],py['CI95_percentile_low'],'bootstrap'),('CI95_high',ci[1],py['CI95_percentile_high'],'bootstrap')]:
  comparison.append(dict(kind=kind,effect=effect,metric=name,native=a,Python_M1=b,abs_difference=abs(a-b),comparison_type=typ,source_row=r['source_row']))
 r['Python_CI_decision_agrees']=r['CI_excludes_zero']==py['CI_excludes_zero'];assert r['Python_CI_decision_agrees']
 rows.append(r);return r
for k,r in paths.items():paths[k]=add('path',k,r,ci_path[k],bc=bc_path[k])
for k,r in indirect.items():
 indirect[k]=add('specific_indirect',k,r,ci_ind[k],bc=bc_ind[k]);a=k.split(' -> ')[0];product=paths[a+' -> TR']['estimate']*paths['TR -> AD']['estimate'];assert abs(product-r['estimate'])<1e-12
for a in ['AIR','EXP','PP']:
 k=a+' -> AD';totals[k]=add('total_association',a+' total -> AD',totals[k],ci_total[k],bc=bc_total[k]);assert abs(totals[k]['estimate']-paths[k]['estimate']-indirect[a+' -> TR -> AD']['estimate'])<1e-12
for k,r in r2.items():r2[k]=add('r2','R2 '+k,r,ci_r2[k])
fit=[]
for metric,start in [('SRMR',664),('d_ULS',674),('d_G',684)]:
 for rr in range(start,start+4):
  a=s.cell(rr,3).value;hi95=s.cell(rr,5).value;hi99=s.cell(rr,6).value;fit.append({'metric':metric,'model':s.cell(rr,2).value,'original':a,'HI95':hi95,'HI99':hi99,'belowHI95':a<hi95,'belowHI99':a<hi99,'source_row':rr})
 # Same fitted score covariance is expected for the complete recursive structure.
 for offset in [0,2]:assert abs(s.cell(start+offset,3).value-s.cell(start+offset+1,3).value)<1e-12
out={'source':N.name,'source_path':str(N),'source_sha256':hashlib.sha256(N.read_bytes()).hexdigest(),'metadata':meta,'settings':settings,'paths':paths,'indirect':indirect,'totals':{a+' -> AD':totals[a+' -> AD'] for a in ['AIR','EXP','PP']},'r2':r2,'results':rows,'comparisons':comparison,'fit':fit,'point_comparison_count':len([r for r in comparison if r['comparison_type']=='point']),'max_point_difference':max(r['abs_difference'] for r in comparison if r['comparison_type']=='point'),'max_CI_boundary_difference':max(r['abs_difference'] for r in comparison if r['metric'].startswith('CI95')),'all_CI_decisions_agree_with_Python':all(r['Python_CI_decision_agrees'] for r in rows),'native_M1_inference_now_available':True,'limitations':['M1 is posthoc exploratory, not confirmation of newly specified theory or causality.','Structural score covariance is saturated; estimated/saturated fit equality does not independently confirm added paths.','Only fixed seed label exported, no numeric seed/draws; bootstrap intervals differ from independent Python streams.','HTMT point statistics unchanged with same item sets; prior nativeBCa one-sided95 criterion still fails EXP-PP and EXP-AD.','Current HTMT interval headers are two-sided2.5% and97.5%; not a new one-sided95BCa run.','M1 native prediction/CVPAT not supplied; M0 prediction results must not be relabelled M1.']}
(B/'native_M1_verified.json').write_text(json.dumps(out,indent=2));pd.DataFrame(comparison).to_csv(O/'M1_native_vs_Python.csv',index=False);pd.DataFrame(rows).to_csv(O/'M1_native_effects.csv',index=False);pd.DataFrame(fit).to_csv(O/'M1_native_fit.csv',index=False)
print(json.dumps({k:v for k,v in out.items() if k in ['settings','point_comparison_count','max_point_difference','max_CI_boundary_difference','all_CI_decisions_agree_with_Python']},indent=2))
print(pd.DataFrame(rows)[['kind','effect','estimate','p','CI95_percentile_low','CI95_percentile_high']].to_string(index=False))
