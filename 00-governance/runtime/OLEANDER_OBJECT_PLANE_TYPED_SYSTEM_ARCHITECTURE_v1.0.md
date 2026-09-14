# OLEANDER Object Plane + Typed System Architecture v1.0

Status: **DRAFT GOVERNANCE EXTENSION**. This is an upper-level semantic calibration for the existing Knowledge System, Complex Project Runtime, Runtime Control, Presentation Layer, Content/Research gates and Retrieval Layer. It does not create `L-1`, a second taxonomy, a fourth Object Plane, or a parallel authority tree.

## 1. First decision: Object Plane before taxonomy

Before any `L0–L7`, Project Axis, runtime object class, or presentation classification is assigned, resolve exactly one primary Object Plane:

- `KNOWLEDGE` — reusable cross-project knowledge objects;
- `PROJECT` — project-specific facts, decisions, requirements, designs, artifacts, tests and evidence;
- `RUNTIME_CONTROL` — control records that drive, coordinate, audit or reopen the operating system.

Hard rule:

`OBJECT PLANE ≠ TAXONOMY LEVEL`.

There is no `L-1`. The plane decision is an orthogonal semantic routing decision.

Routing:

`KNOWLEDGE → Knowledge Classification Contract (L0–L7 + Role + Relations + lifecycle)`

`PROJECT → Project Plane / P-axis / Project Semantic Objects / project state and assurance`

`RUNTIME_CONTROL → Master Runtime control-object schemas`

## 2. Why this separation is mandatory

A reusable method page must not simultaneously carry:

- human-readable method knowledge;
- runtime schema;
- invocation packet;
- receipt history;
- promotion state;
- GitHub/Notion synchronization log;
- D1/readback history.

Those are different semantic planes.

A METHOD knowledge object may explain the reusable method and expose a stable interface contract, but execution packets, receipts, state snapshots and synchronization records belong to `RUNTIME_CONTROL`.

Hard invariant:

`HUMAN KNOWLEDGE BODY ≠ RUNTIME CONTROL RECORD ≠ PROJECT EXECUTION EVIDENCE`.

## 3. Three-plane architecture

### 3.1 KNOWLEDGE plane

Purpose: preserve reusable explanation, theory, method, tool logic, source interpretation, evidence/case knowledge and practice learning that survives one project.

Primary routing dimensions:

`Subject Ownership × L0–L7 × Primary Knowledge Role × Framework Type [L4 only] × Typed Knowledge Relations × Knowledge States × Claim–Evidence × Provenance/Lifecycle`.

### 3.2 PROJECT plane

Purpose: describe what is true, required, chosen, produced, tested, uncertain or changed in one project.

Project semantic classes may include:

- INTENT / NEED / REQUIREMENT / CONSTRAINT / PROJECT CLAIM;
- SYSTEM ELEMENT / BEHAVIOR-STATE MODEL / CONTROLLED VARIABLE;
- WORK PACKAGE / TASK / ARTIFACT;
- INTERFACE / MATERIAL DEPENDENCY;
- DECISION / WAIVER / DEVIATION;
- RISK / ISSUE / ASSUMPTION / UNKNOWN;
- EVIDENCE RECORD / ASSURANCE ACTIVITY / ASSURANCE DECISION;
- BASELINE / CHANGE;
- ACTOR / AUTHORITY ROLE where project-scoped.

These are project semantic objects. They are **not** `RUNTIME_CONTROL` merely because the system stores or validates them.

### 3.3 RUNTIME_CONTROL plane

Purpose: coordinate invocation, precedence, staleness, reopening, promotion, audit and cross-system execution.

The stable control-object family should remain compact:

- `PROJECT_STATE`;
- `DECISION_OBJECT` control envelope when used as orchestration handle;
- `DESIGN_INTELLIGENCE_PACKET`;
- `CROSS_DISCIPLINARY_INTEGRATION_PACKET`;
- `SHARED_VARIABLE_REGISTER`;
- `INTERFACE_REGISTER`;
- `INTERFACE_ACCEPTANCE_CONTRACT`;
- `JOINT_DECISION_RECORD`;
- `DISCIPLINE_REVIEW_RECEIPT`;
- `INTEGRATION_RECEIPT`;
- `DESIGN_REVIEW_RECEIPT`;
- `AUTHORITY_SNAPSHOT`;
- `KNOWLEDGE_SNAPSHOT`;
- `GATE_STATE`;
- `CLAIM_PROMOTION_STATE`;
- `READBACK_RECEIPT`;
- `G9_REUSE_CANDIDATE`.

