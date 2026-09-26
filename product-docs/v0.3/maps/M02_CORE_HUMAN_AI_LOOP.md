# M02｜Core Human–AI Loop

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 从 Design Situation / Resume 到探索、决策、真实制作、whole-design check 与连续协作的主循环

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    U[Human intent / Brief] --> RES[Start / Resume / Continue / Recover]
    RES --> Q[Design Situation + Current Question]
    Q --> SS[Search-space Map]
    SS --> EX[Explore + AI Triage]
    EX --> CH{Human decision needed?}
    CH -- Yes --> DEC[Persistent Design Decision]
    CH -- No --> DV[Develop / Synthesize]
    DEC --> DV
    DV --> MK[Artifact Action / Intended Delta]
    MK --> ACT[Actual Delta]
    ACT --> RB[Readback]
    RB --> WC[Whole-design Check / Critique]
    WC -->|repair / deepen| DV
    WC -->|new framing needed| Q
    WC --> NX[Continue current session / Resume next session]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.2.md)。
