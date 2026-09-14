# OLEANDER Runtime Object × State Allowed Matrix v1.0

Status: **DRAFT GOVERNANCE EXTENSION**. This matrix defines class-specific state machines. Generic `DONE / COMPLETE / APPROVED` must not be used to erase class semantics.

## 1. State-axis separation

A runtime object may carry several independent state axes when applicable:

- `lifecycle_state` — class-specific evolution;
- `disposition` — `OPEN / BLOCKED / CLOSED / OUTSIDE_CLAIM` where applicable;
- `authority_state` — `DRAFT / REVIEWED / APPROVED / CONTROLLED / SUPERSEDED` only when the authority layer needs it;
- `evidence_state` — evidence-specific trust/inspection status;
- `configuration_state` — working/baselined/stale/superseded position;
- `claim_ceiling` — strongest assertion allowed by current evidence.

Hard rule: do not collapse these axes into one status field.

## 2. Object × class-specific state matrix

| Object Type | Allowed lifecycle states | Promotable / authoritative states | Terminal / archival states | Reopen allowed? |
|---|---|---|---|---|
| INTENT | DRAFT → AGREED → BASELINED → ACTIVE | AGREED / BASELINED / ACTIVE | SUPERSEDED / RETIRED | yes, by authority/change |
| NEED | CAPTURED → ANALYZED → AGREED → BASELINED | AGREED / BASELINED | SUPERSEDED / WITHDRAWN | yes |
| REQUIREMENT | DRAFT → ANALYZED → AGREED → BASELINED → SATISFIED_PENDING_ASSURANCE → VERIFIED / FAILED | BASELINED; VERIFIED for verified status | SUPERSEDED | yes |
| CONSTRAINT | PROPOSED → CONFIRMED → ACTIVE | CONFIRMED / ACTIVE | WAIVED_WITH_AUTHORITY / EXPIRED / SUPERSEDED | yes |
| CLAIM | PROPOSED → SUPPORTED → REVIEWABLE → PROMOTED | SUPPORTED / REVIEWABLE / PROMOTED according to claim ceiling | REJECTED / SUPERSEDED | yes; CHALLENGED/REOPENED as event state |
| SYSTEM_ELEMENT | PROPOSED → DEFINED → COORDINATED → BASELINED → IMPLEMENTED → ACCEPTED_FOR_SCOPE | DEFINED+ depending project stage; BASELINED for controlled geometry/system | SUPERSEDED / RETIRED | yes |
| BEHAVIOR_STATE_MODEL | DRAFT → DEFINED → COORDINATED → EXERCISED → VERIFIED → BASELINED | COORDINATED / EXERCISED / VERIFIED / BASELINED according to claim | SUPERSEDED | yes |
| CONTROLLED_VARIABLE | PROVISIONAL → COORDINATED → BASELINED | COORDINATED / BASELINED | SUPERSEDED | yes; CHANGED_REOPENED |
| WORK_PACKAGE | PLANNED → READY → IN_PROGRESS → REVIEW → ACCEPTED_FOR_SCOPE | READY / IN_PROGRESS for active planning; ACCEPTED_FOR_SCOPE for closure | CANCELLED / SUPERSEDED | yes |
| TASK | PLANNED → READY → IN_PROGRESS → REVIEW → DONE | READY / IN_PROGRESS; DONE only with accepted output/readback | CANCELLED / SUPERSEDED | yes |
| ARTIFACT | WORKING → REVIEWABLE → ACCEPTED_FOR_SCOPE → BASELINED | REVIEWABLE / ACCEPTED_FOR_SCOPE / BASELINED | SUPERSEDED / WITHDRAWN | yes; new revision preferred |
| INTERFACE | maturity: IDENTIFIED → DEFINED → COORDINATED → EXERCISED → VERIFIED; disposition separate | required maturity is claim-specific | disposition CLOSED / OUTSIDE_CLAIM; history may be SUPERSEDED | yes; change may reopen |
| MATERIAL_DEPENDENCY | IDENTIFIED → DEFINED → ACTIVE → SATISFIED_FOR_SCOPE | DEFINED / ACTIVE / SATISFIED_FOR_SCOPE | STALE / SUPERSEDED | yes |
| DECISION | OPEN → FRAMED → OPTIONS_READY → EVALUATED → DECIDED → IMPLEMENTED → VERIFIED | DECIDED / IMPLEMENTED / VERIFIED depending decision claim | SUPERSEDED / REJECTED | yes: REOPENED |
| WAIVER | PROPOSED → ASSESSED → APPROVED / REJECTED → ACTIVE | APPROVED / ACTIVE | EXPIRED / CLOSED / SUPERSEDED | yes if conditions change |
| DEVIATION | PROPOSED → ASSESSED → APPROVED / REJECTED → ACTIVE | APPROVED / ACTIVE | EXPIRED / CLOSED / SUPERSEDED | yes |
| ACTOR | CANDIDATE → ACTIVE | ACTIVE | SUSPENDED / RETIRED | yes |
| AUTHORITY_ROLE | CANDIDATE → ACTIVE | ACTIVE | SUSPENDED / RETIRED / SUPERSEDED | yes |
| RISK | IDENTIFIED → ANALYZED → EVALUATED → TREATMENT_PLANNED → TREATED → MONITORED → ACCEPTED / CLOSED | EVALUATED+ when governance complete | CLOSED / ACCEPTED | yes if trigger recurs |
| ISSUE | OPEN → TRIAGED → CONTAINED → ROOT_CAUSE_CONFIRMED → REPAIRED → RETESTED → CLOSED | ROOT_CAUSE_CONFIRMED+ for formal corrective action | CLOSED | yes if regression/reoccurrence |
| ASSUMPTION | PROPOSED → ACTIVE | ACTIVE with owner/ceiling only | CONFIRMED / REFUTED / EXPIRED | yes before terminal evidence |
| UNKNOWN | OPEN → INVESTIGATING | INVESTIGATING | RESOLVED / OUTSIDE_CLAIM | yes |
| EVIDENCE_RECORD | CAPTURED → CHECKED → ACCEPTED_FOR_USE | CHECKED / ACCEPTED_FOR_USE | REJECTED / STALE / SUPERSEDED | recheck, not overwrite |
| ASSURANCE_ACTIVITY | PLANNED → READY → EXECUTED → ANALYZED → PASS / FAIL / INCONCLUSIVE | READY for execution; PASS only after analysis | CLOSED; may be REOPENED | yes |
| ASSURANCE_DECISION | DRAFT → ISSUED → ACCEPTED | ISSUED / ACCEPTED | SUPERSEDED / WITHDRAWN | yes via REOPENED/new decision |
| BASELINE | CANDIDATE → APPROVED → CURRENT | APPROVED / CURRENT | SUPERSEDED | no mutation; new baseline instead |
| CHANGE | PROPOSED → IMPACT_ASSESSED → APPROVED / REJECTED → IMPLEMENTED → VERIFIED → CLOSED | APPROVED / IMPLEMENTED / VERIFIED | REJECTED / CLOSED | new change or reopen before closure |

