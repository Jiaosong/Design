# OLEANDER Training — Route State Semantics

Training ID: `OLEANDER-TRN-2026-08-17-ROUTE-STATE`

## Problem
The current data-visualization skill preserves spatial topology but did not define how operational states such as `NORMAL / DEGRADED / CLOSED / UNKNOWN` must remain distinguishable when hue is unavailable or weak. This can create a false PASS: route geometry is correct while operational meaning collapses.

## Practice
A synthetic route with unchanged topology was rendered in two state systems:

- v1 / REJECT: state meaning carried mainly by color.
- v2 / KEEP FOR TRAINING: color + stroke pattern + marker geometry + explicit endpoint behavior + text.

`CLOSED` receives a hard-stop treatment. `UNKNOWN` is deliberately sparse and labelled `do not assume open`; it is not drawn as a weak version of normal operation.

## Independent Design Crit
- First visual gate: PASS in v2; route remains the primary read.
- Composition / proportion / hierarchy: PASS.
- Typography: PASS; labels support rather than replace state graphics.
- Spatial truth: PASS within calibration boundary; topology is unchanged.
- Scale / field truth: N/A / HOLD; this is synthetic calibration data.
- Node readability: PASS.
- Interaction: N/A; static route-state calibration.
- Professional finish: KEEP FOR TRAINING.

The grayscale derivative was reopened separately. v2 preserves meaningful distinction through pattern, marker form, hard stop and text, while v1 collapses heavily toward a uniform route.

## Failure knowledge
1. Color-coded status is not a complete state system.
2. `UNKNOWN` must not inherit the visual grammar of an open route when the project requires fail-closed interpretation.
3. `CLOSED` and `DEGRADED` need different endpoint/continuity behavior; otherwise the distinction becomes severity styling rather than operational meaning.
4. Topology correctness does not prove state-semantic correctness.
5. Grayscale review is a required low-cost regression check for critical state graphics.

## External calibration
W3C WCAG 2.2 SC 1.4.1 requires that color not be the only visual means of conveying information. WCAG 2.2 SC 1.4.11 requires sufficient contrast for meaningful non-text graphical information and state indicators. These accessibility principles are used here as calibration constraints; this practice is not a claim of full WCAG conformance.

## Skill delta
Updated `oleander-skills/oleander-data-viz/SKILL.md` with an `Operational route-state semantics gate` covering topology/state separation, non-color cues, CLOSED hard stops, UNKNOWN fail-closed presentation, DEGRADED distinction, grayscale proof, source-state provenance and promotion checks.

## Transfer
Applies to route maps, wayfinding, operational network diagrams, facility/service maps, mobile route UI, exhibition navigation and spatial status graphics. It does not authorize changing source topology or inventing real closure/field status.
