# OLEANDER Work Coordination Contract v1.0

Status: CURRENT ACTIVE GOVERNANCE CONTRACT / MAIN-MERGED / CI + MAIN READBACK VERIFIED.
Evidence: PR #400 → merge commit `1d374d6d8ac1ac468c64758c0cd3b79c01ae8c2c`; AI Governance Evals run #3162 / run ID `33093638477` = `SUCCESS`; main path reopened after merge.
Revision note: 2026-09-04 adds `REPAIR-FIRST / REGISTER-LAST` to PROJECT_MODE: an executable defect may not end as a status-only HOLD/OPEN when the Current owner has a legal repair path. The 2026-09-03 durable execution-plane, enabled-state/lease separation and staggered-cadence rules remain in force. This is an implementation revision of the existing coordination contract; it does not create a new Skill, Gate, framework or project authority.
Role: cross-project coordination contract; not a new Design Method, Skill, Gate, or project Source Authority.

## Purpose

Coordinate the five Current OLEANDER workstreams so they operate as one design-office workflow rather than five independent agents.

`GOVERNANCE → KNOWLEDGE → DESIGN → VALIDATION → PRESENTATION → feedback to DESIGN / project Current`

The order is logical ownership, not a requirement that every object visit every stage. Use the minimum sufficient owner set.

## 1. Current automation cadence and collision prevention

The five Current tasks remain enabled as recurring **GPT control-plane owners** and are deliberately staggered in UTC+08:00:

- `GOVERNANCE` — hourly at `:05`.
- `KNOWLEDGE` — hourly at `:15`.
- `DESIGN` — hourly at `:25`.
- `VALIDATION` — hourly at `:36`.
- `PRESENTATION` — hourly at `:55`.

Old `SUPERSEDED` or disabled legacy tasks must remain disabled unless explicitly re-authorized.

A Current task being `enabled` means the owner is available at its scheduled wake-up. **Enabled state is not a project lease.** If no eligible Work Object/lease exists, the task returns `::SKIP_COMPLETION::`; it does not disable itself. A Current recurring task may be disabled only by explicit user pause, supersession, or a governance-confirmed global destructive-write/migration freeze that cannot be isolated through leases.

A task must not write to a logical object currently owned by another task unless it is accepting an explicit Handoff or a bounded concurrent subtask lease on a distinct child item. If concurrent ownership is detected on the same mutable artifact, the later task must HOLD the write and report the collision to GOVERNANCE.

### 1A. Hourly GPT control plane and durable execution plane

The hourly recurrence limit applies to GPT judgment turns, not to already-dispatched native computation.

Control-plane responsibility:

`READ CURRENT → RESOLVE OBJECT/LEASE → PROFESSIONAL JUDGMENT → DISPATCH OR CONSUME → UPDATE/RETURN STATE`

Execution-plane responsibility:

`RESOLVE RUNTIME → RUN NATIVE TOOL → SAVE NATIVE ARTIFACT → PREVIEW/RENDER → REOPEN/ROUNDTRIP → HASH/IDENTITY → PACKAGE/ARTIFACT`

Rules:

- use the Current Universal Production Environment and approved shared runner/runtime for deterministic execution;
- once a durable runner is dispatched, let it finish the deterministic chain available in that job without waiting for another GPT wake-up;
- do not split build/save/render/reopen/hash/package into separate hourly GPT turns merely because GPT recurrence is hourly;
- a runner still in progress at the next owner's wake-up is `WAITING_FOR_EXECUTION_RESULT`, not failure; leave the typed lease intact and SKIP mutation;
- new design/fidelity/Source Authority judgment remains an owner gate and must not be automated away by a runner;
- project progress advances only on persisted artifact/readback state, not because a scheduled task ran;
- GOVERNANCE advances or returns the queue cursor only after actual artifact/handoff readback.

Canonical coordination pattern:

`GPT OWNER → DURABLE RUNNER → PERSISTENT ARTIFACT/RECEIPT → NEXT GPT OWNER`

