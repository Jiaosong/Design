# CH16-P01 v3.3 — Runtime Readback

State: `STATIC CONTRACT READBACK COMPLETE / BROWSER READBACK BLOCKED / DESIGN REVIEW PENDING`

## Static source readback

Confirmed in the authored HTML and interaction contract:

- primary visible resource is the merged derived vector `physical-memory-currentization-v1.2/assets/P02_railing_lean_rest_v1_2.svg`;
- resource path resolves from the P01-v3.3 directory by `../../../physical-memory-currentization-v1.2/assets/...`;
- stage aspect ratio remains `16 / 10`, matching the resource `1600×1000` viewBox;
- image fit is `object-fit: contain`;
- no `cover` or crop behavior is used;
- focus states are clipped to the resource stage while the resource itself remains complete;
- interaction states are `CLEAN / BODY / ASSEMBLY / SERVICE`;
- click/tap controls, direct hotspots and keyboard state switching are authored;
- mobile switches the control rail and supporting evidence to horizontal scroll-snap rather than clipping the resource;
- ODB-02 image/file is not referenced as a visible asset anywhere in the HTML.

## Runtime limitation

A local Chromium / Playwright readback was attempted in the execution runtime. Local `file://` and localhost navigation was rejected by runtime administrator policy (`ERR_BLOCKED_BY_ADMINISTRATOR`). Chromium CLI did not produce a valid screenshot within the execution window.

Therefore:

`BROWSER PASS = NOT CLAIMED`.

This blocker does **not** justify replacing the source, screenshot-faking the page, or treating static source checks as a browser/design pass.

## Review boundary

- Source/interaction contract: `EXECUTED`.
- Static source readback: `COMPLETE`.
- Browser readback: `BLOCKED / PENDING`.
- Machine governance CI: `PENDING PR HEAD`.
- Independent OLEANDER design review: `PENDING`.
- `PIXEL KEEP / MAIN KEEP / PROFESSIONAL FINISH PASS`: `NOT ASSIGNED`.

Truth boundary:
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
