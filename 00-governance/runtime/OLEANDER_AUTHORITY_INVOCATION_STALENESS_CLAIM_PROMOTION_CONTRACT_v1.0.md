# OLEANDER Authority / Invocation / Staleness / Claim / Promotion Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P1**. This contract deepens existing Current Authority, Control Plane, Authority Snapshot, Anti-Pollution, selective readback and promotion semantics. It does not create a second Current Authority.

## 1. Purpose

Before a project, knowledge, runtime-control or presentation action can mutate a Current object, the system must know:

1. **which authority governs this scope**;
2. **which exact object/configuration is being acted on**;
3. **what the invocation is allowed to change**;
4. **what upstream conditions must remain valid**;
5. **what evidence/readback is required after change**;
6. **what the result is allowed to claim**;
7. **what state may be promoted, by whom, and under which gates**.

Core invariant:

`VALID EXECUTION = VALID AUTHORITY + VALID SCOPE + VALID CONFIGURATION + ALLOWED MUTATION + REQUIRED READBACK + CLAIM WITHIN CEILING`.

No successful tool call, export, CI run, receipt, screenshot, model save, page edit or merge can substitute for any missing term above.

## 2. Authority is scoped, not a single global rank

OLEANDER uses two connected authority views.

### 2.1 Global semantic governance

Global governance resolves what the system means and where an object belongs.

Order:

`ROOT CURRENT AUTHORITY → LIVE REGISTRY / IDENTITY CONTRACT → OBJECT PLANE → KNOWLEDGE ARCHITECTURE / APPLICATION MAPPING / PROJECT AXIS → APPLICABLE RUNTIME / EVIDENCE CONTRACT`.

A lower layer can specialize a higher layer only inside delegated scope. It cannot silently redefine a higher-layer invariant.

### 2.2 Project execution authority

For an actual project action, use the existing execution stack:

`MASTER PROTOCOL / PROJECT AUTHORITY → PROJECT STATE → SOURCE AUTHORITY → CURRENT TASK / DECISION QUESTION → CURRENT BASELINE / CONTROLLED OBJECT → APPLICABLE KNOWLEDGE / METHOD → EXECUTION ADAPTER`.

Rules:

- Project State cannot override a Root governance invariant.
- A Current Task cannot override a locked Project State or Source Authority merely because it is newer.
- A Method/Skill can guide execution but cannot invent a project requirement, change authority or project fact.
- An execution adapter/tool has operational capability, not semantic authority.
- A presentation derivative has communication authority only; it does not become Source Authority.

## 3. Authority source classes

Use these source classes to resolve conflicts. They are **classes of authority**, not a universal numeric ranking.

### `SYS_ROOT`
System-wide Current governance, namespace, identity and plane semantics.

### `PROJECT_GOV`
Project/Program Master Protocol, approved Project State, authorized project scope and project decision governance.

### `EXTERNAL_MANDATE`
Applicable law, code, contract, client requirement, licensed standard, regulator/authority decision or other externally controlling requirement.

### `SOURCE_AUTHORITY`
The authoritative source object for geometry, data, content, brand, specification, model, dataset or other project truth.

### `CONFIG_AUTHORITY`
Approved baseline, configuration item state, controlled variable authority and change authority.

### `DECISION_AUTHORITY`
Authorized project decision, waiver/deviation approval, joint decision or acceptance decision.

### `EVIDENCE_AUTHORITY`
Accepted evidence/assurance result for a bounded question/configuration.

### `KNOWLEDGE_METHOD`
Reusable Knowledge/Method/Tool guidance. May constrain how work is performed but cannot self-create project authority.

### `RUNTIME_CONTROL`
Snapshot/register/packet/receipt/gate state. Coordinates authority; does not outrank the source it records.

### `PRESENTATION_DERIVATIVE`
Audience-facing projection. Lowest truth authority by default; may represent stronger sources but cannot silently inherit their semantic authority.

## 4. Conflict-resolution algorithm

When two records appear to conflict, do not use `latest wins`, `most detailed wins`, `highest file version wins`, or `closest to current task wins` as generic rules.

