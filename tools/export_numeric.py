#!/usr/bin/env python3
"""Export numeric-only saved results, with source and transformed checksums.
Usage: python tools/export_numeric.py RESEARCH_ROOT OUTPUT_DIRECTORY
"""
import hashlib,json,sys
from pathlib import Path
SOURCES=['research_v4/results/summary.json','research_v4/results/prediction_models.json','research_v2/results/h03_growth_crates.json','research_v2/results/h07_cross_Cargo.json','research_v2/results/h07_cross_Maven.json','research_v2/results/h07_cross_NPM.json','research_v2/results/h07_cross_Pypi.json']
def numeric(v):
 if isinstance(v,dict):return {k:numeric(x) for k,x in v.items() if not isinstance(x,str)}
 if isinstance(v,list):return [numeric(x) for x in v if not isinstance(x,str)]
 return v
if __name__=='__main__':
 root,out=map(Path,sys.argv[1:]);out.mkdir(parents=True,exist_ok=True);manifest=[]
 for rel in SOURCES:
  p=root/rel;target=out/p.name;target.write_text(json.dumps(numeric(json.loads(p.read_text())),indent=2)+'\n')
  manifest.append({'file':'results/'+p.name,'source_relative':rel,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'transformation':'Only numeric, boolean, null leaves retained; string-valued fields omitted. Private reports/code not copied.'})
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
