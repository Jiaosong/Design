# C04｜QJ-C｜Spatial + Experience Working Pack v2.0

- Date: 2026-08-14
- Scope: `QJ-C19｜Cross-line State Contract Consolidation`
- State: `C HANDOFF CONTRACT / OWNER CONFIRMATION PENDING / FIELD OPEN`
- Field: `FIELD OBSERVED = 0 / FIELD MEASURED = 0`
- Promotion: `NO`

## Purpose
This does not add a new experience method. It converts existing C06/C07/C17 failure, service and route logic into shared handoff fields.

Core separation:
`Experience State != Reality/Operation State != Delivery Modifier`.

## Axis A — Experience State
`MOVE / RECOVER / OBSERVE / READ / WITHDRAW / RETURN`

- MOVE: preserve route continuity.
- RECOVER: body/attention recovery; content degrades.
- OBSERVE: real object / landscape first.
- READ: explanation only when real stimulus exists.
- WITHDRAW: design intentionally recedes; Landscape / Body / Safety take over.
- RETURN: return/exit responsibility becomes first priority.

## Axis B — Reality / Operation State
`NORMAL / DEGRADED / CLOSED / UNKNOWN`

- NORMAL: current known operation can use the intended design logic; not Field Verified.
- DEGRADED: optional depth closes first; Safety / Route / Return remain.
- CLOSED: object/segment/function unavailable; bypass/reroute/exit required.
- UNKNOWN: formal state not confirmed; never render as NORMAL/OPEN.

## Axis C — Delivery Modifier
`NONE / OFFLINE / RETURN-PRIORITY`

- OFFLINE: Digital connectivity cannot be required; Physical / Paper / Human retain Route / Safety / Return / core observation.
- RETURN-PRIORITY: close new Deep Read / Memory entries; elevate Return / Service / Direction.
- OFFLINE and RETURN-PRIORITY may coexist.

## Non-equivalence rules
1. `WITHDRAW != CLOSED`.
2. `OFFLINE != DEGRADED`.
3. `UNKNOWN != NORMAL`.
4. `RETURN-PRIORITY` may overlay NORMAL / DEGRADED / UNKNOWN.
5. Visual/Digital prototype PASS does not change Reality State.

## Minimum transition examples
- Network loss: `OBSERVE + NORMAL + OFFLINE`.
- Rain/wet condition: `MOVE|RECOVER + DEGRADED + NONE`; exact closure conditions remain A-owned.
- Segment closure: `RETURN + CLOSED + RETURN-PRIORITY`.
- Status not confirmed: `MOVE + UNKNOWN + NONE`; no positive OPEN claim.
- Return pressure: any experience state → `RETURN + current reality + RETURN-PRIORITY`.
- Natural closure / R13 candidate: `WITHDRAW + current reality + NONE`; interpretation/Hero/strong Brand withdraw; Safety/Direction may remain.

## D handoff
Owner confirmation required:
- visual system can express experience_state and reality_state together;
- UNKNOWN never uses positive NORMAL/OPEN semantics;
- WITHDRAW lowers Brand / Content / decorative presence;
- Safety / Return may outrank brand.

`D CONFIRMATION PENDING`.

## E handoff
Owner confirmation required:
- data model carries `experience_state / reality_state / delivery_modifier`;
- OFFLINE and RETURN-PRIORITY can overlay independently;
- UNKNOWN is fail-closed;
- complete Digital OFF does not break Route / Safety / Return / core observation.

`E-R1 / E-R2 = CONFIRMATION PENDING`.

## F handoff
Minimum cross-media fields:
`route_segment / experience_state / reality_state / delivery_modifier / reading_mode / evidence_state / open_hold / owner`.

F must consume:
- C17 M0–M7 Macro Route Contract;
- C18 governance correction;
- C19 state contract.

## B lane implication
B stays inside `PRJ-C04-EXPERIENCE-SPATIAL`, not a new P3.

Minimum B-lane fields:
`FULL|LIGHT|OFF / do-not-use condition / route_segment / experience_state / claim_type / source / evidence_state`.

## Gate
`C19 CONTRACT = READY FOR OWNER CONFIRMATION`.

Not closed:
- D implementation;
- E implementation / Digital-OFF receipt;
- B-lane content objects;
- F cross-media artifact;
- any A/G1F Reality claim.

`FIELD OBSERVED = 0 / FIELD MEASURED = 0 / PROMOTION = NO`.
