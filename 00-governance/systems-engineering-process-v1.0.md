# OLEANDER Systems Engineering Process v1.0

**Status:** CANDIDATE PROFESSIONAL DOMAIN PROCESS / CONTROLLED EVOLUTION INPUT  
**Domain:** Systems Engineering  
**Authority position:** subordinate to `complex-project-master-runtime-v1.0.md`, `OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1`, `professional-domain-process-contract-v1.0.md`, Current Knowledge Authority, Shared Design Quality, Cross-Disciplinary Integration, project/system authority and applicable engineering, safety, security, regulatory and configuration owners.  
**Primary professional basis:** ISO/IEC/IEEE 15288:2023; INCOSE Systems Engineering Handbook, Fifth Edition (2023); ISO/IEC/IEEE 29148:2018 for requirements engineering, noting that a third-edition DIS is under development in 2026 and does not supersede the published 2018 edition until formally replaced.  
**Existing OLEANDER knowledge context:** current systems-thinking, decision-analysis, requirements, architecture/interface, risk, verification/validation and domain-specific engineering evidence remain existing Knowledge owners. This process mounts/consumes them and does not create a parallel Systems Engineering knowledge tree.

---

## 1｜Why this process exists

Systems Engineering is needed when a materially complex system-of-interest cannot be responsibly designed, integrated and evidenced as a set of independent discipline outputs. It provides professional logic for stakeholder needs, system requirements, architecture, allocation, interfaces, technical decision-making, integration, verification, validation, transition, operation/support and lifecycle change.

It is not a project-management synonym, not a requirements spreadsheet, not a software-only process, and not a universal OLEANDER meta-process.

Canonical professional chain:

```text
SYSTEM-OF-INTEREST / AUTHORITY / LIFECYCLE CONTEXT
→ STAKEHOLDER NEEDS / CONCERNS / USE CASES
→ SYSTEM REQUIREMENTS + MEASURES
→ SYSTEM ARCHITECTURE / ELEMENTS / ALLOCATION
→ INTERFACES / BUDGETS / TRADE STUDIES / RISKS
→ ELEMENT REALIZATION / SUPPLY / DOMAIN OUTPUTS
→ SYSTEM INTEGRATION
→ VERIFICATION AGAINST SPECIFIED REQUIREMENTS
→ VALIDATION AGAINST INTENDED USE / STAKEHOLDER NEEDS
→ TRANSITION / DEPLOYMENT / HANDOVER
→ OPERATION / SUPPORT / CHANGE / RETIREMENT READBACK
→ REOPEN / G9 CANDIDATE RETURN
```

Hard boundaries:

```text
REQUIREMENTS LIST ≠ SYSTEMS ENGINEERING
MBSE MODEL ≠ SYSTEM TRUTH
SYSTEM ARCHITECTURE DIAGRAM ≠ INTEGRATED SYSTEM
ELEMENT PASS ≠ SYSTEM PASS
INTERFACE DOCUMENT ≠ INTERFACE VERIFIED
SIMULATION PASS ≠ PHYSICAL / OPERATIONAL VALIDATION
VERIFICATION ≠ VALIDATION
TECHNICAL REVIEW ≠ STATUTORY / LICENSED APPROVAL
SYSTEMS ENGINEERING ≠ PROJECT MANAGEMENT
SYSTEMS ENGINEERING ≠ R-F CROSS-DISCIPLINARY INTEGRATION AUTHORITY
CONFIGURATION RECORD ≠ CURRENT AUTHORITY BY RECENCY
V&V PASS IN ONE CONFIGURATION ≠ ALL CONFIGURATIONS
SYSTEMS ENGINEERING PROCESS PASS ≠ DESIGN KEEP ≠ PROJECT PROMOTION
```

---

## 2｜Professional-source alignment and internal decision carriers

ISO/IEC/IEEE 15288:2023 establishes a common framework of system life-cycle process descriptions and explicitly does **not** prescribe one life-cycle model, methodology, modelling approach or technique. The INCOSE Systems Engineering Handbook Fifth Edition aligns with the 2023 process framework while elaborating practice, tailoring and methods.

