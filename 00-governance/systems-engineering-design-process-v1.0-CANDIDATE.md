# OLEANDER Systems Engineering Design Process v1.0 — CANDIDATE

**Status:** `CANDIDATE PROFESSIONAL DOMAIN PROCESS / R-E / NOT CURRENT / NO PROMOTION`

**Domain:** Systems Engineering

**Process ID:** `OLEANDER-SYSTEMS-ENGINEERING-DESIGN-PROCESS`

**Authority position:** subordinate to the OLEANDER Master Runtime, Current System Definition / Knowledge Architecture, `professional-domain-process-contract-v1.0.md`, Cross-Disciplinary Integration, project/organizational authority and the responsible Systems Engineering owner.

**Purpose:** provide a domain-authentic Systems Engineering process for defining, architecting, allocating, verifying, validating, integrating, transitioning, operating and changing a system of interest without turning OLEANDER's own system-design history into a universal lifecycle template.

---

## 1｜Professional-source alignment

Current professional references used for scope calibration:

- ISO/IEC/IEEE 15288:2023 — current system life-cycle process framework; explicitly permits iterative/concurrent/recursive application and does not prescribe one lifecycle model or modelling method.
- INCOSE Systems Engineering Handbook, Fifth Edition — current state-of-good-practice practitioner reference.
- NASA Systems Engineering Handbook — public practitioner reference for system design, product realization, cross-cutting technical management, verification and validation.

These sources establish professional responsibilities, not a mandatory OLEANDER stage numbering system.

`PROFESSIONAL SOURCE ≠ UNIVERSAL STAGE TEMPLATE`.

---

## 2｜Existing OLEANDER alignment

OLEANDER already contains a zero-base system-design chain developed from real design-system needs:

`BEHAVIOUR RESEARCH → PURE USER NEEDS → EXPERIENCE REQUIREMENTS → SYSTEM CONTEXT → OPERATIONAL CONCEPT → CAPABILITY ARCHITECTURE → REVERSE-TRACE VALIDATION → FUNCTIONAL ARCHITECTURE → INFORMATION ARCHITECTURE → HUMAN/SYSTEM ALLOCATION → INTERFACE ARCHITECTURE → SYSTEM REQUIREMENTS → REQUIREMENTS NORMALIZATION → LOGICAL ARCHITECTURE → ALTERNATIVES/ALLOCATION → PBS/PHYSICAL ARCHITECTURE → PDR`.

This candidate does not make that exact chain universal. It compiles the professional semantics beneath it into reusable Systems Engineering stage objects.

---

## 3｜Scope in

Trigger for material claims involving:
- system of interest / boundary / external actors;
- stakeholder needs and operational scenarios;
- system capabilities / functions / behavior / states;
- requirements;
- logical/physical architecture;
- human/system allocation;
- interface architecture and ICD-type control;
- alternatives/trade studies;
- integration planning;
- verification;
- validation;
- transition / deployment / acceptance;
- operations/support/maintenance;
- configuration/change control;
- retirement/disposal where in scope;
- system-of-systems relationships;
- technical risk/opportunity and decision management.

---

## 4｜Scope out / shared authority

Systems Engineering does not automatically own:
- domain-professional design correctness;
- statutory approval;
- specialist engineering calculations;
- software architecture/code quality unless separately assigned;
- human-factors/HCD evidence owned elsewhere;
- procurement/commercial approval;
- project-management scheduling/budget authority;
- operational authority;
- field/as-built truth without evidence.

`SYSTEMS ENGINEERING PASS ≠ DOMAIN PROFESSIONAL PASS ≠ DESIGN KEEP ≠ PROMOTION`.

---

## 5｜Cross-cutting practitioner control objects

### 5.1 Systems Engineering Responsibility / Authority Matrix
Track system authority, domain owners, interface owners, V&V owners, configuration/change authority and final decision authority.

### 5.2 System-of-Interest / Context / Boundary Register
Track system boundary, external systems, actors, environment, assumptions, external dependencies and changed-boundary reopen scope.

### 5.3 Stakeholder Need / Use-Case / Requirement Trace Matrix
Trace:
`STAKEHOLDER / NEED → OPERATIONAL SCENARIO → SYSTEM REQUIREMENT → ARCHITECTURE ELEMENT → VERIFICATION → VALIDATION`.

Need, requirement and verification evidence remain distinct.

### 5.4 Capability / Function / Behavior / State Register
Track capability, function, behavior/state, inputs/outputs, allocation, failure/degraded behavior and owning architecture element.

