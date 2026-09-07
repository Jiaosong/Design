# oleander-3d-pipeline｜Project Usage Feedback Current

Status: `OWNER-LOCAL PROJECT LEARNING / INSTALLED SKILL SUPPORT / SHARED RUNTIME USE ESTABLISHED / EXACT SKILL USAGE PROVENANCE NOT ESTABLISHED / NO NEW SKILL / NO DESIGN PROMOTION`

Purpose: preserve transferable project learning for the existing installed `oleander-3d-pipeline` while distinguishing proven shared-runtime execution from unproven historical Skill invocation.

## Provenance rule｜2026-09-07

The C04 Yunshuiyi cycle proves shared Blender runtime use, real producer failure, repair, rerun, native reopen, artifact return, and regression hardening. That is sufficient project learning to improve the existing 3D owner and shared preflight.

It does **not** by itself prove that an exact `oleander-3d-pipeline` Skill version was read/selected before the failing producer action. Unless direct pre-execution/in-action Skill provenance is recovered, classify this as:

`PROJECT_LEARNING_EVIDENCE / SHARED_RUNTIME_USAGE_ESTABLISHED / SKILL_FEEDBACK_ORPHAN`

Do not relabel it as historical `PROJECT_USAGE_EVIDENCE` for the Skill solely because the project later improved the Skill.

## Current evidence｜2026-09-07

### C04｜云水倚｜Blender 5.2 producer compatibility

Project object: `C04_YUNSHUIYI_REBUILD_MASTER_v003`

Proven execution facts:
- the existing shared Blender runtime was used;
- the producer was repaired and re-dispatched through the existing durable runner;
- final machine run `33954476037` completed producer execution, native reopen, artifact identity, and artifact upload;
- the returned native artifact still requires independent source-fidelity/design review; machine success does not close the design object.

Actual failures observed during the repair cycle:
1. producer requested the obsolete/unsupported `BLENDER_EEVEE_NEXT` engine token against the Current Blender 5.2 runtime;
2. factory-empty startup left `scene.world` absent, and direct `scene.world.color` mutation failed before the model could be produced.

Actual repair / regression consequence:
- use the Current Blender runtime contract and its bounded producer compatibility preflight before expensive native dispatch;
- under Blender 5.2, do not hard-code stale render-engine identifiers that are rejected by the Current runtime;
- after factory-empty startup, explicitly create/resolve optional scene-owned objects such as `World` before dereferencing them;
- keep producer/runtime compatibility failures local to the job/producer until evidence proves a wider runtime failure;
- after repair, run native reopen/identity checks, then return the same Work Object to independent fidelity/design review.

Shared prevention evidence:
- PR #484 / main merge commit `e57e8442921f4c585e4187eb351234fb19fba8c5` added the bounded Blender 5.2 producer preflight to the existing shared runner;
- the preflight covers safe syntax, the stale Eevee token, and empty-factory World write failure that actually occurred;
- this is a bounded regression guard, not a universal Blender linter.

## Transferable bounded rule

`CURRENT RUNTIME VERSION → BOUNDED PRODUCER PREFLIGHT → DURABLE NATIVE EXECUTION → NATIVE REOPEN / IDENTITY → INDEPENDENT FIDELITY / DESIGN REVIEW`

When a producer fails before artifact creation, classify the smallest real failure domain first:

`SCRIPT / API COMPATIBILITY / SCENE INITIALIZATION / JOB MATERIALIZATION / SHARED RUNTIME`

Do not escalate a script/API or scene-initialization defect to `GLOBAL_RUNTIME_MISSING` without evidence.

## Failure / counterexample

Looks like PASS but is not:
- shared Blender archive exists and resolves, but the producer contains an invalid Current-version API token;
- native `.blend` reopens, but source-defining geometry or relation fidelity is still wrong;
- a preview renders, but the editable master or object identity cannot be reopened/verified;
- CI succeeds because a path was not executed in the real Blender runtime.

## Future Skill usage evidence

For a future real 3D project action to count as `PROJECT_USAGE_EVIDENCE` for `oleander-3d-pipeline`, preserve direct pre-execution/in-action Skill provenance and record:

`PROJECT_ID / OBJECT_ID → SKILL_REF + VERSION/COMMIT → RULE/CAPABILITY_USED → RUNTIME → NATIVE ARTIFACT → ACTUAL READBACK → SUCCESS/FAILURE → ROOT CAUSE → REPAIR/RETEST/HOLD → DOWNSTREAM EFFECT → TRANSFER BOUNDARY → FEEDBACK_ACTION`

A future materially different real project/application may provide cross-project evidence. TRAINING_MODE Practice may add bounded capability evidence but does not count as a second real-project usage. Do not create or distort a project to promote this Skill.

## Boundary

This evidence supports producer-preflight, local failure scoping, and native-return discipline only. It does **not** prove:
- historical use of an exact `oleander-3d-pipeline` version where pre-execution/in-action evidence is absent;
- source/reference fidelity;
- Design KEEP;
- field dimensions;
- engineering/manufacturing approval;
- general compatibility with every Blender API or future Blender version.

Maturity: `PROJECT LEARNING / REAL FAILURE + REPAIR + RETEST / SHARED RUNTIME USE ESTABLISHED / EXACT SKILL USAGE PROVENANCE NOT ESTABLISHED / CROSS-PROJECT TRANSFER NOT YET PROVEN`.