OLEANDER therefore does **not** rename the 15288 process set into a compulsory linear stage sequence. It uses internal decision carriers that organize evidence/readback while allowing iteration, concurrency and tailoring:

```text
SE-BASIS        System-of-interest / authority / lifecycle / tailoring basis
SE-NEEDS        Stakeholder needs / concerns / use scenarios / measures of effectiveness
SE-REQ          System requirements / traceability / acceptance measure basis
SE-ARCH         System architecture / element decomposition / allocation / budgets
SE-TRADE        Decision analysis / alternatives / risk / uncertainty / technical planning
SE-REALIZE      Element realization / acquisition / supplier / domain evidence coordination
SE-INTEGRATE    Planned system integration / configuration / interface realization
SE-VERIFY       Verification against specified system requirements
SE-VALIDATE     Validation against intended use / stakeholder needs / operational context
SE-TRANSITION   Transition / deployment / training / acceptance-support / handover
SE-INUSE        Operation / support / maintenance / change / disposal / lifecycle return
```

These are OLEANDER internal professional decision carriers, **not ISO 15288 official stage IDs**. Individual 15288 processes can recur across several carriers or run concurrently.

Professional synchronization with Architecture `ADD-*`, Structural `SE-SPW*`, MEP `BSP-*`, HCD `HCD-*`, software or specialist domains is by required information/interface maturity, not matching numbers.

---

## 3｜Trigger / applicability

Trigger Systems Engineering when the project makes material system-level claims involving one or more of:

- multiple interacting technical/human/physical/software/organizational elements;
- stakeholder needs that must trace to system requirements and acceptance evidence;
- system architecture and allocation across elements/domains;
- complex or safety-/mission-/business-critical interfaces;
- system-level performance budgets or resource constraints;
- alternative architectures/trade studies with multi-variable consequences;
- integration sequencing/configuration dependence;
- verification and validation across multiple evidence types;
- system transition/deployment/commissioning across elements;
- operation/support/maintenance lifecycle responsibility;
- systems of systems or embedded systems;
- complex brownfield/legacy integration;
- requirements/configuration change with propagated downstream effects.

Do not infer Systems Engineering completion merely because:

- a project has many disciplines;
- a requirements spreadsheet exists;
- an architecture diagram or SysML model exists;
- domain components passed their own tests;
- coordination meetings occurred;
- an integration platform reports healthy status.

For promotion-relevant scope, `NOT_REQUIRED` must be explicit under Current trigger/applicability control. Omission is not `NOT_REQUIRED`.

---

## 4｜System-of-interest / authority boundary

Every Systems Engineering invocation must name the **system-of-interest (SoI)** and its boundary. Different hierarchical levels can each be systems in their own right; evidence must not slide between levels without an explicit relation.

Record at minimum:

- SoI identity and version/configuration;
- lifecycle context and intended use;
- owning organization / technical authority;
- acquiring/supplying parties when material;
- external systems / enabling systems;
- operational environment;
- project/program/contract authority relations;
- regulated/safety/security authority interfaces;
- element/decomposition boundary;
- claims excluded from the current SE scope.

Hard separations:

`SYSTEM BOUNDARY ≠ ORGANIZATION CHART`.

`SYSTEM OWNER ≠ EVERY ELEMENT'S PROFESSIONAL AUTHORITY`.

`SE TECHNICAL AUTHORITY ≠ STATUTORY AUTHORITY`.

---

## 5｜Knowledge Integrity / Operational Mount

Consequential system decisions use task/claim-scoped mounts under `knowledge-integrity-and-operational-mount-v1.0.md`.

Existing OLEANDER routes may include:

- NASA Systems Engineering Handbook / Decision Analysis SOURCE objects;
- systems-thinking and complexity knowledge;
- requirements-engineering sources;
- architecture/modelling methods;
- reliability, safety, security and risk methods under their owners;
- domain engineering sources and native test evidence;
- supplier/product/system evidence;
- project configuration and interface evidence;
- operational/incidence/maintenance evidence.

Knowledge boundaries:

