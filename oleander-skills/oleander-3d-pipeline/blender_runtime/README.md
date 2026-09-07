# OLEANDER Blender Runtime — v0.2 Candidate

Status: `OPEN CANDIDATE / NOT INSTALLED CURRENT`
Parent Skill: `oleander-skills/oleander-3d-pipeline/SKILL.md`

This directory is the executable Blender implementation layer of the single OLEANDER 3D Skill. It is not a second Skill or a second Current authority.

## Current runtime compatibility

Current-source compatibility evidence is the consolidated real-runtime receipt:

`BLENDER_RUNTIME_REGRESSION_RECEIPT_5_2_LTS_20260905.json`

Validated environment:

- Blender `5.2.0 LTS`;
- build `fbe6228777e7`;
- canonical resolver `90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh`;
- seventeen bound validation stages: Stage 2 core plus Direct, Feature Stack, Feature Editing, Relations, Relation Apply, Measurement, Angular/Datum, Precision/Inference, Inference v2, Mesh Clearance, Surface Diagnostics, Design Intent, Design Intent Apply, Design Intent Batch, Design Intent Rebuild and Procedural;
- current-source runtime result: `PASS`.

Historical Blender 5.1.2 per-stage receipts remain immutable provenance. They are not current-source compatibility authority after the Blender 5.2 procedural compatibility repair.

## Existing-first module map

Before adding implementation, extend or compose an existing owner when it can carry the requirement:

- identity / metadata / audit / dependency / diff: `properties.py`, `audit.py`, `dependency.py`, `geometry_diff.py`, `review_state.py`;
- direct modeling / editable feature stack: `direct_model.py`, `feature_stack.py`, `feature_edit.py`;
- measurement / ruler / datum / inference: `measurement_system.py`, `measurement_atomic.py`, `angular_datum.py`, `precision_inference.py`, `inference_engine.py`;
- relations / deterministic one-shot correction / configurations: `relation_kernel.py`, `relation_apply.py`, `configuration.py`, `configuration_ops.py`;
- design-intent registry / explicit apply / batch / rebuild: `design_intent.py`, `design_intent_apply.py`, `design_intent_batch.py`, `design_intent_rebuild.py`;
- Geometry Nodes governance: `procedural.py`;
- evaluated mesh clearance / surface diagnostics: `mesh_clearance.py`, `surface_diagnostics.py`;
- CAD-native authority handoff: `professional_adapter/cad_sidecar.py` plus the applicable specialist CAD route.

Do not create a parallel Blender Skill, assembly Skill, CAD Skill, second Workbench framework or one-off professional workflow when an existing owner can be extended. New implementation requires a material capability gap plus authority/anti-pollution preflight.

## Validated Blender-native scope

The Candidate includes validated bounded support for:

- persistent OLE IDs and governed metadata;
- scene/object authority separation;
- dependency graph, stale propagation and geometry/parameter diff;
- direct metric object operations;
- non-destructive Blender-native feature stack and feature editing lifecycle;
- governed relation registry, tolerance audit and deterministic one-shot relation correction with `solver_claim = false`;
- measurement profiles, rulers, angular guides, datum/reference geometry and precision inference;
- evaluated mesh surface clearance and bounded polygon-mesh surface diagnostics;
- design parameter registry, dependency graph, explicit apply, atomic batch apply, rebuild planning and rollback/provenance;
- Geometry Nodes procedural foundation with governed provenance;
- configuration/BOM support, audit and export manifest foundations.

## Specialist-kernel boundary

Blender remains the interactive host, not a universal geometry kernel.

When authoritative B-Rep, parametric CAD, Class-A/NURBS, IFC/BIM, CAE, CAM or other specialist output is required, route through the parent Skill's specialist extension and only claim the bounded scope supported by actual runtime evidence.

For CAD-native objects:

- CAD native source remains geometry authority;
- STEP/BREP/FCStd or other native/exchange artifacts remain traceable;
- Blender receives a typed display/review derivative;
- Blender mesh operations must not be described as equivalent to authoritative B-Rep operations;
- bounded FreeCAD/OCCT probes do not establish general CAD parity.

## Still not claimed

The Candidate does not by itself establish:

- general B-Rep/CAD parity;
- general parametric sketch/feature/assembly solver parity;
- unrestricted assembly mates/joints;
- NURBS/Class-A continuity certification;
- IFC-native author/edit/export/reopen parity;
- associative professional technical-drawing parity;
- engineering approval, manufacturing release, constructability or field truth;
- Design PASS from Machine/CI PASS.

See `PROFESSIONAL_PARITY_STATUS.json` for the current bounded professional capability boundary.

## Development validation sequence

For material runtime changes:

1. resolve Current Project/Object authority and Required Native Output;
2. reuse an existing module before creating implementation;
3. run static contract checks and the smallest affected real-Blender validation;
4. for candidate-wide compatibility, run the canonical Blender 5.2 LTS regression;
5. reopen/read back persisted state where applicable;
6. keep Machine/Compliance evidence separate from Professional Design verdict;
7. update `SKILL.md`, `CAPABILITY.json`, `BLENDER_RUNTIME_WORKBENCH_EXTENSION.md`, `CANDIDATE_GOVERNANCE.json`, parity/capability status and the matching Notion control surface when their facts materially changed.

A material runtime change that is not reflected in its routing/status surfaces is an alignment failure even when its code tests pass.

## Baseline checks retained from the original scaffold

The original Stage-2 baseline remains part of the regression set: stable OLE ID through rename, duplicate-ID failure/repair, missing master/dependency detection, field/engineering/manufacturing state separation, non-manifold review, dependency-path checks, editable manifest output and audit wording that never claims engineering/constructability/design approval.

## Promotion gate

Do not treat this Candidate as installed Current merely because real Blender regression passes. Promotion requires the current OLEANDER Candidate governance gate, fresh main synchronization, current PR authority, contradiction scan, required project-usage or explicit bounded absorption decision, and explicit promotion decision.
