# OLEANDER Project State / Decision Question / Execution Scope Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P2**. Extends the existing P3 Workstream definition and Control Plane. It does not convert P3 into a lifecycle stage and does not create a second Project DB.

## 1. Purpose

A project can have valid authority and still fail operationally if the active state is ambiguous.

Before material execution, the system must resolve:

- what Project/Workstream is active;
- what decision is currently being made;
- what is locked versus open;
- what may be changed in this loop;
- what evidence/gate is currently relevant;
- what dependency blocks advancement;
- what constitutes completion, rejection, deferment or reopen.

Core invariant:

`WORKSTREAM IDENTITY ≠ LOOP ≠ DESIGN STATE ≠ GATE ≠ DECISION QUESTION ≠ TASK STATUS`.

They are separate axes.

## 2. Project State is a Runtime Control snapshot

`PROJECT_STATE` is a Runtime Control object that summarizes the minimum actionable state of a P2 Project and its active P3 Workstreams.

It is not the Project itself.

It is not a task list.

It is not a phase label.

It must be reproducible from Current project/runtime records and must become stale when its material inputs change.

## 3. Project State minimum contract

```yaml
project_state_id:
schema_version:
object_plane: RUNTIME_CONTROL
runtime_control_type: PROJECT_STATE
project_id:
program_id:
authority_snapshot_ref:
current_baseline_refs: []
active_workstreams: []
paused_workstreams: []
blocked_workstreams: []
current_project_objective:
current_project_claim_target:
active_constraints: []
project_level_locked_objects: []
project_level_open_objects: []
critical_interfaces: []
critical_risks: []
critical_unknowns: []
current_gate_refs: []
open_promotion_obligations: []
next_project_decisions: []
state_fingerprint:
status:
stale_if: []
created_at:
updated_at:
```

## 4. Project operational status

Use project operational status only for operational availability:

`ACTIVE | PAUSED | BLOCKED | HOLD | CLOSED | SUPERSEDED`.

Do not reuse this field for Design State.

Definitions:

- `ACTIVE` — at least one authorized Workstream may proceed;
- `PAUSED` — intentionally stopped without unresolved validity conflict;
- `BLOCKED` — cannot proceed because a required dependency/action is unavailable;
- `HOLD` — proceeding would risk semantic/authority/evidence corruption and requires resolution first;
- `CLOSED` — no further execution is required for the defined project scope;
- `SUPERSEDED` — another Project State snapshot has replaced this snapshot.

## 5. Workstream Runtime Card

Every active P3 Workstream should resolve a compact runtime card.

```yaml
workstream_id:
project_id:
scope_in: []
scope_out: []
definition_owner:
decision_rights: []
integration_owner:
authority_snapshot_ref:
current_decision_object_ref:
current_decision_question:
current_loop:
design_state:
current_gate_ref:
current_baseline_refs: []
locked_objects: []
locked_variables: []
open_objects: []
open_variables: []
protected_objects: []
dependencies: []
interfaces: []
active_requirements: []
open_evidence: []
open_risks: []
open_assumptions: []
open_unknowns: []
allowed_mutation_class:
required_readback_level:
claim_target:
claim_ceiling_ref:
stop_conditions: []
reopen_conditions: []
next_decision:
```

## 6. Current Loop

Keep only the existing two primary loop contexts unless a later authority explicitly changes them:

- `EXPLORATION`
- `CANONICAL_PRODUCTION`

### Exploration

Purpose:
- formulate/compare hypotheses;
- test alternatives;
- allow controlled failure;
- discover decision-relevant evidence.

Flow:

`Decision Question → bounded variants / sandbox → compare → reject / branch / candidate`.

Exploration may create candidates but does not grant Current authority.

### Canonical Production

Purpose:
- execute the selected candidate under Current authority;
- produce/edit authoritative carriers;
- run required QA/readback/gates;
- promote/revise/reject.

Flow:

`Candidate → Authority/Contract → Execute → Machine QA → Visual QA → Project QA → triggered specialist gates → Promote / Revise / Reject → Persist / Register`.

`EXPLORATION` and `CANONICAL_PRODUCTION` are contexts, not quality states.

## 7. Design State

