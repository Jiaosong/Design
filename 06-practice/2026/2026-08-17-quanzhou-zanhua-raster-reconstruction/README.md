# 2026-08-17 — Quanzhou Zanhua Raster Visualization Reconstruction Practice

Status: `EXECUTED / SELF-CHECKED / REVIEW PENDING`

Purpose: exercise exact-reference reconstruction together with semantic data-viz reconstruction on a supplied 735×1041 JPEG infographic. This practice is not project authority and does not self-award KEEP.

## Source boundary

- source: user-supplied 735×1041 JPEG;
- no image generation used;
- no OCR used for unreadable microcopy;
- unreadable text/variable meaning remained `UNREADABLE` rather than being invented;
- source raster is reference authority for visible geometry only, not proof of the original author's underlying data table.

## Pipeline exercised

`REFERENCE JPEG → ROI segmentation → mark-family detection → SOURCE_DATA.json → VISUAL_ENCODING_SPEC.json → parametric generator → editable SVG → same-size ROI readback → semantic topology/layer audit → deterministic regeneration`.

## Four reference-derived replacements

1. Main composite: common center/radii, outer thin arcs, teal annular band profile, detected medallion geometry, purple markers and reference-derived landscape support segments.
2. Radial chart: reference-derived center, inner/outer radii, ten dominant sector angles and teal/purple radial lengths.
3. Bubble matrix: reference-derived grid, bubble centers and raster-equivalent radii.
4. Alluvial: reference-derived endpoint rows and 52 pixel-traced paths.

## Fidelity delta

Relative to the earlier hand/proxy reconstruction:

- main composite MAE: `25.0618 → 19.5885`;
- main upper semicircle MAE: `38.6798 → 24.6687`;
- radial ROI MAE: `13.4175` current;
- bubble-matrix ROI MAE: `10.3209` current;
- alluvial ROI MAE: `29.4140 → 28.8175`.

A more sophisticated 19-layer contour parameter family was rejected because it worsened the actual main ROI (`19.7451 → 20.7063`) despite improving its own internal mask objective.

## Semantic-recovery delta

### Alluvial crossing identity

52 traced paths were audited for crossing-order inversion and local tangent continuation.

- `36 HIGH` identity paths;
- `11 MEDIUM`;
- `5 LOW`.

This establishes the blocker:

`PIXEL PATH != RECOVERED SOURCE RELATION`.

Medium/low crossing identities stay candidates even when the path is visually close.

### Landscape layer reconstruction

The accepted landscape extraction contained 46 skeleton support segments, including 28 horizontal contour segments. Continuation/stitching produced 11 stable top-to-bottom geometric layer candidates.

This is an editability improvement from L1 geometry segments toward L2 ordered geometric layers, but the original variable meaning remains unreadable.

`SEGMENT PATH != SEMANTIC LAYER`.

`GEOMETRIC LAYER ORDER != ORIGINAL VARIABLE MEANING`.

## Deterministic generation

The current JSON/spec/generator pipeline was executed twice under the same render path and returned:

- changed-pixel ratio: `0.0`;
- raster MAE: `0.0`;
- maximum channel error: `0`.

This proves deterministic roundtrip only; it does not prove reference fidelity, original data recovery or Design KEEP.

## Local artifact identities

Local runtime evidence generated during practice:

- `SOURCE_DATA_v11.json` — SHA256 `7fe9780b7e2b02e9a1b8722869cb39e2a1d447893a3746d433f7ec763a2d6d4e`;
- `VISUAL_ENCODING_SPEC_v11.json` — SHA256 `786a0b0fd1bfc2d59c3edbeec3dbb8962f8a72d43a8b18056bfbed0376dc5a53`;
- `ALLUVIAL_TOPOLOGY_IDENTITY_v11.json` — SHA256 `0b44b56ce72ff8d6c18141b4ceec95d20c5c0db222b03a860cb04012f623da11`;
- `MAIN_LANDSCAPE_STITCHED_LAYERS_v11.json` — SHA256 `b80883555f6042626555150ab1892b36bd34cb72efaa6425b58eadd165056bf4`;
- current parametric SVG before semantic-only v11 metadata update — SHA256 `5f70c19ae9bc6c460b592d16da0ff63997e5fb1da77e591fc8cb6cabd451fb35`.

## Skill deltas justified by this practice

1. A raster visualization reconstruction needs a data/encoding layer, not only vector tracing.
2. Reference-derived mark geometry must remain separate from original source-data meaning.
3. Alluvial crossings need explicit identity confidence.
4. Skeleton segments require a segment→group/layer promotion gate.
5. A target-ROI regression rejects a more sophisticated repair unless a necessary semantic/editability gain justifies the tradeoff.
6. Deterministic roundtrip is a separate gate from reference fidelity.
7. Exact-reference and data-viz verdicts must remain separate: `RF-C3 != VR-C3`.
