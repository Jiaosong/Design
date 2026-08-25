# Modeling Worker v0.13｜G1 R2 Blender Integration + Reflection Decision

Decision: `BLENDER EXECUTION PASS / REFLECTION VISUAL REVISE / CANDIDATE REVIEW REOPENED / CANDIDATE PROMOTION BLOCKED`.

## Bound execution evidence

- Benchmark: `MW-V013-G1-ERGONOMIC-HANDHELD-SHELL`.
- GitHub head: `80f240c7b530440ae5a80fee43fee12616e97890`.
- Blender Bridge run: `31759322863` / #3 = `SUCCESS`.
- Control Plane run: `31759322853` / #46 = `SUCCESS`.
- AI Governance run: `31759322874` / #672 = `SUCCESS`.
- Blender artifact: `9203993150`.
- Artifact digest: `sha256:d8090d420167521181bc1832ea8147f643030c2c2a6adf5a5efa44ddae3c9b64`.
- Native `.blend` SHA256: `e1d078e1fa0742035c6e8b00c2399446abe4e8bb3c89123d76e541bba41acb9c`.
- Runtime: Blender `5.2.0 LTS` / `CYCLES`.
- Native source mode: `BLENDER_NATIVE_EDITABLE_MIRROR_WITH_JSON_INPUT_AUTHORITY`.
- Six native source objects are editable; baseline/revision meshes remain `DERIVED_EXECUTION_NOT_AUTHORITY`.
- R2 Machine baseline/revision checks remain PASS.
- Outputs include native `.blend`, 32-bit diagnostic EXR, Broad / Strip / Grazing / Zebra baseline views and controlled thumb-revision A/B views.

## Integration result

`Primary Curve Source → Blender native editable source mirror → derived execution mesh → Cycles diagnostic rigs → .blend / EXR / PNG / machine-readable receipt` is now executable and CI-replayed.

This closes the previous v0.13 Blender-integration gap. It does **not** implement Blender-to-JSON source round-trip writeback; JSON R2 remains the replay input authority for this gate.

## Reflection Visual QA

Result: `REVISE`.

The calibrated replay fixed the earlier diagnostic framing defect: Top and Side are no longer cropped and light/card geometry is not directly visible to cameras. Broad exposure is improved but remains too flat for fine form reading, so Broad is treated as mass/proportion evidence rather than fairness evidence.

The stronger Strip / Grazing / Zebra diagnostics consistently expose two unresolved surface behaviors:

1. `INTERFACE BASIN RIGHT TRANSITION` — reflection bands compress and hook around the basin rim/right transition instead of maintaining a clean controlled flow.
2. `RIGHT/FRONT TERMINATION` — a persistent reflection pinch / crease-like convergence remains visible under both Strip and Grazing, with corresponding Zebra compression.

Because these behaviors persist across independent lighting/material diagnostics, they cannot be dismissed as a single-rig lighting artifact. The current evidence does **not** yet isolate whether the root cause is `Surface Construction / termination topology` or an upstream `Relation / Surface Source` condition.

## Fail-closed consequence

The earlier pre-Blender Candidate Review remains immutable historical evidence that the analytic + custom diagnostic benchmark passed at that time. The new Blender Reflection Gate is newer evidence and reopens the current Candidate Review.

Current live disposition:

- Job State: `BLENDER_EXECUTION_VALIDATED / REFLECTION_REVIEW_EXECUTED`.
- Design State: `REVISE` for the G1 R2 Blender-reflection gate; overall v0.13 authority object remains pre-promotion.
- Authority State: `WORKING_SOURCE`.
- Candidate Review: `REOPENED`.
- Candidate Promotion: `BLOCKED / NOT_RUN`.
- v0.12 remains current `PROMOTED / CANONICAL_AUTHORITY / SYNCED / NOT RELEASED`.

## Next legal action

Run a termination/interface **source-vs-execution isolation test** before changing geometry:

`same R2 Source → alternate/densified derived execution topology + analytic/source-space probes → compare Strip/Grazing/Zebra invariance`.

- If the reflection defect changes materially with execution topology, re-enter `Surface Construction / Execution Geometry`.
- If it persists invariantly, re-enter `Relation / Surface Source` and revise the low-frequency interface/termination authority.

No mesh-local cosmetic patch is allowed.

## Boundary

This receipt does not establish ergonomic comfort, anthropometric/usability validation, final industrial-design quality, Class-A surfacing, engineering CAD, manufacturing/tooling feasibility, final CMF, Candidate Authority, Canonical Authority or Release.
