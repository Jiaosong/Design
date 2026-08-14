# G1 R3｜Interior Fairness Visual Decision｜2026-08-14

## Decision State

`R3-V3-BALANCED-SPAN = MACHINE_PASS / INTERIOR_FAIRNESS_PASS / VISUAL_REVISE / WORKING_SOURCE / CANDIDATE_PROMOTION_NOT_RUN`

This receipt records the separate visual decision after the R3 interior-transition fairness gate selected `R3-V3-BALANCED-SPAN` and the variant was executed through the Blender-native Working Source plus the shared `OLEANDER Blender Surface System v1.20.0 / F1_DESIGN_VALIDATION` runtime.

This is a design-routing decision only. It is not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Evidence Identity

Execution head:

`1a7429b71e2a3353eb53c4db039c23324bf78acf`

R3 workflow:

- `OLEANDER Modeling Worker v0.13 R3 Interface Fairness`
- run `31796247645`
- result `SUCCESS`

R3 artifact:

- artifact ID `9217526622`
- name `oleander-modeling-worker-v0-13-g1-r3-interface-31796247645`
- SHA-256 `3f8750a055b5cc58d29cbab6500f9eee4a6f8ec9635ba4d53612aadb0568c28e`
- size `1,484,440 bytes`

The artifact contains the R3 machine report, three Working Source experiment snapshots, fixed-rig R2/R3 Strip-Grazing-Zebra pairs, the R3 visual report, and the saved R2 Blender-native Working Source baseline used for the reversible experiment.

## R3 Machine / Fairness Result

The R2 baseline reproduces the previously isolated interior transition failure:

- max longitudinal normal turn: `28.139737436965273° / 0.01u`
- p95 longitudinal normal turn: `21.397529653022982° / 0.01u`
- max circumferential normal turn: `51.371223160266915° / 0.05rad`
- p95 circumferential normal turn: `34.743378938468396° / 0.05rad`
- max combined score: `52.04278990738308`

All three R3 variants retain the existing R2 Machine QA. Only `R3-V3-BALANCED-SPAN` clears the new working interior fairness gate.

`R3-V3-BALANCED-SPAN`:

- `u_halfspan: 0.18 → 0.24`
- `theta_halfspan_rad: 0.76 → 1.16`
- `core_fraction: 0.50 → 0.25`
- `depth_m: 0.012 → 0.012` (preserved)
- max longitudinal: `7.230559753154585° / 0.01u`
- p95 longitudinal: `5.774716410344036° / 0.01u`
- max circumferential: `8.348954975171377° / 0.05rad`
- p95 circumferential: `7.087252686879561° / 0.05rad`
- max combined score: `8.792850241024752`

Therefore R3-V3 is a valid Machine+Fairness visual candidate. That status does not by itself make it a valid design correction.

## Source Authority / Reversibility

The Blender visual experiment changed only `INTERFACE_DECK_BOUNDARY`.

Source-family differences from the R2 baseline:

- `GRIP_AXIS = 0.0`
- `PALM_PROFILE = 0.0`
- `THUMB_SIDE_PLAN = 0.0`
- `OPPOSITE_SIDE_PLAN = 0.0`
- `LOWER_RETURN_PROFILE = 0.0`
- `INTERFACE_DECK_BOUNDARY = 0.3999999999999999`

The R3 source edit was applied through the Blender-native source object, rendered, then restored. The post-experiment Source digest/readback returned to the R2 baseline. Both R2 reference and R3 candidate render meshes remained `DERIVED_EXECUTION_NOT_AUTHORITY`.

## Fixed-Rig Visual Review

### STRIP

The previous concentrated interface-right reflection hook is substantially reduced. However, the transition is distributed so broadly that the recessed interface basin loses a clear visual edge and reads as a long, shallow top deformation rather than a distinct secondary basin.

### GRAZING

The severe high-contrast ring compression seen around the R2 basin is removed, but the R3 field becomes over-diffuse. The top interface no longer maintains enough separation from the global palm volume. The intended hierarchy `palm volume > interface basin > lower return` is therefore weakened even though the normal field is fairer.

### ZEBRA

The dense concentric compression around the R2 interface is materially simplified, confirming that the fairness correction is real. At the same time, the transition occupies too much of the top field and the interface loses local definition. The right/front termination pattern remains present and is not solved by this experiment.

## Decision

`R3-V3-BALANCED-SPAN` is **not accepted as the current Source correction**.

Classification:

`MACHINE_FAIRNESS_PASS_VISUAL_OVERDISTRIBUTED_REVISE`

Reason:

1. The interior normal-field compression is strongly reduced.
2. The 12 mm depth and TOP_MERIDIAN semantic are preserved.
3. The improvement is achieved by expanding the transition field too aggressively.
4. Basin readability and local interface definition degrade under Strip and Grazing diagnostics.
5. Therefore minimizing normal-turn alone is not a valid optimization objective for OLEANDER surface design.

## QA / Selection Lesson

The first R3 selector ranked eligible variants primarily by the lowest maximum combined normal-turn score. That can bias the system toward over-smoothing.

The next selector must use:

`Fairness Gate first → then minimum legal Source-relation change → then fixed-rig visual review`

not:

`lowest normal-turn score wins`.

This preserves the design relationship while still closing the machine-detected defect.

## Next Legal Action

`R3.1 minimum-change boundary search`

Keep fixed:

- `theta_halfspan_rad = 1.16`
- `core_fraction = 0.25`
- `depth_m = 0.012`
- `theta_center = TOP_MERIDIAN`

Run a narrow professional batch near the R3-V2 / R3-V3 fairness boundary using only `u_halfspan` as the active Source variable. Render every Machine+Fairness PASS variant under the same HERO / Strip / Grazing / Zebra setup before selecting a visual direction.

The right/front termination defect remains a separate open issue and must not be folded into this interface correction.

## Authority Boundary

Current state after this visual decision:

- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains the current promoted canonical authority.

No Promotion is authorized by this receipt.
