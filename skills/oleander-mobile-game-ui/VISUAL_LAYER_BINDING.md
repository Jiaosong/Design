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

## Responsive media art-direction gate

Use this gate when the same evidence-bearing landscape, product, spatial image or scene must carry one claim across materially different viewports. Responsive image handling is not a neutral implementation detail: a crop can remove the object or relation that makes the claim true.

Separate `SOURCE GEOMETRY / FOCAL EVIDENCE / CARRIER CROP` before styling.

- `SOURCE GEOMETRY`: the authoritative or source-bound image/scene. Breakpoints may not redraw, invent or replace its factual relation merely to improve composition.
- `FOCAL EVIDENCE`: the minimum objects and relations that must remain perceivable for the current claim to survive.
- `CARRIER CROP`: breakpoint-specific framing. It may change subject placement, crop window, copy measure and vertical rhythm while preserving focal evidence and truth boundary.

Do not treat `object-fit: cover`, center-crop, automatic face/object detection or generic focal-point metadata as Design PASS. They are implementation mechanisms and still require target-size visual readback.

### Required breakpoint checks

For every evidence-bearing hero/scene, record at least one wide carrier and one narrow carrier. More are required when the product actually ships more materially different breakpoints.

Run:

- `CLAIM-OFF TEST`: hide copy; the focal evidence should still be visually locatable in each carrier.
- `FOCAL-EVIDENCE TEST`: list the required objects/relations and confirm none are cropped, hidden behind copy or reduced below useful reading size.
- `AUTO-CROP ATTACK`: compare the designed crop against a naive center/cover crop. If both are nearly identical, prove that no art direction was actually needed; otherwise the designed crop must materially preserve the claim better.
- `COPY-COLLISION TEST`: verify breakpoint-specific copy placement does not cover the evidence it describes.
- `RETURN/SAFETY TEST`: narrow art direction may not use the focal image area to bury Return, safety or critical state controls.
- `SOURCE-IDENTITY TEST`: desktop and mobile crops must trace to the same approved source/version unless an explicitly authorized alternate source is declared.
- `NATIVE-VIEWPORT READBACK`: review at actual target width/height, not only inside enlarged artboards.

### Hard failures

REVISE/REJECT when:

- a mobile center-crop removes a required object or relation while the copy still asks the user to see it;
- desktop and mobile silently use different landscape/product geometry to preserve a composition;
- breakpoint copy is placed over the exact evidence it references;
- zooming/cropping turns local evidence into a stronger or different factual claim;
- the same `object-position` is reused across carriers even though it causes evidence loss;
- a low-resolution source is enlarged beyond useful evidentiary reading and presented as if detail were verified;
- decorative AI/generative fill is used to extend missing landscape/product evidence outside the source frame.

### Review record

Record at minimum:

`MEDIA_ID / SOURCE_ID / SOURCE_VERSION / CLAIM_ID / FOCAL_OBJECTS / FOCAL_RELATIONS / BREAKPOINT / CROP_OR_VIEWBOX / COPY_SAFE_REGION / REQUIRED_CONTROL_SAFE_REGION / AUTO_CROP_RESULT / NATIVE_READBACK / DOES_NOT_PROVE`.

Promotion test:

> Across wide and narrow carriers, the composition may change but the evidence-bearing relation must not disappear, move to a different source geometry, or be manufactured by the crop.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for mobile-specific crops, layered image derivatives, masks, transparency, texture and bounded raster/vector effects while retaining the recoverable source. Re-evaluate blur radius, texture scale, glow spread, contrast and detail density at actual narrow viewports; an effect that works on desktop may collapse legibility or increase visual noise on mobile. Image-processing effects may not delay the primary task, obscure safe-area controls or replace Reduced Motion/state parity.

## Review inheritance

Run real narrow-viewport readback. Mobile runtime success proves operation only; independent visual review remains separate.
