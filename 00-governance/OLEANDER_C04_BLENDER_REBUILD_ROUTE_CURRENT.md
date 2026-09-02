# OLEANDER C04 Blender Rebuild Route — Current Override

Status: **CURRENT / USER-EXPLICIT OVERRIDE / C04-SCOPED**

Effective date: 2026-09-02

Applies to:
- `PROJECT_ID=PRJ-C04-QINGJIANG-SHISHU`
- `OBJECT_ID=PRJ-C04-DIGITAL-INTERACTION`
- first production queue: `云水倚 → 流体座椅人体工 → 江畔停泊折叠观`

## Authority

This file records the user's explicit route change and therefore overrides stale queue/frontier wording that still describes the C04 model task as `Meshy MASTER → Decimate/LOD → GLB`.

The public/project owner remains:

`CURRENT_OWNER=PRESENTATION`

Two bounded concurrent subtask leases are legal:

- `DESIGN_SUBTASK_LEASE=BLENDER_REBUILD_MASTER`
- `VALIDATION_SUBTASK_LEASE=REBUILD_VALIDATION_AND_WEB_DERIVATIVE`

Neither lease is an owner transfer.

## Current production route

The Current route is:

`/恩施 SOURCE_REFERENCE → DESIGN Blender editable rebuild Candidate .blend → VALIDATION native Blender reopen/fidelity → validated rebuild Candidate → LOD/GLB/browser derivative → PRESENTATION consume`

The following route is superseded as the **primary** route for the first three objects:

`Meshy high-poly → direct decimation → GLB`

Direct Meshy decimation remains allowed only as a diagnostic/reference comparison and must never be named `REBUILD MASTER`.

## Source boundary

The original Meshy OBJ/texture packages and existing product/scene images remain immutable `SOURCE_REFERENCE` assets. They are not deleted or overwritten.

AI/Meshy geometry has no engineering or dimensional authority. When no verified dimensions exist, rebuilt geometry must record `DESIGN_ESTIMATE / UNKNOWN / FIELD_OPEN` as appropriate.

## Blender environment authority

Use the existing repository-wide runtime interface:

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

A job-local missing binary must be represented as a carrier/materialization condition, **not** as absence of the OLEANDER shared Blender environment.

## Completion gates

A C04 rebuild object is not materially advanced by prompt edits, authority reads, receipts, path checks, or runtime probes alone.

Minimum first-round material evidence per object:
- Blender-generated editable geometry;
- `.blend` Candidate identity;
- object/modifier/material hierarchy;
- preview/render or viewport evidence;
- native Blender reopen/readback;
- manifest with source/authority/unknown boundaries.

Only after rebuild validation may Web derivatives be treated as production outputs.

## Persistence

Preferred Drive destination:

`OLEANDER_Project-Archive/05_Cases/C04_Qingjiang-Stone-Book/C04_SOURCE_ASSETS_ENSHI_CURRENT/05_BLENDER_REBUILD_MASTERS/<object>/`

Git stores scripts, manifests, receipts and lightweight previews when appropriate. Large `.blend`/GLB assets use the approved artifact/Drive carrier.

## Truth boundary

`REBUILD CANDIDATE ≠ ENGINEERING MASTER ≠ FIELD PASS ≠ DESIGN KEEP`

`SHARED RUNTIME AVAILABLE ≠ A PARTICULAR JOB HAS ALREADY EXECUTED BLENDER`
