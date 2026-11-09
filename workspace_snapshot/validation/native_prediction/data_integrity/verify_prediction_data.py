"""Read-only audit of native PLSpredict data/model/configuration."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,openpyxl
BASE=Path('/workspace/validation/native_prediction/data_integrity')
P=Path('/workspace/attachments/c7ccdeb6-0e70-4b07-a755-212a824125ff/KidSense_PLSpredict_10x10.xlsx')
CSV=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
w=openpyxl.load_workbook(P,data_only=True);s=w['Complete data set']
canon=lambda x:str(x).replace('\ufeff','').strip()
headers=[canon(s.cell(11056,c).value) for c in range(3,23)]
records=[];indices=[];row=11057
while s.cell(row,2).value not in [None,'']:
 indices.append(int(s.cell(row,2).value));records.append([s.cell(row,c).value for c in range(3,23)]);row+=1
native=pd.DataFrame(records,columns=headers);original=pd.read_csv(CSV);reordered=native[original.columns]
rawdiff=reordered.to_numpy(float)-original.to_numpy(float)
model_cols={c:canon(s.cell(11021,c).value) for c in range(3,8)}
inner=[]
for r in range(11022,11027):
 for c in range(3,8):
  value=s.cell(r,c).value
  if isinstance(value,(int,float)) and value!=0:inner.append([canon(s.cell(r,2).value),model_cols[c]])
outer=[]
for r in range(11031,11051):
 item=canon(s.cell(r,2).value)
 for c in range(3,8):
  value=s.cell(r,c).value
  if isinstance(value,(int,float)) and value!=0:outer.append({'indicator':item,'construct':canon(s.cell(11030,c).value),'native_code':value,'source_cell':f"'Complete data set'!{openpyxl.utils.get_column_letter(c)}{r}"})
settings={str(s.cell(r,2).value):s.cell(r,3).value for r in list(range(10979,10986))+list(range(10990,10994))}
modes={str(s.cell(r,2).value):s.cell(r,3).value for r in range(10998,11003)}
seed_rows=[]
for r in range(10968,11011):
 cells=[s.cell(r,c).value for c in range(2,23)]
 if any('seed' in str(v).lower() for v in cells if v is not None):seed_rows.append({'row':r,'values':[v for v in cells if v is not None]})
nav={w['Navigation'].cell(r,2).value:w['Navigation'].cell(r,3).value for r in range(4,9)}
checks={
 'rows_271':len(native)==271,
 'columns_20':len(headers)==20,
 'same_normalized_column_names':set(headers)==set(original.columns),
 'case_indices_0_to_270':indices==list(range(271)),
 'all_5420_original_values_same_in_row_order':bool(np.array_equal(reordered.to_numpy(float),original.to_numpy(float))),
 'four_structural_edges_same':sorted(inner)==sorted([['AIR','TR'],['EXP','TR'],['PP','TR'],['TR','AD']]),
 'twenty_outer_links':len(outer)==20,
 'all_reflective_codes_minus1':all(z['native_code']==-1.0 for z in outer),
 'all_expected_indicator_assignments':all(z['indicator'] in [f"{z['construct']}{i}" for i in range(1,5)] for z in outer),
 'ten_folds':str(settings['Number of folds'])=='10',
 'ten_repetitions':str(settings['No. of repetitions'])=='10',
 'prediction_type_direct_antecedents':settings['Prediction type']=='Direct antecedents',
 'fixed_seed_label':settings['Seed']=='Fixed seed',
 'log_completed':s.cell(11009,2).value=='All calculations done.'}
assert all(checks.values()),checks
result={'workbook':str(P),'workbook_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'csv':str(CSV),'csv_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),'metadata':nav,'checks':checks,'row_count':len(native),'column_count':len(headers),'exact_cell_comparisons':int(rawdiff.size),'max_abs_cell_difference':float(np.max(np.abs(rawdiff))),'native_column_order_after_BOM_normalization':headers,'BOM_note':'The native AIR1 name contains U+FEFF; removed only to map names. All original numeric values are unchanged.','settings':settings,'outer_weighting_modes':modes,'outer_mode_note':'Export says AUTOMATIC for all constructs; outer model stores reflective -1 codes. Do not claim explicit Mode A label in settings.','prediction_design_interpretation':'Native run is Direct antecedents, not Early antecedents. AD has direct predecessor TR, so this configuration is the appropriate direct-antecedent comparator to earlier conditional AD prediction. Any implementation equality must be checked from prediction values separately.','numeric_seed_value_present':False,'seed_evidence':seed_rows,'seed_limit':'Only Fixed seed is exported; no numeric seed or RNG algorithm is recorded in this settings/log section. Do not infer seed20261106 or same folds as Python.','structural_edges':inner,'outer_links':outer,'log':[s.cell(r,2).value for r in range(11006,11010)],'read_only_original_files':True}
BASE.mkdir(parents=True,exist_ok=True)
(BASE/'native_prediction_data_integrity.json').write_text(json.dumps(result,indent=2))
pd.DataFrame(outer).to_csv(BASE/'native_prediction_outer_mapping.csv',index=False)
print(json.dumps({k:v for k,v in result.items() if k!='outer_links'},indent=2))
