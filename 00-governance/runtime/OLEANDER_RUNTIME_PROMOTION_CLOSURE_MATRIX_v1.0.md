# OLEANDER Runtime Promotion / Closure Matrix v1.0

Status: **DRAFT GOVERNANCE EXTENSION**. This matrix defines when a runtime object may become authoritative/current for its scope and when it may be closed. Promotion and closure are separate decisions.

## 1. Core distinction

`PROMOTION` asks: **may this object become a controlling/current project record for the declared scope?**

`CLOSURE` asks: **is there no remaining in-scope work required for this object under its current claim/configuration?**

Therefore:

- a promoted object may still be OPEN;
- a closed object may be historical and not Current;
- `CLOSED ≠ PROMOTED`;
- `PROMOTED ≠ VERIFIED`;
- `VERIFIED ≠ VALIDATED`;
- `BASELINED ≠ FIELD-PROVEN`.

## 2. Promotion / closure matrix

| Object Type | Minimum promotion state | Promotion prerequisites | Closure prerequisites | Reopen / stale triggers |
|---|---|---|---|---|
| INTENT | AGREED / BASELINED | current authority, scope, rationale, project linkage | superseded/retired only by authority | authority/scope change |
| NEED | AGREED / BASELINED | stakeholder/source provenance, interpretation boundary, owner | withdrawn/superseded under authority | new stakeholder evidence / scope change |
| REQUIREMENT | BASELINED | valid derivation/source, testable statement, owner/change authority, verification route, baseline | VERIFIED or formally waived/deviated/superseded | requirement/source/config/change impact |
| CONSTRAINT | CONFIRMED / ACTIVE | valid authority/source, applicability, owner, version/date | expired/superseded/authorized waiver-deviation | authority/version/scope change |
| CLAIM | REVIEWABLE / PROMOTED | evidence chain, contradictions, uncertainty, scope, claim ceiling, authority | superseded/rejected; otherwise remains active claim | new contradictory evidence/config change |
| SYSTEM_ELEMENT | DEFINED / COORDINATED / BASELINED | identity, system position, owners, requirements/interfaces as applicable | ACCEPTED_FOR_SCOPE or superseded | requirement/interface/variable/change |
| BEHAVIOR_STATE_MODEL | COORDINATED / EXERCISED / VERIFIED | target system, state/behavior definition, linked requirements, readback plan | VERIFIED for behavior claim, or superseded | behavior requirement/input/config change |
| CONTROLLED_VARIABLE | COORDINATED / BASELINED | one current change authority, value/range/unit/tolerance as applicable, consumers/interfaces, baseline | superseded only; active variable is not “closed” | accepted material change/source authority change |
| WORK_PACKAGE | READY / IN_PROGRESS | owner, scope, inputs/outputs, dependencies, acceptance definition | ACCEPTED_FOR_SCOPE and all required child/output obligations reconciled | reopened dependency/change/new scope |
| TASK | READY / IN_PROGRESS | owner, task definition, input/dependency visibility | DONE + required output/readback accepted | failed readback/change/new dependency |
| ARTIFACT | REVIEWABLE / ACCEPTED_FOR_SCOPE / BASELINED | resolvable carrier, provenance/version, declared purpose, owner, relevant semantic links | superseded/withdrawn or accepted for finite scope | represented semantic object/change/baseline change |
| INTERFACE | required maturity for current claim | sides, owner(s), integration owner for major/critical, authority, shared variables/exchanges, acceptance contract when required | disposition CLOSED + maturity >= required_maturity + no in-scope blocker | side/variable/authority/acceptance/change |
| MATERIAL_DEPENDENCY | DEFINED / ACTIVE | provider, consumer, payload/condition, owner, reopen rule | SATISFIED_FOR_SCOPE | provider input/config change |
| DECISION | DECIDED | authority, question, alternatives where material, rationale, evidence/assumptions, locked/open variables, reopen trigger | IMPLEMENTED + required verification/readback, or superseded/rejected | evidence/assumption/config/change invalidates basis |
| WAIVER | APPROVED / ACTIVE | target, authority, rationale, scope, risk/evidence basis, expiry/review trigger | expired/closed/superseded after obligations met | condition/authority/risk change |
| DEVIATION | APPROVED / ACTIVE | target, authority, rationale, scope, risk/evidence basis, correction/expiry route | closed after authorized deviation period/condition ends | condition/config/risk change |
| ACTOR | ACTIVE | identity, role/project linkage | retired/suspended only | assignment change |
| AUTHORITY_ROLE | ACTIVE | scope, delegated authority, precedence | retired/superseded | governance/authority change |
| RISK | EVALUATED | owner, affected objective/object, analysis/evaluation, treatment/acceptance basis | CLOSED or ACCEPTED with residual-risk rationale and evidence | trigger recurrence/new evidence/change |
| ISSUE | ROOT_CAUSE_CONFIRMED / REPAIRED | owner, affected objects, evidence, root cause for material issue, repair route | RETESTED + CLOSED for material issues | regression/reoccurrence/new evidence |
| ASSUMPTION | ACTIVE | explicit statement, owner, dependencies, claim ceiling, confirmation/refutation/expiry trigger | CONFIRMED / REFUTED / EXPIRED | evidence/change invalidates assumption |
| UNKNOWN | INVESTIGATING | owner, scope, investigation route, affected claim/decision | RESOLVED or OUTSIDE_CLAIM with explicit exclusion | new scope / claim expansion |
| EVIDENCE_RECORD | CHECKED / ACCEPTED_FOR_USE | provenance, method, condition, integrity check, applicability | stale/rejected/superseded only; evidence itself is not “closed” | source/config/time validity changes |
| ASSURANCE_ACTIVITY | READY / EXECUTED / ANALYZED | target, criteria, method, configuration, owner/reviewer, evidence plan | PASS/FAIL/INCONCLUSIVE analyzed and formally closed | target/config/evidence changes |
| ASSURANCE_DECISION | ISSUED / ACCEPTED | activity, evidence, per-target result, authority/reviewer, scope/claim ceiling | superseded/withdrawn or accepted as historical final decision | re-assurance trigger/new evidence/config change |
| BASELINE | APPROVED / CURRENT | enumerated included revisions/objects, authority, scope, date/version | SUPERSEDED by new approved baseline | approved change creates successor |
| CHANGE | APPROVED / IMPLEMENTED / VERIFIED | reason, owner, impact assessment, authority, affected objects, reopen plan | VERIFIED + all required downstream re-assurance/retests closed | implementation failure/new impact discovery |

