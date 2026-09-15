# OLEANDER Typed System Second-Pass Binding v1.1

Status: **DRAFT COMPATIBILITY BINDING / POST P1–P11 SECOND PASS**.

This binding does not create new semantic owners. It binds the second-pass `v1.1` matrices to the existing `v1.0` semantic contracts and to `OLEANDER_TYPED_SYSTEM_INTEGRATION_MANIFEST_v1.0`.

## 1. Binding rule

`v1.0 SEMANTIC CONTRACT = semantic owner`

`v1.1 SECOND-PASS MATRIX = executable refinement / validator input`

When the two differ:
1. if v1.1 merely makes an implicit v1.0 rule more explicit, use v1.1 for validator compilation;
2. if v1.1 changes an enum/state/identity meaning, record an integration delta; do **not** silently override v1.0 or Current Authority;
3. Current Notion/GitHub governance remains unchanged until explicit promotion/migration/readback.

## 2. Second-pass map

| Priority | Semantic owner | Second-pass companion |
|---|---|---|
| P1 | `OLEANDER_AUTHORITY_INVOCATION_STALENESS_CLAIM_PROMOTION_CONTRACT_v1.0.*` | `OLEANDER_P1_AUTHORITY_EXECUTION_MATRICES_v1.1.*` |
| P2 | `OLEANDER_PROJECT_STATE_DECISION_SCOPE_CONTRACT_v1.0.*` | `OLEANDER_P2_PROJECT_STATE_DECISION_MATRICES_v1.1.*` |
| P3 | `OLEANDER_NEED_REQUIREMENT_CONSTRAINT_CLAIM_CONTRACT_v1.0.*` | `OLEANDER_P3_REQUIREMENT_CLAIM_MATRICES_v1.1.*` |
| P4 | `OLEANDER_CONTROLLED_VARIABLE_INTERFACE_DEPENDENCY_CONTRACT_v1.0.*` | `OLEANDER_P4_VARIABLE_INTERFACE_MATRICES_v1.1.*` |
| P5 | `OLEANDER_BASELINE_CHANGE_STALENESS_PROPAGATION_CONTRACT_v1.0.*` | `OLEANDER_P5_BASELINE_CHANGE_MATRICES_v1.1.*` |
| P6 | `OLEANDER_EVIDENCE_FORMAL_ASSURANCE_CONTRACT_v1.0.*` | `OLEANDER_P6_EVIDENCE_ASSURANCE_MATRICES_v1.1.*` |
| P7 | `OLEANDER_RISK_ISSUE_ASSUMPTION_UNKNOWN_CONTRACT_v1.0.*` | `OLEANDER_P7_UNCERTAINTY_PROBLEM_MATRICES_v1.1.*` |
| P8 | `OLEANDER_WORK_ARTIFACT_INFORMATION_CARRIER_CONTRACT_v1.0.*` | `OLEANDER_P8_WORK_ARTIFACT_MATRICES_v1.1.*` |
| P9 | `OLEANDER_G9_KNOWLEDGE_DISTILLATION_ADMISSION_CONTRACT_v1.0.*` + Knowledge Classification + Content/Research Standard | `OLEANDER_P9_KNOWLEDGE_ADMISSION_MATRICES_v1.1.*` |
| P10 | Presentation Layer + Style/Technique + Compatibility v1.0 | `OLEANDER_P10_STYLE_EXECUTION_PROFILES_v1.1.*` |
| P11 | `OLEANDER_RETRIEVAL_READER_ROUTING_CONTRACT_v1.0.*` | `OLEANDER_P11_READER_ROUTING_MATRICES_v1.1.*` |

P0 Object Plane/identity remains owned by `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0.*`; no second-pass companion is required unless validator replay exposes an unresolved plane/identity case.

## 3. Priority completion state

Second-pass specification status:

- P0 — `FOUNDATION_PRESENT / REPLAY_REQUIRED`
- P1 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P2 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P3 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P4 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P5 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P6 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P7 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P8 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P9 — `SECOND_PASS_SPEC_COMPLETE / VALIDATOR_REPLAY_REQUIRED`
- P10 — `SECOND_PASS_SPEC_COMPLETE / TARGET_CONDITION_REPLAY_REQUIRED`
- P11 — `SECOND_PASS_SPEC_COMPLETE / READER_AGENT_REPLAY_REQUIRED`