## 3. Object-specific hard state rules

### INTENT / NEED

- `INTENT ACTIVE` requires current authority and scope.
- `NEED BASELINED` requires source/stakeholder provenance and an agreed interpretation boundary.
- A Need does not become `VERIFIED`; verification belongs to specified requirements.

### REQUIREMENT

`REQUIREMENT BASELINED` requires:

- valid source / derivation;
- unambiguous statement;
- acceptance criterion or verification route for consequential requirements;
- owner/change authority;
- baseline reference.

`REQUIREMENT VERIFIED` requires:

- executed assurance activity;
- accepted evidence;
- per-requirement PASS result;
- no unresolved contradictory evidence that invalidates the pass;
- current configuration match.

A requirement may not transition directly `AGREED → VERIFIED` without baseline/assurance trace when configuration control is applicable.

### CONSTRAINT

- `ACTIVE` means the project is currently bound by it.
- `WAIVED_WITH_AUTHORITY` requires an explicit WAIVER/DEVIATION record and does not alter the original constraint history.
- Expiry must be explicit for time/version-sensitive constraints.

### CLAIM

Claim state is separate from claim confidence and evidence ceiling.

Minimum interpretation:

- `SUPPORTED` = at least one resolvable evidence chain exists;
- `REVIEWABLE` = contradiction, uncertainty, scope and source strength are explicit;
- `PROMOTED` = authorized for the declared project communication/decision scope only.

A promoted claim becomes `REOPENED` or superseded when controlling evidence/configuration changes materially.

### SYSTEM_ELEMENT

- `COORDINATED` means participating disciplines agree current definition; it does not mean implemented or validated.
- `BASELINED` requires inclusion in a controlled baseline.
- `IMPLEMENTED` must describe actual implementation scope; models/renders alone do not grant implementation.

### BEHAVIOR_STATE_MODEL

- `EXERCISED` requires actual flow/state/prototype/readback execution.
- `VERIFIED` requires comparison against explicit expected behavior/requirements.
- If user/intended-use success is claimed, verification alone is insufficient; separate validation is required.

### CONTROLLED_VARIABLE

- `COORDINATED` requires resolved definition owner/change authority and known consumers.
- `BASELINED` requires value/range/unit/tolerance where applicable plus baseline reference.
- Any approved material change moves affected downstream objects into stale/reopened states according to impact analysis.

### WORK_PACKAGE / TASK

- `DONE / ACCEPTED_FOR_SCOPE` requires required outputs to exist and be accepted/read back.
- `BLOCKED` must be a disposition/condition, not a replacement lifecycle state.
- Closing a task does not automatically close its parent work package.

### ARTIFACT

