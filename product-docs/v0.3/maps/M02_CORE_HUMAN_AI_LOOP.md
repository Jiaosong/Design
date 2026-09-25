# M02｜Core Human–AI Loop

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 从恢复项目到下一轮连续协作的主循环

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    U[Human intent] --> RES[Resume / Resolve]
    RES --> Q[Current Design Question]
    Q --> EX[Explore]
    EX --> MK[Make real artifact]
    MK --> RB[Readback]
    RB --> CR[Critique]
    CR --> CH{Human decision needed?}
    CH -- No --> DV[Develop / Repair]
    CH -- Yes --> ST[Human Steer]
    ST --> DV
    DV --> MK
    RB --> NX[Continue next session]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
