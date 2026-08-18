# C04｜GIS / Environmental Analysis Redo v0.2.1

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Date: `2026-08-18`  
Upstream: `environment-analysis/v0.2` / PR #249  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS`

## 1｜Material delta only

v0.2.1 does **not** change source data, values, CRS, route topology, current object locks, or evidence status. It repairs presentation semantics exposed by actual-preview readback:

- ENV-01: explicitly shows the 21×21 regional sample grid; slope is classed; aspect arrows are reduced so the figure cannot be read as high-resolution site survey.
- ENV-02: removes the continuous-stream impression; keeps D8 sampled-cell accumulation and marks only high-convergence sampled cells. `DERIVED DRAINAGE ≠ HYDRAULIC DESIGN`.
- ENV-05: replaces one averaged heatmap with summer-solstice / equinox / winter-solstice small multiples, making `RELATIVE SCENARIO` the first-read semantics.
- ENV-03: unchanged `HOLD`; ESA WorldCover 2021 v200 is the intended analytical source, but AOI categorical pixels are not locally materialized/read back.
- ENV-04: unchanged `HOLD`; JRC Global Surface Water is the intended analytical source, but AOI occurrence/seasonality pixels are not locally materialized/read back.
- ENV-06: unchanged spatial authority: `ROUTE-03` is preserved 1:1; current-operation evidence stays in a separate overlay; unbound new-program anchors remain OPEN.

## 2｜Current artifact state

`EXECUTED / PRODUCER ACTUAL-PREVIEW READBACK COMPLETE / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING`

The producer does **not** assign `KEEP`, `DESIGN PASS`, `MAIN`, or Promotion.

## 3｜Binary persistence

Durable Drive package: `C04_GIS_REDO_SPLIT_v0.2.1.zip`  
Drive file ID: `1n_Qyz_BN4VFP45nUHKrmRW4FrhF60s9_`  
Size after independent retrieval: `3,032,975 bytes`  
SHA-256: `1c01ab71486183348e96fc27f738e200592e6a88f3a46fc8b77cc86913c3d075`  
Independent retrieval → rebuild byte-equivalence: `true / PERSISTENCE PASS`.

Persistence PASS proves package recovery only. It does not prove Design PASS, GIS source completeness, Field truth, or Engineering validity.

## 4｜Review frontier

Independent review must inspect actual v0.2.1 previews against current OLEANDER Artifact Review System:

1. ENV-01 — sample-grid honesty / slope-aspect hierarchy / false-precision risk;
2. ENV-02 — potential terrain convergence must not read as a hydraulic drainage network;
3. ENV-03 / 04 — HOLD must read immediately as missing analytical raster evidence, not as a finished analysis page;
4. ENV-05 — relative scenario meaning must precede decorative heatmap reading;
5. ENV-06 — `ROUTE-03` spatial-authority preservation + current-operations evidence hierarchy;
6. whole set — `Evidence → Interpretation → Design Impact`, C04 specificity, first-read, professional finish and cross-media consistency.

No independent verdict = no `KEEP`.