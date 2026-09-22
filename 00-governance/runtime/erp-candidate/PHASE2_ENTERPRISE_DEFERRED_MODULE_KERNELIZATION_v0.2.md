# OLEANDER Enterprise Phase-2 Deferred-Module Kernelization v0.2

Status: `CANDIDATE / NON-AUTHORITATIVE / NO CURRENT PROMOTION`

Phase 2 extends the existing Enterprise Kernel; it does not create a second ERP/PLM/MES/QMS/MBSE platform, database, runtime layer, authority chain or universal state machine.

## Scope

Phase 1 already kernelized ERP / PLM / BPM / QMS. Phase 2 brings the four previously deferred modules into the same kernel/reconciliation path:

- MES → operation work, execution state, resource/input/output relations and actual readback.
- MBSE → requirement, system element, interface, verification and validation as distinct claim scopes.
- Knowledge Graph → source-bound identities, typed relations and provenance only; authority effect remains `NONE`.
- Agent Runtime → session, lease, action, handoff and side-effect readback; success never grants authority.

The combined candidate therefore exposes eight module bindings while retaining the same lower-level primitives: Identity, Authority Binding, State Fact, Relation, Work, Configuration, Evidence, Change, Readback, Receipt and Reconciliation.

## New fail-closed gates

- `MES_READBACK_MISSING`: `COMPLETE` cannot clear without observed actual readback.
- `MBSE_VERIFICATION_INCOMPLETE`: Verification is an independent evidence gate.
- `MBSE_VALIDATION_INCOMPLETE`: Validation is distinct from Verification and cannot be inferred from it.
- `AGENT_SIDE_EFFECT_UNCERTAIN`: uncertain mutation effects require recovery/readback even when the session succeeded.
- `AGENT_LEASE_CONFLICT`: lease conflict independently blocks mutation/advance.

Knowledge Graph does not add an authority blocker because the graph cannot own authority in the first place; all graph relations remain `projection_only=true` and `authority_effect=NONE`.

## Real-project stress

Fresh-source exercises use the existing C01, C04 and Fallingwater adapters, rebuild the v0.3.1 projection, then run Kernel v0.2 and Reconciliation v0.2.

- C01: MES digital execution has observed readback, therefore no MES false blocker; MBSE Validation remains open and correctly HOLDS.
- C04: MBSE Verification and Validation remain open; MES is legitimately not triggered; project remains HOLD.
- Fallingwater: stale/diverged native evidence remains HOLD; MBSE Validation remains open; no P2 Project authority is synthesized.

## Boundaries

Phase 2 does not prove physical fabrication/installation acceptance, Systems Engineering Current authority, Knowledge Current, agent mutation authority, Design KEEP, Professional PASS, statutory approval or Project Promotion. Independent EV4 review remains required before any promotion-ready integration candidate.
