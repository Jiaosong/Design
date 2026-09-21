# OLEANDER Professional Runtime Pack — Candidate 2026-09-20

**State:** CANDIDATE RUNTIME PACK / NOT CURRENT / NO PROFESSIONAL PROMOTION

This package increases real execution depth at R-G/R-H without fabricating professional authority.

## Candidate runtimes

### Structural — OpenSeesPy
- Runtime: OpenSeesPy 3.8.0.0.
- Smoke: deterministic 2D elastic truss, numerical displacement checked against the closed-form axial result.
- Adds real structural-analysis execution capability.
- Does **not** prove project load basis, code compliance, member/connection design, checking, structural professional approval or field conformity.

### Building Services / MEP — EnergyPlus
- Runtime: EnergyPlus 26.1.0 Linux Ubuntu 24.04 x86_64 release.
- Smoke: verified binary + real EnergyPlus example simulation when the packaged example is available.
- Adds a real thermal/building-energy simulation surface for bounded MEP/energy questions.
- Does **not** replace HVAC/electrical/plumbing/fire professional design, sizing authority, commissioning or measured operation.

### Lighting — Radiance
- Runtime: LBNL-ETA Radiance rad6R0P2 Linux release.
- Smoke: compile a real Radiance scene with `oconv`, calculate irradiance using `rtrace -I`, and require a finite positive RGB result.
- Adds real photometric simulation capability.
- Does **not** prove luminaire photometry, compliance, glare/daylight acceptance, field illuminance/luminance or commissioning.

### Landscape — Terrain grading / cut-fill
- Runtime: deterministic stdlib Python.
- Smoke: cell-based existing/proposed elevation comparison with exact cut/fill/net-volume readback.
- Adds a real terrain quantity computation surface.
- Does **not** prove survey authority, civil grading design, hydrology/drainage, geotechnical suitability or field quantities.

## Lifecycle boundary

`RUNTIME SMOKE PASS ≠ CURRENT EXECUTION OWNER ≠ PROFESSIONAL PROCESS PASS ≠ DESIGN KEEP ≠ FIELD TRUTH`.

These runtimes may become usable by project capability plans only after the normal adapter/lifecycle review determines the permitted claim ceiling.