`SPEC_COMPLETE ≠ CURRENT ≠ VALIDATED`.

## 4. Second-pass semantic improvements

### P1
Property-scoped authority; conflict outcomes; Mutation×Readback; staleness routes; nine-axis Claim Ceiling; promotion authority.

### P2
Decision Question grammar; local blocker vs Project HOLD; concurrency; Locked/Open/Protected; mutation-budget escalation; decision fork/merge/lineage.

### P3
Requirement atomicity; authorized derivation; 12 baseline-admission gates; testable acceptance; conflict/waiver; four-direction trace; verification carry-forward.

### P4
Controlled Variable classes; authority/unit/tolerance/reference-system rules; interface objectification; N-way hub/pairwise modeling; closure/acceptance/change propagation.

### P5
Configuration-control threshold; scoped/variant baseline; change authority; partial invalidation; assurance carry-forward; status accounting; collision/rollback/release.

### P6
Evidence admissibility/independence/transferability/uncertainty; Assurance readiness; independence levels; per-target aggregation; contradiction and ceiling grant.

### P7
Risk statement/exposure/residual risk; Issue severity/root-cause confidence/CAPA; Assumption admission; Unknown subclasses/conversion; promotion effects.

### P8
Work acceptance; Task granularity; Source vs Editable Master; derivative loss severity; handoff readback; delivery/access/rework routing.

### P9
Existing-owner action; de-project; generalization strength; transfer/counterexample burden; L4 admission; body/runtime split; dynamic corpus closure.

### P10
Executable parameter bands for all 14 Style Profiles; technique conflicts; medium adaptation; accessibility/truth-risk; target-condition readback.

### P11
Plane-aware candidate pools; decomposed ranking; typed traversal; human vs Agent views; automation permissions; coverage records; 18 regression scenarios.

## 5. Validator compilation precedence

Compile in this order:

`P0 PLANE/IDENTITY → P1 AUTHORITY/SCOPE → P2 ACTIVE DECISION → P3 PROJECT OBLIGATIONS → P4 COUPLING → P5 CONFIG/CHANGE → P6 EVIDENCE/ASSURANCE → P7 UNCERTAINTY/ISSUES → P8 WORK/CARRIERS → P9 KNOWLEDGE ADMISSION → P10 PRESENTATION → P11 RETRIEVAL/ROUTING`.

A later validator can add a stricter condition but cannot legalize a failure in an earlier prerequisite.

Examples:
- P10 visual quality cannot legalize a P3 requirement failure;
- P11 high retrieval relevance cannot legalize a P1 authority conflict;
- P6 evidence cannot be consumed as Current if P5 says its configuration is invalid;
- P9 cannot distill a project result whose source evidence/authority is unresolved.

## 6. Rule namespace

All compiled rules use:

`P<n>/<LOCAL_RULE_ID>`

plus:
- `P0/...` for Plane/identity;
- `INT/...` for cross-contract invariants;
- `REG/...` for regression/replay-only rules.

Local historical IDs remain unchanged in human docs.

## 7. Current integration deltas still open

Carry forward from the Integration Manifest until replay/migration decision:
- `CLAIM` compatibility alias vs canonical `PROJECT_CLAIM`;
- physical Registry `P4 Validation` vs logical `P4 Formal Assurance` + `assurance_type`;
- legacy native `STALE` state vs orthogonal `validity_disposition`;
- early coarse T0–T4 promotion summary vs vector claim ceilings;
- early broad state matrix vs class-specific v1.0/v1.1 state refinements;
- evidence-record strength vs runtime propagated evidence ceiling.

No Current schema migration is authorized by this binding.

## 8. Exit condition

The typed system is not ready for Current promotion until:
1. machine rules are compiled without duplicate/contradictory ownership;
2. regression corpus passes/fails as expected;
3. representative real-project replay tests authority/change/interface/evidence paths;
4. representative Knowledge replay tests classification/body/admission;
5. Presentation/Reader target-condition replay tests P10/P11;
6. migration compatibility impact is known;
7. independent governance review resolves Critical/Major objections;
8. explicit promotion + Notion/GitHub readback occurs.
