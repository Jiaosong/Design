# C04 GIS Data Frontier v0.7.1

## Current state
- Formal GIS board package: **v0.7**
- GitHub PR #259: **MERGED**
- Merge commit: `ea1a6af2c927292040676c7d5e181caabed3666b`
- `image_generation_used=false`
- Professional Design Review: **PENDING**

## Raster materialization frontier

| Dataset | Native resolution | C04 tile / AOI | Current state | Promotion boundary |
|---|---:|---|---|---|
| Copernicus DEM GLO-30 Public | ~30 m | expected N30/E109 tile | BLOCKED_IN_CURRENT_RUNTIME | DSM only; local pixel readback required |
| SRTMGL1 | 1 arc-second | `N30E109.SRTMGL1.hgt.zip` verified in ESA STEP index | AVAILABLE AT INDEX / DOWNLOAD FAILED | fallback only after local parse/readback |
| ESA WorldCover 2021 v200 | 10 m | `N30E108` grid-inferred; verify official grid | HOLD | no WMS RGB / screenshot / generated substitute |
| JRC Global Surface Water v1.4 | 30 m | C04 AOI | HOLD | occurrence / seasonality pixels required |

## Current runtime result
A fresh retry against the ESA STEP SRTMGL1 tile failed to materialize binary bytes locally.  
Therefore **tile existence is verified, but no new 30 m raster is promoted into C04 analysis authority**.

## Independent review
OLEANDER Artifact Review v1.1 requires `COMPLIANCE PASS + PROFESSIONAL DESIGN PASS` before KEEP.  
The current producer can perform actual-preview readback and machine/compliance QA, but **producer self-check is not independent review**. No separate reviewer execution path is available in the current tool surface, so the state remains:

`INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO FAKE VERDICT`

## v0.8 entry condition
Do not redraw v0.7 at fake precision. v0.8 starts only after:
1. real finer raster bytes are locally materialized;
2. CRS / datum / NoData are verified;
3. AOI crop and pixel readback succeed;
4. terrain derivatives are rerun from that raster;
5. actual preview and independent review are completed.

## Truth boundary
`REMOTE DATA ≠ FIELD OBSERVED`  
`DSM ≠ DTM`  
`TILE EXISTS ≠ PIXEL READBACK`  
`CI PASS ≠ DESIGN KEEP`  
`PRODUCER READBACK ≠ INDEPENDENT REVIEW`
