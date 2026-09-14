# OLEANDER Runtime Object × Relation Allowed Matrix v1.0

Status: **DRAFT GOVERNANCE EXTENSION**. This matrix extends `OLEANDER_COMPLEX_PROJECT_RUNTIME_CLASSIFICATION_DETAIL_FRAMEWORK_v1.0` and current Cross-Disciplinary Integration. It does not create a second project taxonomy.

## 1. Matrix semantics

Codes:

- `R` = REQUIRED before authoritative promotion / closure when applicable.
- `A` = ALLOWED.
- `C` = CONDITIONAL; allowed only when the edge carries material project meaning and satisfies the edge contract below.
- `F` = FORBIDDEN as a direct relation family for this primary semantic class; use the correct intermediary object instead.

Relation-family columns:

- `DECMP` = decomposition (`part_of / contains`)
- `ALLOC` = allocation (`allocated_to / owned_by / assigned_to`)
- `REQT` = requirement trace (`derived_from / refines / constrained_by / satisfies`)
- `REAL` = realization (`implements / realizes / produces / represented_by`)
- `COUP` = coupling (`interfaces_via / exchanges_with / depends_on / consumes / produces_for`)
- `AUTH` = authority (`defined_by / controlled_by / approved_by / reviewed_by`)
- `EVID` = evidence / assurance (`evidenced_by / verified_by / validated_by / contradicted_by`)
- `DEC` = decision (`decided_by / locks / rejects / waives`)
- `CHG` = change impact (`affects / invalidates / makes_stale / reopens`)
- `CFG` = lifecycle / configuration (`baselined_in / supersedes / replaced_by`)

`A` never means “connect freely.” Every edge must use an allowed source-type → target-type contract.

## 2. Object × relation-family matrix

| Object Type | DECMP | ALLOC | REQT | REAL | COUP | AUTH | EVID | DEC | CHG | CFG |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| INTENT | C | C | A | C | F | R | A | A | A | A |
| NEED | C | C | R | C | F | R | A | A | A | A |
| REQUIREMENT | C | C | R | A | C | R | R | A | R | R |
| CONSTRAINT | C | C | A | A | C | R | C | A | R | R |
| CLAIM | F | C | A | A | C | R | R | A | R | A |
| SYSTEM_ELEMENT | A | C | A | A | A | R | C | A | R | R |
| BEHAVIOR_STATE_MODEL | A | C | A | A | A | R | R | A | R | R |
| CONTROLLED_VARIABLE | C | C | A | A | R | R | C | R | R | R |
| WORK_PACKAGE | A | R | C | R | A | R | C | A | R | C |
| TASK | A | R | C | R | A | R | C | A | R | C |
| ARTIFACT | C | C | A | A | A | R | C | A | R | R |
| INTERFACE | F | R | A | A | R | R | R | A | R | C |
| MATERIAL_DEPENDENCY | F | R | C | C | R | R | C | A | R | C |
| DECISION | F | C | A | A | C | R | R | R | R | R |
| WAIVER | F | C | R | C | F | R | R | R | R | R |
| DEVIATION | F | C | R | C | C | R | R | R | R | R |
| ACTOR | C | A | F | C | C | C | F | C | C | C |
| AUTHORITY_ROLE | C | A | F | F | C | A | F | C | C | C |
| RISK | C | R | C | C | C | R | R | A | R | C |
| ISSUE | C | R | C | C | C | R | R | A | R | C |
| ASSUMPTION | C | R | A | C | C | R | R | A | R | C |
| UNKNOWN | C | R | C | C | C | R | C | A | R | C |
| EVIDENCE_RECORD | F | C | F | C | F | R | A | F | A | R |
| ASSURANCE_ACTIVITY | C | R | A | C | C | R | R | C | R | R |
| ASSURANCE_DECISION | F | C | A | C | F | R | R | A | R | R |
| BASELINE | C | C | F | F | F | R | C | A | R | R |
| CHANGE | C | R | C | C | C | R | R | R | R | R |

## 3. Required edge contracts

### 3.1 Purpose / obligation trace

Allowed canonical chains include:

`INTENT → derived_into → NEED → derived_into → REQUIREMENT`

`REQUIREMENT → constrained_by → CONSTRAINT`

`REQUIREMENT → satisfied_by → SYSTEM_ELEMENT | BEHAVIOR_STATE_MODEL | CONTROLLED_VARIABLE | ARTIFACT`

`CLAIM → supported_by → EVIDENCE_RECORD | ASSURANCE_DECISION`

Hard rules:

- A `NEED` must not be treated as a verified requirement merely because it is stakeholder-authored.
- A `CONSTRAINT` is not satisfied by a design object; it is complied with, bounded by, or explicitly waived/deviated under authority.
- A `CLAIM` may reference requirements, but a claim is not itself a requirement.

