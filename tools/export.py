#!/usr/bin/env python3
"""Offline, single-worker privacy-minimizing graph export. No network requests.
Usage: python tools/export.py DATA_ROOT RESEARCH_ROOT OUTPUT_DIR
Requires pyarrow and duckdb; all other dependencies are standard library.
"""
import csv, hashlib, io, json, re, sqlite3, sys, zipfile
from pathlib import Path
import duckdb
import pyarrow.parquet as pq

BAD = re.compile(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?:gh[pousr]_|github_pat_|sk-proj-)[A-Za-z0-9_]{16,}|/Users/|/Volumes/|/home/|-----BEGIN .*PRIVATE KEY')
BASE = 'https://github.com/shibaeff/oss-dependency-network-data/releases/download/v1.0.0/'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()

def clean(row):
    for v in row:
        if BAD.search(str(v)): raise ValueError('Unsafe field rejected (value withheld)')
    return row

def write_rows(z,name,header,rows):
    n=0
    with z.open(name,'w',force_zip64=True) as f:
        text=io.TextIOWrapper(f,encoding='utf-8',newline='')
        w=csv.writer(text,lineterminator='\n');w.writerow(header)
        for row in rows: w.writerow(clean(row));n+=1
        text.flush();text.detach()
    return n

def ziprows(z,name):
    f=io.TextIOWrapper(z.open(name),encoding='utf-8',newline='');r=csv.reader(f)
    header=[x.strip().lstrip('# ') for x in next(r)]
    return header,r

def parquet_rows(p,cols):
    for b in pq.ParquetFile(p).iter_batches(batch_size=8192,columns=cols,use_threads=False):
        yield from zip(*(b.column(i).to_pylist() for i in range(len(cols))))

