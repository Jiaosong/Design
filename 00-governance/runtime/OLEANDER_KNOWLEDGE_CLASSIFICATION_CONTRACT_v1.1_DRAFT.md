# OLEANDER Knowledge Classification Contract v1.1 — DRAFT

Status: **DRAFT / KNOWLEDGE PLANE ONLY**. Binding candidate under `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0`. It applies only after `Object Plane = KNOWLEDGE`.

## 1. Eight-axis contract

A canonical Knowledge object is classified by eight independent axes:

`Object Plane × Subject Ownership × Knowledge Level × Primary Knowledge Role × Framework Type × Typed Knowledge Relations × Knowledge State × Information Role`.

No axis may silently substitute for another.

## 2. Axis A — Object Plane

Required value: `KNOWLEDGE`.

If the object is primarily a project fact/execution result, route to `PROJECT`.

If it is primarily a packet/register/receipt/gate/snapshot that drives or audits runtime, route to `RUNTIME_CONTROL`.

## 3. Axis B — Subject Ownership

Required fields:

- `Primary Domain`: normally exactly 1;
- `Primary Topic`: 0..1;
- `Related Domain[]`: 0..N;
- `Application Mapping[]`: 0..N.

Invariants:

- Related Domain is not a second parent;
- Application Mapping is not Domain;
- Project use is not Domain;
- cross-disciplinary relevance does not create a Cross-disciplinary Domain.

## 4. Axis C — Knowledge Level

Frozen controlled levels:

- `L0 System` — whole knowledge-system boundary;
- `L1 Branch` — stable branch spanning multiple long-term Domains;
- `L2 Domain` — professional/knowledge responsibility domain;
- `L3 Topic` — stable problem space within a Domain;
- `L4 Integrating Framework` — integration/routing structure across multiple independent L5 owners;
- `L5 Knowledge Object` — default smallest independently maintainable knowledge responsibility;
- `L6 Source / Evidence / Case` — objects whose primary responsibility is evidentiary/source/case support;
- `L7 Practice / Output` — actual bounded application/output of knowledge in work.

Default: **L5**.

Length, importance, complexity, number of steps, number of disciplines touched, or project frequency do not justify L4.

## 5. L4 admission gate

All five gates are mandatory:

- `BREADTH`: multiple independent L5 owners exist;
- `INTEGRATION`: the candidate owns cross-object selection/combination/conflict/handoff relations;
- `DELEGATION`: subordinate bodies remain in their L5 owners rather than being copied upward;
- `BOUNDARY`: scope-out and owner boundaries are explicit;
- `REUSE`: the integration structure is stable across multiple projects/contexts.

Failure of any gate defaults the object to the appropriate L5 role rather than forcing L4.

## 6. Axis D — Primary Knowledge Role

Exactly one:

`INDEX | THEORY | METHOD | TOOL | SOURCE | EVIDENCE | CASE | PRACTICE`.

Primary-role compounds are forbidden:

- `METHOD/FRAMEWORK`;
- `THEORY/SYSTEM`;
- `INDEX/METHOD`;
- `METHOD/PRACTICE`.

Secondary meaning is expressed by typed relations, Framework Type where applicable, Information Role, or Application Mapping.

## 7. Axis E — Framework Type

Applicable only when `Knowledge Level = L4` and L4 admission passes.

Controlled set:

- `NAVIGATION_MAP`;
- `CONCEPTUAL_MODEL`;
- `METHOD_FAMILY`;
- `PROCESS_ORCHESTRATION`;
- `PROFESSIONAL_SYSTEM_MAP`;
- `TYPOLOGY_FRAMEWORK`;
- `APPLICATION_FRAMEWORK`;
- `DESIGN_LANGUAGE_SYSTEM`;
- `STRATEGY_FRAMEWORK`;
- `EVALUATION_FRAMEWORK`;
- `HISTORICAL_COMPARATIVE_SYNTHESIS`.

New type admission requires documented semantic insufficiency of all existing types.

## 8. Axis F — Typed Knowledge Relations

### Structural hierarchy
`BROADER / NARROWER / PARENT / CHILD` only where genuine hierarchy exists.

### Domain placement
Primary domain/topic placement and related-domain links.