### 3.2 Requirement trace

Allowed direct targets from `REQUIREMENT`:

- `derived_from → INTENT | NEED | REQUIREMENT | external_authority_ref`
- `refines → REQUIREMENT`
- `constrained_by → CONSTRAINT`
- `satisfied_by → SYSTEM_ELEMENT | BEHAVIOR_STATE_MODEL | CONTROLLED_VARIABLE | ARTIFACT`
- `verified_by → ASSURANCE_ACTIVITY | ASSURANCE_DECISION`
- `baselined_in → BASELINE`
- `affected_by → CHANGE`

Forbidden:

- `REQUIREMENT → validated_by` when the assurance only checks specification conformance. Use `verified_by`.
- `REQUIREMENT → evidenced_by → ARTIFACT` as sole assurance. Artifact is a carrier; the evidence record or assurance activity must state what was inspected and under what method.

### 3.3 System realization

`SYSTEM_ELEMENT` may:

- `part_of / contains → SYSTEM_ELEMENT`
- `implements → REQUIREMENT`
- `interfaces_via → INTERFACE`
- `depends_on → MATERIAL_DEPENDENCY | SYSTEM_ELEMENT | CONTROLLED_VARIABLE`
- `represented_by → ARTIFACT`
- `evidenced_by → EVIDENCE_RECORD`
- `baselined_in → BASELINE`

`BEHAVIOR_STATE_MODEL` may:

- `realizes → INTENT | NEED | REQUIREMENT`
- `describes_behavior_of → SYSTEM_ELEMENT`
- `interfaces_via → INTERFACE`
- `represented_by → ARTIFACT`
- `verified_by → ASSURANCE_ACTIVITY`

### 3.4 Controlled variable contract

`CONTROLLED_VARIABLE` must have:

- exactly one active `controlled_by → ACTOR | AUTHORITY_ROLE` change authority;
- one or more `consumed_by → SYSTEM_ELEMENT | BEHAVIOR_STATE_MODEL | INTERFACE | ARTIFACT | ASSURANCE_ACTIVITY` when it is shared;
- `baselined_in → BASELINE` before it is treated as a controlled current value;
- `affected_by → CHANGE` for every material accepted value/range/tolerance change.

A shared variable may have many definition contributors but only one current change authority.

### 3.5 Interface objectification contract

An `INTERFACE` must connect at least two interface sides. Default binary form:

`SIDE_A → interfaces_via → INTERFACE ← interfaces_via ← SIDE_B`

Side types may include `SYSTEM_ELEMENT`, `BEHAVIOR_STATE_MODEL`, `WORK_PACKAGE`, `ARTIFACT`, `ACTOR`, or external systems when explicitly modeled.

For `MAJOR / CRITICAL` interfaces:

- exactly one `integration_owner`;
- explicit `controlled_by / approved_by` authority;
- explicit shared variables / exchanged information where applicable;
- `verified_by → ASSURANCE_ACTIVITY | ASSURANCE_DECISION` before closure at VERIFIED maturity;
- material changes use `reopens / makes_stale` edges to affected interface state and downstream assurance.

Direct `SYSTEM_ELEMENT related_to SYSTEM_ELEMENT` must not substitute for an interface object when the relation has its own owner, acceptance criteria, criticality, tolerance, maturity, evidence, approval, or reopen rule.

### 3.6 Material dependency contract

Create `MATERIAL_DEPENDENCY` only when the dependency itself needs ownership, acceptance, monitoring, or change control. Otherwise use a direct typed `depends_on / consumes` edge.

A material dependency requires:

- provider and consumer;
- accountable owner;
- dependency payload / condition;
- change/reopen logic;
- evidence or readback before `SATISFIED_FOR_SCOPE`.

### 3.7 Decision contract

A consequential `DECISION` must relate to:

- `decided_by → ACTOR | AUTHORITY_ROLE` exactly one current decision authority;
- `based_on → EVIDENCE_RECORD | ASSURANCE_DECISION | REQUIREMENT | CONSTRAINT | RISK | ASSUMPTION` as applicable;
- `locks → CONTROLLED_VARIABLE | REQUIREMENT | SYSTEM_ELEMENT | BEHAVIOR_STATE_MODEL | BASELINE` when it creates a controlled project position;
- `rejects → alternative DECISION option / candidate object` when rejection matters;
- `affected_by → CHANGE` and/or `reopened_by → CHANGE | EVIDENCE_RECORD | ISSUE` when current basis is invalidated.

No consequential decision may close with only `approved_by` and no rationale/evidence basis.