Resolve in this order:

1. **Identity** — are the records about the same logical object?
2. **Plane** — Knowledge, Project or Runtime Control?
3. **Scope** — do both claims actually govern the same project/object/time/configuration/question?
4. **Status** — Current/active/approved versus Candidate/Support/Provenance/Superseded/Expired?
5. **Supersession** — is there an explicit replacement lineage?
6. **Authority owner** — who is authorized to define/change/approve this property?
7. **Delegation** — did the higher authority explicitly delegate this scope?
8. **Configuration** — which baseline/version/configuration was the claim made against?
9. **Evidence freshness** — is the supporting evidence still valid for that configuration and time?
10. **Specificity inside valid delegation** — use the more specific rule only when it does not contradict an undelegated higher authority.
11. **Unresolved conflict** — if still ambiguous, `AUTHORITY_CONFLICT / HOLD`; do not guess.

Hard rules:

- newer does not beat higher authority without valid supersession/change approval;
- project-specific does not beat regulation/contract unless an authorized waiver/deviation exists;
- a source artifact does not beat a later approved Decision/Baseline when that decision legally changed the source;
- an old approved baseline does not remain Current after explicit supersession;
- implementation recurrence does not beat explicit design/brand/source authority;
- runtime receipt records what happened; it does not redefine what should be true.

## 5. Authority Snapshot

`AUTHORITY_SNAPSHOT` is a Runtime Control object that freezes the minimum sufficient authority context needed to execute and later reproduce/inspect a bounded action.

### 5.1 Minimum fields

```yaml
object_id:
runtime_control_type: AUTHORITY_SNAPSHOT
schema_version:
project_id:
workstream_id:
decision_object_id:
object_plane_scope: []
source_object_ids: []
root_authority_ref:
project_authority_refs: []
external_mandate_refs: []
source_authority_refs: []
configuration_refs: []
decision_authority_refs: []
active_constraints: []
protected_objects: []
allowed_mutation_scope:
claim_ceiling_ref:
source_revision_map: {}
authority_fingerprint:
verified_at:
verified_by:
status:
stale_if: []
supersedes:
```

### 5.2 State machine

`CANDIDATE → VERIFIED_CURRENT → STALE → SUPERSEDED`

`VERIFIED_CURRENT` means the snapshot was checked against the Current sources at the recorded time. It does not mean every project object in scope is professionally valid.

### 5.3 Fingerprint

The fingerprint should include only material authority inputs, for example:

`root authority revision + project state revision + active constraint set/hash + source authority revisions + baseline/configuration revisions + current decision-lock set`.

Do not include volatile non-authoritative data merely to force unnecessary invalidation.

## 6. Invocation Contract

Every material execution packet should resolve an invocation envelope before mutation.

### 6.1 Minimum invocation envelope

```yaml
invocation_id:
requested_operation:
object_plane:
project_id:
workstream_id:
decision_object_id:
target_object_ids: []
source_object_ids: []
authority_snapshot_ref:
knowledge_snapshot_ref:
current_baseline_refs: []
current_source_revisions: {}
current_decision_question:
required_outcome:
protected_objects: []
allowed_mutations: []
forbidden_mutations: []
active_constraints: []
open_assumptions: []
open_unknowns: []
required_evidence: []
required_readback: []
claim_target:
claim_ceiling_ref:
stale_if: []
stop_conditions: []
reopen_conditions: []
```

### 6.2 Mutation classes

Use a controlled mutation class:

- `READ_ONLY` — inspect only;
- `PRESENTATION_ONLY` — presentation projection may change, source truth protected;
- `LOCAL_CARRIER_EDIT` — edit one carrier without changing semantic project truth;
- `SEMANTIC_OBJECT_EDIT` — change one Project/Knowledge semantic object inside authority;
- `CROSS_OBJECT_COORDINATION_EDIT` — coordinated change across registered dependent objects;
- `CONFIGURATION_CHANGE` — changes a controlled configuration/baseline candidate;
- `AUTHORITY_CHANGE` — changes authority/registry/identity/governance; highest readback burden.