Project evidence/artifacts/tests referenced by these records remain `PROJECT` objects; the receipt/register/packet that coordinates them is `RUNTIME_CONTROL`.

## 4. Presentation is a projection layer, not a fourth plane

`PRESENTATION` is intentionally **not** a primary Object Plane.

Presentation semantics are an orthogonal projection over approved objects:

`KNOWLEDGE / PROJECT / RUNTIME_CONTROL SOURCE → PRESENTATION PROJECTION → AUDIENCE / MEDIUM / CONTEXT → READBACK`.

Presentation objects such as Audience Contract, Argument Unit, Evidence Projection, View Unit, Style Profile, Technique Set, Sequence and Release describe **how source truth is communicated**, not what plane the source truth belongs to.

Hard rules:

- `PRESENTATION KEEP ≠ PROJECT KEEP`;
- `STYLE ≠ SOURCE AUTHORITY`;
- `PRESENTATION DERIVATIVE ≠ PROJECT EVIDENCE` unless separately admitted through the applicable evidence gate;
- presentation metadata must not mutate source classification.

## 5. Eight-axis Knowledge Classification Contract

For `Object Plane = KNOWLEDGE`, classification uses eight orthogonal axes.

### Axis A — Object Plane

Fixed here as `KNOWLEDGE` after routing.

### Axis B — Subject Ownership

Fields:

- `Primary Domain` — normally exactly 1;
- `Primary Topic` — 0..1 structural position;
- `Related Domain[]` — 0..N;
- `Application Mapping[]` — 0..N.

Hard boundaries:

`Related Domain ≠ second parent`

`Application Mapping ≠ Domain`

`Project use ≠ Domain`

`Cross-disciplinary relevance ≠ new Domain`

### Axis C — Knowledge Level

Freeze the current `L0–L7` model:

- L0 System;
- L1 Branch;
- L2 Domain;
- L3 Topic;
- L4 Integrating Framework;
- L5 Knowledge Object;
- L6 Source / Evidence / Case;
- L7 Practice / Output.

Default canonical knowledge object level: **L5**.

L4 is exceptional and requires a separate admission gate.

### Axis D — Primary Knowledge Role

Exactly one:

`INDEX | THEORY | METHOD | TOOL | SOURCE | EVIDENCE | CASE | PRACTICE`.

Compound primary roles are forbidden. Secondary semantics are expressed through typed relations and Information Role.

### Axis E — Framework Type

Only applicable when the object legitimately passes L4 admission.

Freeze the current controlled set:

`NAVIGATION_MAP | CONCEPTUAL_MODEL | METHOD_FAMILY | PROCESS_ORCHESTRATION | PROFESSIONAL_SYSTEM_MAP | TYPOLOGY_FRAMEWORK | APPLICATION_FRAMEWORK | DESIGN_LANGUAGE_SYSTEM | STRATEGY_FRAMEWORK | EVALUATION_FRAMEWORK | HISTORICAL_COMPARATIVE_SYNTHESIS`.

A new Framework Type requires proof that none of these can represent the object without semantic distortion.

### Axis F — Typed Knowledge Relations

At minimum preserve separate families:

- `STRUCTURAL_HIERARCHY`;
- `DOMAIN_PLACEMENT`;
- `KNOWLEDGE_DEPENDENCY`;
- `EVIDENCE_SUPPORT`;
- `APPLICATION_USE`;
- `LIFECYCLE_LINEAGE`.

Controlled relations should include where applicable:

`REQUIRES_CONCEPT | EXTENDS | REFINES | CONTRASTS_WITH | IMPLEMENTS | CONSTRAINED_BY | SUPPORTS_CLAIM | CONTRADICTS_CLAIM | BOUNDS_CLAIM`.

Hard boundary:

