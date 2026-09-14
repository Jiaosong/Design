# OLEANDER Complex Project Runtime Classification Detail Framework v1.0

Status: DRAFT GOVERNANCE EXTENSION. Extends current Project Axis, Control Plane, and Cross-Disciplinary Design Integration. It does not create a second project taxonomy, knowledge taxonomy, stage system, or authority tree.

## 1. Fundamental separation

Every project-runtime record must separate:

- **Hierarchy** — what contains what;
- **Primary Semantic Class** — what this object is;
- **Facet / Aspect** — from which view the object is described;
- **Typed Relation** — how it relates to another object;
- **State** — how far this object has progressed;
- **Authority** — who may define/change/accept it;
- **Evidence** — why its current claim/state is trusted;
- **Configuration** — which approved version/baseline is current.

No single field may silently perform two of these jobs.

## 2. Project Axis boundary

Retain:

- P0 Portfolio
- P1 Program
- P2 Project
- P3 Workstream
- P4 Formal Assurance (logical interpretation of current P4 Validation)

P0-P2 are project identity hierarchy. P3 is work organization and is not a lifecycle stage. P4 is a formal assurance object linked to the thing being assured; it is not necessarily a child of one P3 workstream.

Required `assurance_type` for P4:
`VERIFICATION | VALIDATION | CERTIFICATION | INDEPENDENT_REVIEW | AUDIT | ACCEPTANCE`.

## 3. Eight semantic families and atomic object types

### F1 Purpose & Obligation
- INTENT
- NEED
- REQUIREMENT
- CONSTRAINT
- CLAIM

### F2 System Definition
- SYSTEM_ELEMENT
- BEHAVIOR_STATE_MODEL
- CONTROLLED_VARIABLE

### F3 Work & Information
- WORK_PACKAGE / TASK
- ARTIFACT

### F4 Coupling & Coordination
- INTERFACE
- MATERIAL_DEPENDENCY when the dependency itself needs ownership, acceptance, or change control

### F5 Decision & Governance
- DECISION
- WAIVER / DEVIATION
- ACTOR / AUTHORITY_ROLE

### F6 Uncertainty & Problem
- RISK
- ISSUE
- ASSUMPTION
- UNKNOWN

`BLOCKED` is a disposition, not an object class. `OPPORTUNITY` is normally a positive-risk polarity unless it requires a separate decision object.

### F7 Evidence & Assurance
- EVIDENCE_RECORD
- ASSURANCE_ACTIVITY
- ASSURANCE_DECISION

### F8 Configuration & Change
- BASELINE
- CHANGE

A configuration item is usually a property of another object, not a new object type.

## 4. Cross-view system aspects

A System Element may participate in multiple aspects without duplication:

- FUNCTION
- PHYSICAL / PRODUCT
- LOCATION / SPATIAL
- TYPE
- BEHAVIOR / STATE
- SERVICE / PROCESS
- INFORMATION / DATA
- HUMAN / ORGANIZATION

Discipline is not a hierarchy. Use discipline as an ownership/review lens.

## 5. Objectification threshold

Create an independent runtime object only when at least one condition applies:

- cross-disciplinary or cross-workstream;
- consumed by multiple downstream objects;
- has independent definition/change/review authority;
- requires independent acceptance or verification;
- has material risk or promoted-claim consequence;
- must remain traceable when its carrier/file is replaced;
- may invalidate downstream work when changed;
- requires historical audit or supersession history.

Otherwise keep the fact as an attribute of the owning object.

## 6. Core data contracts

### 6.1 REQUIREMENT
Minimum:
`id, statement, requirement_type, source_need_or_parent, subject, conditions, acceptance_criteria, verification_method, verification_level, owner, change_authority, priority, status, baseline_ref, traced_to, satisfied_by, verified_by, rationale, assumptions, constraints, version`.

Rules:
- states what is needed, not a hidden implementation decision unless the implementation is itself an authorized constraint;
- must be singular enough to trace and verify;
- high-impact requirement must have bidirectional traceability;
- approved/baselined requirement changes require impact analysis.

