# OLEANDER Product Rendering Standard v0.1 — Timer R54

Status: `STANDARD BUILT / BLENDER 5.2 LTS + CYCLES CPU SMOKE PASS / PRODUCTION RENDER EXECUTION PENDING`

R54 is a production-rendering rebuild, not another visual-tuning round. The objective is to make material appearance portable, auditable, and separable from geometry authority.

## Evidence classes

- **FACT** — canonical GLB bytes, mesh names, positions, face topology, SHA and dimensions.
- **METHOD** — OpenPBR material structure, scene-linear rendering, reflection-card lighting, path tracing and AOV review.
- **VISUALIZATION HYPOTHESIS** — PC+ABS finish, anodized-aluminum finish, PMMA/opal IOR/scatter values until samples are measured.
- **PENDING** — full-quality production R54 render, sample calibration, optical validation and physical CMF validation.

## Geometry contract

The original `assets/pbr/timer_100_pbr.glb` remains authority. Canonical SHA-256:

`900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66`

The R54 render scene is a derivative with a strict allowlist: scene-scale interpretation, UVs, tangents, renderer material bindings, AOV IDs, cameras, lights and non-destructive shading normals. No vertex repositioning, remeshing, beveling, subdivision that changes silhouette, or proxy replacement is permitted.

Source audit: all 21 meshes currently expose `POSITION + NORMAL` only. `TEXCOORD_0` and `TANGENT` are absent. UV/tangent generation is therefore an explicit render-prep stage and must never be confused with geometry redesign.

## Unit contract

Source numerical scene extents are approximately `118 × 123.9 × 34.18`. Project design intent is millimeter-scale. R54 applies a **0.001 render-scene interpretation transform to meters** while leaving source GLB bytes unchanged.

## Material architecture

### Housing — PC+ABS

Dielectric glossy-diffuse base; moderate/high roughness; very weak secondary coat. Fine molded finish modifies roughness at real physical scale. Visible noise/albedo pattern is a failure. Normal mapping is OFF by default and requires macro evidence before use.

### Knob — anodized aluminum

Metallic base. Brushing is represented through anisotropic roughness and tangent direction, not painted concentric lines. Front and cylindrical side may use different tangent fields only when manufacturing intent supports the difference.

### Diffuser — opal translucent dielectric

Required reading: **cool Fresnel surface + milky scattering volume + warm internal illumination + edge-thickness cue**. Emission-only white plastic is rejected. `VISUALIZATION_State_Light` remains a visualization layer, not measured optical evidence.

## Lighting architecture

Studio lighting is reflection design. Named tasks:

- `KEY_BROAD` — housing curvature / broad soft lobe.
- `SIDE_STRIP` — side continuity / edge separation.
- `KNOB_SWEEP` — anodized-metal bright-dark sweep.
- `TOP_DIFFUSER` — cool surface reflection over warm volume.
- `NEG_FILL` — preserve dark side and material contrast.

Direct lights are secondary to reflection geometry and must not flatten material response.

## Camera architecture

Hero and CMF are different jobs. Hero preserves silhouette and product relationship. CMF uses a longer lens and closer crop to reveal roughness, thickness and metallic reflection without becoming a disconnected macro abstraction.

Baseline cameras: Hero 70 mm, CMF 85 mm, material macros 105 mm on a 36 mm sensor model.

## Color management

Keep lighting and compositing scene-linear. CMF review uses **Khronos PBR Neutral**; Hero uses **AgX** only after material approval. Exposure and post contrast must not compensate for a wrong material model.

## Sampling and AOVs

Production target: path tracing + adaptive sampling. Working master: multilayer floating-point EXR. Required passes: Combined, Diffuse Color, Glossy/Specular, Transmission, Emission, Normal, Depth, Shadow, Cryptomatte Object and Cryptomatte Material.

Blender 5.2 routes the R54 multilayer output through a compositor `File Output` node; the scene render output remains regular OpenEXR. This avoids relying on the older direct `RenderSettings.image_settings = OPEN_EXR_MULTILAYER` path.

## Promotion gates

- `R54-G0` Source Authority
- `R54-G1` Render Geometry Equivalence
- `R54-G2` Shading Prep
- `R54-G3` Material Fidelity
- `R54-G4` Studio Reflection
- `R54-G5` Color/AOV
- `R54-G6` Promotion

R54 may replace `hero_poster.png` / `material_poster.png` only after G0–G6 pass and explicit visual approval. Promotion then regenerates internal `SHA256SUMS.txt`, critical-file hashes, outer package SHA and deployment manifest/contract.

Until that gate, current v3.3 POSTERLOCK remains authority. Its deployment manifest authority is the merged PR #33; R54 does not modify that authority.

## Blender 5.2 runtime evidence — 2026-08-11

- Runtime: `Blender 5.2.0 LTS`, commit `fbe6228777e7`.
- Renderer: `Cycles`.
- Current execution device: CPU (`AMD EPYC 9V74`); CUDA/HIP GPU acceleration is unavailable in this container.
- Canonical GLB SHA check: **PASS**.
- Canonical mesh import: **21/21 PASS**.
- Compatibility smoke render: `320 × 240`, `16 samples`, `Khronos PBR Neutral`.
- Beauty EXR: **PASS**.
- Multilayer EXR: **PASS**, with 13 routed outputs covering Combined plus depth/normal/material-lighting and Cryptomatte channel groups.
- Classification: **RUNTIME COMPATIBILITY ONLY / NOT PRODUCTION QUALITY**.

The smoke render proves that Blender 5.2 + Cycles + canonical GLB + R54 camera/light/material/AOV path executes in this environment. It does **not** upgrade R54-G3, G4 or G5 to production PASS, and does not authorize poster promotion.

## Current execution boundary

Blender/Cycles is now available. MaterialX Python, OpenImageIO and OpenColorIO Python remain unavailable in this runtime. Full-quality path-traced R54 rendering at production sample/resolution settings is still `NOT RUN`.
