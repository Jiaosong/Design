# N03B｜DEVELOP

[← STUDIO](N03_STUDIO.md)

| Field | Value |
|---|---|
| Node ID | N03B |
| Children | N03B1, N03B2, N03B3, N03B4 — see [Atomic Children](#atomic-children) |
| Parent | N03 |
| Type | Studio Mode |
| Product job | 把选定方向推进到更高真实专业分辨率 |
| Inputs | Selected direction, Frontier, Findings, Domain process |
| Outputs | Development actions, native/editable artifact deltas |
| Authority | Domain claim remains domain-owned |
| Primary metric | Frontier progression / rework |
| Release priority | P0 |
| Doc state | WORKING |

## Development Ladder

```mermaid
flowchart LR
    C[Concept] --> R[Relation]
    R --> G[Geometry / Behaviour]
    G --> D[Dimension / State]
    D --> T[Detail / Implementation]
    T --> P[Performance / Operation]
    P --> V[Verification / Validation]
```

Not every domain follows the same literal ladder; this is a resolution view, not a universal stage model.

## Feature Nodes

- DEV-F01 Maturity Gap
- DEV-F02 Next Development Frontier
- DEV-F03 Resolution Ladder
- DEV-F04 Professional Depth
- DEV-F05 Intent Check
- DEV-F06 Low-resolution Warning
- DEV-F07 Development Action
- DEV-F08 Domain Adapter Binding
- DEV-F09 Return-to-Whole Check

## Domain Binding

```mermaid
flowchart TD
    D[Development Frontier] --> A{Domain process available?}
    A -- Yes --> P[Bind domain-native process]
    P --> N[Native output]
    N --> R[Readback]
    A -- OPEN --> B[Bounded exploration]
    B --> H[Professional claim HOLD]
```

## Acceptance

A development action specifies target relation, intended improvement, artifact target, readback method and domain owner when relevant.

## Guardrail

Professional depth cannot be inferred from document count or visual finish.\n\n## Atomic Children

```mermaid
flowchart TB
    P[N03B DEVELOP]
    P --> N03B1[N03B1 MATURITY GAP]
    P --> N03B2[N03B2 DEVELOPMENT FRONTIER]
    P --> N03B3[N03B3 DOMAIN ADAPTER]
    P --> N03B4[N03B4 INTENT CHECK]
```

- [N03B1｜MATURITY GAP](atomic/N03B1_MATURITY_GAP.md)
- [N03B2｜DEVELOPMENT FRONTIER](atomic/N03B2_DEVELOPMENT_FRONTIER.md)
- [N03B3｜DOMAIN ADAPTER](atomic/N03B3_DOMAIN_ADAPTER.md)
- [N03B4｜INTENT CHECK](atomic/N03B4_INTENT_CHECK.md)