## 3. Promotion tiers

Promotion should not be binary. Use the minimum tier appropriate to the object:

### T0 — WORKING

- editable / incomplete;
- not controlling;
- may contain open assumptions/unknowns;
- cannot be cited as current authority.

### T1 — REVIEWABLE

- identity and primary semantic class resolved;
- minimum metadata present;
- enough content/state to review;
- open issues visible.

### T2 — CONTROLLED CANDIDATE

- owner/authority resolved;
- relevant relation contracts satisfied;
- configuration/version known;
- evidence/assumption boundary explicit;
- eligible for formal decision/promotion.

### T3 — CURRENT / BASELINED FOR SCOPE

- explicitly approved/promoted by correct authority;
- included in controlling baseline/current register when applicable;
- downstream consumers may rely on it within the declared claim ceiling.

### T4 — ASSURED CURRENT

- T3 plus required verification/validation/acceptance evidence for the stated claim;
- all material reopened dependencies/interfaces resolved for that claim.

T4 does not imply field/operational proof unless field/operational validation was actually part of the assurance contract.

## 4. Closure classes

Use closure semantics appropriate to the object rather than one generic `DONE`:

- `SATISFIED` — obligation/dependency is met for scope;
- `VERIFIED` — specified acceptance requirement passed assurance;
- `VALIDATED` — intended-use/need claim passed validation;
- `ACCEPTED` — authority accepts a decision/artifact/result for scope;
- `RESOLVED` — issue/unknown no longer requires in-scope work;
- `CLOSED` — governance/work object has no remaining in-scope action;
- `SUPERSEDED` — no longer current because a successor is controlling;
- `OUTSIDE_CLAIM` — intentionally excluded, not solved.

These words are not interchangeable.

## 5. Promotion hard blockers

No object may reach T3/T4 when any applicable blocker remains:

1. primary semantic class unresolved;
2. identity/canonical collision unresolved;
3. current authority/change authority conflict;
4. required relation missing;
5. required source/provenance missing;
6. material assumption/unknown hidden or unlabeled;
7. open critical interface below required maturity;
8. requirement has no verification route where one is required;
9. evidence is stale/rejected for the intended claim;
10. current baseline/configuration mismatch;
11. approved material change has unresolved downstream reopen obligations;
12. unresolved Critical/Major independent review objection when independent review is required;
13. claim strength exceeds evidence/assurance ceiling;
14. validation is inferred from verification-only evidence;
15. required field/operational evidence is absent but the object claims field/operational validity.

## 6. Closure hard blockers by family

### Purpose / obligation

