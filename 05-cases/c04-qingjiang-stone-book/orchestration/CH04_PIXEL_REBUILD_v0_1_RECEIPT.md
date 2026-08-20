# CH04 Pixel Web Reconstruction v0.1｜Receipt

Status: `REFERENCE-BOUND WEB RECONSTRUCTION / BROWSER READBACK / PIXEL DIFF EXECUTED / BINARY UNSYNCED / NO_PROMOTION`

## Scope

User instruction: stop image generation and use the OLEANDER reconstruction skill to reproduce the approved CH04 visual reference as a real webpage.

Implemented as fixed-reference-frame HTML/CSS/SVG at `1672×941`, with six CH04 pages and responsive viewport scaling.

- P01/P02/P04/P05: editable HTML/CSS page chrome + bounded reference visual carrier for the complex scene area.
- P03: current `ROUTE-03 = LOCKED CURRENT` SVG carrier reused without route redraw.
- P06: current R06 SVG/landscape carrier reused without changing the real-scene logic.
- No new image-generation call is part of this reconstruction.

## Local production artifacts

- `CH04_PIXEL_REBUILD_v0_1.html` — editable source with relative assets.
- `CH04_PIXEL_REBUILD_v0_1_PORTABLE.html` — one-file offline build.
- `C04_CH04_PIXEL_REBUILD_v0_1_PACKAGE.zip` — source + references + browser readbacks + pixel diffs + QC.

Package bytes: `55,947,804`

Package SHA256: `f72abfbda2e75c1e999fee571154e262316bfa4691e43880cd8fe9865b6ee595`

Portable HTML bytes: `8,529,081`

Portable HTML SHA256: `7249898b6677eaf63bf97b0e3a3533dc58c415d0cc488a1ca8b8b4722af4e4cc`

## OLEANDER fidelity execution

Reference bytes were materialized locally and hashed. The locked frame is `1672×941`. Browser screenshots were rendered in Chromium using Playwright, followed by matched-scale pixel comparison and a second repair pass.

Final MAE RGB:

- P01 `2.109834`
- P02 `1.830847`
- P04 `1.959802`
- P05 `1.451488`

See `CH04_PIXEL_REBUILD_v0_1_FIDELITY_REPORT.md` for boundary and metrics.

## Browser / interaction QC

- 1672×941 reference frame: rendered.
- 1366×768: no horizontal overflow.
- 390×844: no horizontal overflow; fixed canvas scales to viewport width.
- Six page-nav controls are native keyboard-focusable buttons.
- All six visual carriers have alt text.
- External network dependencies: `0`.

## Persistence boundary

The binary package exists and is hash-verified in the active production runtime, but this connector session does not expose a valid local-file → Drive/GitHub-binary upload bridge. Therefore binary persistence is explicitly `UNSYNCED`; this receipt does not claim Drive persistence or repository recovery of the 55 MB package.

GitHub text receipt / review state is persisted; binary promotion is blocked until a durable binary store receives the exact hashed package.

## Truth boundary

P01/P02/P04/P05 scene carriers are reference/presentation visuals and are not geometry, field, geological, accessibility, or engineering authority.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
