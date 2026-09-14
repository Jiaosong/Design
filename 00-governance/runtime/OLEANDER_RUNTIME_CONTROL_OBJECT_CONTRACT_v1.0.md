# OLEANDER Runtime Control Object Contract v1.0

Status: **DRAFT / RUNTIME_CONTROL PLANE ONLY**. Binding candidate under `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0`.

## 1. Scope

Runtime Control objects exist to coordinate, audit, reopen, route or promote project execution. They are not reusable knowledge taxonomy objects and are not the project facts themselves.

`PROJECT FACT / DESIGN / EVIDENCE → RUNTIME CONTROL RECORD → ACTION / GATE / REOPEN / PROMOTION`.

## 2. Stable object family

Keep the family deliberately compact:

- `PROJECT_STATE` — current project operating-state snapshot;
- `DECISION_OBJECT` — orchestration handle for a current decision question, distinct from the Project-plane DECISION semantic record when both are needed;
- `DESIGN_INTELLIGENCE_PACKET` — bounded design-intelligence invocation/output coordination packet;
- `CROSS_DISCIPLINARY_INTEGRATION_PACKET` — coordinated multi-discipline integration packet;
- `SHARED_VARIABLE_REGISTER` — registry of controlled variables and their current authority/consumers;
- `INTERFACE_REGISTER` — registry view over Project-plane INTERFACE objects;
- `INTERFACE_ACCEPTANCE_CONTRACT` — required acceptance obligations for material interfaces;
- `JOINT_DECISION_RECORD` — cross-owner decision coordination receipt;
- `DISCIPLINE_REVIEW_RECEIPT`;
- `INTEGRATION_RECEIPT`;
- `DESIGN_REVIEW_RECEIPT`;
- `AUTHORITY_SNAPSHOT`;
- `KNOWLEDGE_SNAPSHOT`;
- `GATE_STATE`;
- `CLAIM_PROMOTION_STATE`;
- `READBACK_RECEIPT`;
- `G9_REUSE_CANDIDATE`.

Do not create a new Runtime Control type merely because a Project object has a status field.

## 3. Common envelope

All control objects should implement the applicable subset of:

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

## 4. Control semantics

### `depends_on`
Runtime execution dependency. It answers what must remain valid before this control record remains actionable.

### `stale_if`
Explicit invalidation trigger. Examples:
- upstream baseline changed;
- authority snapshot changed;
- required evidence superseded;
- shared variable changed;
- interface reopened;
- source revision changed;
- material project assumption was refuted.

### `claim_ceiling`
Maximum conclusion this control record is allowed to propagate. A receipt may report an execution PASS without granting a stronger design, research, field, safety or professional claim.

### `open_blockers`
Unresolved blockers relevant to the control object. `BLOCKED` remains a state/disposition, not a knowledge category.

### `readback_refs`
Actual reopened/readback evidence required to close or promote the runtime-control state.

## 5. Boundary with Project Plane

Project semantic objects remain in `PROJECT`, including:

- Requirement;
- Constraint;
- System Element;
- Controlled Variable;
- Interface;
- Decision;
- Risk / Issue / Assumption / Unknown;
- Artifact;
- Evidence Record;
- Assurance Activity/Decision;
- Baseline;
- Change.

Runtime control may **register, route, snapshot, validate or reopen** those objects but must not replace their identities.

Examples:

`PROJECT INTERFACE IF-011` → listed in → `RUNTIME_CONTROL INTERFACE_REGISTER IR-04`.

`PROJECT CONTROLLED_VARIABLE VAR-014` → listed in → `RUNTIME_CONTROL SHARED_VARIABLE_REGISTER SVR-02`.

`PROJECT EVIDENCE EVD-044` → referenced by → `RUNTIME_CONTROL READBACK_RECEIPT RBR-17`.

## 6. Boundary with Knowledge Plane

A Knowledge METHOD may define reusable logic for producing or interpreting Runtime Control records, but its human body should not accumulate project-specific receipts, hashes, synchronization histories or current gate state.

Allowed Knowledge-to-Runtime relation examples:

- METHOD `IMPLEMENTS_AS` Runtime schema;
- METHOD `INVOKED_BY` control packet;
- Runtime receipt `USES_KNOWLEDGE_SNAPSHOT`;
- G9 candidate `PROPOSES_DISTILLATION_TO` Knowledge object.

Forbidden:

- storing project `depends_on/stale_if` as Knowledge dependency semantics;
- embedding a changing receipt ledger into a canonical METHOD body;
- treating a GitHub commit/readback event as conceptual knowledge content.

## 7. Staleness propagation

Runtime Control must support explicit invalidation.

Examples:

`AUTHORITY_SNAPSHOT changed → packets using old snapshot = STALE`.

`CONTROLLED_VARIABLE changed → affected Interface Register entries + integration packets + receipts = REOPEN_REQUIRED`.

`BASELINE superseded → receipts proving only previous baseline = HISTORICAL / NOT CURRENT`.

`Evidence rejected/stale → dependent promotion state = REOPEN/HOLD`.

Staleness propagates through registered runtime edges, not by rewriting Knowledge taxonomy.

## 8. Promotion boundary

A runtime-control object can be:

`WORKING | REVIEWABLE | CURRENT_FOR_EXECUTION | STALE | SUPERSEDED | CLOSED` as applicable.

But runtime-control promotion never automatically promotes:

- Project Design Quality;
- Research validity;
- field truth;
- professional compliance;
- Knowledge Content PASS;
- Knowledge CURRENT status.

Those remain owned by their respective gates and source objects.

## 9. G9 boundary

`G9_REUSE_CANDIDATE` is still Runtime Control until Knowledge Distillation admits a reusable object.

Flow:

`Project/Runtime evidence → G9_REUSE_CANDIDATE → deproject / generalize / claim-evidence review / provenance → Knowledge classification → Content/Research gates → Knowledge promotion`.

Project success does not automatically create general knowledge.

## 10. Validator floor

- `RTC-001`: `object_plane` must equal `RUNTIME_CONTROL`;
- `RTC-002`: type must be in the controlled Runtime Control family unless extension admission is documented;
- `RTC-003`: project semantic object identity cannot be replaced by a register/receipt identity;
- `RTC-004`: stale_if triggers must be resolvable where material;
- `RTC-005`: runtime execution PASS cannot exceed `claim_ceiling`;
- `RTC-006`: changed authority/baseline/evidence reopens affected control records;
- `RTC-007`: project-specific receipt/readback history forbidden from canonical Knowledge body;
- `RTC-008`: G9 candidate cannot bypass Knowledge Distillation and Content/Research gates.