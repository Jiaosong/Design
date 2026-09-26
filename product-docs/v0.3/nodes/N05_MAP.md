# N05｜MAP

[← Node Graph](README.md)

| Field | Value |
|---|---|
| Node ID | N05 |
| Children | N05A, N05B, N05C, N05D — see [Atomic Children](#atomic-children) |
| Type | Product Surface |
| Product job | 表达 materially important Design Relation、dependency 与 change impact |
| Inputs | Relations, decisions, artifacts, findings, domain interfaces |
| Outputs | Impact graph + Revision Scope |
| Authority | Map describes dependencies; does not create domain authority |
| Primary metric | Change Impact precision / Full-reset avoidance |
| Release priority | P1 |
| Doc state | WORKING |

## Relation Graph

```mermaid
flowchart LR
    V[Design Value] --> R1[Relation]
    Q[Question] --> R1
    R1 --> A[Artifact]
    R1 --> R2[Dependent Relation]
    R2 --> D[Domain]
    F[Finding] --> R1
    C[Change] --> R1
    C --> I[Impact traversal]
    I --> RS[Revision Scope]
```

## Change Impact

```mermaid
mindmap
  root((Revision Scope))
    AFFECTED
      relations
      artifacts
      decisions
      domains
      verification
    PRESERVED
      valid_relations
      valid_artifacts
    UNKNOWN
      unresolved_dependencies
```

## Feature Nodes

MAP-F01–F11: Relation Create/Link/Importance/Stability, Change Impact, Whole/Local, Artifact/Issue/Professional Binding, Dependency Traversal, Preserve Unaffected Scope.

## Acceptance

- only material relations become first-class;
- change does not imply global reopen;
- unknown dependency remains UNKNOWN;
- unaffected valid work is explicitly preserved.

## Atomic Children

```mermaid
flowchart TB
    P[N05 MAP]
    P --> N05A[N05A DESIGN RELATION]
    P --> N05B[N05B CHANGE IMPACT]
    P --> N05C[N05C REVISION SCOPE]
    P --> N05D[N05D PROFESSIONAL BINDING]
```

- [N05A｜DESIGN RELATION](atomic/N05A_DESIGN_RELATION.md)
- [N05B｜CHANGE IMPACT](atomic/N05B_CHANGE_IMPACT.md)
- [N05C｜REVISION SCOPE](atomic/N05C_REVISION_SCOPE.md)
- [N05D｜PROFESSIONAL BINDING](atomic/N05D_PROFESSIONAL_BINDING.md)
