# Original collected data, v1.1.0

## Published payload

`historical.csv.zip` is byte-for-byte the retained collected npm2016 CSV ZIP, not a newly sanitized export. It contains `nodes.csv` (index, name, _pos), `edges.csv` (source, target), and `gprops.csv` (prop_name, value). All columns and rows were reviewed with `python tools/validate_original_npm.py historical.csv.zip`; results are in `raw-npm2016-validation.json`. No ZIP member was removed or rewritten. Historical mixed-case package names are valid source identifiers.

Original here means **original collected archive**, not original registry HTTP responses, nor a claim that this ZIP is the original Figshare TXT download. Graph metadata, including its literal dataset-name value, is preserved exactly rather than repaired. The cited Figshare dataset offers TXT files; this archive is a CSV conversion. The old v1.0.0 sanitized ZIP removes layout and graph metadata, and its partition supplement is a derived result.

## Attribution and source license

Slijepčević, Tomislav (2016). *The NPM software dependency network (npmjs.com).* figshare. Dataset. https://doi.org/10.6084/m9.figshare.3081640.v3

Related paper: T. Slijepčević, *Package equivalence in complex software network*, https://arxiv.org/abs/1602.03681 (2016). CSV conversion distributed through Netzschleuder, https://networks.skewed.de/ . The previously recorded per-dataset Netzschleuder link does not currently resolve; do not treat that link as independent license verification. The live Figshare API explicitly identifies version 3 as public, non-confidential and **CC BY 4.0**, and the collected archive independently carries the same license. Selected current primary-source evidence is in `raw-license-evidence.json`.

License: https://creativecommons.org/licenses/by/4.0/ ; legal code: https://creativecommons.org/licenses/by/4.0/legalcode . Keep attribution, license and modification information when redistributing. This release makes no further changes to the collected CSV conversion and does not imply endorsement. Public scholarly citation names are retained, not private participant information.

## Explicit exclusions

`raw-publication-manifest.json` identifies the original archive filenames, sizes, available checksums and upstream retrieval locations for 19 Debian ZIPs, the crates.io dump, and the Libraries.io dump. These **21 withheld payloads are not published by publishing their manifest**. Debian archives have maintainer identities and detected email fields; the license remains unverified. crates.io data-access documentation (https://crates.io/data-access) permits retrieval but establishes no explicit dump redistribution license; extracted users, OAuth and owner tables are not republished. Libraries.io https://zenodo.org/records/3626071 conflicts between its API license field and description. The two large tarballs exceed GitHub release asset limits and were neither split nor uploaded. Previously collected sidecar hash provenance is explicit; no giant re-download/read was performed.

Modern npm registry JSON was sanitized at collection and must not be called original API bytes. It remains withheld pending license clarification. Cached HTTP headers, extracted identity tables, private reports, student identities, internal paths and credentials are excluded. No private repository visibility is changed.