`Knowledge dependency ≠ Project Runtime dependency`.

Do not copy project `depends_on / stale_if / shared-variable propagation` semantics into the reusable knowledge graph.

### Axis G — Knowledge State

Classification must remain independent from state. Display separately:

- Authority Layer: `CURRENT | SUPPORT | PROVENANCE | EXCLUDED`;
- Governance;
- Evidence;
- Trust;
- Freshness;
- Content;
- Research R1/R2;
- Bilingual;
- Graph state.

Forbidden inferences:

`CURRENT → trustworthy`

`L4 → mature`

`VERIFIED → higher taxonomy level`

`frequent project use → Framework promotion`

### Axis H — Information Role

Information Role describes how the human-facing carrier is primarily read. It does not change Knowledge Role.

Controlled set:

`EXPLANATION | PROCEDURE | REFERENCE | NAVIGATION | DECISION_SUPPORT | AUDIT_READBACK | CASE_NARRATIVE`.

Examples:

`Knowledge Role=METHOD + Information Role=PROCEDURE`

`Knowledge Role=THEORY + Information Role=EXPLANATION`

`Knowledge Role=INDEX + Information Role=NAVIGATION`.

## 6. L4 Integrating Framework admission gate

L4 requires all of:

1. `BREADTH` — multiple independent L5 owners actually exist;
2. `INTEGRATION` — the object contributes its own cross-object relation/routing/coordination logic;
3. `DELEGATION` — it does not duplicate subordinate L5 bodies;
4. `BOUNDARY` — scope-out and owner boundaries are explicit;
5. `REUSE` — the integration structure is stable across projects/contexts.

A long or important method does not become L4 merely because it has many steps.

`1 method + 40 pages = still potentially L5`.

`3 independent methods + selection/composition/conflict/handoff logic = potential L4 METHOD_FAMILY`.

## 7. L2 Domain Admission Gate

A new L2 Domain requires all of the following at sufficient strength:

- independent stable problem-space semantics;
- multiple Topics/Knowledge Objects, not one orphan page;
- distinct method/validation ecology from adjacent domains;
- distinct regulation/standard/research/evidence ecosystem where applicable;
- identifiable professional owner/reviewer capability;
- long-term cross-project stability;
- non-substitutability: placement in an existing Domain would materially distort semantics.

A project HOLD, application type, or single building typology does not automatically justify a new L2.

Hard rule:

`Cross-disciplinary ≠ Domain`.

Cross-disciplinary integration is primarily a Project/Runtime relation problem.

## 8. Claim–Evidence as addressable semantic layer

Claims should become increasingly addressable instead of remaining only page-level prose or a flat citation count.

Target model:

`Knowledge Object → Claim Cxx → supports / bounds / contradicts → Evidence Eyy → provenance / strength / confidence / conditions`.

Consequential claims should resolve to evidence and explicit limitations. Several weak citations do not automatically produce a strong claim.

Claim identity may initially be local-to-object and later become globally addressable if cross-object reuse justifies objectification.

## 9. Human body vs runtime/provenance separation

A formal METHOD human knowledge body should contain only durable human knowledge such as:

- Core Question;
- Purpose;
- Scope In / Out;
- Inputs;
- Decision Logic;
- Procedure;
- Outputs;
- Failure Conditions;
- Boundary;
- Validation;
- Evidence Basis;
- Limitations;
- Open Questions;
- Related Knowledge.

The following belong outside the professional human body unless needed as a short current pointer:

- Notion page ID;
- latest GitHub commit / PR;
- SHA256/digest;
- apply receipt;
- synchronization timestamp;
- D1 readback;
- migration batch;
- detailed CURRENT/SUPPORT migration history;
- invocation receipts and execution logs.

Persist these under controlled `TECHNICAL_PROVENANCE`, `RUNTIME_METADATA`, `READBACK_HISTORY` or linked `RUNTIME_CONTROL` records.

## 10. Stable runtime-control envelope

Runtime-control objects should use a common envelope where applicable:

