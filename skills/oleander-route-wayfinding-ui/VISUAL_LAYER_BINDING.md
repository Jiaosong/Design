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

## Brand-derived route graphic ↔ functional wayfinding semantic firewall

A route-derived identity graphic may share the same source geometry as a functional route surface, but **shared geometry does not transfer functional authority**.

Declare every route-derived carrier as one of:
- `IDENTITY_TRACE` — brand/section-divider/page-relation/decorative crop;
- `FUNCTIONAL_ROUTE` — orientation, current context, movement decision, Return/recovery, operational state;
- `OPTIONAL_READING` — interpretation/memory layer attached to route context but not owning navigation.

### Allowed / prohibited semantics

`IDENTITY_TRACE` may use source-bound crop, trace, rhythm, opacity, repetition and identity placement. Unless Current Authority explicitly assigns dual use, it must not introduce:
- `YOU ARE HERE` / current-position markers;
- directional arrows or movement verbs;
- start/destination claims;
- distance, time or GPS-like precision;
- `NORMAL / DEGRADED / CLOSED / UNKNOWN` operational state;
- Return/recovery as its sole carrier.

`FUNCTIONAL_ROUTE` may use the same authoritative route geometry, but must make functional semantics explicit enough to decode: node role, current context, decision hierarchy, Return/recovery and truth/state boundary where applicable.

### Failure-seeking tests

1. **CARRIER-ROLE** — record the role before styling: `IDENTITY_TRACE / FUNCTIONAL_ROUTE / OPTIONAL_READING`.
2. **LABEL-OFF** — remove labels. An identity carrier must not still look like an unsupported instruction to move.
3. **ARROW-OFF** — remove directional marks. A functional carrier must retain current-context and Return logic rather than collapsing into a brand trace.
4. **FALSE-AFFORDANCE** — deliberately add node/arrow/start/current markers to the identity carrier. If this creates a plausible movement instruction without owned evidence, reject the treatment.
5. **RETURN-OWNERSHIP** — Return/recovery must not exist only in a decorative/brand layer.
6. **STATUS-OWNERSHIP** — operational-state semantics belong to functional carriers and may not be borrowed as brand decoration.
7. **GEOMETRY-IDENTITY** — brand and functional carriers may share source route geometry; neither may mutate it for graphic convenience unless authority explicitly changes.

Promotion test:
> **Remove labels and arrows: if a brand-derived route trace still looks like an instruction to move, it is borrowing wayfinding authority and must be restated.**

### Hard blockers

- a brand/decorative route trace contains a current-position marker without position authority;
- arrows, `START HERE`, destination cues or movement verbs are added only to make the identity graphic feel more dynamic;
- `CLOSED / UNKNOWN / NORMAL` is encoded on an identity trace as mood/decoration;
- Return exists visually only inside a P06/brand layer while the functional surface lacks recovery semantics;
- opacity/blur/styling is used to argue that a false navigation affordance is “only decorative” after it already reads as instruction;
- the functional route is weakened until brand styling prevents immediate movement/recovery decoding.

Record in review:
```text
CARRIER_ROLE: IDENTITY_TRACE | FUNCTIONAL_ROUTE | OPTIONAL_READING
SOURCE_ROUTE:
OWNED_SEMANTICS:
PROHIBITED_SEMANTICS:
FALSE_AFFORDANCE_RESULT: PASS | REVISE | REJECT
RETURN_OWNERSHIP:
STATUS_OWNERSHIP:
GEOMETRY_IDENTITY_LOCKED: YES | NO
DOES_NOT_PROVE:
```

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for source-preserving crop, map underlay cleanup, masks, alpha, opacity, clipping, blend modes, texture, local contrast and vector-safe/raster-preview effects. Keep route topology, state semantics, labels and source geometry authoritative. Do not use blur, retouch, perspective warp, content-aware or generative edits to remove inconvenient route branches, manufacture precision, hide closure/unknown states or visually imply a connection absent from the source.

## Review inheritance

Review source ↔ UI contradictions, current-context cue, Return/recovery, mobile density, carrier-role authority and state legibility before aesthetic polish.
