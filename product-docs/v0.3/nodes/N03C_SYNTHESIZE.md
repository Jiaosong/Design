# N03C｜SYNTHESIZE

[← STUDIO](N03_STUDIO.md)

| Field | Value |
|---|---|
| Node ID | N03C |
| Children | N03C1, N03C2 — see [Atomic Children](#atomic-children) |
| Parent | N03 |
| Type | Studio Mode |
| Product job | 减少无效复杂度，同时保护独立有效设计信息 |
| Inputs | Relations, components, branches, findings |
| Outputs | Merge/simplification moves + loss checks |
| Authority | Human owns high-impact deletion / simplification |
| Primary metric | simplification accepted without material loss |
| Release priority | P1 |
| Doc state | WORKING |

## Synthesis Mindmap

```mermaid
mindmap
  root((SYNTHESIZE))
    Complexity
      core
      supporting
      redundant
      duplicated
      incidental
    Actions
      merge
      simplify
      hierarchy
      grammar
    Guard
      NO_COMPRESSION
      NO_LOSS
      professional_function
      design_value
```

## Flow

```mermaid
flowchart LR
    C[Complexity review] --> O[Merge / simplify option]
    O --> B[Before / After compare]
    B --> L{Material loss?}
    L -- Yes --> X[Reject / revise]
    L -- No --> H[Human decision]
    H --> A[Artifact change]
    A --> R[Whole-design readback]
```

## Feature Nodes

SYN-F01–F07: Complexity Review, Merge Opportunity, Design Economy, Grammar Consistency, Hierarchy Reinforcement, Simplification Test, Loss Check.

## Acceptance

“更简洁”本身不是删除理由。Any independent valid layer removed requires explicit design rationale and post-change readback.\n\n## Atomic Children

```mermaid
flowchart TB
    P[N03C SYNTHESIZE]
    P --> N03C1[N03C1 COMPLEXITY REVIEW]
    P --> N03C2[N03C2 SIMPLIFICATION / LOSS CHECK]
```

- [N03C1｜COMPLEXITY REVIEW](atomic/N03C1_COMPLEXITY_REVIEW.md)
- [N03C2｜SIMPLIFICATION / LOSS CHECK](atomic/N03C2_SIMPLIFICATION_LOSS_CHECK.md)
