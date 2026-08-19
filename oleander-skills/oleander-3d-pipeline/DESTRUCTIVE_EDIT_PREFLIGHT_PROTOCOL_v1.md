# OLEANDER 3D Destructive Edit Preflight Protocol v1

Status: CANDIDATE / reusable 3D Skill training delta

Benchmark provenance: Porsche 911 992.2 V60–V66.
- V60 proved an operator can report success while destroying the host.
- V63 added a pre-delete mask/retention witness and correctly blocked deletion when one required owner had zero first-match hits.
- V65 proved the apparently missing rear-glass target actually overlapped the host; the zero result came from classifier ownership/order, not missing geometry.

## Core separation

`PREDICATE_MATCH ≠ EXCLUSIVE_OWNER ≠ SAFE_TO_EDIT ≠ EDIT_SUCCEEDED ≠ HOST_PRESERVED ≠ DESIGN_PASS`

`FIRST_MATCH_CODE_ORDER ≠ SEMANTIC_OWNERSHIP`

Use this protocol before a destructive or topology-changing Derived operation when the target region can be predicted/classified before mutation.

## 1. Bind semantic edit scope before target classification

Record:
- host identity and state class;
- operation;
- semantic edit scope;
- Source mutation permission;
- required target/owner IDs;
- protected regions/interfaces;
- target evidence/source;
- classifier method and version;
- expected locality;
- predicted preservation checks and thresholds.

Do not let a historical object name, nested script namespace, list index, or branch order silently define a semantic owner.

## 2. Classifier dependency must be explicit

A classifier may depend on:
- bound Source/Reference tables;
- named semantic curves/sections;
- explicit spatial ranges;
- verified topology groups;
- material/attribute IDs where they are authoritative for the declared task;
- normal/orientation or adjacency evidence when appropriate.

### FORBIDDEN
- hidden dependency on historical namespace depth such as `ctx['ns']['...']` when the semantic input can be bound directly;
- first-match `if/elif/return` order used as the only reason one owner wins over another;
- widening a mask until it produces a non-zero hit without reference/evidence justification;
- using a render mask to substitute for geometry ownership.

## 3. Required owner coverage

Before editing, every required semantic target must have a declared coverage result.

Allowed states:
- `COVERED_EXCLUSIVE`
- `COVERED_SHARED_BOUNDARY_EXPLICIT`
- `MISSING_TARGET_COVERAGE`
- `AMBIGUOUS_MULTI_OWNER`
- `UNRESOLVED`

A required owner with zero coverage blocks destructive execution unless the task explicitly declares that owner not applicable.

Coverage method must match mesh scale. For coarse/evaluated carriers, centroid-only membership may be insufficient; use vertex/edge/polygon overlap, topology groups, spatial intersection, or another justified method.

## 4. Multi-owner conflict audit

Evaluate all relevant owner predicates independently before assigning ownership.

For each candidate primitive/face/region record the owner match set.

If a primitive matches multiple owners:
- do **not** choose the first predicate that ran;
- classify `AMBIGUOUS_MULTI_OWNER` unless an explicit shared-boundary or disambiguation rule exists;
- persist the conflict count and samples;
- block destructive execution when ambiguity affects a required edit region.

A valid disambiguation rule must be semantic and reviewable, for example:
- canonical boundary ownership;
- topology partition;
- surface orientation/normal family with justified threshold;
- adjacency to an authoritative opening boundary;
- explicit host/interface/infill layer ownership.

Code order, object creation order, vertex index order, or timestamp are not valid ownership evidence.

## 5. Predicted host preservation

Before mutation estimate the applicable effects where feasible:
- candidate faces/triangles/volume to remove or replace;
- predicted global face/area/volume retention;
- predicted bounds change;
- protected feature/interface intersection;
- expected component count change;
- Source mutation state.

This is a **preflight estimate**, not a substitute for the post-edit `Derived Edit Host Preservation` receipt.

A preflight may allow execution only when every hard predicted invariant is within the declared budget.

## 6. Preflight decisions

Use:
- `PASS_DESTRUCTIVE_EDIT_ALLOWED`
- `FAIL_DESTRUCTIVE_EDIT_BLOCKED_MISSING_TARGET`
- `FAIL_DESTRUCTIVE_EDIT_BLOCKED_AMBIGUOUS_OWNER`
- `FAIL_DESTRUCTIVE_EDIT_BLOCKED_PREDICTED_HOST_LOSS`
- `HOLD_CLASSIFIER_EVIDENCE_UNRESOLVED`

A blocked preflight is a successful fail-closed behavior when the classifier/evidence is valid. Do not relabel it as infrastructure failure.

## 7. Post-edit linkage

When preflight allows execution:
1. execute the exact declared operation;
2. emit `Derived Edit Host Preservation` evidence;
3. compare predicted vs actual deltas;
4. if actual damage exceeds budget, post-edit FAIL overrides preflight PASS;
5. then run interface/reference/design review separately.

`PREFLIGHT PASS` proves only that the edit was safe enough to attempt under the declared classifier and predicted budget.

## 8. Repeated mismatch routing

If a target repeatedly produces missing/ambiguous coverage:
- audit evidence-carrier scope;
- audit classifier coverage scale;
- audit host/target relation ownership;
- audit representation architecture;
- do not keep expanding tolerances without evidence.

`MASK FAILURE → COVERAGE / OWNERSHIP / REPRESENTATION DIAGNOSIS`, not `ARBITRARY MASK GROWTH`.

## 9. Required receipt

Use `oleander.3d.destructive-edit-preflight-receipt.v1` with:
- `host_id`
- `host_state_class`
- `operation`
- `edit_scope`
- `source_mutation_allowed`
- `classifier_identity`
- `classifier_dependencies`
- `required_owner_ids`
- `owner_coverage`
- `multi_owner_conflicts`
- `predicted_preservation_checks`
- `preflight_result`
- `destructive_edit_allowed`
- `does_not_prove`

## 10. Promotion boundary

Destructive Edit Preflight does not prove:
- the edit will succeed;
- host preservation after execution;
- aperture/interface closure;
- reference fidelity;
- surface fairness/Class-A;
- engineering/manufacturing validity;
- physical CMF;
- Design KEEP / MAIN KEEP.
