# N08B｜SOURCE / EVIDENCE

[← Parent](../N08_KNOWLEDGE.md) · [← Atomic Node Index](../ATOMIC_NODE_INDEX.md)

| Field | Value |
|---|---|
| Node ID | N08B |
| Parent | N08 KNOWLEDGE |
| Type | Atomic Knowledge Node |
| Product job | 保存来源类别、provenance、freshness、authority context 与证据强度 |
| Inputs | Source; Observation/report |
| Outputs | Evidence object |
| Authority | Source authority depends on provenance/context |
| Primary metric | Evidence Provenance Completeness |
| Release priority | P0 |
| Doc state | WORKING |

## Context Graph

```mermaid
flowchart LR
    I0[Source] --> N[N08B SOURCE / EVIDENCE]
    I1[Observation/report] --> N[N08B SOURCE / EVIDENCE]
    N --> O0[Evidence object]
```

## Product Contract

Source existence ≠ applicability；Evidence 必须保留 source_class/date/context/creator/strength。Precedent、expert judgment、AI inference 与 project fact 不得因“看起来可信”而互相升级。

## Source Classes

```text
NORMATIVE
EMPIRICAL
USER_RESEARCH
PROJECT_FACT
OBSERVATION
SIMULATION
PRECEDENT
EXPERT_JUDGMENT
INFERENCE
```

Source Class 描述来源在当前设计判断中的语义角色，不自动决定最终 applicability 或 authority。

## Requirement Links

- `KNW-F02`
- `KNW-F03`

## Acceptance

1. primary/secondary、direct/indirect 可区分
2. freshness 可见
3. provenance 可追踪
4. source class 与 project-truth authority 分开
5. precedent / inference 不直接成为 Project Fact

## Failure / Degraded Behaviour

- source unavailable → evidence unverified, not deleted

## Events / Metrics

- `evidence_linked`
- `evidence_freshness_changed`

## Relations

- Feeds N08C/N08D/N06E/N07D
