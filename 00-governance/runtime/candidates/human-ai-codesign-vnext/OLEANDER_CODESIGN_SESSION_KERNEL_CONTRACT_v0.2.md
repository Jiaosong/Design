# OLEANDER Co-Design Session Kernel Contract v0.2 — CANDIDATE

**Role:** executable Human–AI Co-Design interaction kernel for the vNext candidate.  
**Machine spec:** `OLEANDER_CODESIGN_SESSION_KERNEL_SPEC_v0.2.json`.  
**Ephemeral context schema:** `OLEANDER_CODESIGN_SESSION_CONTEXT_EPHEMERAL_v0.4.schema.json`.  
**Reference runtime:** `codesign_session_kernel_v0_2.py`.  
**Not:** Authority, Project State, professional process, artifact registry, preference database, persistence store, independent reviewer or Promotion owner.

v0.2 keeps the v0.1 operating model but makes the interaction kernel deterministic enough to test. Its main correction is to stop treating one natural-language message as one monolithic `intent`. A message can simultaneously mean **continue the work**, **do not mutate**, and **explain less** without becoming Human design steering.

## 1. Two coupled kernels, one session

### Visible design kernel

`UNDERSTAND → EXPLORE → MAKE → LOOK → CRITIQUE → STEER → LEARN`

### Quiet runtime kernel

`RESOLVE → RESUME → ROUTE → GUARD → HANDOFF → REPORT`

The design kernel drives the experience. The runtime kernel keeps the session attached to Current OLEANDER authority, state, native artifact and review owners.

The kernel is a **persistent interaction concept**, not a persistent state store.

## 2. Four-axis interaction model

v0.1 used one `intent` enum for several different kinds of user instruction. v0.2 separates four independent axes.

### 2.1 Work intent

What useful work is requested:

`START / RESUME / RECOVER / EXPLORE / WILDCARD / REVIEW / REFRAME / SAVE_ROUTE / EXPLAIN / SHOW_WORK / UNRESOLVED`.

### 2.2 Mutation directive

What the session may change:

`NORMAL / READ_ONLY / AUTO_ADVANCE_REVERSIBLE`.

Examples:

- `只读继续检查` = `RESUME + READ_ONLY`;
- `直接做，真正需要我决定时再问` = current work intent + `AUTO_ADVANCE_REVERSIBLE`;
- `继续并完成整个任务` = `RESUME`, **not** `DEFER`, `SELECT` or any other design steer.

### 2.3 Support mode

How much designer-development/explanatory support to expose:

`AUTO / COMPACT / EXPLAIN / OFF`.

This is display/support behavior only. It has no effect on authority, project maturity or the user's competence status.

### 2.4 Human action level

What kind of Human input, if any, occurred:

`NONE / FEEDBACK_SIGNAL / ITERATION_STEER / DESIGN_DECISION / DESIGN_KEEP / PROMOTION_DECISION`.

These levels must never collapse.

`FEEDBACK_SIGNAL ≠ ITERATION_STEER ≠ DESIGN_DECISION ≠ DESIGN_KEEP ≠ PROMOTION_DECISION`.

The Session Kernel may classify all five non-`NONE` levels, but it may routinely apply only `FEEDBACK_SIGNAL / ITERATION_STEER` behavior. Explicit `DESIGN_DECISION / DESIGN_KEEP / PROMOTION_DECISION` signals must be preserved and routed respectively to the existing project-decision, design-review and promotion authorities; the Session Kernel never upgrades them into authority it owns and never applies them as an iteration branch mutation.

## 3. Human steering classifier

Valid next-round Human design actions remain:

`SELECT / MODIFY / MIX / REJECT / REOPEN / DEFER`.

The reference classifier must obey these invariants. One message may contain **multiple clause-scoped Human actions**; do not collapse `不要 A，保留 B，结合 C` into one synthetic action.

1. Generic `继续 / 接着 / finish the whole task` is execution intent, not iteration steer.
2. Silence or failure to reject is never selection.
3. `DEFER` requires an explicit defer signal plus a resolvable pending decision. Generic continuation cannot become defer.
4. `MIX` requires at least two resolvable parent referents.
5. `SELECT / MODIFY / REJECT / REOPEN` require an explicit or unambiguous active referent. If ambiguous, ask one minimum referent question and do not mutate the design as though a steer occurred.
6. `这个不对 / 太像展馆 / 感觉碎` is normally a `FEEDBACK_SIGNAL`. It may generate causal hypotheses and materially different repair directions; it does not become a durable preference.
7. One project choice never creates a global taste/personality/ability profile.
8. Single-letter option aliases such as `A/B/C` are explicit labels, not case-insensitive natural-language tokens; English `a` must never silently bind option A.
9. A consequential `ITERATION_STEER` is not applicable until its referent is typed and revision-resolved. An explicit label with unresolved owner-native revision remains a fail-closed feedback signal until binding resolves.
10. If `DEFER` names a branch rather than the decision object itself, that branch must prove membership in the current pending decision object; an unrelated active branch cannot defer a different decision.

