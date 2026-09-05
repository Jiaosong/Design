# OLEANDER C04 Blender Rebuild Route — Current Override

Status: **CURRENT / USER-EXPLICIT OVERRIDE / C04-SCOPED**

Effective date: 2026-09-02  
Realigned: 2026-09-05

Applies to:
- `PROJECT_ID=PRJ-C04-QINGJIANG-SHISHU`
- first returned rebuild batch: `云水倚 → 流体座椅人体工 → 江畔停泊折叠观`
- scope: Physical / Product / Spatial native-3D work only when editable volume is the required native output.

## Authority

This file records the user's explicit Blender route change and supersedes stale wording that treated the C04 model task as `Meshy MASTER → Decimate/LOD → GLB`.

**Work-object correction:** the three physical/product rebuilds are not lifecycle children of `PRJ-C04-DIGITAL-INTERACTION`. The Web object may consume a validated browser derivative later, but it is not the authority identity for a Physical/Product model. Each material rebuild/validation object must resolve its own stable project object identity, Source Authority, native master, owner, handoff and Flow Completion state before lifecycle advancement.

The whole-project owner is not defined by this route. This route only governs Blender-native production and its downstream handoff.

Legal bounded leases:
- `DESIGN_SUBTASK_LEASE=BLENDER_REBUILD_MASTER` for an explicitly authorized native-3D Work Object;
- `VALIDATION_SUBTASK_LEASE=REBUILD_VALIDATION` for native reopen / fidelity / model validation of that same Work Object;
- a Web runtime derivative lease is separate and exists only after a validated object is explicitly selected for Web/browser consumption.

A Blender lease, Validation lease, or Web derivative lease is not an owner transfer for the whole project.

## Current production route

Canonical model route:

`C04 Source / Existing Mature Design → resolve model Work Object → DESIGN editable Blender Candidate .blend → native reopen/readback → VALIDATION source/reference fidelity + topology/material/body/use-zone checks → applicable Independent Design Verdict / Best-Existing Benchmark → typed handoff → PRESENTATION consume in the required carrier`

Optional Web branch, only when the required presentation output includes browser 3D:

`validated model → bounded LOD/GLB/glTF/browser derivative → browser/runtime validation → PRESENTATION Web consumption`

**GLB/browser is not a mandatory gate for every model.** A model whose project value is technical drawing, board/PDF support, section/axon, product proof or other non-Web output may complete without a browser derivative once all applicable OLEANDER phases are closed.

The following route remains superseded as the primary rebuild route for the returned first batch:

`Meshy high-poly → direct decimation → GLB`

Direct Meshy decimation remains allowed only as diagnostic/reference comparison and must never be named `REBUILD MASTER`.

## Whole-project 3D coverage rule

The returned first batch does **not** close C04 3D production.

`NO MODEL 4 / NO MODEL 5 AUTHORIZATION` in `C04_MODEL_4_MODEL_5_CANDIDATE_AUDIT_v001.md` means only that the nine audited remaining source archives are not automatically promoted into Blender jobs merely because they exist.

A future C04 native-3D Work Object remains legal when all are true:
1. its exact project/design identity is bound to Current Authority / Asset Atlas;
2. it is selected `KEEP / CURRENTIZE / COMPETE` for a concrete scene/use or technical proof;
3. editable volume, spatial relation, body relation, product detail, motion geometry or fabrication/form study is materially required;
4. 2D/vector/editorial/interaction carriers cannot carry the required design truth;
5. Source Authority is sufficient to model defining geometry without fabrication of fact.

Therefore missing Physical P01–P09, Spatial/Technical, body/interface, detail or other whole-project objects may still enter Blender when this gate is satisfied.

## Source boundary

Original Meshy OBJ/texture packages and existing product/scene images remain immutable `SOURCE_REFERENCE` assets. They are not deleted or overwritten.

AI/Meshy geometry has no engineering or dimensional authority. When no verified dimensions exist, rebuilt geometry must record `DESIGN_ESTIMATE / UNKNOWN / FIELD_OPEN` as appropriate.

## Blender environment authority

Use the repository-wide runtime interface:

`00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.md`

Current verified runtime target:
- Blender `5.2.0 LTS`
- build `fbe6228777e7`
- Cycles baseline

Resolution remains:
1. `$OLEANDER_BLENDER_BIN`
2. `blender` on `PATH`
3. managed runtime fallback
4. repository runtime ensure/runner carrier when the current job needs rematerialization

A job-local missing binary is a carrier/materialization condition, **not** absence of the OLEANDER shared Blender environment.

## Completion gates

A C04 rebuild object is not materially advanced by prompt edits, authority reads, receipts, path checks, runtime probes, CI or persistence alone.

Minimum production evidence per model object:
- Blender-generated editable geometry;
- `.blend` Candidate identity;
- object/modifier/material hierarchy;
- preview/render or viewport evidence;
- native Blender reopen/readback;
- manifest with source/authority/unknown boundaries.

Production evidence is followed by all applicable downstream phases:
- source/reference fidelity;
- topology/material/body/use-zone or object-specific validation;
- independent design readback where a design verdict is required;
- Best-Existing Benchmark where KEEP-class promotion is considered;
- typed handoff to the actual presentation carrier;
- Flow Completion state.

A production `RETURNED` state is not model lifecycle `CLOSED`.

## Persistence

Preferred Drive destination:

`OLEANDER_Project-Archive/05_Cases/C04_Qingjiang-Stone-Book/C04_SOURCE_ASSETS_ENSHI_CURRENT/05_BLENDER_REBUILD_MASTERS/<object>/`

Git stores scripts, manifests, receipts and lightweight previews when appropriate. Large `.blend`/GLB assets use the approved artifact/Drive carrier.

## Truth boundary

`REBUILD CANDIDATE ≠ ENGINEERING MASTER ≠ FIELD PASS ≠ DESIGN KEEP`

`PRODUCTION RETURNED ≠ VALIDATION CLOSED ≠ PRESENTATION CLOSED ≠ FLOW COMPLETION`

`SHARED RUNTIME AVAILABLE ≠ A PARTICULAR JOB HAS ALREADY EXECUTED BLENDER`
