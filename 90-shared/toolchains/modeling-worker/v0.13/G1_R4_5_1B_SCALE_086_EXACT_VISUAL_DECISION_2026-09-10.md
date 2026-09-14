# G1 R4.5.1B｜Exact Scale 0.86 Human Visual Decision｜2026-09-10

## Decision

`MACHINE_PASS / SAVED_BLEND_REOPEN_PASS / VISUAL_REVISE / SCALE_0_86_NOT_CONFIRMED / CURRENT_CAP_CONSTRUCTION_REVIEW_REQUIRED / WORKING_SOURCE / CANDIDATE_REVIEW_REOPENED / CANDIDATE_PROMOTION_NOT_RUN`

The exact `termination_cap_pole_curvature_scale = 0.86` confirmation is rejected at the Human Visual gate. The parameter remains useful diagnostic evidence but is **not** confirmed as the current Working Source relation and does not authorize Candidate Promotion.

The bounded pole-curvature-scale search is exhausted for the current fixed cap construction: lowering the scale from `.90` to `.86` improves the Machine metrics and weakens the terminal artifact, but `.86` still retains the same terminal-island / hook organization while its near-pole normal-turn margin is effectively consumed. Further reduction of the same scale is therefore not a legal next action under the fixed `2.0°` near-pole gate.

## Exact Execution Evidence

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.5.1B Scale 0.86 Confirmation`
- run `34485293563` = `SUCCESS`
- head `97c88343015069d6b98002239556fdf2dcbcc76b`
- artifact ID `10155453644`
- artifact `sha256:86805b1f943db2d38d3d6c46e3ca301f67b1cfebb2b4bbc25647dea667efd657`
- artifact size `3,665,013 bytes`

Frozen Source relation:

- Source owner = `LOWER_RETURN_PROFILE`
- `termination_cap_onset_u = 0.88`
- `termination_cap_pole_curvature_scale = 0.86`
- `termination_cap_law = C2_MATCHED_ELLIPTIC_PARABOLOID_POLE`
- `termination_cap_endpoint_section = SYMMETRIC_ELLIPSE_DERIVED_FROM_ONSET_MEANS`
- cap numeric DOFs = `2`
- shared termination envelope exponent = `0.34`
- confirmed R3 interface remains locked

Machine confirmation = PASS:

- onset position continuity error = `0.0 m`
- onset normal continuity = `0.0501049806°`
- confirmed-interface regression = `0.0 m`
- cap-region max normal turn = `2.2879481523°`
- near-pole max normal turn = `1.9922871699°` against fixed hard gate `≤ 2.0°`
- reflection-flow concentration ratio = `1.1484027940`
- radial monotonic violations = `0 / 0`
- closure error = `0.0 m`
- sparse Source scalar count = `50`
- native Source roundtrip = PASS
- shared Blender Surface System runtime = PASS

## Saved Blender Reopen Evidence

The exact `.blend` was closed and opened by a second Blender `5.2.0 LTS` process. Reopen persistence = PASS.

- file: `OLEANDER_G1_R4_5_1B_SCALE_086_WORKING_SOURCE__v0_13.blend`
- file SHA-256: `2c03e71ff65312253c70aaabf99767b5f454b93fbc58298990f97c9a7f2af1ae`
- live Source digest: `61b51dd1918c7e41cbd79b7ea0aa27a75102c26e2d17104c422132f2479beb94`
- saved candidate vertices = `4682`
- embedded cap-aware rebuild vertices = `4682`
- saved-vs-rebuilt max vertex displacement = `0.0 m`
- exact onset `.88` and scale `.86` persisted after reopen
- self-contained Blender Text rebuild retained the cap law and rebuilt the exact derived candidate
- derived mesh remained `DERIVED_EXECUTION_NOT_AUTHORITY`
- Candidate Promotion remained `NOT_RUN`

This closes the previous persistence ambiguity: the failure below is a design/surface-construction failure, not a serialization, readback, runtime, topology-density, or stale embedded-rebuild failure.

## Exact 768 px Human Visual QA

Decision: `REVISE`.

Compared directly with the `.90` control under the same `100 mm` camera and the same shared Surface System rigs:

1. **BROAD** — `.86` slightly reduces the localized terminal dimple/patch, but the terminal region still reads as a separate local event rather than one low-frequency continuation of the body volume.
2. **STRIP** — the compact high-contrast terminal oval remains clearly legible and spatially detached from the broader reflection field. Its reduction relative to `.90` is insufficient to satisfy the explicit gate.
3. **GRAZING** — the terminal crescent/island is weaker than `.90` but remains a distinct closed terminal event.
4. **ZEBRA** — the localized lower hook/loop remains present. The topology of the reflection path is substantially the same as the rejected `.90` control.

The rendered image deltas also confirm that `.86` is a narrow refinement rather than a construction-level visual correction:

- BROAD mean absolute RGB delta vs `.90` = `0.0003083`
- STRIP = `0.0007458`
- GRAZING = `0.0005200`
- ZEBRA = `0.0002548`

No onset kink or obvious closure break is introduced. The failure is specifically the persistence of the appended terminal-cap reflection organization.

## Sufficiency Decision

The current fixed construction

`C2_MATCHED_ELLIPTIC_PARABOLOID_POLE + SYMMETRIC_ELLIPSE_DERIVED_FROM_ONSET_MEANS`

has reached the useful limit of the authorized second DOF. The evidence does **not** justify relaxing the near-pole gate, adding arbitrary profile points, adding a seventh Source family, or applying mesh-local/sculpt corrections.

The next problem layer is the **cap construction / endpoint target relation itself**: the current endpoint target still organizes the terminal field as a compact elliptical event even when its scalar amplitude is reduced to the legal limit.

## Current State

- `R4.4 structural cause = CLOSED`
- `R4.5 onset DOF = METHOD PASS / VISUAL REVISE`
- `R4.5.1 pole-curvature-scale DOF = METHOD PASS / VISUAL REVISE`
- `R4.5.1B exact .86 persistence = PASS`
- `R4.5.1B exact .86 visual decision = REVISE / NOT_CONFIRMED`
- `CURRENT FIXED CAP CONSTRUCTION = REOPEN FOR SUFFICIENCY REVIEW`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current Canonical Authority.

## Next Legal Action

Before any new geometry parameter or construction is introduced, create a fail-closed cap-construction sufficiency contract that compares the current endpoint-target construction against the smallest structurally distinct Source-level alternative while keeping the already-confirmed body/interface Source unchanged.

No parameter tuning is authorized by this receipt. No third numeric DOF is authorized by this receipt. Any proposed construction must first prove its vocabulary, Source ownership, continuity/closure behavior, bounded scalar count, Blender-native roundtrip, self-contained reopen rebuild, and fixed-rig diagnostic plan before execution.

This receipt does not establish Candidate Authority, Canonical Promotion, Class-A, engineering CAD, manufacturing/tooling, ergonomic comfort, final CMF or Release.
