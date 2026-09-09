# OLEANDER Blender Runtime — v0.2 Current

Status: `ABSORBED INTO MAIN / BOUNDED CURRENT`
Parent Skill: `oleander-skills/oleander-3d-pipeline/SKILL.md`

This directory is the executable Blender implementation layer of the single OLEANDER 3D Skill. It is not a second Skill or a second Current authority.

## Shared environment software boundary

OLEANDER Blender is a **shared 3D environment software layer**, not a project-specific Blender plug-in and not a runtime owned by any individual design project.

The stable product boundary is:

```text
Shared OLEANDER Blender Environment
├─ Runtime Core: identity / dependency / authority / audit / diff / stale state
├─ Modeling Environment: direct / parametric / surface / procedural / sculpt / assembly
├─ Domain Workspaces: general / product / spatial / architecture / exhibition / furniture / landscape
├─ Professional Backends: CAD/B-Rep / NURBS / BIM/IFC / GIS / CAE / CAM / drawing
└─ Project Profiles: optional configuration consumers of the shared environment
```

Rules:

- Runtime/Core implementation must remain project-neutral and must not import project IDs, project geometry code, project assets or project-specific authority semantics;
- a project is a **consumer** of the shared environment through an optional Project Profile, never the owner of the Runtime core;
- Domain Workspace is a reusable software mode; it is not a Project Profile;
- Project Profiles may configure units, naming, metadata defaults, review rules, export templates and workspace defaults;
- Project Profiles must not replace geometry/master authority, bypass audit or validation, silently change specialist-kernel routing, or convert project evidence into a global capability claim;
- specialist sidecars are shared capability backends and preserve their own authority contracts across projects;
- project usage evidence may validate that the shared Runtime is consumed in real work, but it does not make project-specific behavior part of the common software.

The Blender scene exposes this boundary through `Scene.oleander_environment`: `domain_workspace`, optional `project_profile_id`, `project_profile_locator`, and `project_profile_state`. An unbound scene remains a valid shared OLEANDER environment with project-neutral defaults.

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

## Current absorption state

The previously separate Runtime/Workbench candidate was absorbed into `main` on 2026-09-07 through PR #470 as a bounded extension of the existing `oleander-3d-pipeline` Current. The absorption does not enable the default environment and does not promote general professional CAD parity or `P0_B_DIRECT_BREP`.

Current governance authority remains `blender_runtime/CANDIDATE_GOVERNANCE.json`, whose historical candidate lineage is retained as provenance while `main` is the only installed Current for the absorbed scope.

## Existing-first module map

Before adding implementation, extend or compose an existing owner when it can carry the requirement:

- shared environment/profile state + object identity / metadata: `properties.py`;
- shared environment UI + audit surface: `panel.py`;
- identity / audit / dependency / diff: `properties.py`, `audit.py`, `dependency.py`, `geometry_diff.py`, `review_state.py`;
- direct modeling / editable feature stack: `direct_model.py`, `feature_stack.py`, `feature_edit.py`;
- measurement / ruler / datum / inference: `measurement_system.py`, `measurement_atomic.py`, `angular_datum.py`, `precision_inference.py`, `inference_engine.py`;
- relations / deterministic one-shot correction / configurations: `relation_kernel.py`, `relation_apply.py`, `configuration.py`, `configuration_ops.py`;
- design-intent registry / explicit apply / batch / rebuild: `design_intent.py`, `design_intent_apply.py`, `design_intent_batch.py`, `design_intent_rebuild.py`;
- Geometry Nodes governance: `procedural.py`;
- evaluated mesh clearance / surface diagnostics: `mesh_clearance.py`, `surface_diagnostics.py`;
- CAD-native authority handoff: `professional_adapter/cad_sidecar.py` plus the applicable specialist CAD route.

Do not create a parallel Blender Skill, assembly Skill, CAD Skill, second Workbench framework or one-off professional workflow when an existing owner can be extended. New implementation requires a material capability gap plus authority/anti-pollution preflight.

## Validated Blender-native scope

The Current absorbed scope includes validated bounded support for:

- persistent OLE IDs and governed metadata;
- scene/object authority separation;
- dependency graph, stale propagation and geometry/parameter diff;
- direct metric object operations;
- Direct Face bounded v0.2 for `BLENDER_NATIVE` mesh masters: one selected face may move along its local normal in mm or within a deterministic geometry-derived U/V tangent basis in mm, with applied-scale/single-user/shape-key fail-closed gates and downstream stale propagation;
- Direct Face provenance records requested metric movement, resolved semantic face descriptor and, for tangent movement, the resolved U/V basis without persisting BMesh edge indices as authority;
- the Direct Face Normal Move entrypoint routes `CAD_NATIVE` objects to a deterministic `OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1` without mutating the Blender display derivative;
- CAD Direct Face intent targets described semantically by normal/center/area/edge-length/bounds data rather than persistent `FaceN`, polygon index or subshape ordinal; ambiguous or missing specialist re-resolution remains `HOLD`;
- `CAD_NATIVE` Tangent Move is explicitly fail-closed in Direct Face v0.2 until the existing shared CAD sidecar absorbs a typed tangent operation; invoking it must not mutate the Blender display derivative or overwrite a previously valid CAD Normal Move intent;
- non-destructive Blender-native feature stack and feature editing lifecycle;
- governed relation registry, tolerance audit and deterministic one-shot relation correction with `solver_claim = false`;
- measurement profiles, rulers, angular guides, datum/reference geometry and precision inference;
- evaluated mesh surface clearance and bounded polygon-mesh surface diagnostics;
- design parameter registry, dependency graph, explicit apply, atomic batch apply, rebuild planning and rollback/provenance;
- Geometry Nodes procedural foundation with governed provenance;
- configuration/BOM support, audit and export manifest foundations.

