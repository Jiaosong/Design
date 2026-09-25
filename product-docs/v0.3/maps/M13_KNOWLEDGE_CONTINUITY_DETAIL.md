# M13｜Knowledge + History Detail

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 证据适用性、claim ceiling、decision history 与 handoff

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    KN[N08A Knowledge Need] --> SE[N08B Source / Evidence]
    SE --> AL[N08C Applicability / Limitation]
    SE --> EC[N08D Contradiction]
    AL --> CC[N08E Claim Ceiling]
    EC --> CC
    DH[N09A Decision History] --> RP[N09C Resume Point]
    RD[N09B Rejected Direction Memory] --> RP
    RP --> HP[N09D Handoff Pack]
    DH --> LC[N09E Project Learning Candidate]
    CC --> DH
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
