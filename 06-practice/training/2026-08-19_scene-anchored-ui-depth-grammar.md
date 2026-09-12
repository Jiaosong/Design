# 2026-08-19｜Mobile Game UI / L5｜Scene-Anchored UI Depth Grammar

Status: `EXECUTED / PRODUCER PIXEL READBACK COMPLETE / KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT PROFESSIONAL DESIGN REVIEW HOLD / NO_PROMOTION`

## Project trigger

C04 ROUTE review history identified a persistent quality problem: the route experience could still read as a 2D UI overlay over landscape rather than as a world-first interactive surface. The recent `World-Viewport Framing` training already addressed whole-world miniaturization; this round targets the next distinct layer: **depth ownership** of cues inside a moving/world view.

Current reusable Skill checked first: `skills/oleander-mobile-game-ui/VISUAL_LAYER_BINDING.md`. It already requires mobile recomposition, narrow-viewport readback, safe-area clarity and effect reduction, but did not state which cues belong to the world versus the screen or how to prove that visually.

## Training question

How can a game-like mobile route surface avoid looking like flat HUD stickers while preserving Return/safety as stable screen controls?

## Actual practice asset

Editable 1920×1080 SVG: `OLEANDER_SCENE_ANCHORED_UI_DEPTH_GRAMMAR_R01.svg`.

The exercise uses synthetic terrain only; it does not reproduce or claim C04 field geometry.

- REJECT: route, R06/R13 nodes, explanation and Return all occupy one screen-fixed plane.
- KEEP candidate: route/node/local labels become `WORLD_BOUND`; Return/global context remain `SCREEN_BOUND`.
- World-bound cues use registered scene position, distance attenuation and legitimate terrain occlusion.
- Screen-bound controls remain stable in safe-area positions and do not pretend to be physical landscape objects.

No image generation was used. All visible content is vector.

## Pixel readback and repair

First rendered candidate exposed a right-panel subtitle overflow. The subtitle was shortened, the SVG was re-rendered and the final PNG + 50% grayscale derivative were reopened.

Final local hashes:

- SVG SHA256: `35eff8e70f32fabd03b7e8739279fca397dc82e9ab153f233b5bdaeee57a7334`
- PNG SHA256: `b620ac1ba1c60148c84aae9fb4f1a3544e4c261efc31b59681fe6602482648b2`
- Gray50 SHA256: `2dc7029bebd96fe99ac6d9175308d4ab0d789c15166a043dfcb571d101f2db24`

## Design Crit

### Execution / compliance gate

`PASS FOR TRAINING EXECUTION`

- editable vector master exists;
- actual PNG and grayscale readback completed after final edit;
- no generated imagery;
- no GPS, field-distance, route-geometry or AR-registration claim;
- Return/safety is not hidden behind world geometry.

### Professional design gate — producer frozen rubric

`KEEP-FOR-TRAINING CANDIDATE`

- **First visual:** PASS. The reject side reads as a flat overlay; the keep side reads as scene + sparse screen chrome before explanatory copy.
- **Composition:** PASS. Landscape/world remains dominant; UI control density is lower on the keep side.
- **Proportion:** PASS. World labels are smaller and distance-sensitive; Return remains stable and large enough to own screen priority.
- **Hierarchy:** PASS. `world → local anchor → global control → metadata` is legible.
- **Typography:** PASS after subtitle overflow repair. Labels remain subordinate to scene geometry.
- **Material / spatial truth:** PASS only as synthetic schematic training. No site material or measured spatial truth is claimed.
- **Scale:** HOLD for production. The board demonstrates relative ownership, not real device ergonomics or field viewing distance.
- **Node readability:** PASS. R06 foreground and R13 farther anchor remain distinguishable without becoming equal card modules.
- **Interaction / narrative:** PASS as a static depth-ownership proof; live tracking/parallax behavior remains unproven.
- **Professional finish:** KEEP-for-training candidate; not C04 MAIN.

Independent Professional Design Reviewer provenance is unavailable in the current tool surface. Therefore the independent Design Gate remains `HOLD / REVIEW REQUIRED`; producer readback is not relabeled as independent review.

## Failure knowledge

1. **Parallax-looking decoration is not depth ownership.** Blur/glow/scale effects cannot substitute for registered scene relation.
2. **All-overlay consistency is a failure mode.** If route, node, label, Return and explanation all obey one screen grid, the world becomes a wallpaper.
3. **Fake occlusion is evidence invention.** A decorative mask or invented terrain cannot be used to make a cue look world-bound.
4. **Return must not be world-owned.** A system/safety control that moves behind terrain or depends on local scene visibility violates task priority.
5. **Static world labels must not imply AR/GPS authority.** When tracking is unavailable, use a truthful diagram/static fallback rather than simulated precision.

## Effective repair

Classify every cue before styling:

`WORLD_BOUND / SCREEN_BOUND / TRANSITIONAL`

Then test:

`SCENE-MOVE → BACKGROUND-OFF → OVERLAY-FLAT → OCCLUSION → RETURN-PRIORITY → STATIC-FALLBACK`.

## Skill delta

Modified existing `skills/oleander-mobile-game-ui/VISUAL_LAYER_BINDING.md`; no new Skill created.

Before: mobile recomposition and effect reduction were required, but the binding did not define depth owners or prevent flat HUD overlay treatment.

After: adds `Scene-anchored depth grammar gate`, including:

- `WORLD_BOUND / SCREEN_BOUND / TRANSITIONAL` classification;
- minimum scene-consistent depth evidence for world cues;
- explicit Return/safety screen ownership;
- fake-occlusion and false-registration hard failures;
- six attack tests;
- machine-review fields: `SURFACE_ID / CUE_ID / DEPTH_OWNER / WORLD_ANCHOR_OR_SCREEN_ZONE / DEPTH_SIGNALS / OCCLUSION_SOURCE / TRACKING_OR_STATIC_MODE / RETURN_PRIORITY / FALLBACK_MODE / AUTHORITY_SOURCE / DOES_NOT_PROVE`.

Promotion test:

> Move the scene mentally or in the prototype: world-bound cues must keep believable depth/occlusion relations, while Return/safety controls remain readable without pretending to be in the landscape.

## Cross-project transfer

Applicable to:

- C04 ROUTE / R06 / R13 world-first mobile surfaces;
- museum/travel companion interfaces;
- map + scene hybrid navigation;
- game-like exploration HUDs;
- 3D viewers with object labels plus global controls;
- product configurators where object annotations must belong to geometry while checkout/safety/system controls remain screen-owned.

Not automatically applicable to:

- conventional 2D maps intentionally operating in diagram mode;
- dashboards where all information is legitimately screen-space;
- regulated AR/navigation claims without tracking/GPS/field authority;
- emergency/safety systems whose screen-fixed controls must override immersive depth;
- static editorial illustrations that make no registration claim.

## Truth boundary

`TRAINING ONLY / SYNTHETIC TERRAIN / NTS / NOT GPS / FIELD OPEN / NO IMAGE GENERATION / NOT C04 MAIN / NO_PROMOTION`.
