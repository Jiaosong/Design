# OLEANDER Need / Requirement / Constraint / Project Claim Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P3**. Applies to the `PROJECT` plane. It does not replace external codes/contracts, Current Project Authority, or Knowledge-plane research objects.

## 1. Core separation

Keep four project semantics distinct:

- `NEED` — a stakeholder/user/operation/project need that should be understood and validated;
- `REQUIREMENT` — a bounded statement of what must be satisfied and verified;
- `CONSTRAINT` — a controlling boundary not freely traded away by ordinary design optimization;
- `PROJECT_CLAIM` — a proposition the project currently intends to assert about a design/result/performance/state.

Hard rule:

`NEED ≠ REQUIREMENT ≠ CONSTRAINT ≠ CLAIM`.

A sentence may imply more than one of these, but then it should be split into separate objects linked by typed relations.

## 2. Need contract

A Need describes a desired outcome, problem, capability, experience or condition from the perspective of a stakeholder/operation/project objective.

Minimum fields:

```yaml
need_id:
project_id:
need_type:
statement:
stakeholder_or_origin:
context:
problem_or_desired_outcome:
importance:
source_refs: []
evidence_refs: []
conditions: []
conflicts: []
owner:
validation_route:
status:
supersedes:
```

Need types:

`STAKEHOLDER | USER | OPERATIONAL | BUSINESS | CIVIC | EXPERIENCE | SAFETY | MAINTENANCE | DELIVERY | RESEARCH | OTHER_CONTROLLED`.

Need state:

`CAPTURED → ANALYZED → AGREED → BASELINED → VALIDATED_FOR_SCOPE | REVISED | WITHDRAWN | SUPERSEDED`.

A Need may remain qualitative. Do not force every Need into a number simply to make it look verifiable.

## 3. Requirement contract

A Requirement translates an authorized Need, external mandate, parent requirement or project decision into a statement precise enough to trace and verify.

Minimum fields:

```yaml
requirement_id:
project_id:
requirement_type:
statement:
subject:
source_need_or_parent_refs: []
external_mandate_refs: []
conditions: []
required_value_or_condition:
unit:
tolerance:
acceptance_criteria:
verification_method:
verification_level:
verification_owner:
definition_owner:
change_authority:
priority:
rationale:
assumptions: []
constraints: []
satisfied_by: []
verified_by: []
baseline_ref:
version:
status:
```

Requirement types:

`FUNCTIONAL | PERFORMANCE | INTERFACE | SPATIAL | HUMAN_FACTORS | ACCESSIBILITY | SAFETY | OPERATIONAL | MAINTENANCE | DATA_INFORMATION | MATERIAL_CMF | ENVIRONMENTAL | SECURITY_PRIVACY | DELIVERY | REGULATORY_DERIVED | OTHER_CONTROLLED`.

## 4. Requirement quality gate

A consequential Requirement should satisfy all applicable tests.

### Singular responsibility
One primary obligation. If independent parts could pass/fail separately, split them.

### Identifiable subject
The thing that must satisfy the requirement is explicit.

### Bounded condition
The context, state, load, user, scenario or operating condition is explicit when it changes meaning.

### Verifiable
A verification method and acceptance criterion can be defined.

### Necessary
It traces to a Need, parent Requirement, external mandate or authorized Project Decision.

### Feasible enough to baseline
No known contradiction makes the requirement impossible under Current scope, unless explicitly accepted as unresolved/high-risk.

### Unambiguous enough for the decision
Avoid undefined adjectives such as `adequate`, `premium`, `intuitive`, `safe`, `fast`, `high quality`, `accessible`, `robust` unless the project defines how they will be judged.

### Solution-neutral where possible
Do not encode an implementation choice as a Requirement unless that implementation is itself an authorized constraint/decision.

## 5. Requirement statement pattern

Preferred pattern when applicable:

`SUBJECT + SHALL/MUST + REQUIRED CONDITION/CAPABILITY + UNDER CONDITIONS + ACCEPTANCE BOUNDARY`.

Example:

`The primary south-entry accessible route shall maintain a clear passage width ≥ X under the approved door-open condition, verified against the Current geometry baseline.`

Do not force this grammar on user-facing Needs or narrative Claims.

## 6. Requirement lifecycle

`DRAFT → ANALYZED → AGREED → BASELINED → SATISFIED_PENDING_ASSURANCE → VERIFIED | FAILED → SUPERSEDED`.

Rules:

