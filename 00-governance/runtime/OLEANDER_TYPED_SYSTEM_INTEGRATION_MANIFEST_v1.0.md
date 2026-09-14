# OLEANDER Typed System Integration Manifest v1.0

Status: **DRAFT INTEGRATION MANIFEST / POST P1–P11 FIRST PASS**. This file does not promote any draft contract. It defines which draft owns which semantic responsibility and how cross-contract conflicts must be handled before any Current promotion.

## 1. Integration principle

`ONE SEMANTIC RESPONSIBILITY → ONE DRAFT OWNER → EXPLICIT COMPATIBILITY BINDINGS → NO TIMESTAMP-BASED WINNER`.

The P1–P11 refinement created more precise class-specific contracts than the early broad matrices. This is expected. The system must now integrate them without creating parallel authority.

## 2. Draft owner map

| Responsibility | Draft owner |
|---|---|
| Object Plane / top-level separation | `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0.*` |
| Project semantic class baseline | `OLEANDER_COMPLEX_PROJECT_RUNTIME_CLASSIFICATION_DETAIL_FRAMEWORK_v1.0.*` |
| Core relation/state/promotion compatibility | `OLEANDER_RUNTIME_*_MATRIX*` + `OLEANDER_RUNTIME_CLASSIFICATION_MATRICES_v1.0.json` |
| Matrix plane/precedence binding | `OLEANDER_PROJECT_SEMANTIC_MATRIX_PLANE_BINDING_v1.0.md` |
| Runtime Control family/envelope | `OLEANDER_RUNTIME_CONTROL_OBJECT_CONTRACT_v1.0.md` |
| P1 authority/invocation/staleness/claim/promotion | `OLEANDER_AUTHORITY_INVOCATION_STALENESS_CLAIM_PROMOTION_CONTRACT_v1.0.*` |
| P2 Project State/Decision Scope | `OLEANDER_PROJECT_STATE_DECISION_SCOPE_CONTRACT_v1.0.*` |
| P3 Need/Requirement/Constraint/Claim | `OLEANDER_NEED_REQUIREMENT_CONSTRAINT_CLAIM_CONTRACT_v1.0.*` |
| P4 Variable/Interface/Dependency | `OLEANDER_CONTROLLED_VARIABLE_INTERFACE_DEPENDENCY_CONTRACT_v1.0.*` |
| P5 Baseline/Change/Staleness propagation | `OLEANDER_BASELINE_CHANGE_STALENESS_PROPAGATION_CONTRACT_v1.0.*` |
| P6 Evidence/Formal Assurance | `OLEANDER_EVIDENCE_FORMAL_ASSURANCE_CONTRACT_v1.0.*` |
| P7 Risk/Issue/Assumption/Unknown | `OLEANDER_RISK_ISSUE_ASSUMPTION_UNKNOWN_CONTRACT_v1.0.*` |
| P8 Work/Artifact/Carrier | `OLEANDER_WORK_ARTIFACT_INFORMATION_CARRIER_CONTRACT_v1.0.*` |
| Knowledge eight-axis classification | `OLEANDER_KNOWLEDGE_CLASSIFICATION_CONTRACT_v1.1_DRAFT.md` |
| P9 G9 distillation/admission | `OLEANDER_G9_KNOWLEDGE_DISTILLATION_ADMISSION_CONTRACT_v1.0.*` |
| Presentation objects | `OLEANDER_PROJECT_PRESENTATION_LAYER_v1.0.*` |
| Style/technique ontology | `OLEANDER_PRESENTATION_STYLE_TECHNIQUE_SYSTEM_v1.0.*` |
| P10 compatibility/truth-risk | `OLEANDER_PRESENTATION_COMPATIBILITY_MATRICES_v1.0.*` |
| P11 retrieval/reader/routing | `OLEANDER_RETRIEVAL_READER_ROUTING_CONTRACT_v1.0.*` |
| Refinement order/status | `OLEANDER_RUNTIME_REFINEMENT_PRIORITY_ROADMAP_v1.0.md` |

## 3. Contract precedence by question

Do not use one universal precedence across all semantics. Route by question.

### “What plane/type is this?”
Object Plane → Project/Knowledge/Runtime owner.

### “What relations/classes are generally legal?”
Core compatibility matrix → refined class contract.

### “What exact states/fields/closure rule apply to this class?”
Refined class contract wins over early compatibility snapshot.

### “Can this action execute?”
P1 Authority/Invocation → P2 Project State/Decision Scope → relevant class contract.

### “What changed/staled/reopens?”
P5 plus affected P3/P4/P6/P7/P8 contract.

### “What does evidence prove?”
P6 + P1 claim-ceiling vector + target P3 Claim/Requirement/Need.

### “Can project learning become reusable knowledge?”
P9 → Knowledge classification → Professional Content/Research gates.

### “How should it be shown?”
Presentation layer → P10, while upstream source/claim ceiling remains authoritative.

### “What should Reader/Agent retrieve?”
P11 after resolving upstream authority/plane/state.

## 4. Known integration deltas discovered in first pass

These are intentional refinement deltas to reconcile, not reasons to delete detail.

### DELTA-01 Need lifecycle
Early core matrix:
`CAPTURED / ANALYZED / AGREED / BASELINED / SUPERSEDED / WITHDRAWN`.

