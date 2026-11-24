#!/usr/bin/env python3
"""Export numeric npm2016 block assignments without serialized info strings.
Usage: python tools/export_partitions.py INPUT_BLOCKS_NPZ OUTPUT_CSV
Requires numpy. Row i maps to source node ID i in npm2016-sanitized.zip.
"""
import csv,sys
from pathlib import Path
import numpy as np
with np.load(sys.argv[1],allow_pickle=False) as z:
 a,b=z['level0'],z['level1']
 assert a.ndim==b.ndim==1 and len(a)==len(b)==154744
 assert a.dtype.kind in 'iu' and b.dtype.kind in 'iu'
 with Path(sys.argv[2]).open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['node_id','level0','level1'])
  w.writerows((i,int(x),int(y)) for i,(x,y) in enumerate(zip(a,b)))
