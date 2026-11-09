"""Diagnostic-only assessment of current KidSense structural restrictions.
No alternative SEM is fitted, no paths/indicators added/deleted, no uploads changed.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np,pandas as pd,openpyxl
BASE=Path('/workspace/validation/next_stage/structural')
CSV=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
NATIVE=Path('/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx')
sys.path.insert(0,'/workspace/validation')
from verify_pls import pls,NAMES
x=pd.read_csv(CSV).to_numpy(float)
fit=pls(x)
z=(x-x.mean(0))/x.std(0,ddof=0)
scores=z@fit['weights']; R=np.corrcoef(scores,rowvar=False)
# Ensure population-standardized score interpretation.
assert np.max(abs(scores.mean(0)))<1e-12
assert np.max(abs(scores.std(0,ddof=0)-1))<1e-12
b=float(fit['beta'][3]);rows=[]
for j,con in enumerate(NAMES[:3]):
 rxt=float(R[j,3]);rxa=float(R[j,4]);rta=float(R[3,4])
 implied=rxt*b;gap=rxa-implied
 partial=(rxa-rxt*rta)/np.sqrt((1-rxt*rxt)*(1-rta*rta))
 # Independent check from residual correlations after projection on TR.
 residual_x=scores[:,j]-rxt*scores[:,3]
 residual_ad=scores[:,4]-rta*scores[:,3]
 residual_r=float(np.corrcoef(residual_x,residual_ad)[0,1])
 assert abs(partial-residual_r)<1e-12
 rows.append({'construct':con,'observed_corr_X_TR':rxt,'observed_corr_X_AD':rxa,'beta_TR_AD':b,'implied_corr_X_AD_under_restricted_model':implied,'observed_minus_implied':gap,'partial_corr_X_AD_controlling_only_TR':float(partial),'partial_corr_residual_check':residual_r,'status':'EXPLORATORY DIAGNOSTIC ONLY'})
w=openpyxl.load_workbook(NATIVE,data_only=True);s=w['Complete data set'];native_comparison=[]
for r in range(526,536):
 label=s.cell(r,2).value;a,c=label.split(' <-> ');v=float(s.cell(r,3).value);ours=float(R[NAMES.index(a),NAMES.index(c)])
 native_comparison.append({'pair':label,'native_corr':v,'recomputed_corr':ours,'abs_difference':abs(v-ours),'source_cell':f"'Complete data set'!C{r}"})
assert max(r['abs_difference'] for r in native_comparison)<1e-8
result={'label':'Diagnostic only; original structural model unchanged','n':len(x),'variables':'Standardized estimated Mode A composite scores, not observed true latent factors','source_CSV':str(CSV),'source_CSV_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),'native_bootstrap_workbook':str(NATIVE),'score_order':NAMES,'score_correlations':R.tolist(),'native_corr_max_abs_difference':max(r['abs_difference'] for r in native_comparison),'native_correlation_comparisons':native_comparison,'restricted_model':['AIR->TR','EXP->TR','PP->TR','TR->AD'],'restriction_equation':'corr(X,AD) = corr(X,TR) * beta(TR->AD) for X=AIR,EXP,PP, under the restricted linear structural model with AD disturbance uncorrelated with upstream X. Since AD has only TR as predictor and scores are standardized, beta(TR->AD)=corr(TR,AD).','diagnostics':rows,'interpretation':['All three upstream construct-score associations with AD exceed the values implied by the TR-only AD equation under upstream-orthogonal-disturbance assumptions.','Positive partial correlations are remaining linear score associations after controlling TR only, not simultaneous direct-path estimates adjusting the other exogenous constructs.','These discrepancies flag restrictions needing theoretical review; they do not identify a unique cause or justify automatic path additions. Alternatives include unmodeled association, correlated disturbances, imperfect measurement or insufficiently distinct constructs.','The analysis uses the same sample and data-derived composite weights; it is exploratory, not confirmatory causal or mediation evidence. No hypothesis-test p-values/intervals are supplied for these diagnostic correlations.','Preserve the prespecified model for primary reporting. A modified model would require substantive item/theory justification, explicit exploratory labeling and preferably validation on independent data.'],'no_new_paths_or_deletions':True}
BASE.mkdir(parents=True,exist_ok=True)
(BASE/'structural_restriction_diagnostics.json').write_text(json.dumps(result,indent=2))
pd.DataFrame(rows).to_csv(BASE/'structural_restriction_diagnostics.csv',index=False)
pd.DataFrame(R,index=NAMES,columns=NAMES).to_csv(BASE/'standardized_composite_correlations.csv')
pd.DataFrame(native_comparison).to_csv(BASE/'native_composite_correlation_check.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
print('Native corr max abs difference:',result['native_corr_max_abs_difference'])
