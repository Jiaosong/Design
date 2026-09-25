# N10A｜RESUME / RECOVER

[← Session Kernel](N10_SESSION_KERNEL.md)

| Field | Value |
|---|---|
| Node ID | N10A |
| Parent | N10 |
| Type | Kernel Node |
| Product job | 从 owner-native carriers 重建 verified working frontier |
| Inputs | explicit project/task/object key, Current, Control Card, checkpoint, artifact/readback |
| Outputs | verified session projection |
| Authority | Read/resolve only; no new project truth |
| Primary metric | Resume Accuracy / VPCR |
| Release priority | P0 |
| Doc state | WORKING |

## Resume Precedence

```mermaid
flowchart TD
    K[Explicit project/task/object key] --> P[Current Project / Task]
    P --> C[Control Card]
    C --> E[Execution Receipt / Checkpoint]
    E --> A[Native Artifact + Readback]
    A --> S[Ephemeral Session Projection]
    M[Chat Memory] -.support only.-> S
```

## Resume Sequence

```mermaid
sequenceDiagram
    participant U as Human
    participant K as Kernel
    participant C as Current carriers
    participant A as Artifact/Readback
    U->>K: 继续 / resume
    K->>C: resolve project frontier
    C-->>K: current identity + checkpoint
    K->>A: resolve exact artifact/readback
    A-->>K: revision + result
    K-->>U: verified Current Question / Frontier / Next Action
```

## Requirements

- explicit key > owner-native Current > checkpoint > artifact/readback;
- chat memory never outranks Current;
- source conflict remains visible;
- stale checkpoint cannot authorize write;
- missing optional carrier narrows confidence rather than inventing state.

## Acceptance

A fresh session reconstructs the same material frontier without requiring user to restate already valid project context.

## Failure

If verified recovery is impossible, return `RESUME_PARTIAL / HOLD_MUTATION` with exact missing carrier(s).

## Events

`project_resume_started` · `frontier_resolved` · `resume_degraded` · `resume_corrected_by_user`
