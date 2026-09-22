# OLEANDER Enterprise Phase 1 ? Kernel + Reconciliation v0.1

Status: **EV2 candidate / read-only / non-authoritative**

Phase 1 does not add another ERP product or runtime layer. It introduces a minimal enterprise kernel and a derived reconciliation decision over the already validated v0.3.1 enterprise projection.

## Scope

Active Phase-1 modules:

`ERP + PLM + BPM + QMS`

Deferred without semantic expansion in this phase:

`MES + MBSE + Knowledge Graph + Agent Runtime`

The deferred modules remain available through v0.3.1 but are not allowed to expand the Phase-1 kernel contract.

## Kernel primitives

The stable kernel vocabulary is deliberately small:

`Identity -> Authority Binding -> State Fact -> Relation -> Work -> Configuration -> Evidence -> Change -> Readback -> Receipt -> Reconciliation`

None of these primitives is a new system of record. Every object carries source references and remains rebuildable.

### Identity
Points to an existing canonical/project/artifact/review/configuration identity. It never manufactures authority.

### Authority Binding
Names the existing owner that already controls a subject/scope. Every kernel binding has `authority_gain=false`.

### State Fact
Represents one orthogonal state family. Project, job, professional, quality, configuration, process and other state families are not collapsed into one universal status.

### Relation
Typed and source-bound. `authority_effect=NONE` is mandatory.

### Work
Projects existing Work Package / Job / BPM process/handoff/exception semantics. Work completion does not grant Design KEEP or Promotion.

### Configuration
Projects PLM version/baseline/release state. `RELEASED` remains configuration identity only.

### Evidence
Projects review/inspection/readback evidence with explicit claim ceiling.

### Change
Projects affected refs, reopen refs and readback requirements. Change cannot close itself.

### Readback
Observed result only; readback is not acceptance.

### Receipt
Source-bound execution/review/quality result at a bounded claim ceiling.

## Reconciliation decision

Reconciliation answers only a coordination question:

`Can the observed Phase-1 state advance without violating an existing blocking authority?`

Output:

- `advance_decision = ALLOW | HOLD | NOT_EVALUATED`
- concrete `blocking_conditions`
- `reopen_set`
- `rerun_set`
- `review_set`
- `required_readback_set`
- `unresolved_authority_conflicts`
- bounded `claim_ceiling`

Every blocker carries its existing `blocking_authority_ref`. The reconciliation engine is **not** that authority.

`ALLOW` is legal only when all blockers and required action sets are empty. Even then, ALLOW means only **Phase-1 coordination clear within observed scope**. It does not mean Design KEEP, Professional PASS, approval, acceptance or Project Promotion.

## Phase-1 fail-closed rules

- stale projection source -> HOLD;
- blocked Work Package / BPM process / open exception -> HOLD;
- Design REVISE / REJECT / HOLD / FAIL -> HOLD;
- open QMS NCR/CAPA -> HOLD;
- QMS inspection REVISE / HOLD / FAIL -> HOLD;
- PLM `IMPLEMENTED_READBACK_PENDING` -> HOLD + required readback;
- unresolved blocking digital-thread relation -> HOLD;
- unresolved authority conflict -> HOLD;
- PLM RELEASED and BPM COMPLETED cannot override a Design/QMS blocker.

## Module projection onto kernel

### ERP
Projects demand/schedule/resource states into `Identity + State Fact + Work + Relation`. ERP remains a planning/coordination view.

### PLM
Projects configuration items and change records into `Configuration + Change + State Fact + Readback requirement`. PLM release never becomes acceptance.

### BPM
Projects process instances, handoffs and exceptions into `Work + State Fact + Relation + Readback`. BPM completion cannot close professional stages.

### QMS
Projects NCR/CAPA/inspection into `Evidence + State Fact + Relation + Readback + Receipt`. CAPA effectiveness and inspection evidence remain explicit.

## Current boundary

Phase 1 adds no R-L, no project axis, no persistent event ledger, no distributed transaction manager, no new knowledge authority, and no autonomous mutation path.

Real-project proof remains open until C01, C04 and Fallingwater/3D are run as EV3 stress cases.
