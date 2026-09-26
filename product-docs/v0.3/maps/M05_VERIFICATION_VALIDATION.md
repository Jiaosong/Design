# M05｜Verification vs Validation

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 避免 implemented-as-specified 与 real-world effectiveness 混淆

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart TD
    CLAIM[Design / Product Claim] --> X{What are we asking?}
    X -->|Implemented as specified?| VFY[Verification]
    X -->|Works for real user/context?| VAL[Validation]
    VFY --> E1[Requirement-matched evidence]
    VAL --> E2[Scenario / behaviour / outcome]
    E1 --> D[Design decision]
    E2 --> D
    D -->|Contradiction| R[Reframe / Revise]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.2.md)。
