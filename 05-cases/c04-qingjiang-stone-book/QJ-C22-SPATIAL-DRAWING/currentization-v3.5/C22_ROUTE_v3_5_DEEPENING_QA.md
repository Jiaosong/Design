# C04 / C22 Route v3.5 — Deepening QA

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Drawing: `DRW-C04-C22-01`  
State: `EXECUTED / ROUTE-GROUNDED / RENDERED / REOPENED / PRODUCER SELF-CHECKED / INDEPENDENT DESIGN REVIEW PENDING`

## Skills applied
- `oleander-story-and-board` (main): one primary claim + one primary visual, distance-readable board hierarchy, explicit sequence.
- `oleander-delivery-qc` (main): editable source + render + reopen + far-read + grayscale + package/version checks.
- `oleander-technical-drawing` PR #172 remains candidate-only and is used only as a calibration reference for source authority / section-reference discipline; it is not treated as merged authority.

## What was deepened
v3.4 correctly restored the first principle: the dominant line is the visitor route. v3.5 deepens that route without creating a parallel graphic system.

1. **Access threshold** — boat and road access remain separate variants, then visibly converge at Yuntankou before cable boarding.
2. **Walking journey** — one continuous route remains the visual first-read; route-width envelopes are editorial reading aids only, not mapped terrain.
3. **Direction** — sparse arrowheads show only the R2 research-transcription direction; the sheet states direction/version remains unvalidated.
4. **Junction proof** — the Honghua Stone Forest spur is isolated as `J-01 / OPTIONAL SPUR`, with a dedicated close-read inset. The main route visibly survives without the spur.
5. **Return proof** — the final closure is traced back to the cable station on the same route, not by inventing a separate Return line.
6. **Cross-sheet detail** — `C22-SEC-A`, frozen `C22-SEC-B / R06`, and `C22-SEC-C` are referenced at their actual route moments.
7. **Near-read detail** — three right-rail diagrams explain cable threshold, optional spur, and natural closure/return using route geometry rather than prose-only explanation.
8. **Thirteen Imprints** — R markers remain small attachments; no R-to-R linking line exists.

## Producer visual review
### First read
PASS at producer level: the walking journey is the largest and darkest continuous graphic. The right rail is subordinate and does not compete with the route.

### Route clarity
PASS at producer level: start/return, the optional spur junction, and natural closure are visually identifiable without reading long paragraphs.

### Detail hierarchy
PASS at producer level after repair: duplicated upper-stage captions were removed; duplicated R06 frozen text was removed; R06 remains only as a frozen section reference and small attached R marker.

### Far read
Generated and reopened at `596×421`. Route loop, cable strip, optional spur, and three right-rail insets remain distinguishable.

### Color-independent check
Grayscale derivative generated. Main route remains dominant by weight and continuity rather than hue alone.

## Technical QC
- SVG remains editable vector text/geometry.
- Inkscape SVG → PNG render: PASS.
- Final PNG size: `2384×1684`.
- Final render reopened after the repair cycle.
- No new raster dependency introduced.
- Repository source is a compacted editable SVG using CSS classes; compaction changes source serialization only.
- Compact SVG was independently rendered and compared against the authored verbose SVG render; `ImageChops` difference bounding box = `None`, i.e. pixel-identical in the executed comparison.

## Hashes
- authored verbose SVG SHA256: `7a05724ee4167ee8b269adf4a67ff910c4810ae0f0d0d8cf242322b7b8107737`
- GitHub compact editable SVG SHA256: `197623f59f9879264ef7ec6d76b89b574abc3bf703c169f1335f73c440b3cfbd`
- rendered PNG SHA256: `10a030d7305eb106e90ed82450d5eb364fe8a48dd4fd95ced2652c25b0cf068d`

## Version hygiene
Route-specific v3.4 files are superseded and removed from the current PR working tree after v3.5 persistence. The separate `C04_C22_01_LANDSCAPE_ANALYSIS_ATLAS_v3_4` lineage remains an independent support drawing and is not superseded by this route deepening.

## Truth boundary
The route is unfolded for sequence readability. Editorial envelopes, arrows and section references do not claim geographic shape, measured spacing, field direction, slope, steps, clear width, GPS, safety, capacity, accessibility or current operations.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`

No producer `PIXEL KEEP / MAIN KEEP / PROFESSIONAL FINISH PASS` is issued.
