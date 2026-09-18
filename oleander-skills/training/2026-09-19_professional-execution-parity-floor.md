# 2026-09-19｜Professional Execution Parity Floor / 横向颗粒度铺平

Status: `HORIZONTAL PARITY IMPLEMENTATION / EXISTING R-E CONTRACT EXTENDED / DOMAIN SEMANTICS PRESERVED / NO BLANKET PROMOTION`

## User direction

`横向铺平`

Interpretation:

> All formally triggered professional domains must reach the same **professional execution-depth floor**, but must not be forced into the same stage count, page count, template or work-product vocabulary.

`SAME GRANULARITY ≠ SAME STAGES ≠ SAME LENGTH ≠ SAME ARTIFACTS`.

---

# 1｜Audit scope

Domains reviewed:

1. Architecture
2. Structural Engineering
3. Building Services / MEP
4. Interior Design
5. Landscape Architecture
6. Lighting Design
7. Digital Product / HCD
8. Systems Engineering

Current architecture status is preserved:
- Architecture = Current formalized / project-exercised reference;
- Structural Engineering = Current formalized + machine-bound;
- Building Services / MEP = Current formalized + machine-bound;
- Interior Design = Candidate / domain process remains OPEN;
- Landscape Architecture = Candidate / OPEN;
- Lighting Design = Candidate / OPEN;
- Digital Product / HCD = Candidate / OPEN;
- Systems Engineering = Candidate / OPEN.

The parity work does not infer Current promotion from definition depth.

---

# 2｜Parity dimensions

The existing Professional Domain Process Contract now requires every process definition to expose an `execution_depth_contract` with:

1. `professional_problem_and_judgment_objects[]`
2. `assumption_uncertainty_objects[]`
3. `option_comparison_objects[]`
4. `native_work_objects[]`
5. `release_control_objects[]`
6. `implementation_field_objects[]`
7. `handover_inuse_objects[]`
8. `independent_review_objects[]`
9. `change_propagation_objects[]`

And:
- `parity_rule`
- `does_not_require[]`

This is enforced by:
- `professional-domain-process.v1.schema.json`;
- `validate_professional_domain_process.py`.

A stage-rich definition without domain-native execution objects is below the floor.

---

# 3｜Audit result before repair

## Architecture

Strength:
- complete ADD-00…17 reasoning chain;
- program / adjacency / options / flow / circulation / code-aware planning / system fit-back / independent plan review;
- project-exercised reference.

Gap:
- no same-level machine-readable process definition;
- practitioner control objects less explicit than Interior / Lighting;
- later procurement/field/closeout objects existed only implicitly/conditionally.

Repair:
- machine-readable `architecture-design-development-process.v1.json`;
- 9 cross-cutting practitioner control objects.

## Structural Engineering

Strength:
- authentic IStructE-aligned stage semantics;
- Basis of Structural Design;
- responsibility/checking/change control;
- real concept/technical/production/construction/handover/use chain.

Gap:
- production/fabrication/inspection/field/closeout objects were named too generically.

Repair:
- Analysis / Calculation Baseline & Check Register;
- Member / Connection / Foundation Release Schedule;
- Fabrication / Shop Drawing / Specialist Submittal Release Register;
- Inspection / Test / Material / ITP Evidence Register;
- Structural RFI / Field Change / Nonconformity Register;
- Structural Closeout / Residual Risk / Monitoring Register.

## Building Services / MEP

Strength:
- authentic system tracks;
- commissioning from early design through in-use;
- controls and measured-performance distinction;
- strong technical and operational chain.

Gap:
- production/submittal/field/closeout evidence was less explicitly objectized than commissioning semantics.

Repair:
- Equipment / System Submittal & Substitution Release Register;
- Builder's Work / Installation / Access Coordination Register;
- Inspection / Test / TAB / Commissioning Witness Matrix;
- MEP RFI / Field Change / Defect Register;
- O&M / Asset / Training / Seasonal Closeout Register.

## Interior Design

