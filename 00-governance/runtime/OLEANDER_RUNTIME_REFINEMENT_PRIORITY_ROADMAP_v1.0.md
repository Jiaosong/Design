# OLEANDER Runtime Refinement Priority Roadmap v1.0

Status: **DRAFT GOVERNANCE EXTENSION / ORDER-OF-WORK ONLY / P1–P11 FIRST-PASS CONTRACTS DRAFTED**. This roadmap does not replace Current Authority, Project Axis, Knowledge Architecture, the Object Plane contract, or any existing gate. It defines the order in which the typed runtime system is deepened so that high-consequence control semantics are stabilized before lower-consequence presentation detail.

## 1. Ordering principle

Refine in the order of **error propagation consequence**, not visual prominence or object count.

A layer ranks earlier when an error in that layer can silently invalidate many downstream objects, create false Current state, or allow overclaim.

Priority rule:

`AUTHORITY / SCOPE ERROR > PROJECT-TRUTH ERROR > CROSS-DISCIPLINE COORDINATION ERROR > CHANGE / STALENESS ERROR > EVIDENCE / ASSURANCE ERROR > CONTENT / KNOWLEDGE ERROR > PRESENTATION ERROR`.

This is not a statement that presentation is unimportant. It means a presentation defect normally cannot be allowed to repair or redefine a wrong upstream project truth.

## 2. Priority sequence and draft status

### P0 — Object Plane + identity routing — DRAFTED

Questions:
- Is the record `KNOWLEDGE`, `PROJECT`, or `RUNTIME_CONTROL`?
- What stable logical object is being acted on?
- Is this the existing Current object or an accidental parallel object?

Primary contracts:
- `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0`
- Anti-Pollution / stable identity rules.

Exit condition:
- plane and identity can be resolved before downstream classification.

### P1 — Authority / Invocation / Precedence / Staleness / Claim Ceiling / Promotion — FIRST-PASS DRAFTED

Why first:
- every later packet, requirement, interface, evidence object, review and presentation depends on a valid authority scope;
- stale authority or an excessive claim ceiling can make otherwise correct work false at system level.

Outputs drafted:
- `OLEANDER_AUTHORITY_INVOCATION_STALENESS_CLAIM_PROMOTION_CONTRACT_v1.0.md/.json`;
- authority source classes and conflict algorithm;
- authority snapshot + invocation envelope;
- mutation classes + RB0–RB4;
- vector-valued claim ceilings;
- promotion/reopen validators.

### P2 — Project State + Decision Question + Execution Scope — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_PROJECT_STATE_DECISION_SCOPE_CONTRACT_v1.0.md/.json`;
- Project State and Workstream Runtime Card;
- Runtime Decision Object;
- Decision Question quality gate;
- locked/open/protected distinction;
- mutation budget, stop/close/reopen/concurrency rules.

### P3 — Need / Requirement / Constraint / Project Claim — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_NEED_REQUIREMENT_CONSTRAINT_CLAIM_CONTRACT_v1.0.md/.json`;
- independent semantics/state machines;
- Requirement atomicity and verification route;
- Requirement Validation vs Verification vs Product Validation;
- constraint/waiver boundary;
- project Claim–Evidence/ceiling rules.

### P4 — Controlled Variable / Interface / Material Dependency — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_CONTROLLED_VARIABLE_INTERFACE_DEPENDENCY_CONTRACT_v1.0.md/.json`;
- variable authority/consumer sensitivity;
- interface objectification, coupling, criticality, maturity/disposition;
- Acceptance Contract;
- N-way interface handling;
- Material Dependency vs Interface threshold;
- register and propagation rules.

### P5 — Baseline / Change / Staleness Propagation — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_BASELINE_CHANGE_STALENESS_PROPAGATION_CONTRACT_v1.0.md/.json`;
- immutable scoped baselines;
- Change lifecycle/impact classes;
- orthogonal validity disposition;
- typed propagation + stop proof;
- reassurance obligations;
- promotion-breaking/concurrency/cross-platform-pointer rules.