### 3.8 Waiver / deviation contract

`WAIVER` and `DEVIATION` must:

- target at least one `REQUIREMENT | CONSTRAINT | BASELINE`;
- have exactly one current approval authority;
- record scope, rationale, expiry/review trigger, risk/evidence basis;
- never silently mutate the waived/deviated object into “compliant.”

A waiver/deviation changes the authorized project position; it does not rewrite the original requirement/constraint history.

### 3.9 Risk / issue / assumption / unknown contract

Every open `RISK | ISSUE | ASSUMPTION | UNKNOWN` must have exactly one accountable owner.

Allowed key relations:

- `RISK → threatens → INTENT | NEED | REQUIREMENT | SYSTEM_ELEMENT | INTERFACE | WORK_PACKAGE | CLAIM | BASELINE`
- `RISK → mitigated_by → WORK_PACKAGE | TASK | DECISION | CHANGE | REQUIREMENT`
- `ISSUE → affects → any material runtime object`
- `ISSUE → repaired_by → CHANGE | TASK | DECISION`
- `ASSUMPTION → supports → REQUIREMENT | DECISION | CONTROLLED_VARIABLE | MODEL | CLAIM`
- `ASSUMPTION → confirmed_by / refuted_by → EVIDENCE_RECORD | ASSURANCE_DECISION`
- `UNKNOWN → investigated_by → WORK_PACKAGE | TASK | ASSURANCE_ACTIVITY | research object`

An `UNKNOWN` cannot become an `ASSUMPTION` without an explicit decision/owner accepting the temporary proposition and its claim ceiling.

### 3.10 Artifact contract

`ARTIFACT` is an information carrier. It may:

- `represents → SYSTEM_ELEMENT | BEHAVIOR_STATE_MODEL | DECISION | CONTROLLED_VARIABLE`
- `implements / documents → REQUIREMENT | CONSTRAINT | DECISION`
- `produced_by → WORK_PACKAGE | TASK`
- `baselined_in → BASELINE`
- `inspected_by → ASSURANCE_ACTIVITY`

Forbidden semantic shortcuts:

- Artifact `CURRENT` does not make represented decisions/variables current.
- Artifact existence does not count as evidence of correctness.
- Artifact approval does not automatically verify the requirements it depicts.

### 3.11 Evidence / assurance contract

`EVIDENCE_RECORD` requires provenance and method/condition appropriate to the claim.

`ASSURANCE_ACTIVITY` must target at least one object under assurance.

`ASSURANCE_DECISION` must reference:

- the assurance activity;
- evidence used;
- per-target result;
- authority/reviewer;
- scope / claim ceiling.

Verification targets `REQUIREMENT | CONSTRAINT | specified interface acceptance condition`.
Validation targets `NEED | INTENT | intended-use scenario | project-level CLAIM`.

`VALIDATION PASS` must not be inferred from verification-only evidence.

### 3.12 Baseline / change contract

`BASELINE` may contain one or more controlled runtime objects/artifacts and must be approved by authority before `CURRENT`.

`CHANGE` must relate to:

- proposer/owner;
- reason;
- affected objects after impact assessment;
- approval authority for material changes;
- implementation evidence;
- re-assurance targets when the change invalidates prior verification/validation.

`APPROVED BASELINE` objects are immutable in history. A material update creates a new revision/baseline and supersession relation; it does not overwrite the old baseline.

## 4. Forbidden direct-edge patterns

The validator should reject at minimum:

1. `ARTIFACT → verifies → REQUIREMENT` without an `ASSURANCE_ACTIVITY / EVIDENCE_RECORD` layer.
2. `EVIDENCE_RECORD → approves → DECISION` — evidence informs; authority approves/decides.
3. `RISK → closed_by → ARTIFACT` without treatment/readback semantics.
4. `ASSUMPTION → verified_by → ARTIFACT` without evidence/assurance method.
5. `INTERFACE → CLOSED` with no assurance relation when required maturity is VERIFIED.
6. `CONTROLLED_VARIABLE → controlled_by` more than one active authority.
7. `BASELINE → replaces → BASELINE` without explicit supersession/change history.
8. `VALIDATION → target REQUIREMENT only` when no Need/Intent/Scenario is traced.
9. `VERIFICATION → target NEED only` when no specified requirement/acceptance criterion exists.
10. generic `related_to` used where a strong semantic relation above exists.

## 5. Relation-resolution precedence

When several relations seem plausible, resolve in this order:

`authority / normative → requirement trace → realization → interface/coupling → evidence/assurance → decision → change impact → lifecycle/configuration → generic semantic adjacency`.

Use generic adjacency only when no stronger runtime semantic relation exists.