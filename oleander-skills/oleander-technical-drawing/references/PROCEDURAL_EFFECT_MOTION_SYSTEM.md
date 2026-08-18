# OLEANDER Technical Drawing — Procedural Effect & Motion System v0.1

**Status:** `CANDIDATE / NO_PROMOTION`  
**Knowledge authority:** Notion `KN-METHOD-TECHDRAW-SPATIAL-TRANSLATION-001`  
**Motion runtime owner:** `oleander-motion`  

This system converts the Surface Treatment Gate into executable parameters, SVG recipes, motion handoffs and regression fixtures.

It is not an effect catalogue. The order is:

`Decision Question → Semantic Owner → Graphic Carrier → Effect Role → Parameter Instance → OFF / Reduced State → Near/Mid/Far → Runtime / Actual Preview → Keep/Reduce/Remove`

Never use:

`Cool Effect → Find a place to apply it`.

## 1. Files

- Parameter library: `VISUAL_EFFECT_PARAMETER_LIBRARY.json`
- SVG recipes: `../recipes/SVG_PROCEDURAL_RECIPES.json`
- Motion handoff recipes: `../recipes/MOTION_HANDOFF_RECIPES.json`
- Recipe validator: `../tools/validate_effect_recipe_register.py`
- Parameter-library validator: `../tools/validate_effect_parameter_library.py`
- SVG builder: `../tools/build_svg_effect_atlas.py`
- Native motion smoke-demo builder: `../tools/build_motion_recipe_demo.py`
- Golden fixture: `../fixtures/reconstruction/EFFECT-RECIPE-01_REGISTER.json`

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

## 3. Static recipe groups

### Continuous fields
- `SVG-R01-LINEAR-FIELD`
- `SVG-R02-RADIAL-FIELD`

Use for mapped continuous variables, controlled tonal hierarchy, source-fidelity gradients or state-bound emission. Analytical use requires domain + mapped variable + legend.

### Discrete / repeated textures
- `SVG-R03-HATCH`
- `SVG-R04-STIPPLE`
- `SVG-R09-CONTOUR-BANDS`

Use when discrete construction is itself meaningful: orientation, category, density, interval or source pattern. Record spacing/density/interval/seed.

### Micro / material / print surface
- `SVG-R05-GRAIN`
- `SVG-R10-EDGE-MODULATION`

Use for material hypothesis or source-fidelity only. Flat authoritative geometry remains underneath.

### Optical hierarchy / state
- `SVG-R06-SHADOW-DEPTH`
- `SVG-R08-GLOW-EMISSION`

Shadow may separate layers but cannot invent physical elevation. Glow requires a state/luminous/material/source owner.

### Conditional distortion
- `SVG-R07-DISPLACEMENT`

Allowed only for material/atmosphere/reference fidelity. Never apply to MAP_BOUND / authoritative analytical geometry.

## 4. Motion handoff groups

Motion recipes are specifications, not a second Motion Skill. Runtime implementation, Reduced Motion, device performance and AR-S10 are still owned by `oleander-motion`.

### Relation / continuity
- `TD-MR01-PATH-TRACE` → Motion Atlas `EF-03`
- `TD-MR04-SHARED-CONTAINER-HANDOFF` → `EF-01`
- `TD-MR08-EXPLODE-ASSEMBLE` → `EF-07`

### Reveal / hierarchy
- `TD-MR02-MASK-REVEAL` → `EF-02`
- `TD-MR03-STRUCTURED-STAGGER` → `EF-05`
- `TD-MR10-BLUR-FOCUS` → `EF-14`

### Data / time / progress
- `TD-MR05-DATA-FILTER-REORDER` → `EF-09`
- `TD-MR07-SCROLL-PROGRESS` → `EF-06`

### Material / field
- `TD-MR06-LIGHT-MATERIAL-STATE` → `EF-08`
- `TD-MR11-GRAIN-EVOLUTION` → `EF-15`
- `TD-MR12-PARTICLE-FIELD` → `EF-16`

### Conditional spatial depth
- `TD-MR09-PARALLAX-DEPTH` → `EF-12`

Map-bound analytical position must never be moved merely to create depth.

## 5. Parameter discipline

Numbers in the library are `CANDIDATE STARTING RANGES`, not rules.

For every real use record:

`Owner / Role / Target Scale / Parameter Value / Source or Model / Why / OFF-state / Failure Trigger / Actual Preview`.

Motion additionally records:

`State Before / State After / Trigger / Duration or Progress Model / Easing or Physics / Interrupt / Reverse / Rapid Repeat / Reduced Motion / Runtime State`.

## 6. OFF / Reduced attack

Static:

`FLAT MASTER → EFFECT ON → GRADIENT OFF → TEXTURE OFF → OPTICAL EFFECT OFF → GRAYSCALE → NEAR/MID/FAR → SMALL/PRINT`

Motion:

`NO-MOTION BASELINE → CANDIDATE → TIMING/PHYSICS VARIANT → REDUCED MOTION → INTERRUPT/REVERSE/RAPID REPEAT → REAL RUNTIME`

Hard rule:

`EFFECT OFF ≠ INFORMATION OFF`.

If disabling an effect removes geometry, topology, required state or critical evidence, the effect has exceeded its authority.

## 7. Regression purpose

The golden fixture deliberately mixes:

- analytical gradient;
- hierarchy hatch;
- deterministic material stipple;
- source-fidelity grain;
- hierarchy shadow;
- state emission glow;
- path trace;
- shared-container continuity;
- native scroll progress;
- modelled particle field.

Negative regressions reject absent owner, absent legend/model, missing seed, generic glow, shadow without reason, displacement on map-bound geometry, motion without Reduced Motion, loss of native scroll baseline, particles without count model and machine-awarded KEEP.

The CI also executes two builders:

1. parameter fixture → SVG effect atlas → XML parse;
2. motion fixture → standalone native HTML/CSS/JS smoke demo with `prefers-reduced-motion`.

## 8. Evidence boundary

`RECIPE EXECUTES ≠ EFFECT IS APPROPRIATE`  
`PARAMETER IN RANGE ≠ AESTHETIC PASS`  
`SVG FILTER ≠ MATERIAL TRUTH`  
`MOTION DEMO ≠ AR-S10 PASS`  
`AUTOMATED PASS ≠ DESIGN KEEP`.