- `REVIEWABLE` requires readable/openable/editable state appropriate to the artifact contract.
- `ACCEPTED_FOR_SCOPE` means artifact quality/fitness for a stated use; it does not grant semantic truth to everything represented.
- `BASELINED` requires inclusion in an approved baseline.
- Superseded artifacts remain immutable evidence of prior configuration.

### INTERFACE

Maturity and disposition must remain separate.

Allowed examples:

- `COORDINATED + OPEN`
- `EXERCISED + BLOCKED`
- `VERIFIED + CLOSED`

Forbidden:

- `CLOSED` below `required_maturity`;
- `VERIFIED` without accepted assurance evidence;
- `CLOSED` while a controlling authority conflict remains unresolved.

### MATERIAL_DEPENDENCY

`SATISFIED_FOR_SCOPE` requires provider/consumer agreement or readback appropriate to the dependency. If provider input changes materially, dependency becomes `STALE` or reopens.

### DECISION

`DECIDED` requires:

- decision question;
- current decision authority;
- alternatives considered when material;
- rationale;
- evidence/assumption/constraint basis;
- affected objects / locked variables;
- reopen trigger.

`VERIFIED` means implemented decision consequences have been read back against the decision acceptance condition. It is not universal project validation.

### WAIVER / DEVIATION

`APPROVED` requires target, authority, rationale, scope, risk basis and expiry/review trigger. `ACTIVE` must not silently change the target requirement/constraint to compliant.

### RISK

- `ANALYZED` requires cause/event/consequence or equivalent risk formulation plus affected objective/object.
- `EVALUATED` requires likelihood/consequence or domain-appropriate qualitative judgment and priority.
- `TREATED` requires actual treatment implementation, not a plan.
- `CLOSED` requires closure evidence or a justified acceptance/retirement basis.

### ISSUE

- `ROOT_CAUSE_CONFIRMED` requires evidence beyond symptom description.
- `REPAIRED` requires the corrective change/action to exist.
- `RETESTED` requires evidence that the actual failure condition was exercised again.
- `CLOSED` is forbidden before required retest for material issues.

### ASSUMPTION

`ACTIVE` requires:

- explicit statement;
- owner;
- objects/decisions relying on it;
- risk/claim ceiling;
- confirmation/refutation or expiry trigger.

Major/Critical assumptions must not remain indefinitely ACTIVE through Pre-Promotion unless explicitly contained outside the promoted claim.

### UNKNOWN

- `INVESTIGATING` requires an owner and investigation route.
- `OUTSIDE_CLAIM` requires explicit scope exclusion; it is not equivalent to resolution.

### EVIDENCE_RECORD

- `CHECKED` means provenance, method, condition and integrity were checked.
- `ACCEPTED_FOR_USE` is claim/scope-specific; evidence may be accepted for one decision and insufficient for another.
- Stale evidence may remain historical but cannot silently support current promotion.

### ASSURANCE_ACTIVITY

Outcome (`PASS / FAIL / INCONCLUSIVE`) is not a generic approval state.

`PASS` requires:

- defined target and acceptance criteria;
- executed method;
- evidence;
- current target/configuration match;
- analyzed result.

### ASSURANCE_DECISION

- `ISSUED` requires per-target result, evidence references, scope/claim ceiling and reviewer/authority.
- `ACCEPTED` means the project accepts the decision for the declared scope.
- If evidence or configuration changes, issue a new/reopened decision rather than rewriting historical assurance.

### BASELINE

- `APPROVED` requires explicit approving authority and enumerated included objects/revisions.
- `CURRENT` means one baseline is controlling for its declared scope.
- Approved/current baselines are immutable; replacement occurs via new baseline + supersession.

### CHANGE

`IMPACT_ASSESSED` requires affected object graph or a documented non-material rationale.

`APPROVED` requires correct change authority.

`IMPLEMENTED` requires actual mutation/readback references.

`VERIFIED` requires all required downstream re-assurance/retests from the impact analysis.

`CLOSED` is forbidden while required reopened objects remain unresolved.

## 4. Generic forbidden state substitutions

Reject at minimum:

- `DONE` used for Requirement, Risk, Interface, Evidence or Assurance Decision;
- `APPROVED` used as a substitute for `VERIFIED`;
- `VERIFIED` used as a substitute for `VALIDATED`;
- `CLOSED` used as proof of evidence sufficiency;
- `CURRENT` used without configuration/authority scope;
- `BASELINED` used for an object that has not been captured in an approved baseline;
- `PASS` used without an assurance target and acceptance criterion;
- `FIELD_VERIFIED` inferred from simulation/model/readback only.

## 5. Reopen precedence

A closed/promoted object must reopen or become stale when any of the following materially changes:

1. controlling authority;
2. baseline/configuration;
3. requirement/constraint;
4. shared controlled variable;
5. interface acceptance contract;
6. source evidence or credible contradiction;
7. intended-use scenario for validation;
8. approved change impact that reaches the object.

Historical states are preserved; reopening creates a new current state/event rather than deleting prior evidence.