```yaml
object_id:
schema_version:
object_plane: RUNTIME_CONTROL
runtime_control_type:
project_id:
workstream_id:
decision_object_id:
authority_snapshot_ref:
knowledge_snapshot_ref:
source_revision:
owner:
participants: []
status:
depends_on: []
stale_if: []
claim_ceiling:
open_blockers: []
readback_refs: []
supersedes:
superseded_by:
created_at:
updated_at:
```

`depends_on / stale_if` are runtime-control semantics and must not leak into the reusable Knowledge dependency ontology.

## 11. Identity policy

Existing canonical IDs are immutable lineage anchors and must not be bulk-renamed merely because classification changes.

Future identity design should increasingly separate:

`stable immutable identity ID + mutable classification metadata`.

Hard rule:

`ID immutable; classification mutable`.

A correction such as `THEORY → METHOD` or `L4 → L5` should normally update classification, not replace identity.

## 12. Retrieval position remains separate

Freeze retrieval/authority position as:

`CURRENT | SUPPORT | PROVENANCE | EXCLUDED`.

This answers where the object participates in retrieval and authority resolution. It does not answer what the knowledge object is.

Examples that are semantically valid:

- `L5 / THEORY / SUPPORT`;
- `L6 / SOURCE / CURRENT`;
- `L4 / INDEX / SUPPORT`;
- `L7 / PRACTICE / PROVENANCE`.

## 13. System architecture

```text
                    OLEANDER CURRENT AUTHORITY
                             │
               ┌─────────────┼─────────────┐
               │             │             │
          KNOWLEDGE        PROJECT    RUNTIME_CONTROL
               │             │             │
        Domain / Topic   Requirement    Packet / Register
        L0–L7            Decision       Receipt / Gate State
        Primary Role     Artifact       Authority Snapshot
        Framework Type   Evidence       Readback / Promotion
        Knowledge Rel.   Interface            │
               │             │                │
               └──────────┬──┴────────────────┘
                          │
                    Claim–Evidence
                          │
              Provenance / Trust / Freshness
                          │
              Content / Research / Assurance
                          │
                   Retrieval / Promotion
                          │
          CURRENT / SUPPORT / PROVENANCE / EXCLUDED

Presentation = orthogonal audience/medium projection over approved source objects.
```

## 14. Validator floor

- `PLANE-001` exactly one primary Object Plane;
- `PLANE-002` L0–L7 forbidden unless Object Plane=KNOWLEDGE;
- `PLANE-003` runtime-control packets/receipts/registers forbidden from masquerading as reusable knowledge body;
- `PLANE-004` project facts/evidence forbidden from being promoted to reusable knowledge without Knowledge Distillation gates;
- `KN-ROLE-001` exactly one Primary Knowledge Role;
- `KN-L4-001` L4 must pass BREADTH+INTEGRATION+DELEGATION+BOUNDARY+REUSE;
- `KN-DOM-001` new L2 must pass Domain Admission Gate;
- `KN-REL-001` `related` cannot replace hierarchy or stronger typed relation;
- `KN-STATE-001` taxonomy level cannot be inferred from trust/maturity/use frequency;
- `KN-BODY-001` runtime/provenance logs cannot dominate human knowledge body;
- `ID-001` classification changes do not rename stable identity by default;
- `PRES-001` Presentation Layer cannot modify upstream truth or evidence ceiling;
- `RUNTIME-001` runtime `depends_on/stale_if` cannot be copied into Knowledge dependency semantics.

## 15. Priority order

1. Freeze `Level × Role × Framework Type` and remove legacy production-rule residues.
2. Complete Master Runtime authority contract: invocation, precedence, staleness, claim ceiling, promotion.
3. Continue full-body Content Review over the **dynamic current corpus**; no fixed total is encoded in this contract.
4. Repair Relation Ontology and graph-open objects with typed relations rather than RELATED inflation.
5. Establish and apply L2 Domain Admission Gate.
6. Split human knowledge body from runtime/provenance/readback in core OLEANDER methods first.
7. Evolve Claim–Evidence Ledger toward addressable claims where consequence/reuse justifies it.
8. Optimize Reader IA and automated routing after the semantics above are stable.

The architecture therefore moves from a Knowledge Tree model to **Typed Knowledge + Project Semantics + Runtime Control Graph**, with the tree retained only where hierarchy is genuinely the right semantic structure.