State:
`DRAFT → ANALYZED → AGREED → BASELINED → SATISFIED_PENDING_ASSURANCE → VERIFIED | FAILED → SUPERSEDED`.

Requirement validation (quality/fit of the requirement statement) is distinct from product validation.

### 6.2 CONSTRAINT
Minimum:
`id, constraint_type, source_authority, scope, affected_objects, condition, exception_rule, waiver_authority, effective_from, effective_to, status`.

State:
`PROPOSED → CONFIRMED → ACTIVE → WAIVED_WITH_AUTHORITY | EXPIRED | SUPERSEDED`.

A constraint must not be weakened by ordinary trade-off scoring.

### 6.3 CONTROLLED_VARIABLE
Minimum:
`id, semantic_name, definition, value_or_range, unit, tolerance, definition_owner, change_authority, source_authority, consumers, interfaces, baseline_ref, last_change, evidence_ref, status`.

State:
`PROVISIONAL → COORDINATED → BASELINED → CHANGED_REOPENED → SUPERSEDED`.

Hard rule: one current change authority per active variable.

### 6.4 INTERFACE
Minimum:
`id, side_a, side_b, interface_type, purpose, owner_a, owner_b, integration_owner, controlling_authority, inputs_outputs, shared_variables, constraints, tolerance, coupling, criticality, required_maturity, maturity, disposition, acceptance_contract, validation_method, evidence_refs, change_reopen_rule`.

Maturity:
`IDENTIFIED → DEFINED → COORDINATED → EXERCISED → VERIFIED`.

Disposition:
`OPEN | BLOCKED | CLOSED | OUTSIDE_CLAIM`.

Rules:
- maturity and disposition are independent;
- `CLOSED` is forbidden below required maturity;
- TIGHTLY_COUPLED interfaces require integrated readback;
- MAJOR/CRITICAL interfaces require an acceptance contract.

### 6.5 DECISION
Minimum:
`id, decision_question, alternatives, criteria, constraints, evidence, assumptions, affected_objects, participating_roles, decision_authority, selected_option, rationale, rejected_options, locked_variables, open_variables, effective_baseline, reopen_trigger, status`.

State:
`OPEN → FRAMED → OPTIONS_READY → EVALUATED → DECIDED → IMPLEMENTED → VERIFIED → SUPERSEDED/REOPENED`.

Rules:
- a decision record is required when a choice materially constrains another discipline/workstream or promoted claim;
- do not average away hard constraints;
- rationale and reopen trigger are mandatory for consequential decisions.

### 6.6 RISK
Minimum:
`id, cause, uncertain_event, consequence, affected_objective, likelihood_basis, impact_basis, exposure_class, owner, treatment, trigger, residual_risk, evidence, review_due, status`.

State:
`IDENTIFIED → ANALYZED → EVALUATED → TREATMENT_PLANNED → TREATED → MONITORED → ACCEPTED/CLOSED`.

### 6.7 ISSUE
Minimum:
`id, observed_problem, detection_evidence, affected_objects, severity, owner, containment, root_cause, corrective_action, verification, reopen_rule, status`.

State:
`OPEN → TRIAGED → CONTAINED → ROOT_CAUSE_CONFIRMED → REPAIRED → RETESTED → CLOSED`.

### 6.8 ASSUMPTION
Minimum:
`id, proposition, why_needed, scope, affected_objects, consequence_if_false, owner, validation_route, expiry_or_trigger, evidence, status`.

State:
`PROPOSED → ACTIVE → CONFIRMED | REFUTED | EXPIRED`.

Major/Critical active assumptions cannot survive pre-promotion without explicit claim ceiling and validation/containment.

### 6.9 UNKNOWN
Minimum:
`id, unknown_question, why_material, affected_objects, owner, resolution_route, decision_deadline, consequence_if_unresolved, status`.

State:
`OPEN → INVESTIGATING → RESOLVED | OUTSIDE_CLAIM`.

Unknown must not be auto-converted into an assumption merely to keep the workflow moving.

