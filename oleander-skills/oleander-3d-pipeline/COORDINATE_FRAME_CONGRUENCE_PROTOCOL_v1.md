# OLEANDER 3D Coordinate Frame Congruence Protocol v1

Status: CANDIDATE / reusable 3D Skill training delta

Benchmark provenance: Porsche 911 992.2 V72 / V75 / V76.
- A reopened V72 parent scene passed its native-artifact and geometry-signature witness.
- A world-space residual audit found exactly 2 EDGE_2 straddling faces.
- The first BMesh diagnostic reused the same canonical boundary against object-local mesh coordinates and selected 0 faces across every tolerance trial.
- Therefore the apparent operator stagnation was not yet an operator/tolerance result; it was a coordinate-frame mismatch between evidence predicate and edit operator.

## Core separation

`SAME_GEOMETRY ≠ SAME_COORDINATE_FRAME`

`PREDICATE_PASS_IN_FRAME_A ≠ OPERATOR_TARGET_IN_FRAME_B`

`CANONICAL_TARGET + UNDECLARED_FRAME_TRANSFORM → INVALID_EDIT_EVIDENCE`

`FRAME_MISMATCH → NO_TOLERANCE / SOLVER / DESIGN CONCLUSION`

Use this protocol when evidence, geometry selection, edit operators, projections, diagnostics or cross-application exchange operate in different coordinate spaces.

## 1. Declare all frames

Record the applicable frames explicitly:
- Source/local object frame;
- parent/assembly frame;
- world/scene frame;
- camera/view/projection frame;
- CAD/GIS/import frame;
- operator evaluation frame;
- reference/measurement frame.

Do not use labels like “same coordinates” without binding the actual transform identity.

## 2. Bind canonical target frame

Every spatial target must declare the frame in which its coordinates are authoritative for the current operation.

Examples:
- aperture boundary in world metres;
- Source section rails in object-local metres;
- site geometry in CRS/project coordinates;
- 2D reference landmarks in calibrated image coordinates;
- camera crop targets in normalized image space.

A target may be transformed for execution, but the canonical frame remains recorded.

## 3. Predicate and operator frames must be congruent

If an evidence predicate and an edit/operator selection are intended to identify the same geometry:
- either run both in the same frame;
- or transform both through an explicit, verified relation to one canonical frame.

At minimum record:
- transform source frame;
- transform target frame;
- transform matrix / deterministic transform identity;
- point/vector/normal semantics;
- scale/axis/origin implications;
- transform verification result.

### HARD RULE

`AUDIT_TARGET_COUNT` and `OPERATOR_SELECTED_COUNT` are not comparable until their frames are congruent.

A mismatch such as `world audit = 2` and `local operator selection = 0` blocks all downstream tolerance/solver conclusions.

## 4. Points, directions, normals and planes are different transform semantics

Do not transform every geometric quantity as a point.

- points include translation;
- directions do not include translation;
- normals/planes require the appropriate inverse-transpose / dual-space handling under non-uniform transforms;
- distances/tolerances may change under scale and must be expressed in the operator frame or normalized back to the canonical frame.

If the transform is non-rigid or non-uniform and the operator depends on metric distance, record the tolerance conversion explicitly.

## 5. Diagnostic-copy normalization is allowed

For a diagnostic-only copy, one valid route is:
1. duplicate the Derived carrier;
2. bake `matrix_world` into the copy’s geometry;
3. reset the copy transform to identity;
4. run both predicate and operator in the resulting world-equivalent local frame;
5. verify world bounds/signature before and after the diagnostic copy operation;
6. discard the copy.

This does not transfer Source Authority to the copy.

## 6. Cross-application and projection cases

The same rule applies to:
- Blender ↔ CAD/DCC exchange;
- object-local ↔ world selection;
- GIS CRS ↔ local project coordinates;
- camera/world ↔ image projection;
- normalized reference image ↔ metric vehicle/site coordinates;
- Geometry Nodes local positions ↔ scene-space diagnostics.

`UNIT_MATCH ≠ FRAME_MATCH` and `AXIS_LABEL_MATCH ≠ TRANSFORM_IDENTITY`.

## 7. Required receipt

Use `oleander.3d.coordinate-frame-congruence-receipt.v1` with:
- `operation_id`
- `geometry_id`
- `geometry_state_class`
- `canonical_target_frame`
- `predicate_frame`
- `operator_frame`
- `transforms`
- `metric_or_tolerance_frame`
- `audit_target_count`
- `operator_selected_count`
- `selection_equivalence_required`
- `frame_checks`
- `frame_result`
- `downstream_evidence_state`
- `does_not_prove`

## 8. Result states

Use:
- `PASS_FRAME_CONGRUENCE`
- `FAIL_FRAME_MISMATCH`
- `HOLD_TRANSFORM_UNVERIFIED`
- `PASS_DIAGNOSTIC_COPY_NORMALIZED_FRAME`

## 9. Failure routing

On frame mismatch:
1. do not tune tolerance/solver;
2. do not widen the selection predicate;
3. bind/verify the transform;
4. rerun the same target count in the operator frame or a shared canonical frame;
5. only then interpret operator behavior.

`FRAME FAILURE → TRANSFORM REPAIR`, not `PARAMETER TUNING`.

## 10. Promotion boundary

Coordinate Frame Congruence PASS proves only that the compared predicate/operator/measurement are spatially comparable under the declared transform. It does not prove geometry quality, correct semantic ownership, aperture closure, reference fidelity, engineering/manufacturing truth, physical CMF, Design KEEP or MAIN KEEP.
