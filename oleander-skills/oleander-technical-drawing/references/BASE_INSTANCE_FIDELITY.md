# OLEANDER Technical Drawing — Base / Main-Body Instance Fidelity

Status: `candidate extension / PR #172`

Use with `MULTILAYER_RELATION_RECONSTRUCTION.md` and `REFERENCE_RECONSTRUCTION_FIDELITY.md` when several panels reuse one site/building/assembly but the reference renders that base with panel-specific visibility, omission, crop, tone or emphasis.

`GEOMETRY MASTER != RENDERED BASE INSTANCE`

`BASE VISUAL CARRIER != GEOMETRY AUTHORITY`

`IDENTICAL <use> IN EVERY PANEL != FIDELITY`

`LOW BASE-CARRIER RECALL != TYPOGRAPHY/JPEG PROBLEM`

## 1. Three different objects must remain separate

### `GEOMETRY_MASTER`
The canonical semantic/recoverable base geometry or source object used to keep panel relationships coherent. It owns stable anchors and object identity.

### `RENDERED_BASE_INSTANCE`
The way that master is shown in one panel: transform, crop, omission, visibility, tone, line density, local emphasis and occlusion.

### `BASE_VISUAL_CARRIER`
A reconstruction-only visual carrier used when an R1/R3 raster contains more neutral-line detail than can be economically reconstructed semantically during calibration. It may improve pixel fidelity but is **not** project/site/technical geometry authority.

The final reconstruction may contain all three. Do not collapse them into one object.

## 2. Base-instance register

Create `BASE_INSTANCE_REGISTER` when a repeated base materially affects fidelity.

For each panel record:

- panel ID;
- semantic master ID;
- semantic base-instance ID;
- page-space ROI;
- transform/crop;
- visibility/omission profile;
- base line/tone class;
- rendered visual-carrier ID if used;
- visual-carrier extraction boundary/method;
- truth/authority state;
- `does_not_prove` boundary;
- per-panel base-fidelity diagnostics.

If two panels render the same site differently, they must not silently share one identical visual instance merely because their semantic master is common.

## 3. Panel visibility is part of the drawing

Record panel-specific:

- shown/hidden building groups;
- faded context;
- vegetation presence;
- road/path emphasis;
- occluded objects;
- clipping/crop;
- line/tone suppression;
- panel-specific additions or deltas.

A correct master geometry with the wrong panel visibility still produces a wrong analytical drawing.

## 4. R3 bounded base visual carrier

For a compressed raster source, a bounded neutral-tone visual carrier may be used **only** when all conditions are met:

1. the semantic master remains present and separately identifiable;
2. the carrier is limited to the declared panel/body ROI;
3. it contains neutral base geometry only, not theme overlays, callout leaders or labels;
4. it is vector (`path/rect/polygon/...`), not an embedded `<image>`;
5. it is grouped by stable panel/tone/object IDs rather than mixed into theme geometry;
6. it is explicitly marked `STRUCTURED_VISUAL_VECTOR_NON_AUTHORITY`;
7. the carrier cannot become project geometry, survey, CAD/BIM, field or engineering authority;
8. producer review remains `REVISE / REVIEW PENDING` until independent review.

This is a fidelity device, not a substitute for semantic reconstruction where the base itself carries the design claim.

## 5. Contamination blockers

A base visual carrier automatically fails when it contains:

- route/theme colors that belong to the analytical overlay;
- editable labels converted into anonymous base paths;
- black callout leaders/anchors;
- side-icon pixels;
- content outside the declared body ROI;
- hidden raster/image embedding;
- an authority/status label implying the source-derived carrier is current project geometry.

`MORE PIXELS RECOVERED` does not excuse contamination.

## 6. Fidelity diagnostics

Use panel-specific diagnostics before full-page MAE:

- neutral/base carrier recall;
- neutral/base precision;
- neutral/base IoU;
- edge/centerline mismatch where applicable;
- panel ROI MAE / changed-pixel ratio;
- repeated-base anchor correspondence;
- visible omission/addition mismatch.

These are diagnostics, not universal acceptance thresholds.

### Stop rule

If the base/main-body carrier is materially incomplete, stop micro-tuning:

`FONT / ICON / AA / JPEG RESIDUAL → STOP → BASE ROI / PANEL INSTANCE / VISIBILITY / MAIN GEOMETRY`.

Do not spend another typography pass while the architecture/site body is still a simplified placeholder.

## 7. Semantic-master preservation

A visual carrier may hide the simplified semantic master from the final render to avoid double lines, but the semantic master must remain recoverable in the editable file/register.

Allowed pattern:

`SEMANTIC MASTER (recoverable, visually quiet/hidden) + PANEL VISUAL INSTANCE (fidelity) + THEME/RELATION SEMANTICS (editable and visible)`.

Forbidden pattern:

`REFERENCE PIXELS → ANONYMOUS FULL-PAGE PATH CLOUD → CALL IT GEOMETRY MASTER`.

## 8. Per-panel instance claim ladder

Use a separate base-instance claim:

- `BI-C0 / BASE IDENTIFIED` — repeated base and panel ROIs identified;
- `BI-C1 / MASTER + INSTANCE MODEL` — semantic master and panel instance profiles exist;
- `BI-C2 / PANEL VISIBILITY RECONSTRUCTED` — transform/visibility/omission/tone are materially reconstructed;
- `BI-C3 / VISUAL BASE FIDELITY CANDIDATE` — recoverable neutral/base carrier is visually close at target size.

`BI-C3 != RF-C3 != TD PASS != GEOMETRY AUTHORITY`.

## 9. Machine gate

Use `tools/validate_base_instances.py` with a `BASE_INSTANCE_REGISTER.json`.

The machine gate can check:

- semantic master exists;
- multiple panel instances are registered;
- each panel has a distinct visual-carrier group when panel-specific rendering is claimed;
- visual carriers contain no `<image>` or `<text>`;
- carrier fills/strokes remain near-neutral;
- carrier is explicitly non-authoritative;
- semantic base instance remains recoverable;
- register remains non-promoted.

Machine PASS cannot prove pixel fidelity, panel completeness, project geometry truth or Design KEEP.

## 10. Producer boundary

Producer may report measured improvements such as `V13 → V14 base IoU/MAE`, but may not convert them into KEEP. Independent review must reopen:

1. reference;
2. target-size render;
3. semantic master;
4. per-panel visual instances;
5. theme/relation layers;
6. contamination/authority boundary.
