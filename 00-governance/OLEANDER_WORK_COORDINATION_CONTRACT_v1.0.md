# OLEANDER Work Coordination Contract v1.0

Status: CURRENT ACTIVE GOVERNANCE CONTRACT / MAIN-MERGED / CI + MAIN READBACK VERIFIED.
Evidence: PR #400 → merge commit `1d374d6d8ac1ac468c64758c0cd3b79c01ae8c2c`; AI Governance Evals run #3162 / run ID `33093638477` = `SUCCESS`; main path reopened after merge.
Revision note: 2026-08-29 aligns KNOWLEDGE Cleanup exit criteria with `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.0`; this consumes the existing retrieval mechanism and does not create a second taxonomy, registry, Skill, Gate, or project authority. 2026-08-28 added Training Mode, outcome distillation, anti-repetition and track-specific training focus after review of real Practice evidence.
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

- Maximum `3` ACTIVE project/object slots across automated project production.
- GOVERNANCE alone may add, reorder, pause, or remove queue entries after reading actual project Current State / Source Authority.
- Other workstreams may continue only an existing queue object or explicit Handoff when operating in `PROJECT_MODE`. They must not open a new project/object because it looks interesting.
- If the queue is empty or stale, project production workstreams do not guess. GOVERNANCE refreshes it first.
- User explicit current instruction overrides queue order for that object; GOVERNANCE then updates the queue.
- The Project Priority Queue does **not** disable bounded capability training. Training is governed separately by Section 14.

## 5. Project Control Card

Every actively automated project should maintain one Current control card using:

`00-governance/templates/OLEANDER_PROJECT_CONTROL_CARD_v1.0.md`

The card is a compact control surface, not a replacement for full project state. It records only the current object frontier and handoff state. KEEP ONE CURRENT control card per project.

## 6. Notion knowledge Cleanup exit criteria

`CLEANUP FIRST` is a phase, not the permanent mission of KNOWLEDGE.

This section consumes `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.0`; that Notion mechanism remains the semantic authority for Retrieval Space, Search Eligibility, Trust, Freshness, Canonical Collision and knowledge-lifecycle behavior. This contract only defines when KNOWLEDGE may count an inventoried Current-scope page as cleanup-closed. It must not create a parallel retrieval rule set.

`ACTIVE ≠ VERIFIED ≠ E4 ≠ CURRENT RETRIEVAL`. A page must not count as `CLEAN` merely because its content, Governance state or Evidence state looks correct while Retrieval / Trust / Freshness / migration relations remain unresolved.

For a page to count as `CLEAN`, all applicable checks must be resolved:

1. Content Identity known.
2. Canonical ID is unambiguous; Canonical parent/path known; Current hierarchy uses `Canonical Parent / Canonical Children`, not legacy parent/child fields.
3. Knowledge Role and valid Domain / L0–L7 position known; Application Mapping and Knowledge Type do not substitute for taxonomy depth.
4. Governance / Authority State known.
5. Evidence State known.
6. `Retrieval Space` explicitly resolved as `CURRENT / SUPPORT / PROVENANCE / EXCLUDED` according to the Current retrieval mechanism.
7. `Search Eligibility` explicitly resolved as `DEFAULT / SCOPED / HISTORY_ONLY / BLOCKED` and does not conflict with Retrieval Space.
8. `Trust State` explicitly resolved as `VERIFIED / UNVERIFIED / UNKNOWN`; `ACTIVE` or high Evidence does not auto-grant VERIFIED.
9. Freshness resolved: stable knowledge may be non-expiring; time-sensitive standards, software, prices, platform capability, regulation or supply claims have current verification/readback and an applicable revalidation boundary.
10. Current / Support / Practice / Provenance / Legacy / Superseded and redirect/supersession relationships are known; Current and Provenance do not compete in the same default retrieval pool.
11. Duplicate relationship and Canonical Collision resolved or explicitly HOLD; one Canonical ID must not have two `ACTIVE + CURRENT/DEFAULT` carriers.
12. Migration Closure resolved: legacy hierarchy fields, old taxonomy residue, stale Current-like labels and deprecated locations do not drive Current retrieval or hierarchy; unresolved migration drift is explicitly OPEN/HOLD.
13. Relation Closure resolved: Canonical Parent/Children, Domain, Source, Method, Project and supersession relations point to the correct semantic owners; generic `相关笔记` or Application Mapping does not replace hierarchy.
14. Prompt/chat/runtime/CI/AI-summary pollution removed or re-homed without information loss.
15. Broken references and orphan relations resolved or explicitly OPEN.
16. Human Professional Voice readback completed where applicable.
17. Actual page fetch/readback agrees with database properties and Current relation state; index/listing metadata alone is not sufficient closure evidence.

A page with clean prose but unresolved migration or relation integrity is recorded as `CONTENT_CLEAN / MIGRATION_OPEN`, `CONTENT_CLEAN / RELATION_OPEN`, or the applicable HOLD state; it is not counted as fully `CLEAN`.

Phase transition:

- `<70%` of reviewed Current-scope pages clean → `CLEANUP_HEAVY`.
- `70–90%` → `BALANCED`.
- `>90%` with no unresolved Authority, Canonical Collision, Retrieval, migration or relation blocker in the inventoried Current-scope denominator → `KNOWLEDGE_HEAVY`.

Percentages apply only to pages actually inventoried into the Current cleanup scope; do not fabricate a denominator from the whole workspace, and do not count unreviewed historical Notes as clean by inference.

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