Strength:
- practitioner-grade reference depth already present;
- RCP, door/hardware, finish, joinery, FF&E, procurement, submittal, mockup, QA/QC, closeout and POE objects.

Repair:
- no content expansion required for parity;
- existing objects mapped explicitly into `execution_depth_contract`.

## Landscape Architecture

Strength:
- correct professional scope and evidence ceiling;
- 11 technical threads;
- grading/drainage/soil/planting/irrigation/hardscape/construction/establishment/in-use stages;
- C04 bounded HOLD exercise.

Gap:
- technical threads were stronger than their persistent release/execution carriers.

Repair:
- Site / Base Authority & Survey Change Register;
- Grading / Drainage Interface Schedule;
- Earthwork / Soil Movement Schedule;
- Retained Tree / Vegetation Protection Execution Register;
- Planting / Soil Establishment & Replacement Register;
- Irrigation / Water / Control Interface Register;
- Material / Submittal / Sample / Mockup / Substitution Release Register;
- Field Change / RFI / Nonconformity Register;
- Maintenance / Operations Access Schedule.

## Lighting Design

Strength:
- deepest candidate practitioner semantics in the current corpus;
- visual tasks, model configurations, photometrics, product/optics, controls, submittal/substitution, aiming/focusing, commissioning, replacement equivalence and post-occupancy.

Repair:
- no content expansion required for parity;
- existing practitioner objects mapped into the shared parity contract.

## Digital Product / HCD

Strength:
- context/needs/interaction/usability/accessibility/implementation/live chain;
- C04 bounded HOLD exercise;
- strong state/error/offline design semantics.

Gap:
- evidence lifecycle was stage-correct but practitioner carriers for study freeze, consent/data eligibility, finding closure, release support and rollout were one level less explicit.

Repair:
- Study Repository / Research Freeze Register;
- Consent / Data Eligibility Register;
- Finding → Fix → Build → Retest Chain;
- Release Support Matrix;
- Content / Localization Release Register;
- Privacy / Security Interaction Handoff Register;
- Instrumentation / Outcome Definition Register;
- Experiment / Rollout Object.

## Systems Engineering

Before:
- Current Architecture Map reserved the professional domain but no R-E professional process carrier existed in repo.
- The user's Library already contains a deep zero-base OLEANDER system-definition chain:
  Behaviour Research → Pure User Needs → Experience Requirements → Context → Operational Concept → Capability → Functional → Information → Human/System Allocation → Interface → Requirements → Logical Architecture → Alternatives/Allocation → PBS/Physical Architecture → PDR.

Repair:
- add Candidate Systems Engineering professional process;
- compile existing OLEANDER system-design semantics rather than invent a disconnected second framework;
- preserve domain-professional authority.

---

# 4｜Systems Engineering professional-source calibration

Public current/recent sources used to calibrate, not copy, professional scope:

## ISO/IEC/IEEE 15288:2023
Current published system life-cycle process framework.
Key transfer:
- processes may be iterative/concurrent/recursive;
- no single lifecycle model/method is mandated;
- supports full lifecycle and technical-management framing.

## INCOSE Systems Engineering Handbook — Fifth Edition
Current practitioner state-of-good-practice reference.

## NASA Systems Engineering Handbook
Public practitioner reference used for:
- system design;
- product realization;
- cross-cutting technical management;
- integration;
- verification;
- validation;
- transition/operations.

No external stage sequence is copied into OLEANDER.

---

# 5｜Systems Engineering Candidate structure

Prose:
`00-governance/systems-engineering-design-process-v1.0-CANDIDATE.md`

Machine:
`00-governance/schemas/systems-engineering-design-process.v1.candidate.json`

