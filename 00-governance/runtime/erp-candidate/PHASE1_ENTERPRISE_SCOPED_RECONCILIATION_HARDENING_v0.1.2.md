# OLEANDER Enterprise Phase-1 Scoped Reconciliation Hardening v0.1.2

Status: `EV2 CANDIDATE / NON-AUTHORITATIVE / NO CURRENT PROMOTION`

This successor repairs two defects exposed by real-project EV3 stress testing without adding a second architecture, authority, runtime layer, write path, or project taxonomy.

## Repair A — claim-scoped state facts

`STATE_FACT` keeps the existing orthogonal state family and now carries an optional `claim_scope`.

Examples:

- `TOP_LEVEL:QUALITY`
- `QMS_INSPECTION:REVIEW_READBACK`
- `QMS_INSPECTION:COMMISSIONING`
- `QMS_INSPECTION:TECHNICAL`
- `REVIEW:DESIGN`
- `BPM_PROCESS_INSTANCE`
- `PLM_CONFIGURATION_ITEM`

Reconciliation may materialize `CROSS_CARRIER_CONTRADICTION` only when facts share the same subject, state family, and claim scope. A local machine/configuration PASS and a professional/operational HOLD are therefore allowed to coexist without being mislabeled as contradictory. Every `EXPLICIT` blocking fact remains fail-closed regardless of whether it participates in a contradiction.

## Repair B — unresolved-authority root dedup

Unresolved authority requirements are grouped by:

`subject_ref + required_owner_kind + authority_contract_ref + scope`

Every triggering blocker/action remains in sorted unique `trigger_refs`; compatibility `trigger_ref` is the deterministic first trigger. This reduces duplicate owner requests without hiding causality.

## Real-project stress readback

The same projection → kernel → reconciliation pipeline was run against:

- C01 R1.7/detail-design/downstream local-current sources.
- C04 exact-main project-control sources.
- Fallingwater V06 local diagnostics and current native `.blend` bytes.

Observed results after repair:

- C01: `HOLD`, contradiction count `0`, unresolved authority requirements `10`.
- C04: `HOLD`, contradiction count `0`, unresolved authority requirements `12`.
- Fallingwater: `SOURCE_READBACK_STALE / DIVERGED / HOLD`, contradiction count `0`, unresolved authority requirements `13`.

The Fallingwater historical save/reopen receipt records native SHA `8AA493897A603154568ECAEAD85B50A3394C421F1361609BF1968B2326053D9B`, while the current local native is `9665818312055D42EA5B5D12877E3DA0DD71953A29F8EA386482E5BC58E59EF8`. The old integrity/furniture PASS is therefore invalid for the current native. The current runtime has neither `blender.exe` nor Python `bpy`; v0.1.2 emits an explicit invalidation receipt and requires a fresh Blender save/reopen + furniture/use audit instead of fabricating a new PASS.

## Boundaries

This repair does not prove Current adoption, enterprise completeness, real-case generalization, Design KEEP, Professional PASS, engineering approval, statutory approval, field truth, or Project Promotion. EV4 independent review remains open.
