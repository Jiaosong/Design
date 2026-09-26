# M11｜STUDIO + COMPARE Detail

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 探索、深化、综合与决策子节点

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    D[N03A1 Direction] --> S[N03A2 Alternative Set]
    S --> M[N03A3 Material Distinctness]
    B[N03A4 Baseline/OFF] --> S
    R[N03A5 Reference Transfer] --> D
    SS[N03A6 Search-space Map] --> D
    S --> TR[N03A7 AI Option Triage]
    M --> TR
    TR --> CW[N04A Comparison World]
    CW --> T[N04B Trade-off]
    T --> DR[N04C Decision Rationale]
    DR --> RC[N04D Reopen Condition]
    DR --> DEC[N04E Design Decision]
    DR --> F[N03B2 Development Frontier]
    MG[N03B1 Maturity Gap] --> F
    DA[N03B3 Domain Adapter] --> F
    F --> IC[N03B4 Intent Check]
    IC --> WC[N03B5 Whole-design Check]
    WC --> CR[N03C1 Complexity Review]
    CR --> LC[N03C2 Loss Check]
    CR --> SYN[N03C3 Design Synthesis]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.2.md)。
