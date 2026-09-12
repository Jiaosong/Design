# G1 R3.3｜Exact-B Interface Confirmation Decision｜2026-08-14

## Decision State

`INTERFACE_RELATION_CORRECTION_CONFIRMED / WORKING_SOURCE / OVERALL_DESIGN_REVISE / CANDIDATE_PROMOTION_NOT_RUN`

The exact `R3.2-B-CORE-RECOVERY` relation is confirmed as the current interface-relation correction for the v0.13 Working Source line.

This closes the **interface-basin relation correction question only**. It does not close the whole G1 design because the separate `RIGHT / FRONT TERMINATION` defect remains open. It is not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Confirmed Source Relation

`INTERFACE_DECK_BOUNDARY`:

- `u_center = 0.62`
- `u_halfspan = 0.26`
- `theta_center = TOP_MERIDIAN`
- `theta_halfspan_rad = 1.06`
- `core_fraction = 0.29`
- `depth_m = 0.012`
- `blend = QUINTIC_SMOOTHERSTEP`

All other sparse Source families remain unchanged.

## Confirmation Evidence

Final widened-context confirmation head:

`c89671f0d08676baa9ce1d6349fa5575643244b2`

Workflow:

- `OLEANDER Modeling Worker v0.13 R3.3 Interface Confirmation`
- run `31798888828`
- result `SUCCESS`

Artifact:

- ID `9218552994`
- name `oleander-modeling-worker-v0-13-g1-r3-3-31798888828`
- SHA-256 `e436809136169acd9ad0da5c4b026ad3ff20be6fabc09dd6d27dc10642283ff5`
- size `5,377,748 bytes`

The previous 120 mm local confirmation view is retained as valid execution evidence but was declared insufficient for judging the whole basin boundary. The Source was not changed. The local diagnostic view alone was widened to 90 mm with greater camera distance, then the exact B relation was re-run.

## Machine QA

All existing R2 Machine checks pass.

Dimensions:

- length `0.1899999976158142 m`
- width `0.08076061552995034 m`
- height `0.09961299177072028 m`

Interface:

- depth `0.011999999999999997 m`
- outer continuity `0.22060952481854423°`
- core continuity `0.36396264549786866°`

The derived geometry remains non-authoritative execution geometry.

## Interior Transition Fairness

The R3 working interior-fairness gate passes:

- samples `1,823`
- max longitudinal normal turn `7.157782125831815° / 0.01u`
- p95 longitudinal `5.9686253060936885° / 0.01u`
- max circumferential normal turn `11.878303134600172° / 0.05rad`
- p95 circumferential `9.31495442131651° / 0.05rad`
- max combined turn score `12.093808946278138`
- p95 combined score `9.812295564579093`

This is a working design diagnostic gate, not a universal Class-A criterion.

## Source / Runtime Authority Checks

The final confirmation verifies:

- exact selected B relation used;
- `TOP_MERIDIAN` semantic preserved;
- only `INTERFACE_DECK_BOUNDARY` changed during the reversible experiment;
- Machine QA pass;
- interior-fairness pass;
- shared Blender Surface System v1.20.0 runtime verified;
- local camera created through the shared Surface System runtime;
- R2 reference and B confirmation meshes remain `DERIVED_EXECUTION_NOT_AUTHORITY`;
- Blender-native Working Source restored after the confirmation experiment;
- all HERO and local Strip / Grazing / Zebra outputs written;
- Candidate Promotion remains `NOT_RUN`.

## Global + Local Visual Decision

### STRIP

R2 presents a visually explicit recessed basin, but the apparent definition is coupled to a compressed ring / trough around the interface transition. B removes the concentrated ring and replaces it with a continuous transition. In the widened local context, the interface still reads as a localized recessed field rather than disappearing into the entire palm surface.

### GRAZING

R2 shows a strong dark annular compression and a pinched right-transition response. B retains a distinguishable local depression while distributing the grazing response more continuously across the transition. The basin remains subordinate to the larger palm volume, which is the intended hierarchy.

### ZEBRA

R2 contains multiple tightly packed and sharply turning bands around the interface. B reduces those bands to a materially simpler and more continuous normal-field reading. The local field remains identifiable without recreating the R2 concentric compression.

## Decision

Confirmed classification:

`INTERFACE_RELATION_CORRECTION_CONFIRMED`

Reasoning:

1. R2 topology isolation established that the defect was not primarily tessellation-driven.
2. R3 proved that a severe fairness correction can over-distribute the basin and destroy hierarchy.
3. R3.1 proved that longitudinal micro-tuning alone cannot solve that hierarchy problem.
4. R3.2 recovered the relation balance by reopening angular field and core fraction, selecting B over A/C.
5. R3.3 repeats the exact B relation without tuning and confirms it under both global and contextual local Strip / Grazing / Zebra diagnostics.
6. The severe interface-right compression is removed while the basin remains a legible secondary recessed field.

Therefore no further interface-relation tuning is justified at this stage.

## Next Legal Action

Move to the separate open defect:

`RIGHT / FRONT TERMINATION → termination-specific source-space diagnostic → determine Source relation ownership → bounded Source-level correction only if evidence supports it`

Do **not** reopen the confirmed interface relation unless the termination correction later creates a measured or visible regression in that region.

## Authority Boundary

Current project state after this decision:

- `INTERFACE RELATION QUESTION = CONFIRMED / CLOSED FOR CURRENT WORKING SOURCE`
- `RIGHT / FRONT TERMINATION = OPEN`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current `PROMOTED / CANONICAL_AUTHORITY / SYNCED / NOT RELEASED`

No Promotion is authorized by this receipt.
