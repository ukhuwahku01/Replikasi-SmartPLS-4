"""Inspect actual model matrices; never infer model identity from filenames."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,openpyxl
BASE=Path('/workspace/validation/native_M1/integrity')
FILES=[Path('/workspace/attachments/7140d531-a2d0-41c7-9894-32ddb8885a16/KidSense_M1_Eksploratori.xlsx'),Path('/workspace/attachments/26bd700e-350c-4942-a407-07f79b4542ff/KidSense_M1_Algorithm.xlsx'),Path('/workspace/attachments/e18b7f20-4dc0-4d43-b5dc-9cdf66b0ef0d/KidSense_M1_Bootstrap_10000.xlsx')]
CSV=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
REFERENCE=Path('/workspace/validation/construct_review/exploratory_M1/M1_exploratory_results.json')
canon=lambda v:str(v).replace('\ufeff','').strip()
source=pd.read_csv(CSV);reference=json.loads(REFERENCE.read_text());rby={r['effect']:r for r in reference['results']};audits=[];comparisons=[]
M1EDGES=sorted([['AIR','TR'],['EXP','TR'],['PP','TR'],['TR','AD'],['AIR','AD'],['EXP','AD'],['PP','AD']])

def read_rows(p):
 w=openpyxl.load_workbook(p,data_only=True);s=w['Complete data set'];rows=[list(r) for r in s.values]
 def val(r,c):return rows[r-1][c-1] if r<=len(rows) and c<=len(rows[r-1]) else None
 def find(label):return next(i+1 for i,row in enumerate(rows) if len(row)>1 and row[1]==label)
 def numeric(v):return isinstance(v,(int,float)) and not isinstance(v,bool)
 def model_matrix(label):
  start=find(label);header=start+1;cols={c:canon(val(header,c)) for c in range(3,len(rows[header-1])+1) if val(header,c)not in [None,'']}
  items=[];r=header+1
  while val(r,2) not in [None,'']:
   for c,name in cols.items():
    v=val(r,c)
    if numeric(v) and v!=0:items.append({'from':canon(val(r,2)),'to':name,'value':float(v),'cell':f"'Complete data set'!{openpyxl.utils.get_column_letter(c)}{r}"})
   r+=1
  return cols,items
 nodecols,inner=model_matrix('Inner model');outercols,outer=model_matrix('Outer model');nodes=list(nodecols.values());edges=sorted([[r['from'],r['to']]for r in inner])
 start=find('Indicator data (original)');header=next(r for r in range(start,start+8)if val(r,2)=='Case index')
 columns=[canon(v)for v in rows[header-1][2:]if v not in [None,'']];data=[];indices=[];r=header+1
 while val(r,2)not in [None,'']:
  indices.append(int(val(r,2)));data.append([val(r,c)for c in range(3,3+len(columns))]);r+=1
 df=pd.DataFrame(data,columns=columns);known=all(c in source.columns for c in columns);subsetdiff=float(np.max(abs(df.to_numpy(float)-source[columns].to_numpy(float))))if known and len(df)==len(source)else None
 nav={str(w['Navigation'].cell(r,2).value):w['Navigation'].cell(r,3).value for r in range(4,9)}
 settingstart=find('Setting');modeStart=find('Construct outer weighting mode');settings={}
 for r in range(settingstart,modeStart):
  if val(r,2)not in [None,'']and val(r,3)not in [None,'']and val(r,2)!=' ':settings[str(val(r,2))]=val(r,3)
 modestart=modeStart+2;modes={};r=modestart
 while val(r,2)not in [None,'']:modes[canon(val(r,2))]=val(r,3);r+=1
 isboot='Bootstrapping' in [v for row in rows for v in row[1:2]]
 def list_table_after(section):
  st=find(section);r=st+1
  while val(r,2)!='List' and r<st+50:r+=1
  if r>=st+50:return[]
  r+=2;out=[]
  while val(r,2) not in [None,'']:
   out.append({'label':canon(val(r,2)),'value':float(val(r,3)),'cell':f"'Complete data set'!C{r}"});r+=1
  return out
 if isboot:
  st=find('Path coefficients');r=st+4;paths=[]
  while val(r,2)not in [None,'']:
   paths.append({'label':canon(val(r,2)),'value':float(val(r,3)),'cell':f"'Complete data set'!C{r}"});r+=1
  st=find('R-square');r=st+4;r2=[]
  while val(r,2)not in [None,'']:
   r2.append({'label':canon(val(r,2)),'value':float(val(r,3)),'cell':f"'Complete data set'!C{r}"});r+=1
  st=find('Outer loadings');r=st+4;loadings=[]
  while val(r,2)not in [None,'']:
   loadings.append({'label':canon(val(r,2)),'value':float(val(r,3)),'cell':f"'Complete data set'!C{r}"});r+=1
  indirect=[]
 else:
  paths=list_table_after('Path coefficients');loadings=list_table_after('Outer loadings');st=find('R-square');r=st+4;r2=[]
  while val(r,2)not in [None,'']:
   r2.append({'label':canon(val(r,2)),'value':float(val(r,3)),'cell':f"'Complete data set'!C{r}"});r+=1
  try:
   st=find('Specific indirect effects');r=st+4;indirect=[]
   while val(r,2)not in [None,'']:
    indirect.append({'label':canon(val(r,2)),'value':float(val(r,3)),'cell':f"'Complete data set'!C{r}"});r+=1
  except StopIteration:indirect=[]
 identity='M1 five-construct partial-mediation model'if edges==M1EDGES and set(nodes)=={'AIR','EXP','PP','TR','AD'}else 'Different four-construct direct-association model; not M1'
 result={'file':p.name,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'metadata':nav,'is_bootstrap_report':isboot,'model_identity_from_matrices':identity,'is_target_M1':edges==M1EDGES and set(nodes)=={'AIR','EXP','PP','TR','AD'},'constructs':nodes,'construct_count':len(nodes),'edges':edges,'edge_count':len(edges),'indicator_count':len(outer),'outer_model_reflective_all':all(z['value']== -1 for z in outer),'outer_model_mapping':outer,'original_data':{'rows':len(df),'columns':len(columns),'column_names':columns,'missing_vs_full20':sorted(set(source.columns)-set(columns)),'row_indices_match':indices==list(range(len(source))),'all_exported_item_values_match_source_subset':subsetdiff==0,'max_abs_value_difference_for_exported_subset':subsetdiff,'full271x20_dataset_embedded':len(df)==271 and set(columns)==set(source.columns)},'settings':settings,'native_outer_modes':modes,'paths':paths,'r2':r2,'loadings':loadings,'specific_indirect':indirect,'comparison_policy':'Only target five-construct M1 is compared to Python M1. Four-construct path coefficients are retained under their own model identity, never substituted into M1.'}
 if result['is_target_M1']:
  for kind,table in [('path',paths),('r2',r2),('loading',loadings),('specific_indirect',indirect)]:
   for a in table:
    if kind=='loading':item,con=a['label'].split(' <- ');exp=reference['M1_loadings'][con][item]
    elif kind=='r2':exp=reference['M1_r2'][a['label']]
    else:exp=rby[a['label']]['estimate']
    comparisons.append({'file':p.name,'model':'M1 five-construct','kind':kind,'label':a['label'],'native':a['value'],'python_M1':exp,'abs_difference':abs(a['value']-exp),'native_cell':a['cell'],'status':'MATCH within1e-8'if abs(a['value']-exp)<=1e-8 else 'DIFFERENCE'})
 return result
for p in FILES:audits.append(read_rows(p))
assert [a['is_target_M1']for a in audits]==[True,False,False]
assert all(a['original_data']['rows']==271 and a['original_data']['all_exported_item_values_match_source_subset']and a['original_data']['row_indices_match']for a in audits)
assert len(comparisons)==32 and all(r['abs_difference']<1e-8 for r in comparisons)
a,b=audits[1],audits[2];cross=[]
for key in ['paths','r2','loadings']:
 amap={r['label']:r for r in a[key]};bmap={r['label']:r for r in b[key]}
 for label,v in amap.items():cross.append({'kind':key,'label':label,'four_construct_algorithm':v['value'],'four_construct_bootstrap_original':bmap[label]['value'],'abs_difference':abs(v['value']-bmap[label]['value'])})
assert max(r['abs_difference']for r in cross)==0
summary={'files':audits,'correct_M1_native_vs_Python':{'scalar_comparisons':len(comparisons),'max_abs_difference':max(r['abs_difference']for r in comparisons),'comparisons':comparisons},'four_construct_algorithm_vs_bootstrap_original':cross,'critical_finding':'Only KidSense_M1_Eksploratori.xlsx corresponds to the intended five-construct M1. The other algorithm and bootstrap files omit TR and its4indicators; they cannot supply M1 bootstrap significance or mediation intervals. Correct M1 native point replication is verified; correct M1 native bootstrap remains unavailable in these3uploads.','no_original_files_modified':True}
BASE.mkdir(parents=True,exist_ok=True);(BASE/'native_M1_model_integrity.json').write_text(json.dumps(summary,indent=2))
pd.DataFrame(comparisons).to_csv(BASE/'correct_M1_native_vs_python_points.csv',index=False)
pd.DataFrame(cross).to_csv(BASE/'four_construct_algorithm_vs_bootstrap.csv',index=False)
pd.DataFrame([{'file':a['file'],'target_M1':a['is_target_M1'],'constructs':','.join(a['constructs']),'construct_count':a['construct_count'],'paths':a['edge_count'],'indicators':a['indicator_count'],'rows':a['original_data']['rows'],'data_match_subset':a['original_data']['all_exported_item_values_match_source_subset'],'full20':a['original_data']['full271x20_dataset_embedded']}for a in audits]).to_csv(BASE/'three_file_model_identity.csv',index=False)
print(pd.read_csv(BASE/'three_file_model_identity.csv').to_string(index=False));print('CorrectM1pointmaxdiff',summary['correct_M1_native_vs_Python']['max_abs_difference']);print('Correct M1 comparisons',len(comparisons));print('Four-modelpointcrossmaxdiff',max(r['abs_difference']for r in cross))