Use Design State independently from Current Loop:

`EXPLORE | CANDIDATE | REVISE | REJECTED | PROMOTED | LOCKED | SUPERSEDED`.

Interpretation:

- `EXPLORE` — hypothesis under active exploration;
- `CANDIDATE` — eligible for structured review/selection;
- `REVISE` — material issue identified; repair required;
- `REJECTED` — not selected for the scoped decision;
- `PROMOTED` — explicitly accepted for the stated scope, not necessarily locked;
- `LOCKED` — promotion plus explicit change-control requirement;
- `SUPERSEDED` — replaced by later authorized state.

Hard rules:

- `CANDIDATE` can exist in either loop context;
- `PROMOTED` does not imply all professional gates are complete;
- `LOCKED` requires a change/reopen path;
- `REVISE` must name a material root cause or unresolved condition;
- `REJECTED` remains traceable when it materially informed the decision.

## 8. Gate is not a phase

`Current Gate` is a pointer to the current promotion/assurance obligation relevant to a decision/object.

A Workstream may:
- pass one gate and later reopen it;
- have different objects at different gates simultaneously;
- participate in multiple assurance objects;
- continue work while another Workstream is blocked.

Never infer project progress percentage from gate number alone.

## 9. Decision Object: Runtime orchestration handle

A Runtime Control `DECISION_OBJECT` exists when a bounded decision must coordinate multiple Project objects, owners, evidence or interfaces.

It is distinct from the Project-plane `DECISION` semantic record that captures the authorized decision result.

### 9.1 Minimum fields

```yaml
decision_object_id:
project_id:
workstream_ids: []
authority_snapshot_ref:
decision_question:
decision_mode:
why_now:
scope_in: []
scope_out: []
source_objects: []
requirements: []
constraints: []
locked_objects: []
locked_variables: []
open_objects: []
open_variables: []
protected_objects: []
alternatives: []
evaluation_criteria: []
mandatory_reject_conditions: []
required_evidence: []
required_readback: []
participating_roles: []
decision_authority:
integration_owner:
claim_target:
claim_ceiling_ref:
status:
resulting_project_decision_ref:
reopen_triggers: []
```

## 10. Decision Question quality gate

A valid Decision Question must be:

### Bounded
It names the object/scope being decided.

### Decisionable
There is at least one possible disposition or choice.

### Consequential
The answer changes a Project object, claim, allocation, baseline, interface or next action.

### Evidence-addressable
The required proof can be named, even if not yet available.

### Authority-addressable
The person/role allowed to decide can be named.

### Reopenable
Material future evidence/change can be linked to a reopen condition.

Reject task-shaped pseudo-questions such as:
- “Make the render better.”
- “Continue modeling.”
- “Research more.”
- “Finish the deck.”

Prefer:
- “Which of A/B maintains the locked circulation while achieving the required support-area program with zero no-go overlap?”
- “Does the current south-entry configuration satisfy REQ-021 under the accepted baseline?”
- “Which presentation projection best establishes Claim C07 for a 90-second jury review without hiding the technical proof?”

## 11. Decision modes

Controlled modes:

`SELECT | COMPARE | ACCEPT | REVISE | REJECT | LOCK | REOPEN | DEFER | ESCALATE`.

These describe the current orchestration question, not the final Project Decision type.

## 12. Locked / Open / Protected

These must remain distinct.

### Locked
Current authorized value/object must not change without a Change/reopen path.

### Open
The decision intentionally leaves this variable/object unresolved or changeable.

### Protected
This invocation may not re-author the object because authority belongs elsewhere, even if the object itself is not globally locked.

Example:
- a project plan geometry may be `LOCKED` globally;
- a source photograph may be `PROTECTED` from geometry-like manipulation in a board task but not globally locked;
- a candidate color palette may be `OPEN` while the logo geometry is `LOCKED`.

## 13. Execution Scope / Mutation Budget

Each decision loop must state the maximum permitted change class from P1:

`READ_ONLY | PRESENTATION_ONLY | LOCAL_CARRIER_EDIT | SEMANTIC_OBJECT_EDIT | CROSS_OBJECT_COORDINATION_EDIT | CONFIGURATION_CHANGE | AUTHORITY_CHANGE`.