### 3.1 Referent binding

Every consequential steer carries one of:

`EXPLICIT / UNAMBIGUOUS_ACTIVE_OBJECT / AMBIGUOUS / NOT_APPLICABLE`.

Only the first two can authorize an `ITERATION_STEER` transition. Consequential referents must resolve to a typed binding:

`REF + KIND + REVISION + LINEAGE_REF`.

The shorthand label shown to the Human may remain `A/B/C`, but mutation/readback proof must bind the owner-native option/object revision rather than a floating display label. A branch binding may additionally carry its `decision_object_ref` when that relationship is needed to prove `DEFER` scope.

Examples:

- `选 B` with A/B/C visible → explicit SELECT B;
- `就按这个` when one candidate is clearly active → unambiguous SELECT;
- `就按这个` while two candidates are simultaneously active → ambiguous; ask the minimum question;
- `保留 A，结合 B` → MIX with both parent refs;
- `这个决定先暂缓` when one pending decision is resolved → DEFER that decision;
- `继续` → no steer.

## 4. Ephemeral session phases

The kernel may use the following **ephemeral execution positions**:

`RESOLVING → WORKING_REVERSIBLE → COMPARISON_BUILDING → COMPARISON_READY → AWAITING_HUMAN_STEER → STEER_BOUND → MUTATION_GUARD → MAKING → READBACK_REQUIRED → REVIEW_REQUIRED → HANDOFF_READY → SESSION_COMPLETE`

with HOLD positions:

`HOLD_AUTHORITY / HOLD_CHECKPOINT / HOLD_PERMISSION / HOLD_NATIVE_SURFACE / HOLD_DECISION_RIGHTS`.

These are not Project State, DD states, professional stages or a lifecycle database. They may disappear when the session ends. The next session reconstructs its view from Current carriers.

## 5. Design focus and option graph

The kernel works on one explicit `decision_object_ref` and one current `key_unknown` at a time, while allowing coupled downstream implications.

Comparable alternatives must share one `comparison_world_id`. Each option records:

- `option_id`;
- materially distinct `mechanism_signature`;
- `parent_refs`;
- actual editable/native `artifact_refs` plus revision/hash-bound `artifact_bindings`;
- `readback_bindings` that point back to the same artifact revision **and artifact content hash** and carry actual-readback evidence;
- `preserved_invariants`;
- strongest benefit;
- strongest failure risk;
- sensitive unknowns;
- branch status.

Cosmetic variants do not count as option-space divergence.

When causally relevant, include `BASELINE / NO-CHANGE / OFF` as a real option rather than assuming intervention is always better.

Rejected and deferred branches remain in lineage. Recency never turns them into Current. Branch transitions are executable semantics: `SELECT/MODIFY/MIX` preserve referenced parents for the next round; `REJECT` becomes `REJECTED_PRESERVED`; `REOPEN` returns the referenced branch to `ACTIVE`; `DEFER` becomes `DEFERRED_PRESERVED` without fabricating a design delta.

## 6. One material co-design round

1. **Resolve** the exact decision object and owner-native Current carriers.
2. **Understand / Frame** actor, outcome, guardrails, key unknown and what is genuinely open.
3. **Explore** materially distinct mechanisms under one comparison world.
4. **Make** the smallest faithful editable/native artifact that exposes the key difference.
5. **Look** at the actual object/state/model/drawing/runtime.
6. **Critique** strongest success, strongest contradiction and root-cause class.
7. Repair obvious non-value defects before asking the Human to choose.
8. If a consequential value choice remains, enter `AWAITING_HUMAN_STEER` with actual comparable artifacts visible.
9. Bind only actual option/object-referenced Human steer.
10. **Guard** the intended mutation against Current authority/source/checkpoint/owner/native constraints.
11. **Make** the next-round artifact while preserving parents and locked invariants.
12. **Read back again**. A Human steer is not implemented until the second-round object is actually inspected.
13. Route triggered professional/integration/technical/independent review.
14. Persist only through existing OLEANDER owners/triggers.

## 7. Second-round Human-feedback delta

A truthful Human-steered second-round delta requires:

