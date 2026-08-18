# OLEANDER Technical Drawing — Effect Operator Router

This module routes Illustrator/Photoshop-style effect families into OLEANDER without allowing visual effects to overwrite geometry, evidence, editability or technical truth.

Hard boundaries:

`VECTOR-SAFE EFFECT != RASTER-ONLY EFFECT`

`2D FAUX 3D != GEOMETRIC 3D`

`EFFECT OFF -> GEOMETRY / RELATION / STATE STILL READS`

`RASTER PREVIEW != AUTHORITATIVE VECTOR / TEXT / GEOMETRY`

`FILTER OUTPUT != DESIGN KEEP`

## 1. Router order

For any requested effect, execute:

`EFFECT NAME -> EFFECT ROLE -> OWNER / MASK -> VECTOR OR RASTER CLASS -> EDITABILITY REQUIREMENT -> TRUTH RISK -> PARAMETER PRESET -> EFFECT-OFF BASELINE -> TARGET-SIZE READBACK -> ATTACK TEST -> REVIEW`.

Do not choose an operator because its software menu name sounds appropriate. Route by communication role and truth boundary.

## 2. Vector-safe / Illustrator-style families

### 2.1 3D and Materials

Use only as either:

- `2D_FAUX_DEPTH` — editable visual depth made from repeated offsets, face fills, low-span gradients or bevel bands; or
- `TRUE_3D_HANDOFF` — route to the existing 3D/Blender pipeline when actual geometry, perspective, occlusion, section, dimension or physical material behavior matters.

Allowed vector preview operators:
- faux extrude;
- faux bevel;
- revolve preview.

Mandatory label when material: `VISUAL DEPTH ONLY / DOES NOT PROVE 3D GEOMETRY`.

### 2.2 SVG Filters

Supported operator primitives:
- `feGaussianBlur`;
- `feDropShadow`;
- `feTurbulence`;
- `feDisplacementMap`;
- `feColorMatrix`;
- `feMorphology`;
- `feBlend`;
- `feComposite`.

Every filter must declare `OWNER`, `PARAMETERS`, `OFF-STATE`, and whether its output changes source-fidelity claims.

### 2.3 Warp / distort / transform

Supported vector deformation classes:
- arc;
- wave;
- bulge;
- flag;
- fisheye;
- repeat transform;
- roughen;
- twist;
- pucker/bloat;
- zigzag.

For map-bound, measured, dimensional or source-authoritative geometry, these are normally forbidden unless the deformation itself is the subject or source-visible reference effect. Decorative deformation cannot silently alter authoritative geometry.

### 2.4 Path / Pathfinder / Convert to Shape

Treat these as geometry utilities rather than styling:
- offset path;
- outline stroke;
- simplify;
- union;
- intersection;
- difference;
- xor;
- rectangle / rounded rectangle / ellipse wrappers.

Any boolean or offset that changes the controlling boundary must preserve provenance to the original object.

### 2.5 Stylize

Available bounded operators:
- inner glow;
- outer glow;
- feather;
- scribble;
- rounded corners;
- controlled shadow.

Outer glow is `AVOID BY DEFAULT`; it requires an explicit role or source-fidelity reason. Scribble / roughness must not make a technical boundary look measured or material-authentic when it is not.

### 2.6 Rasterize / crop marks

`RASTERIZE` is an output adapter, not a design operator. Preserve the editable master before rasterization.

`CROP MARKS` is an output utility. It carries no design authority.

## 3. Raster / Photoshop-style families

Raster families are allowed as preview, reference reconstruction support, texture/optical derivatives, or final raster delivery only when the task permits raster output. They may not replace editable technical text, geometry, dimensions or semantic chart objects.

Supported families:

### Pixelate
- mosaic;
- halftone;
- crystallize proxy.

### Distort
- ripple;
- wave;
- twirl;
- displacement-map preview.

### Blur
- Gaussian;
- motion blur;
- radial/zoom proxy.

### Brush strokes
- dry-brush proxy;
- ink outline;
- crosshatch.

### Sketch
- charcoal proxy;
- photocopy;
- torn-edge proxy.

### Texture
- grain;
- stained-glass proxy;
- texturizer proxy.

### Artistic
- poster edges;
- cutout;
- watercolor proxy.

### Video
- scanline preview;
- deinterlace utility.

Video-family effects are not a default design route.

### Stylize
- emboss;
- find edges;
- solarize;
- wind proxy.

`proxy` means executable approximation, not pixel-identical reproduction of Adobe's proprietary implementation.

## 4. Effect parameter contract

Every reusable effect recipe should expose machine-readable parameters.

Minimum fields:

`effect_id / family / role / owner / mask / vector_or_raster / parameters / seed_or_phase / off_state / reduced_motion_if_animated / export_support / failure_triggers / does_not_prove`.

Examples:

### Faux extrusion
`depth_px / steps / dx / dy / side_tone`.

### Turbulence + displacement
`baseFrequency / numOctaves / seed / scale / channels`.

### Roughen
`amplitude / frequency / seed`.

### Mosaic
`cell_px`.

### Ripple
`amplitude_px / wavelength_px / phase`.

### Motion blur
`distance_px / angle_deg`.

### Emboss
`angle_deg / height / amount`.

## 5. Motion cross-route

When an effect itself changes through time, route the temporal layer to `oleander-motion`.

Effect-aware motion recipes may include:
- gradient focus shift;
- texture reveal through mask/clip;
- blur-to-sharp focus handoff;
- displacement settle;
- emboss/light sweep;
- scanline reveal;
- selected alluvial stream pulse;
- radial-bar sweep.

Static truth remains primary. Reduced Motion must preserve the same state/information without the positional or optical animation.

## 6. Attack tests

At minimum test:

`EFFECT OFF -> TARGET SIZE -> SMALL SIZE -> GRAYSCALE -> VECTOR MASTER RECOVERY -> RASTER EXPORT -> LABEL / DIMENSION LEGIBILITY -> OWNER MASK CHECK -> FALSE DEPTH / FALSE CONTINUITY CHECK`.

Additional tests by family:
- warp/distort: controlling geometry unchanged where required;
- blur/glow: no loss of edges/interfaces;
- grain/texture: no label occlusion and no false material direction;
- faux 3D: no claim of true geometry;
- raster effects: no accidental replacement of editable text/vector objects;
- reconstruction effects: source-visible effect reproduced rather than aesthetically improved.

## 7. Regression boundary

Executable fixtures and hash-stable regeneration prove only that an operator recipe can be reproduced.

`REGRESSION PASS != VISUAL QUALITY PASS != TECHNICAL TRUTH PASS != DESIGN KEEP`.

Keep each fixture paired with its flat/effect-off baseline whenever the effect materially changes first-read.