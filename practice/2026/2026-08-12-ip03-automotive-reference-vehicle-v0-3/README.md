# 2026-08-12｜IP03｜Automotive Reference Vehicle v0.3｜Comprehensive Modeling Benchmark

**Status:** EXPLORATION → F1 DESIGN VALIDATION

v0.1 was rejected for an implausible glass-bubble greenhouse and wheel-detail errors. v0.2 passed Machine QA but still failed Product QA because the greenhouse remained a single dominant glass volume and the roof insert/wheel visual hierarchy remained too synthetic.

## v0.3 modeling correction
The upper vehicle is no longer modeled as one glass bubble. It is rebuilt as:
- body-color cabin / roof shell;
- separate windshield;
- separate front/rear/quarter side windows;
- separate rear glass;
- explicit A/B/C-pillar logic;
- flush panoramic roof insert;
- slimmer five-split-spoke wheel design;
- no full-ring wheel-arch trim;
- subtle shoulder crease and integrated light graphics.

## Target corridor
- body length ≈ 4.42 m
- body width ≈ 1.86 m
- exterior height ≈ 1.43 m
- overall mirror width ≈ 2.08 m
- wheelbase 2.72 m
- track 1.58 m

## F1 review
Machine QA must pass body/cabin manifold, body and mirror-width corridors, wheelbase/track, window count and 8-view render matrix.

Product QA remains independent: stance, wheel/body ratio, front/rear overhang, greenhouse/body ratio, beltline/roofline, window/pillar logic, surfacing continuity, panel seams, light integration, clipping/occlusion, wheel design and coherent automotive reading.

## Reality boundary
Designer benchmark only; not engineering CAD, crash/aero/package/homologation/manufacturing validation.