The initial bounded Direct Face Normal Move route was validated in canonical Blender `5.2.0 LTS` through PR #495: Blender-native `+25 mm` face movement passed with stale propagation, while the CAD-native route produced a governed intent and preserved identical Blender display vertex geometry.

PR #497 then validated deterministic `OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1` → `OLEANDER_CAD_DIRECT_EDIT_REQUEST_v0.1` translation and strict request persistence boundaries in the existing `professional_adapter/cad_sidecar.py` owner. `CAD_DIRECT_INTENT_BRIDGE_RECEIPT_5_2_20260909.json` remains the machine evidence for that request contract.

PR #499 subsequently established a separate bounded authoritative CAD Normal Move execution path: Blender 5.2 interaction/request preparation → FreeCAD 1.1.3 / OCCT semantic face re-resolution → bounded `FACE_NORMAL_MOVE` B-Rep mutation → FCStd/STEP/BREP + typed display derivative → Blender display-only save/reopen readback. `MISSING_HOLD` and `AMBIGUOUS_HOLD` release no authoritative result artifacts. This remains bounded execution evidence, not general B-Rep push/pull or persistent topological naming generality.

Direct Face bounded v0.2 adds the Blender-native Tangent Move interaction on top of that Current architecture. Canonical Blender 5.2 regression validates U/V metric movement, geometry-derived tangent basis, stale propagation and a fail-closed CAD tangent route with zero display mutation. CAD tangent specialist execution is intentionally a later absorption into the existing sidecar; `P0_G_MODELING_INTERACTION` remains PARTIAL and `P0_B_DIRECT_BREP` remains BLOCKED.

The shared-environment Project Profile surface added on 2026-09-09 is a configuration boundary, not a new professional parity claim.

## Specialist-kernel boundary

Blender remains the interactive host, not a universal geometry kernel.

When authoritative B-Rep, parametric CAD, Class-A/NURBS, IFC/BIM, CAE, CAM or other specialist output is required, route through the parent Skill's specialist extension and only claim the bounded scope supported by actual runtime evidence.

For CAD-native objects:

- CAD native source remains geometry authority;
- STEP/BREP/FCStd or other native/exchange artifacts remain traceable;
- Blender receives a typed display/review derivative;
- Direct Face Normal Move may prepare a deterministic CAD direct-edit intent; the existing CAD sidecar validates/serializes the request and, for the bounded #499 scope, a specialist FreeCAD/OCCT executor may uniquely re-resolve and mutate the authoritative B-Rep before Blender receives a display derivative;
- Direct Face Tangent Move currently has no absorbed CAD specialist route and therefore fails closed without mutating Blender display geometry;
- the display mesh must never be mutated as an authoritative CAD result;
- semantic face rebind must fail closed on ambiguity or missing targets and must not persist unstable topology ordinals as authority;
- Blender mesh operations must not be described as equivalent to authoritative B-Rep operations;
- bounded FreeCAD/OCCT proofs do not establish general CAD parity.

## Still not claimed

The absorbed Current scope does not by itself establish:

- CAD tangent direct-edit execution from Direct Face v0.2;
- general B-Rep push/pull, trim or unrestricted direct-edit parity;
- persistent topological naming generality;
- general B-Rep/CAD parity;
- `P0_B_DIRECT_BREP` PASS or `P0_G_MODELING_INTERACTION` PASS;
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

1. resolve shared Runtime authority and, when present, the active Project Profile without allowing the profile to replace Runtime authority;
2. resolve Current Project/Object authority and Required Native Output for project work;
3. reuse an existing module before creating implementation;
4. run static contract checks and the smallest affected real-Blender validation;
5. for current-wide compatibility, run the canonical Blender 5.2 LTS regression;
6. reopen/read back persisted state where applicable;
7. keep Machine/Compliance evidence separate from Professional Design verdict;
8. update `SKILL.md`, `CAPABILITY.json`, `BLENDER_RUNTIME_WORKBENCH_EXTENSION.md`, `CANDIDATE_GOVERNANCE.json`, parity/capability status and the matching Notion control surface only when their material facts change; do not create a promotion delta where the capability class remains unchanged.

A material runtime change that is not reflected in its routing/status surfaces is an alignment failure even when its code tests pass.

## Baseline checks retained from the original scaffold

The original Stage-2 baseline remains part of the regression set: stable OLE ID through rename, duplicate-ID failure/repair, missing master/dependency detection, field/engineering/manufacturing state separation, non-manifold review, dependency-path checks, editable manifest output and audit wording that never claims engineering/constructability/design approval.

## Promotion boundary

`main` is the installed Current for the bounded absorbed Runtime/Workbench scope. Any promotion beyond that scope still requires the current OLEANDER governance gate, fresh main synchronization, contradiction scan, real project-use evidence when applicable, runtime readback, and an explicit promotion decision. Passing real Blender regression alone does not promote blocked parity gates or enable the default environment.
