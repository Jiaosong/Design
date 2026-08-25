# Route & Wayfinding UI Visual Layer Binding

Status: **BINDING ONLY / TOPOLOGY AND DECISION HIERARCHY FIRST**

This Skill already contains route visual rules. The binding below reuses existing OLEANDER wayfinding/data/motion training and does not create a new map style.

## Existing sources to inherit

1. Current `oleander-route-wayfinding-ui` topology and Return rules.
2. Notion practice `2026-08-16｜Information Design / L5｜拓扑优先而非伪地理：多分支路线图可读性`.
3. Existing wayfinding training provenance including commit `673f4516192ed1d703a90df8d9f19b4b27a7590f` (decision-priority / Schiphol transfer).
4. `oleander-data-viz` Operational Route-State Semantics Gate.
5. `oleander-motion/MOTION_LIBRARY_EFFECT_ATLAS.md` for route trace/progress/continuity mechanisms.
6. `oleander-ui-visual-composition` for final screen hierarchy.
7. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for map underlay, mask, opacity, raster/vector compositing and bounded effects.

## Existing visual boundary

Topology/state authority comes before styling. Route color, lineweight, pattern, node emphasis and motion may clarify current context, decision priority and Return; they may not invent GPS precision, live status or geometry. `UNKNOWN` must not be normalized into a visually open route.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for source-preserving crop, map underlay cleanup, masks, alpha, opacity, clipping, blend modes, texture, local contrast and vector-safe/raster-preview effects. Keep route topology, state semantics, labels and source geometry authoritative. Do not use blur, retouch, perspective warp, content-aware or generative edits to remove inconvenient route branches, manufacture precision, hide closure/unknown states or visually imply a connection absent from the source.

## Review inheritance

Review source ↔ UI contradictions, current-context cue, Return/recovery, mobile density and state legibility before aesthetic polish.
