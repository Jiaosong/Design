# CH04 Pixel Reconstruction Fidelity Report v0.1

## Gate state

- Reference Materialization: **PASS**
- Reference Frame Lock: **PASS / 1672×941**
- Browser Runtime Readback: **PASS via Chromium + Playwright**
- Matched-scale Pixel Diff: **EXECUTED**
- Fidelity Repair Cycle: **EXECUTED**
- Full Independent Reconstruction: **HOLD** — scenic carriers are reused as bounded content assets
- Professional Design PASS: **NOT SELF-GRANTED**

## Final pixel metrics

| Page | MAE RGB | RMSE RGB | Pixels max-diff > 10 | Pixels max-diff > 25 |
|---|---:|---:|---:|---:|
| P01 | 2.109834 | 14.686139 | 2.3503% | 1.6979% |
| P02 | 1.830847 | 13.528381 | 2.0815% | 1.4321% |
| P04 | 1.959802 | 15.082116 | 2.2518% | 1.5951% |
| P05 | 1.451488 | 12.096224 | 1.9212% | 1.3153% |

Interior scene carriers are pixel-equivalent because they are explicit source-bound content assets. Remaining mismatch is concentrated in browser-rendered typography, antialiasing, page-background raster noise/gradients, and header/footer chrome.

## Authority preservation

- P03: `ROUTE-03 = LOCKED CURRENT`; no route redraw, smoothing, or topology rewrite.
- P06: existing R06 landscape/source carrier remains the same; only browser scaling is applied uniformly.
- P01/P02/P04/P05: reference visual carriers are presentation references only and do not become spatial/field authority by being placed in the webpage.

## Reconstruction classification

OLEANDER `REVIEW.md` states that direct source reuse cannot be counted as independent reconstruction evidence. Therefore this build is classified as:

`REFERENCE-BOUND PRODUCTION WEB RECONSTRUCTION`

and not:

`FULL INDEPENDENT PIXEL-IDENTICAL REPRODUCTION PASS`.

The scoped fidelity claim is:

`WEB LAYOUT / TYPOGRAPHIC CHROME / FRAME / SPACING / PAGE ASSEMBLY + SOURCE-BOUND VISUAL CARRIER PLACEMENT`.

## Browser QC

- 1672×941 locked desktop frame: rendered.
- 1366×768: no horizontal overflow.
- 390×844: no horizontal overflow.
- Six navigation controls are keyboard-focusable native buttons.
- All six visual carriers have alt text.
- External network dependencies: `0`.

## Promotion boundary

Artifact existence, browser readback, checksums and low pixel error do not equal independent Professional Design PASS. No `KEEP / MAIN KEEP / PROMOTION` is self-granted here.
