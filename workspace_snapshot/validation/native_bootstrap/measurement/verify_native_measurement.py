"""Verify native measurement results and embedded original data, read-only sources."""
from pathlib import Path
import json,sys,hashlib
import pandas as pd,numpy as np,openpyxl
BASE=Path('/workspace/validation/native_bootstrap/measurement')
NATIVE=Path('/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx')
CSV=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
PRIOR=Path('/workspace/validation/pls_point_verification.json')
sys.path.insert(0,'/workspace/validation')
from verify_pls import pls,NAMES,BLOCKS
w=openpyxl.load_workbook(NATIVE,data_only=True);s=w['Complete data set']
canon=lambda x:str(x).replace('\ufeff','').strip()
headers=[canon(s.cell(798,c).value) for c in range(3,23)]
raw=np.array([[s.cell(r,c).value for c in range(3,23)] for r in range(799,1070)],float)
native_frame=pd.DataFrame(raw,columns=headers)
source=pd.read_csv(CSV);native_frame=native_frame[source.columns]
diffs=native_frame.to_numpy()-source.to_numpy()
assert np.max(abs(diffs))==0
indices=[int(s.cell(r,2).value) for r in range(799,1070)]
fit=pls(source.to_numpy(float))
prior=json.loads(PRIOR.read_text());pby={r['construct']:r for r in prior['reliability']}
comparisons=[]
for row in range(124,144):
 label=canon(s.cell(row,2).value);item,con=label.split(' <- ');j=NAMES.index(con);k=list(source.columns[BLOCKS[j]]).index(item)
 a=float(s.cell(row,3).value);b=float(fit['loadings'][j,k]);comparisons.append({'kind':'loading','entity':label,'native':a,'reference':b,'abs_difference':abs(a-b),'native_cell':f"'Complete data set'!C{row}",'reference_method':'Independent covariance PLS Mode A, path weighting, tol1e-12'})
metrics=[('AVE',350,354,'AVE'),('rho_C',379,383,'rho_C'),('alpha_standardized',437,441,'alpha_standardized')]
for metric,first,last,key in metrics:
 for row in range(first,last+1):
  con=canon(s.cell(row,2).value);a=float(s.cell(row,3).value);b=pby[con][key]
  comparisons.append({'kind':metric,'entity':con,'native':a,'reference':b,'abs_difference':abs(a-b),'native_cell':f"'Complete data set'!C{row}",'reference_method':'Previously independently verified CSV measurement result'})
rhoA=[]
for row in range(408,413):
 con=canon(s.cell(row,2).value)
 rhoA.append({'construct':con,'native_rho_A':s.cell(row,3).value,'native_cell':f"'Complete data set'!C{row}",'prior_reference_available':False,'note':'New native SmartPLS result; no rho_A existed in original Python output, not independently recomputed here.'})
# Read original outer-model mapping, inner graph, and automatic weighting option.
outer_map=[]
for row in range(773,793):
 label=canon(s.cell(row,2).value)
 for c in range(3,8):
  value=s.cell(row,c).value
  if isinstance(value,(int,float)) and value!=0:outer_map.append({'indicator':label,'construct':s.cell(772,c).value,'native_outer_model_code':value})
inner=[]
for row in range(764,769):
 for c in range(3,8):
  val=s.cell(row,c).value
  if isinstance(val,(int,float)) and val!=0:inner.append([s.cell(row,2).value,s.cell(763,c).value])
expected_edges=[['AIR','TR'],['EXP','TR'],['PP','TR'],['TR','AD']]
assert sorted(inner)==sorted(expected_edges)
assert len(outer_map)==20
assert all(z['native_outer_model_code']==-1.0 for z in outer_map)
assert all(z['indicator'].startswith(z['construct']) for z in outer_map)
settings={str(s.cell(r,2).value):s.cell(r,3).value for r in [678,679,680,681,682,683,689,690,691,692,693,694,695,696]}
mode_settings={str(s.cell(r,2).value):s.cell(r,3).value for r in range(701,706)}
summary={'source_workbook':str(NATIVE),'source_workbook_sha256':hashlib.sha256(NATIVE.read_bytes()).hexdigest(),'input_CSV_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),'input_data_verification':{'native_original_rows':raw.shape[0],'native_original_columns':raw.shape[1],'normalized_header_names_match':set(headers)==set(source.columns),'row_order_same':indices==list(range(271)),'all_5420_item_values_exact_match':bool(np.array_equal(native_frame.to_numpy(),source.to_numpy())),'max_abs_cell_difference':float(np.max(abs(diffs))),'BOM_header_note':'Native export retains U+FEFF before AIR1; normalized ONLY for name mapping. It does not change any item value or construct assignment.'},'settings':settings,'native_construct_outer_weighting_modes':mode_settings,'outer_mode_note':'Export records AUTOMATIC for all five constructs, not an explicit Mode A label. Native outer model has -1 codes for all 20 reflective links. Independent reflective Mode A fit reproduces their loadings to numerical precision.','outer_model_mapping':outer_map,'inner_edges':inner,'comparison_count':len(comparisons),'max_abs_numeric_difference':max(r['abs_difference'] for r in comparisons),'comparisons':comparisons,'rho_A_native_new':rhoA,'interpretation':'Point measurement results agree within 1e-8. This audit does not compare their bootstrap SE/CI. Source selection 323→271 remains outside this dataset scope.'}
BASE.mkdir(parents=True,exist_ok=True)
(BASE/'native_measurement_verification.json').write_text(json.dumps(summary,indent=2))
pd.DataFrame(comparisons).to_csv(BASE/'native_measurement_comparison.csv',index=False)
pd.DataFrame(rhoA).to_csv(BASE/'native_rhoA_new.csv',index=False)
print(json.dumps({k:v for k,v in summary.items() if k not in ['comparisons','outer_model_mapping']},indent=2))
