# 3D Pipeline Visual Layer Binding

Status: **BINDING / NO UNIVERSAL RENDER LOOK**

This file binds 3D visual output to existing OLEANDER review and training knowledge. It does not introduce a universal render look.

## Existing sources to inherit

1. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`, especially Model / Rendering professional checks.
2. Project-specific Current Design DNA / Visual Bible only when Current Authority explicitly makes it applicable.
3. Existing practice `06-practice/2026/2026-08-11-ip03-blender-cmf-comparison-lab-v1.20/` for bounded CMF/render comparison learning.
4. Existing practice `06-practice/2026/2026-08-16-technical-drawing-lineweight/` when 3D output becomes axonometric/vector technical communication.
5. `MOTION_LIBRARY_EFFECT_ATLAS.md` for 3D animation mechanisms such as explode/assemble, temporal material/light change and camera motion.
6. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for render post-processing, compositing and Illustrator/SVG presentation operators.
7. `COMPUTER_GRAPHICS_QUALITY_LAYER.md` for causal diagnosis of geometry/surface, normals, BSDF/material semantics, diagnostic lighting, light transport, sampling/denoise, color management, and cross-renderer readback. On a non-main candidate branch this remains a candidate binding until promoted through the repository review path.

## Existing visual checks to apply

From Artifact Review v1.1: geometry and construction must remain credible; human/facility/railing/path scale must be plausible; material, roughness, reflection, light and environment must agree. Attractive lighting or material treatment may not hide floating, intersection, unsupported or otherwise incorrect geometry.

The CG quality layer makes that check executable through **CG-Q01—CG-Q10**. Diagnose the earliest broken layer first:

`scale / geometry → silhouette / section → curvature / normals → BSDF / textures → lighting / transport → sampling / denoise → color / display`.

Do not impose the OLEANDER portfolio Visual Bible color/light recipe on unrelated projects. Reuse it only when it is a Current Design Source for that project.

## Diagnostic-before-hero visual rule

When a retained render is being used to judge form, surface quality, or CMF appearance, use claim-fit diagnostic carriers before hero presentation:

- silhouette/profile where primary mass or proportion is under review;
- section/interface where connections and transitions are under review;
- neutral diffuse for gross form;
- reflective/grazing lighting for curvature, waviness, folds, edge and bevel quality;
- neutral calibrated material/light/color setup for controlled CMF comparison.

Hero lighting, depth of field, atmosphere, bloom/glare, strong grading, generative backgrounds, or retouching may not replace those carriers or conceal the defect under review.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for render passes, masks/alpha, layer compositing, exposure/color adjustment, Smart Object-linked render replacement, bounded atmospheric treatment and vector-safe annotation/effect work. Preserve the original render and geometry-derived source. Post-processing, retouch, generative background/people/sky replacement or distortion may create a presentation derivative, but may not repair or conceal invalid geometry, scale, construction, field truth or material logic. `2D FAUX 3D ≠ GEOMETRIC 3D` remains hard.

## Review inheritance

Review real renders and model views at the intended camera distance and final output resolution. `Render PASS ≠ Design PASS`; material/light success does not promote geometry, field evidence or engineering truth.