### 1B. PROJECT_MODE repair-first / register-last

In PROJECT_MODE, discovering a defect is not a completed project action when the Current owner has a legal, executable repair path.

Canonical repair loop:

`READ CURRENT → DIAGNOSE → RESOLVE LEGAL REPAIR PATH → EXECUTE REPAIR → RETEST / REOPEN / BROWSER READBACK → WRITE CURRENT STATE → HANDOFF / NEXT`

Hard rules:

- **REPAIR-FIRST / REGISTER-LAST**: if the defect can be repaired with the currently available connector, approved runtime/runner, repository write frontier, editable native master, or legal bounded handoff, the owner must perform at least one actual repair attempt in the same run before it may end on `HOLD`, `OPEN`, `BLOCKED`, `NEXT_ACTION`, or a status-only record;
- merely writing a blocker, Queue note, Control Card note, receipt, comment, issue, or `NEXT` field is not material project completion when an executable repair is available;
- after a repair attempt, the owner must perform the smallest relevant retest/readback. A write without readback is `REPAIR_UNCONFIRMED`, not completion;
- if the first repair fails and the failure is diagnosable within the same legal owner/tool boundary, inspect the actual failure evidence and make the smallest justified repair/retest rather than converting immediately to a passive HOLD;
- use `HOLD/OPEN/BLOCKED` as the terminal state only when the current run has reached a genuine boundary: missing Source Authority or required bytes, unavailable/failed Current capability after allowed carriers are exhausted, user-exclusive action/credential, external service condition, safety/rights/destructive-write boundary, unresolved same-artifact ownership collision, or a professional gate that requires evidence that does not yet exist;
- when a genuine boundary exists, record **what was actually attempted**, **what failed or is unavailable**, **the exact boundary**, and **what evidence/action would release it**. Do not record a generic blocker where a concrete cause is known;
- runtime/CI/persistence success does not excuse unresolved design, fidelity, browser-pixel, source-binding or project-state defects that remain legally repairable by their owner;
- if a defect belongs to another owner, the current owner must create/return the explicit typed handoff with the failing artifact/evidence. It must not silently mark the object HOLD and leave the legal repair unowned;
- GOVERNANCE must treat repeated `HOLD/OPEN/NEXT_ACTION` with no repair attempt despite an available legal path as `PASSIVE_REGISTRATION_DRIFT` and repair the routing/lease/state, not normalize the drift;
- scheduled wake-up, diagnosis, registration and planning alone do not count as material delta.

This rule does not require unsafe guessing, destructive edits without authority, invented source data, fake field evidence, or bypassing professional approval gates. It requires execution up to the first genuine boundary.

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

- Maximum `3` ACTIVE project/object slots across automated project production.
- GOVERNANCE alone may add, reorder, pause, or remove queue entries after reading actual project Current State / Source Authority.
- Other workstreams may continue only an existing queue object or explicit Handoff when operating in `PROJECT_MODE`. They must not open a new project/object because it looks interesting.
- If the queue is empty or stale, project production workstreams do not guess. GOVERNANCE refreshes it first.
- User explicit current instruction overrides queue order for that object; GOVERNANCE then updates the queue.
- The Project Priority Queue does **not** disable bounded capability training. Training is governed separately by Section 14.
- Queue/lease state and recurring automation enabled state are separate. A lease may be `RETURNED/HOLD` while the recurring owner remains enabled for another object or a later handoff.
- Sequential child-item production must carry an explicit cursor/current-item identity when more than one child is queued, so one item's `RETURNED` state cannot silently block the next child.

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

## 14. Project Mode vs Training Mode

The five recurring tasks have two operating modes. They must be distinguished before any material write.

### 14.1 PROJECT_MODE

Use when at least one is true:

- a Work Object is present in `OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json` and owned by the task;
- an explicit Handoff has been accepted;
- the user's current instruction names or clearly identifies a project/object.

