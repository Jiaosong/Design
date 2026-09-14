# OLEANDER Controlled Variable / Interface / Material Dependency Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P4**. Applies to the `PROJECT` plane and binds to the existing ACTIVE Cross-Disciplinary Design Integration v1.0. It does not replace discipline-specific engineering standards or create a Cross-disciplinary Knowledge Domain.

## 1. Purpose

Complex projects most often fail at relationships rather than isolated objects.

P4 controls three different semantics:

- `CONTROLLED_VARIABLE` — one value/state/definition consumed by multiple objects and requiring explicit authority;
- `INTERFACE` — an objectified relationship where two or more project elements exchange geometry, information, behavior, responsibility or performance;
- `MATERIAL_DEPENDENCY` — a dependency whose validity/change state is important enough to require ownership, traceability or reopen behavior even when a full interface contract is unnecessary.

Hard rule:

`SHARED VARIABLE ≠ INTERFACE ≠ DEPENDENCY`.

They may be linked, but one cannot substitute for another.

## 2. Controlled Variable

A Controlled Variable becomes an independent Project object when at least one is true:

- multiple owners/consumers depend on it;
- changing it can stale/reopen downstream work;
- it is part of an interface acceptance condition;
- it has independent change authority;
- it is baseline/configuration controlled;
- it supports a promoted claim or requirement;
- history of changes must remain auditable.

Otherwise keep the value as a property of its owning Project object.

## 3. Controlled Variable types

Controlled set:

`GEOMETRIC_DATUM | DIMENSION | TOLERANCE | SPATIAL_CLEARANCE | PERFORMANCE_TARGET | CAPACITY | MATERIAL_PROPERTY | CMF_ROLE | TYPOGRAPHY_ROLE | COLOR_TOKEN | CONTENT_TERM | NAMING | STATE_ENUM | DATA_SCHEMA | INTERACTION_PARAMETER | ENVIRONMENTAL_TARGET | HUMAN_FACTOR_ASSUMPTION | MAINTENANCE_ENVELOPE | SCHEDULE_TARGET | COST_TARGET | OTHER_CONTROLLED`.

Do not turn every parameter into a Controlled Variable object.

## 4. Controlled Variable minimum contract

```yaml
variable_id:
project_id:
variable_type:
semantic_name:
definition:
value_or_range:
unit:
tolerance:
conditions: []
definition_owner:
change_authority:
source_authority:
consumers: []
consumer_roles: []
interfaces: []
requirements: []
constraints: []
decision_refs: []
evidence_refs: []
baseline_ref:
current_revision:
last_change_ref:
change_reason:
status:
stale_if: []
```

## 5. Controlled Variable state

`PROVISIONAL → COORDINATED → BASELINED → CHANGED_REOPENED → SUPERSEDED`.

Meaning:

- `PROVISIONAL` — definition/value exists but owner/consumers/coordination are incomplete;
- `COORDINATED` — current consumers acknowledge definition and authority;
- `BASELINED` — value/definition is configuration controlled;
- `CHANGED_REOPENED` — accepted/current value changed and dependent objects require recheck;
- `SUPERSEDED` — replaced by later variable revision/object.

## 6. Variable authority hard rules

- exactly one effective `change_authority` per active controlled property/scope unless an explicit joint authority contract exists;
- `definition_owner` and `change_authority` may differ;
- consumers may propose changes but cannot silently mutate Current value;
- if two disciplines both believe they control the same variable, the variable/interface is `BLOCKED` until authority resolves;
- units, tolerance and conditions are part of the variable definition when materially relevant;
- formatting differences do not create new variable identity.

## 7. Variable consumer contract

Every material consumer relation should record:

`consumer_id + consumed_role + required_condition/range + sensitivity + stale_if_changed + readback_route`.

Sensitivity classes:

- `LOW` — change unlikely to affect validity;
- `MATERIAL` — change requires local recheck;
- `INTERFACE_CRITICAL` — change reopens an Interface/acceptance contract;
- `PROMOTION_CRITICAL` — change can invalidate promoted claim/baseline/assurance.

Consumer sensitivity is not the same as Interface criticality.

## 8. Interface objectification threshold

A relation must become an independent `INTERFACE` object when any applies:

- relationship has its own owner/integration owner;
- exchanged variables/geometry/state require coordination;
- relationship has independent acceptance criteria;
- a change on one side can materially invalidate the other;
- tolerance/allowed variation is relationship-specific;
- relationship must be exercised/verified jointly;
- authority conflicts can occur at the relationship;
- historical interface decisions/reopen history must be audited.

Otherwise a typed relation such as `depends_on` may be sufficient.

## 9. Interface minimum contract

```yaml
interface_id:
project_id:
participants: []
side_a:
side_b:
interface_type:
purpose:
owner_a:
owner_b:
integration_owner:
controlling_authority:
inputs_outputs: []
shared_variables: []
requirements: []
constraints: []
tolerances_or_allowed_variation: []
coupling_relationship:
criticality:
required_maturity:
maturity:
disposition:
evidence_state:
acceptance_contract_ref:
validation_or_verification_method:
readback_refs: []
change_reopen_rule:
baseline_ref:
status_notes:
```

