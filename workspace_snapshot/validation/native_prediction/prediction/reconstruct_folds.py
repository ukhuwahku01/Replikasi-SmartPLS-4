import sys,json
from pathlib import Path
import numpy as np,pandas as pd,openpyxl
sys.path.insert(0,'/workspace/validation')
from verify_pls import pls
W=Path('/workspace/attachments/c7ccdeb6-0e70-4b07-a755-212a824125ff/KidSense_PLSpredict_10x10.xlsx');r=list(openpyxl.load_workbook(W,data_only=True,read_only=True)['Complete data set'].values)
X=pd.read_csv('/workspace/attachments/db7f5ebd-93ee-4498-9458-e1ec5c77d40b/KidSense_SmartPLS4_Input_271.csv').to_numpy(float)
ix=np.array([int(z[1]) for z in r[111:2821]]);actual=np.array([z[2:10] for z in r[2825:5535]],float)
ycols=[16,17,18,19,12,13,14,15];results=[]
for mode in ['first_extra','last_extra','rounded','ceil_boundaries']:
 pred=[];folds=[];ep=[];ei=[];el=[]
 if mode=='first_extra': bounds=np.r_[0,np.cumsum([28]+[27]*9)]
 elif mode=='last_extra': bounds=np.r_[0,np.cumsum([27]*9+[28])]
 elif mode=='rounded': bounds=np.rint(np.linspace(0,271,11)).astype(int)
 else:bounds=np.ceil(np.linspace(0,271,11)).astype(int)
 for rep in range(10):
  order=ix[rep*271:(rep+1)*271]
  for a,b in zip(bounds[:-1],bounds[1:]):
   te=order[a:b];tr=np.setdiff1d(np.arange(271),te);fit=pls(X[tr]);m=X[tr].mean(0);s=X[tr].std(0,ddof=0);scores=(X[te]-m)/s@fit['weights'];pTR=scores[:,:3]@fit['beta'][:3];pAD=scores[:,3]*fit['beta'][3]
   pstd=np.column_stack([pAD[:,None]*fit['loadings'][4],pTR[:,None]*fit['loadings'][3]]);prediction=pstd*s[ycols]+m[ycols];pred.append(prediction);ep.append(X[te][:,ycols]-prediction);ei.append(X[te][:,ycols]-m[ycols]);folds.append({'repetition':rep,'start':int(a),'stop':int(b),'test_indices':te.tolist()})
   lm=[]
   for yy,aa in [(slice(16,20),slice(12,16)),(slice(12,16),slice(0,12))]:
    design=np.column_stack([np.ones(271),X[:,aa]]);coef=np.linalg.lstsq(design[tr],X[tr,yy],rcond=None)[0];lm.append(design[te]@coef)
   el.append(X[te][:,ycols]-np.column_stack(lm))
 pred=np.concatenate(pred);ep=np.concatenate(ep);ei=np.concatenate(ei);el=np.concatenate(el)
 z={'mode':mode,'boundaries':bounds.tolist(),'max_abs_prediction_error':float(abs(actual-pred).max()),'mean_abs_prediction_error':float(abs(actual-pred).mean()),'rmse_of_prediction_difference':float(np.sqrt(np.mean((actual-pred)**2))),'PLS_RMSE':np.sqrt(np.mean(ep**2,0)).tolist(),'IA_RMSE':np.sqrt(np.mean(ei**2,0)).tolist(),'LM_RMSE':np.sqrt(np.mean(el**2,0)).tolist()};results.append(z)
 if abs(actual-pred).max()<1e-4:
  out=Path('/workspace/validation/native_prediction/prediction');np.savez(out/'native_reconstructed_errors.npz',PLS=ep,IA=ei,LM=el);(out/'native_reconstructed_folds.json').write_text(json.dumps(folds,indent=2));print('MATCH')
 print(json.dumps(z))
Path('/workspace/validation/native_prediction/prediction/native_fold_candidates.json').write_text(json.dumps(results,indent=2))
