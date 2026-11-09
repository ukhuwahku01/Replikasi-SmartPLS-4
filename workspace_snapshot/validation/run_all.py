"""Run independent numerical checks; no network or source-file changes."""
from pathlib import Path
import subprocess,sys,os
base=Path(__file__).resolve().parent
settings=os.environ.copy();settings['OPENBLAS_NUM_THREADS']='1';settings['OMP_NUM_THREADS']='1'
for relative in ['verify_pls.py','verify_pls_bootstrap.py','htmt/verify_htmt.py','htmt/verify_htmt_supplement.py','prediction/verify_prediction.py','build_deliverables.py']:
 print('Running',relative,flush=True)
 subprocess.run([sys.executable,str(base/relative)],cwd=base,env=settings,check=True)
print('Complete. See output/.',flush=True)
