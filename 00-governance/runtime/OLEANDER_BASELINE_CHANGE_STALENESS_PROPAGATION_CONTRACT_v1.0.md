# OLEANDER Baseline / Change / Staleness Propagation Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P5**. Applies mainly to the `PROJECT` plane while producing `RUNTIME_CONTROL` reopen/stale obligations. It deepens existing change-impact and selective-readback logic; it does not create a parallel configuration database.

## 1. Purpose

A complex project is not controlled merely because files have versions.

The system must know:
- which configuration is approved Current for a scope;
- which objects are configuration-controlled;
- what change has been proposed/accepted;
- what downstream objects/claims/evidence become stale;
- which prior PASS/KEEP/receipt remains historical but no longer Current;
- what must be rerun before a replacement can be promoted.

Core invariant:

`VERSION HISTORY ≠ CONFIGURATION CONTROL`.

`NEWER FILE ≠ CURRENT BASELINE`.

`LOCAL CHANGE ≠ LOCAL CONSEQUENCE`.

## 2. Configuration-controlled object threshold

Mark an object `configuration_controlled = true` when any applies:

- it is Current source authority for a material project truth;
- it is referenced by a Requirement/Interface/Decision/Assurance result;
- it carries a locked Controlled Variable;
- multiple downstream consumers depend on its exact version;
- it forms part of a promoted project claim;
- changing it can invalidate a material review/gate;
- historical reproducibility/audit is required.

Do not configuration-control every scratch file.

## 3. Baseline object

A `BASELINE` is an approved immutable configuration set for a defined scope.

It answers:

`What exact set of Project objects/revisions is the approved reference for this scope at this point?`

## 4. Baseline types

Controlled set:

`PROJECT | DESIGN | GEOMETRY | TECHNICAL | DATA | CONTENT | BRAND_LANGUAGE | INTEGRATION | ASSURANCE_CONFIGURATION | DELIVERY_RELEASE | OTHER_CONTROLLED`.

A Project may have multiple non-conflicting Current baselines at different scopes. Do not force one giant baseline when scoped baselines are more precise.

## 5. Baseline minimum contract

```yaml
baseline_id:
project_id:
baseline_type:
scope_in: []
scope_out: []
included_objects:
  - object_id:
    revision:
    digest_or_version:
    role:
authority_snapshot_ref:
approval_authority:
approval_decision_ref:
approval_date:
requirements_snapshot: []
constraints_snapshot: []
controlled_variables_snapshot: []
critical_interfaces_snapshot: []
assumptions: []
open_items: []
claim_ceiling_ref:
reopen_triggers: []
supersedes:
status:
```

## 6. Baseline state

`CANDIDATE → APPROVED → CURRENT → SUPERSEDED`.

Hard rules:

- `APPROVED` baseline content is immutable;
- changing one included object does not edit the historical baseline; it creates a Change and later a replacement baseline when approved;
- only one Current baseline may control the same property/scope unless an explicit branch/variant authority exists;
- superseded baseline remains traceable and may support historical evidence only for its own configuration;
- rollback is implemented as an authorized new Change/baseline selection, not history deletion.

## 7. Baseline open items

A baseline may contain explicit open items only when:

- they do not invalidate the stated claim ceiling;
- owner/resolution route is explicit;
- the open item is not hidden from downstream consumers;
- promotion authority accepts the bounded scope.

`OPEN ITEM` cannot be used to hide a Critical authority/safety/interface contradiction.

## 8. Change object

A `CHANGE` is the auditable semantic record for a proposed material alteration to one or more controlled Project objects.

Minimum contract:

```yaml
change_id:
project_id:
change_type:
proposed_change:
reason:
initiator:
authority_snapshot_ref:
source_baseline_refs: []
affected_objects: []
affected_requirements: []
affected_constraints: []
affected_variables: []
affected_interfaces: []
affected_decisions: []
affected_artifacts: []
affected_evidence: []
affected_assurance: []
affected_claims: []
affected_presentations: []
risk_impact: []
dependency_impact: []
impact_class:
implementation_plan:
rollback_or_containment_plan:
approval_authority:
approval_decision_ref:
implementation_refs: []
readback_plan: []
reassurance_obligations: []
resulting_baseline_ref:
status:
```

