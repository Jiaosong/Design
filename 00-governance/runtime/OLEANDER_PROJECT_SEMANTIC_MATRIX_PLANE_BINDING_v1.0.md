# OLEANDER Project Semantic Matrix — Object Plane Binding v1.0

Status: **DRAFT COMPATIBILITY BINDING**.

This binding resolves terminology in the existing draft files:

- `OLEANDER_COMPLEX_PROJECT_RUNTIME_CLASSIFICATION_DETAIL_FRAMEWORK_v1.0.*`;
- `OLEANDER_RUNTIME_OBJECT_RELATION_ALLOWED_MATRIX_v1.0.md`;
- `OLEANDER_RUNTIME_OBJECT_STATE_ALLOWED_MATRIX_v1.0.md`;
- `OLEANDER_RUNTIME_PROMOTION_CLOSURE_MATRIX_v1.0.md`;
- `OLEANDER_RUNTIME_CLASSIFICATION_MATRICES_v1.0.json`.

## Binding

The atomic classes governed by those matrices — Requirement, Constraint, System Element, Controlled Variable, Interface, Decision, Risk, Issue, Assumption, Unknown, Artifact, Evidence, Assurance, Baseline, Change, etc. — are interpreted as **Project-plane semantic objects** unless a row is explicitly a runtime-control record.

Therefore:

`Object Plane = PROJECT` is the default plane for those matrix rows.

The files retain their historical draft filenames to avoid unnecessary lineage churn, but the phrase `runtime object` in them means **project object participating in the runtime**, not `RUNTIME_CONTROL` Object Plane.

## Runtime-control separation

Packets, registers, receipts, gate state, authority/knowledge snapshots, readback receipts and promotion-state controls are governed by:

- `OLEANDER_RUNTIME_CONTROL_OBJECT_CONTRACT_v1.0.md`;
- `OLEANDER_OBJECT_PLANE_TYPED_SYSTEM_ARCHITECTURE_v1.0.*`.

Do not add packet/register/receipt types into the Project semantic Object × State matrix merely because they are operational.

## Presentation separation

Presentation objects remain an orthogonal projection layer governed by:

- `OLEANDER_PROJECT_PRESENTATION_LAYER_v1.0.*`;
- `OLEANDER_PRESENTATION_STYLE_TECHNIQUE_SYSTEM_v1.0.*`.

They are not a fourth Object Plane and must preserve the plane/classification of their upstream source objects.

## Validator interpretation

Any validator compiled from the existing matrices should prepend:

1. resolve `object_plane`;
2. if `PROJECT`, apply the Project semantic class/state/relation matrices;
3. if `RUNTIME_CONTROL`, apply Runtime Control Contract instead;
4. if `KNOWLEDGE`, route to Knowledge Classification Contract;
5. Presentation checks are applied orthogonally to projection/release records.

This binding supersedes any interpretation that all existing matrix classes are members of the `RUNTIME_CONTROL` plane.