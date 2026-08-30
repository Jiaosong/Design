# OLEANDER Computer Graphics Quality Layer

Status: **CANDIDATE EXECUTION DELTA / NO SILENT PROMOTION**

Purpose: extend the existing `oleander-3d-pipeline` with a computer-graphics quality layer for modeling, surfacing, materials, lighting, rendering, sampling, color management, and cross-renderer readback. This file does not create a second 3D Skill, a universal render look, or a physical-material authority.

Canonical knowledge input: Notion `KN-CG-QUALITY-001｜Computer Graphics for Modeling & Rendering｜几何—光传输—材质—采样—色彩`.

## 1. Pixel-causality order

Treat a final pixel as the result of a chain, not a single render setting:

`SCALE / GEOMETRY → CAMERA → SHADING FRAME → BSDF → LIGHTING / ENVIRONMENT → LIGHT TRANSPORT → SAMPLING / RECONSTRUCTION → COLOR TRANSFORM → DISPLAY / DELIVERY`

Diagnose the earliest plausible broken layer first. Downstream presentation controls must not conceal upstream defects.

Hard examples:

- exposure does not repair invalid roughness or missing geometry;
- denoise does not repair insufficient signal;
- smooth shading does not repair a bad surface;
- higher subdivision does not repair wrong primary mass;
- an HDRI does not repair broken curvature or interface geometry;
- post-processing does not repair wrong scale, normals, intersections, or support logic.

## 2. Modeling and evaluated-surface gate

### 2.1 Separate four quantities

Never collapse these into one quality score:

1. source control complexity;
2. evaluated/tessellated surface density;
3. surface fairness / continuity;
4. design quality / reference fidelity.

A sparse causal cage can evaluate to a dense valid surface. A dense mesh can still be a poor surface.

### 2.2 Required diagnostic carriers

For retained form/surface judgments, use at least the carriers relevant to the claim:

- **silhouette carrier** — overall mass, proportion, profile, section changes;
- **section / interface carrier** — how parts, apertures, joints, edges, and transitions actually meet;
- **neutral diffuse carrier** — gross form without decorative reflection noise;
- **reflective / grazing carrier** — highlight flow, curvature waviness, local dents, folds, and edge quality.

A hero perspective alone is insufficient evidence for surface quality.

### 2.3 Normals and tangents

Distinguish geometric normals, face/vertex/corner shading normals, split/custom normals, and tangent frames.

- smooth shading changes shading interpolation, not silhouette geometry;
- weighted/custom normals can be a valid hard-surface representation tool but may not hide wrong topology or curvature;
- normal/tangent errors must be diagnosed separately from geometry errors;
- displacement, bump, and normal mapping have different geometric authority.

### 2.4 Subdivision and displacement

Use subdivision to construct or evaluate the intended limit surface, not as a generic quality slider. Control-loop placement, crease/support strategy, boundary handling, and modifier order must serve the target shape.

High-frequency displacement requires enough evaluated geometric bandwidth. Bump/normal detail may represent microappearance but cannot claim silhouette, fit, or dimension authority.

## 3. Material / BSDF gate

Prefer an energy-coherent layered surface model such as OpenPBR / Principled for general-purpose look development, while preserving project-specific material evidence.

Check material semantics before aesthetic tweaking:

- dielectric vs conductor/metal classification;
- base-color role for that material class;
- Fresnel / IOR behavior where relevant;
- roughness as microfacet-distribution behavior, not a generic brightness control;
- coat, transmission, subsurface, emission, and anisotropy only when the represented structure requires them;
- macro / meso / micro surface frequency assigned to geometry, displacement, normal/bump, and roughness variation intentionally.

Do not use intermediate metalness or arbitrary coat layers as a generic "premium" control.

A render parameter remains a **representation parameter** unless bound to measured/sample/manufacturer evidence.

## 4. Texture and encoding gate

Separate color data from numeric data.

- base-color/color textures participate in the declared color-management path;
- normal, roughness, metallic, displacement/height, masks, and other numeric maps use data/non-color semantics unless the target standard explicitly says otherwise;
- verify channel packing and tangent-basis expectations on interchange;
- choose texture frequency relative to the final camera distance and pixel density; do not add subpixel noise merely to make a material look "detailed".

