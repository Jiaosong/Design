# OLEANDER Blender Runtime — Professional Parity Gate

Status: ACTIVE CANDIDATE GATE
Applies to: `feat/oleander-blender-runtime-workbench` / PR #470
Default-promotion state: **BLOCKED** until the required parity gates below pass with real runtime evidence.

## Principle

OLEANDER Blender Runtime must not become the default OLEANDER modeling environment merely because the Blender extension installs, CI is green, or internal governance features are mature.

Default promotion requires **workflow-level professional capability** across the originally targeted software classes. A similarly named button is not parity. Each gate must demonstrate editable native intent, deterministic execution, reopen/readback, failure handling, dimensional/authority correctness, and where applicable round-trip exchange with a capable specialist kernel.

`professional parity != reimplement every solver inside Blender`

Blender may remain the single interaction shell while specialist open-source or external kernels provide authoritative B-Rep, sketch solving, IFC, CAE, CAM, GIS, or surface operations. The user should not need to manually reconstruct state when crossing those kernels.

## Promotion rule

`OLEANDER Blender Runtime -> DEFAULT` is forbidden until all Tier-P0 gates are PASS and no blocking Tier-P1 gate required by the active project class remains OPEN.

A PASS requires:

1. real Blender runtime execution;
2. deterministic positive and negative tests;
3. native/editable source preservation;
4. unit / axis / coordinate readback;
5. stable OLE identity and dependency lineage;
6. save/reopen or round-trip readback;
7. stale propagation after upstream changes;
8. explicit authority separation;
9. no unsupported solver / engineering / manufacturing / field claims;
10. current dependency version + license + recovery/fallback record.

## Reuse-first dependency policy

Before implementing a specialist capability from zero, evaluate mature existing projects. Adoption state must be one of:

- `DISCOVERED_NOT_PROBED`
- `RUNTIME_PROBED`
- `ADAPTER_IMPLEMENTED_UNVERIFIED`
- `VALIDATED_FOR_BOUNDED_SCOPE`
- `REJECTED_WITH_REASON`

Third-party code is never silently copied into OLEANDER. Prefer adapter/sidecar integration, preserve upstream attribution/license, and keep plugin disappearance as an explicit dependency failure.

### Current reuse candidates

| Capability | Candidate | Intended role | Current OLEANDER state |
|---|---|---|---|
| Constraint sketching | CAD Sketcher + SolveSpace | dimensional/geometric sketch solver | DISCOVERED_NOT_PROBED |
| Parametric/B-Rep/NURBS graph | Sverchok + FreeCAD `Part.Shape` / FreeCAD sidecar | B-Rep/NURBS operations and parametric graph | DISCOVERED_NOT_PROBED |
| BIM / IFC | Bonsai + IfcOpenShell | IFC-native authoring, semantics, quantities, drawings | DISCOVERED_NOT_PROBED |
| CAM | Fabex | CNC toolpath generation and postprocessing | DISCOVERED_NOT_PROBED |
| GIS | BlenderGIS | georeferenced data / terrain bridge | DISCOVERED_NOT_PROBED |
| Technical dimensions/drawing | MeasureIt_ARCH and/or Bonsai drawing stack | dimensions, annotations, linework, sheets | DISCOVERED_NOT_PROBED |
| Native procedural | Blender Geometry Nodes | governed procedural modeling | PARTIALLY_VALIDATED |
| Advanced procedural graph | Sverchok | dataflow / geometry / surface graph extension | DISCOVERED_NOT_PROBED |

A candidate is not a capability until OLEANDER runtime probing proves it works in the supported Blender version and passes the relevant gate below.

---

# Tier P0 — required before default promotion

## P0-A — Parametric CAD / SolidWorks / Fusion / Inventor class

Required professional behaviors:

- 2D sketch entities with dimensional constraints;
- horizontal / vertical / coincident / parallel / perpendicular / tangent / equal / concentric constraints;
- under / fully / over-constrained state reporting;
- stable datum planes / axes / points;
- feature parameters bound to sketch or datum intent;
- extrusion / revolve / sweep / loft on authoritative solid/surface kernel;
- shell / draft / fillet / chamfer;
- hole/interface features with dimensional readback;
- pattern / mirror;
- parameter edit -> deterministic feature rebuild;
- feature failure state without silent geometry corruption;
- assembly components with local reference frames;
- mate / joint relationships for at least coincident, concentric, distance and angle classes;
- named configurations / variants;
- STEP import/export;
- source -> STEP -> reopen dimensional and topology sanity readback.

Professional gate tests:

