# OLEANDER 3D Training Consolidation — 2026-09-01

Status: **CANDIDATE INDEX / NON-AUTHORITY / NO SILENT PROMOTION**

Purpose: consolidate the current 3D training record into capability chains without duplicating the canonical Notion practice pages or `3D_RUNTIME_EVIDENCE_MATRIX.md`.

Authority split:
- Notion practice pages = semantic record, proposition scope, failure provenance, Artifact Review and HOLDs.
- `3D_RUNTIME_EVIDENCE_MATRIX.md` = bounded executable/native/target-runtime facts.
- `PRACTICE_EVIDENCE_MATRIX_20260830.md` = cross-software evidence-class routing.
- This file = navigation/index only.

Hard rule:

`WORKFLOW GREEN != TRAINING CLOSED != DESIGN KEEP`

## A — Form / Representation / Operator Semantics

### PRAC-20260830-3D-01 — Porsche 992 Surface Control vs Evaluated Sampling
- Role: surface-control / evaluated-sampling failure study.
- Retained learning: control density is not surface quality; evaluated sampling is not design authority; Artifact Review remains independent of geometry existence.

### PRAC-20260831-3D-11 — Same-Source NURBS vs SubD
- Native workers: FreeCAD 1.1.3/OpenCASCADE B-Spline revolve + Blender 5.2 Catmull-Clark.
- Confirmed run: `33376553806` — SUCCESS.
- Bounded conclusions:
  - `SAME CONTROL ARCHITECTURE != SAME EVALUATED / LIMIT SURFACE`;
  - `HIGHER SUBD LEVEL != NURBS CONVERSION`;
  - control poles/rings are not automatically interpolation constraints;
  - compare representations on evaluated section/curvature/silhouette plus native reopen.
- HOLD: Rhino native `.3dm`, Zebra/EMap/CurvatureGraph/MatchSrf, G2/G3/Class-A, manufacturing, Design KEEP.

### PRAC-20260831-3D-12 — Operator Failure Anatomy
- Native workers: FreeCAD 1.1.3 B-Rep + Blender 5.2 modifiers.
- Latest visual-fix run: `33389249392` — workflow SUCCESS.
- Artifact: `9756862659`; ZIP digest `sha256:70687957293ce4765119058a8b2bf6f943b237f4076748a66e343a8c64b6c26c`.
- Native semantic findings:
  - FreeCAD Fillet: `5.9 mm` semantic success → `6.0 mm` kernel exception → `6.1 mm` invalid returned shape;
  - FreeCAD Thickness: `11.9 mm` semantic success → `12.0 mm` kernel exception → `12.1/14.0 mm` valid returned original-solid semantic no-op;
  - sphere inward offset: `-9.9 mm` regular domain → `-10.0 mm` zero-radius boundary failure;
  - Blender Bevel Clamp: requested `6.1` and `8.0 mm` both realize the same measured clamped corner clearance `4.701062 mm`;
  - Blender Solidify: requested `2 mm` realizes `1 mm` world thickness with unapplied Z scale `0.5`, and `2 mm` after scale is baked into geometry.
- Revised contract:
  - `RESULT = OPERATOR(INPUT, PARAMETERS, REFERENCES, TOLERANCE, POLICY, TRANSFORM_STATE, CONTEXT)`;
  - `SEMANTIC_SUCCESS = VALIDATE(RESULT, DECLARED_POSTCONDITIONS / INVARIANTS)`.
- Critical boundary: native semantic evidence PASS, but current Bevel/Solidify closeups are still too dark for direct visual discrimination. **Artifact Review = POST-REVIEW FAIL / TRAINING NOT CLOSED.**

## B — Procedural / Parametric / Dependency

### PRAC-20260830-3D-03 — Geometry Nodes Field / Attribute / Instance / Export Bake
- Bounded native propositions: field/attribute domain and type matter; Instance Component is not Mesh Component; Realize is a semantic/materialization decision; static export can discard graph semantics.

### PRAC-20260830-3D-04 — FreeCAD Parametric Dependency & STEP Roundtrip
- Native FreeCAD 1.1.3 dependency/change/recompute/native-reopen/STEP evidence.
- Does not establish Fusion parity.

## C — Surface Detail / Material / Lighting

### PRAC-20260830-3D-02 — Controlled Material–Reflection Attack
- Historical XJ01 runtime evidence retained.
- Recovered structurally matching candidates do not inherit historical 06B identity when authority hash is not restored.

