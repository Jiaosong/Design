# Design Crit — Route State Semantics

## Verdict
`v1 REJECT → v2 REVISE → v3 KEEP FOR TRAINING`

## Common gate
- Authority boundary: PASS — synthetic route only; no project field state, closure, geometry, or safety claim.
- Topology preservation: PASS — all variants use the same route logic; only state encoding and label placement change.
- Editable source: PASS — SVG retained.
- Grayscale derivative: PASS — generated and reopened outside the source SVG.
- Compact-size derivative: PASS after v3 repair — 720 px review performed separately.

## Design quality gate
- First visual gate: PASS in v3. Route remains the dominant read; state graphics do not become a dashboard.
- Composition: PASS. Four states sit on one continuous route with no equal-card fragmentation.
- Proportion: PASS. Critical `CLOSED` and `UNKNOWN` markers receive stronger local form without overwhelming the route.
- Hierarchy: PASS. `NORMAL → DEGRADED → CLOSED / UNKNOWN` can be distinguished through continuity behavior and marker geometry.
- Typography: PASS after v3. `CLOSED`, `UNKNOWN`, and `NO FORWARD ROUTE` no longer collide at compact review size.
- Material / spatial realism: N/A. This is a route-state diagram, not a physical material or spatial render.
- Scale: N/A / HOLD. No real distance, slope, or field measurement is claimed.
- Node readability: PASS.
- Interaction: N/A. Static calibration only.
- Narrative: PASS. The comparison demonstrates the failure of color-only state coding and the correction.
- Professional finish: KEEP FOR TRAINING.

## Failure found
### v1 — REJECT
The color-only version is structurally correct but semantically fragile. In grayscale, state distinction collapses heavily. `UNKNOWN` is particularly dangerous because a continuous line can be mistaken for a weaker but still-open continuation.

### v2 — REVISE
Multi-channel semantics worked, but the actual 720 px derivative exposed a local typography collision around `CLOSED / UNKNOWN / NO FORWARD ROUTE`. Full-size success did not survive compact viewing.

## Repairs
1. Add redundant stroke patterns.
2. Change marker geometry by state.
3. Give `CLOSED` an explicit hard-stop / X treatment.
4. Make `UNKNOWN` sparse and explicitly state `do not assume open`.
5. Reopen a grayscale derivative and verify state hierarchy again.
6. Reopen a 720 px compact derivative, separate the three high-risk labels, then recheck marker recognition without relying on text.

## Reusable rule
Topology correctness and operational-state correctness are separate gates. A route can be geometrically accurate and still be professionally wrong if `CLOSED`, `DEGRADED`, and `UNKNOWN` are ambiguous in grayscale or at the actual delivery scale. Full-size visual PASS cannot override a compact-size regression.
