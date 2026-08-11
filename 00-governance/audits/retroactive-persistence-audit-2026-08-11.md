# OLEANDER Retroactive Production Asset Persistence Audit — 2026-08-11

Status: `AUDIT COMPLETE / P0 RESCUED / REMEDIATION OPEN`
Governance: `Production Asset Persistence Gate v1.0 / PAP-G0—PAP-G6`
Scope: indexed OLEANDER production asset chains, canonical Drive `06_Practice/2026`, GitHub Actions artifacts where referenced, and File Library high-risk binary records.

## Decision boundary

This audit concerns durable byte availability. It does not upgrade or revoke visual, engineering, evidence, rights, user-test or release status unless byte-level reproducibility is itself required. Missing binaries block PAP/Promotion; they do not automatically erase historical execution evidence.

## Audit totals

- 31 asset-level rows
- 23 unique chains
- 7 confirmed `PERSISTENCE FAIL` chains
- 1 rescued `PERSISTENCE PASS` chain: `SP01-R02-GIS`
- 1 current `PERSISTENCE AT RISK` chain
- 8 healthy / durable-recoverable control chains
- 3 `NOT CREATED / N/A` chains
- 1 legacy-source chain explicitly decoupled from current authority
- 3 non-binary archive-incomplete chains

## P0 rescue completed — SP01-R02-GIS

The real QGIS runtime artifact was rescued from GitHub Actions artifact `9087641476` before its provider expiry `2026-09-10T03:15:45Z`.

Source identity:

- workflow run: `31454788861`
- head SHA: `9dab6e96f4446a0a8c76a7e7c825a6f98957274e`
- source digest: `68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`
- bytes: `759942`

Durable stores:

- PAP folder: `16rBzIy15N4g4Bq-HUBdYBianKQyIjplq`
- PAP Drive file: `12mafNIOtzzrYzIf2HTkjz4XcDq_xjSMI`
- Practice canonical mirror folder: `1_h4YvTsO8jXHajgwKua3Y5-87bup0DrF`
- Practice mirror file: `1DMpgFdV_vhdRunRqI3GOBD4rFvNI9DJc`

Independent readback was executed from both Drive copies. Each returned the same `759942` bytes, exact SHA match to the source digest, and `unzip -t` PASS. Spot-check confirmed `.qgz`, GPKG, 9 KDE GeoTIFF rasters, 3 QGIS Layout PNGs, GDAL/QGIS evidence, gate files and sensitivity metrics.

Decision: `PERSISTENCE PASS / RESCUED`.

This closes durable binary persistence only. QGIS runtime evidence remains valid; `Project CRS Gate` and `Project Data Gate` remain OPEN; Candidate Promotion remains NO.

Machine-readable receipt:

`00-governance/audits/pap-sp01-r02-gis-rescue-2026-08-11.json`

## Confirmed persistence-fail chains

1. `TIMER-R54-G3.2` — exact G3.2 `.blend`, canonical GLB and production ZIP cannot currently be re-materialized from a qualified durable store. Historical G0–G5 evidence remains; G7/Promotion stays locked.
2. `TIMER-POSTERLOCK` — audited POSTERLOCK package identity/SHA and constituent hashes survive, but the exact ZIP binary is not currently re-materializable. The older superseded audited ZIP is also missing.
3. `SP02-RELATIONAL-FIELD` — real Rhino `.3dm` plus two historical production ZIPs are not present in the canonical Drive folder and are not currently materializable from File Library.
4. `SP03-ARCH-GEN` — real `OLEANDER_Architecture_Generation_Protocol_01.3dm` was historically read-back verified but the current bytes are unavailable.
5. `B04-CROSS-MEDIA` — Notion/migration record and report survive; `OLEANDER_Cross_Media_Validation_2026-08-06.zip` does not.
6. `IP03-VISUAL-HIERARCHY` — inner evidence files partially survive in Drive, but `OLEANDER_Visual_Grid_01_Blocker_Resolution_v0.2_2026-08-07.zip` does not.
7. `SYNC-REPAIR-LEGACY` — `OLEANDER_GitHub_Notion同步修复包_2026-08-06.zip` has a recorded SHA but no current durable binary. It is legacy WORKING material, not current governance authority.

## Current at-risk chain

`XJ01-R02-SOURCE`

- `XJ01_R02_calibration_master.obj`
- `XJ01_R02_material_masks_v0_1.obj`