`EXPLICIT HUMAN SOURCE → OWNER-NATIVE, HASH-BOUND DECISION-RIGHTS PROOF + OWNER-RULE REVISION → TYPED + REVISIONED DECISION/REFERENT BINDING → HASH-BOUND EDITABLE/NATIVE DELTA REVISION → ACTUAL READBACK BOUND TO THAT SAME REVISION + ARTIFACT CONTENT HASH → INVARIANT-SPECIFIC READBACK BINDING`.

Therefore:

- a pre-steer autonomous probe is **not** a Human-feedback second round;
- a generated artifact without readback is not implementation proof;
- a Human comment without a bound referent is not permission to mutate the wrong branch;
- an `ALLOWED_BY_EXISTING_OWNER_RULE` string by itself is not decision-rights proof; it must be backed by an actual owner-native projection/readback tying the owner-rule revision, actor role, decision object and allowed iteration action together, with authority ceiling `ITERATION_STEER_ONLY`;
- `DEFER` preserves the decision and branches but normally authorizes no design delta by itself;
- `MIX` preserves all selected parents in lineage.
- a readback of revision `r1` cannot prove a made artifact revision `r2`; a readback must also carry the exact made artifact content hash, so matching filenames/revision strings alone are insufficient;
- `invariant_readback_refs` are only an index: each preserved invariant must have a binding to an actual readback of the same artifact revision/content hash; an unrelated readback ref cannot prove invariant preservation;
- an AI-inferred or incomplete steering event cannot satisfy Human-feedback round-two proof.

The steering event records:

`DECISION OBJECT → ACTION → REFERENTS → HUMAN REASON if supplied → CHANGED VARIABLES → PRESERVED INVARIANTS`.

Do not fabricate a reason the Human did not give.

## 8. Auto-advance policy

Auto-advance exists to prevent the assistant from stopping after every tool call, not to bypass Human agency. The stop reason is **computed from projected session/runtime facts**, not supplied as a pre-decided caller verdict.

Side-effect classes:

1. `NONE`;
2. `REVERSIBLE_LOCAL`;
3. `PROJECT_MUTATION_REVERSIBLE`;
4. `PROJECT_MUTATION_AUTHORITY_SENSITIVE`;
5. `EXTERNAL_IRREVERSIBLE_OR_PUBLISHING`.

Default behavior:

- `NONE / REVERSIBLE_LOCAL` → continue when guard allows;
- `PROJECT_MUTATION_REVERSIBLE` → continue only when existing project authority already allows it;
- authority-sensitive, release, publication or irreversible external side effect → existing authorization rules apply; auto-advance does not grant permission.

### 8.1 Real Human stop conditions

Stop and ask/route only when one of these is true:

- consequential steer has ambiguous referent;
- comparable actual artifacts now expose a value-dependent choice the AI cannot legitimately make;
- scope/authority escalation requires Human authorization;
- external irreversible/publishing side effect is next;
- specialist/independent review is required;
- multi-Human decision-rights conflict is unresolved;
- no truthful native/editable substitute exists for the key unknown;
- user asks to stop or requested scope is complete.

Missing facts that do not block the current reversible question remain `OPEN/UNKNOWN` and narrow the claim ceiling instead of freezing all work.

When the Human explicitly `DEFER`s a decision, partition remaining work by dependency: dependent mutations HOLD; unrelated reversible work may continue. `DEFER` must not freeze the whole project by default.

## 9. Mutation guard

Before each material write, project—not duplicate—the applicable Current facts:

`logical object / authority revision + fingerprint / source revision / checkpoint sequence / owner permission / native target / side-effect class / active user constraints`.

For project or external mutation, the guard MUST reread the existing owner-native carrier immediately before the write and bind `logical_object_identity + authority_revision + source_revision + expected_checkpoint_sequence + observed_checkpoint_sequence + carrier_readback_status + resolver_provenance`. The write is eligible only when the carrier readback is `ACTUAL_READBACK`, the resolver provenance is the existing owner resolver, and expected/observed checkpoint sequence are equal. A caller-supplied `ALLOW`, `guard_verdict`, stale projection, or cached permission summary is never authority.

Outcomes:

- valid → intended bounded write;
- stale authority/source/checkpoint → HOLD authority-sensitive mutation and revalidate;
- missing native surface → HOLD native-completion claim; use a truthful editable local prototype only when it answers the current question;
- read-only directive → zero mutation;
- decision-rights conflict → HOLD the conflicting effect, not the entire project;
- unrelated reversible exploration may continue at a lower honest claim ceiling.

## 10. Domain adapter protocol

The shared interaction kernel does **not** create a universal professional stage sequence.

Each triggered domain binds through an adapter projection containing:

