# CH08-S01 v1.4｜Producer Actual-Pixel Readback

State: `PRODUCER CANDIDATE / USER REJECTED v1.3 IMAGE TREATMENT / NO SELF-KEEP / NO_PROMOTION`.

## Material delta from v1.3
- removes CSS radial white-fog masks, duplicate visible source-image layers, scanline-like image overlays and SVG filter-based faux wash;
- replaces them with deterministic raster derivatives generated from the unchanged SRC05 bytes;
- default page displays one final derivative only; SOURCE / TONAL / WASH / FINAL remain recoverable stage states;
- `WASH-TONAL` now uses edge-preserving smoothing + neutral ink-on-paper tonal mapping, with jade retained only by a bounded river mask;
- `WASH-MASK` uses deterministic multi-scale absorption derived from seeded fields and source luminance, with central-karst protection;
- `INK-EDGE` uses source-derived structural edges with explicit spatial owner masks and settlement-detail suppression.

## Current source
`SRC05 / ch08_s01_qingjiang_landscape_official_20230711.jpg` — `da94acea1ae3d7961919a390f9f0ef27ceee2b06bdaf5dd897ee63fb95897f4b` — 1080×608 — original bytes unchanged.

## Runtime
Desktop 1920×1080: overflow `0` / broken images `0` / errors `0`.
Mobile 390×844: overflow `0` / broken images `0` / errors `0` / scrollHeight `1299`.
Small 320×700: overflow `0` / broken images `0` / errors `0`.

## Operator delta evidence
- SOURCE → TONAL mean abs RGB `8.3592`, changed ratio `0.413665`.
- TONAL → WASH mean abs RGB `1.5495`, changed ratio `0.344504`.
- WASH → FINAL mean abs RGB `0.7691`, changed ratio `0.369854`.
- all changed-pixel bounding boxes remain inside the photograph region.

Attack readbacks include target-size, small-size, grayscale, print-mono, and each operation stage.

Producer observation only: the image now reads as a single matte ink-on-paper plate rather than a photograph with CSS fog/filter effects. This is not a Professional Design verdict.
