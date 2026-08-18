# C04 GIS Current Reexecution v0.7.3

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Scope: strict Current OLEANDER reexecution of the user-supplied `C04_GIS_SKILL_EXECUTION_v0.7.zip`.

## Current owner DAG
`oleander-data-viz (PRIMARY) → oleander-story-and-board (presentation support) → oleander-delivery-qc (validator) → independent reviewer (HOLD / unavailable)`

## Current native figures
- `ENV-01` — Slope / Aspect — semantic live-text SVG.
- `ENV-02` — Potential Drainage / D8 — semantic live-text SVG.
- `ENV-SYN-01` — Environmental Synthesis — unweighted FIELD-verification triggers; **not a risk score**.

Stable slots not rebuilt by this minimum-sufficient rerun:
- `ENV-03 Land Cover` = HOLD / WorldCover AOI pixels missing.
- `ENV-04 Water History` = HOLD / JRC GSW AOI pixels missing.
- ENV-05 / ENV-06 remain existing current figures and are not mutated.

## Source / reproduction
- Uploaded v0.7 SHA256: `1437d78568fb634022b52dc0d5d84b230a7c898a640e0fbe69c5a0c52c1f6738`.
- Durable upstream v0.2.1 source package was independently re-retrieved from Drive ID `1n_Qyz_BN4VFP45nUHKrmRW4FrhF60s9_`; SHA256 `1c01ab71486183348e96fc27f738e200592e6a88f3a46fc8b77cc86913c3d075`.
- v0.7 source CSVs are byte-identical to v0.2.1 source/clean CSVs.
- slope/aspect reproduction max difference ≈ `2.09e-7°`; D8 = `441/441` exact; solar scenarios < `3.34e-16`.

## AR-S05 correction
Upstream v0.2.1 GeoTIFF values are source-consistent, but their transform used sample-center endpoint min/max as raster outer bounds, offsetting pixel centers inward. v0.7.3 writes corrected **derived** cell-center rasters locally. Upstream package remains immutable provenance. The corrected binaries are NOT claimed durable from this repository carrier.

## Actual preview delta
- removed smooth contour presentation from these three current boards; one displayed cell = one source sample;
- Qingjiang OSM context geometry unchanged, visual hierarchy reduced;
- first-pass legend / longitude-label collision was found during actual preview and repaired;
- north arrow + approximate projected scale added;
- grayscale + 50% readback completed.

## Status
`EXECUTED / SOURCE REPRODUCED / PRODUCER ACTUAL READBACK COMPLETE / COMPLIANCE PRECHECK PASS / AR-S09 NEW-BINARY PERSISTENCE HOLD / INDEPENDENT PROFESSIONAL DESIGN REVIEW HOLD / NO_PROMOTION`

Local complete package: `C04_GIS_CURRENT_REEXECUTION_v0.7.3.zip`  
Local ZIP bytes: `2171526`  
Local ZIP SHA256: `0429c969eba6774ee9e19e2d03994d7c01f917a8224299f4aa3b7c3b596c2649`

Repository persistence in this PR is **text carrier only**. The three current SVG masters, PNG derivatives, corrected GeoTIFFs and ZIP remain `LOCAL / NEW-BINARY PERSISTENCE HOLD`; no false durable equivalence is claimed.

Truth boundary: `NO IMAGE GENERATION / FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS`.

`Artifact existence ≠ Design quality / Compliance PASS ≠ Professional Design PASS / producer does not self-assign KEEP.`
