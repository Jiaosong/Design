# CH13-01 v4 — OLEANDER Artifact Review

## Object
`PRJ-C04-QINGJIANG-SHISHU / CH13-01 / SHORT RECOVERY / v4`

## Source precedence
- Identity authority: `ODB-02 / 可拆卸倚靠休息板.png / USER ORIGINAL DESIGN SOURCE`.
- Materialized descendant used for this presentation surface: `05_C04_F01_PRODUCT_DESIGN_CURRENTIZED_v4_1.png`.
- Scene binding is a direct rectangular source crop only: `[60,215,1600,930]`.
- Body/use binding is a direct rectangular source crop only: `[1640,230,2495,740]`.
- Both are rendered with `object-fit: contain`; no browser `cover` recrop.
- D Hero is not used. No image generation. No product geometry redraw.

## Material delta from rejected v3
- v3 mixed chapter strategy, intervention ladder and F01 into one board; v4 narrows the page to one claim: **short recovery lets the body continue**.
- The full source scene becomes the dominant field.
- The action sequence stays same-source and secondary.
- Removed intervention-gradient UI strip and removed repeated dashboard-like levels.
- Removed repeated `经过，不被迫停；疲劳，才短时倚靠。` from the authored layer; the source crop retains its original wording while the authored near-read now says `动作先读，构造后读。`
- Desktop title collision from the first v4 render was found and repaired before final export.

## Actual runtime readback
- Chromium system binary via Playwright/Xvfb.
- Desktop `1920×1080`: `scrollWidth=1920`, `scrollHeight=1080`, horizontal overflow=false.
- Mobile `390×844`: `scrollWidth=390`, full document height `1214`, horizontal overflow=false.
- Mobile is semantic vertical reflow, not desktop crop.
- Both bound PNGs decode and remain uncropped by CSS.

## Objective artifact gates
- SOURCE HIERARCHY: PASS.
- SOURCE CROP TRACEABILITY: PASS.
- IMAGE UNIQUENESS: PASS for this surface; no D Hero reuse.
- DESKTOP OPEN / REFLOW: PASS.
- MOBILE OPEN / REFLOW: PASS.
- TRUTH BOUNDARY: PASS.
- INDEPENDENT PROFESSIONAL DESIGN VERDICT: NOT CLAIMED / PENDING.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
