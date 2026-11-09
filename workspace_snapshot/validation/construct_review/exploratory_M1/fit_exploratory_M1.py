"""Exploratory Python supplemental M1, not native SmartPLS or primary replacement.
M0 is retained; all three upstream→AD paths added together in a post hoc exploratory diagnostic
comparison, not selected by their p-values. No item selection, no new sample exclusions, no native model edits.
"""
from pathlib import Path
import sys,json,hashlib,time
from concurrent.futures import ProcessPoolExecutor
import numpy as np,pandas as pd
from scipy.stats import norm
BASE=Path(__file__).resolve().parent
CSV=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
sys.path.insert(0,'/workspace/validation')
from verify_pls import pls as prior_pls
NAMES=['AIR','EXP','PP','TR','AD'];BLOCKS=[np.arange(i*4,i*4+4) for i in range(5)]
M0=[[],[],[],[0,1,2],[3]]
M1=[[],[],[],[0,1,2],[0,1,2,3]]
PATHS=[(0,3),(1,3),(2,3),(3,4),(0,4),(1,4),(2,4)]
PATH_NAMES=[f'{NAMES[a]} -> {NAMES[b]}' for a,b in PATHS]
SEEDS=[20261106,20261107,20261108,20261109]

def fit_cov(R,parents,tol=1e-12,maxiter=1000):
 W=np.zeros((20,5))
 for j,b in enumerate(BLOCKS):W[b,j]=.25
 children=[[k for k,pp in enumerate(parents) if j in pp] for j in range(5)]
 for it in range(maxiter):
  W=W/np.sqrt(np.diag(W.T@R@W))[None,:]
  C=W.T@R@W;E=np.zeros((5,5))
  for j,pp in enumerate(parents):
   if pp:E[pp,j]=np.linalg.solve(C[np.ix_(pp,pp)],C[pp,j])
   if children[j]:E[children[j],j]=C[children[j],j]
  Z=R@W@E;V=np.zeros_like(W)
  for j,b in enumerate(BLOCKS):V[b,j]=Z[b,j]
  V=V/np.sqrt(np.diag(V.T@R@V))[None,:]
  # Consistent positive orientation for item blocks across resamples.
  for j,b in enumerate(BLOCKS):
   if V[b,j].sum()<0:V[b,j]*=-1
  delta=float(np.max(abs(V-W)))
  if delta<tol:W=V;break
  W=V
 else:raise RuntimeError('PLS did not converge')
 C=W.T@R@W;B=np.zeros((5,5));r2=np.zeros(5);vif={}
 for j,pp in enumerate(parents):
  if pp:
   beta=np.linalg.solve(C[np.ix_(pp,pp)],C[pp,j]);B[pp,j]=beta;r2[j]=C[pp,j]@beta
   vif[NAMES[j]]=np.diag(np.linalg.inv(C[np.ix_(pp,pp)])).tolist()
 loads=np.array([(R@W)[b,j] for j,b in enumerate(BLOCKS)])
 return dict(beta=B,r2=r2,weights=W,score_correlations=C,loadings=loads,iterations=it+1,vif=vif)

def fit(X,parents):return fit_cov(np.corrcoef(X,rowvar=False),parents)

def worker(seed):
 X=pd.read_csv(CSV).to_numpy(float);rng=np.random.default_rng(seed);out=np.empty((2500,15));maxit=0
 for i in range(2500):
  z=fit(X[rng.integers(0,len(X),size=len(X))],M1);B=z['beta'];direct=np.array([B[a,b] for a,b in PATHS]);indirect=B[:3,3]*B[3,4];total=B[:3,4]+indirect
  out[i]=np.r_[direct,indirect,total,z['r2'][3:]];maxit=max(maxit,z['iterations'])
 return out,maxit

