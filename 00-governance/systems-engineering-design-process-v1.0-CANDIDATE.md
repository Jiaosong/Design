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
