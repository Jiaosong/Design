# OLEANDER Computer Graphics Quality Layer

Status: **CANDIDATE EXECUTION DELTA / NO SILENT PROMOTION**

Purpose: extend the existing `oleander-3d-pipeline` with a computer-graphics quality layer for modeling, surfacing, materials, lighting, rendering, sampling, color management, and cross-renderer readback. This file does not create a second 3D Skill, a universal render look, or a physical-material authority.

Canonical knowledge input: Notion `KN-THEORY-COMPUTER-GRAPHICS-001｜Computer Graphics for 3D Modeling & Rendering｜三维建模与渲染计算机图形学`.

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

## 4. Texture encoding and frequency

- color textures participate in the color-management pipeline;
- numeric maps such as normal, roughness, metallic, and displacement are treated as data/non-color unless the target specification explicitly defines otherwise;
- map semantics and channel packing must be verified for the target renderer / exchange format;
- microtexture frequency must survive the final camera distance and reconstruction filter instead of degenerating into noise or moiré;
- keep macro, meso, and micro appearance frequencies intentionally separated.

## 5. Lighting: diagnose before stylizing

Use a neutral diagnostic rig before hero lighting when form/surface/material quality is at issue.

Recommended diagnostic carriers, adapted to the actual object:

- large soft card for broad reflection flow;
- narrow/grazing strip for edge and curvature defects;
- controlled black/white cards for reflection boundaries;
- neutral environment for material-energy readback;
- direct-light isolation where needed to separate lighting from transport noise.

Hero lighting may follow only after the relevant diagnostic carrier is credible. Light count is not a quality metric; emitter size, angular extent, direction, contrast, environment ratio, and object scale are often more causally important.

## 6. Light transport and integrator reasoning

Treat path tracing as a stochastic estimator of light transport, not a magic quality switch.

When noise or instability appears, classify the difficult path first:

- direct;
- indirect diffuse;
- glossy/specular;
- transmission/refraction;
- volume;
- caustic;
- tiny/high-energy emitter;
- difficult indirect interior path.

Then choose the relevant response: sampling strategy, emitter design, path guiding when actually supported and appropriate, bounce/transport simplification, adaptive sampling, or controlled production compromise.

Do not globally increase samples before identifying the noise source when a cheaper causal fix is available.

## 7. Sampling, reconstruction, denoise and clamping

- adaptive sampling/noise-threshold mechanisms are preferred over one universal sample number when the renderer supports them;
- denoise is reconstruction after signal acquisition, not a substitute for signal;
- check albedo/normal auxiliary features when supported and useful;
- inspect fine edges, microtexture, glossy detail, thin geometry and temporal consistency after denoise;
- clamping is a production/diagnostic control for extreme outliers, not a universal fix; over-clamping destroys valid highlight energy;
- record the actual rendering/runtime conditions for retained comparisons.

## 8. Color-management gate

Lock color management before visual comparison unless color management itself is the variable under test.

Record at minimum when material:

- scene-linear / working-space assumption;
- input texture encoding;
- view transform;
- look, exposure and white balance if used;
- display/output encoding;
- HDR/wide-gamut target where applicable.

For CMF/material A/B comparisons, all variants must use the same color pipeline unless the explicit test is the color pipeline.

Renderer/display options such as AgX, Khronos PBR Neutral, or ACES are task-specific transforms, not style presets or quality ranks.

## 9. Cross-renderer material readback

`EXPORT PASS ≠ APPEARANCE MATCH`.

For glTF/GLB, USD, FBX or other material handoff, record the represented material model and known losses. Validate at least the relevant subset of:

- base color / metallic / roughness semantics;
- normal/tangent basis;
- UVs and texture transforms;
- channel packing;
- scale;
- environment / lighting;
- exposure and color transform;
- transparency/transmission/coat features when used.

Use a compact calibration set when appearance fidelity matters: neutral gray, dielectric swatch, metal swatch, roughness ladder/spheres, normal-mapped reference, or equivalent project-fit carriers.

## 10. OLEANDER CG quality gates

These gates extend existing Artifact Review; they do not replace it.

- **CG-Q01 Scale & Silhouette** — object scale, primary mass, proportion, and intended silhouette/section read credibly.
- **CG-Q02 Surface Continuity** — reflective/grazing carriers show intentional curvature and edge flow without unexplained waviness, dents, pinching, or broken transitions.
- **CG-Q03 Shading Frame** — normals/tangents/smoothing/custom-normal choices are intentional and do not conceal invalid geometry.
- **CG-Q04 Material Energy Coherence** — material class, IOR/Fresnel, roughness, metalness, coat/transmission/subsurface/emission behavior are semantically coherent for the represented material.
- **CG-Q05 Texture Encoding & Frequency** — color vs numeric encoding, channel semantics, macro/meso/micro frequency and final pixel bandwidth are credible.
- **CG-Q06 Lighting Reveals Form** — at least one diagnostic carrier reveals rather than hides form/surface/material behavior before hero stylization is accepted.
- **CG-Q07 Transport & Sampling** — noise/variance is diagnosed by path class; sampling/denoise/clamp choices preserve required detail and do not fabricate quality.
- **CG-Q08 Color Pipeline** — retained comparisons state and lock the relevant view/display pipeline; no uncontrolled color transform drives material decisions.
- **CG-Q09 Cross-renderer Readback** — exported appearance is checked in the target runtime with known losses/assumptions recorded.
- **CG-Q10 Actual Preview Design Crit** — real intended-camera output is reviewed under OLEANDER Artifact Review; CG/render PASS cannot promote wrong geometry, engineering truth, physical CMF truth, or Design KEEP.

## 11. Diagnostic routing matrix

| Symptom | First inspect | Do not start with |
| --- | --- | --- |
| highlight waves / kinks | curvature, topology, normals, modifier order | HDRI swap, bloom |
| toy/plastic look | real scale, bevel/edge radius, material class, roughness, environment ratio | arbitrary metallic |
| render is noisy | difficult path/light source/sampling distribution | blind sample escalation |
| denoised render is mushy | input signal, albedo/normal guides, fine-detail frequency | stronger denoise |
| material differs after GLB export | semantics, tangent basis, maps/channels, environment/exposure/view transform | blaming exporter generically |
| CMF A/B result changes unpredictably | color pipeline, exposure, texture encoding, lighting lock | changing material values first |
| smooth shading seems to "fix" a bad surface | silhouette/section/reflection carrier | accepting shading as geometry proof |
| displacement looks jagged | evaluated geometric bandwidth, displacement frequency and scale | more contrast in the height map |

## 12. Required quality record for retained 3D/render claims

When a model/render is retained as design evidence or a main presentation candidate, capture the applicable subset of:

- object scale / camera distance;
- silhouette/section carrier;
- surface diagnostic carrier;
- normal/tangent/smoothing strategy;
- material model and evidence boundary;
- lighting diagnostic and hero rigs;
- renderer/integrator and sampling/denoise/clamp settings;
- color pipeline;
- target-runtime appearance readback;
- CG-Q01—CG-Q10 result;
- remaining geometry / physical / field / engineering / manufacturing HOLD.

This layer improves modeling/rendering diagnosis and image quality. It does **not** convert visual plausibility into physical or engineering truth.
