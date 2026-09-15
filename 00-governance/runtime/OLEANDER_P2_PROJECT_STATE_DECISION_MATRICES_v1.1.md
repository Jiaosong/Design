# OLEANDER P2 Project State / Decision Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P2 SECOND PASS**. Semantic owner remains `OLEANDER_PROJECT_STATE_DECISION_SCOPE_CONTRACT_v1.0.*`.

## 1. Purpose

P2 prevents a valid authority stack from being misused by an ambiguous execution state.

Core invariant:

`PROJECT OPERATIONAL STATUS ≠ WORKSTREAM STATUS ≠ LOOP ≠ DESIGN STATE ≠ GATE ≠ DECISION QUESTION ≠ TASK STATUS`.

The system must know what is being decided before deciding what work to do.

---

## 2. Decision Question Grammar

A material Decision Question should compile to:

`DECIDE <disposition/choice> FOR <target object/scope> UNDER <requirements + constraints + locked inputs> USING <named evidence/readback> BY <decision authority> FOR <claim target>, WITH <reopen trigger>`.

### 2.1 Question quality matrix

| Test | PASS condition | FAIL example |
|---|---|---|
| `BOUNDARY` | exact object/scope named | “improve the project” |
| `DECISIONABILITY` | at least one disposition/alternative exists | “continue modeling” |
| `CONSEQUENCE` | answer changes a semantic object, allocation, baseline, claim or next route | “look at this” |
| `EVIDENCE_ADDRESSABLE` | required proof/readback can be named | “make it feel right” with no review condition |
| `AUTHORITY_ADDRESSABLE` | valid decider can be named | everyone/no one owns decision |
| `CONSTRAINT_AWARE` | hard requirements/constraints explicit | option comparison ignores code/locked datum |
| `CLAIM_BOUND` | states what conclusion the decision is intended to establish | vague “PASS” |
| `REOPENABLE` | future invalidating trigger can be named | irreversible decision record with no lineage |

A consequential question must pass all eight.

### 2.2 Task-shaped pseudo-question conversion

- `Make the render better` → `Which camera/material/lighting projection best communicates Claim C07 without altering locked geometry and while passing first-read + source-bound readback?`
- `Continue modeling` → `Does the current model require geometry changes to satisfy REQ-X and IF-Y, or can remaining work stay within LOCAL_CARRIER_EDIT?`
- `Research more` → `Which unresolved Claim/Unknown prevents the current decision, and what evidence would change its disposition?`
- `Finish the deck` → `Which audience release is sufficient to establish the approved argument sequence and required technical proof for the target review?`

---

## 3. Project State Consistency Matrix

| Project operational status | Allowed meaning | Required minimum | Forbidden interpretation |
|---|---|---|---|
| `ACTIVE` | at least one Workstream legally executable | valid Authority Snapshot + one executable Decision Object | all Workstreams healthy |
| `PAUSED` | intentional temporary stop | pause owner/reason/resume condition | evidence or authority conflict hidden as pause |
| `BLOCKED` | required dependency unavailable | blocking dependency + owner + resolution route | automatic global project failure |
| `HOLD` | execution would risk authority/semantic/evidence corruption | explicit HOLD reason + release condition | ordinary queue/waiting status |
| `CLOSED` | defined project scope requires no more execution | closure basis + unresolved items bounded/outside scope | “delivery file exists” |
| `SUPERSEDED` | newer Project State snapshot controls | superseding state ref | project identity deleted |

### 3.1 Global HOLD threshold

A local blocker escalates to Project `HOLD` only when it affects at least one of:
- shared authority;
- shared Current baseline;
- project-critical requirement/constraint;
- critical interface consumed by multiple active streams;
- project-level claim target;
- safety/legal/professional boundary;
- inability to establish which configuration is Current.

Otherwise keep the unaffected Workstreams executable.

---

## 4. Workstream Concurrency Matrix

| Workstream A | Workstream B relation | Can proceed independently? | Required coordination |
|---|---|---|---|
| no shared variables/interfaces/dependencies | independent | YES | normal Project State visibility |
| one-way material dependency A→B | dependent | A may proceed; B only within bounded provisional scope | dependency disposition + stale_if |
| shared controlled variable | coupled | CONDITIONAL | single change authority + consumer registration |
| reciprocal interface | reciprocal | CONDITIONAL | Interface contract + joint readback at required maturity |
| tightly coupled | inseparable for target claim | NO for closure/promotion | integrated prototype/readback |
| shared baseline mutation | configuration-coupled | NO during incompatible revisions | Change + baseline coordination |
| shared external mandate conflict | governance-coupled | NO for affected scope | authority/professional escalation |

