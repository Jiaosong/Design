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
The Web reuses, rather than duplicates, the already-merged editable assets:
- `../digital-currentization/app-game-map-v1/assets/qingjiang-game-map-main.svg`
- `../physical-memory-currentization-v1/assets/P02_railing_rest_current.svg`
- `../physical-memory-currentization-v1/assets/P01_step_light_mechanism.svg`
- `../physical-memory-currentization-v1/assets/M01_qingjiang_journal_spread.svg`
- `../physical-memory-currentization-v1/assets/MEMORY_grammar.svg`

## Raster image layer
`build_crops.py` deterministically crops four existing D source PNGs. No generative image is used. Exact Drive source IDs, crop boxes, byte counts and SHA-256 values are in `CROP_MANIFEST_v1.json`.

The raster crops intentionally exclude board text. All formal Web titles, copy, labels, App text, map text, dimensions and annotations remain HTML/SVG editable text.

## Actual portable Web persisted to Drive
A self-contained portable HTML was independently rebuilt with the four clean raster crops embedded as JPEG data URIs while retaining the canonical SVG dependencies.

- Drive folder: `C04_WEB_FULL_ASSET_RECOMPOSITION_v1`
- folder id: `1o0Er4SLxhwVvErfcWaIVzogJ4Jvo6Owt`
- portable HTML id: `1x6KbC2m53XgbWwfMSoCTnrg1WZdEwA5Q`
- portable HTML: `618554 bytes`
- SHA-256: `23969128fe8ff6699023870db1c867f755a3957db4c2f99b345b04c3cc249f87`

## Finished-product readback
The initial composition was rejected once because external SVG `<object>` elements rendered blank in the finished-product test. The source was repaired to SVG `<img>` references and re-reviewed.

Current readback:
- Desktop: `1440×1000`, full-page height `12069 px`, horizontal overflow = `false`.
- Mobile: `390×844`, full-page height `14311 px`, horizontal overflow = `false`.
- Focused mobile review: App / Map / Physical / Memory readable.
- GitHub-portable composition was independently reopened with system Chromium using the same embedded raster pixels + canonical SVGs; desktop/mobile dimensions matched the reviewed v2 layout.

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

The full ZIP remains a local/user-downloadable delivery artifact in this run; the actual portable HTML is persisted to Drive and the reproducible text/code/lineage is persisted in GitHub. Do not claim the ZIP itself is Drive-persisted unless a later binary upload receipt exists.

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
