"""Audit native SmartPLS PLSpredict export against row-level predictions and CSV.
Run reconstruct_folds.py first for independent model/IA/LM refitting.
"""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,openpyxl
ROOT=Path('/workspace/validation/native_prediction/prediction')
W=Path('/workspace/attachments/c7ccdeb6-0e70-4b07-a755-212a824125ff/KidSense_PLSpredict_10x10.xlsx')
CSV=Path('/workspace/attachments/db7f5ebd-93ee-4498-9458-e1ec5c77d40b/KidSense_SmartPLS4_Input_271.csv')
J=Path('/workspace/attachments/1c6c33c3-8c03-46ac-905a-19d5dc769e24/KidSense_CV_Prediction_Exploratory.json')
r=list(openpyxl.load_workbook(W,data_only=True,read_only=True)['Complete data set'].values)
summary=pd.DataFrame([z[1:9] for z in r[11:19]],columns=['indicator','Q2','RMSE_PLS','MAE_PLS','RMSE_LM','MAE_LM','RMSE_IA','MAE_IA'])
errors=np.array([z[2:10] for z in r[111:2821]],float);predictions=np.array([z[2:10] for z in r[2825:5535]],float);ids=np.array([int(z[1]) for z in r[111:2821]]);ids2=np.array([int(z[1]) for z in r[2825:5535]])
raw=pd.read_csv(CSV)[summary.indicator].to_numpy(float);refit=np.load(ROOT/'native_reconstructed_errors.npz')
old={z['indicator']:z for z in json.loads(J.read_text())['indicators']};rows=[]
for k,z in summary.iterrows():
 row=z.to_dict();o=old[z.indicator]
 row.update(PLS_RMSE_from_native_errors=float(np.sqrt(np.mean(errors[:,k]**2))),PLS_MAE_from_native_errors=float(np.mean(abs(errors[:,k]))),Q2_from_summary=float(1-(z.RMSE_PLS/z.RMSE_IA)**2),RMSE_PLS_custom=o['RMSE_PLS_exploratory'],MAE_PLS_custom=o['MAE_PLS_exploratory'],Q2_custom=o['Q2_predict_analogue'])
 for method in ('PLS','IA','LM'):
  e=refit[method][:,k];row[f'RMSE_{method}_independent_refit']=float(np.sqrt(np.mean(e*e)));row[f'MAE_{method}_independent_refit']=float(np.mean(abs(e)))
 row['Q2_independent_refit']=float(1-np.mean(refit['PLS'][:,k]**2)/np.mean(refit['IA'][:,k]**2))
 row['PLS_RMSE_error_summary_delta']=row['PLS_RMSE_from_native_errors']-row['RMSE_PLS'];row['PLS_MAE_error_summary_delta']=row['PLS_MAE_from_native_errors']-row['MAE_PLS']
 row['RMSE_PLS_native_minus_custom']=row['RMSE_PLS']-row['RMSE_PLS_custom'];row['MAE_PLS_native_minus_custom']=row['MAE_PLS']-row['MAE_PLS_custom'];row['Q2_native_minus_custom']=row['Q2']-row['Q2_custom']
 row['beats_LM_RMSE_native']=bool(z.RMSE_PLS<z.RMSE_LM);row['beats_LM_MAE_native']=bool(z.MAE_PLS<z.MAE_LM);rows.append(row)
lverrors=np.array([z[2:4] for z in r[5541:8251]],float);lvsummary=[]
for k,z in enumerate(r[49:51]):
 lvsummary.append({'construct':z[1],'Q2':z[2],'RMSE':z[3],'MAE':z[4],'RMSE_from_errors':float(np.sqrt(np.mean(lverrors[:,k]**2))),'MAE_from_errors':float(np.mean(abs(lverrors[:,k])))})
report=dict(workbook_sha256=hashlib.sha256(W.read_bytes()).hexdigest(),n_cases=len(np.unique(ids)),repetitions=10,folds=10,case_indices='zero-based 0..270',case_frequency={str(k):int(v) for k,v in zip(*np.unique(np.unique(ids,return_counts=True)[1],return_counts=True))},n_predictions_per_indicator=len(ids),n_indicator_error_values=int(errors.size),prediction_case_order_matches=bool(np.array_equal(ids,ids2)),max_observed_minus_prediction_error_difference=float(abs(raw[ids]-predictions-errors).max()),max_PLS_RMSE_error_summary_difference=max(abs(z['PLS_RMSE_error_summary_delta']) for z in rows),max_PLS_MAE_error_summary_difference=max(abs(z['PLS_MAE_error_summary_delta']) for z in rows),max_Q2_formula_difference=max(abs(z['Q2']-z['Q2_from_summary']) for z in rows),max_refitted_PLS_RMSE_difference=max(abs(z['RMSE_PLS']-z['RMSE_PLS_independent_refit']) for z in rows),max_refitted_IA_LM_RMSE_difference=max(abs(z['RMSE_'+m]-z['RMSE_'+m+'_independent_refit']) for z in rows for m in ('IA','LM')),max_native_custom_RMSE_PLS_difference=max(abs(z['RMSE_PLS_native_minus_custom']) for z in rows),max_native_custom_MAE_PLS_difference=max(abs(z['MAE_PLS_native_minus_custom']) for z in rows),max_native_custom_Q2_difference=max(abs(z['Q2_native_minus_custom']) for z in rows),q2_positive_count=sum(z['Q2']>0 for z in rows),RMSE_wins_LM_native=sum(z['beats_LM_RMSE_native'] for z in rows),MAE_wins_LM_native=sum(z['beats_LM_MAE_native'] for z in rows),RMSE_wins_LM_custom=sum(z['RMSE_PLS_exploratory']<z['RMSE_LM'] for z in old.values()),MAE_wins_LM_custom=sum(z['MAE_PLS_exploratory']<z['MAE_LM'] for z in old.values()),indicators=rows,latent=lvsummary,settings={str(z[1]):z[2] for z in r[10978:11002] if z[1] is not None and z[2] is not None},interpretation=['Native MV prediction errors are observed minus predicted raw Likert item values, verified against supplied CSV by zero-based case index.','Pooled RMSE/MAE from all 2710 predictions per indicator reproduce native summaries.','Native export gives Fixed seed but no numeric seed; exact fold membership is recoverable from exported case order and first-fold size28 then nine folds27, and independently reproduces predictions to <3e-9.','Native vs prior Python differences are consistent with different fold partitions; native folds reproduce all IA and LM metrics and custom PLS predictions closely.','Both native and prior custom workflows use direct antecedents. AD predictions condition on observed TR indicators.','Native PLS beats LM on5/8 RMSE and7/8 MAE, prior custom5/8 and6/8. AD3 MAE winner changes under native folds.','Differences in point prediction losses do not alone establish statistically significant improvement; consult native CVPAT.'])
ROOT.joinpath('native_prediction_validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));pd.DataFrame(rows).to_csv(ROOT/'native_prediction_comparison.csv',index=False)
print(json.dumps({k:v for k,v in report.items() if k not in ('indicators','settings')},indent=2,ensure_ascii=False))
print(pd.DataFrame(rows)[['indicator','RMSE_PLS','RMSE_PLS_custom','RMSE_PLS_native_minus_custom','Q2','beats_LM_RMSE_native','beats_LM_MAE_native']].to_string(index=False))
