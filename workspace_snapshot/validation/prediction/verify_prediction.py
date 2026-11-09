"""Independent verification of KidSense exploratory CV, no upload edits."""
from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from verify_pls import pls
import numpy as np,pandas as pd
from sklearn.model_selection import KFold
ROOT=(Path(__file__).resolve().parent.parent.parent / 'validation/prediction')
CSV=(Path(__file__).resolve().parent.parent.parent / 'attachments/db7f5ebd-93ee-4498-9458-e1ec5c77d40b/KidSense_SmartPLS4_Input_271.csv')
J=(Path(__file__).resolve().parent.parent.parent / 'attachments/1c6c33c3-8c03-46ac-905a-19d5dc769e24/KidSense_CV_Prediction_Exploratory.json')
x=pd.read_csv(CSV).to_numpy(float); j=json.loads(J.read_text()); n=len(x); err_mean=[];err_lm=[];err_pls=[]
for rep in range(j['repetitions']):
 for tr,te in KFold(n_splits=j['folds'],shuffle=True,random_state=j['seed']+rep).split(x):
  y=x[:,12:]; err_mean.append(y[te]-y[tr].mean(0));preds=[]
  for jj in [slice(0,4),slice(4,8)]:
   a=x[:,:12] if jj.start==0 else x[:,12:16];aa=np.column_stack([np.ones(n),a]);coef=np.linalg.lstsq(aa[tr],y[tr,jj],rcond=None)[0];preds.append(aa[te]@coef)
  err_lm.append(y[te]-np.hstack(preds))
  fit=pls(x[tr]);train_mean=x[tr].mean(0);train_sd=x[tr].std(0,ddof=0)
  scores=((x[te]-train_mean)/train_sd)@fit['weights']
  latent_TR=scores[:,:3]@fit['beta'][:3];latent_AD=scores[:,3]*fit['beta'][3]
  standardized_prediction=np.column_stack([latent_TR[:,None]*fit['loadings'][3],latent_AD[:,None]*fit['loadings'][4]])
  prediction=standardized_prediction*train_sd[12:]+train_mean[12:]
  err_pls.append(y[te]-prediction)
err_mean=np.concatenate(err_mean);err_lm=np.concatenate(err_lm);err_pls=np.concatenate(err_pls)
pls_rmse=np.sqrt(np.mean(err_pls**2,axis=0));pls_mae=np.mean(abs(err_pls),axis=0)
mean_rmse=np.sqrt(np.mean(err_mean**2,axis=0));lm_rmse=np.sqrt(np.mean(err_lm**2,axis=0));mean_mae=np.mean(abs(err_mean),axis=0);lm_mae=np.mean(abs(err_lm),axis=0)
rows=[]
for k,r in enumerate(j['indicators']):
 q=1-(pls_rmse[k]/mean_rmse[k])**2
 row=dict(indicator=r['indicator'],RMSE_PLS_recalculated=pls_rmse[k],MAE_PLS_recalculated=pls_mae[k],RMSE_PLS_abs_difference=abs(pls_rmse[k]-r['RMSE_PLS_exploratory']),MAE_PLS_abs_difference=abs(pls_mae[k]-r['MAE_PLS_exploratory']),q2_reported=r['Q2_predict_analogue'],q2_recalculated=q,q2_abs_difference=abs(q-r['Q2_predict_analogue']),RMSE_mean_recalculated=mean_rmse[k],RMSE_LM_recalculated=lm_rmse[k],MAE_mean_recalculated=mean_mae[k],MAE_LM_recalculated=lm_mae[k],RMSE_mean_abs_difference=abs(mean_rmse[k]-r['RMSE_IA_mean']),RMSE_LM_abs_difference=abs(lm_rmse[k]-r['RMSE_LM']),MAE_mean_abs_difference=abs(mean_mae[k]-r['MAE_IA_mean']),MAE_LM_abs_difference=abs(lm_mae[k]-r['MAE_LM']),beats_mean_RMSE=bool(pls_rmse[k]<mean_rmse[k]),beats_LM_RMSE=bool(pls_rmse[k]<lm_rmse[k]),beats_mean_MAE=bool(pls_mae[k]<mean_mae[k]),beats_LM_MAE=bool(pls_mae[k]<lm_mae[k]))
 rows.append(row)
report=dict(n_rows=n,n_columns=x.shape[1],CSV_actual_sha256=hashlib.sha256(CSV.read_bytes()).hexdigest(),declared_source_sha256=j['source_sha256'],hash_matches=j['source_sha256']==hashlib.sha256(CSV.read_bytes()).hexdigest(),repetitions=10,folds=10,predictions_per_indicator=n*10,baseline_split_method='KFold(n_splits=10,shuffle=True,random_state=20261105+repetition), repetition=0..9',baseline_units='Original Likert item units; training-fold mean and training-fold ordinary least squares with intercept.',TR_LM_predictors='AIR1..AIR4, EXP1..EXP4, PP1..PP4',AD_LM_predictors='TR1..TR4 observed in test fold (conditional prediction)',q2_positive_count=int(sum(r['q2_recalculated']>0 for r in rows)),PLS_beats_LM_RMSE_count=sum(r['beats_LM_RMSE'] for r in rows),PLS_beats_LM_MAE_count=sum(r['beats_LM_MAE'] for r in rows),max_PLS_RMSE_abs_difference=max(r['RMSE_PLS_abs_difference'] for r in rows),max_PLS_MAE_abs_difference=max(r['MAE_PLS_abs_difference'] for r in rows),max_q2_abs_difference=max(r['q2_abs_difference'] for r in rows),max_baseline_RMSE_abs_difference=max(max(r['RMSE_mean_abs_difference'],r['RMSE_LM_abs_difference']) for r in rows),max_baseline_MAE_abs_difference=max(max(r['MAE_mean_abs_difference'],r['MAE_LM_abs_difference']) for r in rows),indicators=rows,limitations=['The declared SHA256 does not hash the supplied CSV; it may identify the unprovided raw 323-row survey. Baseline numeric match independently supports use of the supplied 271-row input.','No SmartPLS PLSpredict/CVPAT execution is represented by these exploratory results.','AD prediction depends on observed TR test indicators, so is not a forecast of AD from only AIR/EXP/PP.','RMSE and MAE compare errors by different loss functions; 5/8 beats_LM count is specific to RMSE.','CV performance differences alone are not statistical significance tests.'])
ROOT.joinpath('prediction_validation.json').write_text(json.dumps(report,indent=2))
pd.DataFrame(rows).to_csv(ROOT/'prediction_comparison.csv',index=False)
print(json.dumps({k:v for k,v in report.items() if k not in ['indicators']},indent=2))