Additionally, define a mutation budget:

```yaml
allowed_object_classes: []
allowed_object_ids: []
allowed_properties: []
forbidden_object_ids: []
forbidden_properties: []
max_change_impact_class:
required_change_record_if_exceeded:
```

If the repair needed to answer the Decision Question exceeds the budget, stop and escalate/change-authorize rather than silently widening scope.

## 14. Dependency disposition

Every dependency relevant to the active Decision Question should be one of:

`SATISFIED | OPEN_NONBLOCKING | OPEN_BLOCKING | STALE | INVALIDATED | OUTSIDE_SCOPE`.

A Workstream may proceed with `OPEN_NONBLOCKING` dependencies only when the claim ceiling and downstream consequence remain explicitly bounded.

## 15. Stop conditions

Stop the current execution loop when any material condition occurs:

- authority becomes stale/conflicted;
- required dependency becomes `OPEN_BLOCKING`;
- necessary mutation exceeds authorized budget;
- protected object would need unauthorized re-authoring;
- required evidence cannot be obtained in the current route;
- current hypothesis is falsified and no legal candidate remains;
- claim target becomes invalid/out-of-scope;
- current baseline changed materially;
- safety/compliance/professional boundary requires another authority.

`STOP` means change route, reframe, escalate, research or HOLD; it does not mean silently lower the standard.

## 16. Completion conditions

A Decision Object may close only when:

- the Decision Question received an explicit disposition;
- the authorized Project-plane Decision/acceptance/rejection record exists when consequential;
- changed objects have required readback;
- affected interfaces/dependencies are updated;
- required evidence/assurance result is bound;
- locked/open variables are updated;
- downstream reopen/stale obligations are registered;
- claim ceiling accurately reflects what was established;
- next decision, if any, is explicit.

## 17. Reopen conditions

Reopen the Decision Object when:

- a locked input changes;
- a key assumption is refuted/expired;
- new evidence contradicts the decision basis;
- an interface/shared variable changes materially;
- implementation fails readback;
- a higher authority changes requirement/constraint;
- independent review raises a material objection;
- the accepted alternative cannot be implemented under Current conditions.

Reopen does not erase the historical decision; it creates a new decision cycle linked to the prior basis.

## 18. Parallel-workstream rule

Project State must support concurrency.

One blocked Workstream does not automatically block all others.

Global HOLD is justified only when the blocker affects:
- shared authority;
- shared Current baseline;
- a project-critical dependency;
- a cross-cutting requirement/constraint;
- a critical interface needed by multiple active streams;
- a promoted project claim that would become false.

## 19. Validator floor

- `PSTATE-001` Project State snapshot references valid P2 Project identity;
- `PSTATE-002` active Workstream runtime card must resolve authority + Decision Question;
- `PSTATE-003` Project operational status cannot replace Design State;
- `PSTATE-004` Current Gate cannot be treated as lifecycle phase/progress percentage;
- `DECQ-001` material Workstream execution requires bounded Decision Question;
- `DECQ-002` task-shaped pseudo-question cannot close a consequential decision;
- `DECQ-003` Decision Question requires decision authority when consequential;
- `DECQ-004` Decision Object must distinguish orchestration record from resulting Project Decision;
- `SCOPE-001` locked/open/protected sets are semantically distinct;
- `SCOPE-002` operation exceeding mutation budget requires Change/escalation;
- `SCOPE-003` protected object unauthorized re-authoring fails;
- `DEP-001` material dependency requires explicit disposition;
- `STOP-001` stop condition cannot be bypassed by silently lowering claim/quality standard;
- `CLOSE-001` Decision Object closure requires explicit disposition + required readback;
- `REOPEN-001` material input change reopens historical decision cycle without deleting lineage;
- `PAR-001` local Workstream blocker does not auto-globalize without project-critical propagation evidence.

## 20. P2 closure condition

P2 is sufficiently refined for draft review when Project State, Workstream Runtime Card, Decision Object, Decision Question gate, mutation budget, dependency disposition, stop/close/reopen semantics and concurrency rules all have machine-readable counterparts and edge-case tests.
