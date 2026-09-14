# OLEANDER Runtime Refinement Priority Roadmap v1.0

Status: **DRAFT GOVERNANCE EXTENSION / ORDER-OF-WORK ONLY**. This roadmap does not replace Current Authority, Project Axis, Knowledge Architecture, the Object Plane contract, or any existing gate. It defines the order in which the new typed runtime system should be deepened so that high-consequence control semantics are stabilized before lower-consequence presentation detail.

## 1. Ordering principle

Refine in the order of **error propagation consequence**, not visual prominence or object count.

A layer ranks earlier when an error in that layer can silently invalidate many downstream objects, create false Current state, or allow overclaim.

Priority rule:

`AUTHORITY / SCOPE ERROR > PROJECT-TRUTH ERROR > CROSS-DISCIPLINE COORDINATION ERROR > CHANGE / STALENESS ERROR > EVIDENCE / ASSURANCE ERROR > CONTENT / KNOWLEDGE ERROR > PRESENTATION ERROR`.

This is not a statement that presentation is unimportant. It means a presentation defect normally cannot be allowed to repair or redefine a wrong upstream project truth.

## 2. Priority sequence

### P0 — Object Plane + identity routing — ALREADY DRAFTED

Questions:
- Is the record `KNOWLEDGE`, `PROJECT`, or `RUNTIME_CONTROL`?
- What stable logical object is being acted on?
- Is this the existing Current object or an accidental parallel object?

Primary contracts:
- `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0`
- Anti-Pollution / stable identity rules.

Exit condition:
- plane and identity can be resolved before downstream classification.

### P1 — Authority / Invocation / Precedence / Staleness / Claim Ceiling / Promotion — FIRST TO DEEPEN

Why first:
- every later packet, requirement, interface, evidence object, review and presentation depends on a valid authority scope;
- stale authority or an excessive claim ceiling can make otherwise correct work false at system level.

Required outputs:
- authority source classes;
- precedence algorithm;
- authority snapshot contract;
- invocation envelope;
- stale triggers and propagation;
- independent claim-ceiling dimensions;
- promotion/reopen rules;
- machine validator rules.

### P2 — Project State + Decision Question + Execution Scope

Questions:
- What project/workstream/decision is active?
- What is locked, open, outside claim and forbidden to change?
- What constitutes material completion for this loop?

Required outputs:
- Project State contract;
- Decision Object control envelope;
- scope lock / mutation budget;
- stop and reopen conditions.

### P3 — Need / Requirement / Constraint / Project Claim

Why before geometry or artifacts:
- design objects should not become the hidden source of requirements;
- Verification requires a traceable requirement target;
- claims need explicit evidence ceilings.

Required outputs:
- requirement atomicity;
- requirement provenance;
- acceptance criteria;
- requirement-validation vs product-validation boundary;
- constraint authority and waiver logic;
- project-claim trace contract.

### P4 — Controlled Variable / Interface / Material Dependency

Why high priority:
- this is the main cross-disciplinary propagation layer;
- one wrong shared variable can invalidate multiple disciplines while each local artifact remains internally correct.

Required outputs:
- variable authority and consumer registry;
- interface objectification threshold;
- interface acceptance contract;
- coupling/criticality rules;
- integrated readback;
- N-way interface handling.

### P5 — Baseline / Change / Staleness Propagation

Questions:
- what configuration is Current?
- what does a change invalidate or reopen?
- when is previous evidence historical rather than Current?

Required outputs:
- immutable baseline contract;
- change-impact graph;
- stale propagation engine;
- local/material/coupled/promotion-breaking change rules;
- downstream reassurance obligations.

### P6 — Evidence / Assurance / Claim Ceiling

Questions:
- what was actually observed or tested?
- what was Verification versus Validation?
- what conclusion does the evidence not establish?

Required outputs:
- evidence-record contract;
- assurance activity/decision split;
- result-per-target semantics;
- contradiction handling;
- field/simulation/prototype separation;
- claim-ceiling binding.

### P7 — Risk / Issue / Assumption / Unknown

Required outputs:
- class-specific state machines;
- trigger/expiry rules;
- consequence-if-false;
- residual risk;
- assumption confirmation/refutation;
- unknown resolution and `OUTSIDE_CLAIM` rules.

### P8 — Work / Artifact / Information Carrier

Questions:
- what work remains?
- what carrier represents which semantic object?
- what can be replaced without changing truth?

Required outputs:
- Work Package / Task contracts;
- artifact carrier semantics;
- editable-master / derivative distinction;
- source-to-derivative relation;
- information-loss/readback contract.

### P9 — Knowledge Distillation + Classification + Content Gates

Questions:
- what project/runtime learning is genuinely reusable?
- what remains project-specific?
- what belongs in L0–L7 and with which Role/relations?

Required outputs:
- G9 admission contract;
- deproject/generalize rules;
- Claim–Evidence migration;
- eight-axis classification;
- Human Knowledge Body vs Runtime Metadata separation;
- R1/R2/K1–K5/B1/IR execution.

### P10 — Presentation Projection / Style / Technique

Questions:
- how should valid source truth be communicated to a given audience/medium/context?
- which style axes and techniques solve the communication problem?
- what truth risk does each presentation transformation introduce?

Required outputs:
- presentation runtime objects;
- style-profile axes;
- technique library;
- Style × Technique compatibility;
- Medium × Style adaptation;
- Technique × Evidence-risk matrix;
- presentation release/readback.

### P11 — Retrieval / Reader / Automation / Routing Optimization

Do last because UI/routing must reflect the stabilized semantic model rather than force the model to fit an early interface.

Required outputs:
- Reader information architecture;
- plane-aware search/filter;
- typed graph traversal;
- minimum sufficient runtime routing;
- automated validators and regression tests.

## 3. Completion discipline

For each priority item, use the same closure sequence:

`READ CURRENT → IDENTIFY EXISTING OWNER → DEFINE SEMANTIC GAP → WRITE HUMAN CONTRACT → WRITE MACHINE CONTRACT → DEFINE VALIDATOR RULES → TEST EDGE CASES → READBACK → KEEP AS DRAFT UNTIL AUTHORITY PROMOTION`.

Do not start a lower-priority item merely because the higher-priority document exists. A priority item is sufficiently refined only when its core conflicts, state transitions, relation cardinalities, failure modes and machine-readable invariants are explicit.

## 4. Current next action

`P1 Authority / Invocation / Precedence / Staleness / Claim Ceiling / Promotion` is the active refinement target.
