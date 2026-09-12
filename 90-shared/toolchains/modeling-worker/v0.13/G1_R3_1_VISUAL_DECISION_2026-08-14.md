# G1 R3.1｜Minimum-Change Fairness-Boundary Visual Decision｜2026-08-14

## Decision State

`R3.1-V1-U231 / V2-U233 / V3-U235 = MACHINE_PASS / INTERIOR_FAIRNESS_PASS / VISUAL_REVISE / WORKING_SOURCE / CANDIDATE_PROMOTION_NOT_RUN`

This receipt records the visual decision after the R3.1 minimum-change fairness-boundary batch. All three variants were rendered as independent professional diagnostics under the same HERO camera and shared `OLEANDER Blender Surface System v1.20.0 / F1_DESIGN_VALIDATION` Strip / Grazing / Zebra setup.

This is design-routing evidence only. It is not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Evidence Identity

Execution head:

`d9398b316b02fe1a59ec8c74be831a8d737cf68e`

Workflow:

- `OLEANDER Modeling Worker v0.13 R3.1 Minimum-Change Batch`
- run `31796743285`
- result `SUCCESS`

Artifact:

- artifact ID `9217718477`
- name `oleander-modeling-worker-v0-13-g1-r3-1-31796743285`
- SHA-256 `f9f3941bb8b9d5e94d54fc5e2e9c177d96b5c1c10b64c2ceb0f884ed539e0618`
- size `2,703,302 bytes`

## Machine / Fairness Result

All three variants retain the R2 Machine QA and pass the R3 working interior fairness gate.

### R3.1-V1-U231

- `u_halfspan = 0.231`
- relation-change cost = `1.3096491228070175`
- max longitudinal = `7.593117041528593° / 0.01u`
- p95 longitudinal = `5.986207149158124° / 0.01u`
- max circumferential = `8.339934524235133° / 0.05rad`
- p95 circumferential = `7.090028383432866° / 0.05rad`
- max combined = `8.86179612902338`

### R3.1-V2-U233

- `u_halfspan = 0.233`
- relation-change cost = `1.3207602339181286`
- max longitudinal = `7.512418676366341° / 0.01u`
- p95 longitudinal = `5.906533240738286° / 0.01u`
- max circumferential = `8.342057693416715° / 0.05rad`
- p95 circumferential = `7.0966753639965745° / 0.05rad`
- max combined = `8.846435047195303`

### R3.1-V3-U235

- `u_halfspan = 0.235`
- relation-change cost = `1.3318713450292397`
- max longitudinal = `7.451440898908893° / 0.01u`
- p95 longitudinal = `5.840772116307209° / 0.01u`
- max circumferential = `8.344110816144203° / 0.05rad`
- p95 circumferential = `7.107710226878021° / 0.05rad`
- max combined = `8.827883612094524`

Machine recommendation by the corrected selector was `R3.1-V1-U231`, because fairness is treated as a gate and U231 is the smallest legal relation change among the passing batch.

## Source Authority Control

All variants changed only `INTERFACE_DECK_BOUNDARY`. `GRIP_AXIS`, `PALM_PROFILE`, `THUMB_SIDE_PLAN`, `OPPOSITE_SIDE_PLAN`, and `LOWER_RETURN_PROFILE` remained numerically unchanged. Interface depth remained `0.012 m`, `theta_center = TOP_MERIDIAN` remained locked, all rendered meshes remained `DERIVED_EXECUTION_NOT_AUTHORITY`, and the Blender-native Working Source was restored after the batch.

## Fixed-Rig Visual Review

### STRIP

Compared with R2, all three R3.1 variants remove much of the concentrated right-transition reflection hook. However, the interface basin no longer reads as a distinct secondary recessed field. The top becomes a broad, low-frequency depression. U231 / U233 / U235 are visually very close; the 0.004 range in `u_halfspan` does not recover interface definition.

### GRAZING

The R2 compressed dark ring is strongly reduced, confirming that the normal-field correction remains effective. Yet all three R3.1 variants still distribute the transition over too much of the upper surface. The relation hierarchy `palm volume > interface basin > lower return` remains weakened.

### ZEBRA

The R2 interface compression is simplified in every R3.1 variant, but the top transition occupies a much broader field. Differences among U231 / U233 / U235 are too small to justify further one-dimensional `u_halfspan` refinement. The right/front termination pattern remains open and unchanged.

## Decision

All three R3.1 variants are rejected as current Source corrections.

Classification:

`FAIRNESS_PASS_ONE_DIMENSIONAL_U_SEARCH_VISUALLY_INSUFFICIENT_REVISE`

Interpretation:

1. The fairness gate works and prevents the severe R2 interior normal compression.
2. Minimum-change selection works as governance logic, but the currently fixed `theta_halfspan_rad = 1.16` and `core_fraction = 0.25` already over-distribute the basin before `u_halfspan` is considered.
3. Varying only `u_halfspan` inside the passing band cannot recover local interface definition.
4. Therefore further R3.1 longitudinal micro-tuning is not a legal use of project time; re-entry must return to the interface relation pair controlling angular field and core extent.

## Next Legal Action

`R3.2 angular-field / core-fraction relation search`

Keep fixed:

- `theta_center = TOP_MERIDIAN`
- `depth_m = 0.012`
- all non-interface Source families
- no mesh-local correction

Re-open as active sparse variables:

- `theta_halfspan_rad`
- `core_fraction`
- `u_halfspan` only as the minimum longitudinal compensation required to pass fairness

Target:

Find the smallest relation departure from R2 that passes the working interior fairness gate **and** restores a distinct interface-basin reading under Strip / Grazing / Zebra. Fairness remains a gate, not the design objective.

The right/front termination defect remains separate and open.

## Authority Boundary

- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current promoted canonical authority.

No Promotion is authorized by this receipt.
