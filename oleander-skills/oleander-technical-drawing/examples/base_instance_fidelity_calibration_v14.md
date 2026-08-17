# Base-instance fidelity calibration — V13 → V14

Status: `training/calibration provenance only / not Golden / not project geometry authority`.

This calibration came from a 944×2048 compressed analytical atlas in which seven panels reused one axonometric site. Flow/network carriers had already improved, but the central architectural/site body still used one visually simplified repeated base.

The calibration exposed a separate reconstruction problem:

`SEMANTIC MASTER CORRECT ENOUGH FOR RELATIONS != RENDERED BASE CLOSE ENOUGH FOR FIDELITY`.

## Effective repair

V14 separated:

- recoverable semantic `GEOMETRY_MASTER`;
- per-panel `RENDERED_BASE_INSTANCE`;
- bounded neutral-tone `BASE_VISUAL_CARRIER` for R3 fidelity only;
- thematic/flow/callout layers kept separate.

The semantic master remained in the SVG but was removed from visual contribution to avoid double simplified linework. No source bitmap was embedded.

Measured producer diagnostics at 944×2048:

- full-page MAE: `9.436 → 6.829`;
- changed pixels @ tolerance 12: `17.61% → 9.17%`;
- P01 neutral/base IoU: `0.344 → 0.750`;
- P02: `0.281 → 0.649`;
- P03: `0.345 → 0.763`;
- P04: `0.303 → 0.752`;
- P05: `0.334 → 0.746`;
- P06: `0.271 → 0.577`;
- P07: `0.459 → 0.783`.

These metrics are diagnostic only and do not award RF-C3, BI-C3, TD PASS or Design KEEP.

## Failed follow-up experiments

V15 lowered neutral thresholds and added exclusion rectangles in an attempt to recover more dark base detail while removing label/callout contamination. V16 restored the V14 thresholds while keeping the exclusions.

Both were rejected as producer experiments because they worsened the primary target-size diagnostics versus V14:

- V15 MAE `6.831`, changed@12 `9.76%`;
- V16 MAE `7.151`, changed@12 `10.09%`;
- V14 remained MAE `6.829`, changed@12 `9.17%`.

This is a useful anti-pattern:

`MORE BASE PIXELS != BETTER RECONSTRUCTION`.

Do not keep lowering extraction thresholds or expanding masks merely to increase apparent detail. Reopen contamination, panel ROI and actual target-size metrics.

## Skill consequences

The calibration produced `references/BASE_INSTANCE_FIDELITY.md` and the `BASE-01` machine regression.

Required separation for future work:

`GEOMETRY_MASTER → PANEL INSTANCE PROFILE → OPTIONAL NON-AUTHORITY VISUAL CARRIER → THEME/RELATION LAYERS`.

Producer verdict boundary remains `SELF-CHECKED / REVISE / REVIEW PENDING` until independent review reopens the actual candidate.
