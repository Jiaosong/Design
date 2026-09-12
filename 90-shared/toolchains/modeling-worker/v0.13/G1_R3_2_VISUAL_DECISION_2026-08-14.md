# G1 R3.2｜Angular-Field / Core-Recovery Visual Decision｜2026-08-14

## Decision State

`R3.2-B-CORE-RECOVERY = WORKING_SOURCE_DIRECTION_SELECTED / MACHINE_PASS / INTERIOR_FAIRNESS_PASS / VISUAL_DIRECTION_PASS / CANDIDATE_PROMOTION_NOT_RUN`

This receipt records the design-direction decision after R3.2 re-opened the angular field and interface core fraction following the R3.1 one-dimensional longitudinal-search rejection.

This decision selects a **Working Source direction for confirmation**. It is not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Evidence Identity

Execution head:

`0dfb94c559f41d325a329753c94b02c52e9f613c`

Workflow:

- `OLEANDER Modeling Worker v0.13 R3.2 Relation Recovery Batch`
- run `31797721129`
- result `SUCCESS`

Artifact:

- artifact ID `9218083899`
- name `oleander-modeling-worker-v0-13-g1-r3-2-31797721129`
- SHA-256 `116e21cfad0e227e8f4d8ca3e9f3b176604cf30fabe9d547842ce4ee0eb95033`
- size `2,702,466 bytes`

The first R3.2 execution correctly blocked `R3.2-C-DEFINED-CORE` before rendering because its initial relation pushed overall height below the existing Machine gate. The gate was not relaxed. C was revised to remain inside the existing dimensional authority boundary, after which the full batch was re-executed successfully.

## Professional Batch

All three final variants:

- modify only `INTERFACE_DECK_BOUNDARY`;
- keep `theta_center = TOP_MERIDIAN`;
- keep `depth_m = 0.012`;
- preserve all other Source families;
- pass existing R2 Machine QA;
- pass the R3 working interior-transition fairness gate;
- remain reversible `WORKING_SOURCE` experiments;
- render only derived `DERIVED_EXECUTION_NOT_AUTHORITY` meshes.

### A｜R3.2-A-COMPACT-ANGULAR

Source relation:

- `u_halfspan = 0.25`
- `theta_halfspan_rad = 1.04`
- `core_fraction = 0.25`
- `depth_m = 0.012`

Machine / fairness:

- overall height = `0.1006801329985445 m`
- relation-change cost = `1.257309941520468`
- max longitudinal = `6.8807152349250496° / 0.01u`
- p95 longitudinal = `5.78720886957386° / 0.01u`
- max circumferential = `11.327059485364474° / 0.05rad`
- p95 circumferential = `8.99583254039181° / 0.05rad`
- max combined = `11.50217932802786`

Visual reading:

- smallest aggregate visual departure from R2;
- compressed R2 reflection ring is removed;
- angular footprint is compact relative to R3.1;
- however, the recessed interface remains too weakly differentiated from the palm volume under Strip / Grazing.

Decision: `RETAIN AS LOWER-CHANGE REFERENCE / NOT SELECTED`.

### B｜R3.2-B-CORE-RECOVERY

Source relation:

- `u_halfspan = 0.26`
- `theta_halfspan_rad = 1.06`
- `core_fraction = 0.29`
- `depth_m = 0.012`

Machine / fairness:

- overall height = `0.09961299137430771 m`
- relation-change cost = `1.2591812865497078`
- max longitudinal = `7.157781925787901° / 0.01u`
- p95 longitudinal = `5.9686250880495075° / 0.01u`
- max circumferential = `11.878303442714293° / 0.05rad`
- p95 circumferential = `9.314954521152911° / 0.05rad`
- max combined = `12.09380929196481`

Visual reading:

- the severe R2 interior reflection compression remains removed;
- compared with A, the larger core recovers more local interface definition;
- compared with C, the right-transition highlight remains less concentrated and the design retains more machine margin;
- under Zebra the top field is simplified without recreating the R2 concentric compression;
- the basin remains subordinate to the palm volume rather than disappearing into it.

Decision: `WORKING_SOURCE_DIRECTION_SELECTED_FOR_CONFIRMATION`.

### C｜R3.2-C-DEFINED-CORE

Final source relation:

- `u_halfspan = 0.26`
- `theta_halfspan_rad = 1.09`
- `core_fraction = 0.30`
- `depth_m = 0.012`

Machine / fairness:

- overall height = `0.09952905860984601 m`
- relation-change cost = `1.2786549707602342`
- max longitudinal = `7.22625973161154° / 0.01u`
- p95 longitudinal = `5.994006095733598° / 0.01u`
- max circumferential = `11.252542922446677° / 0.05rad`
- p95 circumferential = `9.024542388978439° / 0.05rad`
- max combined = `11.51233400661922`

Visual reading:

- core definition is stronger than A;
- the right transition becomes more optically concentrated than B;
- overall height and p95 longitudinal turn sit closer to their current working limits;
- the additional relation departure does not produce enough design benefit to justify selecting it over B.

Decision: `RETAIN AS UPPER-CORE REFERENCE / NOT SELECTED`.

## Design Decision

Selected direction:

`R3.2-B-CORE-RECOVERY`

Reasoning:

1. R2 proved that a strongly defined compact basin with the original relation produces unacceptable interior normal-field compression.
2. R3 / R3.1 proved that minimizing normal turn by spreading the transition too widely destroys the basin hierarchy.
3. R3.2-B sits between those failure modes: the interface is still legible as a secondary recessed field, but the severe compressed reflection ring is not restored.
4. B retains more margin than C against the current height and longitudinal-fairness boundaries while producing stronger interface definition than A.
5. Therefore the project now has a preferred **Working Source relation direction**, but not enough evidence to close Candidate Review or promote authority.

Classification:

`INTERFACE_RELATION_DIRECTION_RECOVERED_CONFIRMATION_REQUIRED`

## Next Legal Action

`R3.3 confirmation of B → localized interface close-up + fixed HERO Strip/Grazing/Zebra + termination-separated review`

R3.3 must:

- use the exact B relation without additional tuning as its primary confirmation input;
- preserve the R2 Source families and authority boundary;
- add a localized interface diagnostic view/crop so basin definition and right-transition fairness are judged directly rather than only through the global HERO view;
- keep the right/front termination defect explicitly separate;
- avoid new Source variables unless the confirmation itself fails.

If B passes confirmation, it may close the **interface-relation correction question** and return to Candidate Review. That still does not automatically authorize Candidate Promotion.

## Authority Boundary

Current state:

- `DESIGN STATE = REVISE / INTERFACE DIRECTION SELECTED`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- `RIGHT / FRONT TERMINATION = OPEN`
- v0.12 remains the current promoted canonical authority.

No Promotion is authorized by this receipt.
