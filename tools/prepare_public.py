#!/usr/bin/env python3
"""Reduce a local export catalog to explicitly license-cleared public assets.
Usage: python tools/prepare_public.py EXPORT_DIR REPOSITORY_DIR
Never uploads anything. Unknown/conflicting upstream licenses stay catalog-only.
"""
import json,sys
from pathlib import Path

def prepare(exports,repo):
 records=json.loads((exports/'catalog.json').read_text())
 for item in records:
  if item['id'].endswith('/0'):item['id']=item['id'][:-1]+'0.93r6'
  if item.get('asset') and item['id']!='npm/2016':
   item['local_export_sha256']=item.pop('sha256');item['local_export_bytes']=item.pop('bytes')
   item.pop('asset');item.pop('url');item['status']='withheld-unverified-upstream-license'
  elif item.get('asset'):item['status']='published'
 (repo/'catalog.json').write_text(json.dumps(records,indent=2)+'\n')
 (repo/'SHA256SUMS').write_text(''.join(f"{x['sha256']}  {x['asset']}\n" for x in records if 'asset' in x))
 return records
if __name__=='__main__':prepare(*(Path(x) for x in sys.argv[1:]))
