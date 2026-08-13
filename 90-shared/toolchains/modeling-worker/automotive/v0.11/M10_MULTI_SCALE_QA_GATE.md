# Automotive v0.11｜M10 Multi-Scale QA Gate

Status: `M10 OPEN / M5-M9 LOCKED / PROMOTION BLOCKED`

## Purpose

M10 is the final Modeling Contract validation gate for this generic automotive Modeling Worker benchmark. It verifies that the passed authority chain remains coherent when observed at macro, meso and micro scales.

M10 does not add or optimize geometry, components, details or CMF. Any failure must be routed back to the smallest responsible passed gate.

## Locked authority chain

- M5 primary Source: `R29A`;
- M6 semantic routing architecture;
- M7 secondary wheelhouse / glazing benchmark;
- M8 linked wheel-detail instance benchmark;
- M9 neutral semantic material binding.

Canonical R29A Source hash:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

## Scale matrix

### Macro
Questions:
- overall silhouette and package remain coherent;
- wheel/body scale remains correct under 0.700 m HP contract;
- R29A crown does not produce a new broad-volume failure;
- materials/details remain subordinate to body proportion.

Views:
- `M10_MACRO_SIDE`
- `M10_MACRO_HERO_FRONT`
- `M10_MACRO_HERO_REAR`

### Meso
Questions:
- front/rear fender crown and wheelhouse remain integrated;
- glazing shell stays aligned with glasshouse routing;
- material hierarchy does not conceal surface defects;
- secondary geometry does not project through primary Source.

Views:
- `M10_MESO_FRONT_ARCH`
- `M10_MESO_REAR_ARCH`
- `M10_MESO_GLASSHOUSE`

### Micro
Questions:
- linked spoke/ring instances remain centered and contained;
- tire/detail material binding remains consistent;
- no instance or secondary-geometry drift is visible at detail scale.

Views:
- `M10_MICRO_FRONT_WHEEL`
- `M10_MICRO_REAR_WHEEL`

## Machine gate

M10 machine PASS requires:
- canonical R29A Source hash unchanged through complete M10 scene assembly/render;
- Source topology unchanged;
- M6 region counts exact;
- M7 secondary geometry signatures stable before/after M10 render;
- M8 prototype signatures stable;
- M8 instance transforms/linked mesh relationships stable;
- M9 six-material binding manifest complete and `NOT_FINAL_CMF`;
- canonical wheel HP package exact;
- 40 spoke + 4 rim-ring linked-instance counts retained;
- all three QA scales represented;
- exactly 8 diagnostic views render;
- no view is promoted as engineering or production evidence;
- resource receipt records render count, resolution, samples and elapsed execution time.

## Human M10 review

At each scale inspect:
- visibility / occlusion;
- scale / proportion;
- cropping / framing;
- lighting adequacy;
- whether the view hides or exaggerates a defect.

Decision rules:
- `PASS`: no material issue remains that requires reopening a passed gate;
- `REVISE M9/M8/M7/M6/M5`: name the smallest responsible gate;
- no vague “needs more detail” decision is allowed.

## Candidate Authority boundary

If M10 passes, the benchmark may become:

`MODELING WORKER v0.11 CANDIDATE AUTHORITY`

This means:
- trustworthy editable benchmark Source;
- semantic routing available;
- secondary/detail dependency chain validated;
- neutral material binding validated;
- multi-scale visual QA completed.

It does **not** mean:
- Class-A automotive surfacing;
- engineering CAD;
- crash/aero validation;
- manufacturing feasibility;
- production panel splits;
- homologation;
- final CMF.

## Promotion rule

M10 PASS permits a separate **Promote** decision.

It does not automatically:
- merge PR #85;
- sync to canonical Notion/Drive;
- replace system-level Blender Surface System authority.