## 9. Change types

`CORRECTION | DESIGN_CHANGE | REQUIREMENT_CHANGE | CONSTRAINT_CHANGE | VARIABLE_CHANGE | INTERFACE_CHANGE | DATA_CHANGE | CONTENT_CHANGE | AUTHORITY_CHANGE | TOOL_ENVIRONMENT_CHANGE | RELEASE_CHANGE | OTHER_CONTROLLED`.

Change type describes what changed; impact class describes consequence.

## 10. Change lifecycle

`PROPOSED → IMPACT_ASSESSED → APPROVED | REJECTED → IMPLEMENTED → VERIFIED → CLOSED`.

Meanings:

- `PROPOSED` — change described, impact not yet trusted;
- `IMPACT_ASSESSED` — material affected set and required reopen/readback identified;
- `APPROVED` — authorized to implement, not yet proven successful;
- `IMPLEMENTED` — mutation executed against named target configuration;
- `VERIFIED` — required readback/re-assurance confirms the intended change and bounded consequences;
- `CLOSED` — resulting states/baselines/promotion obligations reconciled;
- `REJECTED` — proposal not authorized; retain rationale/history.

## 11. Impact classes

Retain:

- `NON_MATERIAL`
- `LOCAL_MATERIAL`
- `INTERFACE_MATERIAL`
- `COUPLED_SYSTEM`
- `PROMOTION_BREAKING`

Classification is by consequence, not file size, edit count or author discipline.

### NON_MATERIAL
No change to semantic project truth, controlled variable, requirement, acceptance condition, authority, claim or source geometry/data.

Typical: typo, metadata correction, presentation-only alignment change.

### LOCAL_MATERIAL
Material project change inside one bounded owner/object with no consumed shared variable/interface/claim consequence.

### INTERFACE_MATERIAL
Changes an exchanged variable, tolerance, authority, behavior or acceptance condition used across an Interface.

### COUPLED_SYSTEM
Propagates across multiple Interfaces/subsystems or alters a system success condition.

### PROMOTION_BREAKING
Invalidates the basis of a Current promoted claim, baseline, assurance decision, integration receipt or released source authority.

## 12. Impact assessment algorithm

For every material proposed change:

1. identify changed semantic object/property;
2. resolve current baseline/configuration;
3. enumerate direct typed consumers;
4. enumerate material second-order consumers until propagation boundary is proven;
5. inspect Controlled Variables and Interfaces;
6. inspect Requirements/Constraints/Decisions;
7. inspect Evidence/Assurance applicability;
8. inspect promoted Claims and released Presentations;
9. assign impact class;
10. define stale/reopen consequence per affected object;
11. define required owner/readback/re-assurance;
12. obtain approval authority.

Unknown material dependency graph = impact assessment incomplete.

## 13. Staleness state for affected objects

Do not overwrite each object's native state machine with one universal `STALE` field.

Use an orthogonal validity disposition:

`CURRENT_VALID | RECHECK_REQUIRED | REOPEN_REQUIRED | INVALID_FOR_CURRENT_CLAIM | HISTORICAL_ONLY`.

Examples:

- old evidence for superseded geometry → `HISTORICAL_ONLY`;
- interface after a variable change → `REOPEN_REQUIRED`;
- visualization after color-token change → perhaps `RECHECK_REQUIRED`;
- safety verification after requirement change → `INVALID_FOR_CURRENT_CLAIM` until rerun.

## 14. Propagation graph

Material change propagation uses typed edges:

`CHANGE → changed object/property → consumers → Interfaces/Dependencies → Artifacts/Decisions → Evidence/Assurance → Claims → Gate/Promotion/Release`.

Do not propagate through generic `related_to` edges unless a material dependency is separately established.

## 15. Propagation boundary proof

A propagation branch may stop only when one of these is explicit:

- downstream object does not consume the changed property;
- tolerance/acceptance range absorbs the change;
- dependency was removed/superseded;
- affected object is outside the current claim scope;
- independent authority confirms no material impact;
- object will be intentionally superseded rather than repaired.