```text
REFERENCE ARCHITECTURE ≠ PROJECT ARCHITECTURE
PAST TRADE STUDY ≠ CURRENT DECISION
REQUIREMENT TEMPLATE ≠ VALID REQUIREMENT SET
MODEL CONSISTENCY ≠ PHYSICAL TRUTH
SUPPLIER CLAIM ≠ INTEGRATED SYSTEM PERFORMANCE
ONE-PROJECT LESSON ≠ UNIVERSAL SYSTEMS RULE
```

Existing Knowledge Architecture L0–L7 remains the only knowledge hierarchy.

---

## 6｜Cross-cutting Systems Engineering control objects

### 6.1 System Basis / Tailoring / Responsibility Matrix

Record:

- SoI, lifecycle and claim boundary;
- applicable 15288 process responsibilities and tailored exclusions;
- technical authority and decision rights;
- discipline/element owners;
- verification/validation owners;
- safety/security/regulatory interfaces;
- configuration/change responsibility;
- supply/acquisition responsibility;
- required independent review.

Tailoring must be explicit. “Agile”, “small project” or “concept stage” is not sufficient reason to silently omit a required outcome.

### 6.2 Stakeholder Need / Concern Register

For each material stakeholder/affected actor:

`STAKEHOLDER → CONTEXT / MISSION / USE → NEED / CONCERN → PRIORITY / AUTHORITY → SUCCESS MEASURE → SOURCE / EVIDENCE → CONFLICT / TRADE-OFF → REQUIREMENT TRACE`.

Needs are not automatically system requirements; translation requires engineering interpretation and acceptance criteria.

### 6.3 System Requirement / Traceability Register

For each consequential requirement preserve:

- stable requirement ID;
- statement and rationale;
- source / owner / authority;
- applicability / configuration;
- priority/criticality;
- measure / tolerance / acceptance method;
- allocation to system element(s);
- parent/derived relation;
- interface dependency;
- verification method / level;
- validation relation where applicable;
- change history and affected downstream artifacts.

`TRACE EXISTS ≠ REQUIREMENT IS CORRECT`.

### 6.4 System Architecture / Allocation Register

Record:

- functions/behaviours;
- logical/physical elements;
- allocation relations;
- system states/modes;
- interfaces;
- performance/resource budgets;
- redundancy/fault-containment where relevant;
- enabling systems;
- alternatives considered and rejected;
- architecture decision rationale;
- assumptions/uncertainty.

### 6.5 Interface Control Register

System Engineering may own a domain-native interface specification/control artifact, but OLEANDER R-F remains the owner of cross-disciplinary **maturity/disposition truth**.

Each material interface should resolve:

`END A / OWNER → END B / OWNER → EXCHANGED MATTER/ENERGY/DATA/CONTROL/HUMAN ACTION → DIRECTION → LIMIT / TIMING / PROTOCOL / GEOMETRY → SOURCE OF TRUTH → CONFIGURATION → VERIFICATION → CHANGE OWNER`.

### 6.6 Technical Decision / Trade Study Register

Preserve:

`DECISION QUESTION → FEASIBLE ALTERNATIVES → CRITERIA → WEIGHTS/AUTHORITY (IF USED) → EVIDENCE → UNCERTAINTY/SENSITIVITY → RISKS → TRADE-OFF → DECISION → CONDITIONS → REOPEN TRIGGER`.

A weighted score is a decision aid, not objective truth. Sensitivity and dominated/near-equivalent alternatives must not be hidden.

### 6.7 V&V Matrix

Separate verification and validation:

- **Verification:** did the defined system/configuration satisfy specified requirements?
- **Validation:** does the realized/representative system satisfy stakeholder needs and intended use in the relevant context?

For every material item preserve exact configuration, level, method, procedure, environment, equipment/model, acceptance criterion, result, deviation and evidence ref.

---

## 7｜SE-BASIS — System / Lifecycle / Tailoring Basis

**Professional question:** What is the system-of-interest, why does it exist, which lifecycle/configuration is being engineered, and what process/authority boundary applies?

Resolve:

- SoI / system level;
- lifecycle purpose and intended operation;
- stakeholder/mission context;
- system boundary and external/enabling systems;
- project/acquisition/supply context;
- applicable process tailoring;
- technical authority;
- regulated/safety/security triggers;
- brownfield/legacy/configuration constraints;
- current open evidence/authority gaps.