P3 refined Need contract adds:
`VALIDATED_FOR_SCOPE / REVISED`.

Resolution:
- refined P3 lifecycle is draft owner;
- early matrix remains compatibility snapshot until compiled from refined source.

### DELTA-02 Claim naming
Early core matrix uses `CLAIM`; P3 uses `PROJECT_CLAIM` to avoid confusion with Knowledge Claim/Presentation Argument.

Resolution:
- canonical Project semantic class should become `PROJECT_CLAIM` in future validator compilation;
- accept `CLAIM` as draft compatibility alias until migration/promotion decision.

### DELTA-03 P4 naming
Current Registry calls P4 `Validation`; refined contracts use logical `Formal Assurance` with explicit `assurance_type`.

Resolution:
- retain physical compatibility until migration impact is reviewed;
- semantic layer requires `assurance_type` and Verification/Validation distinction now;
- no registry rename is authorized by this draft alone.

### DELTA-04 Staleness
Some class states include `STALE`; P5 introduces orthogonal `validity_disposition` to avoid corrupting class-specific state machines.

Resolution:
- where `STALE` historically exists as a class state, treat it as compatibility state;
- new model prefers native class state + orthogonal validity disposition;
- migration requires replay before removing legacy state values.

### DELTA-05 Promotion vocabulary
Early core matrix has generic T0–T4. P1 introduces vector claim ceilings and class-specific promotion.

Resolution:
- T0–T4 remain coarse routing/status summary only;
- they cannot replace vector claim ceilings or class-specific gates.

### DELTA-06 Evidence strength vocabulary
P1 claim ceiling and P6 Evidence strength use related but distinct vocabularies.

Resolution:
- P6 owns evidence-record strength;
- P1 owns maximum claim/evidence ceiling propagated by runtime;
- do not collapse them into one enum.

## 5. Validator namespace rule

Several contracts deliberately use local rule IDs such as `REQ-001`, `PROM-001`, `REOPEN-001`. These are readable locally but collide globally.

Compiled validator IDs must namespace them:

`<CONTRACT_NAMESPACE>/<LOCAL_RULE_ID>`.

Examples:
- `P3/REQ-001`;
- `P5/PROM-001`;
- `P1/REOPEN-001`;
- `P10/TRUTH-004`.

Do not rename historical draft text solely to make rule IDs globally unique; namespace at compilation.

## 6. Shared enum ownership

Use one owner for shared semantics:

- Object Plane → P0 Object Plane contract;
- mutation class / RB0–RB4 / claim-ceiling vectors → P1;
- Design State / Loop / Decision Mode → P2;
- Requirement/Constraint/Project Claim types/states → P3;
- Interface maturity/disposition/coupling/criticality → P4;
- change impact / validity disposition → P5;
- assurance type/evidence strength/assurance dispositions → P6;
- risk/issue/assumption/unknown states → P7;
- carrier role/loss profile → P8;
- Knowledge Role/Level/Framework Type → Knowledge classification contract;
- E0–E3 presentation truth-risk → P10;
- Retrieval Space/Search Eligibility/query plane → P11.

Consumers reference these owners rather than redefining enums locally in future implementations.

## 7. Cross-contract invariants

The following must hold system-wide:

1. `Object Plane` resolved before taxonomy/runtime class routing.
2. One stable logical object cannot be replaced by a register/receipt/view identity.
3. Artifact/Presentation carrier cannot self-create semantic truth authority.
4. Latest/newest does not equal Current without valid authority/configuration.
5. Class state, validity disposition, evidence state, claim ceiling and retrieval state are independent.
6. Verification and Validation remain distinct end-to-end.
7. Change propagation follows typed material dependencies.
8. Runtime/Project success cannot bypass G9/Knowledge gates.
9. Presentation cannot raise source claim ceiling.
10. Retrieval cannot collapse status dimensions into one opaque authority score.
11. Automation cannot self-certify professional/design/research/bilingual/field truth.
12. Current counts are dynamic census snapshots, never fixed corpus ceilings.

## 8. Cross-contract audit categories

Before promotion, compile checks for:

- enum collision / divergent spelling;
- semantic duplicate object class;
- state-machine conflict;
- relation direction/cardinality conflict;
- same concept owned by two contracts;
- missing source-contract pointer;
- validator rule collision;
- forbidden inference contradiction;
- promotion/reopen mismatch;
- current Notion/GitHub contract mismatch;
- migration compatibility impact;
- real-project replay failure.

## 9. Promotion impact rule

No individual P1–P11 contract should be promoted to Current in isolation if its semantics alter a shared enum/identity/state used by another contract.

Promotion unit should normally be:

`Object Plane + Integration Manifest + affected semantic contracts + compatibility/migration plan + validators/evals + Current Authority binding/readback`.

Presentation-only extensions may be promoted separately only when they do not modify upstream project/knowledge/runtime semantics.

## 10. Current draft conclusion

P1–P11 now form a first-pass integrated typed operating-system model. The next maturity step is **validator compilation + representative project replay**, not more taxonomy or more object classes.

Until that replay occurs, retain `DRAFT GOVERNANCE EXTENSION` and do not modify main/Notion Current merely because the contract set is internally detailed.