def main():
 started=time.time();X=pd.read_csv(CSV).to_numpy(float)
 old=prior_pls(X);control=fit(X,M0)
 ctrl={'beta_max_abs_difference':float(np.max(abs(np.array([control['beta'][a,b] for a,b in PATHS[:4]])-old['beta']))),'loadings_max_abs_difference':float(np.max(abs(control['loadings']-old['loadings']))),'r2_max_abs_difference':float(np.max(abs(control['r2'][3:]-old['r2']))),'control_tolerance':1e-8}
 assert all(ctrl[k]<=1e-8 for k in ['beta_max_abs_difference','loadings_max_abs_difference','r2_max_abs_difference']),ctrl
 fit1=fit(X,M1);B=fit1['beta'];point=np.r_[[B[a,b] for a,b in PATHS],B[:3,3]*B[3,4],B[:3,4]+B[:3,3]*B[3,4],fit1['r2'][3:]]
 with ProcessPoolExecutor(max_workers=4) as pool:parts=list(pool.map(worker,SEEDS))
 draws=np.concatenate([r[0] for r in parts]);assert draws.shape==(10000,15) and np.isfinite(draws).all()
 np.save(BASE/'M1_bootstrap_10000.npy',draws)
 labels=PATH_NAMES+[f'{con} -> TR -> AD' for con in NAMES[:3]]+[f'{con} total -> AD' for con in NAMES[:3]]+['R2 TR','R2 AD']
 kinds=['path']*7+['specific_indirect']*3+['total_association']*3+['r2']*2
 rows=[]
 for j,(label,kind) in enumerate(zip(labels,kinds)):
  ci=np.quantile(draws[:,j],[.025,.975]);sd=draws[:,j].std(ddof=1)
  rows.append({'kind':kind,'effect':label,'estimate':float(point[j]),'bootstrap_mean':float(draws[:,j].mean()),'bootstrap_SE':float(sd),'CI95_percentile_low':float(ci[0]),'CI95_percentile_high':float(ci[1]),'CI_excludes_zero':bool(ci[0]>0 or ci[1]<0),'bootstrap_valid_count':int(np.isfinite(draws[:,j]).sum()),'status':'EXPLORATORY PYTHON ONLY; native M1 not run'})
 # Full recursive structural covariance parameterization at score level.
 # Exogenous covariance free; TR regressed on all3 X; AD on all4 predecessors.
 C=fit1['score_correlations'];A=B.T;noise=np.zeros((5,5));noise[:3,:3]=C[:3,:3]
 for j in [3,4]:noise[j,j]=1-fit1['r2'][j]
 inv=np.linalg.inv(np.eye(5)-A);implied=inv@noise@inv.T
 saturation_diff=float(np.max(abs(C-implied)));assert saturation_diff<1e-10
 meanings={'AIR':'Perceived AI reliability, not objective AI reliability','EXP':'Perceived explainability: understanding reasons/basis/confidence/errors/interpreting alerts','PP':'Perceived privacy protection of child data/consent camera-mic/storage-deletion/overall adequacy, not technical security audit','TR':'Trust','AD':'Hypothetical conditional adoption intention: trial/use/early warnings/continuance, not observed adoption'}
 result={'status':'Exploratory supplemental Python M1; native SmartPLS M1 unrun; M0 primary model preserved','source_csv':str(CSV),'source_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),'n':len(X),'indicator_count':20,'constructs':NAMES,'investigator_supplied_construct_meanings':meanings,'construct_definition_provenance':'Investigator operational definitions; no theoretical source supplied','measurement':'All20 original indicators retained in reflective Mode A; no data filtering or item deletion','estimator':'Custom covariance-based PLS-PM Mode A path weighting; convergence max normalized weight change1e-12; maximum1000 iterations; positive block orientation','M0_control':ctrl,'M0_paths':PATH_NAMES[:4],'M1_paths':PATH_NAMES,'M1_supplement_rationale':'Add all AIR/EXP/PP direct paths to AD together to investigate TR-only AD restrictions, not select paths by p value.','bootstrap':{'resamples':10000,'independent_default_rng_seeds':SEEDS,'resamples_per_seed':2500,'seed_streams_combined_in_order':True,'interval':'Percentile2.5% and97.5%; two-sided95%','standard_error':'SampleSD,ddof1','numeric_seed_matches_native':False,'native_bootstrap_not_expected_identical':'Different RNG/resampling implementations and construct-score fitting can produce different bootstrap SE and intervals.','max_iterations_observed':max(r[1] for r in parts)},'results':rows,'M0_r2':dict(zip(['TR','AD'],old['r2'].tolist())),'M1_r2':dict(zip(['TR','AD'],fit1['r2'][3:].tolist())),'M1_score_correlations':C.tolist(),'M1_loadings':{con:dict(zip([f'{con}{i}' for i in range(1,5)],fit1['loadings'][j].tolist())) for j,con in enumerate(NAMES)},'M1_inner_VIF':fit1['vif'],'structural_saturation':{'structural_parameters':15,'observed_score_covariance_unique_entries':15,'implied_vs_score_covariance_max_abs_diff':saturation_diff,'boundary':'Three correlated exogenous composites freely covary; TR has all3 X parents; AD has all4 preceding composites as parents. This complete recursive structural covariance parameterization is saturated (zero structural covariance degrees of freedom).','implication':'Any improved in-sample score covariance fit or AD R2 is not evidence confirming the added paths, causality or mediation theory. Measurement restrictions can remain; the full item-level model need not be saturated.'},'limitations':['Same-sample exploratory supplementary analysis; no preregistration claim.','Construct weights change when paths are added, so between-model R2 differences are not necessarily pure nested-regression increments on fixed identical scores.','Direct/indirect estimates are model-conditional associations, not causal effects.','Discriminant-validity/item-overlap concerns are not solved by adding direct paths.','Do not replace M0 or claim native SmartPLS validation until a separate native M1 run is exported.','No external predictive validation or M1 PLSpredict/CVPAT run is supplied.'],'elapsed_seconds':time.time()-started}
 (BASE/'M1_exploratory_results.json').write_text(json.dumps(result,indent=2))
 pd.DataFrame(rows).to_csv(BASE/'M1_exploratory_results.csv',index=False)
 pd.DataFrame(C,index=NAMES,columns=NAMES).to_csv(BASE/'M1_composite_correlations.csv')
 print('M0control',ctrl);print(pd.DataFrame(rows).to_string(index=False));print('Saturation',result['structural_saturation']);print('elapsed',result['elapsed_seconds'])
if __name__=='__main__':main()