1. constrained bracket or housing from sketch through solid features;
2. parameter change rebuilds dependent features without manual mesh editing;
3. intentionally impossible feature produces controlled FAIL/HOLD;
4. two-part fit-critical assembly preserves interfaces through reopen;
5. STEP round-trip preserves units and bounded dimensional deviation.

**Current state: NOT PASSED.** Existing Blender Modifier feature stack and Design Intent metadata are insufficient for this gate.

## P0-B — Plasticity-class direct B-Rep solid modeling

Required:

- authoritative B-Rep body;
- face push/pull and offset;
- direct face translate/rotate with topology update;
- robust boolean union/subtract/intersect;
- split body / trim;
- shell;
- variable/constant fillet and chamfer at bounded scope;
- pattern / mirror;
- body healing/check;
- B-Rep -> Blender display derivative while preserving native master;
- deterministic measurement from B-Rep source.

Mesh booleans do not satisfy this gate.

**Current state: NOT PASSED.**

## P0-C — Rhino / Alias class curve, NURBS and surface diagnostics

Required:

- degree / control point / knot inspection;
- curve rebuild;
- interpolate/control-point curves;
- loft / sweep1 / sweep2 or bounded equivalent;
- network / patch or governed equivalent;
- trim / split / join;
- blend / match surface;
- explicit G0 / G1 / G2 continuity checks; G3 when supported by selected kernel;
- zebra/reflection-line diagnostic;
- curvature comb;
- Gaussian/mean curvature or equivalent surface diagnostic;
- minimum radius / deviation map;
- draft/thickness diagnostic separated from mold/engineering approval;
- source NURBS/B-Rep master preserved, not converted silently to mesh.

Professional gate artifact: one consumer-product shell with controlled highlight flow, continuity report, zebra, curvature evidence and reopenable authoritative surface source.

**Current state: NOT PASSED.** Current triangulated mesh dihedral/thickness diagnostics do not equal Class-A/NURBS authority.

## P0-D — Houdini-class procedural authoring foundation

Required at bounded professional scope:

- published parameters;
- stable node/group identity;
- geometry/attribute spreadsheet or equivalent inspector;
- named attribute inventory;
- dependency graph;
- deterministic cache/bake state;
- node/group versioning;
- procedural diff;
- debug visualization;
- performance timing/profile;
- LOD/proxy generation;
- broken dependency and missing node-group failure states;
- save/reopen and deterministic re-evaluation.

Geometry Nodes alone is not enough unless these production controls exist.

**Current state: PARTIAL.** Geometry Nodes creation/binding/persistence is validated; professional procedural debugging/profile/cache controls are incomplete.

## P0-E — Revit / BIM / IFC class

Required bounded professional workflow:

- IFC is native authority, not Blender tags only;
- IFC project/site/building/storey spatial hierarchy;
- class/type/predefined-type assignment;
- property sets and quantities;
- object <-> IFC stable identity;
- openings/void relationships;
- type-like reusable parameter sets;
- basic system/containment/aggregation relationships;
- IFC import/edit/export/reopen;
- changed IFC entity readback;
- geometry/semantic round-trip audit;
- quantity extraction bound to current IFC model;
- drawing/view linkage where supported.

**Current state: NOT PASSED.** Bonsai/IfcOpenShell is the primary reuse candidate.

## P0-F — Professional technical drawing

Required:

- stable plan / elevation / section / axon / exploded view IDs;
- orthographic projection from current governed geometry;
- hidden/visible line classes;
- section cut representation;
- line-weight/style classes;
- associative or explicitly regeneration-bound dimensions;
- editable text/annotations;
- detail/callout references;
- title block / sheet / revision identity;
- BOM/parts index binding;
- SVG/PDF or equivalent vector output;
- geometry change -> drawing marked stale;
- regeneration/readback after change.

**Current state: NOT PASSED.** Measurement guides are not a drawing service.

## P0-G — Professional modeling interaction / SketchUp + CAD ergonomics

Required:

- exact numeric entry;
- endpoint/midpoint/center/intersection inference;
- parallel/perpendicular/collinear inference;
- axis locks;
- temporary tracking/reference points;
- extension lines;
- measurement-first guides;
- real construction planes/axes;
- push/pull on capable solid route;
- context-aware move/rotate/scale;
- predictable local/world coordinate control;
- section plane workflow;
- user-visible unit/precision/tick system;
- undo-safe atomic operations.

**Current state: STRONG PARTIAL.** Metric, ruler, angular, datum, inference and tracking foundations are validated; push/pull solid workflow and section workflow remain incomplete.

