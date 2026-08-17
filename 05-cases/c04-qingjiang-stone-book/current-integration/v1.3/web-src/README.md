# C04 Web v1.3 — Editable / Rebuildable Text Source

This directory stores the editable Web presentation source for the annotation-bound, no-compression C04 v1.3 carrier.

## Rebuild

Run:

```bash
python build.py
```

This concatenates:
- `page_top.html`
- `chapters/*.html` in numeric order
- `page_bottom.html`
- `style_parts/*.css` in numeric order

and creates `index.html` + `styles.css` beside `app.js`.

## Binary assets

Mature raster/SVG/video assets are deliberately not duplicated into Git history. Copy the `assets/` directory from the persisted production package `C04_WEB_v1_3_NO_COMPRESSION.zip` beside the rebuilt `index.html` before opening the page.

Persistent package:
`/Oleander/C04_Qingjiang-Stone-Book/CURRENT/C04_WEB_v1_3_NO_COMPRESSION.zip`

SHA256:
`58ec2a9808d74b8eb9d3ded8b6139971bd8a555f9f1a21b77f3a738958255b3d`

## Boundary

The 13 source chapter fragments are macro chapters, not a page-count policy. The current rendered Web contains 60 content blocks as an implementation readback only; count remains unbounded and no target range is defined.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / FIELD PASS=NONE / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
