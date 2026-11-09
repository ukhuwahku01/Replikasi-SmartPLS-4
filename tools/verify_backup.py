#!/usr/bin/env python3
"""Verify every snapshot file and optionally its original workspace source.
Uses Python standard library only; never accesses credentials or the network.
"""
from pathlib import Path
import argparse,hashlib,json,sys

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source-workspace',type=Path);args=ap.parse_args();repo=Path(__file__).resolve().parent.parent
 m=json.loads((repo/'BACKUP_MANIFEST.json').read_text());errors=[];seen=set()
 for e in m['files']:
  p=repo/e['backup_path'];seen.add(p.resolve())
  if not p.is_file():errors.append('Missing: '+e['backup_path']);continue
  if p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']:errors.append('Hash/size mismatch: '+e['backup_path'])
  if args.source_workspace:
   src=args.source_workspace/e['source_path']
   if not src.is_file() or sha(src)!=e['sha256']:errors.append('Source differs/missing: '+e['source_path'])
 actual={p.resolve() for p in (repo/'workspace_snapshot').rglob('*') if p.is_file()}
 for p in actual-seen:errors.append('Unmanifested snapshot file: '+str(p.relative_to(repo)))
 if len(m['files'])!=m['file_count'] or sum(x['bytes'] for x in m['files'])!=m['total_payload_bytes']:errors.append('Manifest totals inconsistent')
 sums=''.join(f"{e['sha256']}  {e['backup_path']}\n" for e in m['files'])
 if (repo/'SHA256SUMS').read_text()!=sums:errors.append('SHA256SUMS differs from manifest')
 if errors:
  print('\n'.join(errors));raise SystemExit(1)
 print(f"PASS: {m['file_count']} snapshot files, {m['total_payload_bytes']} bytes; all SHA-256 checks match.")
 if args.source_workspace:print('All original workspace files match the snapshot.')
if __name__=='__main__':main()
