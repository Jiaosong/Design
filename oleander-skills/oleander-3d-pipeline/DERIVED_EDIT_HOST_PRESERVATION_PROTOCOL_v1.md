# OLEANDER 3D Derived Edit Host Preservation Protocol v1

Status: CANDIDATE / reusable 3D Skill training delta

Provenance: Porsche 911 V60 aperture experiment. A rear-glass Boolean returned success and changed geometry, yet reduced the rendered host from 8,637 faces to 96 faces. The command executed; the intended local edit failed catastrophically.

## Core separation

`OPERATOR_APPLIED ≠ GEOMETRY_CHANGED ≠ LOCAL_EDIT_SUCCEEDED ≠ HOST_PRESERVED ≠ DESIGN_PASS`

Use this gate for destructive or topology-changing Derived operations including Boolean difference/intersection, trim, remesh, decimate, voxelization, destructive Geometry Nodes realization, topology cleanup, projection/cut, retopology replacement, or scripted mesh surgery.

## 1. Declare edit locality before execution

Every destructive edit must declare:
- host identity and state class;
- operation type;
- semantic edit scope;
- expected affected region or component;
- protected regions/components/interfaces;
- whether Source mutation is allowed;
- preservation metrics and task-specific thresholds.

A `LOCAL` edit cannot be validated only by checking that some geometry changed.

## 2. Before/after host witness

Capture before and after at the same evaluated state where applicable:
- vertices / edges / faces / triangles;
- object count or connected-component count when meaningful;
- world-space bounds and dimensions;
- protected landmark positions or named interfaces;
- Source digest when Source must remain unchanged.

Additional domain metrics may be required: area, volume, silhouette, section area, UV/material IDs, hierarchy, collision, assembly interfaces, or geospatial footprint.

## 3. Preservation budget is task-specific

Do not hard-code one universal face-retention ratio. Instead declare a preservation budget appropriate to the edit.

Examples:
- local aperture cut: global body bounds should remain nearly unchanged and the host should retain the overwhelming majority of its primary shell;
- decimation: face count is expected to fall, so silhouette, bounds, normals and protected feature error own the gate instead;
- Boolean union: face count may rise materially, so connectedness, bounds and protected interface continuity matter more;
- trim/crop intentionally deleting half an object must declare that region as the target rather than pretending to be local.

Thresholds must state units or ratios and why they are appropriate to the claim.

## 4. Fail closed on catastrophic deltas

A destructive Derived edit is `FAIL_HOST_PRESERVATION` when any protected invariant exceeds its declared budget, even when:
- Blender returns exit code 0;
- the modifier/operator reports success;
- the object still exists;
- geometry changed;
- a receipt was written;
- a render was produced.

For local edits, catastrophic collapse, global bounds loss, protected-region deletion, uncontrolled component explosion, or unrelated interface movement are hard failures.

## 5. Source boundary

A Derived host preservation PASS does not allow Source mutation by implication.

When Source is protected:
- capture Source identity/digest before and after;
- destructive operations occur on Derived/working copies only;
- any Source delta requires a separate authorized Source edit receipt.

`HOST_PRESERVED` therefore does not prove `SOURCE_UNCHANGED` unless the Source witness also passes.

## 6. Negative experiments are retained

A validly executed destructive experiment that fails host preservation remains useful failure evidence. Record:
- exact operator/runtime;
- before/after metrics;
- first failed invariant;
- artifact preview when available;
- root cause hypothesis;
- rollback/LKG.

Do not rewrite `FAIL_HOST_PRESERVATION` as runtime failure unless execution itself failed.

## 7. Repeated destructive failure escalates to representation repair

Do not keep tuning the same destructive operator after evidence shows the representation is the likely owner of the failure.

Escalate from `OPERATOR_PARAMETER` to `REPRESENTATION_ARCHITECTURE` when one or more are true:
- the same semantic local edit repeatedly violates the global host-preservation budget;
- changing solver/tolerance/normals only moves or hides the failure without stabilizing the host;
- the intended opening/interface is identity-bearing and should own a persistent shared boundary;
- the destructive operation is being applied after evaluation even though the aperture/interface is a first-class construction relation;
- preserving the host requires masks, opaque infill, render tricks, or unrelated geometry edits.

Preferred escalation order:
1. keep the last known good Source/Derived host frozen;
2. stop operator-parameter search;
3. reclassify the failure as `REPRESENTATION / TOPOLOGY / ARCHITECTURE` rather than `PARAMETER`;
4. move the boundary upstream into generated construction or a shared-boundary patch network when semantically appropriate;
5. if an evaluated Derived carrier must be edited, use an operation whose locality can be explicitly classified and measured;
6. rerun host preservation, interface closure, visual-reference and Design gates independently.

For a major aperture, `POST_EVALUATED_BOOLEAN` is not privileged merely because it is convenient. A generated opening, topology-owned boundary, trim-aware patch network, CAD feature, or other domain-appropriate representation may be the correct route.

`REPEATED_OPERATOR_FAILURE → REPRESENTATION_RECLASSIFICATION`, not `MORE_UNBOUNDED_TUNING`.

This escalation rule does not mean Boolean/remesh/trim are forbidden. It means their continued use must remain causally justified by preserved evidence.

## 8. Required receipt

Use `oleander.3d.derived-edit-host-preservation-receipt.v1` with:
- `host_id`
- `host_state_class`
- `operation`
- `edit_scope`
- `locality`
- `source_mutation_allowed`
- `source_unchanged_or_na`
- `before`
- `after`
- `preservation_checks`
- `operator_execution`
- `host_preservation_result`
- `evidence_result`
- `design_result`
- `does_not_prove`

## 9. Promotion boundary

Host preservation can prove only that the declared destructive operation stayed within its preservation contract. It does not prove:
- reference fidelity;
- surface fairness/Class-A;
- construction/manufacturing validity;
- physical CMF;
- Design KEEP / MAIN KEEP.