Unknown mutation scope defaults upward, not downward.

### 6.3 Protected-object rule

A protected object may be referenced, measured, masked, compared or projected according to its contract but not re-authored by a lower-authority owner.

Examples:
- board layout cannot reshape authoritative plan geometry;
- visual polish cannot edit accepted test data;
- downstream model cleanup cannot change a locked datum without a Change record;
- a Knowledge page cannot absorb changing receipt logs merely because they are relevant.

## 7. Selective Readback Contract

Readback burden follows mutation blast radius.

### `RB0 NONE`
Pure read-only inspection; no mutation.

### `RB1 LOCAL`
Reopen the changed carrier/object and verify the intended local delta.

### `RB2 DEPENDENCY`
Reopen direct registered consumers/dependents and check no material contradiction.

### `RB3 INTEGRATION`
Required for interface/shared-variable/coupled-system changes; check integrated readback across affected owners.

### `RB4 AUTHORITY`
Required for authority, identity, baseline, cross-platform pointer or promotion changes; re-read authority state and drift across required platforms.

Rules:
- unknown blast radius expands to the next sufficient level;
- successful write/export/commit is not readback;
- hash equality proves file identity, not semantic/design correctness;
- visual claims require actual rendered/readback evidence;
- field claims require field evidence, not artifact existence.

## 8. Staleness model

Staleness is an explicit semantic state, not merely an old timestamp.

### 8.1 Trigger families

`AUTHORITY_CHANGE`
- root/current authority changed;
- project state changed;
- decision/change authority changed.

`CONFIGURATION_CHANGE`
- baseline superseded;
- controlled variable changed;
- source model/data revision changed.

`REQUIREMENT_CHANGE`
- requirement/constraint changed;
- waiver/deviation expired or withdrawn.

`INTERFACE_CHANGE`
- interface reopened;
- coupling/criticality/acceptance obligation changed.

`EVIDENCE_CHANGE`
- evidence rejected, contradicted, superseded or out of calibration/time validity;
- new material contradictory evidence appears.

`ASSUMPTION_UNKNOWN_CHANGE`
- assumption refuted/expired;
- previously open unknown resolved in a way that invalidates current work.

`METHOD_ENVIRONMENT_CHANGE`
- software/model/instrument/runtime version changed materially;
- execution surface known failure or reliability state invalidates earlier receipt.

`TIME_OR_EXTERNAL_CHANGE`
- regulation/standard/product version changed;
- review/verification due date passed for mutable content.

### 8.2 Consequence classes

- `INFORMATIONAL` — record only; no validity loss;
- `RECHECK_REQUIRED` — current state may remain usable but must be rechecked before next promotion;
- `REOPEN_REQUIRED` — prior closure/promotion is no longer sufficient for the affected scope;
- `INVALIDATED` — object/receipt cannot be used as Current evidence for the affected claim.

### 8.3 Propagation rule

Propagate only through registered typed edges and material consumers.

`LOCAL CHANGE ≠ GLOBAL INVALIDATION`, but also `LOCAL CHANGE ≠ LOCAL CONSEQUENCE`.

Unknown dependency graph for a material change is itself a blocker until the blast radius is bounded.

## 9. Claim Ceiling is vector-valued

Do **not** use one scalar maturity number for all truth dimensions. A result may be strong in one dimension and open in another.

Use independent ceiling axes.

### 9.1 Execution ceiling

`NOT_RUN | EXECUTED | READBACK_CONFIRMED`

### 9.2 Evidence ceiling

`NO_EVIDENCE | CONTEXTUAL | INDIRECT | DIRECT_BOUNDED | ASSURED_FOR_SCOPE`

### 9.3 Design-quality ceiling

`UNASSESSED | REVISE | REVIEWABLE | KEEP_SUPPORT | KEEP_MAIN`

Only applicable independent/project design review may grant KEEP states.

### 9.4 Technical ceiling

`UNCHECKED | COORDINATED | TECHNICALLY_CHECKED | VERIFIED_FOR_SCOPE`

Professional sign-off, when legally/professionally required, remains a separate authority state.

