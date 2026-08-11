# OLEANDER Production Asset Persistence Gate v1.0

Status: ACTIVE
Date: 2026-08-11
Scope: All production outputs that contain non-trivial binary authoring files, canonical models, render scenes, simulation models, CAD/native source files, packaged releases or other assets that cannot be reconstructed from text records alone.

## Decision

A production asset set may not enter Promotion / Archive PASS unless **at least one real binary copy of every required production asset is stored in a durable persistence location and has been independently retrieved and SHA-256 verified**.

Text records, filenames, hashes, screenshots, previews, Notion pages, GitHub Markdown, local `/mnt/data`, temporary sandbox paths, expiring workflow artifacts and signed URLs are evidence of identity or process only. They are **not** substitutes for the binary asset itself.

## Required production quartet

For production work that generates these asset classes, the persistence set must contain:

1. **Native source / authoring binary** — e.g. `.blend`, `.3dm`, `.f3d`, `.psd`, `.ai`, `.c4d`, `.hip`, native CAD/parametric scene or equivalent.
2. **Canonical model / interchange authority** — e.g. `.glb`, `.step/.stp`, `.iges/.igs`, `.obj`, `.fbx`, `.usd/.usdz` or project-defined canonical geometry/data binary.
3. **Production ZIP** — a complete immutable package containing the production scene/model, required configs/scripts and release/review artifacts for that gate.
4. **Checksum records** — `SHA256SUMS.txt` for package contents plus a checksum for the production ZIP itself.

If one of these classes is genuinely not applicable to the artifact type, it must be marked `N/A` with a reason in the persistence manifest. `N/A` may not be used to hide a missing asset that was actually generated or used.

## What counts as a durable binary persistence location

Accepted when a stable provider object/file ID exists and retrieval is possible:

- Google Drive stored binary file;
- GitHub Release asset;
- Git LFS object when the repository is actually configured for and retaining that asset;
- another managed durable object store with a stable identifier and documented retention policy;
- ChatGPT File Library **only when the actual binary file can be re-materialized/downloaded and a retrieval SHA check has passed**.

The following do **not** qualify as the sole durable copy:

- `/mnt/data`, local temp directories, notebook/container filesystems or ephemeral runtime storage;
- GitHub Actions artifacts with an expiry date, unless a second non-expiring durable copy already exists;
- signed temporary URLs;
- Notion pages, Markdown/JSON records or checksum-only records without the binary;
- PNG/JPG review images, videos or screenshots of a binary asset;
- a File Library search record that exposes only metadata, preview or checksum but cannot re-materialize the original bytes.

## PAP gates

| ID | Gate | PASS condition |
|---|---|---|
| PAP-G0 | Asset Inventory | Required native source, canonical model, production ZIP and checksum set are explicitly identified. |
| PAP-G1 | Local Integrity | Size and SHA-256 are calculated from the actual production bytes before upload. |
| PAP-G2 | Durable Upload | Every required binary has at least one durable provider copy with stable file/object ID. |
| PAP-G3 | Independent Retrieval | The durable copy is downloaded/re-materialized again after upload; upload success alone is insufficient. |
| PAP-G4 | Retrieval Integrity | Retrieved bytes match expected size + SHA-256; ZIP is opened/tested and native/canonical files are parsable where practical. |
| PAP-G5 | Persistence Manifest | Provider, stable ID, path/URL reference, SHA, byte size, verification date and retention class are recorded. |
| PAP-G6 | Cross-System Receipt | Notion + GitHub governance records point to the same manifest/status; Drive/object-store location is recorded. |

**AR-S09 may not PASS and Promotion / Archive may not begin until PAP-G0—PAP-G6 PASS for all triggered production binaries.**

## Status vocabulary

- `PERSISTENCE PENDING` — persistence work has not been completed or retrieval has not been verified.
- `PERSISTENCE FAIL` — a required binary is missing, only ephemeral copies remain, the stored object cannot be retrieved, or retrieved SHA/size does not match.
- `PERSISTENCE PASS` — all triggered PAP gates pass.

`PERSISTENCE PASS` concerns durable asset availability only. It does not imply visual, engineering, evidence, rights or release approval.

## Hard FAIL conditions

Any of the following blocks AR-S09 and Promotion / Archive:

- native production scene was used/generated but no durable binary copy exists;
- canonical model has only a filename/hash/preview record;
- production ZIP checksum exists but the ZIP itself cannot be retrieved;
- provider upload is claimed without stable object/file ID;
- upload succeeded but independent retrieval was not performed;
- retrieved size/SHA differs from the production record;
- sole copy is in an expiring workflow artifact or ephemeral runtime;
- Notion/GitHub/Drive records disagree about the authoritative binary location or SHA.

## Canonical folder pattern

Recommended durable-store structure:

`Production-Asset-Persistence/<Project>/<Version>/<Production-ID>/`

with:

- `native/`
- `canonical/`
- `package/`
- `checksums/`
- `receipts/`

The manifest is stored in `receipts/` and may be mirrored to GitHub as text. Binary authority stays in the qualified durable store.

## Persistence manifest minimum fields

Every persistence receipt must record:

- project / case / practice identity;
- version and production gate/run ID;
- artifact role: `native_source | canonical_model | production_zip | checksum`;
- filename;
- byte size;
- SHA-256;
- durable provider;
- stable provider file/object ID;
- durable path or provider URL reference;
- retention class / expiry if any;
- upload timestamp;
- independent retrieval timestamp;
- retrieved byte size and SHA-256;
- open/unzip/parse verification result;
- overall persistence status;
- Promotion eligibility.

## Promotion rule

The promotion chain is now:

`generate → QA → final artifact review → package → hash → durable upload → independent retrieval → SHA/open verification → PAP PASS → AR-S09 PASS → Promotion / Archive`

No `POST-REVIEW PASS`, renderer gate PASS, code PASS or checksum record may skip the persistence stage.

## Trigger incident｜Timer Light Basin R54 G3.2

The 2026-08-11 Timer Light Basin R54 G3.2 incident establishes the trigger case for this rule:

- the authoritative `R54_HERO_BEAUTY_G3_2.blend` identity, byte size and SHA were recorded;
- the production ZIP identity and SHA were recorded;
- review PNGs and gate records remained available;
- the actual G3.2 `.blend` / production ZIP could not later be re-materialized from the currently accessible persistence sources.

Therefore this asset set is retrospectively classified:

`PERSISTENCE FAIL / SOURCE BINARY MATERIALIZATION MISSING`

This does **not** revoke the historical G0–G5 render evidence. It blocks any claim that the G3.2 native production scene is durably recoverable and keeps the next Promotion gate locked until a valid binary is recovered or a newly authorized production scene is generated and persisted under this rule.