**Native outputs:** System Basis / Tailoring / Responsibility Matrix; SoI context/boundary model; initial lifecycle and technical-management plan; open-risk/authority register.

**Exit:** system and authority boundary are explicit enough to develop stakeholder needs without silently widening the claim.

**Does not prove:** requirements completeness, architecture, feasibility or system acceptance.

---

## 8｜SE-NEEDS — Stakeholder Needs / Intended Use / Measures

**Professional question:** What do stakeholders and affected actors need the system to achieve, under which use/mission conditions, and how will success be recognized?

Develop:

- stakeholder classes and decision roles;
- mission/use cases and scenarios;
- operational states/modes;
- desired outcomes / measures of effectiveness;
- constraints and prohibitions;
- high-consequence failure concerns;
- lifecycle/support needs;
- conflicting stakeholder needs;
- assumptions and unresolved context.

**Native outputs:** stakeholder needs/concepts of operation or equivalent use-context evidence; measure basis; conflict/trade-off register.

**Does not prove:** correct system requirements or selected architecture.

---

## 9｜SE-REQ — System Requirements / Traceability

**Professional question:** What verifiable system requirements correctly translate authorized needs and constraints for the declared system/configuration?

Develop requirements that are, where applicable:

- necessary and traceable;
- implementation-neutral at the appropriate level;
- unambiguous enough to verify;
- bounded by units/tolerances/conditions;
- uniquely identifiable;
- feasible within current evidence;
- allocated only after justified architecture decisions;
- linked to verification method/level;
- change-controlled.

Use ISO/IEC/IEEE 29148:2018 as the current published requirements-engineering reference where applicable; its 2026 DIS successor is a **draft under development**, not current replacement authority.

**Native outputs:** System Requirement / Traceability Register; requirement baseline candidate; acceptance-method map; conflicts/open items.

**Does not prove:** system architecture, element design or verified compliance.

---

## 10｜SE-ARCH — System Architecture / Decomposition / Allocation

**Professional question:** What arrangement of system elements, functions, behaviours and interfaces can satisfy the current system requirements with acceptable lifecycle consequences?

Develop competing architecture alternatives where material. Resolve:

- functional/behavioural decomposition;
- logical/physical/system-element structure;
- states/modes;
- requirement allocation;
- interface architecture;
- performance/resource budgets;
- fault/redundancy strategy where triggered;
- make/buy/reuse/COTS/legacy consequences;
- human-system/software/physical allocations;
- lifecycle/support implications;
- assumptions/uncertainty.

**Native outputs:** system architecture model/views; allocation register; interface set; architecture decision record; updated requirement traces.

`MBSE MODEL EXISTS ≠ ARCHITECTURE FIT`.

**Does not prove:** realized element performance or integrated system behaviour.

---

## 11｜SE-TRADE — Decision Analysis / Risk / Technical Planning

**Professional question:** Which system-level decisions are sufficiently evidenced, and what uncertainty/risk remains before commitment?

Apply decision analysis where consequences warrant it:

- alternatives and feasibility boundaries;
- criteria and authority;
- quantitative/qualitative evidence;
- uncertainty and sensitivity;
- risks/opportunities;
- lifecycle cost/schedule/resource implications where in scope;
- technical performance measures;
- assumptions and triggers.

Trade studies support decisions; they do not replace accountable human/technical authority.

**Native outputs:** Technical Decision / Trade Study Register; risk/uncertainty log; decision records; updated plans/budgets.

---

## 12｜SE-REALIZE — Element Realization / Acquisition / Supply Coordination

**Professional question:** Are system elements being realized/acquired/supplied against controlled requirements, interfaces and configuration assumptions?

Coordinate, without absorbing each element owner's professional authority:

- allocated requirements;
- supplier/element specifications;
- make/buy/reuse decisions;
- COTS/legacy identity and limits;
- element verification evidence;
- deviations/waivers;
- interface implementation evidence;
- configuration status;
- readiness for system integration.

**Native outputs:** element evidence/readiness register; supplier/deviation records; integration prerequisites; configuration baseline candidate.

