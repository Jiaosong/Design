# Representation Router Protocol v1

Status: CANDIDATE SPECIALIST EXTENSION.

Architecture binding: this protocol is a **K3 Execution Router modeling specialization** under OLEANDER Project Control Plane v0.3. It does not create a new Current Authority, Project Flow, Workstream, Validation object, system Gate, breaker, QA layer or promotion state.

Purpose: choose the correct Source representation before geometry production. The router prevents a domain-specific modeling habit from becoming the default for unrelated products.

## INPUT
- Project Control Card / task context when the work belongs to project execution;
- task intent: reproduce / originate / modify / diagnose / visualize;
- reference availability and authority resolved by K2;
- known dimensions, interfaces and component/package constraints;
- material/manufacturing intent when known;
- required downstream use: concept, visual prototype, engineering handoff, animation, spatial proof, technical drawing;
- available authoring capabilities/applications.

## MUST CHECK
1. Is a specific existing object/version the visual authority?
2. Are dimensional/manufacturing constraints dominant over freeform appearance?
3. Is the primary identity a continuous reflective shell?
4. Is the dominant geometry rotational or sweep-based?
5. Is form governed by a skeleton, mechanism, ergonomic chain or assembly graph?
6. Is form governed by soft-material behavior?
7. Is terrain/site/geospatial authority dominant?
8. Does the object require more than one representation family?
9. Does the route preserve the Control Plane's current Decision Question, Locked Variables and Authority boundary?

## ROUTE DECISION
### Specialist modeling route
- specific existing target → `REFERENCE_RECONSTRUCTION`;
- no governing visual target / original design → `STRUCTURE_TO_FORM`;
- mixed task → declare one primary modeling route and explicit secondary evidence route.

These are K3 specialist route names, not project modes. Project mode remains `EXPLORE / CANDIDATE / AUTHORITY` as resolved by the Control Plane.

### Representation family
- dimension/manufacturing dominant rigid product → `PARAMETRIC_SOLID_CAD`;
- continuous reflective shell / industrial design surface → `FEATURE_CURVE_STRUCTURED_SUBD` or CAD/NURBS equivalent;
- axial/rotational dominant → `PROFILE_REVOLVE`;
- mechanism/wearable/frame/assembly driven → `SKELETON_SECTION_ASSEMBLY`;
- textile/foam/rubber/soft-body driven → `SOFT_MATERIAL_SIM_SCULPT_RETOPO`;
- site/terrain/network dominant → `TERRAIN_GIS_SPATIAL`;
- mixed causal owners → `HYBRID` with one Source owner per family.

Application choice follows representation. `Blender`, `Rhino`, `Alias`, `Fusion`, `SolidWorks`, `FreeCAD`, `Houdini`, etc. are capabilities, not route names.

## REQUIRED SPECIALIST OUTPUT
`MODELING_ROUTE_RECEIPT.json` with:
- `schema`;
- `task_id`;
- `modeling_intent`;
- `route`;
- `representation_family`;
- `source_authority_owner`;
- `hard_constraints[]`;
- `functional_constraints[]`;
- `design_decisions[]`;
- `assumptions[]`;
- `required_stage_graph[]`;
- `required_diagnostics[]`;
- `does_not_prove[]`.

This receipt supplements rather than replaces the existing Project Control Card and Authority receipts.

## ALLOWED
- hybrid representation when causal ownership is explicit;
- changing the specialist route before Source promotion if new evidence proves the initial representation unsuitable;
- placeholder package volumes when exact components are not yet selected, provided they are marked assumptions/ranges.

## FORBIDDEN
- defaulting to a cube/SubD/Boolean workflow because Blender is available;
- using one automotive/product surface grammar for all 3D tasks;
- promoting sculpt/remesh output to manufacturing Source without the existing required translation/review evidence;
- selecting a representation only because it produces attractive renders quickly;
- hiding missing package/interface knowledge behind exterior styling;
- using this router to change P0–P4 identity, Design State, Authority State or existing Gate semantics.

## FAIL / HOLD
Specialist results route back through the existing K4 Review Router:
- `HOLD_MODELING_ROUTE_UNRESOLVED`
- `FAIL_REPRESENTATION_CONTRADICTS_TASK`
- `FAIL_SOURCE_OWNER_AMBIGUOUS`
- `REOPEN_REPRESENTATION_MODEL`

## Escalation through existing CB-01
Do not introduce a separate escalation Gate. If the same Decision Question receives 2 consecutive Visual/Project REVISE results, Control Plane CB-01 requires Root Cause Reclassification. Only when that reclassification identifies the representation layer as causal should K3 emit `REOPEN_REPRESENTATION_MODEL` and re-run this router.
