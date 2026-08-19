# C04 App v1.29 — Implementation Readback

## Material delta
- Added four non-evidence texture assets: paper, monochrome ink mist, Qingjiang-family blue-green water-current wash, and deep-water blue-black ink.
- Texture strength is screen-specific rather than global: TODAY/READ/BOOK/SERVICE remain low-contrast; ROUTE/R06 use water-current material motion; R13 carries the strongest dark ink atmosphere.
- Added material response to exploration behavior states (`SEEK / APPROACH / FOCUS / ENTER / REVEAL / WITHDRAW / RETURN`) via subtle texture shift/scale, not neon glow.
- Added a restrained side exploration cue and brush-ring map-anchor focus. ROUTE-03 geometry remains unchanged.
- R06 optional reveal enters as an ink-sheet layer; R13 keeps `PLAY OFF` and body-first priority.

## Runtime facts
- 390×844: document width == viewport width; minimum visible button target = 44.00px; keyboard route pan delta = 40px; JS/page errors = 0.
- 430×932: document width == viewport width; minimum visible button target ≈ 44.00px; keyboard route pan delta = 40px; JS/page errors = 0.
- Reduced Motion: running animations = 0; errors = 0.
- Seven App screens expose a material texture layer; texture assets do not modify route/state data.

## Repair during readback
- First pass exposed a ~30px `contextClose` width. Repaired to 44px minimum and increased route-child rail/button height to 44px.
- Screenshot waits were extended beyond transition duration so review frames represent settled pixels rather than cross-fade intermediate states.

## Claim boundary
`Texture / motion / runtime PASS ≠ Professional Design PASS`.

Textures are `AI-GENERATED TEXTURE ASSET / NON-EVIDENCE / REPLACEABLE`. They do not prove Qingjiang landscape, route, GPS, live status, safety, or field conditions.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS / STATUS UNKNOWN`.