### 5.5 Information / Human-System Allocation / Interface Register
Track information entity, producer/consumer, human vs system responsibility, interface identity, exchanged item, condition, protocol/medium where relevant, failure behavior and acceptance evidence.

### 5.6 Assumption / Decision / Trade Study Register
For consequential architecture decisions:
- decision question;
- alternatives;
- criteria;
- assumptions;
- evidence;
- uncertainty;
- reversibility;
- rejected rationale;
- decision authority;
- reopen trigger.

`SCORE HIGHEST ≠ AUTOMATIC SYSTEM DECISION`.

### 5.7 Requirements Baseline / Normalization / Change Register
Track requirement ID, statement, rationale, source trace, owner, verification method, validation relevance, conflicts/duplicates, baseline, change authority and affected architecture/test objects.

### 5.8 Configuration / Baseline / Change Control Register
Track exact system/product/configuration baseline, controlled artifacts, revisions, change requests, impact, disposition, implementation and verification/revalidation scope.

### 5.9 Verification Cross-Reference Matrix
For each requirement:
- verification method;
- verification level;
- test/analysis/inspection/demonstration source;
- configuration/test article;
- procedure;
- acceptance criterion;
- result;
- anomaly;
- retest;
- closure.

`VERIFICATION = BUILT/IMPLEMENTED CORRECTLY AGAINST REQUIREMENTS`.

### 5.10 Validation Scenario / Evidence Matrix
Track user/stakeholder objective, operational context, scenario, representative system/configuration, validation method, expected outcome, observed outcome, limitation and disposition.

`VALIDATION = RIGHT SYSTEM FOR INTENDED USE / CONTEXT`.

### 5.11 Integration / Interface Verification Register
Track integration sequence, interface preconditions, interface version, connected elements, test condition, incompatibility/anomaly, workaround, owner and regression/retest scope.

### 5.12 Anomaly / Problem / Deviation / Waiver Decision Register
Track exact configuration and requirement/interface affected. A waiver cannot silently convert failed V&V to PASS; changed criterion/claim remains governed by Current Decision Rights and fresh validation semantics.

### 5.13 Transition / Operations / Support / Retirement Register
Track deployment/transition readiness, training, support, monitoring, spares/assets, operational constraints, maintenance, degraded operation, change feedback, retirement/decommissioning and knowledge return.

---

## 6｜SYSENG-DP0 — Scope, System of Interest & Authority

**Professional question:** What is the system of interest, where is its boundary, who owns consequential decisions, and what claim is this SE process allowed to make?

### Native outputs
- Systems Engineering Responsibility / Authority Matrix;
- System-of-Interest / Context / Boundary Register;
- initial lifecycle/use/transition scope;
- initial risk/assumption register;
- claim ceiling.

### Does not prove
stakeholder needs, architecture, requirements validity, V&V or operational success.

---

## 7｜SYSENG-DP1 — Stakeholder Needs, Operational Context & Concept

**Professional question:** What outcomes, actors, operational scenarios, constraints and degraded conditions must the system address before functions or solutions are committed?

### Required work
- stakeholders and affected actors;
- operational scenarios / mission threads;
- environment/context;
- external systems;
- normal/degraded/failure states;
- stakeholder needs and success conditions;
- human authority / responsibility conditions.

### Native outputs
- stakeholder need set;
- operational concept / mission threads;
- context diagrams;
- Stakeholder Need / Use-Case / Requirement Trace Matrix seed;
- unresolved need/assumption register.

### Does not prove
system requirements completeness or architecture feasibility.

---

## 8｜SYSENG-DP2 — Capabilities, Functions, Behavior & States

**Professional question:** What must the system be capable of doing, which functions/behaviors realise those capabilities, and how do states/degraded modes interact?

### Required work
- capability architecture;
- functional decomposition;
- functional relations/flows;
- state/mode behavior;
- failure/degraded behavior;
- reverse trace to stakeholder need;
- early allocation hypotheses without premature physical lock.

### Native outputs
- capability architecture;
- function catalogue;
- behavior/state models;
- Capability / Function / Behavior / State Register;
- reverse-trace report.

### Does not prove
requirements baseline, physical architecture or implementation feasibility.

---

## 9｜SYSENG-DP3 — Information, Human/System Allocation & Interfaces

**Professional question:** What information must exist/exchange, who or what performs each responsibility, and where are the system/interface boundaries?