For glTF metallic-roughness delivery, validate the exact target semantics and target renderer instead of assuming a Blender viewport match proves interchange fidelity.

## 5. Lighting is first a measurement rig

Before hero lighting, use diagnostic lighting that reveals form.

Recommended roles, not universal values:

- large soft card/source for broad reflection-flow continuity;
- narrow grazing strip for folds, edge transitions, waviness, and bevel quality;
- neutral environment for material/energy comparison;
- controlled black/white cards or equivalent reflection boundaries for product surfaces.

If the surface fails under diagnostic lighting, do not move directly to atmosphere, depth of field, bloom, glare, cinematic grading, or generative background repair.

Hero lighting starts only after geometry/surface/material diagnostics are credible. Hero light count is not a quality metric; source shape, angular size, placement, contrast structure, and environment relationship are more important than adding lights indiscriminately.

## 6. Light transport and renderer route

The rendering equation couples emission, incoming radiance, visibility, and BSDF response. Treat reflections, transmission, indirect light, occlusion, and multiple bounces as connected transport, not as independent visual effects.

### Cycles / path-traced route

Use for offline path-traced reflection/transmission/volume behavior and high-quality lighting evidence when the claim requires it.

- Monte Carlo noise is estimator variance under a finite sample budget;
- diagnose which path family is difficult before increasing samples blindly;
- use adaptive sampling / noise-threshold mechanisms when appropriate;
- evaluate path guiding only when the actual runtime/device and scene type support it; it is not a universal caustics solution;
- clamping can suppress pathological fireflies but too-low values remove legitimate highlight energy;
- record device/backend, sample policy, denoise policy, and materially relevant light-path settings.

### EEVEE / realtime route

Use for realtime preview or when the actual delivery renderer is realtime.

`EEVEE MATCH ≠ CYCLES EQUIVALENCE`.

Validate the target feature set: ray tracing/screen-space behavior, probes, shadowing, transparency, transmission, normal/tangent handling, tone mapping, and other target-specific approximations.

## 7. Sampling and denoise gate

Do not treat sample count as a universal quality number.

Noise diagnosis asks first: direct, indirect, glossy, transmission, volume, caustic, tiny bright emitter, or another difficult path?

Denoise policy:

- denoise only after enough underlying signal exists for the feature being reviewed;
- compare noisy and denoised outputs when fine texture, edges, micro-highlights, or small features matter;
- use albedo/normal auxiliary features when the chosen denoiser/runtime supports them and they improve detail preservation;
- do not let strong low-sample denoise erase a defect that the review is supposed to see.

## 8. Color-management gate

Rendering/compositing calculations should remain in an intentional scene-linear working space, with display/view transforms treated as explicit parts of the result.

For retained renders and especially A/B comparisons record:

- working color space;
- display device / display intent;
- view transform;
- look if used;
- exposure;
- output encoding / file color space;
- HDR/SDR intent where relevant;
- external OCIO configuration identity if non-default.

Route examples, not universal prescriptions:

- **Khronos PBR Neutral** when conservative PBR/product color presentation is the goal;
- **AgX** for general photographic/high-dynamic-range hero rendering where its tone reproduction fits the design intent;
- **ACES 2.x** when a real ACES cross-application / wide-gamut / HDR production pipeline requires it.

Changing the view transform invalidates a controlled material comparison unless color management itself is the tested variable.

## 9. Cross-renderer calibration

A successful export proves I/O, not visual equivalence.

For material-critical handoff keep a small calibration set where practical:

- neutral gray reference;
- representative dielectric material;
- representative metal/conductor material;
- roughness range or project-relevant swatches;
- normal-map/tangent test when normal maps are material;
- known camera/light/environment/exposure.

Read back in the target renderer and record deltas in material response, normals/tangents, transparency/transmission, environment, exposure, and color transform.

## 10. CG symptom → first-check routing

