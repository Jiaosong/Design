# OLEANDER Blender Runtime / Workbench Extension

Status: PROPOSED IMPLEMENTATION LAYER
Parent authority: `oleander-skills/oleander-3d-pipeline/SKILL.md`

## Purpose

Turn Blender into the primary interactive OLEANDER 3D workbench without pretending that Blender's mesh kernel is equivalent to specialist CAD, BIM, CAE, CAM or Class-A systems.

The user should be able to remain in one interactive environment while OLEANDER routes each task to the appropriate deterministic geometry or analysis backend, then returns governed results to a shared object-identity layer.

This extension does not replace the parent 3D Skill. It implements a Blender-first runtime shell under the existing rules for Current master, dimension authority, exchange, field/manufacturing HOLD, AI visual boundaries and round-trip validation.

## Core principle

`one interaction environment != one geometry kernel`

OLEANDER Blender is a unified design environment composed of specialist kernels and services:

```text
OLEANDER Blender Workbench
├─ Blender scene / mesh / curve / sculpt / animation / shading / rendering
├─ Geometry Nodes procedural runtime
├─ CAD sidecar: B-Rep / NURBS / STEP / sketch constraints / assembly
├─ BIM semantic sidecar: IFC / element semantics / quantities
├─ CAE sidecar: governed analysis exchange and result readback
├─ CAM/fabrication sidecar: process-specific manufacturing derivatives
├─ Drawing service: vector technical drawing and annotation
└─ OLEANDER governance: object identity / authority / validation / version / audit
```

No sidecar is considered available until runtime probing proves it is callable in the current environment.

## Unified object identity

Every logical design object must have a persistent OLEANDER identity independent of application-specific object names.

Minimum object metadata:

```yaml
ole_id: OLE_QJ_R06_PLATFORM_BEAM_001
object_class: structural_member
master_type: CAD_NATIVE | BLENDER_NATIVE | BIM_NATIVE | EXTERNAL_NATIVE
master_locator: governed locator
unit_system: mm
geometry_authority: VERIFIED_SOURCE | GOVERNED_ESTIMATE | FIELD_OPEN
material_authority: SPECIFIED | ESTIMATE | VISUAL_ONLY
field_state: VERIFIED | OPEN
engineering_state: APPROVED | OPEN | NOT_APPLICABLE
manufacturing_state: RELEASED | OPEN | NOT_APPLICABLE
lod: 300
assembly_id: OLE_QJ_R06_PLATFORM_ASSY_001
derivative_ids: []
```

Blender object names may mirror `ole_id`, but the identity must not depend solely on the Blender datablock name.

## Six-kernel architecture

### 1. Geometry Kernel

Supported geometry families:

- mesh / subdivision;
- curve / spline;
- volume / voxel;
- B-Rep solid;
- NURBS surface;
- point cloud / reality-capture derived geometry;
- terrain / GIS-derived geometry.

Routing rule:

- mesh, sculpt, subdivision, scene assembly -> Blender native;
- procedural mesh/curve generation -> Geometry Nodes;
- fit-critical product/mechanical geometry -> CAD sidecar;
- Class-A-critical final surface authority -> specialist surface/CAD runtime when available;
- point cloud / survey truth -> reality-capture route, never silently remeshed into field truth.

### 2. Relation Kernel

Relations must survive ordinary visual editing where possible and must be explicit when they cannot.

Relation types:

- dimensions;
- sketch constraints;
- datums and reference frames;
- mates / joints / assembly relations;
- geometric constraints;
- spatial design constraints;
- procedural dependencies;
- array / distribution relations;
- parent-child and attachment relations;
- state/configuration relations.

High-level spatial constraints may include rules such as `offset_from_wall=300mm`, `equal_spacing`, `face_route`, `align_to_axis`, or `maintain_clearance`, but each must resolve to inspectable parameters rather than opaque AI-generated geometry.

### 3. Semantic Kernel

