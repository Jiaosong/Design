# M03｜Autonomy × Control

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** AI 自动推进与 Human authority 的决策边界

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart TD
    A[Next action] --> R{Reversible?}
    R -- No --> H[Human authorization / authority route]
    R -- Yes --> S{Scope + Current fresh?}
    S -- No --> G[Mutation Guard / Re-resolve]
    S -- Yes --> V{Human-only value decision?}
    V -- Yes --> H
    V -- No --> P{External irreversible / publish?}
    P -- Yes --> H
    P -- No --> X[Auto-advance]
    X --> B[Actual result]
    B --> C[Readback]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
