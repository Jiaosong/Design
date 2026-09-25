# N06｜ARTIFACTS

[← Node Graph](README.md)

| Field | Value |
|---|---|
| Node ID | N06 |
| Children | N06A, N06B, N06C, N06D, N06E, N06F — see [Atomic Children](#atomic-children) |
| Type | Product Surface |
| Product job | 维护真实可编辑 artifact 的 identity、role、revision、fidelity 与 readback |
| Inputs | Design action, native source, external authoring result |
| Outputs | Artifact revision + actual readback |
| Authority | Native/source authority remains owner-native |
| Primary metric | Readback Completion / Revision Integrity |
| Release priority | P0 |
| Doc state | WORKING |

## Artifact Truth Chain

```mermaid
flowchart LR
    Q[Question] --> A[Artifact logical object]
    A --> R1[Revision n]
    R1 --> RB1[Readback n]
    RB1 --> F[Finding / Decision]
    F --> R2[Revision n+1]
    R2 --> RB2[Readback n+1]
```

## Artifact Roles

```mermaid
mindmap
  root((Artifact Role))
    Native_Design_Source
    Working_Source
    Canonical_Derivative
    Export
    Preview
    Prototype
    Simulation
    Reference
    AI_Visual
    Snapshot
```

## Feature Nodes

ART-F01–F12: Register, Role, Native Link, Revision, Relation Binding, Question Binding, Readback, Cross-version Compare, Fidelity/Claim Ceiling, Content Binding, Stale Warning, Degraded Substitute.

## Hard Distinction

```text
FILE EXISTS
≠ CURRENT ARTIFACT
≠ READ
≠ VALID
≠ DESIGN KEEP
≠ PROFESSIONAL PASS
```

## Acceptance

Any material mutation that contributes to a completion/validation claim must bind the intended revision and actual readback.\n\n## Atomic Children

```mermaid
flowchart TB
    P[N06 ARTIFACTS]
    P --> N06A[N06A ARTIFACT IDENTITY]
    P --> N06B[N06B ARTIFACT ROLE]
    P --> N06C[N06C REVISION IDENTITY]
    P --> N06D[N06D READBACK]
    P --> N06E[N06E FIDELITY / CLAIM CEILING]
    P --> N06F[N06F DEGRADED SUBSTITUTE]
```

- [N06A｜ARTIFACT IDENTITY](atomic/N06A_ARTIFACT_IDENTITY.md)
- [N06B｜ARTIFACT ROLE](atomic/N06B_ARTIFACT_ROLE.md)
- [N06C｜REVISION IDENTITY](atomic/N06C_REVISION_IDENTITY.md)
- [N06D｜READBACK](atomic/N06D_READBACK.md)
- [N06E｜FIDELITY / CLAIM CEILING](atomic/N06E_FIDELITY_CLAIM_CEILING.md)
- [N06F｜DEGRADED SUBSTITUTE](atomic/N06F_DEGRADED_SUBSTITUTE.md)
