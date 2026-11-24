# OSS dependency network data

A privacy-minimized data publication, separate from private research repositories. **This is a partial publication, not a claim that all locally available snapshots are cleared for redistribution.**

## Download

Release: [v1.0.0](https://github.com/shibaeff/oss-dependency-network-data/releases/tag/v1.0.0)

| Public asset | Contents |
| --- | --- |
| [npm2016-sanitized.zip](https://github.com/shibaeff/oss-dependency-network-data/releases/download/v1.0.0/npm2016-sanitized.zip) | 154,744 package nodes; 517,098 directed dependency rows, including 47 self-loops; no isolates in the source population |
| [npm2016-partitions.csv.gz](https://github.com/shibaeff/oss-dependency-network-data/releases/download/v1.0.0/npm2016-partitions.csv.gz) | 154,744 numeric node/block assignments from a saved nested SBM fit |

Use [catalog.json](catalog.json) for exact bytes, SHA-256, sources, input fingerprints, row counts, licenses and publication status. [SHA256SUMS](SHA256SUMS) covers the release assets. [publication-manifest.json](publication-manifest.json) records GitHub asset IDs and provider digests after upload.

## Provenance and licensing — important corrections

* **npm2016:** source [DOI 10.6084/m9.figshare.3081640.v3](https://doi.org/10.6084/m9.figshare.3081640.v3), obtained through the [Netzschleuder npm catalog](https://networks.skewed.de/net/npm_dependencies). Attribution is to the original dataset creator identified by the linked DOI record, and the Netzschleuder conversion. The upstream catalog and cached archive identify **CC BY 4.0**. [License](https://creativecommons.org/licenses/by/4.0/). Changes: retained only node IDs/package names and edge endpoints; removed layout coordinates and graph-level metadata. The original ZIP is not republished because its graph metadata includes personal attribution strings; attribution is provided through the DOI here instead. Partitions are additional derived numeric results on the loop-free simple graph, not original source metadata.
* **Libraries.io 1.6.0:** the [actual Zenodo record](https://zenodo.org/records/3626071) is internally inconsistent: API `metadata.license.id` is `cc-by-4.0`, while the record description explicitly says **Creative Commons Attribution-ShareAlike 4.0 International** and requires attribution to Libraries.io, a project from Tidelift. **All four payloads (Cargo, Maven, NPM, Pypi) are withheld pending clarification.** No invented resolution of that conflict is used. Includes provenance about data from Libraries.io, a project from Tidelift; DOI 10.5281/zenodo.3626071. The upstream 24,890,021,718-byte archive is not mirrored.
* **crates.io:** the cached dump README and the [current upstream data-access source](https://github.com/rust-lang/crates.io/blob/main/svelte/src/routes/data-access/+page.svelte) describe access but do **not** supply the CC0 license asserted in older local notes. That assertion is rejected. **The 26 sanitized derived graphs are withheld until a redistribution license is established.** Source dump timestamp: `2026-11-11T02:00:11.696081176Z`; local retrieval label: `2026-11-12`. The 2,197,040,152-byte original dump, all owner/user identities, and all raw/interim tables are excluded.
* **Debian:** the [actual dataset page](https://networks.skewed.de/net/debian_dependencies) does not state the CC BY 4.0 license asserted in older notes. Netzschleuder's AGPL footer licenses website code, not automatically every hosted dataset. **All 19 sanitized release archives and 19 named package-only exports are therefore catalog-only pending clarification.** Original archives contain maintainer names/emails and are excluded regardless of licensing. Upstream public links are in the catalog.
* **Modern npm:** cached seed-selected registry relations were sanitized locally; no blanket upstream metadata redistribution license was verified. **Payload withheld**, with source hashes/counts/semantics cataloged. No live registry download was performed for this publication.

`NOASSERTION` means no license claim, **not** public domain and not permission to redistribute. Numeric aggregate results authored for this publication are supplied under CC0 to the extent of the publisher's rights; this does not relicense upstream databases. Repository tools are MIT licensed, independently of dataset licenses. See [LICENSE](LICENSE).

Upstream web evidence URLs, retrieval times and response fingerprints are recorded in [license-evidence.json](license-evidence.json). Full pages containing personal information are not copied here. Attribution does not imply endorsement.

## Schema and semantics

See [SCHEMA.md](SCHEMA.md). Every dependency edge points **dependent → declared dependency**; reverse reachability describes potential structural exposure, not observed runtime failure or an exploit. These graphs do not resolve version constraints or perform package installation.

## Offline tools and verification

Python 3.11+; one worker. Validation uses only the standard library:

```sh
python tools/validate.py downloads catalog.json
```

Download the asset ZIP into `downloads/` first. The validator checks SHA-256, byte size, ZIP CRC, exact member names, CSV widths, duplicate node IDs, endpoint membership, row counts, loop counts, isolates and prohibited credential/email/internal-path patterns. It prints one JSON result per present graph ZIP; it does not claim missing files were checked. For a standalone asset checksum use `shasum -a 256 downloads/npm2016-sanitized.zip`.

To reproduce **local sanitized exports** from existing cached inputs (no network; may include license-withheld outputs):

```sh
python -m pip install -r requirements.txt
python tools/export.py DATA_ROOT RESEARCH_ROOT local-exports
python tools/validate.py local-exports local-exports/catalog.json
python tools/prepare_public.py local-exports output-repository
python tools/export_partitions.py npm2016_blocks.npz npm2016-partitions.csv
```

`DATA_ROOT` and `RESEARCH_ROOT` are caller-supplied paths; no private machine paths are embedded. The input layout matches relative paths in `tools/export.py`; no upstream multi-GB downloads are automated. `prepare_public.py` is a conservative license gate and creates the initial catalog/checksums, not the separately registered partition supplement. It never uploads. DuckDB uses one thread/512 MB; Arrow reads batches with threads disabled. The serial validator retains only node and incident-ID sets; no full edge set. ZIP byte hashes can differ between export runs because ZIP timestamps are not normalized; compare the per-member CSV content for semantic reproducibility.

## Derived results and limitations

`results/` contains numeric-only saved aggregate results, not manuscripts, correspondence, logs, or a claim of freshly rerun experiments. String-valued fields were omitted to minimize accidental identifying metadata. `results/manifest.json` fingerprints original inputs and transformed files. Graph-statistic counts are distinct from typed source-edge counts: analytic crates graphs filter runtime/non-optional-only edges and collapse pairs; npm2016 analytic fits drop 47 loops. Counterexample node indices in saved numeric results refer to analytic dense relabelings, described in SCHEMA.md, not arbitrary source IDs. Cross-ecosystem numeric summaries do not include the withheld Libraries.io graph payloads.

`local-validation.json` is an executed validation report for **66 local graph ZIPs**, including withheld graphs. It is not a release inventory. The catalog explicitly distinguishes local fingerprints from published assets. No private report, student identity, personal name, email, token, owner list, or raw correspondence is intentionally published. Package names are public registry identifiers, not personal identity fields. Pattern scans are defense in depth, not a proof that arbitrary third-party strings can never resemble a personal name.

The most important remaining gap is upstream redistribution-license clarification; publication intentionally excludes uncertain payloads instead of presenting unsupported CC0/CC-BY claims.