Geometry may carry domain meaning without making unsupported engineering claims.

Supported semantic families:

- product / component / assembly;
- architecture / interior / exhibition;
- landscape / site / route;
- BIM/IFC element type;
- material / finish / manufacturer reference;
- construction / installation state;
- maintenance state;
- evidence state;
- project stable IDs.

A semantic tag does not certify compliance, engineering approval or field truth.

### 4. Validation Kernel

`OLEANDER AUDIT` must separate machine-checkable facts from professional approval.

Baseline automated checks:

- units and world scale;
- bounding-box plausibility;
- transforms / pivots / origins;
- normals;
- non-manifold geometry;
- duplicate geometry;
- degenerate geometry;
- material naming;
- missing/absolute texture paths;
- modifier state;
- dependency health;
- object identity collisions;
- LOD/poly-density thresholds;
- UV state when required;
- export target compatibility;
- CAD-master vs display-mesh authority;
- sidecar round-trip deviation;
- field/engineering/manufacturing state completeness.

Audit result example:

```text
GEOMETRY             PASS
UNITS_AXES           PASS
DEPENDENCIES         PASS
ROUND_TRIP           PASS
DIMENSION_AUTHORITY  GOVERNED_ESTIMATE
FIELD_VERIFIED       NO
ENGINEERING_APPROVAL OPEN
CONSTRUCTABILITY     OPEN
DESIGN_QUALITY       REVIEW_REQUIRED
```

Never collapse these into one generic `PASS`.

### 5. Representation Kernel

The same governed object system may produce:

- viewport representation;
- clay/model render;
- photoreal render;
- diagram render passes;
- orthographic views;
- section/elevation;
- axonometric;
- exploded view;
- animation;
- realtime viewer;
- web GLB/glTF;
- technical drawing;
- BOM/quantity derivative.

Final technical labels, dimensions and explanatory text remain vector/editable. Raster render text is never final technical annotation.

### 6. Governance Kernel

Governance functions:

- Current master pointer;
- derivative typing;
- authority state;
- object-level version;
- configuration/version branch;
- geometry diff;
- parameter diff;
- dependency graph;
- plugin/runtime dependency record;
- deterministic export manifest;
- SHA/commit lineage when material;
- round-trip test result;
- superseded-state tracking.

## Workbench modes

The Blender UI should be reorganized by design intent rather than by a collection of unrelated add-ons.

### DESIGN

- Product
- Spatial
- Architecture
- Exhibition
- Furniture
- Landscape

### BUILD

- Direct
- Parametric
- Surface
- Procedural
- Sculpt
- BIM

### DOCUMENT

- Plan
- Elevation
- Section
- Axonometric
- Exploded
- Detail
- BOM

### VISUALIZE

- Product studio
- Spatial scene
- Analytical diagram
- Animation
- Realtime

### VALIDATE

- Geometry
- Dimension
- Assembly
- Material
- Fabrication
- OLEANDER Audit

The UI may expose specialist tools contextually, but must not hide the actual authoritative runtime or modeling type.

## Specialist capability absorption

### CAD / SolidWorks / Fusion / Inventor advantages

Implement through CAD sidecar, not fake mesh features:

- sketches with dimensional/geometric constraints;
- datum planes/axes/points;
- feature parameters;
- B-Rep solids;
- shell / draft / fillet / chamfer;
- pattern / mirror;
- fit-critical holes and interfaces;
- assembly relations;
- STEP import/export;
- deterministic dimensional readback.

The Blender scene receives a display/review representation while native CAD remains authority when required.

### Rhino / Alias advantages

Target capabilities:

- curve degree/CV inspection;
- rebuild / match;
- loft / sweep / network / blend;
- surface continuity G0/G1/G2/G3 where supported;
- zebra analysis;
- curvature comb;
- Gaussian curvature;
- draft analysis;
- thickness / minimum-radius analysis;
- deviation map against authoritative surface.

