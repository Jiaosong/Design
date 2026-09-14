# OLEANDER Project Semantic Matrix — Object Plane Binding v1.0

Status: **DRAFT COMPATIBILITY BINDING / REFINED CONTRACT PRECEDENCE ADDED**.

This binding resolves terminology and precedence in the existing draft files:

- `OLEANDER_COMPLEX_PROJECT_RUNTIME_CLASSIFICATION_DETAIL_FRAMEWORK_v1.0.*`;
- `OLEANDER_RUNTIME_OBJECT_RELATION_ALLOWED_MATRIX_v1.0.md`;
- `OLEANDER_RUNTIME_OBJECT_STATE_ALLOWED_MATRIX_v1.0.md`;
- `OLEANDER_RUNTIME_PROMOTION_CLOSURE_MATRIX_v1.0.md`;
- `OLEANDER_RUNTIME_CLASSIFICATION_MATRICES_v1.0.json`.

## 1. Object Plane binding

The atomic classes governed by those matrices — Requirement, Constraint, System Element, Controlled Variable, Interface, Decision, Risk, Issue, Assumption, Unknown, Artifact, Evidence, Assurance, Baseline, Change, etc. — are interpreted as **Project-plane semantic objects** unless a row is explicitly a runtime-control record.

Therefore:

`Object Plane = PROJECT` is the default plane for those matrix rows.

The files retain their historical draft filenames to avoid unnecessary lineage churn, but the phrase `runtime object` in them means **project object participating in the runtime**, not `RUNTIME_CONTROL` Object Plane.

## 2. Refined-contract precedence

The first-pass Object×Relation / Object×State / Promotion matrices are **core compatibility matrices**. They retain broad class/relation/cardinality structure and are useful for validator compilation, but they are no longer the sole normative draft source for class-specific fields/state semantics after the P1–P11 refinement pass.

When a refined per-class contract exists, use this precedence:

`OBJECT PLANE / IDENTITY → REFINED PER-CLASS CONTRACT → CORE MATRIX COMPATIBILITY RULE → LEGACY EARLY STATE SNAPSHOT`.

If a refined contract adds a legitimate state, field, boundary or validator that is absent from the earlier core matrix, the refined contract governs. The difference is a **draft integration delta**, not an error in the refined contract.

If the core matrix and refined contract directly contradict each other semantically, mark `CROSS_CONTRACT_CONFLICT` and resolve before promotion. Do not silently choose whichever file is newer.

## 3. Refined Project-contract owners

### Purpose / obligation
`OLEANDER_NEED_REQUIREMENT_CONSTRAINT_CLAIM_CONTRACT_v1.0.md/.json`

Owns detailed Need / Requirement / Constraint / Project Claim state, quality, trace and verification semantics.

### Cross-disciplinary coupling
`OLEANDER_CONTROLLED_VARIABLE_INTERFACE_DEPENDENCY_CONTRACT_v1.0.md/.json`

Owns Controlled Variable / Interface / Material Dependency detail, including N-way interfaces and Acceptance Contract.

### Configuration / change
`OLEANDER_BASELINE_CHANGE_STALENESS_PROPAGATION_CONTRACT_v1.0.md/.json`

Owns Baseline / Change state, orthogonal validity disposition, propagation and reassurance rules.

### Evidence / assurance
`OLEANDER_EVIDENCE_FORMAL_ASSURANCE_CONTRACT_v1.0.md/.json`

Owns Evidence Record / Assurance Activity / Assurance Decision semantics, including Verification/Validation/Certification boundaries.

### Uncertainty / problem
`OLEANDER_RISK_ISSUE_ASSUMPTION_UNKNOWN_CONTRACT_v1.0.md/.json`

Owns Risk / Issue / Assumption / Unknown states, transitions, conversion lineage and promotion effect.

### Work / carrier
`OLEANDER_WORK_ARTIFACT_INFORMATION_CARRIER_CONTRACT_v1.0.md/.json`

Owns Work Package / Task / Artifact carrier roles, master/derivative/loss/handoff semantics.

## 4. Runtime-control separation

Packets, registers, receipts, gate state, authority/knowledge snapshots, readback receipts and promotion-state controls are governed by:

- `OLEANDER_RUNTIME_CONTROL_OBJECT_CONTRACT_v1.0.md`;
- `OLEANDER_AUTHORITY_INVOCATION_STALENESS_CLAIM_PROMOTION_CONTRACT_v1.0.md/.json`;
- `OLEANDER_PROJECT_STATE_DECISION_SCOPE_CONTRACT_v1.0.md/.json`;
- `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0.*`.

Do not add packet/register/receipt types into the Project semantic Object × State matrix merely because they are operational.

## 5. Knowledge separation

Reusable Knowledge is governed by:

- `OLEANDER_KNOWLEDGE_CLASSIFICATION_CONTRACT_v1.1_DRAFT.md`;
- `OLEANDER_G9_KNOWLEDGE_DISTILLATION_ADMISSION_CONTRACT_v1.0.md/.json`;
- Current Professional Knowledge Content & Research Standard v1.0.

Project state/dependency/staleness semantics must not be reused as Knowledge taxonomy/dependency semantics.

## 6. Presentation separation

Presentation objects remain an orthogonal projection layer governed by:

- `OLEANDER_PROJECT_PRESENTATION_LAYER_v1.0.*`;
- `OLEANDER_PRESENTATION_STYLE_TECHNIQUE_SYSTEM_v1.0.*`;
- `OLEANDER_PRESENTATION_COMPATIBILITY_MATRICES_v1.0.md/.json`.

They are not a fourth Object Plane and must preserve the plane/classification and claim ceiling of their upstream source objects.

## 7. Retrieval / routing binding

Reader and automation behavior is governed by:

- `OLEANDER_RETRIEVAL_READER_ROUTING_CONTRACT_v1.0.md/.json`.

It must resolve plane and refined owner before applying generic matrix/state logic.

## 8. Validator interpretation

Any validator compiled from the existing matrices should:

1. resolve `object_plane`;
2. resolve exact object class/control type/projection type;
3. load the applicable refined contract when one exists;
4. apply core relation/cardinality matrix as compatibility floor;
5. apply class-specific state/field/promotion rules from the refined owner;
6. report `CROSS_CONTRACT_CONFLICT` when two active draft contracts genuinely contradict rather than silently choosing by timestamp;
7. if `RUNTIME_CONTROL`, apply Runtime Control/P1/P2 contracts instead of Project class states;
8. if `KNOWLEDGE`, route to Knowledge/G9 contracts;
9. apply Presentation checks orthogonally to projection/release records.

This binding supersedes any interpretation that all existing matrix classes are members of the `RUNTIME_CONTROL` plane or that the early state snapshot can override later class-specific refinement.