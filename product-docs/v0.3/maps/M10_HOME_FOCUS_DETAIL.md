# M10｜HOME + FOCUS Detail

[← Visual Maps](README.md) · [← Node Graph](../nodes/README.md)

**Purpose:** 恢复状态、形成 Question 与下一 frontier 的原子节点图

> This map is a view of product nodes and relations. It does not create a new authority or state.

```mermaid
flowchart LR
    N01A[Resume Snapshot] --> N01B[Frontier]
    N01C[Critical Open] --> N01B
    N01D[Active Artifact] --> N01A
    N01B --> N01E[Next Action]
    N02A[Problem] --> N02B[Current Question]
    N02C[Design Value] --> N02B
    N02D[Constraint / Assumption] --> N02B
    N02B --> N02E[Success Condition]
    N02E --> N02F[Reframe when contradicted]
    N02B --> N01B
```

## Reading Rule

沿图进入 Node Docs 阅读 behaviour、acceptance、authority、metric 和 open questions；不要把图中的箭头解释成 ownership，边语义见 [Node Relation Schema](../nodes/NODE_RELATION_SCHEMA_v0.3.1.md)。
