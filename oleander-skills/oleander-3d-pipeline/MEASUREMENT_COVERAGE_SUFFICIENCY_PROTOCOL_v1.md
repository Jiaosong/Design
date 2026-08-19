# OLEANDER 3D Measurement Coverage Sufficiency Protocol v1

Status: CANDIDATE / reusable evidence-gate training delta

Provenance: Porsche 911 992.2 V59. The candidate obtained a SIDE upper-envelope RMSE of about 0.0139 m against the calibrated reference curve, yet the actual side preview still read as a generic/toy sports car and FRONT/REAR body-only profile errors remained outside their screening limits. Carrier congruence and one accurate projection curve were therefore insufficient for a whole-form claim.

## Core separation

`CARRIER_CONGRUENT ≠ MEASUREMENT_COVERAGE_SUFFICIENT ≠ CLAIM_PROVEN ≠ DESIGN_PASS`

Use this gate after Evidence Carrier Congruence. Carrier congruence asks whether the right object/scope is being measured. Coverage sufficiency asks whether the measurement set spans the dimensions, feature families and held-out views necessary for the declared claim.

## 1. Declare the claim extent

For each evidence claim record:
- `claim_id`;
- claim scope/carrier;
- required dimensions or domains, e.g. X/Z silhouette, Y/Z width distribution, plan taper, section hierarchy, local interface, time/state, assembly clearance;
- required identity-critical feature families;
- required fit views and held-out views;
- whether the claim is screening, diagnostic, comparative, or promotion-capable.

A whole-form or whole-visible claim normally cannot be supported by one scalar, one section, one projection axis, one crop, or one fitted view unless the claim is explicitly narrowed to that evidence.

## 2. Record what was actually measured

Persist:
- measured dimensions/domains;
- measured feature families;
- measured views/cameras;
- sampling density or station set where relevant;
- normalization frame;
- unmeasured critical dimensions/features/views;
- known blind spots.

Examples:
- `SIDE_TOP_ENVELOPE_XZ` measures the upper silhouette in one projection; it does not measure body thickness, greenhouse opening proportion, wheel-to-body stance, front/rear width-by-height distribution, lamp-host integration or plan taper.
- a Zebra pass measures reflection continuity under a controlled rig; it does not measure silhouette proportion or physical curvature tolerance unless the claim and method explicitly include them.
- one section through a landscape node does not prove sequence, return route, visibility or crowd capacity.

## 3. Coverage relation

Use:
- `SUFFICIENT_FOR_DECLARED_SCREEN`;
- `SUFFICIENT_FOR_DECLARED_CLAIM`;
- `PARTIAL_DIAGNOSTIC_ONLY`;
- `INSUFFICIENT_CRITICAL_DIMENSION_MISSING`;
- `INSUFFICIENT_CRITICAL_FEATURE_MISSING`;
- `INSUFFICIENT_HELD_OUT_VIEW_MISSING`;
- `UNRESOLVED`.

A narrow metric may PASS numerically while the coverage relation remains PARTIAL/INSUFFICIENT.

## 4. Hard failures

Fail closed when:
- a whole-visible or reference-fidelity claim is promoted from one fitted silhouette/profile only;
- all measured views are fit views and no required held-out view is reviewed;
- a claim about a named feature family is made while that family is not measured directly or by a validated equivalent;
- one projection axis is used to infer an unmeasured orthogonal distribution;
- an aggregate score hides a failed critical dimension/feature/view;
- sparse stations miss the visible defect that the claim says is absent;
- a metric is accurate only because it measures the same curve/target used to generate the candidate and no independent dimension/view remains.

## 5. Gate-local results remain visible

Do not average away contradictory evidence.

Example:
- SIDE upper envelope: PASS;
- FRONT width-by-height: REJECT;
- REAR width-by-height: REJECT;
- hood/fender local hierarchy: SCREENED;
- held-out 3/4 visual identity: REJECT/HOLD.

The correct global conclusion is not a numerical average. It is the strongest claim supported by the complete required coverage set.

## 6. Held-out evidence

For reference reconstruction and controlled design validation, explicitly separate:
- `FIT_EVIDENCE` used to derive/tune the candidate;
- `REGRESSION_LOCKS` protecting previously established dimensions;
- `HELD_OUT_EVIDENCE` not used as the direct fitting target.

Held-out failure blocks promotion even when fitted metrics pass.

## 7. Required receipt

Use `oleander.3d.measurement-coverage-receipt.v1` with:
- `claim_id`;
- `claim_scope`;
- `required_dimensions`;
- `measured_dimensions`;
- `required_feature_families`;
- `measured_feature_families`;
- `fit_views`;
- `held_out_views_required`;
- `held_out_views_reviewed`;
- `unmeasured_critical_items`;
- `coverage_relation`;
- `metric_results`;
- `result`;
- `does_not_prove`.

## 8. Promotion boundary

Measurement Coverage PASS proves only that the declared evidence set covers the declared claim extent. It does not prove the measurements are correct, the reference is authoritative, the geometry is good, reference fidelity, Class-A continuity, field truth, engineering/manufacturing validity, Design KEEP or MAIN KEEP.