`ELEMENT OWNER PASS ≠ SYSTEM PASS`.

---

## 13｜SE-INTEGRATE — System Integration / Configuration Realization

**Professional question:** Can the controlled system elements be assembled/configured into the intended system increment without unresolved critical interface contradictions?

Plan and read back:

- integration sequence;
- exact element/software/data/configuration identities;
- enabling systems/test environment;
- interface preconditions;
- build/assembly/deployment steps;
- observed interface behaviour;
- integration defects/anomalies;
- rollback/recovery where material;
- resulting system configuration identity.

**Boundary with R-F:** Systems Engineering owns its domain-native integration planning/artifacts and system assembly reasoning. OLEANDER R-F remains authoritative for cross-disciplinary interface maturity/disposition and acceptance propagation.

`SE INTEGRATION ACTIVITY ≠ R-F INTEGRATION PASS`.

---

## 14｜SE-VERIFY — System Verification

**Professional question:** Does the exact controlled system/configuration satisfy the specified system requirements at the appropriate verification level?

Use one or more justified methods such as inspection, analysis, demonstration and test. For each result bind:

- requirement ID/revision;
- system/configuration/element level;
- method and procedure;
- environment/input conditions;
- measurement/model/tool identity;
- acceptance criterion;
- actual result;
- anomaly/deviation;
- evidence artifact;
- reviewer/authority where triggered.

**Native outputs:** verification matrix/report; nonconformance/deviation register; requirement disposition/readback.

`VERIFIED AGAINST REQUIREMENT ≠ VALIDATED FOR INTENDED USE`.

---

## 15｜SE-VALIDATE — System Validation

**Professional question:** Does the realized or representative system satisfy stakeholder needs and intended use in the relevant operational context?

Validation may require:

- representative operational scenarios;
- representative users/operators;
- realistic environment/load/data;
- mission/use effectiveness measures;
- human-system interaction evidence;
- failure/degraded modes;
- pilot/field/operational evaluation where material;
- unresolved transfer boundary when full operational conditions are unavailable.

**Native outputs:** validation plan/report; stakeholder-need disposition; operational limitation; retest/reopen requirements.

`SIMULATION VALIDATION ≠ FIELD VALIDATION UNLESS CLAIM BOUNDARY SAYS SO`.

**Does not prove:** statutory approval, all future configurations or every operational environment.

---

## 16｜SE-TRANSITION — Transition / Deployment / Handover

**Professional question:** Can the verified/validated system increment be transferred into its intended operational/support environment without losing controlled configuration, capability or evidence?

Resolve as applicable:

- deployment/install/configuration;
- site/environment readiness;
- data migration;
- operator/maintainer training;
- documentation and support assets;
- spares/logistics;
- operational acceptance criteria;
- known limitations/waivers;
- rollback/contingency;
- as-deployed configuration identity.

Transition evidence is not automatically release authority or statutory acceptance.

---

## 17｜SE-INUSE — Operation / Support / Change / Retirement

**Professional question:** What does actual system use reveal about requirements, architecture, interfaces, support assumptions and lifecycle decisions?

Read back where available:

- operational performance;
- incidents/anomalies;
- reliability/availability/maintainability evidence;
- support demand;
- configuration changes;
- obsolescence/supplier changes;
- cyber/safety/environment changes;
- operator/user feedback;
- mission/use changes;
- retirement/disposal consequences.

Material evidence may reopen affected system conclusions immediately. Reusable learning is separately routed through G9/Knowledge/Evolution owners.

`INCIDENT ≠ UNIVERSAL CAUSAL RULE`.

---

## 18｜Cross-disciplinary interfaces

Systems Engineering can be triggered across many professional domains, but it does not become their super-authority. Material interfaces may include:

- Product / Business / Client authority;
- Architecture / Spatial Design;
- Structural / MEP / Civil / industrial engineering;
- Software / data / cloud / embedded systems;
- Digital Product / HCD / Human Factors;
- Safety / Reliability / Security / Cybersecurity;
- Manufacturing / Supply / Procurement;
- Test / Commissioning / Quality;
- Operations / Maintenance / Support;
- Statutory / Licensed professional authorities.