### PRAC-20260830-3D-06 — High→Low Tangent Normal Bake
- Native Blender 5.2 bake/reopen evidence.
- Tangent-normal bake does not make low geometry macro-shape equivalent to high geometry.

### PRAC-20260830-3D-08 — Macro Geometry + Meso Tangent Bake
- Representation choice is governed by `frequency × view × required cue`.
- Normal/bump is insufficient when silhouette/parallax/self-occlusion/physical relief is required.

### PRAC-20260830-3D-10 — Material Data Semantics × Diagnostic Lighting
- Same roughness PNG bytes interpreted as Non-Color vs sRGB are not the same shader input semantics.
- Broad/Strip/Grazing diagnostic names earn authority only through output separation.
- Actual review: KEEP SUPPORT / DIAGNOSTIC EVIDENCE, not Physical CMF Approval or Design KEEP.

## D — Exchange / Runtime / Technical Art

### PRAC-20260830-3D-05 — GLB Chromium Target Runtime
- Blender → GLB → Chromium/Three/WebGL readback.
- `EXPORT PASS != TARGET-RUNTIME PASS`.

### PRAC-20260830-3D-07 — Signed Axis & Handedness + 2026-09-01 Negative-Determinant Extension
- Initial signed static transform witness established Blender `(x,y,z) → target (x,z,-y)` for the tested exporter/runtime carrier.
- 2026-09-01 extension: workflow `OLEANDER 3D glTF Negative Scale TBN Witness` run `33460924293` — SUCCESS.
- Tested tangent contract: `effective_w = tangent.w * sign(det(M_world))`.
- Actual WebGL framebuffer readback:
  - positive determinant expected/observed `[134,130,0,255]` / `[134,130,0,255]`;
  - negative determinant expected/observed `[121,130,0,255]` / `[121,130,0,255]`;
  - max channel delta `0`;
  - positive-vs-negative separation drift approximately `0.23771 deg`, inside the unchanged `<=0.5 deg` discriminator.
- Revised HOLD: non-uniform negative scale, nested negative transforms, applied/baked mirror parity, animation/skinning/morph, cameras/lights, full production PBR, hardware/other engines, Design KEEP.

### PRAC-20260830-3D-09 — Mirrored UV Tangent Basis
- `TANGENT.w`, UV convention and final perturbed normal belong to one exchange/shading contract.
- Triangulation after tangent-space bake is not shading-neutral.

## Consolidated theory that now has bounded executable support

1. **Representation** — control architecture, evaluated sampling and representation semantics are separate authorities.
2. **Dependency** — Timeline / modifier stack / node graph / declarative rebuild are not interchangeable dependency semantics.
3. **Instances** — prototype/reference + transform/attributes is not the same model as realized geometry.
4. **Surface detail** — representation bandwidth must be selected by the visual/physical cue required at the target view.
5. **Material data** — texture bytes do not define shader-input semantics without color/data interpretation.
6. **Interchange** — units/axis/UV/tangent/handedness/transform determinant/texture pixel/fragment output form a dependent handoff contract.
7. **Operators** — requested parameters and API validity do not prove realized design intent; semantic success requires declared postconditions and failure sweeps.

## Still OPEN / do not promote by association

- PRAC-12 visual diagnostic repair and POST-REVIEW PASS;
- Rhino 8 native `.3dm` + Class-A diagnostics;
- Autodesk Fusion native parameter/assembly/change-sweep benchmark;
- Houdini `.hip`, Maya `.ma/.mb`, 3ds Max `.max`, SketchUp `.skp` native practice;
- physical CMF correspondence, manufacturing and engineering truth;
- hardware GPU/driver and other-engine parity;
- Design KEEP.

## Governance correction

`oleander-skills/oleander-3d-pipeline/evals/evals.json` and `evals/modeling_essence_deep_cases.jsonl` are candidate diagnostic definitions. The current `AI Governance Evals` workflow executes `evals/scripts/validate_evals.py` against the global governance/golden corpus including `evals/golden/skills.jsonl`. A green governance workflow MUST NOT be described as execution of all local 3D diagnostic cases.

## Current candidate boundary

PR #468 remains **OPEN / DRAFT / NOT MERGED / CANDIDATE / NOT INSTALLED CURRENT**. `main` remains Current until explicit promotion after applicable evidence/readback/review gates.
