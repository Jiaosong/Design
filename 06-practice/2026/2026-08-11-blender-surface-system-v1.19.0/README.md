# OLEANDER Blender Surface System｜v1.19.0｜Designer Estimate & Realistic Process Simulation Gate

Status: REVIEW / STACKED ON v1.18.0 / NOT MERGED
Primary: IP03
Supporting: SP03
Scope: DESIGNER ONLY

## Purpose
Use defensible estimated values and visually realistic process simulation for CMF / Blender design work.

Supplier selection, exact grade, TDS/SDS, coating chemistry and production proof are **not prerequisites** for this system. Those remain downstream Engineering / Production Handoff topics.

## Designer parameter ladder
`D0 UNDEFINED → D1 DESIGN_ESTIMATE → D2 DESIGN_CALIBRATED → D3 PROJECT_LOCKED_VISUAL_PROFILE`

## Active design estimates
- XJ01 PP Fine Matte: roughness 0.52, design range 0.48–0.58; subtle meso/micro hierarchy.
- XJ01 PU Soft Matte: roughness 0.66, range 0.60–0.72.
- XJ01 coated iron visual: metallic 0, roughness 0.46, range 0.40–0.55.
- Timer Housing: roughness 0.55, range 0.48–0.62.
- Timer Knob: roughness 0.28 / anisotropy 0.48 with directional logic.
- Timer Diffuser: roughness 0.34 / transmission 0.85 with visually tuned scatter/Fresnel.

## Powder-coat simulation rule
Treat the visible coat as an opaque dielectric layer over metal: Metallic = 0; narrow roughness variation; very weak optional bump; microstructure should disappear at normal product-view distance. Validate with broad-strip and grazing-strip reflections. Reject chrome response, visible sandpaper grain, exaggerated orange peel and random base-color speckle.

## Process-simulation rule
The goal is to reproduce the **visual mechanism** of a plausible finish closely enough for design judgment, not to recreate a named supplier formula.

Reality boundary: Blender parameters are representation controls, not laboratory or supplier measurements.
