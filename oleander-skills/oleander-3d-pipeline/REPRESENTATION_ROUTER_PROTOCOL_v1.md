# Representation Router Protocol v1

Status: CURRENT CANDIDATE.

Purpose: choose the correct Source representation before geometry production. The router prevents a domain-specific modeling habit from becoming the default for unrelated products.

## INPUT
- task intent: reproduce / originate / modify / diagnose / visualize;
- reference availability and authority;
- known dimensions, interfaces and component/package constraints;
- material/manufacturing intent when known;
- required downstream use: concept, visual prototype, engineering handoff, animation, spatial proof, technical drawing;
- available authoring applications.

## MUST CHECK
1. Is a specific existing object/version the visual authority?
2. Are dimensional/manufacturing constraints dominant over freeform appearance?
3. Is the primary identity a continuous reflective shell?
4. Is the dominant geometry rotational or sweep-based?
5. Is form governed by a skeleton, mechanism, ergonomic chain or assembly graph?
6. Is form governed by soft-material behavior?
7. Is terrain/site/geospatial authority dominant?
8. Does the object require more than one representation family?

## ROUTE DECISION
### Reference intent
- specific existing target → `REFERENCE_RECONSTRUCTION`.
- no governing visual target / original design → `STRUCTURE_TO_FORM`.
- mixed task → declare one primary route and explicit secondary evidence route.

### Representation family
- dimension/manufacturing dominant rigid product → `PARAMETRIC_SOLID_CAD`;
- continuous reflective shell / industrial design surface → `FEATURE_CURVE_STRUCTURED_SUBD` or CAD/NURBS equivalent;
- axial/rotational dominant → `PROFILE_REVOLVE`;
- mechanism/wearable/frame/assembly driven → `SKELETON_SECTION_ASSEMBLY`;
- textile/foam/rubber/soft-body driven → `SOFT_MATERIAL_SIM_SCULPT_RETOPO`;
- site/terrain/network dominant → `TERRAIN_GIS_SPATIAL`;
- mixed causal owners → `HYBRID` with one Source owner per family.

Application choice follows representation. `Blender`, `Rhino`, `Alias`, `Fusion`, `SolidWorks`, `FreeCAD`, `Houdini`, etc. are toolchain choices, not route names.

## REQUIRED OUTPUT
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

## ALLOWED
- hybrid representation when causal ownership is explicit;
- changing route before Source promotion if new evidence proves the initial representation unsuitable;
- placeholder package volumes when exact components are not yet selected, provided they are marked assumptions/ranges.

## FORBIDDEN
- defaulting to a cube/SubD/Boolean workflow because Blender is available;
- using one automotive/product surface grammar for all 3D tasks;
- promoting sculpt/remesh output to manufacturing Source without an explicit translation gate;
- selecting a representation only because it produces attractive renders quickly;
- hiding missing package/interface knowledge behind exterior styling.

## FAIL / HOLD
- `HOLD_MODELING_ROUTE_UNRESOLVED`
- `FAIL_REPRESENTATION_CONTRADICTS_TASK`
- `FAIL_SOURCE_OWNER_AMBIGUOUS`
- `REOPEN_REPRESENTATION_MODEL`

## Escalation
If repeated controlled edits cannot correct the same defect without cross-view/interface regressions, route to `STOP_PARAMETER_TUNING_REOPEN_REPRESENTATION`, then re-evaluate this protocol before continuing.