### Required work
- information entities/relations/authority;
- human-only / human-led / assistable allocation;
- external/internal interfaces;
- interface contracts;
- failure/degraded interface behavior;
- acknowledgement vs acceptance;
- organizational authority interfaces.

### Native outputs
- information architecture;
- human/system allocation;
- interface architecture;
- Information / Human-System Allocation / Interface Register;
- interface-control / exchange set.

### Does not prove
interface implementation, domain design PASS or integration success.

---

## 10｜SYSENG-DP4 — System Requirements, Normalization & V&V Planning

**Professional question:** Are requirements necessary, traceable, solution-neutral enough, testable, non-contradictory and paired with credible verification/validation routes?

### Required work
- derive requirements from needs/capabilities/functions/interfaces/invariants;
- normalize duplicates/conflicts;
- remove solution bias/unverifiable wording;
- assign owner;
- define verification method;
- define validation relevance/scenario;
- preserve authority constraints and failure consequences;
- baseline/change control.

### Native outputs
- system requirements baseline;
- normalized requirements set;
- Requirements Baseline / Normalization / Change Register;
- Verification Cross-Reference Matrix plan;
- Validation Scenario / Evidence Matrix plan;
- requirement coverage / orphan / conflict report.

### Does not prove
implemented conformance or operational suitability.

---

## 11｜SYSENG-DP5 — Logical Architecture, Alternatives & Allocation

**Professional question:** Which logical architecture and allocation best satisfy the requirements while preserving interface, human authority, risk and V&V feasibility?

### Required work
- logical elements/responsibilities;
- materially different architecture alternatives;
- allocation of functions/requirements;
- interface/topology comparison;
- technical risk/opportunity;
- verification/integration consequences;
- trade study with uncertainty/reversibility;
- human decision.

### Native outputs
- logical architecture;
- architecture alternative set;
- allocation matrix;
- Assumption / Decision / Trade Study Register;
- selected/rejected architecture rationale.

### Does not prove
physical implementation readiness.

---

## 12｜SYSENG-DP6 — Physical Architecture / PBS, Integration Strategy & PDR Baseline

**Professional question:** Is the system decomposed into physical/realization elements with controlled interfaces, configuration and integration strategy sufficient for the current design baseline?

### Required work
- PBS / physical architecture;
- make/buy/realization boundaries where in scope;
- interface/control allocations;
- configuration items;
- integration sequence;
- V&V level allocation;
- operational/support constraints;
- preliminary design review readiness.

### Native outputs
- PBS / physical architecture;
- controlled interface set;
- integration strategy;
- configuration-item baseline;
- Configuration / Baseline / Change Control Register;
- PDR evidence package / disposition where applicable.

### Does not prove
production/implementation completion or V&V PASS.

---

## 13｜SYSENG-DP7 — Integration, Verification, Validation & Transition

**Professional question:** Does the implemented system/configuration satisfy requirements, work across interfaces and meet intended stakeholder use in the declared context?

### Required work
- configuration/test-article identity;
- integration execution;
- interface verification;
- requirement verification;
- anomaly/problem/change;
- regression/retest;
- validation scenarios;
- acceptance/transition readiness;
- residual limitation.

### Native outputs
- Verification Cross-Reference Matrix results;
- Validation Scenario / Evidence Matrix results;
- Integration / Interface Verification Register;
- anomaly/problem/deviation register;
- transition/acceptance evidence;
- residual open-item register.

### Hard boundary

`VERIFICATION PASS ≠ VALIDATION PASS`.

`COMPONENT PASS ≠ INTEGRATED SYSTEM PASS`.

### Does not prove
future operational performance or domain-professional approval outside Systems Engineering scope.

---

## 14｜SYSENG-DP8 — Operations, Support, Change, Retirement & Learning

**Professional question:** What does actual operation reveal, what must change/reverify/revalidate, and how are support, retirement and learning bounded?

### Required work
- operations/performance evidence;
- incidents/anomalies;
- maintenance/support;
- configuration change;
- degraded operation;
- obsolescence;
- transition/retirement;
- post-change V&V;
- bounded knowledge return.

### Native outputs
- Transition / Operations / Support / Retirement Register;
- operational discrepancy register;
- post-change V&V record;
- retirement/decommissioning plan where triggered;
- bounded G9 learning candidates.

### Does not prove
causal reusable knowledge without G9 validation.

---

## 15｜Professional interface map

Systems Engineering exchanges controlled variables with every triggered domain. It does not become a super-authority over those professions.

