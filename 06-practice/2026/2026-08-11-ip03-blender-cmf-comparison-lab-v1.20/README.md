# 2026-08-11｜IP03｜Blender Surface System v1.20.0｜Material Preset × Parameter Preset × CMF Comparison Lab

## Decision Question
Can the five v1.19 realistic process-simulation profiles produce stable, distinguishable material readings under one fixed camera and Broad / Strip / Grazing light rigs without visible procedural artifacts?

## Loop / Fidelity
- Loop: `CANONICAL_PRODUCTION` after v1.19 candidate promotion.
- Fidelity: `F1_DESIGN_VALIDATION`.
- Scene compile: once.
- Render defaults: `640×640 / 8 samples / Adaptive Sampling / Persistent Data`.

## Locked Variables
Camera, coupon pose, world/background, material center parameters, base colors, render transform, external rig definitions.

## Open Variable
Lighting rig only: `BROAD / STRIP / GRAZING`.

## Material Presets
- Fine Matte Powder-Coated Metal
- Injection-Molded PP Fine Matte
- PU Soft Matte Contact Surface
- Brushed / Anodized Aluminum Visual Simulation
- Milky Transmissive Diffuser Visual Simulation

## Visual QA
- coated metal must remain dielectric and not read as chrome;
- PP / PU must remain distinguishable without obvious procedural grain;
- micro-bump should disappear at product scale and only become legible under diagnostic grazing light;
- brushed/anodized aluminum must show directional response without painted stripes;
- diffuser must retain Fresnel/transmission depth and avoid glass-card / flat-emission reading;
- framing, clipping, occlusion, sampling and hotspot artifacts are checked for all 15 outputs.

## Exit Condition
Either the center values form a stable F1 acceptable corridor and can be promoted to D2, or the failing preset is revised without forcing the other four to rerender.

## Current reusable contract
- `90-shared/toolchains/blender-surface-system/v1.20.0/CMF_PRESET_CONTRACT_v1.20.0.json`
- `90-shared/toolchains/blender-surface-system/v1.20.0/CMF_PRESET_PROMOTION_v1.20.0.json`
- `90-shared/toolchains/blender-surface-system/v1.20.0/CMF_F1_POST_REVIEW.md`

Historical builder provenance remains at commit `60320785ec104ce44322a58d4e199054f84fd0ad` under its original `tools/oleander-blender-surface/v1.20.0/...` path. That historical path is not current repository routing.

## Reality Boundary
All Blender values are designer representation controls. This Lab does not validate supplier, production or measured physical properties.