- Requirement cannot close as verified without accepted assurance.
- Constraint cannot close merely because the team decided to ignore it; use waiver/deviation authority.
- Claim cannot be closed by formatting/publication alone.

### System definition

- System Element cannot be accepted for scope while critical required interfaces are unresolved.
- Controlled Variable is not “closed” while active; it is controlled/current or superseded.

### Work / artifact

- Work Package cannot close while mandatory child outputs or dependencies remain open.
- Task cannot close when required output/readback failed.
- Artifact cannot grant semantic closure to represented objects.

### Coupling

- Interface cannot close below required maturity.
- Tight coupling cannot close on discipline-isolated review only.
- Material dependency cannot close without provider-consumer satisfaction evidence.

### Decision / governance

- Decision cannot close at `DECIDED` if implementation/readback is part of its acceptance contract.
- Waiver/deviation cannot remain indefinitely ACTIVE without expiry/review control.

### Uncertainty / problem

- Risk cannot close because likelihood was judged low; residual risk must be accepted or treatment/retirement justified.
- Material Issue cannot close before repair + required retest.
- Assumption cannot close as confirmed without evidence; expiry is not confirmation.
- Unknown `OUTSIDE_CLAIM` is exclusion, not resolution.

### Evidence / assurance

- Evidence cannot be promoted beyond its actual method/condition.
- Assurance Activity cannot PASS without target + criteria + evidence + analysis.
- Assurance Decision cannot outlive a materially changed target/configuration without revalidation.

### Configuration / change

- Baseline history cannot be overwritten.
- Change cannot close before required downstream re-assurance is complete.

## 7. Reopen propagation matrix

| Trigger | Must reopen / stale at minimum |
|---|---|
| Requirement change | satisfying system elements, controlled variables, affected interfaces, artifacts, verification activities, decisions/baselines relying on it |
| Constraint/authority change | affected requirements, decisions, waivers/deviations, baseline/configuration |
| Controlled-variable change | all registered consumers, relevant interfaces, artifacts, assurance activities/results |
| Interface acceptance change | interface sides, integrated prototype/readback, assurance decision |
| System-element geometry/behavior change | dependent elements, interfaces, artifacts, requirements assurance, baseline |
| New contradictory evidence | claims, decisions, assumptions, assurance decisions using prior evidence |
| Material Issue / regression | repaired object, prior decision, affected baseline, assurance evidence |
| Approved material Change | all affected objects from impact graph plus required downstream gates |
| Intended-use scenario change | validation plan/activity/decision, related needs/claims |
| Baseline replacement | consumers referencing old baseline if not explicitly version-pinned |

`LOCAL CHANGE ≠ LOCAL CONSEQUENCE` remains a hard rule.

## 8. Promotion receipt

Every T3/T4 promotion should produce or update a compact receipt containing:

```yaml
object_id:
object_type:
promotion_tier:
current_state:
scope:
claim_ceiling:
authority:
baseline_ref:
required_relations_ok:
required_evidence_refs:
open_assumptions:
open_unknowns:
open_interfaces:
independent_review_state:
promotion_decision:
promoted_at:
reopen_triggers:
```

The receipt is a runtime governance record, not a replacement for the object itself.

## 9. Closure receipt

For consequential closure, retain:

```yaml
object_id:
closure_semantic: SATISFIED|VERIFIED|VALIDATED|ACCEPTED|RESOLVED|CLOSED|SUPERSEDED|OUTSIDE_CLAIM
closure_scope:
closure_basis:
evidence_refs:
authority:
residual_risk:
remaining_outside_claim:
baseline_or_configuration:
closed_at:
reopen_trigger:
```

## 10. Validator minimum rules

- `PROM-001` no T3/T4 with unresolved authority conflict.
- `PROM-002` no T3/T4 above claim/evidence ceiling.
- `PROM-003` no current controlled variable without exactly one active change authority.
- `PROM-004` no assured-current requirement without assurance PASS.
- `PROM-005` no assured-current validation claim from verification-only route.
- `CLOSE-001` no Interface CLOSED below required maturity.
- `CLOSE-002` no Major/Critical Issue CLOSED before required retest.
- `CLOSE-003` no material Change CLOSED before downstream re-assurance closure.
- `CLOSE-004` no Work Package CLOSED with mandatory child/output obligation open.
- `CLOSE-005` no Baseline overwrite; closure occurs by supersession.
- `REOPEN-001` material accepted change must produce affected/reopened object set.
- `REOPEN-002` stale evidence must invalidate dependent promotion where evidence is material.
- `REOPEN-003` superseded baseline must not remain controlling for unversioned consumers.