| Symptom | First checks | Do not start with |
| --- | --- | --- |
| highlight waves / kinks | curvature, topology, normals, modifier order | HDRI swap, bloom |
| toy-like plastic look | scale, bevel/edge geometry, material class, roughness structure, reflection-card shape | arbitrary metalness |
| flat/no volume | section, light-source shape, reflection boundaries, grazing light | global contrast boost |
| color too saturated / shifted | input encoding, working space, view transform, exposure | repainting base color |
| microdetail becomes mush | texture frequency, tessellation, samples, denoise | sharpening only |
| fireflies | tiny bright sources, glossy/transmission/caustic paths, importance/sampling | aggressive clamping first |
| realtime/offline mismatch | target renderer feature subset, probes/rays, tangent basis, tone mapping | declaring engines equivalent |

## 11. OLEANDER CG Quality Gates

### CG-Q01 — Scale & Silhouette
Real-world scale, primary mass, silhouette, and key sections are plausible and bound to the declared authority.

### CG-Q02 — Surface Continuity
Reflection/curvature flow has no unintended dents, waves, folds, pinching, or broken transitions at the intended viewing distance.

### CG-Q03 — Shading Frame
Normals, tangents, smoothing, and normal mapping agree with the intended geometry and target renderer.

### CG-Q04 — Material Energy Coherence
Dielectric/metal, IOR/Fresnel, roughness, coat, transmission, subsurface, emission, and anisotropy are semantically coherent for the represented material.

### CG-Q05 — Texture Encoding & Frequency
Color vs data encoding, channel semantics, tangent space, UVs, and spatial frequency are correct for the target pipeline.

### CG-Q06 — Lighting Reveals Form
Diagnostic lighting exposes surface quality before hero lighting is allowed to stylize it.

### CG-Q07 — Transport & Sampling
Noise is diagnosed by path/variance source; adaptive sampling, guiding, clamping, and denoise are used intentionally and do not hide review defects.

### CG-Q08 — Color Pipeline
Working space, view/display transform, exposure, and output encoding are explicit and locked in comparisons.

### CG-Q09 — Cross-renderer Readback
Where interchange matters, a representative calibration scene/material set is reopened in the target renderer and visual semantic losses are declared.

### CG-Q10 — Actual Preview Design Crit
The final render/model view is reviewed at the intended camera distance/output resolution under OLEANDER Artifact Review. `Render PASS ≠ Design PASS` remains binding.

## 12. Default modeling → rendering quality loop

1. lock reference, units, dimensions, and source authority;
2. establish primary mass, silhouette, sections, and interfaces with minimum sufficient source controls;
3. evaluate the final modifier/procedural carrier and inspect curvature/reflection flow;
4. run neutral diffuse + reflective/grazing diagnostic views;
5. calibrate material semantics under a neutral controlled rig;
6. diagnose difficult light paths and set sampling/denoise policy;
7. lock color pipeline and exposure;
8. build hero lighting/composition only after diagnostic gates are credible;
9. review at final viewing distance and output resolution;
10. perform target-renderer/export readback when delivery crosses software/runtime boundaries.

## 13. Source stack / verification date

Verified 2026-08-30 against the current source stack used for this candidate:

- PBRT v4 — Light Transport Equation, Monte Carlo Integration, Path Tracing: https://pbr-book.org/4ed/
- OpenPBR Surface: https://academysoftwarefoundation.github.io/OpenPBR/
- Blender 5.2 Manual — Principled BSDF, Cycles Sampling/Path Guiding, Denoise, Color Management, Subdivision Surface: https://docs.blender.org/manual/en/5.2/
- libigl Tutorial — normals and differential-geometry concepts: https://libigl.github.io/tutorial/
- Khronos glTF 2.0 specification: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- Google Filament PBR reference: https://google.github.io/filament/Filament.md.html

Software/spec details are freshness-sensitive and require re-verification when runtimes or standards change.

## Does not prove

This layer does not prove physical material measurement, manufacturer CAD/Class-A, field truth, photometric certification, exact colorimetric sample match, structural/engineering/manufacturing approval, reference fidelity, `DESIGN KEEP`, or `MAIN KEEP`.
