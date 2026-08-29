# OLEANDER Project Control Card v1.0

> Compact Current control surface. This card does not replace full Project State or Source Authority. KEEP ONE CURRENT per project.

- `PROJECT_ID`:
- `PROJECT_NAME`:
- `CURRENT_OBJECT_ID`:
- `OBJECT_TYPE`:
- `CURRENT_OWNER`: KNOWLEDGE / DESIGN / PRESENTATION / VALIDATION / GOVERNANCE
- `STATE`: ACTIVE / HANDOFF_READY / IN_REVIEW / REVISE / HOLD / CLOSED
- `SOURCE_AUTHORITY`:
- `UPSTREAM_MASTER`:
- `CURRENT_NATIVE_MASTER`:
- `CURRENT_PR_FRONTIER`:
- `CURRENT_MATERIAL_DELTA`:
- `NEXT_OWNER`:
- `NEXT_ACTION`:
- `RESIDUAL_HOLD`:
- `VOICE_PROFILE_REF`:
- `COPY_CLASS`: PUBLIC_COPY / INTERNAL_DESIGN_COPY / MACHINE_COPY / MIXED_WITH_EXPLICIT_SEGMENTATION
- `LAST_READBACK`:
- `UPDATED_AT`:

## Handoff

- `FROM_OWNER`:
- `TO_OWNER`:
- `WHAT_CHANGED`:
- `WHAT_MUST_BE_CHECKED_OR_CHANGED_NEXT`:
- `REQUIRED_NATIVE_OUTPUT`:
- `DIMENSION_GEOMETRY_AUTHORITY`:
- `KNOWN_ASSUMPTIONS`:
- `HANDOFF_STATE`: NONE / READY / ACCEPTED / RETURNED_REVISE / RETURNED_HOLD / CLOSED

## Existing-project repair execution integrity

Use only when the same logical object is being continued/repaired under `oleander-design-process/EXISTING_PROJECT_REPAIR_EXTENSION.md`.

- `EXECUTION_MODE`: STANDARD / EXISTING_PROJECT_REPAIR
- `BEST_EXISTING_ARTIFACT_ID`:
- `BEST_EXISTING_REF`:
- `ROLLBACK_REF`:
- `PRESERVE_DIMENSIONS`:
- `RUN_ID`:
- `PRODUCER_OWNER`:
- `SKILL_REFS`:
- `RUN_INPUTS`: artifact_id + digest + location
- `RUN_OUTPUTS`: artifact_id + digest + location
- `ARTIFACT_DELTA_STATE`: NONE / MATERIAL
- `CHANGED_ARTIFACT_IDS`:
- `AUTHORITY_BINDING_CHANGED`: true / false
- `READBACK_STATE`: NOT_RUN / PASS / FAIL / HOLD
- `READBACK_MEDIUM`:
- `READBACK_ARTIFACT_IDS`:
- `DEPENDENCY_EDGES`: input_artifact_id + current_input_digest + consumed_input_digest + output_artifact_id + output_status
- `CHANGE_IMPACT`: artifact_id + DIRECT/INDIRECT + required action + OPEN/DONE/HOLD/N_A
- `RECEIVER_MASTER_REF`:

Fail-closed transition rule:

`HANDOFF READY|ACCEPTED|CLOSED → MATERIAL DELTA + RUN OUTPUT + REAL READBACK PASS + VALID OWNER TRANSFER + NEXT CHECK`

Stale rule:

`CURRENT INPUT DIGEST ≠ CONSUMED INPUT DIGEST → OUTPUT ≠ CURRENT`

Use `STALE / REGEN_REQUIRED / RETEST_REQUIRED / HOLD` until the dependency is regenerated/retested or explicitly held.

Closure rule:

`CLOSED` is forbidden while required change-impact items or dependency edges remain unresolved.

This block records execution integrity only. It does not grant Design KEEP, technical PASS, browser PASS, Field PASS or release authority.

## Project Voice Profile

- `SPEAKER`:
- `AUDIENCE`:
- `MEDIUM`:
- `SENTENCE_LENGTH_TENDENCY`:
- `PROFESSIONAL_DENSITY`:
- `EMOTIONAL_RANGE`:
- `TITLE_PATTERN`:
- `PRESERVE_TERMS`:
- `AVOID_TERMS_OR_STRUCTURES`:
- `POSITIVE_SAMPLE`:
- `REJECT_SAMPLE`:

## Usage evidence attached to this object

For any Candidate Skill used materially:

`SKILL + VERSION → ACTUAL ARTIFACT → SUCCESS/FAILURE → ROOT CAUSE → REPAIR/RETEST → DOWNSTREAM EFFECT → TRANSFER BOUNDARY → HOLD`
