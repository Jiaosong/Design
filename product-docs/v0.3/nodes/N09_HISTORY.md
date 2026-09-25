# N09｜HISTORY

[← Node Graph](README.md)

| Field | Value |
|---|---|
| Node ID | N09 |
| Type | Product Surface |
| Product job | 保存改变设计理解的重要历史，并支持 Resume / Handoff / Reopen |
| Inputs | decisions, reframes, revisions, findings, validation, frontier changes |
| Outputs | timeline, rationale, resume point, handoff pack |
| Authority | History preserves lineage; does not redefine Current by recency |
| Primary metric | Handoff correction / Resume success |
| Release priority | P1 |
| Doc state | WORKING |

## History Mindmap

```mermaid
mindmap
  root((HISTORY))
    Decision
      rationale
      accepted_cost
      reopen_condition
    Branch
      selected
      rejected_preserved
      reopened
    Reframe
      old
      new
      preserved
      invalidated
    Artifact
      meaningful_revision
      readback
    Continuity
      resume_point
      handoff
```

## What History Excludes

```text
file opened
agent started
routine save
tool success
formatting change
log noise
```

unless one materially changes design truth or recovery.

## Feature Nodes

HIS-F01–F09.

## Acceptance

History tells a future collaborator **why the design is here**, not merely **what the system did**.
