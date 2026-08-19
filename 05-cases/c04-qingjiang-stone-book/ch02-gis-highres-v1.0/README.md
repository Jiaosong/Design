# C04 CH02 GIS GLO-30 v1.0

Project: `PRJ-C04-QINGJIANG-SHISHU`

State: `REAL SOURCE MATERIALIZED / DERIVATIVES EXECUTED / PRODUCER ACTUAL-PREVIEW R2 COMPLETE / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO_PROMOTION`.

## Source precision delta

The terrain-analysis authority is no longer the historical `21×21 / 441` remote sample grid.

Current terrain source:

- dataset: Copernicus DEM GLO-30 Public;
- source model: DSM, not bare-earth DTM;
- tile: `Copernicus_DSM_COG_10_N30_00_E109_00_DEM`;
- raw tile: `44,951,183 bytes`;
- raw SHA256: `e63e9787f8f6daffa90da722d72c1375767dc65ab558bd8535d4f295ffec2f06`;
- CH02 analysis extent: `[109.75, 30.29, 109.81, 30.315]` WGS84;
- extent semantics: analytical corridor only, **not a surveyed site polygon**;
- metric analysis CRS: `EPSG:32649`;
- analysis grid: `193×94` envelope at `30×30 m`;
- valid source-derived metric cells: `17,766`;
- NoData edge cells: `376`, explicitly `-9999` and excluded from statistics / D8.

Corrected derived statistics:

- elevation: `370.0–1005.7 m`, median `627.2 m`;
- slope: median `12.9°`, P90 `28.4°`, max `74.6°`;
- D8 accumulation: P90 `18`, P99 `159`, max `965` contributing cells;
- relative solar mean: summer `0.924`, equinox `0.785`, winter `0.518`.

## Real execution / repair

Existing real QGIS/GDAL runtime was reused as an execution adapter only; no second GIS environment was invented.

- corrected QGIS/GDAL run: `32214746886` = `SUCCESS`;
- workflow artifact: `9351963976`;
- artifact digest: `sha256:fb797a44ad221fe8bffeb462a278595b60be80d4c5faedbacc0b26e235831ae0`.

First materialization exposed a real defect: `-tap` UTM warp edge pixels had no explicit destination NoData and were read as false `0 m`. That run was rejected. The corrected run uses `-dstnodata -9999` and excludes invalid edge cells from all statistics and D8 routing.

The temporary adapter in the frozen `practice/` tree was removed after execution; the final branch carries no `practice/` delta.

## Current producer drawings

- `ENV-01` Slope / Aspect — real 30 m terrain, 20 m vector contours, mapped sections.
- `ENV-02` D8 Potential Convergence — real 30 m D8; R1 cell-link comb rejected in producer readback; R2 groups the same source links above P96.5 into topology-preserving continuous potential-convergence paths. These paths are **not observed channels**.
- `ENV-SYN-01` Environmental Synthesis — same extent / scale, slope + D8 potential convergence + winter solar kept as separate questions; no composite risk score.
- `ENV-03` Land Cover — `HOLD`.
- `ENV-04` Water History — `HOLD`.

No image generation was used.

## CH14 binding

Current C04 CH14 LIGHT implementation:

- Bone Mist `#F1EDE4`
- River Black `#111918`
- Deep Water `#133B3C`
- Jade Current `#2E7571`
- Wet Stone `#65706A`
- Sediment Sand `#D8C9B1`
- Cinnabar `#B8543E`

Grammar: `CONTEMPORARY EDITORIAL + LANDSCAPE SPACE / LINE + TRACE`; functional/cartographic readability remains above brand decoration.

## Recoverable binary source package

Google Drive: `C04_CH02_GIS_GLO30_v1.0_SOURCE_COMPLETE.zip`

- Drive file ID: `1ftO58EWiMVhv3jMb8Z15cLKQ5u2KTywD`;
- provider raw readback: `57,733,141 bytes`;
- local + independent raw readback SHA256: `4989aa835444a9eb25b7e626162147b7b2a5471331e4acc6496612221c6e1086`;
- ZIP integrity: PASS.

The package contains the raw Copernicus tile, AOI crop, metric raster, slope/aspect/hillshade/20 m contours/D8/solar native GIS data, editable SVG masters, 3200×1800 previews, QC derivatives and receipts.

## Truth / review boundary

`REMOTE SOURCE-GROUNDED / FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.

GLO-30 does not prove surveyed site boundary, field-measured elevation, bare-earth terrain beneath vegetation/buildings, observed drainage, hydraulic capacity, geohazard safety, constructability, or independent `Design PASS / MAIN KEEP`.
