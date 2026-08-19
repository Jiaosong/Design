# C04 GIS Map-Embedded Redo v0.9.0 — Execution Receipt

Project: `PRJ-C04-QINGJIANG-SHISHU`
Chapter: `CH02 / 场地与山水分析`
Date: `2026-08-19`

## Execution state

`EXECUTED / PRODUCER ACTUAL READBACK COMPLETE / MAP-EMBEDDED-SPATIAL-CLAIM PRODUCER PRECHECK PASS / INDEPENDENT PROFESSIONAL DESIGN REVIEW HOLD / NO_PROMOTION`

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`.

## Source authority

- Terrain/elevation authority remains the durable `21×21 / 441` remote sample grid.
- Source coordinates: `EPSG:4326`.
- Metric display/derivative CRS: `EPSG:32649`.
- OpenStreetMap Qingjiang centerline is context geometry only.
- `ROUTE-03` is not used by these three plates and is unchanged.
- Source precision is **not** promoted by this redesign.

## New map-embedded placement rule applied

All geographically locatable findings are encoded on-map at the corresponding sample/geometry position. The previous detached conclusion lane is removed. Off-map / floating metadata is restricted to the minimum legend, units, thresholds, necessary numbers and source/precision status.

- `ENV-01`: P90 steep samples + major connected sample clusters `S1–S4` labelled directly on-map.
- `ENV-02`: D8 accumulation values at exact sample positions + high-accumulation clusters `A1–A5` labelled directly on-map. Adjacency cue is `NOT A CHANNEL`.
- `ENV-SYN-01`: slope / D8 accumulation / winter-solar triggers at exact sample positions + multi-trigger clusters `M1–M4`; `NOT A RISK SCORE`.

Sample-cluster envelopes are presentation cues around connected source samples. They are **not** surveyed site boundaries or continuous measured zones.

## Precision boundary

- Slope P90: `32.41262472180764°`.
- D8 accumulation P90: `7 sampled cells`.
- Winter relative solar P10: `0.2355468767438297`.
- 50 m contour lines are linear-between-source-sample cartographic guides only; they do not add measurements or increase source resolution.
- Copernicus DEM GLO-30 public COG remains the intended higher-resolution terrain source, but tile bytes were not materialized in this runtime. No silent substitution occurred.
- `ENV-03 Land Cover` and `ENV-04 Water History` remain `HOLD` pending actual analytical pixels.

## Native local package

`C04_GIS_MAP_EMBEDDED_REDO_v0.9.0.zip`

- bytes: `7,553,612`
- SHA256: `2a3ddd6779378d50d97917ace7993c9cfb423432ed05697f682214d5acd08058`

Native contents include editable SVG masters, 3840×2160 PNG review derivatives, grayscale/far-read QC, source CSV copies, trigger classification CSV, source/precision notes, execution receipt and SHA manifest.

**Persistence boundary:** this GitHub receipt records the execution but does not claim the local SVG/PNG/ZIP bytes are stored byte-equivalently in GitHub. Artifact existence/persistence and professional design approval remain separate gates.

## Workflow / Skill

Owner chain: `oleander-data-viz → oleander-story-and-board → oleander-delivery-qc → independent reviewer`.

This branch also updates the reusable Skill rules so future spatial-analysis layouts cannot move a locatable finding into a detached sidebar as the primary `WHERE` carrier.

No AI image generation was used.