- `AGREED` means stakeholders/authority accepted the requirement statement, not that the design satisfies it;
- `BASELINED` freezes the requirement version under change control;
- `SATISFIED_PENDING_ASSURANCE` means the design appears to implement it but formal verification is not yet closed;
- `VERIFIED` requires an Assurance Activity + accepted evidence for this exact requirement/configuration;
- `FAILED` is a valid state and must not be deleted;
- materially changed Requirement creates a new version/reopens downstream assurance.

## 7. Verification route

Before a consequential Requirement can be baselined, define at least one verification route:

`INSPECTION | ANALYSIS | DEMONSTRATION | TEST | MEASUREMENT | REVIEW | MODEL_CHECK | DOCUMENT_CHECK | COMBINATION`.

Verification route must also name:
- target configuration;
- required environment/condition;
- result type;
- acceptance boundary;
- responsible owner;
- evidence carrier.

A method label without conditions and acceptance criteria is not a complete verification route.

## 8. Requirement Validation vs Product Validation

Keep two meanings separate.

### Requirement validation
Question:
`Is this the right requirement to represent the underlying Need/mandate?`

Typical evidence:
- stakeholder review;
- scenario analysis;
- contradiction check;
- requirement quality review;
- operational reasoning.

### Product/system validation
Question:
`Does the realized design/system satisfy the Need/intended use in the real or representative use context?`

Requirement verification alone cannot answer product validation.

## 9. Constraint contract

A Constraint is a controlling boundary that ordinary design trade-off cannot silently relax.

Minimum fields:

```yaml
constraint_id:
project_id:
constraint_type:
statement:
source_authority:
source_locator:
scope:
affected_objects: []
condition:
required_boundary:
exception_rule:
waiver_or_deviation_authority:
effective_from:
effective_to:
change_or_expiry_trigger:
status:
```

Constraint types:

`REGULATORY | CONTRACTUAL | CLIENT_LOCK | SITE | GEOMETRIC | BUDGET | SCHEDULE | RIGHTS_LICENSE | SAFETY | ACCESSIBILITY | MATERIAL_AVAILABILITY | EXISTING_CONDITION | TOOL_ENVIRONMENT | AUTHORITY_BOUNDARY | OTHER_CONTROLLED`.

Constraint state:

`PROPOSED → CONFIRMED → ACTIVE → WAIVED_WITH_AUTHORITY | EXPIRED | SUPERSEDED`.

## 10. Constraint rules

- A Constraint must name its source authority or explicitly remain `PROPOSED/UNCONFIRMED`.
- `REFERENCE` or precedent does not automatically become a Constraint.
- A project preference is not a regulatory Constraint.
- An external mandate may include an authorized exception/waiver route; ordinary design preference cannot invent one.
- Constraint conflicts require authority resolution; do not average or trade them away with weighted scoring.
- Expired/superseded Constraint must stop constraining new Current work, but remain in lineage.

## 11. Waiver / Deviation boundary

Use a Project-plane `WAIVER` or `DEVIATION` when a controlling Requirement/Constraint is intentionally varied under authorized conditions.

Minimum relation:

`Requirement/Constraint → waived/deviated by → authorized WAIVER/DEVIATION → affected objects → evidence/risk basis → expiry/review trigger`.

No informal note can substitute for this when the variance is material.

## 12. Project Claim contract

A Project Claim is an assertion the project currently makes or wants to make about a Project object, result, behavior, performance, value or state.

Minimum fields:

```yaml
claim_id:
project_id:
claim_type:
statement:
target_object_refs: []
source_requirement_need_refs: []
supporting_evidence_refs: []
contradicting_evidence_refs: []
bounding_evidence_refs: []
conditions: []
uncertainties: []
does_not_establish: []
claim_ceiling_ref:
owner:
review_authority:
status:
last_verified_at:
reopen_triggers: []
```

Claim types:

`FACTUAL_STATE | DESIGN_INTENT | COMPLIANCE | PERFORMANCE_PREDICTION | TECHNICAL_FIT | USER_EXPERIENCE | FIELD_CONDITION | OPERATIONAL_OUTCOME | VALUE_BENEFIT | RESEARCH_INTERPRETATION | PRESENTATION_MESSAGE | OTHER_CONTROLLED`.

## 13. Claim state

`PROPOSED → SUPPORTED → REVIEWABLE → PROMOTED → REOPENED | REJECTED | SUPERSEDED`.

`PROMOTED` always means promoted for a named scope/ceiling. It does not mean universally true.

## 14. Claim–Evidence binding

A consequential Claim must resolve to explicit evidence relations:

- `SUPPORTED_BY`
- `CONTRADICTED_BY`
- `BOUNDED_BY`

For each evidence relation, preserve:
- direct/indirect/contextual role;
- configuration/version;
- conditions;
- evidence strength;
- confidence;
- what the evidence does **not** establish.

