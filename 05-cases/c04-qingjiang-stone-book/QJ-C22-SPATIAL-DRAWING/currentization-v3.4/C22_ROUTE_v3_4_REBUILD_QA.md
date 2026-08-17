# C22-01 v3.4 — Route-grounded rebuild QA

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Drawing: `DRW-C04-C22-01`  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`

## Why v3.1 / v3.2 were rejected

Both versions treated route lines as a drawing-language problem before resolving what the lines represented. This inverted authority: the route shape should come from visitor movement evidence, not from a graphic system.

## v3.4 correction

The drawing is rebuilt around one semantic fact: **the dominant line is the visitor walking route**.

- Macro access is separated above the walking route: `浑水河码头 OR 自驾云坛口 → 云坛口旅游码头 → cross-river cable → cable upper station`.
- The main field is an **unfolded route transcription** based on the C04 R2 remote-loop candidate.
- Red Flower Stone Forest is shown only as `VIEW OBJECT / OPTIONAL SPUR`.
- Thirteen-Imprints identifiers are attached as small reading marks; they have no independent connection lines.
- Route geometry is intentionally unfolded for sequence readability and does not claim geographic shape.

## Post-generation visual check

Actual SVG was rendered through Inkscape and the 2384 px preview was reopened.

Producer observations after repair:
- route is the first visual read;
- no dashboard/card-wall composition;
- no abstract node network competing with the route;
- red-flower-stone-forest spur reads as subordinate;
- labels no longer collide materially in the route field;
- C22 truth state remains visible but visually subordinate;
- far-read and grayscale derivatives generated.

This is producer QA only. No `PIXEL KEEP`, `MAIN KEEP`, or `PROFESSIONAL FINISH PASS` is self-issued.
