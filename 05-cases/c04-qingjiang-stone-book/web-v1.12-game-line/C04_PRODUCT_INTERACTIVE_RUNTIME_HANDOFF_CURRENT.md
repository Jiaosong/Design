# C04 PRODUCT INTERACTIVE RUNTIME HANDOFF — 云水倚

PROJECT_ID: `PRJ-C04-QINGJIANG-SHISHU`
OBJECT_ID: `PRJ-C04-DIGITAL-INTERACTION`
CURRENT_OWNER: `PRESENTATION`
NEXT_OWNER_FOR_RUNTIME_CARRIER: `VALIDATION`
NATIVE_MASTER: `05-cases/c04-qingjiang-stone-book/web-v1.12-game-line/index.html`
PR_FRONTIER: `#465 / agent/c04-web-v1-12-currentize-20260830`

## Presentation target

Place **云水倚** inside the existing `身体 / Physical` reading, as an interactive body-support object. It must remain secondary to the Qingjiang landscape/journey and must not create a new product-showcase chapter.

Target source MASTER:
`/恩施/Meshy_AI_云水倚_0823040512_texture_obj.zip` (~158.8 MB)

The MASTER package is preservation-only source material. Do not rename, overwrite, decimate-in-place, or load the package directly in the Web runtime.

## Current visible gap

The current Physical reading explains body need and intervention intensity but has no stable Web model derivative for the confirmed product MASTER. A static screenshot, generic proxy, AI redraw, or a different model would falsely imply interactive completion.

## Required interaction sequence

The Web derivative must support this minimum state sequence without explanatory text being required for comprehension:

1. `FIRST READ / REST` — product silhouette and bodily support orientation are legible immediately.
2. `AFFORDANCE CUE` — subtle orbit/drag cue; no decorative continuous spin.
3. `USER ACTION` — drag/orbit changes viewpoint while retaining a stable vertical/world reference.
4. `IMMEDIATE FEEDBACK` — active interaction state is visible through restrained part/surface emphasis, not a UI-card overlay.
5. `DETAIL REVEAL` — one hotspot reveals a physically meaningful contact/support/interface detail only if that detail is actually present in the MASTER.
6. `EXPLODED / PART RELATION` — optional exploded state is allowed only when the MASTER contains separable parts/groups with truthful relationships; otherwise omit exploded mode rather than inventing part boundaries.
7. `RECOVERY / RETURN` — a clear reset returns to the canonical first-read viewpoint and REST state.

Required adjacent-state readback: `REST → USER ACTION` and `USER ACTION → DETAIL REVEAL`.

## Visual features that must survive derivative preparation

Preserve from the MASTER after direct inspection:
- overall silhouette and characteristic curvature;
- body-contact / leaning / resting surface geometry that defines use;
- visible thickness changes that materially affect the first read;
- support-to-ground relationship and any clearly modeled structural/support transitions;
- major material boundaries, surface direction and authored texture identity when they are genuinely present in the source;
- proportions between major visible masses.

Do not infer missing engineering facts from appearance.

## Geometry/material simplification boundary

Allowed after direct MASTER inspection and before Web export:
- removal of hidden/internal geometry that has no visible or interaction role;
- consolidation of redundant material slots and texture maps while preserving visible appearance;
- reduction of micro tessellation, invisible backfaces, tiny bevel subdivisions and duplicated vertices where silhouette/contact reading is unaffected;
- Web-oriented LOD/mesh optimization generated as a NEW derivative, never by overwriting MASTER;
- texture resizing/transcoding only after visual comparison against the MASTER at the actual Web viewing distance.

Not allowed:
- changing the product silhouette to meet performance;
- flattening body-contact curvature into a generic bench/seat;
- merging parts that must move/highlight separately for the approved interaction;
- inventing joints, fasteners, seams, exploded parts or construction logic absent from the MASTER;
- substituting AI-generated geometry or unrelated low-poly furniture.

## Runtime derivative request to VALIDATION

Return a repo-addressable Web derivative generated from the exact MASTER above, together with:
- derivative path and source-to-derivative identity record;
- scene orientation / canonical camera proposal;
- list of actual separable mesh groups/material groups found in the MASTER;
- explicit statement of whether truthful exploded mode is possible;
- actual hotspot candidates tied to existing geometry only;
- proof that MASTER remains untouched;
- browser-loadable carrier and any required local textures;
- measured runtime/performance results separately from Presentation Design KEEP.

Presentation will decide final camera, crop, hierarchy, motion restraint and KEEP/REVISE only after the derivative can be rendered interactively at 1920, 1366-class and 390 mobile.

## Truth boundary

`MASTER KEEP ≠ WEB RUNTIME KEEP`
`CONCEPT KEEP ≠ PIXEL KEEP`
`RUNTIME/PERFORMANCE PASS ≠ PRESENTATION KEEP`

Until the derivative returns, status is:

`PRODUCT SOURCE CONFIRMED / INTERACTION HYPOTHESIS LOCKED / WEB DERIVATIVE HOLD / DESIGN KEEP NOT CLAIMED`
