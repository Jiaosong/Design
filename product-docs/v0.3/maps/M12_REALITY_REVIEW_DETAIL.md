# M12｜MAP + ARTIFACT + REVIEW Detail

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 关系、artifact、readback、finding、verification/validation 的细节点图

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    R[N05A Design Relation] --> I[N05B Change Impact]
    I --> S[N05C Revision Scope]
    P[N05D Professional Binding] --> I
    R --> A[N06A Artifact Identity]
    A --> AR[N06B Artifact Role]
    A --> RV[N06C Revision Identity]
    RV --> RB[N06D Readback]
    AR --> FC[N06E Fidelity / Claim Ceiling]
    RB --> RT[N07A Review Target]
    RT --> F[N07B Finding]
    F --> RC[N07C Root Cause]
    RC --> S
    RB --> V[N07D Verification]
    RB --> VA[N07E Validation]
    F --> IR[N07F Independent Review]
    S --> RR[N07G Recheck / Re-readback]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
