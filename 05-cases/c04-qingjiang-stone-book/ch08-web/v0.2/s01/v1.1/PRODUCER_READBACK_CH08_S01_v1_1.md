# CH08-S01 v1.1｜Producer Actual-Pixel Readback

State: `PRODUCER CANDIDATE / NO SELF-KEEP / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO_PROMOTION`

## Current authority consumed
- CH08 current role: `MASTER DESIGN STRATEGY / MASTER INTEGRATION / NOT A SECOND SUBSYSTEM`.
- source slot: `CH08-S01-MAIN`.
- current image source: `SRC05 / 5pszhdcxjz.jpg`, SHA256 `da94acea1ae3d7961919a390f9f0ef27ceee2b06bdaf5dd897ee63fb95897f4b`.
- image generation: `OFF`.
- Image Ops execution owner: `T-VISUAL-IMAGE-OPS-001` (`TOOL / execution template / ACTIVE`).
- v1.1 operation IDs are **project-scoped bindings**, not new global OLEANDER recipe names.

## Material delta from v1.0 producer study
1. Keeps the CH14-derived bounded editorial frame and image-first mobile order.
2. Replaces vague aesthetic treatment with explicit non-destructive display operations: tonal field, bounded Bone Mist wash mask and a low-opacity ink-edge raster preview.
3. Every operation has a query-addressable off state. `?fx=off` restores the complete unfiltered source display without changing layout/copy.
4. The duplicate edge layer is the same underlying source and remains the same `CH08-S01-MAIN` semantic image slot; it is not a second content-image allocation.

## Runtime readback
Desktop `1920×1080`:
- scrollWidth/clientWidth = `1920/1920`; horizontal overflow = `0`.
- scrollHeight/clientHeight = `1080/1080`.
- broken images = `0`; recorded console/page errors = `0`.
- bounded image field = x `551`, y `185.5`, w `1317`, h `648`.

Mobile `390×844`:
- scrollWidth/clientWidth = `390/390`; horizontal overflow = `0`.
- full scrollHeight = `1277`.
- broken images = `0`; recorded console/page errors = `0`.
- image-first field = x `0`, y `64`, w `390`, h `405.11`.

Both DOM image layers reopen at natural source size `1080×608`; no new pixel detail is claimed. Direct file/localhost deployment is outside this readback evidence.

## Image Ops attack tests
All measured visual deltas are bounded to the desktop source image rectangle `[551,186,1868,834]`; copy/layout pixels are not changed by toggling the three image operations.

| Test | Mean absolute RGB delta | Changed pixel ratio |
|---|---:|---:|
| all FX off → on | 8.5913 | 0.4106 |
| tonal off → on | 1.2035 | 0.382501 |
| wash off → on | 6.6038 | 0.200365 |
| edge off → on | 1.9994 | 0.344066 |

Actual derivatives exist for: `GRAYSCALE`, complete `FX_OFF`, `TONAL_OFF`, `WASH_OFF`, `EDGE_OFF`, desktop and mobile target-size review.

## Producer-observed open points｜not an independent verdict
- Source native resolution is `1080×608`; the reviewed desktop display modestly upscales it. The edge preview may improve separation but **does not restore resolution or create evidence**.
- Desktop title and landscape intentionally carry high visual weight; whether their balance reaches portfolio-level first-read quality remains for independently attributable Professional Design Review.
- Full effect-off baseline remains readable and source-complete; independent review must still judge whether the effect-on version materially improves rather than merely styles the page.

## Review boundary
This document records implementation/readback evidence only. It issues no `KEEP`, `MAIN KEEP` or `Professional Design PASS`.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
