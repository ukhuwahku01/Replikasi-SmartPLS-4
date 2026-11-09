from pathlib import Path
import numpy as np, pandas as pd, json
from sklearn.model_selection import KFold, RepeatedKFold
CSV=Path('/workspace/attachments/db7f5ebd-93ee-4498-9458-e1ec5c77d40b/KidSense_SmartPLS4_Input_271.csv')
J=Path('/workspace/attachments/1c6c33c3-8c03-46ac-905a-19d5dc769e24/KidSense_CV_Prediction_Exploratory.json')
x=pd.read_csv(CSV).to_numpy(float); seed=20261105;n=len(x); target=json.loads(J.read_text())['indicators']; reference=np.array([r['RMSE_IA_mean'] for r in target]);lmref=np.array([r['RMSE_LM'] for r in target]);
def splits(mode):
 rng=np.random.default_rng(seed)
 if mode=='repeated_kfold': return [list(RepeatedKFold(n_splits=10,n_repeats=10,random_state=seed).split(x))[r*10:(r+1)*10] for r in range(10)]
 out=[]
 for rep in range(10):
  if mode=='kfold_seed_plus_rep': ss=list(KFold(n_splits=10,shuffle=True,random_state=seed+rep).split(x))
  elif mode=='kfold_rng_seed': ss=list(KFold(n_splits=10,shuffle=True,random_state=int(rng.integers(0,2**31-1))).split(x))
  elif mode=='kfold_rng_seed_32': ss=list(KFold(n_splits=10,shuffle=True,random_state=int(rng.integers(0,2**32-1))).split(x))
  else:
   if mode=='numpy_permutation': perm=rng.permutation(n)
   elif mode=='numpy_per_rep': perm=np.random.default_rng(seed+rep).permutation(n)
   elif mode=='randomstate_permutation':
    if rep==0: rs=np.random.RandomState(seed)
    perm=rs.permutation(n)
   chunks=np.array_split(perm,10);ss=[(np.concatenate([q for i,q in enumerate(chunks) if i!=j]),t) for j,t in enumerate(chunks)]
  out.append(ss)
 return out
rows=[]
for mode in ['kfold_seed_plus_rep','kfold_rng_seed','kfold_rng_seed_32','numpy_permutation','numpy_per_rep','randomstate_permutation','repeated_kfold']:
 for ddof in (0,1,99):
  mse_reps=[];lmmse_reps=[]; mse_folds=[];lmmse_folds=[]
  for ss in splits(mode):
   errs=[];lerrs=[]
   for tr,te in ss:
    y=x[:,12:];mean=y[tr].mean(0);sd=np.ones(8) if ddof==99 else y[tr].std(0,ddof=ddof);e=(y[te]-mean)/sd; errs.append(e);mse_folds.append((e**2).mean(0))
    preds=[]
    for jj in [slice(0,4),slice(4,8)]:
     a=x[:,:12] if jj.start==0 else x[:,12:16]; aa=np.column_stack([np.ones(n),a]);coef=np.linalg.lstsq(aa[tr],y[tr,jj],rcond=None)[0];preds.append(aa[te]@coef)
    pred=np.hstack(preds);le=(y[te]-pred)/sd;lerrs.append(le);lmmse_folds.append((le**2).mean(0))
   mse_reps.append((np.concatenate(errs)**2).mean(0));lmmse_reps.append((np.concatenate(lerrs)**2).mean(0))
  for agg in ['pooled','mean_rep_rmse','mean_fold_rmse']:
   if agg=='pooled': z=np.sqrt(np.mean(mse_reps,0));lm=np.sqrt(np.mean(lmmse_reps,0))
   elif agg=='mean_rep_rmse': z=np.mean(np.sqrt(mse_reps),0);lm=np.mean(np.sqrt(lmmse_reps),0)
   else: z=np.mean(np.sqrt(mse_folds),0);lm=np.mean(np.sqrt(lmmse_folds),0)
   rows.append(dict(mode=mode,ddof=ddof,aggregation=agg,max_abs_error_mean=float(np.max(abs(z-reference))),max_abs_error_LM=float(np.max(abs(lm-lmref))),RMSE_mean=z.tolist(),RMSE_LM=lm.tolist()))
rows.sort(key=lambda r:r['max_abs_error_mean'])
Path('/workspace/validation/prediction/baseline_candidates.json').write_text(json.dumps(rows,indent=2))
for r in rows[:6]: print(r)