Typical shared objects:
- stakeholder/use requirements;
- system capabilities/functions;
- allocated requirements;
- interface conditions;
- physical envelopes;
- performance budgets;
- failure/degraded states;
- verification evidence;
- validation scenarios;
- configuration/change state.

`SYSTEM ALLOCATION ≠ DOMAIN PROFESSIONAL APPROVAL`.

---

## 16｜Mandatory HOLD / REVISE

Hold/revise when:
- system boundary is unresolved for a consequential decision;
- stakeholder needs are feature lists without source/context;
- functions are written as premature components;
- requirements lack source/rationale/verification method;
- duplicate/conflicting requirements are silently retained;
- one trade score chooses the architecture automatically;
- interface ownership is ambiguous;
- configuration tested differs from configuration claimed;
- requirement verification is inferred from design intent;
- validation is replaced by verification;
- component tests are used as integrated-system PASS;
- a waived/changed requirement mutates historical failed evidence to PASS;
- operational change does not trigger impact/reverification/revalidation;
- Systems Engineering claims another profession's approval.

---

## 17｜Candidate promotion boundary

Remain Candidate until:
1. machine definition validates against the Current Professional Domain Process Contract;
2. current professional-source audit is reviewed;
3. at least one real project/system instance exercises requirements→architecture→V&V trace;
4. one interface/integration failure path is preserved;
5. verification and validation are independently evidenced;
6. a configuration/change reopen path is exercised;
7. independent Systems Engineering review confirms practitioner realism;
8. authorized promotion updates Current Architecture Map / owner pointers.

Until then:

`SYSTEMS ENGINEERING DOMAIN PROCESS = OPEN`.

---

## 18｜Candidate invariants

`NEED ≠ REQUIREMENT`

`FUNCTION ≠ COMPONENT`

`REQUIREMENT PRESENT ≠ REQUIREMENT VALID`

`ARCHITECTURE SELECTED ≠ IMPLEMENTATION VERIFIED`

`VERIFICATION ≠ VALIDATION`

`COMPONENT PASS ≠ SYSTEM INTEGRATION PASS`

`SYSTEMS ENGINEERING ≠ DOMAIN SUPER-AUTHORITY`

`CURRENT PROFESSIONAL PROCESS REMAINS OPEN UNTIL EXPLICIT PROMOTION`.

---

## 2026-09-19｜Execution Binding Contract｜Systems Engineering professional-depth parity

**Status effect:** additive candidate-depth binding only. Systems Engineering remains `CANDIDATE / NOT CURRENT / NO PROMOTION`. No universal lifecycle, MBSE product or new Systems Skill family is created.

### Knowledge binding
Consequential SE decisions resolve Current sources/methods for need/goal/requirement, trade study, interfaces, configuration, verification and validation. Applicable anchors include:
- `KN-METHOD-DESIGN-GOAL-CONTRACT-001` — Need vs Goal vs Objective vs Requirement vs Criterion boundary;
- `KN-METHOD-DESIGN-TRADE-STUDY-001` — alternatives / hard gates / uncertainty / sensitivity / decision corridor;
- `SRC-NASA-STAKEHOLDER-GOALS-001` — scoped need/goal/objective/requirement source;
- `SRC-NASA-DECISION-ANALYSIS-001` — scoped systems decision-analysis/trade-study source;
- current requirements-engineering, interface-management, configuration/change, V&V and domain-professional sources.

### `required_native_outputs[]`
- Systems Engineering responsibility/authority matrix and System-of-Interest/context/boundary register;
- stakeholder need / use-case / requirement trace matrix;
- capability / function / behavior / state register and models;
- information / human-system allocation / interface register;
- normalized system requirements baseline and change register;
- logical architecture alternatives, allocation and trade-study records;
- PBS / physical architecture / controlled interface set and configuration baseline;
- verification cross-reference matrix and integration/interface verification evidence;
- validation scenario/evidence matrix;
- anomaly/problem/deviation/waiver decision register with retest/reverification state;
- transition / operations / support / retirement register and post-change V&V record.

### `execution_owner_requirements[]` / `required_capabilities[]`
- `oleander-research [INSTALLED_CORE]` — external standards/source comparison/evidence;
- `oleander-design-process [INSTALLED_CORE]` — goal framing, function-to-concept synthesis, trade-space/design reasoning, interface coupling and change propagation; **not independent Systems Engineering approval**;
- `oleander-data-viz [INSTALLED_CORE]` — system/trace/relationship visualization when useful; visualization does not become requirements/configuration authority;
- `oleander-delivery-qc [INSTALLED_CORE]` — package/export integrity only.