## P0-H — Assembly / configuration / product data

Required:

- component identity separate from occurrences;
- local coordinate systems;
- assembly hierarchy;
- configuration/variant manager;
- exploded/transport/install/operate/service states;
- BOM with part-number conflict detection;
- mate/joint dependency integration;
- purchased-component provenance;
- mass/density metadata when authoritative source exists;
- center-of-mass readback when valid;
- assembly interference/clearance report at bounded geometry scope.

**Current state: PARTIAL.** Configuration and BOM are validated; assembly solver/mates and product-data depth are incomplete.

## P0-I — Product visualization / KeyShot / VRED class

Required:

- physical camera metadata and lens/sensor control;
- reusable studio light rigs;
- HDRI/environment provenance;
- IES support where applicable;
- PBR material presets separated from specification authority;
- color management / OCIO / ACES policy;
- product turntable/configuration rendering;
- object/material ID passes;
- render preset/version manifest;
- identical-source render reopen/readback;
- realtime derivative path with authority separation.

**Current state: PARTIAL via Blender native.** Must still receive OLEANDER validation receipts before default promotion.

---

# Tier P1 — specialist professional integrations

These do not need to be reimplemented internally, but the Blender shell must integrate them professionally when the active project requires them.

## P1-A — CAM

Candidate: Fabex.

Gate:

- stock/tool/work-coordinate definition;
- at least profile, pocket and bounded 3D milling workflow;
- toolpath simulation;
- postprocessor identity;
- G-code derivative hash;
- source geometry version binding;
- explicit manufacturing HOLD until external machine/process review.

## P1-B — GIS / large scene / survey

Candidate: BlenderGIS plus governed GIS sidecar where needed.

Gate:

- CRS metadata;
- large-coordinate/origin strategy;
- terrain/DEM linkage;
- georeferenced import/export;
- survey/reference geometry separated from design geometry;
- tile/proxy/LOD workflow;
- coordinate round-trip test.

## P1-C — CAE

Gate is adapter-based, not visual-only:

- solver identity/version;
- mesh generation/export identity;
- materials and properties;
- loads/boundary conditions;
- solve status/convergence metadata;
- result units;
- result field readback bound to geometry version;
- stale result after geometry/material/load changes;
- engineering approval remains separate.

## P1-D — fabrication/additive

Required when relevant:

- source geometry identity;
- units/orientation;
- watertight/manifold checks;
- 3MF/STL derivative lineage;
- target slicer/tool reopen when available;
- fabrication context separated from geometry authority.

---

# Additional original-target capability gates

## Maya-class animation / rigging

Blender native may satisfy this gate only after validating rig identity, constraints, animation state, NLA/action management, timeline/state export and FBX/Alembic round-trip for the bounded target workflow.

## Cinema 4D / MoGraph-class motion graphics

Geometry Nodes/instances may satisfy this gate after validating cloners/arrays, falloff/field-like control, deterministic random seeds, effector-style parameterization, cache and versioned procedural state.

## ZBrush-class sculpt workflow

Validate high-poly sculpt, multires/dyntopo policy, retopology handoff, normal/displacement bake lineage and reopenability. Sculpt quality itself remains a design review, not an automated PASS.

## Substance-class material workflow

Either integrate a capable texture authoring sidecar or validate a Blender-native procedural/PBR route with texture-set identity, channel contract, UV dependency, bake provenance and material-specification separation.

## Marvelous-class cloth workflow

Use Blender cloth or specialist sidecar only after validating pattern/source identity where applicable, physical parameter provenance, cache/bake state and non-claim boundaries for manufacturing patterns.

---

# Default environment promotion checklist

OLEANDER Blender Runtime may be proposed as the default modeling environment only when:

- [ ] P0-A Parametric CAD PASS
- [ ] P0-B Direct B-Rep PASS
- [ ] P0-C NURBS/Class-A bounded professional PASS
- [ ] P0-D Procedural professional foundation PASS
- [ ] P0-E BIM/IFC PASS
- [ ] P0-F Technical drawing PASS
- [ ] P0-G Modeling interaction PASS
- [ ] P0-H Assembly/configuration PASS
- [ ] P0-I Product visualization PASS
- [ ] all adopted dependencies have version/license/recovery records
- [ ] real Blender install/reopen/round-trip matrix passes
- [ ] failure envelopes include missing sidecar/plugin and incompatible-version tests
- [ ] required specialist P1 gate passes for each target project class
- [ ] PR is merged and `main` readback confirms one CURRENT

Until then the runtime status must remain **CANDIDATE / NOT DEFAULT**.
