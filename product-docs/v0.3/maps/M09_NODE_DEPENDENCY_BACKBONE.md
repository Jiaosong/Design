# M09｜Node Dependency Backbone

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 一级产品节点之间的主依赖

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart TB
    HOME --> FOCUS
    FOCUS --> STUDIO
    STUDIO --> ARTIFACTS
    ARTIFACTS --> REVIEW
    REVIEW --> STUDIO
    REVIEW --> MAP
    MAP --> STUDIO
    KNOWLEDGE --> FOCUS
    KNOWLEDGE --> REVIEW
    COMPARE --> STUDIO
    COMPARE --> HISTORY
    ARTIFACTS --> HISTORY
    REVIEW --> HISTORY
    SESSION[SESSION KERNEL] -.orchestrates.-> HOME
    SESSION -.orchestrates.-> STUDIO
    SESSION -.orchestrates.-> ARTIFACTS
    PEOPLE[PEOPLE / AUTHORITY] --> SESSION
    INTEGRATIONS --> ARTIFACTS
    HEALTH[SYSTEM HEALTH] --> SESSION
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.2.md)。
