"""Independent covariance-based PLS-PM Mode A, reflective path weighting.
Preserves original uploaded evidence; all outputs are separate verification files.
"""
from pathlib import Path
import numpy as np, pandas as pd, json
from scipy.stats import norm
ROOT=(Path(__file__).resolve().parent.parent / 'attachments')
CSV=next(ROOT.rglob('KidSense_SmartPLS4_Input_271.csv'))
EXPECTED=json.loads(next(ROOT.rglob('KidSense_PLS_10000_results.json')).read_text())
NAMES=['AIR','EXP','PP','TR','AD']
BLOCKS=[np.arange(i*4,i*4+4) for i in range(5)]

def pls(X,tol=1e-12,maxiter=1000):
    R=np.corrcoef(X,rowvar=False)
    W=np.zeros((20,5))
    for j,b in enumerate(BLOCKS): W[b,j]=.25
    for it in range(maxiter):
        W=W/np.sqrt(np.diag(W.T@R@W))[None,:]
        C=W.T@R@W
        E=np.zeros((5,5))
        E[:3,3]=np.linalg.solve(C[:3,:3],C[:3,3])
        E[3,:3]=C[3,:3]
        E[3,4]=C[3,4]
        E[4,3]=C[4,3]
        Z=R@W@E
        V=np.zeros_like(W)
        for j,b in enumerate(BLOCKS): V[b,j]=Z[b,j]
        V=V/np.sqrt(np.diag(V.T@R@V))[None,:]
        if np.max(np.abs(V-W))<tol:
            W=V; break
        W=V
    else: raise RuntimeError('Did not converge')
    C=W.T@R@W
    beta=np.r_[np.linalg.solve(C[:3,:3],C[:3,3]),C[3,4]]
    r2=np.array([C[:3,3]@beta[:3],beta[3]**2])
    vif=np.r_[np.diag(np.linalg.inv(C[:3,:3])),1.]
    f2=np.r_[beta[:3]**2/(vif[:3]*(1-r2[0])),r2[1]/(1-r2[1])]
    loads=np.diag(R@W[:,np.repeat(np.arange(5),4)]) if False else np.array([(R@W)[b,j] for j,b in enumerate(BLOCKS)])
    return dict(beta=beta,r2=r2,vif=vif,f2=f2,loadings=loads,weights=W,iterations=it+1)

def run():
 X=pd.read_csv(CSV).to_numpy(float); z=pls(X)
 rows=[]
 for i,p in enumerate(EXPECTED['paths']):
  for key,actual in [('beta',z['beta'][i]),('VIF',z['vif'][i]),('f2',z['f2'][i]),('t',abs(p['beta'])/p['se']),('p',2*norm.sf(abs(p['t'])))]:
   rows.append(dict(section='paths',label=p['path'],metric=key,reported=p[key],recomputed=float(actual),abs_diff=float(abs(actual-p[key]))))
 for i,p in enumerate(EXPECTED['r2']): rows.append(dict(section='r2',label=p['construct'],metric='r2',reported=p['r2'],recomputed=float(z['r2'][i]),abs_diff=float(abs(z['r2'][i]-p['r2']))))
 for i,p in enumerate(EXPECTED['indirect']):
  a=z['beta'][i]*z['beta'][3]
  rows.append(dict(section='indirect',label=p['effect'],metric='beta',reported=p['beta'],recomputed=float(a),abs_diff=float(abs(a-p['beta']))))
 import openpyxl
 wb=openpyxl.load_workbook(next(ROOT.rglob('*.xlsx')),data_only=True)
 reliability=[]
 for j,row in enumerate(list(wb['Reliability'].values)[1:]):
  xb=X[:,BLOCKS[j]]; cov=np.cov(xb,rowvar=False); raw_alpha=4/3*(1-np.trace(cov)/cov.sum()); R=np.corrcoef(xb,rowvar=False); rbar=(R.sum()-4)/12; a=4*rbar/(1+3*rbar); l=z['loadings'][j]
  vals=[a,l.sum()**2/(l.sum()**2+np.sum(1-l*l)),np.mean(l*l),l.min(),l.max(),xb.mean()]
  for name,expect,actual in zip(list(wb['Reliability'].values)[0][1:],row[1:],vals): rows.append(dict(section='Reliability',label=NAMES[j],metric=name,reported=expect,recomputed=float(actual),abs_diff=float(abs(actual-expect))))
  reliability.append(dict(construct=NAMES[j],alpha_standardized=a,alpha_raw=raw_alpha,rho_C=vals[1],AVE=vals[2],loading_min=vals[3],loading_max=vals[4],mean=vals[5]))
 # Straightline sensitivity can be reproduced directly; attention flags absent in supplied CSV.
 keep=np.ptp(X,axis=1)>0; zs=pls(X[keep]); sr=list(wb['Sensitivity_paths'].values)[3]
 vals=np.r_[zs['beta'],zs['r2']]
 for name,exp,a in zip(list(wb['Sensitivity_paths'].values)[0][2:],sr[2:],vals): rows.append(dict(section='Sensitivity_no_straightline',label=name,metric='value',reported=exp,recomputed=float(a),abs_diff=float(abs(a-exp))))
 out={'method':'Independent covariance-based reflective PLS-PM Mode A, path weighting; convergence max absolute normalized-weight change <1e-12','n':len(X),'iterations':z['iterations'],'checks':rows,'point_beta':z['beta'].tolist(),'r2':z['r2'].tolist(),'reliability':reliability,'straightline_removed_n':int(keep.sum()),'sensitivity_beta':zs['beta'].tolist(),'sensitivity_r2':zs['r2'].tolist()}
 (Path(__file__).resolve().parent.parent / 'validation/pls_point_verification.json').write_text(json.dumps(out,indent=2))
 pd.DataFrame(rows).to_csv(str(Path(__file__).resolve().parent / 'pls_point_comparison.csv'),index=False)
 print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
 print(pd.DataFrame(rows).groupby('section').abs_diff.max())
 print(pd.DataFrame(rows)[lambda d:d.abs_diff>1e-6].to_string(index=False))
if __name__=='__main__':run()
