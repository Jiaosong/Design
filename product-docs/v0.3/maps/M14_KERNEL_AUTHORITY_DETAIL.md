# M14｜Kernel + Authority Detail

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 四轴 interaction、steer、autonomy、mutation 与多人权责

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart TB
    WI[N10F Work Intent] --> K[N10 Session Kernel]
    MD[N10G Mutation Directive] --> K
    SM[N10H Support Mode] --> K
    HA[N10I Human Action Level] --> K
    K --> RR[N10A Resume / Recover]
    K --> HS[N10B Human Steer]
    K --> AS[N10C Autonomy / Human Stop]
    AS --> MG[N10D Mutation Guard]
    K --> CC[N10E Continuity / Closure]
    AR[N11A Actor Role] --> SR[N11B Scoped Rights]
    SR --> HS
    SR --> MG
    SR --> CH[N11C Conflict Hold]
    CH --> AS
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
