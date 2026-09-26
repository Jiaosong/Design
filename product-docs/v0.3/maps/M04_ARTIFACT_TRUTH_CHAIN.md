# M04｜Artifact Truth Chain

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 设计问题、intended delta、真实 artifact change、readback、finding 与 revision 的证据链

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    Q[Design Question] --> REL[Design Relation]
    REL --> ART[Artifact]
    ART --> INT[Intended Delta]
    INT --> GUARD[Action Guard]
    GUARD --> ACT[Artifact Action]
    ACT --> DELTA[Actual Delta]
    DELTA --> REV[Revision]
    REV --> RB[Readback]
    RB --> FIND[Finding]
    FIND --> NEXT[Next Design Action]
    NEXT --> REV2[New Revision]
    REV2 --> RB2[Re-readback]
    EVID[Evidence] --> Q
    EVID --> FIND
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.2.md)。