If the active kernel cannot certify the requested surface continuity, state the limitation explicitly.

### Plasticity-style direct modeling

Provide context-sensitive direct solid operations when a capable B-Rep runtime is present:

- push/pull face;
- offset face;
- boolean;
- split;
- shell;
- fillet/chamfer;
- direct face move/rotate;
- pattern/mirror.

Do not present mesh booleans as equivalent to B-Rep direct solid modeling.

### Houdini advantages

Extend Geometry Nodes workflow with governance around:

- published parameters;
- dependency inspection;
- attribute inspection;
- cache/bake state;
- debug visualization;
- performance profile;
- geometry diff;
- node-group version;
- LOD generation;
- deterministic procedural asset manifest.

### SketchUp advantages

Spatial direct mode should prioritize:

- real-world numeric input;
- endpoint / midpoint / intersection snapping;
- parallel/perpendicular inference;
- axis locks;
- guide lines;
- direct face extrusion;
- section planes;
- measurement-first interaction.

### Revit/BIM advantages

Use semantic objects and IFC route for:

- element type;
- family/type-like parameter sets;
- spatial containers;
- quantity extraction;
- system relationships;
- IFC round-trip when available.

A Blender object with an IFC label is not automatically a valid BIM deliverable.

### KeyShot / VRED / realtime advantages

Standardize:

- physical camera metadata;
- product studio rigs;
- HDRI/environment provenance;
- physical light/IES dependency;
- material presets with visual vs specification authority;
- OCIO/ACES color-management contract;
- render/realtime derivative tracking.

## Material system

Separate visual shading from material specification.

Material record may include:

- visual PBR parameters;
- base color / texture set;
- real thickness where relevant;
- density;
- nominal specification;
- finish/process;
- manufacturer/product reference;
- weathering/maintenance notes;
- cost estimate source;
- carbon-data source;
- material authority state.

A shader is not a material specification.

## Technical drawing layer

The workbench must support a governed route from verified 3D geometry to editable/vector drawing output.

Required drawing concepts:

- orthographic projection;
- section/elevation;
- hidden-line strategy;
- line-weight classes;
- stable view ID;
- associative dimensions where runtime permits;
- editable labels;
- callout/detail references;
- parts/BOM indexing;
- revision identity.

If associativity cannot be maintained, mark the drawing as a derivative requiring regeneration/readback after geometry changes.

## Assembly and configuration system

Support named configurations such as:

- size variants;
- material variants;
- left/right variants;
- installation state;
- transport state;
- operating state;
- maintenance state;
- disassembly/exploded state.

Configurations should prefer parameter/state changes over duplicated uncontrolled geometry.

## Large-scene / GIS / survey mode

For landscape, architecture and territory-scale work support:

- tile/region loading;
- instance/proxy strategy;
- LOD;
- large-coordinate origin management;
- survey coordinate metadata;
- DEM/terrain derivation;
- point-cloud linkage;
- GIS layer linkage;
- explicit separation of survey truth, derived model and design geometry.

Coordinate simplification for Blender display must never silently overwrite the survey/reference coordinate authority.

## CAE route

OLEANDER Blender may prepare and exchange analysis geometry and read results, but it does not become a solver merely by visualizing results.

CAE handoff record must include:

- solver/runtime identity;
- geometry version;
- material assumptions;
- boundary conditions;
- load cases;
- mesh assumptions;
- solve status;
- result units;
- convergence/quality evidence when available;
- engineering approval state.

Automated analysis output remains `ENGINEERING OPEN` unless qualified review/approval exists.

## CAM / fabrication route

Potential process routes:

- CNC;
- laser/waterjet;
- sheet fabrication;
- additive manufacturing;
- woodworking;
- robotic fabrication.

Manufacturing derivatives must preserve:

- source master identity;
- units;
- process orientation;
- stock/material assumptions;
- kerf/tool compensation assumptions when applicable;
- machine/postprocessor identity when applicable;
- generated file hash;
- reopen/verification state.