Concurrency optimization must never bypass integration obligations.

---

## 5. Locked / Open / Protected Matrix

These are independent flags, not one enum.

| Condition | Locked | Open | Protected | Legal action |
|---|---:|---:|---:|---|
| selected geometry under baseline | YES | NO | may be | read/reference; change only through Change/reopen |
| unresolved candidate material | NO | YES | NO | explore within mutation budget |
| external Source Authority photo/data | may be NO | maybe | YES to lower-authority re-authorship | derive/project with disclosed transformation; do not rewrite truth |
| locked datum owned by another discipline | YES | NO | YES | consume; request Change from authority |
| open color palette while logo geometry fixed | logo YES / palette NO | palette YES | logo may be protected | modify palette only |
| historical superseded candidate | NO | NO | YES for immutable provenance | reference/history only |

Hard contradictions:
- same property cannot be simultaneously `LOCKED` and `OPEN` for same scope/configuration;
- `PROTECTED` does not imply globally locked;
- locked value without change/reopen route is governance dead-end and invalid for active development.

---

## 6. Mutation Budget Escalation Matrix

| Current budget | Needed action | Outcome |
|---|---|---|
| `READ_ONLY` | any write | stop; request higher budget |
| `PRESENTATION_ONLY` | source truth edit | reject/reframe; presentation may only project |
| `LOCAL_CARRIER_EDIT` | semantic value changes | escalate to `SEMANTIC_OBJECT_EDIT` |
| `SEMANTIC_OBJECT_EDIT` | registered dependent objects must change | escalate to `CROSS_OBJECT_COORDINATION_EDIT` |
| `CROSS_OBJECT_COORDINATION_EDIT` | Current baseline/configuration changes | create/route through `CONFIGURATION_CHANGE` |
| `CONFIGURATION_CHANGE` | authority/identity/promotion policy changes | escalate to `AUTHORITY_CHANGE` |
| any | required action touches protected object without authority | HOLD/ESCALATE, never auto-expand |

Budget escalation must occur **before** mutation, except when an unplanned mutation is detected after the fact; then mark unauthorized delta and do not normalize it as Current.

---

## 7. Dependency Disposition Matrix

| Disposition | Can execute? | Can promote? | Required action |
|---|---:|---:|---|
| `SATISFIED` | YES | YES, subject to other gates | none |
| `OPEN_NONBLOCKING` | YES within bounded claim | CONDITIONAL | carry explicit ceiling + due/reopen trigger |
| `OPEN_BLOCKING` | NO for dependent decision | NO | resolve dependency or reframe scope |
| `STALE` | only non-reliant exploratory work | NO for affected claim | recheck/revalidate |
| `INVALIDATED` | NO | NO | replace/rework basis |
| `OUTSIDE_SCOPE` | YES if genuinely non-material | YES if claim excludes it | record boundary |

A dependency cannot be downgraded from blocking to nonblocking merely to preserve schedule.

---

## 8. Decision Object Lifecycle Matrix

Recommended orchestration lifecycle:

`OPEN → FRAMED → OPTIONS_READY → EVIDENCE_READY → DECISION_READY → DISPOSITIONED → IMPLEMENTATION_PENDING → READBACK_PENDING → CLOSED`

Alternative terminal/branch states:

`DEFERRED | ESCALATED | REJECTED | REOPENED | SUPERSEDED`.

The resulting Project-plane `DECISION` remains a separate semantic record.

### 8.1 Lifecycle entrance conditions

| State | Minimum entrance condition |
|---|---|
| `FRAMED` | valid Decision Question + scope + authority |
| `OPTIONS_READY` | alternatives/dispositions satisfy hard constraints or invalid options explicitly rejected |
| `EVIDENCE_READY` | required comparison/readback evidence available or explicit Unknown prevents progress |
| `DECISION_READY` | criteria + constraints + evidence + authority coherent |
| `DISPOSITIONED` | explicit authorized SELECT/ACCEPT/REVISE/REJECT/LOCK/DEFER/ESCALATE |
| `IMPLEMENTATION_PENDING` | consequential decision record exists and mutation route defined |
| `READBACK_PENDING` | implementation delta exists and required RB level known |
| `CLOSED` | readback + affected dependencies/interfaces + claim ceiling + next decision updated |

