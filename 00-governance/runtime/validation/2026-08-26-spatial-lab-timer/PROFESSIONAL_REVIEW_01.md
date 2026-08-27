# Spatial Lab｜Professional Review 01

Date: 2026-08-27
Surface: `browser_spatial_lab`
Review method: artifact-first. Reviewed Front/Top/Axon orthographic, Perspective and 390×844 readbacks before reading Scene JSON / derivation receipt.
Verdict: **REVISE / RETEST REQUIRED / ACTIVE NOT GRANTED**

## Artifact-first verdict
Projection math and proxy truth labeling are working, but the finished viewport is not yet a professional proxy/spatial-review surface. The Timer Light Basin proxy reads first as an anonymous architectural box rather than five explicitly derived product components. The runtime preserves AABB relations in data, but does not make preserved relation, source-component identity, overall bounds, or scale evidence legible in the viewport itself.

## Findings
### S01｜Critical｜Proxy objects have no viewport identity
The canonical-derived objects are `01_Upper_Housing`, `02_Formed_Diffuser`, `17_Side_Knob`, `18_Bottom_Cover`, and `19_Silicone_Foot_Ring`, but none of these identities is visible in the finished viewport. Subtle gray fills are insufficient to tell a reviewer which proxy corresponds to which source mesh.

**Root Cause:** object identity remains in Scene JSON only; renderer treats boxes as anonymous solids.

**Feedback Action:** add bounded object-label/selection overlay using exact object IDs and `proxy_role`, with hide/show control. Labels are review metadata and must never imply source geometry equivalence.

**Retest Evidence:** artifact-first readback can identify all visible proxy components without opening Scene JSON.

### S02｜Critical｜No explicit overall bounds or dimension readback
The viewport says `units=mm` and `grid≈20 mm`, but does not display the scene/proxy overall X/Y/Z extents or component dimensions. A proportion-review tool cannot rely only on an approximate grid.

**Root Cause:** Fit Scene calculates bounds internally but does not expose the measured extents as finished-view evidence.

**Feedback Action:** display calculated overall proxy bounds and optional selected-object `size / position`; orthographic views should include an exact scale bar or dimension reference derived from current projection and units.

**Retest Evidence:** orthographic artifact can answer overall width/depth/height and selected component size without manual grid counting.

### S03｜High｜AABB proxy can be visually mistaken for form/silhouette evidence
Although the header says `PROXY_ONLY`, the first visual is a coherent shaded solid. For Timer this produces a building-like box and hides the source product's curved/specific silhouette. The risk is not geometric falsification in data; it is visual over-interpretation.

**Root Cause:** current truth boundary is textual but not coupled to the visual representation mode.

**Feedback Action:** add an unmistakable viewport-level `AABB PROXY / RELATION + BOUNDS ONLY / NOT FORM OR SILHOUETTE` state; default derived proxies to a visibly analytical treatment such as translucent/wireframe-capable boxes rather than presentation-like solids.

**Retest Evidence:** a viewer cannot reasonably read the proxy as the canonical product form when the side panel is hidden.

### S04｜High｜Source→proxy correspondence is not inspectable in the viewport
The derivation receipt proves each proxy AABB matches its selected canonical mesh bounds with near-zero error, but the runtime only shows source name/hash and a generic derivation string. It does not expose which proxy came from which source mesh nor the per-object derivation status.

**Root Cause:** source provenance is scene-level, while derivation is object-level.

**Feedback Action:** support optional object metadata fields for `source_mesh_id / derivation / source_bounds` and surface them on selection. Keep them declarative; the browser runtime does not re-hash or prove canonical GLB geometry.

**Retest Evidence:** selecting a proxy reveals exact source mesh identity and AABB derivation without claiming re-verification by the Lab.

### S05｜Medium｜Orthographic scale semantics are too approximate
`grid≈20 mm` is useful orientation but not an exact professional scale reference. In orthographic review the screen projection is deterministic, so an exact screen-space scale bar can be provided; in Perspective the same treatment would be misleading because scale varies with depth.

**Root Cause:** one generic grid annotation is used across different projection semantics.

**Feedback Action:** separate `ORTHOGRAPHIC EXACT SCALE REFERENCE` from `PERSPECTIVE GRID / DEPTH-DEPENDENT`. Never show a perspective scale bar as globally exact.

## What is already acceptable
- Canonical source name/SHA and `geometryEquivalent=false` are explicit.
- AABB derivation is bounded and does not replace canonical GLB.
- Five selected proxies match source AABBs according to persisted derivation evidence.
- Front orthographic depth invariance is proven in browser testing.
- Front/Top/Axon are distinguished from Perspective camera readback.
- Invalid/dirty/unsupported scenes fail closed.
- Unit validation, source SHA requirement, duplicate-ID and negative-size checks are present.
- Spatial runtime remains zero external dependency.

These functional and evidence qualities do not substitute for professional proxy readability.

## Decision
`REVISE`.

Do **not** promote Spatial Lab to ACTIVE. Required next transaction:

`S01–S05 repair → actual browser readback on same canonical Timer proxy → artifact-first professional retest → then reconsider promotion`.

Canonical GLB remains Source Authority. AABB proxies remain relation/bounds review derivatives only and must not be used for form, material, manufacturing, BIM/CAD or engineering claims.