Relevant existing `oleander-design-process` extensions may be selected by the resolver when triggered: `FUNCTION_TO_CONCEPT_SYNTHESIS_EXTENSION`, `SYSTEM_INTERFACE_COUPLING_EXTENSION`, `REQUIREMENT_VERIFICATION_TRACEABILITY_EXTENSION`, `INFORMATION_REQUIREMENT_EXCHANGE_CONTRACT_EXTENSION`, and computational option-space support. They refine the current object; they are not a parallel Systems Engineering process.

**Specialist execution gap / routing rule:** the Current core Skill Registry has no installed Systems Engineering / requirements / MBSE / configuration / V&V specialist Skill. Consequential SE claims must bind the actual project SE owner, domain professionals, requirements/configuration repository and verification/validation tools/evidence appropriate to the project. `MODEL / TRACE TOOL PASS ≠ SYSTEMS ENGINEERING PASS`.

### `tool_adapter_requirements[]`
- controlled requirements/need/use-case repository with stable IDs, source, version, status and change history;
- system/context/function/behavior/interface modelling carrier appropriate to the decision;
- configuration/baseline/change-control carrier;
- test/analysis/simulation/inspection/runtime evidence carrier for verification as applicable;
- user/mission/operational scenario evidence carrier for validation;
- anomaly/problem/deviation/waiver and retest/reverification record;
- project-authorized MBSE/requirements/test tools when used; tool syntax/product semantics cannot redefine OLEANDER or project authority.

### `typed_handoff_contracts[]`
- Project/Stakeholder Authority → SE: need/mission/outcome/constraints/decision rights;
- HCD/Operations → SE: user/operational scenarios, human-system needs and validation context;
- SE → Domain Professionals: requirement/interface/allocation objects with IDs, source, rationale, assumptions and acceptance owner;
- Domain Professionals → SE: feasibility/performance/interface evidence + limits + changed assumptions;
- SE → Implementation/Integration: configuration baseline, interface contract, verification method and required evidence;
- Verification → SE: exact requirement/configuration/procedure/result/anomaly;
- Validation → SE: exact use context/scenario/configuration/outcome/limitation;
- Change Authority → SE: authorized change → affected requirements/interfaces/configuration → reverification/revalidation scope.

### `actual_readback_requirements[]`
- stakeholder need → requirement → architecture/allocation → verification → validation trace;
- requirement quality and normalization against source intent, not merely field completeness;
- logical/physical architecture and interface consistency at the current baseline;
- configuration identity of every V&V result;
- verification method/result against the exact requirement and acceptance criterion;
- validation scenario/context/outcome against intended use and stakeholder need;
- anomaly/deviation/waiver disposition and exact retest/reverification/revalidation closure;
- post-change impact graph, not only edited requirement text.

### `reopen_triggers[]`
System boundary/external dependency change; stakeholder need/mission/use-case change; requirement source/interpretation change; function/allocation/interface/architecture/configuration change; domain-professional constraint change; failed verification/integration/validation; anomaly/deviation/waiver; operational evidence; transition/support/retirement assumption change.

### Object-level invocation matrix

#### A｜Need / Context / Operational Concept
- Knowledge: goal-contract + stakeholder/mission/operational sources.
- Skills: research + design-process; HCD/domain owners when human/domain evidence is consequential.
- Tool class: controlled context/use-case/need repository and editable context/mission-thread carrier.
- Native carrier: SOI boundary, external systems/actors/environment, needs, operational scenarios, assumptions.
- Readback: boundary and scenario cover the claimed mission/use; need/goal/requirement distinctions remain intact.
- Reopen: boundary/mission/stakeholder/context/external dependency change.

#### B｜Capability / Function / Behavior / Human-System / Interface Architecture
- Knowledge: function-to-concept, interface coupling and applicable domain/HCD sources.
- Skills: design-process installed owner + domain professionals; data-viz optional for analytical relation views.
- Tool class: editable system model/graph/table with stable IDs and typed relations.
- Native carrier: capability/function/behavior/state, information architecture, human-system allocation, interface register.
- Readback: solution-neutral functions are not prematurely physicalized; interface direction/data/energy/material/control/permission semantics agree across views.
- Reopen: function/allocation/interface/state/domain constraint change.

#### C｜Requirements Baseline / Normalization / Change
- Knowledge: current requirements-engineering sources + goal/requirement boundary.
- Skills: design-process requirement trace support; project SE/configuration owner required.
- Tool class: requirements repository with source, rationale, verification method, owner, baseline and change history.
- Native carrier: normalized requirement set, trace matrix, baseline/change register.
- Readback: every material requirement has source/intent/applicability/testability and does not silently narrow the source.
- Reopen: source/interpretation/architecture/interface/feasibility/test-method or authorized-change delta.

