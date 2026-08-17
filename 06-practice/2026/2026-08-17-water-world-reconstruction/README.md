# Water World — reconstruction benchmark

Status: `EXTERNAL PROFESSIONAL REFERENCE / STRUCTURAL RECONSTRUCTION / RF-C1 CANDIDATE / REVIEW PENDING`

Reference project: Information is Beautiful — **Water World – the distribution of all the water in all the world**.

Source page: https://informationisbeautiful.net/visualizations/water-world-distribution-of-the-all-the-water-in-all-the-world/

The source page credits David McCandless for design/research and Miriam Quick for research, and cites USGS and FAO as sources. This practice uses the project only as an external reconstruction benchmark.

## Why this benchmark

The current OLEANDER technical-drawing reconstruction subsystem needed a real external test rather than a synthetic fixture. Water World is useful because it combines:

- a sparse white editorial field;
- multiple semantic colour families;
- unequal circle sizes;
- curved relation lines;
- several nested hubs;
- small labels with tight baseline relationships;
- a title whose exact face/advance width materially affects perceived fidelity;
- deliberately uneven information density.

## Materialized reference state

The exact original vector/PDF/CAD asset was **not** materialized in the current execution environment. The visible benchmark available to the producer is the 512×512 web/image-search reference.

Therefore the maximum producer claim for this run is:

`RF-C1 / GEOMETRIC FIDELITY CANDIDATE`

not `RF-C3 / PIXEL-EXACT`.

## Real artifact

- `WATER_WORLD_RF_C1_RECONSTRUCTION.svg` — editable vector reconstruction; no embedded source raster.
- `WATER_WORLD_RECONSTRUCTION_REPORT.json` — truth boundary and next-gate requirements.

Local render/reopen produced a 1024×1024 PNG review derivative. The PNG is review evidence only and is not source authority.

## Observed failure from the first render

The first render exposed two concrete fidelity gaps that a generic similarity score would not diagnose well:

1. title face/advance width/baseline did not reproduce the reference closely enough;
2. the lower-right organism chain and human-use labels had different density/avoidance behaviour from the reference.

A second vector revision reduced those issues without embedding or tracing the source image.

## Current boundary

This practice does **not** claim:

- pixel-exact equality;
- exact original font identity;
- exact Bezier control points;
- exact visible stroke raster phase;
- exact hidden/cropped labels outside recoverable reference detail;
- ownership or project authority over the original Information is Beautiful design.

For RF-C3, the next execution must materialize the exact reference pixels/vector, lock renderer + font shaping, populate A0–A4/object forensic registers, and run a zero-tolerance critical-ROI comparison.

`REFERENCE FIDELITY != TECHNICAL TRUTH != DESIGN KEEP`.
