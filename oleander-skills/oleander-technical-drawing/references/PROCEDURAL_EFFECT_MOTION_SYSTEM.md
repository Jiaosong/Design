# OLEANDER Technical Drawing — Procedural Effect & Motion System v0.2

**Status:** `CANDIDATE / NO_PROMOTION`  
**Knowledge authority:** Notion `KN-METHOD-TECHDRAW-SPATIAL-TRANSLATION-001`  
**Motion runtime owner:** `oleander-motion`  

This system converts the Surface Treatment Gate into executable parameters, SVG recipes, motion handoffs and regression fixtures.

It is not an effect catalogue. The order is:

`Decision Question → Semantic Owner → Graphic Carrier → Effect Role → Parameter Instance → OFF / Reduced State → Near/Mid/Far → Runtime / Actual Preview → Keep/Reduce/Remove`

Never use:

`Cool Effect → Find a place to apply it`.

## 1. Files

- Core parameter library: `VISUAL_EFFECT_PARAMETER_LIBRARY.json`
- Extension parameters: `VISUAL_EFFECT_PARAMETER_EXTENSION_02.json`
- SVG recipes: `../recipes/SVG_PROCEDURAL_RECIPES.json`
- Motion handoff recipes: `../recipes/MOTION_HANDOFF_RECIPES.json`
- Cross-skill routing: `../recipes/CROSS_SKILL_EFFECT_ROUTES.json`
- Core recipe validator: `../tools/validate_effect_recipe_register.py`
- Parameter-library validator: `../tools/validate_effect_parameter_library.py`
- Extension validator: `../tools/validate_effect_extension_02.py`
- Core SVG builder: `../tools/build_svg_effect_atlas.py`
- Core native motion builder: `../tools/build_motion_recipe_demo.py`
- Extension SVG builder: `../tools/build_svg_effect_extension_02.py`
- Extension native motion builder: `../tools/build_motion_extension_02_demo.py`
- Golden fixtures: `EFFECT-RECIPE-01_REGISTER.json` + `EFFECT-RECIPE-02_EXTENDED_REGISTER.json`

## 2. Effect ownership

Every effect instance must have `semantic_owner_id`.

Allowed role families:

- `ANALYTICAL_FIELD` — a real mapped/derived variable; legend required.
- `MATERIAL_SURFACE` — material/surface hypothesis or source-grounded identity.
- `HIERARCHY_RECESSION` — visual downweighting; must not masquerade as data.
- `PRESENTATIONAL_ATMOSPHERE` — explicitly non-evidence.
- `REFERENCE_FIDELITY` — source reconstruction only; may not upgrade authority.
- `STATE_EMISSION` — a real state/light owner; no generic glow.

If a role cannot be named, remove the effect.

## 3. Static SVG recipe groups

### Continuous fields
- `SVG-R01-LINEAR-FIELD`
- `SVG-R02-RADIAL-FIELD`

### Discrete / repeated textures
- `SVG-R03-HATCH`
- `SVG-R04-STIPPLE`
- `SVG-R09-CONTOUR-BANDS`
- `SVG-R12-HALFTONE`
- `SVG-R15-DASH-RHYTHM`

### Micro / material / print surface
- `SVG-R05-GRAIN`
- `SVG-R10-EDGE-MODULATION`
- `SVG-R13-PAPER-FIBER`

### Optical hierarchy / state
- `SVG-R06-SHADOW-DEPTH`
- `SVG-R08-GLOW-EMISSION`
- `SVG-R11-BLUR-FOCUS`
- `SVG-R14-BLEND-OVERLAY`

### Cross-skill source passes
- `SVG-R16-HILLSHADE-PASS` — requires GIS/DEM/source pass.
- `SVG-R17-AO-DEPTH-PASS` — requires same-camera 3D AO/depth/ID pass.
- `SVG-R18-SOURCE-CLIP-REVEAL` — direct-source presentation framing only; required scale/status/source labels remain.

### Conditional distortion
- `SVG-R07-DISPLACEMENT`

Allowed only for material/atmosphere/reference fidelity. Never apply to MAP_BOUND / authoritative analytical geometry.

## 4. Motion handoff groups

Motion recipes are specifications, not a second Motion Skill. Runtime implementation, Reduced Motion, device performance and AR-S10 are still owned by `oleander-motion`.

### Relation / continuity
- `TD-MR01-PATH-TRACE` → EF-03
- `TD-MR04-SHARED-CONTAINER-HANDOFF` → EF-01
- `TD-MR08-EXPLODE-ASSEMBLE` → EF-07
- `TD-MR13-TOPOLOGY-SAFE-MORPH` → EF-04
- `TD-MR19-VIEW-TRANSITION` → EF-10