`DISPOSITIONED ≠ CLOSED`.

---

## 9. Fork / Merge / Alternative Lineage

Exploration may fork; Current must not silently multiply.

### Fork
Create branch alternatives when:
- alternatives cannot coexist in one configuration;
- evidence must be collected independently;
- mutation risks contaminating comparison.

Each alternative records:
`origin decision object + inherited locked inputs + unique open variables + evidence + status`.

### Merge
A merge is legal only when:
- combined alternative is itself evaluated as a new candidate;
- locked/constraint compatibility is checked;
- inherited evidence is still applicable;
- resulting configuration receives its own readback.

Forbidden:
- cherry-picking only favorable evidence from rejected alternatives;
- merging incompatible baselines without Change analysis;
- keeping multiple alternatives as implicit Current.

---

## 10. Decision Lineage Contract

Every consequential Decision Object cycle records:

`prior_decision_object_ref → trigger_for_new_cycle → retained_basis → invalidated_basis → new_question → resulting_project_decision_ref`.

Reopen never erases prior reasoning. It changes current applicability.

If a prior decision is still valid for some scope/configuration, preserve that bounded validity rather than declaring the whole decision false.

---

## 11. Project State Fingerprint

The Project State fingerprint should include only action-relevant state:
- Authority Snapshot fingerprint;
- Current project baseline refs;
- active Workstream IDs + current Decision Object refs;
- project-level locked objects/variables;
- active critical requirements/constraints;
- critical interface state;
- promotion-breaking open issues/unknowns;
- current claim target.

Do not hash volatile task chatter or incidental timestamps into the state fingerprint.

Fingerprint mismatch consequence:
- if informational: refresh snapshot without reopen;
- if decision/material scope changed: mark prior Project State `STALE/SUPERSEDED` and compile a new snapshot;
- never continue material execution on an unknown mismatch.

---

## 12. Stop / Hold / Reframe Matrix

| Condition | STOP current action | Workstream BLOCKED | Project HOLD | Reframe allowed |
|---|---:|---:|---:|---:|
| mutation exceeds budget | YES | maybe | only if shared/global | YES through authority route |
| local evidence missing | YES for dependent decision | YES | usually NO | YES if claim/scope legitimately narrows |
| authority conflict local to Workstream | YES | YES | only if shared authority affected | after conflict resolution |
| external mandate applicability unresolved | YES | YES | YES if project-wide/material | only with authorized boundary |
| one alternative falsified | NO if legal alternatives remain | NO | NO | continue comparison |
| all legal alternatives falsified | YES | YES | maybe | YES: reopen requirements/assumptions/strategy |
| shared baseline identity uncertain | YES | YES | YES | after baseline authority resolution |
| presentation output fails readback | YES for release | NO for unrelated production | NO | repair presentation only |

Reframing is legal only when it does not silently weaken a requirement/constraint or hide a failed claim.

---

## 13. Validator additions for P2 v1.1

- `P2/DECQ-M01`: consequential Decision Question must pass all eight quality tests.
- `P2/STATE-M01`: Project `ACTIVE` requires at least one executable Workstream under valid Authority Snapshot.
- `P2/HOLD-M01`: local blocker cannot globalize to Project HOLD without a listed project-critical propagation basis.
- `P2/LOCK-M01`: same property/scope cannot be both LOCKED and OPEN.
- `P2/SCOPE-M01`: mutation-budget escalation must occur before higher-class mutation.
- `P2/DEP-M01`: OPEN_NONBLOCKING requires explicit claim ceiling and reopen/due trigger.
- `P2/LIFE-M01`: DISPOSITIONED cannot close before implementation/readback obligations where consequential.
- `P2/FORK-M01`: multiple alternatives cannot share implicit Current status.
- `P2/MERGE-M01`: merged candidate requires new compatibility/readback evaluation.
- `P2/LINEAGE-M01`: reopened decision retains prior lineage and identifies invalidated basis.
- `P2/FPRINT-M01`: material Project State fingerprint mismatch blocks continuation until refresh/recompile.

## 14. P2 v1.1 closure test

Second-pass P2 is ready for validator compilation when a test suite can distinguish:
- task versus Decision Question;
- local BLOCKED versus Project HOLD;
- Open versus Locked versus Protected;
- legitimate concurrency versus hidden coupling;
- legal scope expansion versus unauthorized mutation;
- disposition versus actual closure;
- forked candidate versus multiple Current;
- reopen lineage versus overwritten history.
