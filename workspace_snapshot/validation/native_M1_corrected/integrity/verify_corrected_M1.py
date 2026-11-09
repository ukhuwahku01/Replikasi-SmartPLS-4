"""Read-only data/model/settings and point-estimate audit of corrected native M1."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,openpyxl
BASE=Path('/workspace/validation/native_M1_corrected/integrity')
P=Path('/workspace/attachments/510e4ab6-8e13-4421-bf7e-f75ae9606f06/KidSense_M1_DenganTR_Bootstrap_10000.xlsx')
A=Path('/workspace/attachments/7140d531-a2d0-41c7-9894-32ddb8885a16/KidSense_M1_Eksploratori.xlsx')
CSV=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
J=Path('/workspace/validation/construct_review/exploratory_M1/M1_exploratory_results.json')
canon=lambda v:str(v).replace('\ufeff','').strip()
source=pd.read_csv(CSV);ref=json.loads(J.read_text());rby={r['effect']:r for r in ref['results']}
w=openpyxl.load_workbook(P,data_only=True);s=w['Complete data set'];wa=openpyxl.load_workbook(A,data_only=True);sa=wa['Complete data set']
def find(sheet,label):return next(r[0].row for r in sheet.iter_rows()if len(r)>1 and r[1].value==label)
def boot_table(section):
 st=find(s,section);r=st+4;out=[]
 while s.cell(r,2).value not in [None,'']:
  out.append({'label':canon(s.cell(r,2).value),'value':float(s.cell(r,3).value),'cell':f"'Complete data set'!C{r}"});r+=1
 return out
point={k:boot_table(sec)for k,sec in [('path','Path coefficients'),('loading','Outer loadings'),('r2','R-square'),('specific_indirect','Specific indirect effects')]}
# Read prior correct native algorithm independently from the actual workbook.
prior={}
for kind,sec in [('path','Path coefficients'),('loading','Outer loadings')]:
 st=find(sa,sec);r=next(r for r in range(st,st+55)if sa.cell(r,2).value=='List')+2
 while sa.cell(r,2).value not in [None,'']:
  prior[(kind,canon(sa.cell(r,2).value))]=float(sa.cell(r,3).value);r+=1
for kind,sec in [('r2','R-square'),('specific_indirect','Specific indirect effects')]:
 r=find(sa,sec)+4
 while sa.cell(r,2).value not in [None,'']:
  prior[(kind,canon(sa.cell(r,2).value))]=float(sa.cell(r,3).value);r+=1
comparisons=[]
for kind,table in point.items():
 for a in table:
  if kind=='loading':item,con=a['label'].split(' <- ');py=ref['M1_loadings'][con][item]
  elif kind=='r2':py=ref['M1_r2'][a['label']]
  else:py=rby[a['label']]['estimate']
  native_prior=prior[(kind,a['label'])]
  comparisons.append({'kind':kind,'label':a['label'],'native_corrected_bootstrap_O':a['value'],'native_prior_correct_algorithm':native_prior,'Python_M1':py,'abs_difference_vs_native_algorithm':abs(a['value']-native_prior),'abs_difference_vs_Python':abs(a['value']-py),'source_cell':a['cell']})
# Original case data, preserving actual source CSV.
header=find(s,'Indicator data (original)')+3
assert s.cell(header,2).value=='Case index'
columns=[canon(s.cell(header,c).value)for c in range(3,s.max_column+1)if s.cell(header,c).value not in [None,'']]
rows=[];indices=[];r=header+1
while s.cell(r,2).value not in [None,'']:
 indices.append(int(s.cell(r,2).value));rows.append([s.cell(r,c).value for c in range(3,len(columns)+3)]);r+=1
native=pd.DataFrame(rows,columns=columns);diff=native[source.columns].to_numpy(float)-source.to_numpy(float)
# Model graph/mapping from native matrices.
innerstart=find(s,'Inner model');ih=innerstart+1;nodes=[canon(s.cell(ih,c).value)for c in range(3,8)];edges=[]
for r in range(ih+1,ih+6):
 for c in range(3,8):
  v=s.cell(r,c).value
  if isinstance(v,(int,float))and v!=0:edges.append([canon(s.cell(r,2).value),canon(s.cell(ih,c).value)])
outerstart=find(s,'Outer model');oh=outerstart+1;outer=[]
for r in range(oh+1,oh+21):
 for c in range(3,8):
  v=s.cell(r,c).value
  if isinstance(v,(int,float))and v!=0:outer.append({'indicator':canon(s.cell(r,2).value),'construct':canon(s.cell(oh,c).value),'code':v,'cell':f"'Complete data set'!{openpyxl.utils.get_column_letter(c)}{r}"})
settings={str(s.cell(r,2).value):s.cell(r,3).value for r in list(range(702,709))+list(range(713,721))}
modes={str(s.cell(r,2).value):s.cell(r,3).value for r in range(725,730)}
# Saturated-vs-estimated fit equality is expected for structurally saturated M1.
fit_rows=[]
for metric,st in [('SRMR',660),('d_ULS',670),('d_G',680)]:
 for typ,offset in [('mixed',4),('composite',6)]:
  sr=st+offset;er=sr+1
  for c,name in [(3,'Original sample (O)'),(4,'Sample mean (M)'),(5,'HI95'),(6,'HI99')]:
   av=float(s.cell(sr,c).value);bv=float(s.cell(er,c).value)
   fit_rows.append({'metric':metric,'model_type':typ,'quantity':name,'saturated':av,'estimated':bv,'abs_difference':abs(av-bv),'saturated_cell':f"'Complete data set'!{openpyxl.utils.get_column_letter(c)}{sr}",'estimated_cell':f"'Complete data set'!{openpyxl.utils.get_column_letter(c)}{er}"})
expected_edges=sorted([['AIR','TR'],['EXP','TR'],['PP','TR'],['TR','AD'],['AIR','AD'],['EXP','AD'],['PP','AD']])
checks={'271_rows':len(native)==271,'20_columns':len(columns)==20,'5420_values_match':bool(np.array_equal(native[source.columns].to_numpy(float),source.to_numpy(float))),'case_order_0_to270':indices==list(range(271)),'5_constructs':set(nodes)=={'AIR','EXP','PP','TR','AD'},'7_expected_edges':sorted(edges)==expected_edges,'20_reflective_items':len(outer)==20 and all(z['code']== -1 for z in outer),'indicator_assignment_expected':all(z['indicator']in[f"{z['construct']}{i}"for i in range(1,5)]for z in outer),'samples10000':str(settings['Samples'])=='10000','complete':settings['Complexity']=='Complete (slower)','percentile':settings['Confidence interval method']=='Percentile bootstrap','two_tailed':settings['Test type']=='Two-tailed','alpha005':float(settings['Significance level'])==.05,'32_point_comparisons':len(comparisons)==32,'points_exact_native_algorithm':all(r['abs_difference_vs_native_algorithm']==0 for r in comparisons),'points_match_Python1e8':all(r['abs_difference_vs_Python']<1e-8 for r in comparisons),'fit_saturated_estimated_numerically_equal':max(r['abs_difference']for r in fit_rows)<1e-12}
assert all(checks.values()),checks
nav={str(w['Navigation'].cell(r,2).value):w['Navigation'].cell(r,3).value for r in range(4,9)}
result={'workbook':str(P),'workbook_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'prior_native_correct_M1_algorithm':str(A),'prior_native_correct_M1_algorithm_sha256':hashlib.sha256(A.read_bytes()).hexdigest(),'source_CSV_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),'metadata':nav,'checks':checks,'data':{'n':len(native),'indicator_count':len(columns),'cell_count':int(diff.size),'max_abs_cell_difference':float(np.max(abs(diff))),'note':'Native AIR1 name includes BOM; only column-name normalization applied. Source files preserved.'},'constructs':nodes,'edges':edges,'outer_mapping':outer,'settings':settings,'outer_modes':modes,'numeric_seed_value_recorded':False,'point_comparisons':comparisons,'max_point_diff_native_vs_algorithm':max(r['abs_difference_vs_native_algorithm']for r in comparisons),'max_point_diff_native_vs_Python':max(r['abs_difference_vs_Python']for r in comparisons),'fit_comparisons':fit_rows,'fit_max_abs_saturated_vs_estimated_difference':max(r['abs_difference']for r in fit_rows),'interpretive_boundary':['Correct native five-construct M1 bootstrap identity is now verified; previous four-construct bootstrap must remain separate.','M1 has all7recursive paths with3freely correlated exogenous composites; its structural score covariance is saturated.','Saturated and estimated SRMR/d_ULS/d_G equal numerically in both mixed and composite models, as expected from that structural saturation. This is not independent confirmation of added direct paths or causal/mediation theory.','The full item measurement model need not be saturated. Mixed and composite fit statistics differ; simple SRMR cutoffs are not interchangeable with bootstrap exact-fit tests.','Same-sample exploratory M1 remains supplemental; M0 prespecified primary model and unresolved construct-discrimination caveats remain.'],'original_files_modified':False}
BASE.mkdir(parents=True,exist_ok=True);(BASE/'corrected_M1_integrity.json').write_text(json.dumps(result,indent=2))
pd.DataFrame(comparisons).to_csv(BASE/'corrected_M1_point_comparisons.csv',index=False);pd.DataFrame(fit_rows).to_csv(BASE/'corrected_M1_fit_saturation_check.csv',index=False)
print('Checks',checks);print('Maxnativepointdifference',result['max_point_diff_native_vs_algorithm']);print('MaxPythonpointdifference',result['max_point_diff_native_vs_Python']);print('Fitmaxdifference',result['fit_max_abs_saturated_vs_estimated_difference'])