### Reveal / hierarchy / attention
- `TD-MR02-MASK-REVEAL` → EF-02
- `TD-MR03-STRUCTURED-STAGGER` → EF-05
- `TD-MR10-BLUR-FOCUS` → EF-14
- `TD-MR15-KINETIC-TYPE` → EF-17

### Data / time / progress
- `TD-MR05-DATA-FILTER-REORDER` → EF-09
- `TD-MR07-SCROLL-PROGRESS` → EF-06

### Material / field
- `TD-MR06-LIGHT-MATERIAL-STATE` → EF-08
- `TD-MR11-GRAIN-EVOLUTION` → EF-15
- `TD-MR12-PARTICLE-FIELD` → EF-16
- `TD-MR14-REFRACTION-DISPLACEMENT` → EF-13

### Conditional interaction / spatial depth
- `TD-MR09-PARALLAX-DEPTH` → EF-12
- `TD-MR16-CAMERA-ORBIT-DOLLY-FOCUS` → EF-18
- `TD-MR17-CURSOR-LINKED-RESPONSE` → EF-19
- `TD-MR18-SMOOTH-SCROLL-INFRA` → EF-20
- `TD-MR20-DRAG-INERTIA` → EF-11

Conditional does not mean recommended-by-default. Parallax, refraction, cursor response, smooth scroll, kinetic type and camera motion require a named task/continuity role and an explicit fallback.

## 5. Cross-skill authority

Use `CROSS_SKILL_EFFECT_ROUTES.json` before applying a pass-derived or runtime effect.

- `oleander-data-viz / GIS` owns cleaned data, model, domain, CRS, hillshade/density/time-state evidence.
- `oleander-3d-pipeline` owns geometry, camera, depth, AO and object/material ID passes.
- `oleander-story-and-board` owns surrounding narrative framing and may not alter technical figure authority.
- `oleander-motion` owns runtime implementation, Reduced Motion, performance and AR-S10.
- `oleander-delivery-qc` owns export parity for alpha, ICC/color space, raster/vector retention and video/runtime delivery checks.

`UPSTREAM PASS AUTHORITY ≠ DOWNSTREAM PRESENTATION OWNERSHIP`.

## 6. Parameter discipline

Numbers in the libraries are `CANDIDATE STARTING RANGES`, not rules.

For every real use record:

`Owner / Role / Target Scale / Parameter Value / Source or Model / Why / OFF-state / Failure Trigger / Actual Preview`.

Motion additionally records:

`State Before / State After / Trigger / Duration or Progress Model / Easing or Physics / Interrupt / Reverse / Rapid Repeat / Reduced Motion / Runtime State`.

## 7. OFF / Reduced attack

Static:

`FLAT MASTER → EFFECT ON → GRADIENT OFF → TEXTURE OFF → OPTICAL EFFECT OFF → GRAYSCALE → NEAR/MID/FAR → SMALL/PRINT`

Motion:

`NO-MOTION BASELINE → CANDIDATE → TIMING/PHYSICS VARIANT → REDUCED MOTION → INTERRUPT/REVERSE/RAPID REPEAT → REAL RUNTIME`

Hard rule:

`EFFECT OFF ≠ INFORMATION OFF`.

If disabling an effect removes geometry, topology, required state or critical evidence, the effect has exceeded its authority.

## 8. Regression purpose

Fixture 01 covers the core set: analytical gradient, hatch, deterministic stipple, source-fidelity grain, hierarchy shadow, state glow, path trace, shared-container continuity, native scroll progress and modelled particle field.

Fixture 02 covers the conditional/cross-skill set: blur, halftone, paper fiber, source-pass blend, dash rhythm, synthetic hillshade mechanism, synthetic AO/depth mechanism, safe source clip, topology morph, refraction, kinetic type, camera, cursor response, smooth-scroll contract, view transition and interruptible drag.

Hillshade/AO/depth fixture graphics are explicitly `SYNTHETIC MECHANISM DEMO`; they do not substitute for GIS/DEM/model passes.

Negative regressions reject absent owner/legend/model/seed/pass provenance, unsafe source crop, map-bound displacement/refraction, motion without Reduced Motion, loss of native scroll/pointer/keyboard baseline, and machine-awarded KEEP.

CI executes two SVG builders and two native HTML/CSS/JS motion builders. Build success proves mechanism execution only.

## 9. Evidence boundary

`RECIPE EXECUTES ≠ EFFECT IS APPROPRIATE`  
`PARAMETER IN RANGE ≠ AESTHETIC PASS`  
`SVG FILTER ≠ MATERIAL TRUTH`  
`SYNTHETIC PASS DEMO ≠ GIS / 3D PASS`  
`MOTION DEMO ≠ AR-S10 PASS`  
`AUTOMATED PASS ≠ DESIGN KEEP`.
