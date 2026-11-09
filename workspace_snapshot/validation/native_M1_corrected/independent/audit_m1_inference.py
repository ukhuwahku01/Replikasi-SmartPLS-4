#!/usr/bin/env python3
"""Narrow verification of corrected native five-node M1 bootstrap inference."""
from pathlib import Path
import json,hashlib
from scipy import stats
from openpyxl import load_workbook
OUT=Path('/workspace/validation/native_M1_corrected/independent')
FILE=Path('/workspace/attachments/510e4ab6-8e13-4421-bf7e-f75ae9606f06/KidSense_M1_DenganTR_Bootstrap_10000.xlsx')
PREVIOUS=Path('/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx')
HTMT_JSON=Path('/workspace/attachments/d0bcb909-7b59-4061-ba39-2de66241055c/KidSense_HTMT_10000_validation.json')
ONE=Path('/workspace/validation/native_htmt_one_sided/independent/independent_one_sided_htmt.json')
ORDER=['AIR','EXP','PP','TR','AD']
def norm(t):return '-'.join(sorted((x.strip() for x in t.split('<->')),key=ORDER.index))
def main():
 w=load_workbook(FILE,data_only=True);s=w['Complete data set'];old=load_workbook(PREVIOUS,data_only=True)['Complete data set']
 meta={w['Navigation'].cell(i,2).value:w['Navigation'].cell(i,3).value for i in range(4,9)}
 settings={s.cell(i,2).value:s.cell(i,3).value for i in range(696,730) if s.cell(i,2).value and s.cell(i,3).value is not None}
 def extract(rows,pctoffset,bcoffset):
  out=[]
  for i in rows:
   name=s.cell(i,2).value;beta,mean,se,t,p=[s.cell(i,j).value for j in range(3,8)];lo,hi=[s.cell(i+pctoffset,j).value for j in (5,6)];bclo,bchi=[s.cell(i+bcoffset,j).value for j in (6,7)]
   tt=abs(beta)/se;pp=2*stats.t.sf(tt,9999)
   out.append({'effect':name,'source_row':i,'beta':beta,'mean':mean,'SE':se,'t_native':t,'p_native':p,'t_recomputed_absbeta_over_SE':tt,'t_difference':tt-t,'t9999_two_sided_p_numeric_check':float(pp),'p_check_difference':float(pp-p),'percentile_CI95_two_sided':[lo,hi],'corrected_CI95_two_sided':[bclo,bchi],'percentile_excludes_zero':lo>0 or hi<0,'corrected_excludes_zero':bclo>0 or bchi<0,'p_nominal_below_005':p<.05})
  return out
 paths=extract(range(12,19),11,22);indirect=extract(range(75,78),7,14);total=extract(range(98,105),11,22)
 bypath={x['effect']:x for x in paths}
 for r in indirect:
  origin=r['effect'].split(' -> ')[0];product=bypath[f'{origin} -> TR']['beta']*bypath['TR -> AD']['beta'];r['product_of_paths']=product;r['difference_from_product']=r['beta']-product
 oldpct={norm(old.cell(i,2).value):[old.cell(i,j).value for j in (3,5,6)] for i in range(466,476)}
 oldbc={norm(old.cell(i,2).value):[old.cell(i,j).value for j in (3,6,7)] for i in range(480,490)}
 py={p['pair']:p for p in json.loads(HTMT_JSON.read_text())['pairs']};htmt=[]
 for i in range(484,494):
  pair=norm(s.cell(i,2).value);a=[s.cell(i,j).value for j in (3,5,6)];b=[s.cell(i+14,j).value for j in (3,6,7)]
  htmt.append({'pair':pair,'point':a[0],'PCT_CI95_two_sided':a[1:],'corrected_CI95_two_sided':b[1:],'max_abs_difference_vs_M0native_PCT':max(abs(v-o) for v,o in zip(a,oldpct[pair])),'max_abs_difference_vs_M0native_corrected':max(abs(v-o) for v,o in zip(b,oldbc[pair])),'point_difference_vs_python':a[0]-py[pair]['HTMT+']})
 result={'source':str(FILE),'source_sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'metadata':meta,'settings':settings,'paths':paths,'specific_indirect':indirect,'total_effects':total,'max_abs_t_difference':max(abs(r['t_difference']) for r in paths+indirect+total),'max_abs_p_t9999_numeric_check_difference':max(abs(r['p_check_difference']) for r in paths+indirect+total),'htmt':htmt,'max_abs_HTMT_table_difference_vs_M0native':max(max(r['max_abs_difference_vs_M0native_PCT'],r['max_abs_difference_vs_M0native_corrected']) for r in htmt),'current_HTMT_header_PCT':[s.cell(483,j).value for j in (5,6)],'current_HTMT_header_corrected':[s.cell(497,j).value for j in (6,7)],'prior_authoritative_one_sided_native_file':json.loads(ONE.read_text())['source'],'conclusion_notes':['Corrected bootstrap belongs to KidSense_M1_Eksploratori and estimates all seven paths plus three specific indirect effects.','AIR direct effect is not significant at nominalalpha.05 and its interval includes0; this is not proof the populationdirecteffect is0 and not proof fullmediation.','EXP and PP direct effects plus allthree specificindirect effects are positive with percentile95% intervals excluding0. Report directandindirect associations in exploratoryM1, not causal mediation or confirmatorymodeldiscovery.','AIR TOTAL effect differs from AIR DIRECT: nativep.047521 andpct95% excludes0, but corrected95% crosses0. Preserve this methoddifference if totaleffect is discussed.','CurrentHTMT bounds are two-sided2.5%/97.5%; allpoints andCIbounds match earlierM0native exactly. Addingdirectpaths did not resolve measurementdiscrimination.','Keep priornativeBCaONE-sided95% run as source for threshold.90:EXP-PPupper.908139 andEXP-ADupper.912789 remain not established;8of10meetcriterion. Do not rename currentupper97.5 to95.','The p numerical cross-check using t(df9999) differs by at most 1.4e-8 and gives identical alpha.05 decisions; retain native p, do not claim an exact reproduction of its numerical routine or a rerun of bootstrap draws.','No modelselection or causalclaim follows merely from significantposthoc paths. Retain design-only parentalperception/hypotheticalconditionaladoption interpretation.']}
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'M1_inferential_check.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k not in ['paths','specific_indirect','total_effects','htmt']},indent=2))
if __name__=='__main__':main()
