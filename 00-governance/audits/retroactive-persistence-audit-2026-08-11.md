# OLEANDER Retroactive Production Asset Persistence Audit — 2026-08-11

Status: `v1.1 / PATH-RESOLUTION-CORRECTED / REMEDIATION OPEN`  
Governance: `Production Asset Persistence Gate v1.0 / PAP-G0—PAP-G6`

The original v1.0 Drive audit package remains preserved as a **pre-remediation discovery snapshot**. v1.1 is the current canonical status and corrects false negatives caused by same-name / migrated Drive directory resolution.

## Decision boundary

This audit concerns durable byte availability. Persistence recovery does not upgrade visual, engineering, rights, field/user-test or release/promotion status.

## Current totals

- 31 asset-level rows
- 23 unique chains
- **4 confirmed `PERSISTENCE FAIL` chains**
- **1 `PERSISTENCE AT RISK` chain**
- **11 healthy / recovered / durable-recoverable chains**
- 3 `NOT CREATED / N/A` chains
- 1 legacy-source chain explicitly decoupled from current authority
- 3 non-binary archive-incomplete chains

## New hard rule — Candidate Path Enumeration

A binary may be classified as missing only after this sequence is executed:

`filename search → enumerate all same-name / migrated / legacy candidate folders → parent lineage → actual folder contents → stable file ID → independent retrieval → SHA/size/open test`

**An empty duplicate folder is not evidence that the binary is lost.**

This rule was added because the initial audit produced real false negatives.

## Recovered chains

### SP01-R02-GIS — `PERSISTENCE PASS / RESCUED`

- source GitHub Actions artifact: `9087641476`
- source / retrieved SHA-256: `68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`
- bytes: `759942`
- PAP Drive file: `12mafNIOtzzrYzIf2HTkjz4XcDq_xjSMI`
- Practice mirror file: `1DMpgFdV_vhdRunRqI3GOBD4rFvNI9DJc`
- dual independent retrieval SHA PASS + unzip PASS

Project CRS/Data reality gates remain OPEN; Candidate Promotion remains NO.

### SP03-ARCH-GEN — `PERSISTENCE PASS / RECOVERED BY CORRECT PATH RESOLUTION`

The initial audit resolved an empty same-name folder `1QUYTwtijoMG_07qiv3dsOr_-eg89SZnm`. A second same-name folder was populated:

- populated folder: `1gX7ZSVeanhIUrwbwxOs6u8evM8u2dXnH`
- original `.3dm`: `1EeJlcfWb86j2LJVXptoGMv2-FjOTkjqw`
- bytes: `758952`
- SHA-256: `e7d8c9d493af5aedd7cad1bcef379807ce8e691846a7ff377c0e025b85e651c1`
- PAP copy: `10bXZezsLy6njrdENLVaLDAVnQ3Abra4A`
- source Drive retrieval + PAP re-retrieval SHA/size PASS
- file header identifies Rhino 3DM format; full Rhino semantic reopen remains PENDING

### B04-CROSS-MEDIA — `PERSISTENCE PASS / RECOVERED BY CORRECT PATH RESOLUTION`

The initial audit resolved empty same-name folder `1urcHNOBqdYYSj93Pkc9qnOhZHVR0YVta`. The populated canonical folder is `1PF2e5HMO6GQa6p_h-Je7DBbPe1AkmtBV`.

- original ZIP: `11pnHOagOL95zss9c8BwuryV51GJWp7KI`
- bytes: `723993`
- SHA-256: `b5d388cad2a4916275f2d8a6dc136824b978f3e59d8021356a896dcc8ac99eaa`
- source unzip PASS
- PAP copy: `1ZOJ7hPPYWYPFfs44xbpa0YIa6fuGKwV_`
- PAP re-retrieval SHA/size/unzip PASS

### IP03-VISUAL-HIERARCHY — `PERSISTENCE PASS / RECOVERED BY CORRECT PATH RESOLUTION`

The populated canonical folder was overlooked by the initial audit.