### 9.5 Field/operational ceiling

`NOT_FIELD | FIELD_OBSERVED | FIELD_MEASURED | IN_USE_VALIDATED`

Simulation, render, precedent, lab prototype or desk research cannot populate a field state by implication.

### 9.6 Research ceiling

Keep R1 and R2 independent:

`R1 = NOT_APPLICABLE | OPEN | REVISE | PASS | HOLD | REJECT`

`R2 = NOT_APPLICABLE | OPEN | REVISE | PASS | HOLD | REJECT`

`R2 PASS` never promotes `R1`.

### 9.7 Compliance/professional ceiling

`NOT_APPLICABLE | OPEN | REVIEWED_FOR_SCOPE | ACCEPTED_BY_AUTHORITY`

Do not synthesize professional approval from automated checks.

### 9.8 Presentation ceiling

`NOT_PRESENTED | DRAFT | READBACK_REVIEWED | KEEP_FOR_AUDIENCE`

Presentation KEEP cannot raise any upstream ceiling.

## 10. Cross-ceiling forbidden inferences

Hard failures:

- `EXECUTED → DESIGN KEEP`;
- `CI PASS → PROFESSIONAL ACCEPTANCE`;
- `RENDER PASS → TECHNICAL VERIFIED`;
- `SIMULATION PASS → FIELD VERIFIED`;
- `VERIFICATION PASS → VALIDATION PASS`;
- `MANY CITATIONS → HIGH EVIDENCE STRENGTH`;
- `LATEST FILE → CURRENT BASELINE`;
- `PRESENTATION KEEP → PROJECT KEEP`;
- `METHOD COMPLIANCE → QUALITY IMPROVEMENT`;
- `PROJECT SUCCESS → REUSABLE KNOWLEDGE CURRENT`.

## 11. Promotion Contract

Promotion is an explicit authority action. It is not inferred from completion of work.

### 11.1 Promotion request

```yaml
promotion_id:
target_object_id:
target_plane:
from_state:
requested_state:
scope:
authority_snapshot_ref:
current_baseline_ref:
required_gates: []
gate_results: []
claim_ceiling_before:
claim_ceiling_requested:
material_dependencies: []
open_blockers: []
independent_review_ref:
readback_refs: []
promotion_authority:
decision:
decided_at:
reopen_triggers: []
```

### 11.2 Promotion rules

- Promotion authority must be valid for the target object/state.
- All applicable required gates must pass; non-applicable gates must be explicitly marked rather than silently omitted.
- A promotion cannot raise a claim dimension beyond its supporting authority/evidence.
- The weakest material dependency bounds the promoted scope.
- Open Critical contradiction/authority conflict blocks promotion.
- Major unresolved issues require explicit bounded containment and cannot be hidden in notes.
- Promotion creates/updates a Current state only after required readback.
- Promotion of a Runtime Control record does not automatically promote its referenced Project/Knowledge objects.

## 12. Reopen Contract

A promoted/closed object must reopen when an explicit material trigger invalidates its basis.

Common triggers:
- authority snapshot changed materially;
- governing requirement/constraint changed;
- source authority or baseline changed;
- material controlled variable changed;
- interface reopened;
- evidence became stale/rejected/contradicted;
- Major/Critical assumption refuted/expired;
- unresolved unknown resolved adversely;
- independent review raises a new Critical/Major objection;
- field/in-use evidence contradicts predicted performance;
- implementation deviates from accepted configuration.

Reopen must identify:

`trigger → affected object → invalidated/recheck claim dimension → required owner → required readback/assurance → new promotion obligation`.

## 13. Authority-change rule

Changes to any of the following are `AUTHORITY_CHANGE` and automatically require RB4:

- Root Current Authority pointer/semantic contract;
- canonical object identity or Current carrier;
- Project Master Protocol/Project State authority;
- change/decision authority assignment;
- baseline Current pointer;
- cross-platform Current pointer/redirect;
- promotion policy or claim-ceiling contract.

Authority changes must not be smuggled through a normal artifact edit.

## 14. Failure modes

Reject/HOLD when:

