# C04｜清江十三印 App + Game Map v1

State: `MAIN CANDIDATE / CURRENTIZATION / FIELD OPEN / NO_PROMOTION`

This package is a real front-end redesign of the existing Qingjiang digital system. It replaces the research-dashboard first read with a visitor-facing mobile product while preserving route/evidence constraints.

## Product structure
- `TODAY｜今日清江` — journey/service entry, route and return before content.
- `ROUTE｜探索地图` — game-style relational map with BOAT / CABLE / WALK, branching exploration, Thirteen Imprints, rest, service and Return.
- `READ｜十三印` — R01–R13 remain a complete skippable/reorderable content library; audience depth changes the action/value, not the route.
- `MY BOOK｜我的石书` — personal route/photo/read/rest/listen/write memory; no score or required collection.
- `SERVICE / RETURN` — always reachable; unknown remains fail-closed; no-phone fallback remains valid.

## Interaction checks
`PASS`: four main tabs, Service/Return access, R06 dialog, audience-depth switch, map layer filter, removal of numeric completion semantics.

## Design / production rules
- No AI image is used in this v1 build.
- UI and map text are HTML/SVG vector/editable text.
- Standalone map: `assets/qingjiang-game-map-main.svg`.
- Map is `NTS / RELATIONAL`, not survey/GPS authority.
- R01: no forced UI. R13: high-attention PLAY off.
- FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION.

## Design Crit
Current result: `KEEP_AFTER_REVISION / MAIN CANDIDATE` for App + standalone Game Map.
The next pixel-level improvement should use real Qingjiang source imagery/terrain evidence only where it increases specificity without implying measured geography.
