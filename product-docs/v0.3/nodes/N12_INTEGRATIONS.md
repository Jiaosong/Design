# N12｜INTEGRATIONS

[← Node Graph](README.md)

| Field | Value |
|---|---|
| Node ID | N12 |
| Type | Integration Node |
| Product job | 连接专业 authoring / analysis / storage / external systems，同时保持 artifact role、authority 与 degraded behaviour |
| Inputs | integration capability + scoped permission |
| Outputs | tool action / imported result / native locator |
| Authority | Connector availability does not grant project authority |
| Primary metric | integration success + truthful degradation |
| Release priority | P1/P2 |
| Doc state | WORKING |

## Integration Map

```mermaid
mindmap
  root((INTEGRATIONS))
    Authoring
      CAD_BIM
      Figma_UI
      3D
      IDE
    Analysis
      Simulation
      GIS
      Data
    Storage
      Local
      Drive
      Cloud
    External
      Publish
      Collaboration
      Delivery
```

## Interaction Contract

```mermaid
sequenceDiagram
    participant K as Kernel
    participant G as Mutation Guard
    participant I as Integration
    participant A as Native Artifact
    participant R as Readback
    K->>G: proposed tool action
    G-->>K: allow / hold
    K->>I: execute allowed action
    I->>A: actual tool/native change
    A-->>R: actual result
    R-->>K: readback
```

## Requirements

- least necessary tool scope;
- explicit external irreversible boundary;
- integration failure must report partial success truthfully;
- unavailable tool may use bounded substitute only when current question remains answerable;
- integration output role is explicit.

## Open

Security/privacy permission architecture remains required before broad external beta.