- folder: `1lg6rVBdRzXrxu1Aj7VVpfzvdKxbwKsqo`
- original ZIP: `1Tewq-5YT4ZMG0tDjkqR9Zz_Llz1a_FE2`
- bytes: `845606`
- SHA-256: `b50586e77ee1bb3deddaa2a69d520f9e6e34b867b0434e86c6781460c9eef7e1`
- 23 package files; unzip PASS
- PAP copy: `1MoJjL-PmeTjHoR4AV36Urm_9fg6zUZpa`
- PAP re-retrieval SHA/size/unzip PASS

The Visual Grid / `v0.7-R1` contents remain Legacy evidence and do not become current IP authority.

## Canonical v1.1 Drive package

Current canonical Drive folder:

- folder ID: `1PXhKKv1E5K9M7Lw3KBejJyCqmGiYQFlF`
- ZIP ID: `1P65rfFJjyBmZ7R-is9LWedR0PXbIvql8`
- external SHA sidecar ID: `1HOuIvyTwL5bqH1jrmK4ouV7qiON506O_`
- Markdown report ID: `1XHiQEaWiVYyJPaL5TYvbANVgSX2Ifq5W`
- CSV registry ID: `1M64cyf2bNkiVQVsPL6ytIusQFsX4AxvG`
- ZIP bytes: `20050`
- SHA-256: `83917cda1d50a74fbb52e5456743909371226b59d7f0af0f97fea66c226954ce`
- independent Drive re-download: **PASS**
- external sidecar match: **PASS**
- `unzip -t`: **PASS**

A second Drive folder created during re-verification was renamed `SECONDARY-COPY__Retroactive-Audit-v1.1-2026-08-11` and is explicitly **non-canonical**. Folder ID: `1Ov2Hk0qDFmcJYHgHb4rajjp0VDnLdlB9`.

## Remaining confirmed FAIL chains

1. `TIMER-R54-G3.2` — exact G3.2 `.blend`, canonical GLB and production ZIP still cannot be re-materialized. Historical G0–G5 evidence remains; G7/Promotion stays locked.
2. `TIMER-POSTERLOCK` — package identity/SHA and constituent hashes survive, but exact POSTERLOCK ZIP bytes are not currently re-materializable.
3. `SP02-RELATIONAL-FIELD` — real Rhino `.3dm` plus two historical ZIPs remain missing after exact-name, naming-variant, canonical-folder, Digital-Skills and Legacy intake searches.
4. `SYNC-REPAIR-LEGACY` — legacy WORKING package has a recorded SHA but no durable binary; no current governance-authority impact.

### SP02 exact historical identity

Expected `.3dm`:

- `OLEANDER_Relational_Field_01_State_B.3dm`
- SHA-256 `644dd36bbdd8303aa8f0b51ed34e8f00dbfcd0f7a1e9f9a9eae46ee8ea68cc41`
- `1,136,022` bytes

Known folder `1a0hTLo0tUF8Ey1c7o5vO8sKmblso5tgI` is empty. No regenerated substitute may inherit the historical identity.

## Current AT RISK — XJ01-R02-SOURCE

Actual File Library objects still exist:

- `XJ01_R02_calibration_master.obj`
- `XJ01_R02_material_masks_v0_1.obj`

However, the Drive connector rejects File Library file IDs as uploadable connector file references. Until exact bytes can be materialized, hashed and re-uploaded to a durable store, status remains `PERSISTENCE AT RISK / FILE LIBRARY ONLY`.

## Not-created / N/A

Do not misclassify absent native files when execution never occurred:

- Fusion `.f3d` — not generated.
- Grasshopper `.gh/.ghx` — real runtime/solve not executed.
- Revit `.rfa/.rvt` — native Revit run not performed.

## Current remediation order

`P1 Timer/XJ01 → P2 SP02 Relational Field → P3 legacy provenance + receipt/checksum backfill`

Canonical v1.1 audit package SHA-256:

`83917cda1d50a74fbb52e5456743909371226b59d7f0af0f97fea66c226954ce`
