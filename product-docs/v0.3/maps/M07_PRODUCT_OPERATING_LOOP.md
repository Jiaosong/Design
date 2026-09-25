# M07｜Product Operating Loop

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 从 customer problem 到发布后学习的产品经营闭环

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    C[Customer problem] --> S[Strategy / PRFAQ]
    S --> P[Master PRD]
    P --> N[Node Specs]
    N --> B[Build]
    B --> E[Eval / Pilot]
    E --> M[Metrics]
    M --> L[Launch Readiness]
    L --> D{Decision}
    D -->|Continue| R[Roadmap]
    D -->|Iterate| P
    D -->|Reframe| S
    D -->|Stop| X[Close / Preserve Learning]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