- `domain_id`;
- `professional_process_status = CURRENT / CANDIDATE / OPEN / NOT_APPLICABLE`;
- exact `professional_process_ref` when one exists;
- current domain-native question;
- required native output roles;
- readback methods;
- claim ceiling;
- HOLD conditions.

If the domain process is `OPEN`, the kernel may still do bounded pre-professional exploration when truthful, but it cannot award professional PASS or invent a fake universal process to satisfy a test.

Architecture remains Architecture. Digital Product/HCD remains HCD. Physical product work remains OPEN at the professional-process layer until a genuine owner-native process exists or another existing process is correctly triggered.

## 11. Multiple Humans and decision rights

Potential actor roles include:

`DESIGNER / CLIENT_OR_STAKEHOLDER / SPECIALIST / INDEPENDENT_REVIEWER / PROJECT_AUTHORITY / PROMOTION_AUTHORITY`.

The latest Human message is not universal authority.

Examples:

- a designer may steer iteration but not waive specialist structural truth;
- a client may change a value priority but not manufacture statutory compliance;
- producer/AI critique cannot satisfy independent review;
- promotion authority is not implied by participation in design critique.

When scopes conflict, route through existing owner/decision-rights rules and enter `HOLD_DECISION_RIGHTS` only for the affected effect.

## 12. Designer development without profiling

Default support mode is `AUTO`.

At most once per material round unless the user asks for more:

`ONE KEY DISTINCTION → WHY IT CHANGES THIS DESIGN → AT MOST ONE TRANSFER QUESTION`.

Support may fade because:

- the user explicitly asks for less explanation; or
- the **current session** shows repeated clear judgment on the same distinction.

Do not carry that fade inference forward as a competence claim. Do not persist a psychological profile, hidden ability score or durable taste profile. Designer-development evidence never changes authority.

Track separately:

1. artifact learning;
2. designer learning;
3. system-evolution candidate.

Only the third enters existing G9/Evolution governance.

## 13. Continuity and plugin-off survival

`conversation context != project state`.

Resume precedence remains owner-native:

`explicit project/task/object key → Current Project/Task → Control Card → active Execution Receipt/checkpoint → actual native artifact + readback`.

Chat memory is never authority.

The ephemeral session context may contain locators and projected facts, but it must not be written as a plugin-owned `session.json` source of truth. If a resumable checkpoint is needed, write through the existing Execution Receipt / Control Card / Project State trigger.

Uninstalling or replacing the plugin/session UI must leave Current project state, continuation checkpoints, native artifacts and authority intact.

## 14. Readback and closure dimensions

Actual readback is mandatory after:

- material making;
- root-cause repair;
- Human-steered second round.

Neither a successful tool call, CI PASS, plugin health indicator, generated image nor polished presentation proves design quality.

Report closure as separate dimensions:

`SESSION_RESULT / DESIGN_CANDIDATE / PROFESSIONAL_STATE / REVIEW_STATE / PERSISTENCE_STATE / PROMOTION_STATE`.

Never collapse them into one PASS.

## 15. Required v0.2 machine validation

The reference runtime/fixture suite must demonstrate at least:

- `CONTINUE` does not become `DEFER` or `SELECT`;
- a message can be `RESUME + READ_ONLY` without action-level collapse;
- `AUTO_ADVANCE_REVERSIBLE` stops at a real Human value decision;
- affective rejection stays a feedback signal and does not create durable preference;
- ambiguous `就按这个` requires minimum referent clarification;
- unambiguous `就按这个` may bind to the one active object;
- `MIX` requires two parents;
- compound messages preserve multiple clause-scoped Human actions;
- option aliases do not false-bind English articles or incidental text;
- explicit defer requires a pending decision;
- Human-feedback second-round claim fails without explicit Human source, allowed decision rights, typed/revisioned referents, matching artifact/readback revisions or invariant readback;
- comparison readiness fails when an option lacks revision-bound artifact/readback evidence;
- `DEFER` blocks only dependent work;
- branch transitions preserve rejected/deferred/reopened lineage;
- Human-stop decisions are computed from facts rather than caller-provided stop verdicts;
- read-only blocks writes;
- publishing/irreversible actions stop for authorization;
- `OPEN` professional-process adapter cannot award professional PASS.

These machine tests validate Session Kernel behavior only. They do not substitute for real Human co-design trials, professional review or Current promotion.

## 16. v0.2 acceptance boundary

v0.2 is structurally acceptable only if it improves interaction determinism **without** creating:

- a second Project State;
- a shadow checkpoint database;
- a second artifact registry;
- a new universal professional stage family;
- a preference/competence authority;
- AI-owned Design KEEP or Promotion authority.

The intended outcome is a stronger design partner, not a larger governance stack.
