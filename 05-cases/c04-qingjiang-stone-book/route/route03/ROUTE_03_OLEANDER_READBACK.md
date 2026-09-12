# ROUTE-03 OLEANDER Readback

## Source / transformation
- Raw uploaded SVG preserved.
- Main line and dashed branch path geometry are reused directly from the uploaded source.
- 17 named nodes retained.
- A-D route modes retained.
- Parking lot, marina, tourist centre and north cue retained.
- No exact distance / slope / GPS / travel-time / current-operation claim added.

## First visual
- Route is the dominant first read.
- No dashboard/card-wall structure.
- No glow/HUD/game-map styling.
- No duplicated node-order strip.
- No per-node English duplication.
- No decorative icon family.

## Best-existing / source comparison
- Side-by-side file: `ROUTE_03_SOURCE_BENCHMARK_1920x1080.png`.
- Producer detects no regression in topology legibility.
- New artifact has stronger route hierarchy and lower visual noise than the uploaded source.
- This is producer readback only; no independent KEEP is claimed.

## Production QC
- PNG: 1920×1080
- Far-read: 480×270 generated.
- Grayscale: generated.
- Independent SVG render: successful.
- Mean PNG/SVG-render channel difference: 0.000
- HTML/SVG/PNG/raw source are packaged together.

## Current state
`EXECUTED / SELF-CHECKED / SOURCE-COMPARED / INDEPENDENT DESIGN REVIEW PENDING`
