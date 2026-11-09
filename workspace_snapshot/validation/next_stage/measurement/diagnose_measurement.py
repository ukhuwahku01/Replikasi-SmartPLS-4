"""Exploratory measurement diagnostics, original model/items preserved.
These are independent Python computations anchored to previously matched native PLS.
"""
from pathlib import Path
import sys,json
import numpy as np,pandas as pd
sys.path.insert(0,'/workspace/validation')
from verify_pls import pls
B=Path(__file__).resolve().parent
C=Path('/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv')
d=pd.read_csv(C);X=d.to_numpy(float);z=pls(X);Z=(X-X.mean(0))/X.std(0,ddof=0);Y=Z@z['weights'];names=['AIR','EXP','PP','TR','AD']
R=np.corrcoef(Y,rowvar=False);CL=np.corrcoef(np.column_stack([Z,Y]),rowvar=False)[:20,20:]
rows=[]
for i,name in enumerate(d.columns):
 j=i//4;other=[k for k in range(5) if k!=j];k=max(other,key=lambda k:abs(CL[i,k]));row={'indicator':name,'assigned_construct':names[j],**{f'corr_{n}':float(CL[i,h]) for h,n in enumerate(names)},'own_loading':float(CL[i,j]),'highest_other_construct':names[k],'highest_other_crossloading':float(CL[i,k]),'own_minus_highest_other_abs':float(abs(CL[i,j])-abs(CL[i,k]))}
 rows.append(row)
pd.DataFrame(rows).to_csv(B/'crossloadings.csv',index=False)
ave=np.mean(z['loadings']**2,axis=1);sqrtAVE=np.sqrt(ave);fl=R.copy();np.fill_diagonal(fl,sqrtAVE)
fl_pairs=[]
for i in range(5):
 for j in range(i+1,5):
  fl_pairs.append(dict(pair=names[i]+'-'+names[j],latent_corr=float(R[i,j]),sqrtAVE_a=float(sqrtAVE[i]),sqrtAVE_b=float(sqrtAVE[j]),passes_descriptive_FL=bool(abs(R[i,j])<min(sqrtAVE[i],sqrtAVE[j]))))
# Correlations between items of the two flagged construct pairs; descriptive only.
item_pairs=[]
for a,b in [('EXP','PP'),('EXP','AD')]:
 for ia in [d.columns.get_loc(a+str(i)) for i in range(1,5)]:
  for ib in [d.columns.get_loc(b+str(i)) for i in range(1,5)]:
   item_pairs.append(dict(construct_pair=a+'-'+b,item_a=d.columns[ia],item_b=d.columns[ib],pearson_r=float(np.corrcoef(X[:,ia],X[:,ib])[0,1])))
item_pairs.sort(key=lambda r:abs(r['pearson_r']),reverse=True)
pd.DataFrame(item_pairs).to_csv(B/'flagged_cross_item_correlations.csv',index=False)
pd.DataFrame(R,index=names,columns=names).to_csv(B/'score_correlations.csv')
pd.DataFrame(fl,index=names,columns=names).to_csv(B/'fornell_larcker_descriptive.csv')
res={'n':len(X),'method':'Independent Python PLS-PM Mode A/path weighting, score normalized; previously matched native point fit, not new SmartPLS run','constructs':names,'crossloadings':rows,'score_correlation_matrix':R.tolist(),'AVE':dict(zip(names,ave.tolist())),'sqrtAVE':dict(zip(names,sqrtAVE.tolist())),'fornell_larcker_pairs':fl_pairs,'crossloadings_own_highest_count':sum(r['own_minus_highest_other_abs']>0 for r in rows),'lowest_own_vs_other_margin':min(r['own_minus_highest_other_abs'] for r in rows),'highest_cross_item_pairs':item_pairs,'limitations':['These descriptive diagnostics do not replace the preregistered HTMT one-sided CI criterion.','Cross-loadings and Fornell-Larcker can appear acceptable despite HTMT inference not established.','Item wording and theoretical construct definitions are not present; numerical correlations do not prove wording overlap or justify deletion.','No items, cases or structural paths have been changed.']}
(B/'measurement_diagnostics.json').write_text(json.dumps(res,indent=2))
print('Own-loadings highest',res['crossloadings_own_highest_count'],'of20; smallestmargin',res['lowest_own_vs_other_margin'])
print('Fornell-Larcker descriptive passes',sum(r['passes_descriptive_FL'] for r in fl_pairs),'of10')
print(pd.DataFrame(rows)[['indicator','own_loading','highest_other_construct','highest_other_crossloading','own_minus_highest_other_abs']].to_string(index=False))
print('Top crossitems:',item_pairs[:8])
