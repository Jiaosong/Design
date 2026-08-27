# OLEANDER Work Coordination Contract v1.0

Status: CURRENT ACTIVE GOVERNANCE CONTRACT / MAIN-MERGED / CI + MAIN READBACK VERIFIED.
Evidence: PR #400 → merge commit `1d374d6d8ac1ac468c64758c0cd3b79c01ae8c2c`; AI Governance Evals run #3162 / run ID `33093638477` = `SUCCESS`; main path reopened after merge.
Role: cross-project coordination contract; not a new Design Method, Skill, Gate, or project Source Authority.

## Purpose

Coordinate the five Current OLEANDER workstreams so they operate as one design-office workflow rather than five independent agents.

`GOVERNANCE → KNOWLEDGE → DESIGN → PRESENTATION → VALIDATION → feedback to DESIGN / project Current`

The order is logical ownership, not a requirement that every object visit every stage. Use the minimum sufficient owner set.

## 1. Current automation cadence and collision prevention

The five Current tasks must remain enabled and deliberately staggered in Asia/Singapore / UTC+08:00:

- `GOVERNANCE` — hourly at `:05`.
- `KNOWLEDGE` — every 2 hours at `:15`.
- `DESIGN` — hourly at `:25`.
- `PRESENTATION` — hourly at `:40`.
- `VALIDATION` — every 2 hours at `:55`.

Old `SUPERSEDED` or disabled legacy tasks must remain disabled unless explicitly re-authorized.

A task must not write to a logical object currently owned by another task unless it is accepting an explicit Handoff. If concurrent ownership is detected, the later task must HOLD the write and report the collision to GOVERNANCE.

## 2. Work Object identity

Every material project action must resolve one Work Object before editing. Minimum fields:

- `PROJECT_ID`
- `OBJECT_ID`
- `OBJECT_TYPE`
- `CURRENT_OWNER` = KNOWLEDGE / DESIGN / PRESENTATION / VALIDATION / GOVERNANCE
- `UPSTREAM_MASTER`
- `SOURCE_AUTHORITY`
- `CURRENT_NATIVE_MASTER`
- `CURRENT_PR_FRONTIER` or other canonical write frontier
- `STATE` = ACTIVE / HANDOFF_READY / IN_REVIEW / REVISE / HOLD / CLOSED
- `NEXT_OWNER`
- `NEXT_ACTION`
- `RESIDUAL_HOLD`

Do not invent a new Object ID for a revision of the same logical object. Version, commit, page, render, export, validation artifact, and presentation derivative remain children/versions of the same Object ID unless the design scope materially changes.

## 3. Handoff contract

A handoff is valid only when it identifies the same Work Object and includes enough information for the receiver to continue without re-interpreting the project from scratch.

Required handoff fields:

- `PROJECT_ID / OBJECT_ID`
- `FROM_OWNER / TO_OWNER`
- `UPSTREAM_MASTER`
- `CURRENT_NATIVE_MASTER`
- `REQUIRED_NATIVE_OUTPUT` when applicable
- `SOURCE / DIMENSION / GEOMETRY AUTHORITY`
- `KNOWN_ASSUMPTIONS`
- `WHAT_CHANGED`
- `WHAT_MUST_BE_CHECKED_OR_CHANGED_NEXT`
- `CURRENT_PR_FRONTIER`
- `RESIDUAL_HOLD`

A receiver must read the upstream master before editing. A returned `REVISE/HOLD` must be attached to the same Object ID. `HANDOFF SENT ≠ HANDOFF CLOSED`.

GOVERNANCE checks for orphan handoffs: sent but not accepted, validation requiring a design repair that never returned to DESIGN, presentation changes not reflected in the Current master, or changed master without downstream re-readback.

## 4. Project Priority Queue

The single machine-readable queue is:

`00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json`

Rules:

- Maximum `3` ACTIVE project/object slots across automated work.
- GOVERNANCE alone may add, reorder, pause, or remove queue entries after reading actual project Current State / Source Authority.
- Other workstreams may continue only an existing queue object or explicit Handoff. They must not open a new project/object because it looks interesting.
- If the queue is empty or stale, production workstreams do not guess. GOVERNANCE refreshes it first.
- User explicit current instruction overrides queue order for that object; GOVERNANCE then updates the queue.

## 5. Project Control Card

Every actively automated project should maintain one Current control card using:

`00-governance/templates/OLEANDER_PROJECT_CONTROL_CARD_v1.0.md`

The card is a compact control surface, not a replacement for full project state. It records only the current object frontier and handoff state. KEEP ONE CURRENT control card per project.

## 6. Notion knowledge Cleanup exit criteria

`CLEANUP FIRST` is a phase, not the permanent mission of KNOWLEDGE.

For a page to count as `CLEAN`, all applicable checks must be resolved:

