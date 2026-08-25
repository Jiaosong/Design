# 3D Pipeline Visual Layer Binding

Status: **BINDING ONLY / NO NEW METHODOLOGY**

This file binds 3D visual output to existing OLEANDER review and training knowledge. It does not introduce a universal render look and does not override `SKILL.md` authority/state rules.

## Existing sources to inherit

1. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`, especially Model / Rendering professional checks.
2. Project-specific Current Design DNA / Visual Bible only when Current Authority explicitly makes it applicable.
3. Existing practice `06-practice/2026/2026-08-11-ip03-blender-cmf-comparison-lab-v1.20/` for bounded CMF/render comparison learning.
4. Existing practice `06-practice/2026/2026-08-16-technical-drawing-lineweight/` when 3D output becomes axonometric/vector technical communication.
5. `MOTION_LIBRARY_EFFECT_ATLAS.md` for 3D animation mechanisms such as explode/assemble, temporal material/light change and camera motion.
6. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for render post-processing, compositing and Illustrator/SVG presentation operators.
7. The Camera Claim Gate in `SKILL.md` whenever camera/projection is part of the design claim rather than a neutral carrier.

## Existing visual checks to apply

From Artifact Review v1.1: geometry and construction must remain credible; human/facility/railing/path scale must be plausible; material, roughness, reflection, light and environment must agree. Attractive lighting or material treatment may not hide floating, intersection, unsupported or otherwise incorrect geometry.

Do not impose the OLEANDER portfolio Visual Bible color/light recipe on unrelated projects. Reuse it only when it is a Current Design Source for that project.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for render passes, masks/alpha, layer compositing, exposure/color adjustment, Smart Object-linked render replacement, bounded atmospheric treatment and vector-safe annotation/effect work. Preserve the original render and geometry-derived source. Post-processing, retouch, generative background/people/sky replacement or distortion may create a presentation derivative, but may not repair or conceal invalid geometry, scale, construction, field truth or material logic. `2D FAUX 3D ≠ GEOMETRIC 3D` remains hard.

## Material identity gate

A shader name, texture slot, successful render or different base color does not by itself prove professional material identity or CMF separation.

Use a controlled camera/light condition before artistic lighting variants, then separate at least the applicable material roles:
`BASE COLOR / CONDUCTOR-DIELECTRIC BEHAVIOR / ROUGHNESS-SPECULAR RESPONSE / NORMAL-RELIEF / OCCLUSION / TEXTURE SCALE-DIRECTION / EDGE BEHAVIOR`.

Rules:
1. Do not collapse material identity into hue alone. Metalness/conductor behavior, roughness response and dielectric behavior remain semantically distinct where the renderer exposes them.
2. Texture frequency, scale and direction must be plausible at modeled object scale and the intended camera distance. Visible tiling/repetition, arbitrary procedural grain or wrong grain scale is `REVISE` even when the texture technically loads.
3. Material families should remain reasonably distinguishable when hue is reduced. Run grayscale/desaturation when color may be carrying too much of the identity.
4. Edge response is part of material reading. Sharp, chipped, rounded, laminated, oxidized, cut, end-grain, polished or weathered edges must agree with the intended material/fabrication logic; generic edge wear is not a substitute.
5. Reject `gray model + color labels` as a finished material system when named materials share nearly identical roughness, highlight behavior, texture scale and edge response.
6. Review at two scales: first read tests material-family separation on the whole object; near read tests surface behavior. Microtexture visible only in a close crop cannot prove distant hero-view realism.
7. Controlled comparisons lock geometry, camera, light and applicable postprocess. A change in exposure/crop cannot be used to make one material appear more distinct.
8. Keep truth boundaries explicit. Digital material separation does not prove measured reflectance, approved physical sample, weathering life, fire/slip performance, fabrication quality or field installation.
9. If the required renderer/runtime is unavailable, a deterministic calibration board may test hierarchy/response logic but cannot substitute for final runtime/PBR validation.
10. Use renderer shader models (for example metallic-roughness categories) as implementation compatibility models only, not as proof that a real material physically matches the shader.

Failure-seeking readback:
- `COLOR_OFF` — material family remains distinguishable without hue doing all the work;
- `NEUTRAL_LIGHT` — artistic lighting cannot manufacture separation;
- `TEXTURE_SCALE` — texture frequency/direction survives object-scale check;
- `EDGE_BEHAVIOR` — edge treatment agrees with fabrication/material logic;
- `WHOLE_VS_DETAIL` — close-up microdetail does not overclaim whole-object material realism.

Record at minimum:
`MATERIAL_ID / CLAIMED_FAMILY / SHADER_MODEL / BASE_COLOR_ROLE / ROUGHNESS_SPECULAR_ROLE / TEXTURE_SCALE_DIRECTION / EDGE_BEHAVIOR / CAMERA_LIGHT_LOCK / COLOR_OFF_RESULT / WHOLE_DETAIL_RESULT / PHYSICAL_VALIDATION_REQUIRED / DOES_NOT_PROVE`.

## Interaction cue escalation gate

When CMF, surface treatment or rendered appearance is used to communicate a physical action, do not credit hue/value/finish as the primary interaction proof until the action survives removal of those later cues.

Default escalation:

`GEOMETRY / STATE FEEDBACK → TACTILE / SURFACE → MARKING → VALUE → HUE / CHROMA`

Rules:

1. Geometry/state feedback owns the primary action relation whenever practical: travel direction, stop/detent, exposed/hidden state, mechanical separation, hinge/pivot, squeeze zone, slide channel or release boundary.
2. Tactile/surface cues may reinforce grip/contact/manipulation zones but may not invent an action unsupported by geometry/state feedback.
3. Marking may clarify an already legible action; text/arrows are not accepted as the sole routine discoverability mechanism.
4. Value and hue/chroma are salience amplifiers, not standalone proof of Slide/Wring/Release semantics.
5. A polished render is a presentation carrier, not evidence that an ambiguous interaction is discoverable.
6. Wet-hand, force-dependent, safety-relevant or repeated-use interactions remain physically unproven until corresponding real task evidence exists.

### Failure-seeking readback

- `COLOR_OFF` — remove hue/chroma; intended action should remain inferable.
- `MARK_OFF` — remove text/arrows/symbols; geometry + state + tactile structure should still carry the core action.
- `SURFACE_OFF` — remove ribs/texture/finish; if the action collapses, state whether geometry must change or tactile-only discovery requires physical validation.
- `POLISH_OFF` — inspect neutral-light / low-style output so highlight control and dramatic lighting cannot masquerade as clarity.

Hard failures:

- hue/value is the only reason a movable/releasable part appears actionable;
- stronger local contrast is treated as proof of action direction;
- render polish hides that mechanically different states have the same silhouette/state relation;
- diagnostic exploded/reveal view is used to claim normal-use discoverability without a normal-use carrier;
- physical interaction risk is promoted from digital evidence alone.

Record at minimum:

`INTERACTION_ID / TARGET_ACTION / PRIMARY_GEOMETRY_CUE / STATE_FEEDBACK / TACTILE_CUE / MARKING_CUE / VALUE_CUE / HUE_CUE / COLOR_OFF_RESULT / MARK_OFF_RESULT / SURFACE_OFF_RESULT / PHYSICAL_VALIDATION_REQUIRED / DOES_NOT_PROVE`.

Promotion test: **Remove hue, marking and texture in that order: the intended action must remain inferable from geometry/state feedback before CMF signal is credited.**

## Lifecycle evidence framing gate

When a render/comparison board makes a lifecycle claim such as `WET`, `WATERMARK`, `DIRTY-WIPED`, `SCRATCHED` or `AGED`, camera scale must come from the decision claim, not the desire to make the defect dramatic.

Default evidence ladder:

`WHOLE PRODUCT → LOCAL CONTEXT → INTERFACE / DETAIL`

Rules:

1. Use the **minimum sufficient carrier**. Whole-product continuity needs whole/context evidence; local residue may use bounded local context; interface discontinuity must retain adjacent materials/mechanism.
2. Every attacked state requires a matched baseline at the same camera, crop, light geometry and exposure unless explicitly justified otherwise.
3. Carrier changes are allowed between different claims, not within a baseline–attack pair.
4. Macro/detail may diagnose local phenomena but cannot by itself prove whole-product failure, cleanliness collapse or lifecycle severity.
5. Preserve enough stable geometry to recover where every local/detail crop belongs. Orphan macros are not primary lifecycle evidence.
6. Rendering/compositing may expose a lifecycle proxy but may not manufacture dirt, wetness, scratch depth, ageing extent or service-life consequence beyond the declared hypothesis.

### Failure-seeking readback

- `BASELINE_PAIR` — baseline/attack framing, light and exposure match.
- `WHOLE_CONSEQUENCE` — global claims are checked on a whole/context carrier.
- `CROP_RETURN` — local carrier can be located on the parent product without guessing.
- `SEVERITY_LOCK` — severity survives constant crop/exposure.
- `CLAIM_CARRIER` — carrier answers the decision question, not merely the most dramatic frame.
- `NEUTRAL_LIGHT` — retain a neutral-light readback when sheen/highlight drives the signal.

Hard failures:

- every lifecycle state is shown as macro/detail regardless of claim;
- local stain/watermark/scratch is described as whole-product failure without context;
- baseline and attacked states use different framing/exposure without analytical reason;
- crop scale becomes the apparent severity variable;
- digital proxy is promoted as measured durability, chemistry, friction, ageing rate or service life.

Record at minimum:

`LIFECYCLE_STATE / DECISION_CLAIM / CARRIER_SCALE / PARENT_PRODUCT_ANCHOR / BASELINE_ID / ATTACK_ID / CAMERA_LOCK / CROP_LOCK / LIGHT_LOCK / EXPOSURE_LOCK / WHOLE_CONSEQUENCE_REQUIRED / PHYSICAL_VALIDATION_REQUIRED / DOES_NOT_PROVE`.

Promotion test: **For every lifecycle claim, prove the minimum sufficient context and a locked baseline pair; severity must survive when crop and exposure are held constant.**

## Cross-media correspondence gate

Use this gate whenever the same design object is represented across two or more of: plan, section, axonometric, model view, render, diagram, technical detail, or interactive spatial view.

Default sequence:

`SOURCE AUTHORITY → SHARED ANCHORS → INVARIANTS → MEDIA TRANSLATION → SIDE-BY-SIDE READ → MEDIUM-SPECIFIC CRIT`

Rules:
1. Declare stable correspondence anchors before styling: durable IDs for the minimum places, joints, edges, route decisions, datum points, section cuts, cameras, components or objects that must remain recognisable across media.
2. Separate invariants from reprojectable properties. Anchor identity, order, adjacency, side-of-relation and design role are invariant; camera, projection, crop, graphic style and local silhouette may change when the medium requires it.
3. Shared labels are not proof of correspondence. If two views carry the same ID but depict a different order, adjacency, side, elevation relation, component role or termination logic, mark `REVISE / REJECT`.
4. Derived views may not locally redraw authoritative geometry merely to improve composition. Change camera, crop, hierarchy, linework, annotation or framing first.
5. When exact survey/field geometry is unavailable, preserve only the relation Current Authority supports and keep synthetic/inferred/provisional/NTS status explicit.
6. Where a relation crosses plan/section/model boundaries, use at least one explicit binding mechanism: shared anchor IDs, cut IDs, camera IDs, callouts, datum names, object IDs or correspondence table.
7. Review the set side by side. A reviewer should be able to follow the same object/sequence without relying on captions alone.
8. `MODEL/RENDER QUALITY ≠ CORRESPONDENCE QUALITY`. A clean render may still depict a different relation from plan/section; a technically corresponding model may still fail medium-specific design quality.
9. For route/sequence work verify stable order and branch logic; for assemblies/details verify component identity, joint location, side and termination logic.
10. Correspondence PASS never proves material realism, field accuracy, engineering approval, accessibility or overall Design PASS.

Record at minimum:
`OBJECT_ID / SOURCE_AUTHORITY / VIEW_IDS / SHARED_ANCHORS / INVARIANTS / REPROJECTABLE_PROPERTIES / CORRESPONDENCE_RESULT / MEDIUM_SPECIFIC_REVIEW / DOES_NOT_PROVE`.

## Dimension-to-object binding gate

Use this gate whenever a model, axonometric, orthographic, exploded view or technical presentation contains dimensions intended to prove scale, clearance, position, component size, body relationship or installation relation.

Default review order:

`SOURCE VALUE → MEASURED OBJECT / INTERVAL → ATTACHMENT CARRIER → FIRST-READ MODEL → NEAR-READ DIMENSION → TRUTH BOUNDARY`

Rules:
1. A dimension is not visually present merely because its number exists in a register/table/nearby note. The measured object, interval, edge, datum or relation must be unambiguous in the intended view.
2. Bind critical dimensions directly with extension lines, witness lines, leaders, aligned dimensions, section references or another explicit geometric carrier appropriate to the medium.
3. Separate `CRITICAL ATTACHED DIMENSIONS` from `SECONDARY SCALE / PARAMETER RAILS`. First-interpretation values stay on-object; repeated/supporting values may move to a near-read rail.
4. Annotation may not destroy first-read model/body/joint/route evidence. Revise projection, spacing, crop, leader routing or page allocation instead of detaching critical values.
5. Human/ergonomic dimensions must name the body condition they refer to and may not imply percentile/accessibility/population standards without supporting evidence.
6. Nominal/model dimensions, scenario values, field measurements and engineering tolerances are different evidence classes. Keep source class and `DOES NOT PROVE` adjacent when consequential.
7. `MODEL SCALE READ ≠ FIELD MEASUREMENT ≠ ENGINEERING APPROVAL`.
8. Numeric source authority owns value/unit/interval/datum. Presentation may alter leader position, spacing, hierarchy and weight, not the number or measured relation.
9. Review at two distances: first read keeps the object dominant; near read lets every critical value trace to the exact object/interval.
10. Promotion requires target-size reopened proof. Export success, dimension text presence or a clean parameter table cannot substitute for on-object legibility.

Record at minimum:
`DIMENSION_ID / SOURCE_VALUE / UNIT / EVIDENCE_CLASS / OBJECT_OR_INTERVAL / DATUM / ATTACHMENT_CARRIER / FIRST_READ_RESULT / NEAR_READ_RESULT / DOES_NOT_PROVE`.

## Review inheritance

Review real renders and model views at the intended camera distance and final carrier size. `Render PASS ≠ Design PASS`; material/light success does not promote geometry, field evidence, physical interaction, lifecycle truth or engineering validity.
