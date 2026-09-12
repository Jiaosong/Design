# C04 CH02 GIS Landscape Analytical Drawing Redo v0.9

Project: `PRJ-C04-QINGJIANG-SHISHU`

Status: `PRODUCER EXECUTED / ACTUAL PREVIEW R2 / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO_PROMOTION`

## Why this is a redo

The previous GIS boards were rejected by the user because increasing output pixels, interpolation density or panel complexity did not solve the actual problem. This rerun applies the current `oleander-data-viz` Landscape GIS Analytical Drawing binding and rebuilds the presentation grammar from scratch:

`DOMINANT TERRAIN FIELD → ONE ANALYTICAL VARIABLE → MAPPED SECTION / EVIDENCE INSET → SPATIAL FINDING → FIELD CONSEQUENCE`

The target is a landscape-architecture analytical drawing, not a GIS dashboard or software screenshot.

## Reference digestion transferred into production

- one large spatial field owns first read;
- continuous terrain / contours / water precede decorative styling;
- raw source grid stays auditable but exits MAIN visual grammar when it overwhelms spatial reading;
- one analytical variable per panel;
- hydrology is rendered as D8 flow hierarchy + convergence markers, not large colored cells;
- plan and section are mapped together where vertical terrain relation matters;
- professional density comes from line, contour, object specificity and annotation, not blur/glow;
- project aesthetics bind to cartography but do not dissolve it.

## CH14 binding

Palette is inherited from the current C04 CH09-P01 CH14 implementation:

- Bone Mist `#F1EDE4`
- River Black `#111918`
- Deep Water `#133B3C`
- Jade Current `#2E7571`
- Wet Stone `#65706A`
- Sediment Sand `#D8C9B1`
- Cinnabar `#B8543E`

Grammar: `CONTEMPORARY EDITORIAL + LANDSCAPE SPACE / LINE + TRACE / brand presence LIGHT`.

## Precision boundary

Current executed local boards still use the existing `21×21 / 441` remote sample authority. A `321×321` continuous display surface is allowed only for contour / relief readability and is explicitly `DISPLAY DERIVED / DOES NOT INCREASE SOURCE PRECISION`.

The true precision frontier is **real 30 m source materialization**. `acquire_render_glo30.py` is committed here to materialize the public Copernicus GLO-30 `N30/E109` tile, crop the current CH02 analytical corridor, read CRS / transform / NoData, rerun slope/aspect/D8/solar, and regenerate the same drawing system from true raster cells.

The current tool surface cannot create/launch a new GitHub workflow, so this acquisition is **prepared but not executed**. Do not claim the current boards as 30 m GIS.

## Stable IDs / truth

- `ENV-01` Slope / Aspect — producer artifact rebuilt locally.
- `ENV-02` Drainage — producer artifact rebuilt locally; R1 muddy hillshade rejected, R2 repaired to muted elevation field + crisp contours + D8 hierarchy.
- `ENV-SYN-01` Environmental Synthesis — locked-extent small multiples; no risk score.
- `ENV-03` Land Cover — HOLD.
- `ENV-04` Water History — HOLD.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS`.

No image generation was used.
