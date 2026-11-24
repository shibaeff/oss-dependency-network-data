#!/usr/bin/env python3
"""Validate downloaded ZIP assets against catalog: hashes, CSVs, endpoints and privacy.
Usage: python tools/validate.py ASSET_DIRECTORY [CATALOG_JSON]
One worker; streams edges; retains node IDs and incident IDs only.
"""
import csv,hashlib,io,json,re,sys,zipfile
from pathlib import Path
BAD=re.compile(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?:gh[pousr]_|github_pat_|sk-proj-)[A-Za-z0-9_]{16,}|/Users/|/Volumes/|/home/|-----BEGIN .*PRIVATE KEY')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def rows(z,name):
 with z.open(name) as raw:
  r=csv.reader(io.TextIOWrapper(raw,encoding='utf-8',newline=''));header=next(r)
  assert len(header)==len(set(header))
  for row in r:
   assert len(row)==len(header),(name,'width')
   assert not any(BAD.search(x) for x in row),(name,'privacy pattern')
   yield row

def validate(folder,catalog):
 reports=[]
 for item in json.loads(catalog.read_text()):
  if 'asset' not in item:continue
  p=folder/item['asset']
  if not p.exists():continue
  assert p.stat().st_size==item['bytes'];assert digest(p)==item['sha256'],p.name
  if not p.name.endswith('.zip'):continue
  with zipfile.ZipFile(p) as z:
   assert z.testzip() is None
   assert set(z.namelist())=={'nodes.csv','edges.csv'}
   ids=set();n=0
   for row in rows(z,'nodes.csv'):
    assert row[0] not in ids;ids.add(row[0]);n+=1
   e=loops=0;incident=set()
   for row in rows(z,'edges.csv'):
    a,b=row[:2];assert a in ids and b in ids,(p.name,'dangling edge');e+=1;loops+=a==b;incident.add(a);incident.add(b)
   assert n==item['node_rows'] and e==item['edge_rows'],p.name
   reports.append(dict(asset=p.name,nodes=n,edges=e,self_loop_rows=loops,isolates=len(ids-incident),sha256=item['sha256']))
  print(json.dumps(reports[-1]),flush=True)
 assert reports,'No assets found'
 return reports
if __name__=='__main__':
 folder=Path(sys.argv[1]);catalog=Path(sys.argv[2]) if len(sys.argv)>2 else Path('catalog.json')
 validate(folder,catalog)