PROJECT_MODE may modify the actual project frontier after reading Current State / Source Authority. It must use the stable `PROJECT_ID / OBJECT_ID`, Current native master and normal Handoff rules.

### 14.2 TRAINING_MODE

Use when no eligible project Work Object exists but the scheduled task still has a verified capability/quality gap worth practicing.

TRAINING_MODE rules:

- queue emptiness is **not** a reason to stop all training;
- select a bounded Practice object from an existing Skill/Practice gap, recent failure, Candidate evidence gap or explicitly rotating professional domain;
- use real professional references or verified standards first; synthetic/neutral exercise material is allowed only when clearly marked and when it does not pretend to be project truth;
- training writes only to Practice / Candidate evidence / knowledge surfaces or a dedicated training frontier;
- training must not silently mutate a project Current, Source Authority, production master or production PR;
- project re-application is optional and only permitted when a real queued/explicit project object is available; otherwise record a transfer rule, not an invented project patch;
- project-specific source bytes may be used for bounded Practice only when authority permits; the training derivative remains SUPPORT / PRACTICE unless explicitly handed back into project production;
- all normal Evidence Gate / Design Quality Gate / Human Professional Voice / non-proof boundaries remain in force.

If neither a project object nor a material training gap exists, return `::SKIP_COMPLETION::`.

## 15. Training Outcome Ladder and evidence distillation

Training progress is evaluated by evidence maturity, not number of runs or page length.

`OBSERVATION → PRACTICE_EVIDENCE → CROSS_CONTEXT_EVIDENCE → PROJECT_USAGE_EVIDENCE → VALIDATED_CANDIDATE → ACTIVE`

Definitions:

- `OBSERVATION` — useful precedent or visible fact; no reusable claim yet.
- `PRACTICE_EVIDENCE` — an actual editable/inspectable exercise with A/B or attack, readback and at least one explicit failure condition.
- `CROSS_CONTEXT_EVIDENCE` — the same bounded rule survives a materially different medium, object, scale or project context; mere repetition does not count.
- `PROJECT_USAGE_EVIDENCE` — the rule/Skill changes a real project object and records downstream consequence, failure/repair and residual HOLD.
- `VALIDATED_CANDIDATE` — the claimed reusable capability has sufficient diverse usage/readback and the applicable existing review requirements are satisfied; this still does not automatically mean ACTIVE.
- `ACTIVE` — only through the existing explicit promotion authority and independent review requirements.

`M6 PRACTICED`, `E2`, CI success, producer pixel readback, one good A/B or one project application must never be translated automatically into ACTIVE.

### 15.1 One training run = one compact evidence record

A material training run should be reducible to:

`GAP → EXISTING-FIRST SOURCE → ARTIFACT → A/B OR ATTACK → READBACK → FAILURE/ROOT CAUSE → REPAIR/RETEST → TRANSFER RULE → BOUNDARY → STATUS`

Detailed commands, repeated process-integrity boilerplate, duplicated Current rules, repeated CI status and long narrative chronology belong in Evidence History / Validation Ledger / K06 when they are needed for audit. They do not belong in the Current reusable rule surface.

### 15.2 Thin Current Practice rule

A Current Practice page should make the reusable rule readable without mining old run logs. Its effective top layer should contain only:

- Current rule / capability claim;
- Trigger / when to use;
- professional workflow or technique;
- failure symptoms + at least one counterexample;
- transfer boundary / non-proof;
- 1–3 strongest evidence links;
- current maturity/status;
- next missing evidence required for promotion.

Historical extensions remain preserved, but once their rule is absorbed into the Current top layer they should not remain the only place where the rule can be discovered. A page labelled `Thin L7 index` must not continue growing as an unlimited chronological superpage.

### 15.3 Anti-repetition

Before a new training exercise, read the last relevant 3 evidence entries or the Current Practice summary.

Repeat a topic only when one of these is true:

