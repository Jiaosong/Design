# Spatial Lab Professional Retest 01 — 2026-08-27

**Surface:** `browser_spatial_lab`  
**Review source:** Professional Review 01 / S01–S05  
**Binding:** Timer Light Basin canonical GLB-derived AABB proxy, read-only  
**Verdict:** **PASS S01–S05 / INDEPENDENT KEEP OPEN / ACTIVE NOT GRANTED**

## Artifact-first retest
- **S01 PASS** — viewport legend lists all five source-mesh proxy IDs; selected object is highlighted and labeled.
- **S02 PASS** — proxy-scene X/Y/Z bounds, declared canonical GLB X/Y/Z bounds, selected-object size and position are visible.
- **S03 PASS** — `AABB PROXY ONLY — NOT FORM / SILHOUETTE / CAD GEOMETRY` is a primary viewport warning.
- **S04 PASS** — selected source/object ID → proxy role, axis map and `geometryEquivalent=false` are inspectable in the viewport.
- **S05 PASS** — orthographic views expose exact **view-plane** scale; Perspective explicitly states `NO UNIFORM SCALE / DEPTH-DEPENDENT`.

## Canonical source recheck
`timer_100_pbr.glb` was rehashed unchanged: `900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66`, 8,507,960 bytes, 21 meshes.

Canonical bounds are 118.000 × 123.900 × 34.180 mm in source XYZ, or 118.000 × 34.180 × 123.900 mm in Lab X/Y/Z after the existing XZY axis map. The selected five-proxy scene is smaller in Y/Z; the runtime now displays proxy-scene and canonical-source bounds separately so they cannot be conflated.

## Regression
- `geometryEquivalent=true` → fail-closed.
- Dirty scene → export blocked.
- 390px readback → no horizontal overflow; no page errors.
- Zero external runtime dependency retained.

## Boundary
This retest proves the shared proxy/camera/proportion **readback surface** is more professionally legible. It does **not** make the AABB proxy canonical geometry, product silhouette/form evidence, CAD/BIM, DFM or engineering proof.

**Promotion:** `INDEPENDENT_KEEP_OPEN_ACTIVE_NOT_GRANTED`.
