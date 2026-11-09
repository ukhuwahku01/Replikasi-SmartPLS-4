#!/usr/bin/env python3
"""Check workbook HTMT consistency and reproducible sensitivity subsets."""
from pathlib import Path
import json,itertools
import numpy as np,pandas as pd
from openpyxl import load_workbook
ROOT=(Path(__file__).resolve().parent.parent.parent / 'validation/htmt')
CSV=(Path(__file__).resolve().parent.parent.parent / 'attachments/db7f5ebd-93ee-4498-9458-e1ec5c77d40b/KidSense_SmartPLS4_Input_271.csv')
REF=(Path(__file__).resolve().parent.parent.parent / 'attachments/d0bcb909-7b59-4061-ba39-2de66241055c/KidSense_HTMT_10000_validation.json')
XLSX=(Path(__file__).resolve().parent.parent.parent / 'attachments/6cb0d79d-f565-4c78-977d-a9f20909c62b/KidSense_JADS_Validasi_Lanjutan_10000.xlsx')
d=pd.read_csv(CSV); ref=json.loads(REF.read_text()); w=load_workbook(XLSX,data_only=True)
blocks=['AIR','EXP','PP','TR','AD']; groups={s:[d.columns.get_loc(f'{s}{j}') for j in range(1,5)] for s in blocks}; tri=np.triu_indices(4,1)
def calc(frame):
 c=np.abs(frame.corr().to_numpy()); within={s:c[np.ix_(g,g)][tri].mean() for s,g in groups.items()}
 return {f'{a}-{b}':float(c[np.ix_(groups[a],groups[b])].mean()/np.sqrt(within[a]*within[b])) for a,b in itertools.combinations(blocks,2)}
rows=list(w['HTMT_10k'].values); bypair={r['pair']:r for r in ref['pairs']}; consistency=[]
for row in rows[1:]:
 p,point,bc,pct,status,point85=row; orig=bypair[p]
 expected=[orig['HTMT+'],orig['BC_upper95_one_sided'],orig['percentile_upper95_one_sided']]
 numeric=[float(point),float(bc),float(pct)]
 consistency.append({'pair':p,'max_abs_numeric_difference':max(abs(a-b) for a,b in zip(numeric,expected)),'At_090_workbook':status,'At_090_expected':'Pass' if orig['BC_upper95_one_sided']<.9 else 'NOT established','At_085_point_workbook':point85,'At_085_expected':'<.85' if orig['HTMT+']<.85 else '>=.85'})
mask=d.nunique(axis=1).eq(1)
scenarios={'primary':d,'uniform_excluded':d.loc[~mask]}
headers=list(w['HTMT_sensitivity'].values)[0]; tests=[]
for row in list(w['HTMT_sensitivity'].values)[1:]:
 name,n,*reported=row
 if name not in scenarios:
  tests.append({'scenario':name,'reported_n':n,'status':'UNVERIFIED','reason':'D1/D2 pass flags and respondent mapping are absent from supplied CSV; subset membership cannot be reconstructed.'}); continue
 frame=scenarios[name]; calculated=calc(frame); values=[]
 for key,display in zip(headers[2:],reported):
  pair=key.replace('–','-'); val=calculated[pair]
  values.append({'pair':pair,'recomputed':val,'reported':display,'recomputed_rounded4':round(val,4),'matches_reported_rounded4':round(val,4)==display,'absolute_rounding_difference':abs(val-display)})
 tests.append({'scenario':name,'reported_n':n,'recomputed_n':len(frame),'status':'VERIFIED' if len(frame)==n and all(v['matches_reported_rounded4'] for v in values) else 'MISMATCH','values':values})
result={'workbook':str(XLSX),'csv':str(CSV),'uniform_definition':'All 20 supplied indicator values are identical within a row.','uniform_rows_removed':int(mask.sum()),'zero_based_uniform_row_positions':np.flatnonzero(mask.to_numpy()).tolist(),'workbook_HTMT_10k_vs_json':consistency,'workbook_HTMT_numeric_max_abs_difference':max(c['max_abs_numeric_difference'] for c in consistency),'all_workbook_classifications_match':all(c['At_090_workbook']==c['At_090_expected'] and c['At_085_point_workbook']==c['At_085_expected'] for c in consistency),'sensitivity':tests,'limitations':['D1D2_pass and both are unverified because original eligibility flags are absent.','Matching repeated answer patterns or uniform responses does not on its own prove invalid responding.']}
(ROOT/'htmt_workbook_supplement.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