Stages:
- SYSENG-DP0 Scope, System of Interest & Authority
- SYSENG-DP1 Stakeholder Needs, Operational Context & Concept
- SYSENG-DP2 Capabilities, Functions, Behavior & States
- SYSENG-DP3 Information, Human/System Allocation & Interfaces
- SYSENG-DP4 System Requirements, Normalization & V&V Planning
- SYSENG-DP5 Logical Architecture, Alternatives & Allocation
- SYSENG-DP6 Physical Architecture / PBS, Integration Strategy & PDR Baseline
- SYSENG-DP7 Integration, Verification, Validation & Transition
- SYSENG-DP8 Operations, Support, Change, Retirement & Learning

Practitioner objects include:
- Systems Engineering Responsibility / Authority Matrix
- System-of-Interest / Context / Boundary Register
- Stakeholder Need / Use-Case / Requirement Trace Matrix
- Capability / Function / Behavior / State Register
- Information / Human-System Allocation / Interface Register
- Assumption / Decision / Trade Study Register
- Requirements Baseline / Normalization / Change Register
- Configuration / Baseline / Change Control Register
- Verification Cross-Reference Matrix
- Validation Scenario / Evidence Matrix
- Integration / Interface Verification Register
- Anomaly / Problem / Deviation / Waiver Decision Register
- Transition / Operations / Support / Retirement Register

Hard boundary:
`VERIFICATION ≠ VALIDATION`.

Systems Engineering remains an integration/traceability/architecture/V&V profession, not a super-authority over Architecture, Structural, MEP, Interior, Landscape, Lighting, HCD or statutory owners.

---

# 6｜Architecture machine parity

Architecture remains the Current reference process.

New machine carrier:
`00-governance/schemas/architecture-design-development-process.v1.json`

It mirrors the existing Current ADD-00…17 chain; it does not create a second Architecture process.

Architecture Map factual readback is updated from:
Architecture Current but not machine-carrier explicit
to:
`FORMALIZED + MACHINE_BOUND + PROJECT-EXERCISED REFERENCE`.

No Architecture lifecycle or stage IDs are changed.

---

# 7｜Anti-regression

AIG failure cases added:

- `FAIL-041` — many stages/framework prose claimed as professional execution parity without practitioner/release/implementation objects;
- `FAIL-042` — horizontal parity misread as identical stage/template/artifact structure;
- `FAIL-043` — Verification and Validation collapsed;
- `FAIL-044` — Systems Engineering used as domain super-authority.

These supplement existing Interior `FAIL-023..030` and Lighting `FAIL-031..040` practitioner regressions.

---

# 8｜What this work explicitly does not do

No:
- universal professional stage sequence;
- universal page count;
- universal table set;
- new Core Skill;
- second professional-process framework;
- automatic promotion of Candidate domains;
- automatic professional PASS from machine definition;
- automatic project exercise claim for Structural/MEP/Systems Engineering;
- replacement of domain-professional authority by Systems Engineering.

---

# 9｜Parity-floor interpretation

A professional domain meets the **definition-level execution floor** when it can answer, in its own semantics:

1. What professional question is being decided?
2. What assumptions/unknowns remain?
3. What materially different alternatives exist?
4. What native/editable work objects carry the decision?
5. What object is released/checked before downstream reliance?
6. What real implementation/field/runtime evidence exists?
7. What closes handover/in-use/maintenance/live operation where applicable?
8. Who independently reviews it?
9. What exact objects/interfaces reopen after change?

This still does **not** prove:
- project execution;
- independent review occurred;
- professional PASS;
- field/runtime truth;
- Design KEEP;
- Promotion.

---

# 10｜Target maturity after this batch

Definition-level target:

`EIGHT PROFESSIONAL DOMAINS → ONE SHARED CONTRACT ENVELOPE → DOMAIN-NATIVE EXECUTION_DEPTH_CONTRACT → MACHINE VALIDATION → NO TEMPLATE FLATTENING`.

Current/candidate authority remains unchanged except for factual Architecture machine-binding readback.

`PARITY FLOOR PASS ≠ CURRENT PROMOTION`

`DEFINITION DEPTH ≠ PROJECT EXECUTION`

`PROJECT EXECUTION ≠ PROFESSIONAL PASS`

`PROFESSIONAL PASS ≠ DESIGN KEEP`.