### 6.10 ARTIFACT
Minimum:
`id, artifact_type, carrier_uri, version, producer, owner, represents, implements, evidence_role, baseline_ref, supersedes, status`.

Rule: Artifact is a carrier. It is not automatically a requirement, decision, evidence, or baseline.

State:
`WORKING → REVIEWABLE → ACCEPTED_FOR_SCOPE → BASELINED | SUPERSEDED | WITHDRAWN`.

### 6.11 EVIDENCE_RECORD
Minimum:
`id, evidence_type, question, source_or_method, setup_or_condition, observation_or_data, uncertainty, provenance, supports, contradicts, strength, claim_ceiling, repeatability, status`.

State:
`CAPTURED → CHECKED → ACCEPTED_FOR_USE | REJECTED → STALE/SUPERSEDED`.

### 6.12 ASSURANCE_ACTIVITY
Minimum:
`id, assurance_type, target_object, target_requirement_or_need, method, procedure, environment, configuration_under_test, acceptance_criteria, executor, reviewer, evidence_outputs, result, limitations, status`.

State:
`PLANNED → READY → EXECUTED → ANALYZED → PASS | FAIL | INCONCLUSIVE → CLOSED/REOPENED`.

Verification target: requirement/specification.
Validation target: stakeholder need, intended use, scenario or project intent.

### 6.13 BASELINE
Minimum:
`id, baseline_type, scope, included_objects, authority, approval_date, hashes_or_versions, assumptions, open_items, supersedes, status`.

State:
`CANDIDATE → APPROVED → CURRENT → SUPERSEDED`.

Approved baseline is immutable; replacement creates a new baseline.

### 6.14 CHANGE
Minimum:
`id, proposed_change, reason, initiator, affected_objects, dependency_impact, interface_impact, requirement_impact, artifact_impact, evidence_impact, risk_impact, baseline_impact, approval_authority, decision_ref, implementation_refs, verification_refs, status`.

State:
`PROPOSED → IMPACT_ASSESSED → APPROVED | REJECTED → IMPLEMENTED → VERIFIED → CLOSED`.

Change impact classes:
`NON_MATERIAL | LOCAL_MATERIAL | INTERFACE_MATERIAL | COUPLED_SYSTEM | PROMOTION_BREAKING`.

## 7. Authority contract

Do not use one generic Owner field for consequential objects. Distinguish:

- `definition_owner`
- `change_authority`
- `integration_owner`
- `review_authority`
- `contributors[]`
- `consumers[]`
- `external_authorities[]`

One role/person may occupy multiple authority slots, but the slots remain semantically distinct.

## 8. Typed relation families

### Decomposition
`part_of / contains`

### Allocation
`allocated_to / owned_by / assigned_to`

### Need and requirement trace
`derived_from / refines / constrained_by / satisfies`

### Realization
`implements / realizes / produces / represented_by`

### Coupling
`interfaces_via / exchanges_with / depends_on / consumes / produces_for`

### Authority
`defined_by / controlled_by / approved_by / reviewed_by`

### Evidence and assurance
`evidenced_by / verified_by / validated_by / contradicted_by`

### Decision
`decided_by / locks / rejects / waives`

### Change impact
`affects / invalidates / makes_stale / reopens`

### Lifecycle/configuration
`baselined_in / supersedes / replaced_by`

`related_to` is discovery-only and cannot substitute for a strong semantic relation.

## 9. Relation cardinality floor

- Requirement → source Need/parent: `1..N` for derived requirements; root externally mandated requirements may point directly to Source Authority.
- Requirement → verification route: `1..N` before baseline when consequential.
- Controlled Variable → change authority: exactly `1` while active.
- Interface → side_a/side_b: exactly `1 + 1`; N-way interfaces should use explicit participant collection or decompose if pairwise behavior differs.
- Interface → integration_owner: `1` for MAJOR/CRITICAL.
- Decision → decision_authority: exactly `1` current authority.
- Risk/Issue/Assumption/Unknown → owner: exactly `1` accountable owner while open.
- Evidence → provenance/method: at least `1` resolvable source/method.
- Verification Activity → target requirement: `1..N`, but each result must preserve per-requirement disposition.
- Validation Activity → target Need/Intent/Scenario: `1..N`.
- Baseline → included configuration-controlled objects: `1..N`.
- Change → affected object set: `1..N` after impact analysis unless explicitly NON_MATERIAL with rationale.

