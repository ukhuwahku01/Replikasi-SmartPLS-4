"""Recompute 10,000 PLS resamples, four independent default_rng streams."""
from pathlib import Path
import json, numpy as np, pandas as pd
from concurrent.futures import ProcessPoolExecutor
from verify_pls import pls, CSV, EXPECTED

def worker(seed):
 X=pd.read_csv(CSV).to_numpy(float); rng=np.random.default_rng(seed)
 out=np.empty((2500,9))
 for i in range(2500):
  z=pls(X[rng.integers(0,len(X),size=len(X))])
  b=z['beta']; out[i]=np.r_[b,b[:3]*b[3],z['r2']]
 return out
if __name__=='__main__':
 with ProcessPoolExecutor(max_workers=4) as pool:
  draws=np.concatenate(list(pool.map(worker,EXPECTED['seed_streams'])),axis=0)
 np.save(str(Path(__file__).resolve().parent / 'pls_bootstrap_10000.npy'),draws)
 rows=[]
 for i,p in enumerate(EXPECTED['paths']):
  for metric,expected,actual in [('se',p['se'],draws[:,i].std(ddof=1)),('ci_low',p['ci95'][0],np.quantile(draws[:,i],.025)),('ci_high',p['ci95'][1],np.quantile(draws[:,i],.975))]:
   rows.append(dict(section='paths',label=p['path'],metric=metric,reported=expected,recomputed=float(actual),abs_diff=float(abs(expected-actual))))
 for offset,kind in [(4,'indirect'),(7,'r2')]:
  for i,p in enumerate(EXPECTED[kind]):
   for j,q in enumerate([.025,.975]):
    actual=np.quantile(draws[:,offset+i],q); expected=p['ci95'][j]
    rows.append(dict(section=kind,label=p.get('effect',p.get('construct')),metric='ci_low' if j==0 else 'ci_high',reported=expected,recomputed=float(actual),abs_diff=float(abs(expected-actual))))
 pd.DataFrame(rows).to_csv(str(Path(__file__).resolve().parent / 'pls_bootstrap_comparison.csv'),index=False)
 (Path(__file__).resolve().parent.parent / 'validation/pls_bootstrap_verification.json').write_text(json.dumps({'resamples':10000,'seeds':EXPECTED['seed_streams'],'draws_per_seed':2500,'rng':'numpy.random.default_rng','CI':'percentile 2.5% and 97.5%','checks':rows,'max_abs_difference':max(x['abs_diff'] for x in rows)},indent=2))
 print(pd.DataFrame(rows).to_string(index=False))
