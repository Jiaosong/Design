# M06｜Decision Chain

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 从 Design Situation / Question 到 persistent Design Decision、rationale、artifact consequence 与 reopen

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    P[Design Situation<br/>Problem / Opportunity / Ambition] --> Q[Question]
    Q --> O[Options]
    O --> C[Compare]
    C --> T[Trade-offs]
    T --> H[Human Steer / Scoped Rights]
    H --> D[N04E Design Decision]
    D --> R[Rationale]
    R --> RC[Reopen condition]
    D --> A[Artifact Action]
    A --> RB[Readback]
    RC -->|condition met| D
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.2.md)。