def build(data,research,out):
    out.mkdir(parents=True,exist_ok=True);records=[]
    def finish(p,id,source,license,inputs,nodes,edges,semantics):
        records.append(dict(id=id,asset=p.name,url=BASE+p.name,bytes=p.stat().st_size,sha256=sha(p),source=source,license=license,inputs=inputs,node_rows=nodes,edge_rows=edges,semantics=semantics))
        print(id,nodes,edges,flush=True)
    for folder in sorted((data/'graphs/crates/2026-11-12').iterdir()):
        if not (folder/'nodes.parquet').exists():continue
        p=out/('crates-'+folder.name+'.zip')
        # Preserve original IDs and all typed declarations, not a simple graph.
        with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            n=write_rows(z,'nodes.csv',['id','name','created_at','declared_at','version'],parquet_rows(folder/'nodes.parquet',['package_id','name','created_at','declared_at','version_str']))
            e=write_rows(z,'edges.csv',['source','target','kind','optional_any','optional_only','declarations'],parquet_rows(folder/'edges.parquet',['src','dst','kind','optional_all','optional_only','n_decl']))
        finish(p,'crates/'+folder.name,'https://static.crates.io/db-dump.tar.gz','NOASSERTION: public factual topology; no explicit dump license located; prior CC0 claim rejected',{f.name:sha(f) for f in folder.glob('*.parquet')},n,e,'See SCHEMA.md; declared edges, not resolved installations; optional_any is original optional_all bool_or.')
    for source in sorted((data/'raw/debian/2026-11-12').glob('*.csv.zip')):
        p=out/('debian-'+source.name)
        with zipfile.ZipFile(source) as src,zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            h,rows=ziprows(src,'nodes.csv');cols=[h.index(k) for k in ['index','name','kind','version']]
            n=write_rows(z,'nodes.csv',['id','name','kind','version'],([r[i] for i in cols] for r in rows))
            h,rows=ziprows(src,'edges.csv')
            e=write_rows(z,'edges.csv',['source','target','type','constraint','alternatives'],rows)
        finish(p,'debian/'+source.name.removesuffix('.csv.zip'),'https://networks.skewed.de/net/debian_dependencies','NOASSERTION: upstream dataset page does not state a data license; prior CC-BY claim not substantiated',{source.name:sha(source)},n,e,'Sanitized full relational graph; isolates, virtual/missing nodes, parallel edges and loops preserved; no maintainer/descriptions/gprops.')
        # A named, simple package-only dependency graph for analysis.
        named=out/('debian-'+source.name.replace('.csv.zip','-packages.zip'))
        con=duckdb.connect();con.execute("SET threads=1; SET memory_limit='512MB'")
        with zipfile.ZipFile(p) as z:
            _,rows=ziprows(z,'nodes.csv');nodes=[r for r in rows if r[2]=='package'];keep={r[0] for r in nodes}
            _,rows=ziprows(z,'edges.csv');pairs=sorted({(int(r[0]),int(r[1])) for r in rows if r[2] in ('Depends','Pre-Depends') and r[0] in keep and r[1] in keep and r[0]!=r[1]})
        with zipfile.ZipFile(named,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            nn=write_rows(z,'nodes.csv',['id','name'],((r[0],r[1]) for r in nodes));ee=write_rows(z,'edges.csv',['source','target'],pairs)
        finish(named,'debian-packages/'+source.name.removesuffix('.csv.zip'),'https://networks.skewed.de/net/debian_dependencies',records[-1]['license'],{source.name:sha(source)},nn,ee,'Original node IDs preserved; package-only Depends/Pre-Depends induced subgraph, deduplicated and loop-free; package isolates retained.');con.close()
    source=research/'historical.csv.zip';p=out/'npm2016-sanitized.zip'
    with zipfile.ZipFile(source) as src,zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        h,rows=ziprows(src,'nodes.csv');cols=[h.index(k) for k in ['index','name']]
        n=write_rows(z,'nodes.csv',['id','name'],([r[i] for i in cols] for r in rows))
        _,rows=ziprows(src,'edges.csv');e=write_rows(z,'edges.csv',['source','target'],rows)
    finish(p,'npm/2016','https://doi.org/10.6084/m9.figshare.3081640.v3','CC-BY-4.0; attribution via upstream DOI and network catalog; transformed CSV removes layout and graph metadata',{'historical.csv.zip':sha(source)},n,e,'2016 source node IDs, loops and edge multiplicities retained. Source excludes packages without any dependency relation.')
    import xml.etree.ElementTree as ET
    root=ET.parse(research/'dependencies.graphml').getroot();ns={'g':'http://graphml.graphdrawing.org/xmlns'}
    names=[n.attrib['id'] for n in root.findall('.//g:node',ns)];mapping={n:i for i,n in enumerate(names)}
    edges=json.loads((research/'edges.json').read_text());p=out/'npm-modern-sanitized.zip'
    with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        n=write_rows(z,'nodes.csv',['id','name'],enumerate(names));e=write_rows(z,'edges.csv',['source','target'],sorted({(mapping[r['source']],mapping[r['target']]) for r in edges}))
    finish(p,'npm/modern','https://registry.npmjs.org/','NOASSERTION: registry factual dependency relations only; no blanket package-content license asserted',{'edges.json':sha(research/'edges.json'),'dependencies.graphml':sha(research/'dependencies.graphml')},n,e,'Bounded 15-seed BFS pilot, latest metadata at cached retrieval times; depth <=5, cap 800 fetched; production only, boundary nodes included; not registry census.')
    # Catalog-only entries for conflicting upstream license metadata.
    for folder in sorted((data/'graphs/librariesio').iterdir()):
        records.append(dict(id='librariesio/'+folder.name,status='withheld-license-conflict',source='https://zenodo.org/records/3626071',license='CONFLICT: API metadata cc-by-4.0; description explicitly Attribution-ShareAlike 4.0; payload withheld pending clarification',inputs={f.name:sha(f) for f in folder.glob('*.parquet')},node_rows=pq.ParquetFile(folder/'nodes.parquet').metadata.num_rows,edge_rows=pq.ParquetFile(folder/'edges.parquet').metadata.num_rows))
    (out/'catalog.json').write_text(json.dumps(records,indent=2)+'\n')
    return records

if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit(__doc__)
    build(*(Path(x) for x in sys.argv[1:]))
