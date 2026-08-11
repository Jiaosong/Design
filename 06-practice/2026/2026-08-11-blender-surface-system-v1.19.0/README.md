# OLEANDER Blender Surface System｜v1.19.0｜Designer Estimate & Realistic Process Simulation Gate

Status: REVIEW / BASED ON MERGED v1.18.0 / NOT YET PROMOTED
Primary: IP03
Supporting: SP03
Scope: DESIGNER ONLY

## Purpose
Use defensible estimated values and visually realistic process simulation for CMF / Blender design work.

Supplier selection, exact grade, TDS/SDS, coating chemistry and production proof are **not prerequisites** for this designer gate. Those remain downstream Engineering / Production Handoff topics.

## Two independent state systems

v1.19.0 introduces a designer parameter ladder:

`D0 UNDEFINED → D1 DESIGN_ESTIMATE → D2 DESIGN_CALIBRATED → D3 PROJECT_LOCKED_VISUAL_PROFILE`

This ladder answers only: **may this value/profile be used for current design representation?**

It does **not** replace or upgrade the v1.18 evidence claim lanes:

`EVIDENCE_BOUND / VISUALIZATION_LOCKED / REFERENCE_ONLY / BLOCKED / UNKNOWN`

Hard firewall:

> `D1 / D2 / D3` never implies measured evidence, process truth, generic archetype authority or claim-lane promotion.

A target may therefore be `D2 DESIGN_CALIBRATED` for visual continuity while its manufacturing process remains `BLOCKED` or `UNKNOWN` as an evidence claim.

## Active design estimates

- XJ01 PP visual: roughness 0.52, design range 0.48–0.58; `D2`, while project finish/texture evidence remains visualization-only and generic archetype autobind remains denied.
- XJ01 PU visual: roughness 0.66, range 0.60–0.72; `D1`, while exact PU family/process/finish remains UNKNOWN and legacy merged TPE/PU process binding remains BLOCKED.
- XJ01 coated-iron **visual hypothesis**: metallic 0, roughness 0.46, range 0.40–0.55; `D1`, while actual powder-coat/process claim remains BLOCKED/UNKNOWN.
- Timer Housing: roughness 0.55, range 0.48–0.62; project-specific `D3` visual profile only.
- Timer Knob: roughness 0.28 / anisotropy 0.48; project-specific `D3` visual profile only.
- Timer Diffuser: roughness 0.34 / transmission 0.85; project-specific `D3` visual profile only.

## Powder-coat visual simulation rule

When a designer explicitly chooses a powder-coated-metal **visual hypothesis**, simulate the plausible visible mechanism as an opaque dielectric coat over metal: Metallic = 0; narrow roughness variation; very weak optional bump; microstructure should disappear at normal product-view distance. Validate with broad-strip and grazing-strip reflections. Reject chrome response, visible sandpaper grain, exaggerated orange peel and random base-color speckle.

This does not assert that XJ01 or any other project actually uses powder coating. For XJ01 iron, the v1.18 process claim remains `BLOCKED / UNKNOWN` until project evidence exists.

## Process-simulation rule

The goal is to reproduce the **visual mechanism of a plausible finish hypothesis** closely enough for design judgment, not to recreate a named supplier formula and not to establish manufacturing truth.

All generic simulation profiles are:

- `AUTOBIND = DENY`;
- `DESIGNER_EXPLICIT_SELECTION_ONLY`;
- `EVIDENCE_CLAIM_IMPACT = NONE`.

## Reality boundary

Blender parameters are representation controls, not laboratory or supplier measurements. Engineering / Production Handoff remains separate and downstream. v1.19 design promotion can lock a visual profile; it cannot promote evidence claims without the applicable evidence process.
