# C04 / C22 Route v3.8 — Official-guide spatial transcription QA

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Object: `DRW-C04-C22-01`

## Why v3.5 was rejected

User review identified that v3.5 did not visually correspond to either the official guide or the real scenic-area morphology. The defect was structural, not cosmetic:

- route was artificially unfolded into an editorial loop;
- river / banks / cable / peak forest no longer inherited the official guide composition;
- the line became the subject instead of the landscape;
- the result read as a designer-made route diagram rather than Honghua Peak Forest.

Therefore v3.5 Route = `REVISE / SUPERSEDED`.

Local v3.6 and v3.7 experiments were also rejected before repository persistence.

## v3.8 correction

v3.8 re-anchors the sheet to the 2025-08-05 official hand-drawn guide first-read:

1. Qingjiang occupies the upper horizontal field.
2. North-bank Yuntankou/service is retained at the upper-left.
3. Cable crosses the river nearly vertically into the south-bank scenic area.
4. South-bank peak forest is the dominant field.
5. Walking route is drawn as a white terrain-following, branching, switchback carrier rather than an invented closed ring.
6. Rxx remains a small reading attachment and does not own the path.
7. Operator photographs are used only to calibrate morphology: steep karst, cliff/slope-following walkway, cable-in-peak-forest context.

## Important limitation

This is a professional vector transcription of the official guide's **composition and relation topology**, not a pixel-for-pixel trace and not a survey/GIS reconstruction.

Exact micro-route order, GPS, length, slope, stairs, clear width, accessibility, safety, capacity and current operating state remain open.

## Production QA

- SVG parsed and rendered through CairoSVG.
- Full render: `2384×1684`.
- Far-read derivative: `1192×842`.
- Full render reopened visually after generation.
- Main first-read: landscape / river / cable / official-guide path composition.
- No raster dependency embedded in editable SVG.

## Hashes

- SVG SHA256: `efc2cdfc5478d3f857234543d27539c44b715dbee411c2b49bb6e121c95bddda`
- PNG SHA256: `f17f2d9d212413ceb996fdc3e9a0b0785f3439ab2f675b46a648014f68a3b2d3`

## Producer state

`EXECUTED / SOURCE-REANCHORED / RENDERED / REOPENED / PRODUCER SELF-CHECKED / INDEPENDENT DESIGN REVIEW PENDING`

No producer `PIXEL KEEP`, `MAIN KEEP`, `PROFESSIONAL FINISH PASS`, Field PASS or Promotion.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
