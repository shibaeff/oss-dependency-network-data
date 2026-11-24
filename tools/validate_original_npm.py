"""Validate the collected, unmodified npm2016 CSV archive (stdlib only)."""
import csv
import hashlib
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path


def validate(path):
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist()) == {'nodes.csv', 'edges.csv', 'gprops.csv'}
        assert z.testzip() is None
        def rows(name):
            return csv.reader(io.TextIOWrapper(z.open(name), encoding='utf-8'), escapechar='\\')
        nr = rows('nodes.csv')
        assert next(nr) == ['# index', ' name', ' _pos']
        ids = set()
        for row in nr:
            assert len(row) == 3
            n, name, pos = row
            assert n.isdigit() and n not in ids
            ids.add(n)
            assert re.fullmatch(r'(?:@[A-Za-z0-9._~-]+/)?[A-Za-z0-9._~-]+', name)
            assert re.fullmatch(r'array\(\[\s*[-+0-9.eE]+\s*,\s*[-+0-9.eE]+\s*\]\)', pos)
            assert all(math.isfinite(float(v)) for v in re.findall(r'[-+0-9.eE]+', pos[7:-2]))
        er = rows('edges.csv')
        assert next(er) == ['# source', ' target']
        count = loops = 0
        incident = set()
        for row in er:
            assert len(row) == 2 and all(v in ids for v in row)
            count += 1
            loops += row[0] == row[1]
            incident.update(row)
        gr = rows('gprops.csv')
        assert next(gr) == ['# prop_name', ' value']
        props = dict(gr)
        assert set(props) == {'name', 'description', 'citation', 'url', 'upstream_license', 'tags'}
        assert 'CC BY 4.0' in props['upstream_license']
        assert props['url'] == 'https://doi.org/10.6084/m9.figshare.3081640.v3'
        # All graph metadata is reviewed public dataset description/citation/license.
        for value in props.values():
            assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|/Users/|/Volumes/|gh[pousr]_[A-Za-z0-9]+|-----BEGIN .*PRIVATE KEY', value)
        assert (len(ids), count, loops, len(ids-incident)) == (154744, 517098, 47, 0)
        return {'filename': path.name, 'bytes': path.stat().st_size,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'node_rows': len(ids), 'edge_rows': count, 'self_loops': loops,
                'isolates': len(ids-incident), 'zip_crc': 'passed',
                'columns': {'nodes.csv': ['index', 'name', '_pos'], 'edges.csv': ['source', 'target'], 'gprops.csv': ['prop_name', 'value']},
                'graph_property_keys': sorted(props),
                'review': 'All cells validated. Public package identifiers, numeric layout, endpoints and public scholarly attribution only; no identity tables, emails, credentials or internal paths.'}


if __name__ == '__main__':
    print(json.dumps(validate(sys.argv[1]), indent=2))
