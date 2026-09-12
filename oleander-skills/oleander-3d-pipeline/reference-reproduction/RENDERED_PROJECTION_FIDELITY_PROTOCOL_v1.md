# OLEANDER 3D Pipeline — Rendered Projection Fidelity Protocol v1

A calibrated Source curve is not sufficient evidence that the **final visible model** reproduces the reference. This gate measures the final evaluated candidate projection, not the Source target that generated it.

Core rule:

`Source target compliance ≠ Evaluated geometry projection ≠ Rendered visual fidelity`

## Required projections
For reference reproduction of an existing vehicle/product, evaluate at minimum:
- SIDE orthographic;
- FRONT orthographic;
- REAR orthographic;
- PLAN or a plan-constraining view;
- at least one identity-bearing 3/4 view for independent visual review.

## Independent provenance
Every metric requires:
- `reference_target_source`: external/calibrated reference evidence;
- `candidate_measurement_source`: final evaluated geometry or rendered candidate projection.

The candidate source may not be the same JSON/control family that owns the reference target.

## Minimum metric families
### SIDE
- overall length / axle relation;
- upper silhouette;
- lower body / wheel-arch silhouette;
- A-pillar base;
- C-pillar / quarter-window rear extent;
- roof apex location;
- rocker and bumper termination heights.

### FRONT
- body width;
- roof/cabin width ratio;
- windshield lower width ratio;
- lamp centre/diameter relation;
- fender crown vs hood centre height;
- lower intake band proportion.

### REAR
- body width;
- roof/backlight width ratio;
- rear shoulder pinch / haunch relation;
- lightbar height and width relation;
- lower bumper/diffuser mass.

## Failure logic
- If Source contour error is low but evaluated projection is wrong: `FAIL_SOURCE_TO_PROJECTION_FIDELITY`.
- If SIDE passes while FRONT/REAR fails: `HOLD_CROSS_SECTION_MODEL_INSUFFICIENT`.
- If geometry passes orthographic projections but 3/4 volume still fails: `REVISE_VOLUMETRIC_TRANSITION`.
- If only lighting/material causes the mismatch: route to Render/CMF, not geometry.

## Forbidden
- deriving candidate metrics from the same reference target values;
- per-camera geometry changes;
- accepting one orthographic view as full reference fidelity;
- using detail density, badges, graphics or CMF to compensate for macro projection errors;
- treating pixel similarity alone as Class-A or engineering proof.

## Gate states
- `PROJECTION_MACHINE_SCREENING_PASS`
- `PROJECTION_MACHINE_SCREENING_FAIL`
- `REFERENCE_FIDELITY_REVIEW_KEEP / REVISE / REJECT`

Machine projection PASS remains a screening state. Final KEEP requires actual multi-view reference review.
