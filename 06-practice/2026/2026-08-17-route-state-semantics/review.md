# Design Crit — Route State Semantics

## Verdict
`v1 REJECT → v2 KEEP FOR TRAINING`

## Common gate
- Authority boundary: PASS — synthetic route only; no project field state, closure, geometry, or safety claim.
- Topology preservation: PASS — v1 and v2 use the same route logic; only state encoding changes.
- Editable source: PASS — SVG retained.
- Grayscale derivative: PASS — generated and reopened outside the source SVG.

## Design quality gate
- First visual gate: PASS in v2. Route remains the dominant read; state graphics do not become a dashboard.
- Composition: PASS. Four states sit on one continuous route with no equal-card fragmentation.
- Proportion: PASS. Critical `CLOSED` and `UNKNOWN` markers receive stronger local form without overwhelming the route.
- Hierarchy: PASS. `NORMAL → DEGRADED → CLOSED / UNKNOWN` can be distinguished through continuity behavior and marker geometry.
- Typography: PASS. Labels clarify state semantics but are not the sole carrier.
- Material / spatial realism: N/A. This is a route-state diagram, not a physical material or spatial render.
- Scale: N/A / HOLD. No real distance, slope, or field measurement is claimed.
- Node readability: PASS.
- Interaction: N/A. Static calibration only.
- Narrative: PASS. The comparison demonstrates the failure of color-only state coding and the correction.
- Professional finish: KEEP FOR TRAINING.

## Failure found
The color-only version is structurally correct but semantically fragile. In grayscale, state distinction collapses heavily. `UNKNOWN` is particularly dangerous because a continuous line can be mistaken for a weaker but still-open continuation.

## Repairs
1. Add redundant stroke patterns.
2. Change marker geometry by state.
3. Give `CLOSED` an explicit hard-stop / X treatment.
4. Make `UNKNOWN` sparse and explicitly state `do not assume open`.
5. Reopen a grayscale derivative and verify the state hierarchy again.

## Reusable rule
Topology correctness and operational-state correctness are separate gates. A route can be geometrically accurate and still be professionally wrong if `CLOSED`, `DEGRADED`, and `UNKNOWN` are not unambiguous at the actual delivery scale.
