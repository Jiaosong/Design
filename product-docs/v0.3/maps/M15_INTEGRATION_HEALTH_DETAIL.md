# M15｜Integration + Settings + Health Detail

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 工具连接、外部写入、降级与产品健康

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    IC[N12A Integration Contract] --> EW[N12B External Write]
    IC --> DI[N12C Degraded Integration]
    CP[N13B Connector Permissions] --> IC
    DP[N13A Data / Privacy Settings] --> IC
    HS[N14A Health Signal] --> DR[N14B Degraded Route]
    DI --> DR
    DR --> IR[N14C Incident / Recovery]
    AC[N13C Accessibility Settings] --> UI[Visible Product Surfaces]
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