## 10. Promotion and closure invariants

A promoted object may not claim a maturity/evidence state higher than its weakest material dependency permits.

Hard rules:
- no Requirement `VERIFIED` without an Assurance Activity and accepted evidence;
- no Validation PASS solely from requirement verification;
- no Interface `CLOSED` below required maturity;
- no MAJOR/CRITICAL Interface closure with unresolved authority conflict;
- no DECIDED consequential choice without authority+rationale+reopen trigger;
- no active shared variable with multiple current change authorities;
- no approved Baseline overwrite in place;
- no approved Change closure before affected required assurance is rerun;
- no promoted claim depending on an expired Major/Critical assumption without explicit containment;
- no Artifact treated as semantic truth merely because it is the latest file.

## 11. Database/runtime implementation principle

Do not create one database per object type. The ontology is logical; physical storage may use existing Projects DB, project-scoped runtime records, integration packets, Git/Drive artifacts, and future D1/graph adapters.

Minimum physical rule:
`stable object_id + primary_semantic_class + typed relations + state fields + authority refs + evidence/configuration refs`.

Knowledge Notes remain for reusable cross-project knowledge. Project-runtime facts stay in project/runtime structures unless distilled through the existing knowledge promotion gates.

## 12. Validator floor

- `OBJ-001` exactly one Primary Semantic Class;
- `OBJ-002` Discipline cannot be project/system hierarchy;
- `REQ-001` baselined requirement has trace + verification route;
- `REQ-002` requirement change has impact analysis;
- `VAR-001` active shared variable has exactly one change authority;
- `IFC-001` MAJOR/CRITICAL interface has acceptance contract;
- `IFC-002` TIGHTLY_COUPLED interface has integrated readback;
- `DEC-001` consequential decision has authority+rationale+reopen trigger;
- `ASM-001` Major/Critical assumption has validation/expiry/containment;
- `CHG-001` approved material change has affected-object graph;
- `CFG-001` approved baseline is immutable;
- `EVD-001` evidence has method/source/condition/provenance;
- `VER-001` verification result resolves to Requirement target;
- `VAL-001` validation result resolves to Need/Intent/Scenario target;
- `ART-001` artifact is not silently promoted into Requirement/Decision/Evidence;
- `AUTH-001` no conflicting current change authorities;
- `STATE-001` object uses only its allowed state machine;
- `PROM-001` promoted claim does not exceed evidence/assurance ceiling.

## 13. External calibration basis

Calibrated against, without adopting as parallel Authority:
- ISO/IEC/IEEE 15288:2023 — system life-cycle processes;
- ISO/IEC/IEEE 29148:2018 and 2026 DIS revision — requirements engineering;
- IEC 81346-1:2022 — multi-aspect system structuring/reference designations;
- ISO 21511 — WBS guidance;
- ISO 31000 — risk management;
- ISO 10007 — configuration management;
- ISO 19650 — information management;
- OMG SysML v2 — requirement/structure/behavior/analysis/verification traceability;
- buildingSMART IFC — objectified relationships;
- NASA Systems Engineering Handbook / NPR 7123 — requirements, interface, V&V, configuration, risk and decision analysis.

## 14. Runtime formula

`PROJECT RUNTIME OBJECT = Stable Identity + One Primary Semantic Class + Multiple Facets + Typed Relations + Authority Contract + Class-Specific State Machine + Evidence State + Configuration State + Scope + Provenance`

The project system therefore remains multi-axis. No attempt should be made to collapse Project identity, System structure, Work structure, Discipline, Lifecycle, Evidence, Configuration and Runtime semantics into one tree.