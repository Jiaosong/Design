# OLEANDER Technical Drawing — Editorial Callout Fidelity

Status: `candidate extension / PR #172`

Use with `REFERENCE_RECONSTRUCTION_FIDELITY.md`, `PIXEL_FORENSIC_PROTOCOL.md`, and `MULTILAYER_RELATION_RECONSTRUCTION.md` when a supplied reference contains small editorial side-icons, callout leaders, and dense labels whose fidelity cannot be judged from full-page metrics.

`ICON CROP != ICON COMPONENT`

`TEXT ROI != FULL-PAGE TYPOGRAPHY SCORE`

`LEADER NEAR TARGET != LEADER ON TARGET`

## 1. Leader target landing

For a callout relation, verify separately:

`LABEL / ICON → LEADER ROUTE → ELBOW(S) → ANCHOR CENTER → TARGET OBJECT`.

When the reference contains a visible filled anchor dot, record its center in source pixels and the candidate center. A leader that ends one or more pixels away from the source anchor remains a relationship-fidelity error even if the line appears visually close at page scale.

For compressed raster sources, local dark-dot/blob detection may be used as a producer diagnostic, but it must be visually confirmed on ambiguous intersections. The result is not independent KEEP evidence.

## 2. Editorial icon component boundary

Small surrounding pictograms may be too low-resolution to reconstruct internal vector semantics reliably while still being important to visual fidelity.

Allowed bounded recovery for R1/R3 reconstruction:

- isolate an explicit source box around the icon only;
- convert that bounded icon to vector cells/paths when needed for visual recovery;
- keep the icon inside one stable semantic component group;
- retain its relation identity, placement and scale as editable properties;
- do not embed the source bitmap as the final icon;
- do not treat the icon's internal recovered pixels as technical geometry or project authority.

This is `COMPONENT-LEVEL EDITABILITY`, not full semantic reconstruction of every pictogram stroke.

### Crop-contamination blocker

The icon source box must not silently include:

- adjacent label glyphs;
- leader segments that belong to the callout topology;
- neighboring symbols;
- unrelated panel geometry.

If crop contamination appears after rendering, repair the source box/mask before increasing palette/detail. A higher-fidelity contaminated crop is still wrong.

## 3. Editorial icon fidelity order

Repair in this order:

`SOURCE BOX → CROP CONTAMINATION → POSITION → SCALE → SILHOUETTE → PALETTE/TONE → MICRODETAIL`.

Do not micro-tune color while the icon is clipped or offset.

For pixel-vector extraction, increase palette/detail only after the component boundary is correct. Report the method and keep the component non-authoritative.

## 4. Typography-only ROI

Full-page MAE is a poor typography diagnostic because disappearing or lightened text can numerically improve a page dominated by white space.

For each important label, create a text-focused ROI and inspect:

- exact string;
- line break;
- text anchor/alignment;
- baseline;
- run width;
- visible bounding box;
- font size;
- inferred/exact font identity;
- fill/tone under the locked renderer;
- rotation for street/route labels.

Compare typography ROIs separately from full-page error. A lighter label is not an improvement merely because it lowers global MAE.

If the exact source font is unavailable, preserve editable text and record `FONT SUBSTITUTE / RF-C3 UNAVAILABLE` when the metric difference is material.

## 5. Street / route label calibration

Rotated labels must be calibrated in page coordinates, not only relative to a simplified candidate road geometry. Record:

- page-space center/baseline;
- rotation angle;
- text extent;
- route association;
- whether the current reconstructed route geometry itself is still approximate.

A correctly spelled street name placed on the wrong road segment is a relation error, not merely a typography error.

## 6. Targeted-fidelity report

For these references, add class-specific evidence:

- leader-target displacement register;
- icon-union ROI metrics;
- typography ROI metrics;
- selected reference/candidate contact sheet;
- full-page metrics only as secondary context.

Report before → after for the same ROI masks so improvement is attributable.

## 7. Promotion boundary

A producer may report:

- `SELF-CHECKED`;
- `REVISE`;
- `REVIEW PENDING`;
- measured pixel/anchor deltas.

The producer may not convert `0 px detected anchor displacement`, low icon ROI MAE, or improved typography ROI into `PIXEL KEEP`, `PROFESSIONAL FINISH PASS`, or RF-C3 when source/font/render conditions do not support it.