### Knowledge dependency
`REQUIRES_CONCEPT | EXTENDS | REFINES | CONTRASTS_WITH | IMPLEMENTS | CONSTRAINED_BY`.

### Evidence support
`SUPPORTS_CLAIM | CONTRADICTS_CLAIM | BOUNDS_CLAIM`.

### Application use
Knowledge-to-method/tool/practice/application bindings without pretending they are hierarchy.

### Lifecycle lineage
`SUPERSEDES | SUPERSEDED_BY | DERIVED_FROM | MIGRATED_FROM` as controlled provenance/lifecycle semantics.

`RELATED` is discovery-only. If a stronger relation is known, use the stronger relation.

Project-runtime relations such as `depends_on`, `stale_if`, shared-variable propagation and reopen propagation are forbidden in the reusable knowledge relation ontology.

## 9. Axis G — Knowledge State

Show state independently from classification:

- Authority Layer: `CURRENT | SUPPORT | PROVENANCE | EXCLUDED`;
- Governance State;
- Evidence State;
- Trust State;
- Freshness State;
- Content State;
- Research R1/R2;
- Bilingual State;
- Graph State.

Forbidden inference rules:

- `CURRENT` does not mean true/verified;
- `L4` does not mean mature;
- `VERIFIED` does not imply a higher Level;
- many project uses do not imply L4;
- Content PASS does not imply Research PASS;
- Graph CLEAN does not imply Content PASS.

## 10. Axis H — Information Role

Controlled set:

`EXPLANATION | PROCEDURE | REFERENCE | NAVIGATION | DECISION_SUPPORT | AUDIT_READBACK | CASE_NARRATIVE`.

Information Role describes the primary human-reading function of the carrier. It does not replace Knowledge Role.

## 11. Domain Admission Gate

New L2 Domain admission requires:

1. independent stable semantics;
2. multiple Topics/Knowledge Objects;
3. distinct method/validation ecology;
4. relatively distinct evidence/regulation/standard/research ecology where applicable;
5. identifiable professional ownership/review capability;
6. long-term cross-project stability;
7. non-substitutability within current Domains.

A HOLD, project type, building typology, new technology, or temporary cluster is not sufficient by itself.

## 12. Claim objectification

Claims inside a Knowledge Object should be addressable when they are consequential, reused, contradicted, independently reviewed, or require separate evidence state.

Minimum claim contract:

`claim_id, parent_object_id, claim_type, statement, scope, conditions, supports[], contradicts[], bounds[], evidence_strength, confidence, uncertainty, claim_ceiling, validation_state`.

A claim may remain locally scoped to its parent object until cross-object reuse justifies a global identity.

## 13. Human knowledge body contract

For METHOD, the durable human body should normally include:

`Core Question → Purpose → Scope In/Out → Inputs → Decision Logic → Procedure → Outputs → Failure Conditions → Boundary → Validation → Evidence Basis → Limitations → Open Questions → Related Knowledge`.

Runtime/provenance/readback records are linked externally rather than copied into the body.

## 14. Identity and retrieval

- Existing IDs remain immutable lineage anchors.
- New objects should prefer stable identity IDs with mutable classification metadata.
- Retrieval position remains exactly `CURRENT | SUPPORT | PROVENANCE | EXCLUDED`.

## 15. Validator rules

- `KCL-001`: Object Plane must be KNOWLEDGE;
- `KCL-002`: exactly one Primary Domain normally required for canonical objects;
- `KCL-003`: Related Domain cannot satisfy parent cardinality;
- `KCL-004`: exactly one Primary Knowledge Role;
- `KCL-005`: L4 requires all five admission gates;
- `KCL-006`: Framework Type only when L4;
- `KCL-007`: new Framework Type requires insufficiency proof;
- `KCL-008`: runtime `depends_on/stale_if` forbidden as reusable knowledge relations;
- `KCL-009`: state cannot auto-modify taxonomy classification;
- `KCL-010`: runtime/provenance logs cannot dominate human knowledge body;
- `KCL-011`: ID remains stable through classification correction;
- `KCL-012`: Cross-disciplinary is not an L2 Domain merely because multiple disciplines participate.