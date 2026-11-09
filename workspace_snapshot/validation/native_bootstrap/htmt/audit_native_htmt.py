#!/usr/bin/env python3
"""Compare uploaded native SmartPLS HTMT point estimates and two-sided CIs.
Does not reconstruct a native one-sided 95% upper endpoint from two-sided CIs.
"""
from pathlib import Path
import json,re,hashlib
from openpyxl import load_workbook
OUT=Path('/workspace/validation/native_bootstrap/htmt')
FILE=Path('/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx')
PREVIOUS=Path('/workspace/attachments/d0bcb909-7b59-4061-ba39-2de66241055c/KidSense_HTMT_10000_validation.json')
ORDER=['AIR','EXP','PP','TR','AD']
def norm(pair):
 a,b=[x.strip() for x in pair.split('<->')]
 return '-'.join(sorted((a,b),key=ORDER.index))
def main():
 w=load_workbook(FILE,data_only=True);s=w['Complete data set']; ref={x['pair']:x for x in json.loads(PREVIOUS.read_text())['pairs']}
 pct={norm(s.cell(i,2).value):{'row':i,'point':s.cell(i,3).value,'mean':s.cell(i,4).value,'lower_025':s.cell(i,5).value,'upper_975':s.cell(i,6).value} for i in range(466,476)}
 bc={norm(s.cell(i,2).value):{'row':i,'point':s.cell(i,3).value,'mean':s.cell(i,4).value,'bias':s.cell(i,5).value,'lower_025':s.cell(i,6).value,'upper_975':s.cell(i,7).value} for i in range(480,490)}
 settings=[{'row':i,'name':s.cell(i,2).value,'value':s.cell(i,3).value} for i in range(668,708) if s.cell(i,2).value and s.cell(i,3).value is not None]
 rows=[]
 for pair,r in ref.items():
  p=pct[pair];b=bc[pair]
  row={'pair':pair,'native_percentile':p,'native_BC':b,'prior_python_point':r['HTMT+'],'point_difference_native_minus_python':p['point']-r['HTMT+'],'prior_python_percentile_two_sided':r['percentile_CI95_two_sided'],'prior_python_BC_two_sided_upper_975':r['BC_upper97.5_two_sided'],'percentile_lower_difference_native_minus_python':p['lower_025']-r['percentile_CI95_two_sided'][0],'percentile_upper_difference_native_minus_python':p['upper_975']-r['percentile_CI95_two_sided'][1],'BC_upper_difference_native_minus_python':b['upper_975']-r['BC_upper97.5_two_sided'],'native_point_below_090':p['point']<.9,'native_point_below_085':p['point']<.85,'native_percentile_upper_975_below_090':p['upper_975']<.9,'native_BC_upper_975_below_090':b['upper_975']<.9,'native_percentile_upper_975_below_1':p['upper_975']<1,'native_BC_upper_975_below_1':b['upper_975']<1,'native_one_sided_upper_95':None,'native_one_sided_endpoint_status':'NOT_EXPORTED_CANNOT_RECONSTRUCT_FROM_2.5_97.5_BOUNDS'}
  rows.append(row)
 changes=[]
 for r in rows:
  prior=ref[r['pair']]['percentile_CI95_two_sided'][1]<.9
  if prior!=r['native_percentile_upper_975_below_090']:
   changes.append({'pair':r['pair'],'prior_PCT_upper975':ref[r['pair']]['percentile_CI95_two_sided'][1],'native_PCT_upper975':r['native_percentile']['upper_975'],'interpretation':'Native upper endpoint is below .90; prior Python endpoint was just above .90. Draw equivalence is not established; this near-boundary classification differs between the two bootstrap outputs. The cause cannot be isolated from summaries alone.'})
 result={'source_file':str(FILE),'source_file_sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'sheet':'Complete data set','settings':settings,'run_summary':{'samples':10000,'test_type':'Two-tailed','significance_level':.05,'selected_CI_method':'Percentile bootstrap','also_exported_CI_table':'Bias-corrected confidence intervals','seed_description':'Fixed seed; numeric value not shown in these settings','save_results_per_sample':'No','CI_endpoints_exported':[.025,.975],'native_one_sided_upper95_available':False},'pairs':rows,'max_abs_point_difference':max(abs(r['point_difference_native_minus_python']) for r in rows),'max_abs_percentile_lower_difference':max(abs(r['percentile_lower_difference_native_minus_python']) for r in rows),'max_abs_percentile_upper_difference':max(abs(r['percentile_upper_difference_native_minus_python']) for r in rows),'max_abs_BC_upper_difference':max(abs(r['BC_upper_difference_native_minus_python']) for r in rows),'native_count_point_below_090':sum(r['native_point_below_090'] for r in rows),'native_count_point_below_085':sum(r['native_point_below_085'] for r in rows),'native_count_PCT_upper975_below_090':sum(r['native_percentile_upper_975_below_090'] for r in rows),'native_count_BC_upper975_below_090':sum(r['native_BC_upper_975_below_090'] for r in rows),'native_count_PCT_upper975_below_1':sum(r['native_percentile_upper_975_below_1'] for r in rows),'native_count_BC_upper975_below_1':sum(r['native_BC_upper_975_below_1'] for r in rows),'percentile_threshold_090_changes':changes,'interpretation':['All original-sample HTMT estimates match previous Python values to floating-point precision. Bootstrap intervals are close but do not match exactly; numeric seed and draw equivalence cannot be established from exported settings.','Two-sided 95% percentile and BC upper97.5 endpoints exceed .90 for EXP-PP and EXP-AD. Do not claim all pairs meet this .90 criterion.','All two-sided percentile and BC intervals lie below 1. This weaker criterion is satisfied for all pairs but is not equivalent to the .90 criterion.','Desired native one-sided upper95 endpoints are not provided. Cannot convert or interpolate upper97.5 into upper95 from the available endpoint summaries. A one-sided native run or full per-sample native estimates is required.','For eight pairs, observed upper97.5<.90 also bounds the smaller upper95 below .90 for the same distribution; for EXP-PP and EXP-AD, upper97.5>=.90 alone does not determine the unexported upper95 classification.','Previous Python one-sided BC upper95 values .909878 (EXP-PP) and .913699 (EXP-AD) remain Python findings; they are not native one-sided estimates.']}
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'native_htmt_audit.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k not in ['settings','pairs']},indent=2))
 print('\nPAIR | native point | PCT97.5 | BC97.5 | dPCT97.5 | dBC97.5')
 for r in rows:print(r['pair'],r['native_percentile']['point'],r['native_percentile']['upper_975'],r['native_BC']['upper_975'],r['percentile_upper_difference_native_minus_python'],r['BC_upper_difference_native_minus_python'])
if __name__=='__main__':main()