#### D｜Logical / Physical Architecture + Trade Study
- Knowledge: trade-study owner + function-to-concept + domain constraints.
- Skills: design-process; computational option-space only when variables/constraints justify it; domain professionals close specialist feasibility.
- Tool class: architecture/allocation model + trade-study ledger with uncertainty/sensitivity.
- Native carrier: alternatives, allocation, logical architecture, PBS/physical architecture, decision record.
- Readback: concept families materially differ; hard gates/unknowns/sensitivity visible; score does not auto-select the system.
- Reopen: requirement/interface/domain feasibility/cost-risk/assumption/change evidence.

#### E｜Verification / Integration / Anomaly
- Knowledge: requirement-verification traceability + interface/configuration sources.
- Skills: design-process for trace/change; actual domain/test/simulation/integration owner = `PROJECT_SPECIALIST_REQUIRED`.
- Tool class: test/analysis/simulation/inspection/runtime evidence tied to exact configuration.
- Native carrier: verification cross-reference, interface verification, anomaly/deviation/waiver, retest record.
- Readback: requirement + method + configuration + result + criterion + anomaly disposition are all exact and current.
- Reopen: configuration/method/criterion/result/anomaly/fix change.

#### F｜Validation / Transition / Operations / Retirement
- Knowledge: stakeholder need/use context + HCD/operations/support sources.
- Skills: design-process + HCD/domain/operations owners as applicable.
- Tool class: validation scenario/evidence + operational/support/transition records.
- Native carrier: validation matrix, transition/support/retirement register, operational discrepancy, post-change V&V.
- Readback: validation proves intended-use evidence for the current configuration/context, not merely requirement verification.
- Reopen: intended use/user/mission/operational environment/configuration/support/retirement condition change.

### Professional boundary
`TRACE COMPLETE ≠ REQUIREMENTS VALID`; `MODEL COMPLETE ≠ ARCHITECTURE ACCEPTED`; `VERIFICATION PASS ≠ VALIDATION PASS`; `SYSTEMS ENGINEERING PASS ≠ DOMAIN PROFESSIONAL PASS`; `TOOL CONSISTENCY ≠ CONFIGURATION AUTHORITY`; `CI / EXPORT PASS ≠ PROFESSIONAL REVIEW`.
## External Mature-KB Absorption Delta｜NASA IRD + V&V｜2026-09-20

Status: `CANDIDATE STRENGTHENING / SOURCE-BOUND / NO PROMOTION`.

### Source mount
- `SRC-NASA-SE-APPENDIX-IRD-VV-001` — NASA Systems Engineering Handbook appendices / interface + verification + validation control artifacts: https://app.notion.com/p/3e1b86be5c4781048b6fe7b4bd23a455

This L6 SOURCE is `SUPPORT / SCOPED`. NASA lifecycle/governance is not imported as a universal OLEANDER process.

### Typed native control objects
- `REQ VERIFICATION OBJECT = requirement_id + definitive_source + acceptance_criterion + verification_method + verification_level + owner + exact_configuration + result_ref + anomaly/disposition`;
- `VALIDATION OBJECT = stakeholder_need + intended_use/context + scenario/method + exact_configuration + evidence_ref + observed_outcome + limitation + residual_risk`;
- `INTERFACE OBJECT = interface_id + precedence + side_A/side_B responsibility + change_authority + coordinate_system + engineering_units + tolerance/limit_contract + detailed_requirements + verification_ref`.

### Hard attacks
- `TRACE COMPLETE ≠ REQUIREMENT VALID`;
- `VERIFICATION ≠ VALIDATION`;
- `INTERFACE DRAWING ≠ INTERFACE CONTRACT` when precedence, responsibility, coordinate/unit/tolerance or change authority is missing;
- local subsystem PASS cannot close tightly-coupled integration.

### Configuration/change consequence
Every V&V result must bind exact configuration identity. A material requirement/interface/configuration change reopens affected verification, integration and validation scope rather than merely editing the latest document.

### Boundary
`NASA CONTROL ARTIFACT SOURCE ABSORBED ≠ NASA LIFECYCLE ADOPTION ≠ SYSTEMS CURRENT ≠ DOMAIN PROFESSIONAL PASS ≠ INTEGRATED SYSTEM TRUTH`.
