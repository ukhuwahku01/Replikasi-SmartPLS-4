#!/usr/bin/env python3
"""Scoped audit of native M1 topology vs mismatched algorithm/bootstrap exports."""
from pathlib import Path
import json,hashlib
from openpyxl import load_workbook
OUT=Path('/workspace/validation/native_M1/independent')
FILES={'intended_M1':'/workspace/attachments/7140d531-a2d0-41c7-9894-32ddb8885a16/KidSense_M1_Eksploratori.xlsx','new_algorithm':'/workspace/attachments/26bd700e-350c-4942-a407-07f79b4542ff/KidSense_M1_Algorithm.xlsx','new_bootstrap':'/workspace/attachments/e18b7f20-4dc0-4d43-b5dc-9cdf66b0ef0d/KidSense_M1_Bootstrap_10000.xlsx'}
def inspect(path):
 w=load_workbook(path,data_only=True);s=w['Complete data set'];n=w['Navigation']; meta={n.cell(i,2).value:n.cell(i,3).value for i in range(4,9)}
 def find(label):return [i for i in range(1,s.max_row+1) if s.cell(i,2).value==label]
 start=find('Inner model')[0];header=[s.cell(start+1,j).value for j in range(3,s.max_column+1)];nodes=[v for v in header if v not in [None,'']];edges=[]
 for r in range(start+2,start+2+len(nodes)):
  source=s.cell(r,2).value
  for c,target in enumerate(header,3):
   v=s.cell(r,c).value
   if isinstance(v,(int,float)) and v!=0:edges.append({'source':source,'target':target,'source_row':r,'column':c,'value':v})
 start_outer=find('Outer model')[0];items=[]
 for r in range(start_outer+2,s.max_row+1):
  label=s.cell(r,2).value
  if label in [None,'']:break
  items.append(str(label).lstrip('\ufeff'))
 settings={}
 for r in range(1,s.max_row+1):
  key=s.cell(r,2).value
  if key in ['Complexity','Save results per sample','Confidence interval method','Significance level','Test type','Samples','Seed'] and s.cell(r,3).value is not None:settings[key]={'value':s.cell(r,3).value,'row':r}
 indirect=[]
 for title in ['Total indirect effects','Specific indirect effects']:
  matches=find(title)
  if not matches:
   indirect.append({'section':title,'status':'not present'});continue
  r=matches[0];indirect.append({'section':title,'title_row':r,'following_rows':[{'row':i,'cells':[s.cell(i,j).value for j in range(2,8)]} for i in range(r+1,min(r+8,s.max_row)+1)]})
 evidence=[{'row':r,'text':s.cell(r,2).value} for r in range(1,s.max_row+1) if isinstance(s.cell(r,2).value,str) and ('Running samples [' in s.cell(r,2).value or s.cell(r,2).value in ['All calculations done.','Calculating indirect effects.','Calculating specific indirect effects'])]
 return {'file':path,'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'metadata':meta,'inner_model_header_row':start+1,'nodes':nodes,'node_count':len(nodes),'edges':edges,'edge_count':len(edges),'items':items,'item_count':len(items),'settings':settings,'indirect_sections':indirect,'completion_evidence':evidence}

def main():
 reports={name:inspect(path) for name,path in FILES.items()}
 edges={name:{(e['source'],e['target']) for e in r['edges']} for name,r in reports.items()}
 result={'exports':reports,'algorithm_and_bootstrap_same_topology':edges['new_algorithm']==edges['new_bootstrap'],'both_new_topologies_match_intended_M1':edges['new_algorithm']==edges['intended_M1'] and edges['new_bootstrap']==edges['intended_M1'],'missing_nodes_new':['TR'],'missing_intended_paths_new':sorted(' -> '.join(e) for e in edges['intended_M1']-edges['new_bootstrap']),'length2_directed_paths_new':[f'{a}->{b}->{d}' for a,b in edges['new_bootstrap'] for c,d in edges['new_bootstrap'] if b==c],'diagnosis':'The latest algorithm and bootstrap exports analyze a 4-node 3-path 16-indicator model with no TR mediator, not the intended 5-node 7-path 20-indicator M1. The bootstrap explicitly used Complete (slower) and completed 10000 samples. No directed two-step path exists, so absent indirect effects are explained by model topology, not an Amount of results setting left below Complete.','safe_conclusions':['AIR->AD beta0.1281935, p0.0421857 belongs only to the 4-node model without TR. It is not the direct effect controlling TR in 5-node M1.','Correct intended-M1 algorithm report gives AIR->AD beta0.0456046 and three indirect point estimates, but its matching native M1 bootstrap is not among these new exports.','Do not combine M1 point estimates with standard errors, confidence intervals, p-values or model-fit bootstrap thresholds from the no-TR model.','The no-TR exports may be retained as a separate exploratory alternative with explicit topology; they are not corrupt merely because labels suggest M1.','No mediation classification can be based on the no-TR bootstrap. Correct M1 algorithm point estimates alone do not establish native bootstrap significance of its direct or indirect effects.'],'rerun_steps':['In the SmartPLS project, select the editable KidSense_M1_Eksploratori model diagram (not the report/model named pls-sem). Confirm AD,AIR,EXP,PP,TR and four indicators each before calculation. XLSX reports are evidence and not the editable model.','Confirm seven paths AIR/EXP/PP->TR, TR->AD, and AIR/EXP/PP->AD. Preserve original model and data; do not remove TR or edit spreadsheet numbers.','Run the PLS-SEM algorithm on that active diagram, then run Bootstrapping from that same model: Complete (slower),10000 samples,Two-tailed,alpha0.05,Percentile bootstrap to match planned direct/indirect inference; use Fixed seed and record numeric seed if interface exposes it.','Verify resulting report metadata/model name, inner matrix includes TR, outer matrix has20 items, Path coefficients has7 effects, Specific indirect effects has AIR/EXP/PP->TR->AD with bootstrap SE/CI. Generic omitted notice alone is not a reason to toggle Complete again.','Export algorithm and bootstrap reports with distinct filenames and record they belong to the same5-node M1. Keep previous4-node exports separately labelled rather than overwriting evidence.']}
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'M1_export_identity_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps({k:v for k,v in result.items() if k!='exports'},indent=2,ensure_ascii=False))
 print({k:{'nodes':v['nodes'],'paths':v['edge_count'],'items':v['item_count']} for k,v in reports.items()})
if __name__=='__main__':main()