Both actual OBJ files still surface in File Library, but PAP requires real re-materialization + SHA verification. They are absent from the corresponding Drive R54 output folder. Status: `PERSISTENCE AT RISK / FILE LIBRARY ONLY`.

## Strong healthy controls

### SP01-R02 GIS

- two stable Drive file IDs
- independent re-download from both copies
- exact SHA match: `68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`
- unzip PASS
- status: `PERSISTENCE PASS / RESCUED`

### SP02-R03 Runtime Closure Handoff v1.4 FINAL

- Drive ZIP stable ID: `1lwdw6NehMEkdgvdD4C-Vg7g4PNu-QmOr`
- sidecar stable ID: `1B2Ro16RhRIO4qpSroUqv_dzt9pR7MXyc`
- expected/retrieved SHA: `8a0d1eb06efb270dd572708fdc722c5e466d46d2040839c594c156245cb24fd3`
- audit re-download: PASS
- unzip: PASS

Persistence PASS does not imply a real `.gh/.ghx` solve; that runtime gate remains separate.

Other durable-recoverable controls include SP03-R02 curated/raw runtime ZIPs, SP04-R02 Interoperability QA ZIP, C01 RealPhoto package, OLEANDER GitHub Migration package and durable Drive-native Motion records.

## Not-created / N/A

Do not misclassify absent native files when no native execution occurred:

- Fusion `.f3d` — not generated.
- Grasshopper `.gh/.ghx` — real runtime/solve not executed.
- Revit `.rfa/.rvt` — native Revit run not performed; software-neutral geometry path used.

## Non-binary archive completeness gaps

These are tracked separately from PAP core-binary loss:

- 2026-08-08 IP03 Product Interface — generated SVG/JSON/CSV files; Drive folder created but upload explicitly blocked.
- 2026-08-09 SP03 Light Sequence — generated SVG/JSON/CSV files; original folder did not receive files; later SP03-R02 is a separate durable production chain.
- IP04 Wayfinding optional AI PNG — core native Google Doc is durable; PNG was explicitly not claimed as archived.

## Remaining priority queue

### P1

- Timer G3.2 exact `.blend` + canonical GLB + production ZIP.
- Timer exact POSTERLOCK ZIP.
- XJ01 R02 OBJ source chain.

### P2

- SP02 Relational Field native/package chain.
- SP03 Architecture Generation `.3dm`.
- B04 Cross-Media ZIP.
- IP03 Visual Hierarchy ZIP.

### P3

- Legacy/superseded package recovery where useful.
- Backfill external package checksums + PAP receipts for durable-recoverable controls.
- Preserve identity legacy-source gaps as provenance only; never reconstruct them from previews under the old identity.

## Durable audit authority

Detailed 31-row registry and complete audit package are stored in Google Drive under:

`OLEANDER_Project-Archive/Production-Asset-Persistence/Retroactive-Audit-2026-08-11/`

Stable Drive IDs:

- folder: `1qbIwmGyjmGjiKNrjLZsbOoVvlPNtGgBb`
- complete audit ZIP: `1oYLWLODfEOlD7bY5fXLRDbk2ym1Dle0E`
- ZIP sidecar: `1bm1FtZPsAP__1m-sz1AjQXsz2batAC0l`
- Markdown: `16K5fpEaacKKhz0l-hYHDnNNuK4Z1pv7s`
- JSON registry: `10FEah_8T5xkkvF3rfcRbZQJIK_eYxjgQ`
- CSV registry: `15RqF2xWE12Al-jV7on6FeYGbia3eZMR6`
- remediation queue: `1q4tjHODxLCMT7XPfjiadia8mbi_qDHgZ`

Audit ZIP upload was independently re-downloaded from Drive. Retrieved SHA-256:

`db9a51dae4346afb522ff92f00f3cc7e1a629d8a1cd8f18b139ba6f9689fc1e7`

The external sidecar contains the same SHA and `unzip -t` passes.

## Required status-language correction

Historical `ARCHIVED` must not imply that the binary is durably present. Where a record survives but the package does not, use explicit wording such as:

- `RECORD ARCHIVED / BINARY PERSISTENCE FAIL`
- `INNER EVIDENCE PARTIALLY ARCHIVED / PACKAGE BINARY PERSISTENCE FAIL`
- `PERSISTENCE FAIL / SOURCE BINARY MATERIALIZATION MISSING`
- `PERSISTENCE PASS / RESCUED`

P0 is closed. Remaining remediation order is:

`P1 current-authority recovery → P2 historical recovery → P3 receipt/checksum backfill`
