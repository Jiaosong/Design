# M08｜Release Gates

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 内部参考、外部 pilot、longitudinal、多 Human 与 beta 的推进门

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart TD
    A[Internal Reference] --> B{Core semantics pass?}
    B -- No --> A
    B -- Yes --> C[Closed External Pilot]
    C --> D{Value + guardrails?}
    D -- No --> E[Iterate / Reframe]
    D -- Yes --> F[Longitudinal Pilot]
    F --> G{Continuity sustained?}
    G -- No --> E
    G -- Yes --> H[Multi-human Pilot]
    H --> I{Security / Privacy / Ops ready?}
    I -- No --> J[HOLD]
    I -- Yes --> K[Productized Beta]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