Each domain retains its native professional process and claim ceiling. Systems Engineering manages system-level traceability, architecture and evidence relations within scope; R-F manages OLEANDER cross-disciplinary interface truth.

---

## 19｜Configuration / change discipline

Every consequential SE claim is configuration-bound. At minimum resolve:

`SOI ID → CONFIGURATION / BASELINE → REQUIREMENTS REV → ARCHITECTURE REV → ELEMENT REVS → INTERFACE REVS → V&V EVIDENCE → DECISION / ACCEPTANCE SCOPE`.

Changes reopen by relation, not chronology:

- changed stakeholder need may reopen requirements and downstream architecture/V&V;
- changed requirement reopens affected allocations/elements/interfaces/V&V;
- changed architecture reopens affected allocations/interfaces/integration/V&V;
- changed element/configuration reopens affected interface/integration/verification/validation evidence;
- unrelated file/timestamp changes do not globally invalidate the system.

Historical evidence remains immutable under the configuration it actually verified/validated.

---

## 20｜Model / simulation / digital engineering boundary

Models can be authoritative engineering work products only within explicit model scope, configuration, assumptions and validation.

Record for consequential models:

- model purpose;
- represented system/configuration;
- fidelity/abstraction;
- assumptions and input data;
- solver/tool/version;
- calibration/verification/validation status;
- sensitivity/uncertainty;
- output claim ceiling.

`MODEL RUN SUCCESS ≠ MODEL VALIDITY`.

`MODEL VALIDITY FOR CLAIM A ≠ CLAIM B`.

---

## 21｜AI collaboration boundary

AI may assist with:

- requirement quality checks and traceability proposals;
- architecture alternative generation;
- interface inventory/checks;
- trade-study structuring;
- model/code/test assistance;
- anomaly clustering;
- evidence retrieval/synthesis;
- change-impact analysis.

AI may not:

- invent stakeholder needs or measured system evidence;
- self-award requirement/architecture/V&V acceptance;
- convert a model prediction into field truth;
- infer interface closure from document presence;
- act as an independent professional reviewer merely because a different model/session is used;
- promote one project lesson into reusable systems knowledge through prose.

---

## 22｜Professional completion / readback

A Systems Engineering process claim may close only within declared SoI/configuration/scope when:

1. system/lifecycle/authority boundary is explicit;
2. stakeholder needs and consequential requirements are traceable/current;
3. system architecture/allocation and material interfaces are controlled;
4. key technical decisions preserve evidence/uncertainty;
5. exact configuration is identifiable;
6. required element evidence and integration prerequisites are resolved;
7. verification evidence closes the specified requirement claims being asserted;
8. validation evidence closes the intended-use/stakeholder claims being asserted;
9. critical cross-domain interfaces have required R-F maturity/disposition;
10. transition/in-use limitations remain inside the claim ceiling;
11. required independent/specialist/statutory review is complete where triggered;
12. actual readback and does-not-prove boundaries are retained.

Hard separation:

```text
SYSTEMS ENGINEERING PROCESS PASS ≠ ELEMENT PROFESSIONAL PASS
SYSTEMS ENGINEERING PROCESS PASS ≠ R-F INTEGRATION PASS
SYSTEMS ENGINEERING PROCESS PASS ≠ DESIGN KEEP
SYSTEMS ENGINEERING PROCESS PASS ≠ SAFETY / SECURITY / STATUTORY APPROVAL
SYSTEMS ENGINEERING PROCESS PASS ≠ RELEASE AUTHORITY
SYSTEMS ENGINEERING PROCESS PASS ≠ PROJECT PROMOTION
```

---

## 23｜G9 / lifecycle return

Operational evidence can reopen the affected system conclusion immediately. Reusable process/domain learning remains a separate candidate route:

`ACTUAL SYSTEM OUTCOME → PROJECT/SYSTEM REOPEN WHEN NEEDED`  
`ACTUAL SYSTEM OUTCOME → BOUNDED G9 LESSON CANDIDATE → EXISTING KNOWLEDGE OWNER / EVOLUTION ROUTE`.

Observation, repeated failure or a successful repair does not itself prove causation or universal transferability.
