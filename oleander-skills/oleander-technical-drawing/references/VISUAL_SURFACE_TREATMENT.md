# Visual Surface Treatment — texture, gradient and materiality gate

Status: candidate / Notion-derived executable companion. Knowledge authority remains the OLEANDER Notion Skill object; this file is an implementation reference, not the knowledge authority.

## Purpose

Use this module after spatial/technical semantics are resolved. It governs `GRADIENT / TEXTURE / GRAIN / PATTERN / HATCH / STIPPLE / OPACITY / SHADOW / BLUR / GLOW / EDGE_MODULATION` so surface effects add legibility or materiality without inventing spatial truth.

`SURFACE EFFECT PRESENT != MATERIAL TRUTH`

`GRADIENT PRESENT != CONTINUOUS DATA`

`TEXTURE PRESENT != REAL MATERIAL`

`OPACITY / SHADOW != SPATIAL EVIDENCE`

`PRETTY NOISE != PROFESSIONAL FINISH`

## 1. Declare the surface role before styling

Every material surface treatment must own exactly one primary role:

- `ANALYTICAL_FIELD` — carries a source-grounded or explicitly provisional continuous variable/field.
- `MATERIAL_SURFACE` — carries material/surface identity or a declared material hypothesis.
- `HIERARCHY_RECESSION` — pushes base/context evidence backward so the current task layer reads first; it is not data.
- `PRESENTATIONAL_ATMOSPHERE` — mood/depth/presentation only; mark `NON_EVIDENCE`.
- `REFERENCE_FIDELITY` — reproduces source-visible tone, paper, grain, print or material appearance for reconstruction fidelity; does not become semantic/material authority.

A treatment with no semantic owner or role is decorative by default and must not enter a professional analytical/technical artifact as proof.

## 2. Gradient grammar

A gradient must register:

`ROLE -> MAPPED VARIABLE (if analytical) -> AXIS/FIELD LOGIC -> STOPS/RANGE -> INTERPOLATION -> WHY -> OFF-STATE`

Allowed spatial logics include linear axis, radial field, distance field, along-path, slope-oriented, hydrological direction, bounded local mask, or another explicit relation.

Rules:

- `ANALYTICAL_FIELD` gradients require a named variable and legend/scale reference.
- Categorical/discrete states must not be made to look continuous unless the gradient is explicitly non-semantic presentation.
- `HIERARCHY_RECESSION` and `PRESENTATIONAL_ATMOSPHERE` must not claim a mapped physical/data variable.
- `Gradient OFF` must leave the geometry/topology/core relation intelligible; the gradient may carry the continuous value but cannot be the only proof that the base geometry exists.
- Avoid multi-directional or rainbow gradients with no analytical/material basis.

## 3. Texture grammar

A texture must register:

`OWNER -> ROLE -> SCALE -> DENSITY RANGE -> DIRECTIONALITY -> LOCAL MASK -> VARIATION/SEED -> CONTRAST -> FAILURE TRIGGER`

Distinguish:

- `HATCH / LINE_TEXTURE` — direction, cut, layer, material build-up or flow structure.
- `STIPPLE / POINT_TEXTURE` — density, particulate/vegetation field, print grain or bounded surface variation.
- `PATTERN` — repeated module/organization whose repetition is itself meaningful.
- `GRAIN` — micro visual/material/print grain; normally material or reconstruction fidelity, not route/data authority.
- `MACRO_VEIN_LAYER_ABRASION` — larger veins/layers/wear; bind to material structure or explicit design hypothesis.

Uniform noise across the whole sheet is not a material system. A single raster overlay cannot silently become material or geometry authority.

## 4. Multi-scale surface reading

Review surface treatments at three distances:

`NEAR STRUCTURE -> MID RHYTHM -> FAR FIELD`

- Near: texture unit/edge/line must remain legible without false precision or dirty noise.
- Mid: density/direction/repetition should form a stable rhythm.
- Far: treatment should collapse into the intended field/hierarchy without swallowing the primary relation.

## 5. Material truth boundary

Reuse Role-Bound CMF logic: variable finish/texture belongs to a material/part/region role, not decorative appetite.

Declare one material truth state:

- `SOURCE_CONFIRMED`
- `DESIGN_HYPOTHESIS`
- `REFERENCE_VISIBLE_ONLY`
- `NON_MATERIAL_PRESENTATION`

A realistic texture with `DESIGN_HYPOTHESIS` or `REFERENCE_VISIBLE_ONLY` does not prove real installed material, process, durability, roughness, ageing or field condition.

## 6. Opacity, shadow, blur and glow

- `OPACITY`: hierarchy recession, overlay separation or uncertainty. If it carries uncertainty, bind a legend/scale.
- `SHADOW`: layer/axon/edge depth explanation only; never substitutes for support, thickness or connection geometry.
- `BLUR`: non-authoritative background, atmosphere or explicit uncertainty; never blur a boundary and then claim precise registration.
- `GLOW`: only when there is a real/emulated luminous field/state basis or reference-fidelity requirement. Generic 'tech' glow is presentation, not analysis.

## 7. Mandatory attack tests

When treatment is material to the result, register:

`FLAT MASTER -> GRADIENT OFF -> TEXTURE OFF -> OPACITY/HIERARCHY OFF -> GRAYSCALE -> NEAR/MID/FAR -> SMALL/PRINT FALLBACK`

Conditional rules:

- If a gradient is used, `gradient_off` must be reviewed.
- If texture/pattern/grain/hatch/stipple is used, `texture_off` must be reviewed.
- If color carries semantic classes/continuous values, grayscale must be reviewed or an explicit reason given why grayscale equivalence is not expected.
- If treatment is visible only at one zoom and collapses to dirt/noise at small size, revise density/contrast or retire it at that scale.

## 8. Machine register

Use `VISUAL_SURFACE_REGISTER` with at least:

- `surface_id`
- `semantic_owner_id`
- `surface_role`
- `source_basis`
- `truth_state`
- `technique`
- `does_not_prove`
- `off_state_result`
- `near_mid_far_review`
- technique-specific fields for gradient or texture

Machine validator: `tools/validate_visual_surface_treatment.py`.

Machine PASS only proves contract consistency. It does not prove taste, material realism, visual excellence, professional finish, Design KEEP, Engineering PASS, Field PASS or Promotion.