Several weak sources do not automatically become strong evidence.

## 15. Claim ceiling application

A Claim cannot exceed the independent ceilings defined in P1.

Examples:

- simulation can support `PERFORMANCE_PREDICTION` but not automatically `FIELD_CONDITION`;
- visual rendering can support design-intent/appearance claims but not structural compliance;
- machine geometry checks can support bounded dimensional fit but not user experience;
- stakeholder preference evidence does not automatically prove long-term operational outcome;
- manufacturer data can support product-property context but does not prove project-specific installed performance without applicability evidence.

## 16. Need → Requirement → Design → Assurance → Validation chain

Preferred trace:

`NEED → derives REQUIREMENT → satisfied_by SYSTEM_ELEMENT / CONTROLLED_VARIABLE / BEHAVIOR → verified_by ASSURANCE → contributes_to NEED/INTENDED-USE VALIDATION`.

Do not collapse the chain to:

`Need → drawing → PASS`.

## 17. Requirement conflict classes

When Requirements conflict, classify the conflict before trade-off:

- `HARD_CONSTRAINT_CONFLICT` — cannot be traded without authority/waiver;
- `REQUIREMENT_REQUIREMENT_CONFLICT` — two authorized requirements cannot both be satisfied as written;
- `RESOURCE_TRADEOFF` — both remain valid but optimization is needed;
- `INTERFACE_CONFLICT` — different owners/objects impose incompatible conditions;
- `AMBIGUITY_CONFLICT` — wording/ownership unclear rather than technically incompatible;
- `STALE_REQUIREMENT_CONFLICT` — one requirement belongs to superseded configuration.

Only the valid conflict class determines the repair path.

## 18. Change impact

Material Requirement/Constraint/Claim changes must identify affected:

- System Elements;
- Controlled Variables;
- Interfaces;
- Decisions;
- Artifacts;
- Evidence;
- Assurance Activities/Decisions;
- Baselines;
- Presentation claims if already released.

Previously passing assurance becomes historical for the superseded target when the changed condition invalidates applicability.

## 19. Source-strength boundary

Use source classes without turning them into automatic truth scores.

Potential sources:
- law/regulator/contract;
- approved client/project authority;
- standard/code;
- measured field evidence;
- verified project model/data;
- peer-reviewed research;
- manufacturer/product documentation;
- precedent/case;
- user quote/interview;
- design assumption;
- AI-generated suggestion.

Source class and claim confidence remain separate.

## 20. Failure modes

Fail/HOLD when:

- Requirement has no traceable origin and is presented as mandatory;
- Requirement bundles independent obligations that can pass/fail separately;
- acceptance criterion is missing for a consequential baselined Requirement;
- verification method is named but conditions/configuration are undefined;
- precedent/reference is promoted into Constraint without authority;
- an implementation choice is hidden inside a supposedly solution-neutral Requirement without authorization;
- Requirement changes but old PASS is carried forward without re-assurance;
- Project Claim lacks evidence/ceiling appropriate to its type;
- contradiction is hidden instead of bound to the Claim;
- compliance/field/operational Claim is inferred from a lower evidence class.

## 21. Validator floor

- `NEED-001` Need has identifiable origin/stakeholder/context;
- `NEED-002` Need validation distinct from requirement verification;
- `REQ-001` Requirement has one primary obligation or is split;
- `REQ-002` consequential Requirement traces to Need/parent/external mandate/authorized Decision;
- `REQ-003` consequential baselined Requirement has acceptance criteria + verification route;
- `REQ-004` Requirement state cannot become VERIFIED without Assurance Activity + accepted evidence;
- `REQ-005` material Requirement change reopens affected assurance;
- `REQ-006` implementation choice cannot masquerade as Requirement without authorized basis;
- `CON-001` active Constraint has source authority;
- `CON-002` Reference/Precedent cannot self-promote to Constraint;
- `CON-003` material variance from Constraint requires authorized Waiver/Deviation;
- `CLM-001` consequential Claim has explicit evidence bindings;
- `CLM-002` Claim type compatible with claim ceiling/evidence class;
- `CLM-003` contradictions/bounds cannot be silently dropped;
- `CLM-004` promoted Claim scope/conditions/ceiling explicit;
- `TRACE-001` Need→Requirement→Design→Assurance trace preserved for material claims;
- `TRACE-002` previous assurance not reusable after material target/configuration change without applicability proof.

## 22. P3 closure condition

P3 is sufficiently refined for draft review when Need, Requirement, Constraint and Project Claim have separate contracts/state machines, Requirement atomicity/verification/validation rules are explicit, claim-evidence/ceiling rules are machine-readable, and change/conflict propagation is defined.
