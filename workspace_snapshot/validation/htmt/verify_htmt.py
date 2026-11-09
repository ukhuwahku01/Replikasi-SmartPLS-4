#!/usr/bin/env python3
"""Recalculate HTMT+ and 10,000 seeded nonparametric bootstrap intervals.

Uses only the supplied 271-row CSV; no claims about discarded/source rows are
validated. HTMT+ = mean absolute cross-construct item Pearson correlations /
sqrt(mean absolute within-A pair correlations * within-B pair correlations).
The within means exclude diagonals and count each unordered pair once.
The BC intervals correct bias only, with no acceleration (not BCa).
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT=(Path(__file__).resolve().parent.parent.parent / 'validation/htmt')
CSV=(Path(__file__).resolve().parent.parent.parent / 'attachments/db7f5ebd-93ee-4498-9458-e1ec5c77d40b/KidSense_SmartPLS4_Input_271.csv')
REFERENCE=(Path(__file__).resolve().parent.parent.parent / 'attachments/d0bcb909-7b59-4061-ba39-2de66241055c/KidSense_HTMT_10000_validation.json')

def main():
 p=argparse.ArgumentParser(); p.add_argument('--csv',type=Path,default=CSV); p.add_argument('--reference',type=Path,default=REFERENCE); p.add_argument('--output',type=Path,default=ROOT); args=p.parse_args()
 args.output.mkdir(parents=True,exist_ok=True)
 d=pd.read_csv(args.csv)
 ref=json.loads(args.reference.read_text())
 blocks=['AIR','EXP','PP','TR','AD']
 groups=[[d.columns.get_loc(f'{name}{k}') for k in range(1,5)] for name in blocks]
 pairs=list(itertools.combinations(range(len(groups)),2)); tri=np.triu_indices(4,k=1)
 def htmt(x):
  cor=np.abs(np.corrcoef(x,rowvar=False))
  within=np.array([cor[np.ix_(g,g)][tri].mean() for g in groups])
  return np.array([cor[np.ix_(groups[a],groups[b])].mean()/np.sqrt(within[a]*within[b]) for a,b in pairs])
 x=d.to_numpy(float); point=htmt(x)
 rng=np.random.default_rng(ref['seed'])
 bs=np.empty((ref['resamples'],len(pairs)))
 for b in range(len(bs)):
  bs[b]=htmt(x[rng.integers(0,len(x),size=len(x))])
 np.save(args.output/'htmt_bootstrap_10000.npy',bs)
 rows=[]
 for j,(a,b) in enumerate(pairs):
  name=f'{blocks[a]}-{blocks[b]}'
  source=next(r for r in ref['pairs'] if r['pair']==name)
  pct=np.quantile(bs[:,j],[.025,.975,.95])
  prop=float(np.mean(bs[:,j]<point[j])); z0=float(norm.ppf(prop))
  bc=np.quantile(bs[:,j], norm.cdf(2*z0+norm.ppf([.95,.975])))
  values={'HTMT+':float(point[j]),'percentile_CI95_lower':float(pct[0]),'percentile_CI95_upper':float(pct[1]),'percentile_upper95_one_sided':float(pct[2]),'BC_upper95_one_sided':float(bc[0]),'BC_upper97.5_two_sided':float(bc[1])}
  expected={'HTMT+':source['HTMT+'],'percentile_CI95_lower':source['percentile_CI95_two_sided'][0],'percentile_CI95_upper':source['percentile_CI95_two_sided'][1],**{k:source[k] for k in values if k in source and k!='HTMT+'}}
  row={'pair':name,**values,'z0':z0,'bootstrap_fraction_below_point':prop,'point_below_090':bool(point[j]<.9),'point_below_085':bool(point[j]<.85),'one_sided_PCT_under090':bool(pct[2]<.9),'one_sided_BC_under090':bool(bc[0]<.9),'one_sided_BC_under085':bool(bc[0]<.85)}
  row['max_abs_difference']=float(max(abs(values[k]-expected[k]) for k in values))
  row['differences']={k:float(values[k]-expected[k]) for k in values}
  rows.append(row)
 digest=hashlib.sha256(args.csv.read_bytes()).hexdigest()
 summary={'csv':str(args.csv),'dataset_sha256_actual':digest,'dataset_sha256_expected':ref['dataset_sha256'],'hash_matches':digest==ref['dataset_sha256'],'rows':len(d),'columns':len(d.columns),'missing_cells':int(d.isna().sum().sum()),'duplicate_full_rows':int(d.duplicated().sum()),'response_range':[float(x.min()),float(x.max())],'integer_values_only':bool(np.all(x==np.floor(x))),'seed':ref['seed'],'resamples':ref['resamples'],'generator':'NumPy default_rng PCG64','method':'HTMT+ absolute Pearson, percentile and bias-corrected BC (no acceleration)','max_abs_difference':max(r['max_abs_difference'] for r in rows),'pairs':rows,'limitations':['Original 323 responses and 52 exclusions are not available; selection criteria cannot be verified.','The JSON states Python+NumPy rather than SmartPLS; these calculations do not certify native SmartPLS software output.']}
 (args.output/'htmt_verification.json').write_text(json.dumps(summary,indent=2))
 flat=[]
 for r in rows:
  rr={k:v for k,v in r.items() if k!='differences'}
  rr.update({f'diff_{k}':v for k,v in r['differences'].items()}); flat.append(rr)
 pd.DataFrame(flat).to_csv(args.output/'htmt_verification.csv',index=False)
 print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
