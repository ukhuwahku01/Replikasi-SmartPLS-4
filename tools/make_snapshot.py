#!/usr/bin/env python3
"""Create a byte-preserving snapshot of this task's research files.
No credentials or Git metadata are read. Existing different backup files are not overwritten.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,shutil
ROOTS=('attachments','validation','smartpls4_native')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source-workspace',type=Path,default=Path('/workspace'));args=ap.parse_args()
 repo=Path(__file__).resolve().parent.parent;source=args.source_workspace.resolve();entries=[];excluded=[]
 for name in ROOTS:
  base=source/name
  if not base.is_dir():raise SystemExit(f'Missing required source directory: {base}')
  for p in sorted(base.rglob('*')):
   if p.is_symlink():raise SystemExit(f'Unexpected symlink; not followed: {p}')
   if not p.is_file():continue
   relative=p.relative_to(source)
   if '__pycache__' in p.parts or p.suffix=='.pyc':excluded.append({'source_path':str(relative),'reason':'Generated Python bytecode cache'});continue
   target=repo/'workspace_snapshot'/relative;sha=digest(p)
   if target.exists() and digest(target)!=sha:raise SystemExit(f'Existing backup differs; preserve it before replacing: {target}')
   target.parent.mkdir(parents=True,exist_ok=True)
   if not target.exists():shutil.copy2(p,target)
   if digest(target)!=sha:raise SystemExit(f'Copy verification failed: {relative}')
   entries.append({'source_path':str(relative),'backup_path':str(target.relative_to(repo)),'bytes':p.stat().st_size,'sha256':sha})
 manifest={'format_version':1,'created_at_utc':datetime.now(timezone.utc).isoformat(),'user_facing_timezone':'Asia/Jakarta','repository':'https://github.com/ukhuwahku01/Replikasi-SmartPLS-4','source_roots':list(ROOTS),'file_count':len(entries),'total_payload_bytes':sum(e['bytes'] for e in entries),'excluded':excluded,'files':entries}
 (repo/'BACKUP_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 (repo/'SHA256SUMS').write_text(''.join(f"{e['sha256']}  {e['backup_path']}\n" for e in entries))
 print(json.dumps({'backed_up_files':len(entries),'bytes':manifest['total_payload_bytes'],'excluded_cache_files':len(excluded)}))
if __name__=='__main__':main()
