# C04 GIS Skill Execution v0.7

Project: `PRJ-C04-QINGJIANG-SHISHU`

Status: `EXECUTED / ACTUAL PREVIEW READBACK COMPLETE / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING`

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS`

## Current execution chain

`C04 Current → CH02 truth boundary → oleander-data-viz → Cartographic Task Hierarchy → oleander-story-and-board → oleander-delivery-qc → OLEANDER Artifact Review`

This run uses **no image generation**. Formal authority remains source CSV/JSON + current GeoTIFF inputs + editable SVG masters. PNG is preview/export only.

## Boards

1. `ENV-01｜坡度—坡向分析 / Slope & Aspect Analysis`
2. `ENV-02｜潜在汇水与径流方向 / Potential Drainage & Flow Direction`
3. `ENV-03｜环境综合分析 / Environmental Synthesis`

## Actual current data

- grid: `21×21 / 441 sampled cells`
- approximate sample spacing: `288 m E–W × 139 m N–S`
- elevation: `370–988 m`
- slope: median `12.5°`, P90 `32.4°`, max `53.1°`
- D8 accumulation: P90 `7`, max `48 upstream sampled cells`
- relative solar mean: summer `0.93`, equinox `0.77`, winter `0.49`

## Evidence boundary

- ENV-01 contour fields are display interpolation only; statistics remain original 441 samples.
- ENV-02 does not invent a continuous drainage network; derived arrows are shown only at top-10% sampled convergence cells.
- `D8 convergence ≠ drainage network / hydraulic capacity`.
- WorldCover AOI pixels: `HOLD / NO MAIN PROMOTION`.
- JRC Global Surface Water AOI pixels: `HOLD / NO MAIN PROMOTION`.
- No screenshot, WMS RGB, OSM absence, hand-drawn range, or generative image is used to substitute missing analytical pixels.

## QA

- 3 editable SVG masters created.
- 3 PNG previews reopened for producer actual-readback.
- ENV-03 first readback exposed misplaced elevation text; repaired and reopened.
- grayscale derivatives: generated.
- 50% far-read derivatives: generated.
- Machine QC: `PASS`.
- Independent design review: `PENDING` — producer does not self-assign KEEP.

## Package

Local package: `C04_GIS_SKILL_EXECUTION_v0.7.zip`

SHA256: `1437d78568fb634022b52dc0d5d84b230a7c898a640e0fbe69c5a0c52c1f6738`

`Artifact existence ≠ Design quality / Machine QC ≠ MAIN KEEP`.
