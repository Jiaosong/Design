# Mobile Game UI Visual Layer Binding

Status: **BINDING ONLY / MOBILE RECOMPOSITION, NOT A NEW STYLE**

This Skill is an ergonomics and mobile-resilience gate. It does not own an independent visual-effect style.

## Existing sources to inherit

1. `oleander-ui-visual-composition` for visual hierarchy and finish.
2. Existing browser-tested practice `06-practice/2026/2026-08-18-responsive-recomposition/`.
3. `oleander-motion` / `MOTION_LIBRARY_EFFECT_ATLAS.md` for Reduced Motion and temporal mechanisms.
4. `oleander-ui-interaction` for touch/focus/state parity.
5. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
6. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for mobile image preparation and bounded effects.

## Existing responsive visual rule

Do not merely stack or shrink a desktop composition. Preserve information, but allow breakpoint-specific order, span, emphasis and density to change when task priority requires it. A technically responsive layout can still be a visual REVISE if the first task is delayed or support content becomes co-primary.

Effects that cost target size, safe-area clarity, touch discoverability, native control or Reduced Motion equivalence must be reduced or removed.

## Scene-anchored depth grammar gate

Use this gate when a mobile/game-like surface overlays route, node, observation, object or distance cues on a landscape/world view. The goal is not generic AR styling; it is to make every cue visibly belong to the correct depth owner.

Classify each visible cue before styling:

- `WORLD_BOUND`: route segments, local nodes, object labels, distance/approach relations and other cues whose meaning depends on scene position.
- `SCREEN_BOUND`: Return, safety, global mode, critical service/status and controls that must remain readable while the scene moves.
- `TRANSITIONAL`: temporary focus/reveal cues that may originate at a world anchor and resolve into a screen reading layer.

A cue may not borrow another owner's behavior merely because the layout is easier. In particular, world-bound route/node information must not become a stack of screen-fixed cards, and Return/safety controls must not masquerade as physical objects in the landscape.

### Required depth evidence

For `WORLD_BOUND` cues, use at least two scene-consistent depth signals when the carrier permits them:

1. registered position relative to the scene/object;
2. scale or density attenuation with distance;
3. partial occlusion by legitimate scene geometry;
4. perspective/orientation alignment;
5. local motion/parallax consistent with the scene;
6. controlled label leader anchored to the object rather than to the screen grid.

Occlusion is evidence of ownership, not decoration. Never invent terrain, object geometry, GPS position or visibility merely to create an occlusion effect.

For `SCREEN_BOUND` cues, preserve stable safe-area placement, target size and reading priority through scene movement. Return/safety may visually dominate a world cue when the task or operational state requires it.

### Attack tests

Before promotion, run:

- `SCENE-MOVE TEST`: mentally or actually pan the scene; world-bound cues should move/occlude with it while screen-bound controls remain stable.
- `BACKGROUND-OFF TEST`: remove scenery; any cue that only appears world-bound because of decorative background treatment is REVISE.
- `OVERLAY-FLAT TEST`: flatten all cues to one UI plane; if the result is nearly indistinguishable from the candidate, depth ownership is not doing real work.
- `OCCLUSION TEST`: verify every occlusion is caused by authorized scene geometry, not by a decorative mask.
- `RETURN-PRIORITY TEST`: scene depth must never bury Return/safety/system-critical controls.
- `STATIC-FALLBACK TEST`: when tracking/parallax is unavailable, the fallback must remain truthful and readable without pretending to be registered AR.

### Hard failures

REVISE/REJECT when any of the following occurs:

- route/node/object cues read as generic screen-fixed HUD stickers over a background image;
- a screen-fixed label claims precise world registration without tracking/GPS/field authority;
- fake occlusion or invented terrain is introduced to simulate depth;
- parallax, blur or glow is used as the sole evidence that a cue belongs to the world;
- Return/safety becomes scene-occluded or moves with the world;
- a world cue remains the same size, position and overlap behavior across a large scene move without a declared diagram mode;
- decorative depth effects make `UNKNOWN` look like verified location/status.

### Review record

Record at minimum:

`SURFACE_ID / CUE_ID / DEPTH_OWNER / WORLD_ANCHOR_OR_SCREEN_ZONE / DEPTH_SIGNALS / OCCLUSION_SOURCE / TRACKING_OR_STATIC_MODE / RETURN_PRIORITY / FALLBACK_MODE / AUTHORITY_SOURCE / DOES_NOT_PROVE`.

Promotion test:

> Move the scene mentally or in the prototype: world-bound cues must keep believable depth/occlusion relations, while Return/safety controls remain readable without pretending to be in the landscape.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for mobile-specific crops, layered image derivatives, masks, transparency, texture and bounded raster/vector effects while retaining the recoverable source. Re-evaluate blur radius, texture scale, glow spread, contrast and detail density at actual narrow viewports; an effect that works on desktop may collapse legibility or increase visual noise on mobile. Image-processing effects may not delay the primary task, obscure safe-area controls or replace Reduced Motion/state parity.

## Review inheritance

Run real narrow-viewport readback. Mobile runtime success proves operation only; independent visual review remains separate.