1. Content Identity known.
2. Canonical parent/path known.
3. Knowledge Role known.
4. Authority State known.
5. Evidence State known.
6. Current / Support / Practice / Provenance / Legacy / Superseded relationship known.
7. Duplicate relationship resolved or explicitly HOLD.
8. Prompt/chat/runtime/CI/AI-summary pollution removed or re-homed without information loss.
9. Broken references and orphan relations resolved or explicitly OPEN.
10. Human Professional Voice readback completed.

Phase transition:

- `<70%` of reviewed Current-scope pages clean → `CLEANUP_HEAVY`.
- `70–90%` → `BALANCED`.
- `>90%` with no unresolved Authority blocker in Current-scope pages → `KNOWLEDGE_HEAVY`.

Percentages apply only to pages actually inventoried into the Current cleanup scope; do not fabricate a denominator from the whole workspace.

## 7. External Skill / Knowledge digestion

Existing Skill / Existing Knowledge First remains mandatory, but discovery is not adoption.

External resource sequence:

`DISCOVER → SOURCE CHECK → CAPABILITY MAPPING → COMPARE TO CURRENT OLEANDER → EXTRACT → ADAPT / COMPOSE / WRAP → BOUNDED PROJECT TEST → READBACK → KEEP / REJECT / HOLD`

Required comparison fields:

- source / author / version / maintenance state
- license / rights
- capability coverage
- inputs / outputs / dependencies
- native output fit
- evidence quality
- known failure / false-positive / false-negative conditions
- conflict with OLEANDER Authority
- reusable portion
- non-transferable portion

If an existing mature resource covers approximately `60%+` of the needed capability, default to extension/adapter/composition rather than parallel reimplementation.

## 8. Candidate Skill Usage Evidence

A Candidate Skill cannot advance on explanation, CI, Golden Cases, or one successful smoke alone.

Maintain Usage Evidence for real project applications:

- `PROJECT_ID / OBJECT_ID`
- skill/version
- actual owner/runtime
- native artifact
- success
- failure
- root cause
- repair/retest
- downstream effect
- transfer boundary
- unresolved HOLD

Promotion evidence should include more than one materially different project/application when the Skill claims cross-project reuse. Producer self-review still cannot grant Independent KEEP.

## 9. Project Voice Profile and Copy Classes

Human Professional Voice is a constraint against AI-like language, not one universal OLEANDER tone.

Each active project may define a lightweight `VOICE_PROFILE`:

- speaker / institutional voice
- audience
- medium
- sentence length tendency
- professional density
- acceptable emotional range
- title pattern
- terms to preserve
- terms/structures to avoid
- one positive sample and one reject sample from the project itself

Every material text object also declares one Copy Class:

- `PUBLIC_COPY` — audience-facing; project-specific, concise, human professional voice.
- `INTERNAL_DESIGN_COPY` — studio working language; can use design shorthand but not chat residue or vague AI summaries.
- `MACHINE_COPY` — IDs, hashes, paths, tokens, PASS/REVISE/HOLD, schemas; preserve exact machine semantics.

Do not rewrite MACHINE_COPY to sound human. Do not expose INTERNAL process labels as PUBLIC_COPY unless the project explicitly uses them as content.

## 10. Reporting noise and Current pollution

Scheduled tasks report only material delta. Current surfaces keep concise effective state; detailed training history, smoke logs, validation traces, repeated review evidence, and process logs go to Practice / Validation Ledger / K06 or equivalent history surfaces.

Default completion summary is limited to:

`OBJECT → MATERIAL DELTA → ACTUAL REPAIR/RESULT → READBACK → HOLD → NEXT OWNER/ACTION`

No material delta → `::SKIP_COMPLETION::`.

## 11. NO-CHURN

Do not modify Skill, Method, Policy, Runtime, Registry, taxonomy, schedule, or project structure merely because another run occurred.

A governance/framework change requires at least one material trigger:

- new real failure or blocker;
- new project application evidence;
- external standard/tool/version change that affects behavior;
- source/authority conflict;
- repeated responsibility collision;
- duplication/pollution discovered;
- measurable quality regression;
- user explicit instruction.

`NO MATERIAL DELTA = NO COMMIT`.

## 12. Consolidation

Consolidation is continuous and event-driven; do not create another recurring task solely for it.

GOVERNANCE reviews consolidation when any trigger appears:

- overlapping Skill ownership;
- Candidate unused across a meaningful review window;
- market Skill/knowledge now supersedes a weaker OLEANDER implementation;
- duplicate runtime/wrapper/validator;
- repeated routing confusion;
- more than one Current object for the same logical responsibility.

Actions: KEEP / MERGE / COMPOSE / REDIRECT / DEPRECATE / SUPERSEDE / HOLD. Preserve provenance and information; never bulk-delete by name similarity.

## 13. Non-proof boundaries

This coordination contract does not prove design quality, engineering approval, field truth, manufacturing safety, independent review, or Candidate promotion. It coordinates ownership and continuity only.