## 10. Interface types

`PHYSICAL_GEOMETRIC | MECHANICAL_STRUCTURAL | ELECTRICAL_DATA | HYDRAULIC_ENVIRONMENTAL | HUMAN_ERGONOMIC | SPATIAL_CIRCULATION | VISUAL_PERCEPTUAL | SEMANTIC_CONTENT | INTERACTION_STATE | SERVICE_OPERATIONAL | BRAND_LANGUAGE | INFORMATION_SCHEMA | MAINTENANCE_REPLACEMENT | TEMPORAL_LIFECYCLE | OTHER_CONTROLLED`.

Type describes the dominant exchange semantics, not the discipline name.

An Architecture×Structure interface may be `PHYSICAL_GEOMETRIC`, `MECHANICAL_STRUCTURAL`, or both through facets/sub-relations; do not use discipline names as interface types.

## 11. Coupling

Use:

- `INFORMATIVE` — awareness only; no material consumed output/shared control;
- `DEPENDENT` — mainly directional consumption;
- `RECIPROCAL` — both sides materially constrain each other;
- `TIGHTLY_COUPLED` — relationship cannot be judged from isolated outputs; assembled/integrated readback required.

Coupling is not risk/quality.

## 12. Criticality

Use:

- `ROUTINE`
- `MATERIAL`
- `MAJOR`
- `CRITICAL`

Assess at least:

- consequence to people/use/experience/system behavior;
- effect on project intent/promoted claims;
- safety/accessibility/regulatory consequence;
- dependency fan-out;
- uncertainty/assumption load;
- reversibility;
- late-change cost/disruption;
- authority/evidence sensitivity.

Do not average away hard critical conditions. One hard Critical condition is sufficient.

## 13. Interface maturity and disposition

Maturity:

`IDENTIFIED → DEFINED → COORDINATED → EXERCISED → VERIFIED`.

Disposition:

`OPEN | BLOCKED | CLOSED | OUTSIDE_CLAIM`.

They are independent axes.

Legal examples:
- `COORDINATED + OPEN`;
- `EXERCISED + BLOCKED`;
- `VERIFIED + CLOSED`.

Illegal:
- `CLOSED` below `required_maturity`.

## 14. Maturity meaning

### IDENTIFIED
Participants and relationship are known.

### DEFINED
Exchanged variables/behavior, authority, constraints and acceptance question are explicit.

### COORDINATED
Participants agree on Current interface definition and authority.

### EXERCISED
Relationship has been instantiated in an integrated model/prototype/rehearsal/state flow/readback appropriate to the decision.

### VERIFIED
Accepted evidence satisfies the current Interface Acceptance Contract for the stated claim ceiling/configuration.

`VERIFIED` does not automatically mean field-proven, code-compliant, fabrication-ready or operationally validated.

## 15. Required maturity rule

Required maturity comes from the claim/decision, not a fixed project phase.

Examples:

- early geometry coordination claim may close at `COORDINATED`;
- claim about assembled fit/behavior requires at least `EXERCISED` and normally `VERIFIED` before promotion;
- field/operational claim requires the corresponding field/operational evidence ceiling in addition to Interface maturity.

## 16. Interface Acceptance Contract

Required for all `MAJOR` and `CRITICAL` Interfaces and any lower-criticality interface whose closure depends on a material shared acceptance question.

Minimum:

```yaml
acceptance_contract_id:
interface_id:
claim_or_decision_scope:
required_maturity:
participants: []
controlling_authority:
shared_variables_and_ranges: []
requirements: []
constraints: []
acceptance_questions: []
acceptance_criteria: []
test_or_readback_method:
configuration_under_test:
required_evidence: []
per_participant_obligations: []
allowed_open_items: []
claim_ceiling_if_pass:
reopen_triggers: []
review_authority:
status:
```

A contract with only “both disciplines agree” is insufficient for a material interface.

## 17. Governance floor

| Condition | Minimum floor |
|---|---|
| ROUTINE + low coupling | owner + change rule + concise register entry |
| MATERIAL | explicit acceptance question + authority + required maturity + readback |
| MAJOR | Acceptance Contract + integrated readback + explicit reopen scope |
| CRITICAL | full Acceptance Contract + no authority conflict + integrated verification + independent whole-system review before promotion |
| any TIGHTLY_COUPLED | assembled/integrated prototype or readback mandatory |

Criticality sets the floor. Coupling may increase method burden but cannot lower it.

## 18. N-way interfaces

Use one N-way Interface object only when all participants genuinely share:

- one acceptance question;
- one controlling authority model;
- one coherent shared-variable set;
- one integrated readback.

If participant pairs have materially different variables, tolerances, acceptance conditions or authority, decompose into explicit pairwise/sub-interface objects linked to a parent integration interface.

Do not force an N-way relationship into pairwise edges when the system behavior exists only as an assembled whole.

## 19. Material Dependency

A `MATERIAL_DEPENDENCY` is appropriate when dependency itself must be tracked but a full Interface is unnecessary.

