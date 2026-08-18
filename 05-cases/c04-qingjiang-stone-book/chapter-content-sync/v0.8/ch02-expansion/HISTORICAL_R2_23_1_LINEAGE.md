# Historical R2.23.1 lineage reconciliation

Status: `PROVENANCE ONLY / NOT CURRENT AUTHORITY`

## Trigger
User supplied ChatGPT share `6a8414a6-b71c-83ec-a465-5ffbdf1a7e02`. The current web runtime could not retrieve the share body, so no unread share content is treated as verified evidence. Project-history retrieval surfaced the earlier `R2.23.1_remote-reconstruction` chain as the likely related CH02/GIS lineage.

## Recovered historical chain
- Approx. date: 2026-08-01.
- Stage: `R2.23.1_remote-reconstruction`.
- Historical source stack: OSM + registered local guide map + GlobalBuildingAtlas `ours2` (historical record: 153 LoD1 buildings) + SRTM 30 m.
- Historical CRS: `EPSG:32650`.
- Historical outputs: drawing-set PDF, CAD GIS base DXF, GIS base GeoJSON, 8-node coordinate CSV, K01–K12 coordinate CSV, QA report, README.
- Historical Git record: branch `agent/r2-23-1-remote-reconstruction`, commit `09d1295`, recorded as **not pushed**.
- Historical semantic boundary: remote reconstruction / provisional; not a survey result.

## Current authority decision
`R2.23.1` must not be resurrected as current route, geometry, raster, node-coordinate, building-base, or placement authority.

Current CH02 remains governed by:
- `ROUTE-03 = LOCKED CURRENT`;
- the 2026-08-18 stable environmental figure IDs;
- current raster materialization gates for ENV-03 / ENV-04;
- `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS`.

The historical SRTM 30 m usage does **not** close the current raster gate. Any reuse requires fresh byte retrieval/readback, CRS/datum/NoData verification, trustworthy AOI binding, and comparison against current route/source carriers.

## No-loss / no-pollution
Preserve valid R2.23.1 files and methods as provenance, QA comparison material, and source-history evidence. Do not auto-inherit its precision claims, coordinates, K01–K12 placement, building base, or route geometry into the current project.
