"""Classify actual SmartPLS models in three uploads; filenames are not authority."""
from pathlib import Path
import json,hashlib,sys
import numpy as np,pandas as pd,openpyxl
B=Path(__file__).resolve().parent;O=B/'output';O.mkdir(exist_ok=True)
F={
'KidSense_M1_Eksploratori.xlsx':Path('/workspace/attachments/7140d531-a2d0-41c7-9894-32ddb8885a16/KidSense_M1_Eksploratori.xlsx'),
'KidSense_M1_Algorithm.xlsx':Path('/workspace/attachments/26bd700e-350c-4942-a407-07f79b4542ff/KidSense_M1_Algorithm.xlsx'),
'KidSense_M1_Bootstrap_10000.xlsx':Path('/workspace/attachments/e18b7f20-4dc0-4d43-b5dc-9cdf66b0ef0d/KidSense_M1_Bootstrap_10000.xlsx')}
ref=json.loads(Path('/workspace/validation/construct_review/exploratory_M1/M1_exploratory_results.json').read_text());refrows={r['effect']:r for r in ref['results']}
expected=set(ref['M1_paths']);summaries=[];points=[]
def locate(s,text,start=1):
 return next(r for r in range(start,s.max_row+1) if s.cell(r,2).value==text)
def block(s,title):
 p=locate(s,title);r=p+1
 while s.cell(r,2).value is None:r+=1
 headers=[str(s.cell(r,c).value or '').replace('\ufeff','') for c in range(3,s.max_column+1)];cols=[(c,n) for c,n in enumerate(headers,3) if n]
 data=[];r+=1
 while s.cell(r,2).value is not None:
  label=str(s.cell(r,2).value).replace('\ufeff','');data.append((r,label,{n:s.cell(r,c).value for c,n in cols}));r+=1
 return cols,data
for name,path in F.items():
 w=openpyxl.load_workbook(path,data_only=True);s=w['Complete data set'];meta={w['Navigation'].cell(r,2).value:w['Navigation'].cell(r,3).value for r in range(4,9)}
 cols,model=block(s,'Inner model');constructs=[n for _,n in cols];edges=[]
 for rr,src,values in model:
  for dest,value in values.items():
   if isinstance(value,(int,float)) and value!=0:edges.append(src+' -> '+dest)
 _,outer=block(s,'Outer model');items=[label for rr,label,values in outer]
 paths={}
 start=locate(s,'Path coefficients')
 if 'Bootstrap' in name:
  first=locate(s,'Mean, STDEV, T values, p values',start)+2;rr=first
  while s.cell(rr,2).value is not None:
   paths[s.cell(rr,2).value]={'estimate':s.cell(rr,3).value,'SE':s.cell(rr,5).value,'t':s.cell(rr,6).value,'p':s.cell(rr,7).value,'row':rr};rr+=1
  ci_start=locate(s,'Confidence intervals',start)+2
  for rr in range(ci_start,ci_start+len(paths)):
   k=s.cell(rr,2).value;paths[k]['CI_low']=s.cell(rr,5).value;paths[k]['CI_high']=s.cell(rr,6).value
   assert abs(paths[k]['t']-abs(paths[k]['estimate'])/paths[k]['SE'])<1e-12
 else:
  rr=locate(s,'List',start)+2
  while s.cell(rr,2).value is not None:paths[s.cell(rr,2).value]={'estimate':s.cell(rr,3).value,'row':rr};rr+=1
 # R-square estimates, keeping native provenance.
 rp=locate(s,'R-square');head=locate(s,'Mean, STDEV, T values, p values',rp) if 'Bootstrap' in name else locate(s,'Overview',rp)
 rr=head+2;r2={}
 while s.cell(rr,2).value is not None:r2[str(s.cell(rr,2).value)]=s.cell(rr,3).value;rr+=1
 settings={k:s.cell(r,3).value for r in range(1,s.max_row+1) if (k:=s.cell(r,2).value) in ['Weighting scheme','Type of results','Complexity','Confidence interval method','Test type','Significance level','Samples','Seed','Parallel processing']}
 correct=set(edges)==expected and set(constructs)=={'AIR','EXP','PP','TR','AD'} and len(items)==20
 row={'file':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'metadata':meta,'constructs':constructs,'n_constructs':len(constructs),'n_items_in_model':len(items),'n_paths':len(edges),'paths':paths,'edges':edges,'missing_expected_M1_paths':sorted(expected-set(edges)),'extra_paths':sorted(set(edges)-expected),'contains_TR':'TR' in constructs,'model_items':items,'R2':r2,'settings':settings,'correct_M1_structure':correct,'status':'M1 algorithm correct; bootstrap still needed' if correct else 'Different direct-only model withoutTR; cannot substitute M1','indirect_available':'Specific indirect effects' in [s.cell(r,2).value for r in range(1,s.max_row+1)] and 'TR' in constructs}
 if correct:
  for k,v in paths.items():points.append({'metric':'path','label':k,'native':v['estimate'],'Python_M1':refrows[k]['estimate'],'abs_difference':abs(v['estimate']-refrows[k]['estimate']),'source_row':v['row']})
  p=locate(s,'Specific indirect effects');rr=locate(s,'Matrix',p)+2
  while s.cell(rr,2).value is not None:
   k=s.cell(rr,2).value;v=s.cell(rr,3).value
   if k in refrows:points.append({'metric':'specific_indirect','label':k,'native':v,'Python_M1':refrows[k]['estimate'],'abs_difference':abs(v-refrows[k]['estimate']),'source_row':rr})
   rr+=1
  for k,v in r2.items():points.append({'metric':'R2','label':k,'native':v,'Python_M1':ref['M1_r2'][k],'abs_difference':abs(v-ref['M1_r2'][k]),'source_row':None})
 summaries.append(row)
assert len([r for r in summaries if r['correct_M1_structure']])==1
assert max(r['abs_difference'] for r in points)<1e-8
bad_algo=next(r for r in summaries if r['file']=='KidSense_M1_Algorithm.xlsx');bad_boot=next(r for r in summaries if r['file']=='KidSense_M1_Bootstrap_10000.xlsx')
assert set(bad_algo['edges'])==set(bad_boot['edges'])
assert all(abs(bad_algo['paths'][k]['estimate']-v['estimate'])<1e-14 for k,v in bad_boot['paths'].items())
result={'files':summaries,'M1_point_comparisons':points,'point_comparison_count':len(points),'max_M1_point_abs_difference':max(r['abs_difference'] for r in points),'native_M1_bootstrap_available':False,'conclusion':'One correct5construct20item7path M1 algorithm export, but uploaded bootstrap and namedAlgorithm use a4construct16item3path direct-only model withoutTR. Do not join bootstrap to the correct M1 point estimates.','needed':'Bootstrap10000 two-sided percentile from the actual KidSense_M1_Eksploratori model withTR and all7paths.','original_files_modified':False}
(B/'export_audit.json').write_text(json.dumps(result,indent=2));pd.DataFrame(points).to_csv(O/'M1_point_comparison.csv',index=False)
print(json.dumps({'files':[{k:r[k] for k in ['file','metadata','constructs','n_items_in_model','n_paths','R2','correct_M1_structure']} for r in summaries],'point_comparison_count':len(points),'max_M1_point_abs_difference':result['max_M1_point_abs_difference']},indent=2))
