# C22-01 v3.9 — OLEANDER Skill QA

## Skill correction

Applied the candidate `oleander-technical-drawing` rules as calibration, specifically:
- `SOURCE_CARRIER_PRECEDENCE`
- `SPATIAL_TRANSLATION_PROTOCOL`
- `FLOW_DIRECTION_ANALYSIS`

The critical correction is `SOURCE EXISTS != REDRAW REQUIRED`.

The existing `qingjiang_route_guide_translated.svg` is treated as the source carrier and reused directly. No route Bézier, branch, route-mode edge, or node position is redrawn for visual preference.

## v3.8 disposition

`v3.8 = REJECT / SUPERSEDED`.

Reason: it replaced a sufficient source carrier with invented landscape/route illustration. That violates source-carrier precedence and failed the project first-visual gate.

## v3.9 visual strategy

- carrier occupies the dominant drawing field;
- no fake topography, fake trees, fake buildings or invented scenic illustration;
- only one C04 interface-zone highlight is added;
- right-side close-read is a crop of the same carrier, not a reconstructed route;
- typography and metadata remain subordinate to the source carrier.

## Flow integrity

The parent sheet does not create a second route network.
The source carrier remains the only route geometry owner.

Source SHA256: `1acfb9d708a96d9ac59900610fe724413b4b9cea4bddf1b6d0fcc27f8034c5b9`

## Production QA

- SVG source: editable.
- Source carrier preserved as vector content in a reusable symbol.
- Full render: 2384×1684.
- Far-read derivative: 1192×842.
- CairoSVG render succeeded.
- No new raster dependency introduced.

## Producer state

`EXECUTED / SOURCE-CARRIER-REUSED / RENDERED / PRODUCER SELF-CHECKED / INDEPENDENT DESIGN REVIEW PENDING`

No producer `PIXEL KEEP / MAIN KEEP / PROFESSIONAL FINISH PASS`.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