Examples:
- render depends on Current model revision;
- downstream calculation depends on one dataset;
- publication page depends on approved translation;
- procurement decision depends on supplier evidence;
- task depends on authority approval.

Minimum fields:

```yaml
dependency_id:
project_id:
source_object:
consumer_object:
dependency_type:
direction:
required_condition:
owner:
criticality:
current_disposition:
stale_if:
readback_route:
status:
```

Dependency types:

`DATA | GEOMETRY | DECISION | REQUIREMENT | EVIDENCE | AUTHORITY | CONFIGURATION | RESOURCE | SCHEDULE | CONTENT | OTHER_CONTROLLED`.

Direction:

`SOURCE_TO_CONSUMER | RECIPROCAL`.

State:

`IDENTIFIED → DEFINED → ACTIVE → SATISFIED_FOR_SCOPE | STALE | SUPERSEDED`.

## 20. Dependency vs Interface test

Use `MATERIAL_DEPENDENCY` when:
- relationship is primarily prerequisite/consumption;
- acceptance can be judged on source validity/availability;
- no separate relationship-specific tolerance/behavior needs joint verification.

Upgrade to `INTERFACE` when:
- both sides constrain each other materially;
- shared variables/tolerances need coordination;
- relationship has independent acceptance behavior;
- integrated exercise/readback is needed.

## 21. Shared Variable Register

The Runtime Control `SHARED_VARIABLE_REGISTER` is a registry view over Project `CONTROLLED_VARIABLE` objects.

It must not replace variable identities.

Register minimum:
- variable ID;
- current revision/value/range;
- definition owner;
- change authority;
- consumers;
- related interfaces;
- baseline;
- current stale/reopen state.

## 22. Interface Register

The Runtime Control `INTERFACE_REGISTER` is a registry view over Project `INTERFACE` objects.

It must show at least:
- ID;
- participants;
- type;
- integration owner;
- criticality;
- coupling;
- required maturity;
- actual maturity;
- disposition;
- authority conflict state;
- acceptance contract;
- current readback/evidence;
- stale/reopen state.

## 23. Change propagation

For every material Controlled Variable / Interface / Dependency change:

`changed object → registered consumers → affected interface/dependency → affected artifact → affected decision → affected assurance → affected gate/promotion`.

Ask:
1. what changed?
2. who consumes it?
3. which Interface contracts changed?
4. which artifacts became stale?
5. which Decisions must reopen?
6. which assurance/readback must rerun?
7. which promoted claim/baseline is invalidated?

## 24. Integration readback

Integrated readback must inspect the relationship, not just prove both local objects exist.

Possible forms:
- federated/coordinated model;
- 1:1 detail/mock-up;
- combined state-flow/prototype;
- real route + signage/content test;
- responsive UI with content/motion/accessibility states;
- grading + drainage + path + planting model;
- data schema + actual visualization + decision task.

Fidelity is determined by Decision Question and criticality.

## 25. Failure modes

Fail/HOLD when:

- shared variable has conflicting current change authorities;
- material consumer is not registered and change blast radius is unknown;
- Interface uses one generic `status` instead of maturity + disposition;
- Interface closes below required maturity;
- MAJOR/CRITICAL Interface lacks Acceptance Contract;
- TIGHTLY_COUPLED Interface is judged only from isolated discipline outputs;
- authority conflict is hidden as an “open coordination item”;
- N-way Interface structure hides materially different pairwise obligations;
- dependency should be an Interface but is left as generic `depends_on` to avoid governance burden;
- Interface maturity is used to imply field/compliance/professional proof outside its evidence ceiling.

## 26. Validator floor

- `VAR-001` active Controlled Variable has exactly one effective change authority unless explicit joint contract;
- `VAR-002` material Controlled Variable has registered consumers;
- `VAR-003` baselined variable material change triggers downstream reopen analysis;
- `VAR-004` unit/tolerance/conditions present where material;
- `IFC-001` Interface has participants + integration owner where required;
- `IFC-002` maturity and disposition stored independently;
- `IFC-003` CLOSED requires maturity ≥ required maturity;
- `IFC-004` MAJOR/CRITICAL requires Acceptance Contract;
- `IFC-005` TIGHTLY_COUPLED requires integrated readback;
- `IFC-006` authority conflict blocks closure/promotion;
- `IFC-007` Interface VERIFIED cannot exceed its evidence/claim ceiling;
- `IFC-008` N-way Interface must justify shared contract or decompose;
- `DEP-001` Material Dependency has source + consumer + condition + owner + stale rule;
- `DEP-002` dependency requiring bilateral/shared acceptance must upgrade to Interface;
- `REG-001` Runtime registers reference Project objects; they do not replace identities;
- `PROP-001` material change propagates through registered consumers/interfaces/assurance;
- `PROP-002` unknown material blast radius blocks closure or expands investigation.

## 27. P4 closure condition

P4 is sufficiently refined for draft review when Controlled Variable authority/consumer semantics, Interface objectification/coupling/criticality/maturity/disposition/acceptance, N-way handling, Material Dependency boundary, registers and propagation/readback rules all have machine-readable counterparts.
