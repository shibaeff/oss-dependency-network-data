# Graph formats and snapshot semantics

All exported CSVs are UTF-8 with a header and LF record terminators, inside ZIP archives. Names are public package identifiers. Treat all cells as data, never evaluate formulas. All IDs are scoped to their own graph.

## Public npm2016 ZIP

* `nodes.csv`: `id` (integer), `name` (package name). IDs are original source indices, not re-ranked names. Source population excludes packages with no dependency relation; no missing isolates are synthesized.
* `edges.csv`: `source,target` (integers referencing nodes). A row `u,v` means package u declares a dependency on v. Original multiplicities and self-loops are retained (47 loops); no weights or version resolution.
* Snapshot: upstream early-2016 npm observation, not a fresh registry crawl. Changes relative to source ZIP: `_pos` coordinates and `gprops.csv` omitted. Original archive checksum is in `catalog.json`.

## Public partition supplement

Gzipped CSV: `node_id,level0,level1`, one row per npm2016 node. `node_id` is the original npm2016 integer node ID. `level0` and `level1` are nested directed degree-corrected stochastic-block-model labels from a cached fit. Labels are arbitrary integers, not package categories or causal groups. Source fit analyzed a deduplicated, loop-free graph: 154,744 nodes and 517,051 edges. The 47 source self-loops were dropped for that fit, not from the published source-derived ZIP. Fit settings and numerical results are historical saved outputs, not a new convergence guarantee. Potentially identifying free-text `info` fields from NPZ files are not exported.

## Catalog-only crates exports

* `nodes.csv`: `id,name,created_at,declared_at,version`. Original crates `package_id` is the ID; timestamps are UTC. `declared_at` is selected version publication time, not each edge's introduction time.
* `edges.csv`: `source,target,kind,optional_any,optional_only,declarations`. One row per selected source version, source package, target package, and dependency kind. `kind` is `runtime`, `build`, or `dev`. `optional_any` is Boolean OR of original optional declarations; `optional_only` is Boolean AND. `declarations` is the count collapsed into that row. Thus `optional_any` does **not** mean all declarations optional. Raw requirements and source version IDs are deliberately omitted from the sanitized export.
* For `at_DATE`, select the latest currently non-yanked version published at or before the metadata cutoff (publication time descending, version ID descending tie break). Historical yanking state is not recovered. Keep only dependencies whose targets also have a selected version. These are retrospectively reconstructed snapshots, not independently captured historical registries. Every selected node is retained, including isolates. No extra loop/pair removal is applied to the typed export.
* `latest` uses the dump's default version table, not the same selection rule as `at_DATE`.
* Available labels: Jan 1 and Jul 1 for 2015 through 2026, plus `at_2026-11-11` and `latest` (26 graphs). The `at` source JSON metadata governs exact cutoffs; dates are not inferred from ZIP creation time.
* Analytic dense indices in numeric results are zero-based order of ascending original package ID. Analysis uses runtime declarations, excludes pairs where `optional_only` is true, collapses repeated endpoint pairs, and drops self-loops. No assertion of installability or resolved features/targets is made.

## Catalog-only Debian exports

19 release labels: `0.93r6`, `buzz`, `rex`, `bo`, `hamm`, `slink`, `potato`, `woody`, `sarge`, `etch`, `lenny`, `squeeze`, `wheezy`, `jessie`, `stretch`, `buster`, `bullseye`, `bookworm`, `trixie`.

Each full sanitized release ZIP contains:

* `nodes.csv`: `id,name,kind,version`. `id` is the upstream node index; `kind` is `package`, `virtual`, or `missing`. Retains source population, including isolates. Maintainer, description, and all other node attributes are omitted.
* `edges.csv`: `source,target,type,constraint,alternatives`. Relationship field determines meaning; only `Depends` and `Pre-Depends` are hard dependencies. Other rows may encode `Recommends`, `Suggests`, `Enhances`, `Conflicts`, `Breaks`, `Replaces`, or `Provides`. Do not interpret every relationship as a dependency. Constraints are literal upstream strings, not evaluated; OR alternatives are separate edges with an alternatives count, not simultaneous mandatory requirements. Full source parallel relationships and loops are preserved.
* Upstream uses i386/all binary package indices and all release components; absent/virtual names are explicit nodes. Duplicate package names in indices use the upstream first entry. Archived distributions reflect final point releases, not initial release dates. Bookworm and trixie reflect upstream's 2026-10-30 archive snapshot. Local archive retrieval label is 2026-11-12.

A separate `-packages.zip` keeps `kind=package` nodes (including resulting isolates), only `Depends`/`Pre-Depends` edges between retained nodes, drops loops, and deduplicates endpoint pairs. `nodes.csv` is `id,name`; IDs stay original and may be noncontiguous. Saved analytic dense indices are instead zero-based order of retained original nodes; map through that ordered node table before comparing numeric result indices.

All original Debian ZIPs remain excluded: they contain personal maintainer fields.

## Catalog-only Libraries.io graphs

The four local parquet snapshots are inventoried but **no payload is released**. They derive from 1.6.0 (2020-01-12), not modern ecosystem censuses. Nodes are all projects in a platform, including isolates; IDs are original project IDs and names. Select latest project version preferring matching `latest_number`, then publication time and version ID descending. Directed edges select known same-platform destination projects, nonoptional declarations, and platform runtime kinds: Cargo `normal/runtime`, Maven `compile/runtime`, NPM/Pypi `runtime`. Deduplicate endpoint pairs and exclude self-loops. Raw names/created dates and literal minimum requirement strings exist locally; owner identities are not part of these graph snapshots. License ambiguity is documented in README.

## Catalog-only modern npm pilot

The sanitized local graph has a dense integer `id,name` mapping from cached GraphML node order and distinct `source,target` pairs from cached edges JSON. It does not contain maintainers, repositories, raw metadata or requirement strings. Sampling starts from 15 public package names (`react next express webpack vite typescript eslint jest axios lodash chalk commander debug prettier rollup`), follows latest production dependencies, bounds depth at 5 and fetched records at 800, and includes unfetched boundary packages. Dev/optional/peer declarations are omitted. Cache records were obtained at differing times; this is not one atomic registry snapshot. npm aliases are converted to target package names by the original collector. Scope and selection bias prevent registry-wide claims.

## Catalog/checksum fields

`node_rows` and `edge_rows` are executed row counts, not compressed line counts. `inputs` maps upstream/local input filenames to SHA-256. Published entries have `asset,url,bytes,sha256`; withheld entries have `status`, source/license notes, input checksums, and where locally exported, `local_export_bytes,local_export_sha256`. These local fingerprints do not imply public accessibility. All catalogs exclude raw personal metadata and private absolute paths. ZIP validation reports give retained self-loop and isolate counts for the exact local export bytes.
