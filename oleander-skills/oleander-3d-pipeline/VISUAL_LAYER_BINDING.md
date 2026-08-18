# 3D Pipeline Visual Layer Binding

Status: **BINDING ONLY / NO NEW METHODOLOGY**

This file binds 3D visual output to existing OLEANDER review and training knowledge. It does not introduce a universal render look.

## Existing sources to inherit

1. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`, especially Model / Rendering professional checks.
2. Project-specific Current Design DNA / Visual Bible only when Current Authority explicitly makes it applicable.
3. Existing practice `06-practice/2026/2026-08-11-ip03-blender-cmf-comparison-lab-v1.20/` for bounded CMF/render comparison learning.
4. Existing practice `06-practice/2026/2026-08-16-technical-drawing-lineweight/` when 3D output becomes axonometric/vector technical communication.
5. `MOTION_LIBRARY_EFFECT_ATLAS.md` for 3D animation mechanisms such as explode/assemble, temporal material/light change and camera motion.
6. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for render post-processing, compositing and Illustrator/SVG presentation operators.

## Existing visual checks to apply

From Artifact Review v1.1: geometry and construction must remain credible; human/facility/railing/path scale must be plausible; material, roughness, reflection, light and environment must agree. Attractive lighting or material treatment may not hide floating, intersection, unsupported or otherwise incorrect geometry.

Do not impose the OLEANDER portfolio Visual Bible color/light recipe on unrelated projects. Reuse it only when it is a Current Design Source for that project.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for render passes, masks/alpha, layer compositing, exposure/color adjustment, Smart Object-linked render replacement, bounded atmospheric treatment and vector-safe annotation/effect work. Preserve the original render and geometry-derived source. Post-processing, retouch, generative background/people/sky replacement or distortion may create a presentation derivative, but may not repair or conceal invalid geometry, scale, construction, field truth or material logic. `2D FAUX 3D ≠ GEOMETRIC 3D` remains hard.

## Interaction cue escalation gate

When CMF, surface treatment or rendered appearance is being used to communicate a physical action, do not credit hue/value/finish as the primary interaction proof until the action survives removal of those later visual cues.

Default cue escalation order for physical-product interaction studies:

`GEOMETRY / STATE FEEDBACK → TACTILE / SURFACE → MARKING → VALUE → HUE / CHROMA`.

Rules:

1. Geometry/state feedback owns the primary action relation whenever practical: travel direction, stop/detent, exposed/hidden state, mechanical separation, hinge/pivot, squeeze zone, slide channel or release boundary.
2. Tactile/surface cues may reinforce grip, contact or manipulation zones but may not invent an action unsupported by geometry/state feedback.
3. Marking may clarify an already legible action; text/arrow labels are not accepted as the sole discoverability mechanism for routine manipulation.
4. Value and hue/chroma are salience amplifiers. They may strengthen part distinction or state recognition but may not be used to claim reliable Slide/Wring/Release semantics by themselves.
5. A visually attractive render is a presentation carrier, not evidence that an ambiguous interaction is discoverable.
6. For wet-hand, force-dependent, safety-relevant or repeated-use interactions, digital visual proof remains incomplete until the corresponding physical task is tested.

### Required failure-seeking readback

For every interaction-signalling CMF study, run these removals in order and record the result:

- `COLOR_OFF` — remove hue/chroma. Intended action must remain inferable.
- `MARK_OFF` — remove text/arrows/printed symbols. Geometry + state + tactile structure should still carry the core action.
- `SURFACE_OFF` — remove ribs/texture/finish differences. If the action collapses completely, state whether geometry must change or whether tactile-only discovery is intentionally being tested physically.
- `POLISH_OFF` — inspect neutral-light / low-style output so highlight control, glossy edges or dramatic lighting cannot masquerade as interaction clarity.

Hard failures:

- hue/value is the only reason a movable or releasable part appears actionable;
- a stronger local contrast is treated as proof of action direction;
- render polish hides that two mechanically different states have the same silhouette/state relation;
- a diagnostic exploded/reveal view is used to claim normal-use discoverability without a normal-use carrier;
- physical interaction risk is promoted from digital evidence alone.

Record at minimum:

`INTERACTION_ID / TARGET_ACTION / PRIMARY_GEOMETRY_CUE / STATE_FEEDBACK / TACTILE_CUE / MARKING_CUE / VALUE_CUE / HUE_CUE / COLOR_OFF_RESULT / MARK_OFF_RESULT / SURFACE_OFF_RESULT / PHYSICAL_VALIDATION_REQUIRED / DOES_NOT_PROVE`.

Promotion test: **Remove hue, marking and texture in that order: the intended action must remain inferable from geometry/state feedback before any CMF signal is credited.**

## Lifecycle evidence framing gate

When a render or comparison board is used to make a lifecycle claim such as `WET`, `WATERMARK`, `DIRTY-WIPED`, `SCRATCHED` or `AGED`, the camera scale must be chosen from the decision claim rather than from the desire to make the defect visually dramatic.

Default evidence ladder:

`WHOLE PRODUCT → LOCAL CONTEXT → INTERFACE / DETAIL`.

Rules:

1. Use the **minimum sufficient carrier** for the claim. Whole-product continuity requires a whole/context view; local residue may use a bounded local-context carrier; interface discontinuity must retain the adjacent materials/mechanism that make the interface meaningful.
2. Every attacked state requires a **baseline pair** at the same camera, crop, light geometry and exposure unless the comparison explicitly states otherwise. Do not change crop or exposure inside a pair to rescue or exaggerate a direction.
3. Carrier changes are allowed **between different claims**, not within a baseline–attack pair. A state-specific view is valid only when the decision question changes with it.
4. A macro/detail view may diagnose a local phenomenon but may not by itself claim whole-product failure, cleanliness collapse or lifecycle severity.
5. Preserve enough stable geometry in every non-whole carrier to recover where the crop belongs on the product. Orphan macro crops are not accepted as primary lifecycle evidence.
6. Rendering, compositing or post-processing may expose a lifecycle proxy but may not manufacture dirt, wetness, scratch depth, ageing extent or service-life consequence beyond the declared digital hypothesis.

### Required failure-seeking readback

- `BASELINE_PAIR` — baseline and attack use matched camera/crop/light/exposure.
- `WHOLE_CONSEQUENCE` — if the claim is global, inspect the whole-product carrier rather than inferring from a macro crop.
- `CROP_RETURN` — reviewer can identify where a local/detail carrier belongs on the parent product without guessing.
- `SEVERITY_LOCK` — hold crop and exposure constant; the claimed severity must survive.
- `CLAIM_CARRIER` — verify that the selected carrier answers the stated decision question and is not simply the most dramatic frame.
- `NEUTRAL_LIGHT` — when highlight or sheen is part of the lifecycle signal, retain a neutral-light readback so stylized lighting cannot manufacture failure.

Hard failures:

- every lifecycle state is shown as a macro/detail crop regardless of claim;
- a local stain, watermark or scratch is described as whole-product failure without contextual evidence;
- baseline and attacked states use different framing/exposure without explicit analytical reason;
- crop scale itself becomes the apparent severity variable;
- a lifecycle proxy is promoted as measured durability, chemistry, friction, ageing rate or service life.

Record at minimum:

`LIFECYCLE_STATE / DECISION_CLAIM / CARRIER_SCALE / PARENT_PRODUCT_ANCHOR / BASELINE_ID / ATTACK_ID / CAMERA_LOCK / CROP_LOCK / LIGHT_LOCK / EXPOSURE_LOCK / WHOLE_CONSEQUENCE_REQUIRED / PHYSICAL_VALIDATION_REQUIRED / DOES_NOT_PROVE`.

Promotion test: **For every lifecycle claim, prove the minimum sufficient context and a locked baseline pair; severity must survive when crop and exposure are held constant.**

## Review inheritance

Review real renders and model views at the intended camera distance. `Render PASS ≠ Design PASS`; material/light success does not promote geometry, field evidence or engineering truth.