Record the stop reason for Major/Critical propagation branches.

## 16. Reassurance obligation

A Change must not close merely because the edited artifact reopens successfully.

For each affected assurance object, set:

`NO_RERUN_NEEDED_WITH_REASON | REVIEW_APPLICABILITY | PARTIAL_RERUN | FULL_RERUN | NEW_ASSURANCE_REQUIRED`.

Rules:

- requirement target/configuration changed materially → previous verification cannot remain Current without applicability proof;
- field condition changed → lab/simulation result may remain informative but cannot prove current field state;
- interface acceptance condition changed → interface assurance reopens;
- evidence transformation only changed presentation carrier without changing evidence semantics → recheck projection, not necessarily source evidence.

## 17. Promotion-breaking behavior

When impact class = `PROMOTION_BREAKING`:

- affected Current promotion state becomes `REOPEN_REQUIRED` or invalid for stated scope;
- associated runtime receipt becomes stale;
- release/presentation must not continue presenting the old claim as Current;
- a new promotion decision is required after repair/readback/re-assurance;
- historical promoted state remains in lineage.

No silent “patch and keep Current” behavior.

## 18. Authority change special case

`AUTHORITY_CHANGE` automatically requires P1 `RB4`.

Examples:
- change Current carrier pointer;
- change decision/change authority;
- modify Root/Project authority semantics;
- reassign baseline Current pointer;
- change object identity/namespace mapping.

Authority Change cannot be classified `NON_MATERIAL` merely because no design geometry changed.

## 19. Cross-platform baseline pointers

When Current state is mirrored across Notion/GitHub/Drive/runtime systems:

- one logical Current pointer remains authoritative according to Current governance;
- mirrors must record source authority and revision;
- sync lag creates `RECHECK_REQUIRED`, not a second Current;
- contradictory Current pointers = authority conflict/HOLD;
- pointer repair requires RB4 readback.

## 20. Change collision / concurrency

If two approved/in-flight Changes overlap a controlled property/object:

- detect overlap before implementation;
- identify shared baseline ancestor;
- determine whether changes commute;
- if non-commuting, serialize or reopen both under a joint decision;
- never let last writer silently win.

Optimistic concurrency is allowed only when overlap detection and readback are reliable.

## 21. Change rejection and abandoned branches

Rejected/abandoned Change proposals remain traceable when they influenced a consequential Decision.

They do not remain active dependencies unless explicitly referenced.

Candidate artifacts produced only for a rejected change must not be mistaken for Current source authority.

## 22. Validator floor

- `CFG-001` approved baseline immutable;
- `CFG-002` exactly one effective Current baseline per controlled property/scope unless authorized branching;
- `CFG-003` newer artifact cannot replace Current baseline without Change/promotion;
- `CFG-004` superseded baseline evidence historical for superseded configuration;
- `CHG-001` material Change has affected-object set before approval;
- `CHG-002` impact class based on semantic consequence, not file/edit count;
- `CHG-003` unknown material blast radius blocks approval/closure;
- `CHG-004` implemented Change requires readback appropriate to impact;
- `CHG-005` Change closure requires reassurance obligations reconciled;
- `STALE-001` affected objects receive orthogonal validity disposition;
- `STALE-002` invalid/historical evidence cannot support Current claim;
- `PROP-001` propagation follows typed material dependencies;
- `PROP-002` propagation stop for Major/Critical branch requires explicit reason;
- `PROM-001` promotion-breaking change reopens affected promotion/release;
- `AUTHCHG-001` authority change requires RB4 and cannot be NON_MATERIAL;
- `SYNC-001` contradictory cross-platform Current pointers = HOLD;
- `CONC-001` overlapping non-commuting Changes cannot use last-writer-wins.

## 23. P5 closure condition

P5 is sufficiently refined for draft review when baseline immutability/current-pointer semantics, Change lifecycle/impact analysis, orthogonal staleness disposition, typed propagation, reassurance obligations, promotion-breaking behavior and concurrency rules have a machine-readable counterpart.
