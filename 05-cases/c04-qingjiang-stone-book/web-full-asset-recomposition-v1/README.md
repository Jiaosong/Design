# C04｜Web Full-Asset Recomposition v1

State: `ACTUAL WEB MATERIAL DELTA / MAIN CANDIDATE / FIELD OPEN / NO_PROMOTION`

This successor does **not** inherit the old fixed 20-screen deck behavior. It recomposes C04 from the full Existing Design Asset Atlas and the actual App/Game Map + Physical/Memory currentization already merged into `main`.

## Continuous public sequence
1. Hero — `先游清江，再读清江。`
2. Qingjiang culture content engine
3. BOAT / CABLE / WALK journey
4. editable game-style route map
5. visitor-facing Qingjiang App (Today / Route / Read / My Book)
6. full Thirteen Imprints library
7. R06 scene + audience depth + recovery
8. R13 body/return reduction
9. Physical/body currentization
10. Memory/IP currentization
11. Return

No fixed page/screen count is used.

## Canonical editable dependencies
The GitHub source reuses, rather than duplicates, the already-merged editable assets:
- `../digital-currentization/app-game-map-v1/assets/qingjiang-game-map-main.svg`
- `../physical-memory-currentization-v1/assets/P02_railing_rest_current.svg`
- `../physical-memory-currentization-v1/assets/P01_step_light_mechanism.svg`
- `../physical-memory-currentization-v1/assets/M01_qingjiang_journal_spread.svg`
- `../physical-memory-currentization-v1/assets/MEMORY_grammar.svg`

## Raster image layer
`build_crops.py` deterministically crops four existing D source PNGs. No generative image is used. Exact Drive source IDs, crop boxes, byte counts and SHA-256 values are in `CROP_MANIFEST_v1.json`.

The raster crops intentionally exclude board text. All formal Web titles, copy, labels, App text, map text, dimensions and annotations remain HTML/SVG editable text.

## Actual independent portable Web persisted to Drive
The first Drive HTML persisted during this run embedded the raster crops but still referenced repository SVG relative paths. That file was immediately demoted and renamed `SUPERSEDED_PARTIAL__...`; it is **not** the current portable receipt.

The current Drive carrier is a true single-file HTML: the four clean raster crops **and** all map / Physical / Memory SVGs are embedded inside the HTML. It contains no relative asset dependency.

- Drive folder: `C04_WEB_FULL_ASSET_RECOMPOSITION_v1`
- folder id: `1o0Er4SLxhwVvErfcWaIVzogJ4Jvo6Owt`
- CURRENT portable HTML: `C04_WEB_FULL_ASSET_RECOMPOSITION_v1_PORTABLE_FULL.html`
- CURRENT file id: `1iePFyl5vZrRzKEmLMBpv5JPB4r0-0egu`
- bytes: `649914`
- SHA-256: `58b20cb20eac0b2a0b8bd6ce8518ff38e87283892543a0d0bec09683f7b9b164`
- previous partial file id: `1x6KbC2m53XgbWwfMSoCTnrg1WZdEwA5Q` → `SUPERSEDED_PARTIAL`, not Current.

## Finished-product readback
The initial composition was rejected once because external SVG `<object>` elements rendered blank in the finished-product test. The source was repaired to SVG `<img>` references and re-reviewed.

Current source readback:
- Desktop: `1440×1000`, full-page height `12069 px`, horizontal overflow = `false`.
- Mobile: `390×844`, full-page height `14311 px`, horizontal overflow = `false`.
- Focused mobile review: App / Map / Physical / Memory readable.

Current **single-file Drive portable** was independently reopened with system Chromium after all raster + SVG assets were embedded:
- desktop `1440×1000` → `12069 px`, no horizontal overflow;
- mobile `390×844` → `14311 px`, no horizontal overflow;
- all `7/7` embedded image layers decoded with non-zero natural dimensions.

## Design Crit
- Overall Web: `KEEP_AFTER_REVISION / MAIN CANDIDATE`.
- Strongest current section: `App / Game Map integration`.
- Weakest current section: `Culture visual specificity`; it still needs a verified Qingjiang-specific culture visual/diagram rather than generic decoration.
- Physical: P02 + Journal are strongest; PHY-01 remains `HOLD`, not false selection.
- R06 / R13: non-generative crops from existing D assets; no measured geometry or site-photo claim is created by crop.
- Mobile fixed navigation footprint is a refinement item, not a current blocking defect.

## Complete local delivery bundle
- `C04_WEB_FULL_ASSET_RECOMPOSITION_v1.zip`
- bytes: `7234093`
- SHA-256: `dcef64ded2b0168e5a95f4909eb970b6a9bc2e1678d1fa4a1134710ab2762d87`

The full ZIP remains a local/user-downloadable delivery artifact in this run; the independently openable portable HTML is persisted to Drive and the reproducible text/code/lineage is persisted in GitHub. Do not claim the ZIP itself is Drive-persisted unless a later binary upload receipt exists.

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