### P6 — Evidence / Formal Assurance / Claim Ceiling — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_EVIDENCE_FORMAL_ASSURANCE_CONTRACT_v1.0.md/.json`;
- Evidence Record / Assurance Activity / Assurance Decision separation;
- Verification / Validation / Certification / Independent Review / Audit / Acceptance semantics;
- applicability/uncertainty/freshness/contradiction;
- per-target results;
- field/simulation/prototype boundaries.

### P7 — Risk / Issue / Assumption / Unknown — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_RISK_ISSUE_ASSUMPTION_UNKNOWN_CONTRACT_v1.0.md/.json`;
- four independent semantic classes/state machines;
- risk treatments/residual risk;
- issue root-cause/retest/anti-repeat;
- assumption authority/expiry/claim ceiling;
- Unknown non-conversion rule;
- lineage conversions and promotion constraints.

### P8 — Work / Artifact / Information Carrier — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_WORK_ARTIFACT_INFORMATION_CARRIER_CONTRACT_v1.0.md/.json`;
- Work Package / Task / Artifact separation;
- carrier roles;
- editable master/source/derivative distinction;
- loss profile;
- cross-software handoff/readback;
- artifact authority boundaries.

### P9 — Knowledge Distillation + Classification + Content Gates — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_G9_KNOWLEDGE_DISTILLATION_ADMISSION_CONTRACT_v1.0.md/.json`;
- G9 candidate lifecycle;
- existing-owner-first;
- de-project/provenance separation;
- transfer statement + counterexample gate;
- eight-axis Knowledge classification;
- Human Knowledge Body vs Runtime Metadata;
- Claim-level evidence + R1/R2/K1–K5/B1/IR promotion.

### P10 — Presentation Projection / Style / Technique — FIRST-PASS DRAFTED

Existing presentation contracts:
- `OLEANDER_PROJECT_PRESENTATION_LAYER_v1.0.md/.json`;
- `OLEANDER_PRESENTATION_STYLE_TECHNIQUE_SYSTEM_v1.0.md/.json`.

Additional matrices drafted:
- `OLEANDER_PRESENTATION_COMPATIBILITY_MATRICES_v1.0.md/.json`;
- Style × Technique Family matrix;
- Style × Medium matrix;
- Technique × Evidence Truth-Risk matrix;
- E0–E3 transformation boundaries;
- medium-specific readbacks;
- accessibility/bilingual/static/reduced-motion rules.

### P11 — Retrieval / Reader / Automation / Routing Optimization — FIRST-PASS DRAFTED

Outputs drafted:
- `OLEANDER_RETRIEVAL_READER_ROUTING_CONTRACT_v1.0.md/.json`;
- plane-aware retrieval;
- typed relation expansion;
- separated Reader state columns;
- dynamic corpus contract;
- Claim-first retrieval;
- Project-vs-Knowledge query precedence;
- minimum sufficient execution owner routing;
- automation limits/fail-closed behavior;
- return-to-source/contradiction/staleness visibility;
- regression scenarios.

## 3. Completion discipline

For each priority item, use the same closure sequence:

`READ CURRENT → IDENTIFY EXISTING OWNER → DEFINE SEMANTIC GAP → WRITE HUMAN CONTRACT → WRITE MACHINE CONTRACT → DEFINE VALIDATOR RULES → TEST EDGE CASES → READBACK → KEEP AS DRAFT UNTIL AUTHORITY PROMOTION`.

A first-pass contract is **not** Current promotion. The first pass is sufficient only to begin cross-contract consistency review and real-project replay. Each item can still receive REVISE after replay or contradiction testing.

## 4. Next refinement stage

P1–P11 first-pass human + machine contracts are now drafted on the feature branch. The next work should be **cross-contract integration rather than adding more taxonomy**:

1. run cross-file consistency and enum/reference audit;
2. compile validator rules into one validator/eval manifest;
3. replay representative real projects against the contracts;
4. repair contradictions/over-modeling revealed by replay;
5. independently review governance and migration impact;
6. only then propose Current Authority / Notion / main promotion.

No draft contract in this branch is Current merely because it exists or is internally detailed.