- previous run failed and a materially different repair/retest is needed;
- a new context attacks the transfer boundary;
- a new professional source changes the method;
- a project application exposes a new failure;
- an explicit review/promotion evidence gap remains.

Changing only the reference case, color, project name or surface styling is not a new training delta.

## 16. Track-specific training focus

The five tasks do not train the same thing.

### 16.1 PRESENTATION

Primary question: `Does the final visible artifact reach professional publication quality?`

Train and retain evidence around:

- first-read / dominant field / hierarchy;
- grid versus hierarchy: grid orders relations, visual mass argues priority;
- typography, measure, spacing and read-distance behavior;
- crop, figure-ground, localized image anchor, image-text relation and responsive art direction;
- packaging face-specific reading: front `IDENTIFY + CHOOSE`, side `HANDLE + USE`, back `VERIFY + TRACE` when source/brief supports those roles;
- controlled premiumity without decorative luxury or fake finish;
- Web/UI visual hierarchy, responsive final pixels, state/feedback presentation;
- motion hierarchy and settled-state visual continuity;
- final multi-size / thumbnail / grayscale / far-near readback;
- cross-media consistency and Project Voice Profile.

Do not turn every successful visual observation into a new Skill. Prefer strengthening the existing Candidate/installed owner with evidence.

### 16.2 DESIGN

Primary question: `How does evidence become a design decision?`

Train and retain evidence around:

- Evidence → Finding → Design Consequence;
- site / audience / behavior / route / service / system relationships;
- causal sequence and relation diagrams that do not collapse into equal-card grammar;
- spatial organization, massing, section, threshold, circulation and option comparison;
- product requirement → function → part role → proportion → form → structure → material → interaction;
- form proof before finish / atmosphere;
- role-bound CMF reasoning before decorative finish choice;
- IA / user flow / state model / storyboard as design structure, not final polish;
- deletion tests, adverse-condition tests and rejected alternatives;
- explicit Handoff generation when technical or presentation ownership begins.

### 16.3 VALIDATION

Primary question: `Does the same design object actually survive the real medium/toolchain/interface?`

Train and retain evidence around:

- exact source/native master/model identity;
- units / scale / axis / dimensions / geometry authority;
- reopen / roundtrip / format semantics;
- native browser width, overflow, keyboard/focus and responsive behavior;
- settled interaction states, not transition screenshots;
- same-object view continuity;
- fail-closed missing source, poster/fallback/load/error behavior;
- exact view ↔ evidence binding, or explicit `UNBOUND` rather than fake completeness;
- packaging/prepress/color/profile/print constraints when relevant;
- Candidate runtime proof boundaries;
- explicit `PROVEN / NOT PROVEN` for field, engineering, Class-A, machine safety, physical sample, proprietary native format and specialist finishing.

### 16.4 KNOWLEDGE

Primary question: `What professional knowledge should become reusable Current knowledge rather than another run log?`

Train/maintain:

- one-page-at-a-time Cleanup First;
- source/version/scope/evidence classification;
- external knowledge and Skill digestion rather than collection;
- Type Brief completion only when a real Design/Presentation/Validation gap exposes missing type knowledge;
- repeated Practice findings distilled into concise Current rules;
- project experience prevented from silently becoming universal law;
- thin indexes and explicit Evidence History separation;
- honest cleanup denominator and phase transition.

### 16.5 GOVERNANCE

Primary question: `Is training producing stronger reusable capability without creating more system noise?`

Monitor:

- PROJECT_MODE versus TRAINING_MODE routing;
- stalled training caused by an empty project queue;
- Practice superpage growth and duplicate extensions;
- Candidate evidence coverage across materially different contexts;
- Usage Evidence completeness;
- old evidence already absorbed into Current rules;
- orphan handoffs and project write leakage from training;
- no-churn, consolidation and one-owner integrity;
- whether a new run actually advances the Training Outcome Ladder.

A run that only increases page length, CI count, case count or terminology without advancing reusable evidence should be treated as `NO MATERIAL TRAINING DELTA`.