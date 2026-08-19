# C04 CH16-P01 v3.1｜Presentation Contract

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Page: `CH16-P01`

## Authority correction

Current C04 integration rule is explicit:

`ORIGINAL BOARD ≠ FINAL PUBLIC PIXEL`

ODB-02 remains the design-source anchor and near-read/source support. The final CH16-P01 public surface must use a cleaner current representation of the body/product/use relation while preserving the original design identity.

The previous v3.0 rule that promoted the full original board to the direct final public carrier is superseded.

## ODB-02 usage

The original board **may be shown**, but only as:

- `DESIGN SOURCE`;
- `SOURCE / EVOLUTION`;
- `NEAR-READ SUPPORT`.

It must not be relabeled as the final current public pixel.

## No-crop rule｜2026-08-19 user constraint

When ODB-02 is displayed:

- preserve the full original frame;
- preserve original aspect ratio;
- use `contain`, never `cover`;
- no clipping mask that removes board content;
- no partial detail crop presented as if it were the source board;
- no crop made merely to fit a fixed viewport.

If the board plus current representation cannot be read professionally in one viewport/page, use **carousel or sequential full-frame presentation** instead of cropping or compressing.

### Carousel behavior

A valid carousel may contain separate roles such as:

1. current clean representation / first read;
2. full uncropped ODB-02 source board;
3. technical/currentization proof when relevant.

Every source-board slide must contain the complete ODB-02 frame. A later technical/detail image is a different artifact and must be labeled as such; it is not a cropped continuation of ODB-02.

Desktop and mobile may recompose order and scale, but may not delete content or crop the original source board.

## Source-byte condition

Exact ODB-02 bytes are not currently materialized in the execution runtime. Therefore actual offline/Web embedding of the original board remains `HOLD_NO_SOURCE_BYTES` until the exact source is materialized.

This HOLD does not authorize using a screenshot recreation, derivative currentization, C23 drawing or AI-generated substitute as the source-board slide.

## Truth boundary

Historical source-board dimensions/load remain source-board content only and are not promoted to current engineering controls.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
