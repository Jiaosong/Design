# 2026-08-12｜IP03｜Automotive Reference Vehicle｜Comprehensive Modeling Benchmark

**Status:** EXPLORATION → F1 DESIGN VALIDATION

## Decision Question
Can one unbranded reference vehicle provide a sufficiently comprehensive benchmark for OLEANDER product modeling, material binding, surfacing review, detail hierarchy, rendering, and QA?

## Modeling target
Generic fastback/crossover, approximately:
- length 4.42 m
- width 1.86 m
- height 1.48 m
- wheelbase 2.72 m
- track 1.58 m
- wheel radius 345 mm

These are design estimates, not homologation/engineering dimensions.

## Coverage
- lofted exterior body shell
- wheel-arch booleans
- greenhouse/glass
- panoramic roof
- wheels / tires / spokes / brake discs / calipers
- lights / light guides
- mirrors / handles / panel seams / trim
- interior seats / dashboard / screen / steering wheel
- automotive paint, glass, PP, PU/rubber, coated metal, anodized/metal, emissive lighting
- beauty, orthographic, detail and clay surfacing views

## F1 views
1. HERO_FRONT_3Q
2. REAR_3Q
3. SIDE_PROFILE
4. TOP_3Q
5. FRONT_ORTHO
6. WHEEL_DETAIL
7. CABIN_DETAIL
8. CLAY_SURFACING

## QA
Machine QA checks dimensional corridor, wheelbase/track, primary manifold meshes, component counts, and render matrix.

Visual QA must separately check overall automotive proportion, wheel/body relationship, glass/body ratio, stance, overhangs, surfacing continuity, panel-gap logic, clipping/occlusion, light integration, detail density and whether the model reads as a coherent vehicle rather than an assembly of primitives.

## Reality Boundary
Designer benchmark only. Not engineering CAD, crash/aero/ergonomics/package/homologation/production validation.
