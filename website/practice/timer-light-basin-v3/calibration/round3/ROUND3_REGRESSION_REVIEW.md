# v3.3 Photography Calibration — Round 3 regression review

**Date:** 2026-08-10  
**Run:** GitHub Actions `Timer v3.3 Photography Round 3` / run `31350071652`  
**Environment:** Chromium / WebGL 2.0 / ANGLE → Vulkan → SwiftShader  
**Decision:** `REJECTED REGRESSION / NON-AUTHORITATIVE / DOES NOT SUPERSEDE FINAL LOCK`

## Why this round is rejected as calibration evidence

Round 3 changed the calibration geometry representation itself. It rebuilt the external product surfaces using a simplified `LatheGeometry`/primitive rig rather than the canonical GLB or the previously verified surface-equivalent calibration subset. That introduces a confounding variable before lighting/material evaluation.

The authoritative geometry-equivalence gate for v3.3 is:

- canonical source: `assets/pbr/timer_100_pbr.glb`
- canonical SHA-256: `900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66`
- verified calibration subset: `calibration/timer_visual_calibration_subset.glb`
- subset SHA-256: `ad18d9afb489cff1eece609a1e722c5b723872e84c6a96768b0c51a9339d57b2`
- equivalence tolerance: `1e-5 mm`
- Housing / Diffuser / Side Knob / Bottom Cover / Silicone Foot Ring: identical visible triangle surfaces, bounds and surface area at the recorded tolerance.

## Round 3 visual result

| Gate | Result | Reason |
|---|---|---|
| Housing highlight | **REJECT** | Simplified housing profile reads clay-like / banded and cannot certify the canonical enclosure curvature. |
| Diffuser volume | **REJECT** | Edge volume improves, but the center remains too flat/warm and the simplified rig is not the authoritative diffuser surface. |
| Metal knob reflection | **REJECT** | A side reflection sweep exists, but the front face is too dead/dark and the primitive cylinder cannot certify the canonical knob response. |
| Contact shadow falloff | **REJECT** | Contact core is weak and the finite ground setup remains visible; not acceptable as final grounding evidence. |

## Authority decision

The Round 3 result is preserved as a **rejected experiment**, not a new render-lock decision. It does **not** reopen or supersede the existing v3.3 lock because it did not test the locked geometry representation under controlled same-condition calibration.

The existing authoritative lock remains the calibration record produced with the canonical/surface-equivalent geometry and four reviewed final frames:

- `calibration/final_lock/housing.png`
- `calibration/final_lock/diffuser.png`
- `calibration/final_lock/knob.png`
- `calibration/final_lock/shadow.png`

`FINAL HERO / CMF RENDER PROFILE LOCK = LOCKED` remains a **photography visualization target only**. Optical performance, measured material appearance, thermal, electrical, DFM/DFA, tolerances and user recognition remain NOT RUN.
