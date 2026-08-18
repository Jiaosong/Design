# SOURCE NOTE｜C04 GIS Redo Split v0.2

## Current project authority
- `C04_CURRENT.md` / Project Architecture v3.2.
- `C04_ACTIVE_EXECUTION_CURRENT.md`.
- `ROUTE-03 = LOCKED CURRENT` for route relational topology.
- Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`.

## Terrain
- Open-Meteo Elevation API.
- API documentation states the service uses Copernicus DEM 2021 GLO-90 at about 90 m resolution.
- This run preserves 441 previously materialized elevation samples on a 21×21 regular WGS84 context grid.
- The grid is a **remote context corridor**, not the scenic-area boundary.

## Qingjiang context line
- OpenStreetMap Qingjiang centerline segment.
- Used only as remote context geometry.

## Land cover
- Intended analytical authority: ESA WorldCover 2021 v200.
- Official product: 10 m, EPSG:4326, 11 land-cover classes, 3×3 degree COG tiles.
- A real 2020 `N30E108` tile index was independently located as fallback evidence, but AOI pixels were not successfully materialized in this runtime.
- Therefore: `HOLD / NO SUBSTITUTE PIXELS`.

## Surface-water history
- Intended analytical authority: JRC Global Surface Water v1.4.
- Official product: 30 m; occurrence 0–100%; seasonality in months; Landsat-derived 1984–2021 record.
- AOI pixels were not successfully materialized in this runtime.
- Therefore: `HOLD / NO SUBSTITUTE PIXELS`.

## Current operations
First-party/operator evidence used in this research pass supports:
- 2025: via ferrata and water projects opened at Honghua Peak Forest.
- 2026: cableway serves local resident commuting between Xintang and Shadi.
- 2026: missed-last-service incident confirms Return / fallback is an actual operational issue.
- 2026: landscaping and maintenance work covers port and Honghua Peak Forest areas.

Exact new-program anchors are NOT assigned onto ROUTE-03 unless already spatially bound.
