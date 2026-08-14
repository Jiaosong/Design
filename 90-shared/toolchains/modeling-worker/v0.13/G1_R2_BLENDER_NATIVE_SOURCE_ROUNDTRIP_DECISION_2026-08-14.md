# Modeling Worker v0.13｜G1 R2 Blender Native Surface Source Round-trip Decision｜2026-08-14

## Decision

`BLENDER NATIVE SOURCE ROUND-TRIP PASS / SAVED-BLEND REOPEN+REBUILD PASS / REFLECTION VISUAL REVISE RETAINED / CANDIDATE REVIEW REOPENED / CANDIDATE PROMOTION NOT RUN`

This receipt closes the integration question: the v0.13 sparse Surface Source is no longer only a JSON authority mirrored into Blender. After bootstrap, the six Blender-native source objects are the editable `WORKING_SOURCE` representation used to rebuild derived execution geometry. The original JSON R2 source/correction remain immutable bootstrap seed + provenance and are not overwritten by Blender edits.

## Bound runtime evidence

- PR: `#95`
- branch/head: `agent/modeling-worker-v0-13-generalization-reentry @ 11ed0dc1372e28fc11559916d9ed2c08387c3aae`
- Blender Bridge: `#29` / run `31762356416` / `SUCCESS`
- Control Plane: `#72` / run `31762356329` / `SUCCESS`
- AI Governance: `#703` / run `31762356234` / `SUCCESS`
- Blender: `5.2.0 LTS`
- render engine: `Cycles`
- Blender Surface System: `v1.20.0 / F1_DESIGN_VALIDATION`
- artifact id: `9205096114`
- artifact digest: `sha256:4582de638442fbc385ed6f15710dff62d8a663737605f56eeac7802550a5353a`
- native `.blend` SHA-256 after reopen/rebuild verification: `e38996c6af59dbf23a38787c2c81192382115cc326ce0e62eb7b2bab04528cda`

## Native Working Source

Collection: `OLEANDER_SOURCE_AUTHORITY`

Editable source objects:

- `OL_SRC_GRIP_AXIS`
- `OL_SRC_PALM_PROFILE`
- `OL_SRC_THUMB_SIDE_PLAN`
- `OL_SRC_OPPOSITE_SIDE_PLAN`
- `OL_SRC_LOWER_RETURN_PROFILE`
- `OL_SRC_INTERFACE_DECK_BOUNDARY`

Derived execution objects remain explicitly non-authoritative:

- `OL_DERIVED_G1_R2_BASELINE`
- `OL_DERIVED_G1_R2_THUMB_REVISION`

Locked semantic retained without creating a 49th source scalar: `INTERFACE_DECK_BOUNDARY.theta_center = TOP_MERIDIAN`.

## Round-trip evidence

Blender control-point storage is float32; bootstrap readback tolerance is therefore explicitly `1e-8 m`, not an impossible bit-identical float64 comparison. Maximum observed bootstrap family error was `6.437301636e-9 m` on `GRIP_AXIS`, inside the declared representation tolerance.

Controlled Blender-native edit:

- source object: `OL_SRC_THUMB_SIDE_PLAN`
- control index: `3`
- requested edit: `+0.003 m`
- observed source change: `0.003000002354 m`
- changed source families: `THUMB_SIDE_PLAN` only
- derived surface max displacement: `0.001021227935 m`
- restored source error: `0.0 m`

Result: `PASS`.

## Saved .blend continuity test

The generated `.blend` was opened in a second Blender 5.2 process. The embedded text block `OLEANDER_G1_R2_REBUILD.py` was executed after a new native source edit.

- saved `.blend` contains native source object: PASS
- saved `.blend` contains derived surface: PASS
- embedded rebuild text present: PASS
- native edit changes rebuilt derived surface: `0.001021225005 m` / PASS
- `OLEANDER_G1_R2_LIVE_SOURCE.json` reflects the edit: PASS
- source restored and rebuilt surface returns to baseline: `0.0 m` error / PASS
- derived object remains `DERIVED_EXECUTION_NOT_AUTHORITY`: PASS
- Authority State remains `WORKING_SOURCE`: PASS
- Candidate Promotion remains `NOT_RUN`: PASS

Therefore the saved Blender file is a continuing editable source document, not merely a rendered export container.

## Machine QA retained after native readback

Baseline and controlled revision both retain the R2 Machine gate, including:

- sparse authority scalar count: `48`
- L/W/H baseline: `0.189999998 / 0.080760616 / 0.104816465 m`
- interface boundary loops: `1`
- broad fairness baseline: `2.812692° longitudinal / 4.183682° circumferential`
- interface continuity: `0.173789° outer / 0.232724° core`
- execution mesh is not authority: PASS

## Surface System diagnostics

The artifact includes:

- Broad perspective / top / side
- Strip perspective
- Grazing perspective
- Zebra normal-field perspective
- controlled relation A/B Broad + Strip
- 32-bit master EXR
- native `.blend`
- native-source snapshot
- round-trip snapshot
- saved-blend reopen/rebuild report

## Reflection Visual QA remains REVISE

Native-source integration does **not** erase the prior real Blender reflection findings. The following remain open:

1. `INTERFACE BASIN RIGHT TRANSITION` — reflection-band compression / hook at the basin-right transition.
2. `RIGHT / FRONT TERMINATION` — persistent pinch / crease-like convergence under Strip and Grazing, with Zebra compression.

These defects existed before the round-trip bridge and the source geometry was not revised in this integration task. Therefore their Visual disposition remains `REVISE`.

Next legal action follows the existing isolation contract:

`same R2 Source → alternate / densified derived execution topology + analytic/source-space probes → compare Strip / Grazing / Zebra invariance`

- if defect changes materially with execution topology: classify `Surface Construction / Execution Geometry`;
- if defect remains invariant: classify `Relation / Surface Source` and re-enter upstream relationship revision.

No cosmetic mesh-local patch is authorized.

## Current state

- Job State: `BLENDER_NATIVE_SOURCE_ROUNDTRIP_VALIDATED`
- Design State: `REVISE`
- Authority State: `WORKING_SOURCE`
- Candidate Review: `REOPENED`
- Candidate Promotion: `NOT_RUN / BLOCKED`
- v0.12: remains current `CANONICAL_AUTHORITY`

## Boundary

This receipt proves Blender-native editable Working Source readback/rebuild and saved-file continuation for this bounded G1 R2 benchmark. It does not establish ergonomic comfort, universal design reasoning, final industrial-design quality, Class-A surfacing, engineering CAD, manufacturing/tooling feasibility, final CMF, Candidate Authority, Canonical Promotion or Release.