A toolpath preview is not manufacturing approval.

## Design compiler behavior

The target architecture is dependency-driven:

```text
Design Intent
→ Parameters / Constraints / Relations
→ Geometry
→ Semantics / Material / Construction State
→ Validation
→ Drawings / BOM / Render / Animation / Web / Fabrication Derivatives
```

Changing an authoritative upstream parameter should mark affected downstream representations stale and regenerate them where deterministic routes exist.

Example dependency propagation:

```text
platform_width 2400 -> 3000
→ structure geometry stale
→ cladding quantity stale
→ lighting distribution stale
→ BOM stale
→ drawing dimensions stale
→ exploded view stale
→ GLB stale
→ render cameras REVIEW
```

No downstream output may remain silently presented as current after its upstream authority changes.

## AI command layer

Natural-language control may translate user intent into deterministic operations, parameter changes and governed tool calls.

Allowed pattern:

`language instruction -> parsed operation -> explicit parameters -> deterministic kernel -> readback -> audit`

Disallowed pattern for authoritative geometry:

`language instruction -> opaque generated mesh -> claim dimensions/engineering correctness`

AI may propose parameters, but verified or governed dimension authority still controls final geometry.

## Plugin isolation

Third-party Blender add-ons are dependencies, not invisible parts of the master model.

Record:

- add-on name;
- version;
- license when relevant;
- objects/data affected;
- whether resulting geometry remains editable without the add-on;
- bake state;
- fallback/recovery path.

A missing add-on must produce a dependency warning, not silent degradation.

## Runtime capability levels

### L0 — Blender Native

Mesh, curves, Geometry Nodes, sculpt, materials, animation, render, scene organization.

### L1 — Governed Blender Workbench

OLEANDER object identity, metadata, audit, presets, dependency graph, export manifests and technical representation helpers.

### L2 — Specialist Sidecars

CAD/B-Rep/NURBS, IFC/BIM, reality capture, drawing, CAE/CAM services where actual runtime is available.

### L3 — Verified Cross-domain Pipeline

Round-trip validation, geometry deviation tests, stale-dependency propagation, controlled manufacturing/engineering handoffs and reopen verification.

Do not claim L2/L3 capability without active runtime evidence.

## Minimum implementation sequence

1. Object identity + metadata schema.
2. OLEANDER Audit panel.
3. unit/axis/dependency/export manifest checks.
4. workspace presets and command palette.
5. Geometry Nodes parameter/dependency governance.
6. CAD sidecar adapter and STEP round-trip test.
7. technical drawing derivative service.
8. assembly/configuration manager.
9. BIM/IFC semantic adapter.
10. large-scene/GIS/reality-capture adapter.
11. material specification layer.
12. CAE/CAM governed handoff adapters.
13. object-level diff and stale-output propagation.
14. natural-language deterministic operator layer.

## Non-goals

- Reimplement every specialist solver inside Blender.
- Claim Blender mesh operations are equivalent to parametric CAD.
- Claim visual smoothness is Class-A verification.
- Claim IFC tags alone are BIM validation.
- Claim rendered material appearance is a material specification.
- Claim simulation visualization is engineering approval.
- Replace real geometry/drawing/text with AI-generated images.

## Required implementation evidence

A future executable implementation must demonstrate at minimum:

1. a Blender-native object retaining stable `ole_id` through rename/duplicate/export;
2. one governed parameter change producing a traceable geometry update;
3. one CAD-native object producing a Blender display derivative while preserving CAD master authority;
4. STEP or equivalent round-trip with scale/bounding-box/deviation checks;
5. one stale downstream derivative detected after upstream geometry changes;
6. OLEANDER Audit separating geometry PASS from FIELD/ENGINEERING/DESIGN status;
7. vector/editable technical annotation output;
8. dependency manifest listing external add-ons/sidecars;
9. reopen/readback evidence;
10. no AI-generated visual serving as geometry or dimension authority.