- authority source cannot be resolved;
- two active authorities control the same property without delegation/conflict resolution;
- a stale snapshot is reused as Current;
- invocation mutation exceeds allowed scope;
- protected object was re-authored by a lower-authority layer;
- required readback is missing;
- requested claim exceeds any applicable ceiling;
- promotion has no authorized promoter;
- superseded evidence/baseline is presented as Current;
- runtime receipt is used as proof of design/research/field/professional quality beyond its ceiling;
- lower-specificity or newer implementation silently overrides an external mandate or Project Authority.

## 15. Validator floor

- `AUTH-001` exactly one effective change/decision authority per controlled property/scope unless explicit joint authority contract exists;
- `AUTH-002` no generic latest-wins resolution across authority classes;
- `AUTH-003` lower authority cannot override undelegated higher constraint;
- `AUTH-004` unresolved authority conflict = HOLD;
- `SNAP-001` material invocation requires a resolvable Authority Snapshot;
- `SNAP-002` snapshot fingerprint must match material Current sources before reuse;
- `SNAP-003` changed material fingerprint invalidates snapshot reuse;
- `INV-001` mutation class required for material write;
- `INV-002` target objects and protected objects cannot overlap for a forbidden edit operation;
- `INV-003` operation outside allowed mutation scope = reject;
- `RB-001` required readback level follows mutation blast radius;
- `RB-002` unknown material blast radius expands readback / blocks closure;
- `STALE-001` material stale trigger must map to consequence and affected objects;
- `STALE-002` invalidated evidence/receipt cannot support Current promotion;
- `CLAIM-001` claim ceiling must be vector-valued across applicable axes;
- `CLAIM-002` forbidden cross-ceiling inference = fail;
- `CLAIM-003` field claim requires field/operational evidence state;
- `PROM-001` promotion requires explicit authority + applicable gates + readback;
- `PROM-002` promotion cannot exceed weakest material dependency ceiling;
- `PROM-003` Runtime Control promotion cannot auto-promote Project/Knowledge truth;
- `REOPEN-001` material trigger must reopen/recheck affected promoted objects;
- `REOPEN-002` reopen record must state invalidated claim dimension and closure obligation.

## 16. Edge-case examples

### Example A — newer model conflicts with approved baseline

A newer `.skp` exists but no approved Change/Baseline update exists.

Result:
- newer file = artifact candidate;
- approved baseline remains Current;
- do not use file modification time as authority;
- if the newer file is intended to replace Current, create Change → impact → approval → readback → new Baseline.

### Example B — board redraws geometry for clarity

Presentation owner simplifies a plan into a cleaner diagram.

Result:
- allowed only as disclosed presentation projection if claim does not require exact geometry;
- exact spatial/technical claims must still bind to authoritative geometry;
- presentation derivative cannot replace Source Authority.

### Example C — simulation validates expected performance

Simulation passes all planned scenarios.

Result:
- execution/evidence/technical ceilings may rise for the bounded simulation claim;
- field ceiling remains `NOT_FIELD`;
- operational validation remains open unless separately evidenced.

### Example D — requirement changed after verification

Requirement R-21 was VERIFIED, then changed materially.

Result:
- previous verification becomes historical for old requirement configuration;
- affected design, interface, evidence and assurance objects reopen according to typed dependency edges;
- no carry-forward PASS without re-assurance.

### Example E — method page contains successful project receipt

A METHOD page describes a project where the method worked.

Result:
- reusable bounded learning may enter a Practice/Case/G9 candidate;
- receipt/hash/PR/sync history stays Project/Runtime Control provenance;
- project success cannot self-promote the METHOD's research/content state.

## 17. P1 closure condition

This priority item is considered sufficiently refined for draft review when:

- authority classes and conflict algorithm are explicit;
- Authority Snapshot and Invocation envelopes are explicit;
- mutation classes and readback levels are explicit;
- staleness triggers/consequences are explicit;
- claim ceilings are independent axes, not one maturity score;
- promotion and reopen contracts are explicit;
- machine-readable counterpart and validators exist;
- representative edge cases pass without requiring hidden interpretation.
