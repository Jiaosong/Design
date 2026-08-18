# C04｜Remote Raster Materialization Attempt 2｜2026-08-18

## Result

`ENV-03 LAND COVER = HOLD`  
`ENV-04 WATER HISTORY = HOLD`

This is an evidence-state result, not an execution omission. No substitute pixels were generated.

## ENV-03｜ESA WorldCover 2021 v200

Official source characteristics confirmed in this pass:
- WorldCover 2021 = `v200`;
- 10 m global land-cover product;
- 11 land-cover classes;
- EPSG:4326;
- analytical Map layer available as Cloud-Optimized GeoTIFF tiles;
- official WMS/WMTS is RGB presentation and is not suitable as the analytical pixel source.

Attempted access routes included the official data-access/AWS grid path. The runtime could resolve the official binary grid URL but could not materialize the binary AOI classification pixels into the local reproducible package.

Therefore:
- no forest percentage;
- no cropland percentage;
- no bare-rock boundary;
- no categorical AOI raster claim;
- no OSM feature absence converted into land-cover absence;
- no WMS RGB / screenshot / AI vegetation pattern converted into evidence.

## ENV-04｜JRC Global Surface Water

Official dataset characteristics confirmed in this pass:
- downloadable analytical products use 30 m mapped layers;
- `occurrence` encodes long-term water frequency;
- `seasonality` encodes months of water presence;
- the v1.4 historical record covers through 2021; the current JRC access page also documents later update/correction caveats.

The official download page and delivery mechanisms were resolved, but AOI occurrence / seasonality GeoTIFF pixels were not materialized into the reproducible local package in this runtime.

Therefore:
- no historical water-frequency percentage is claimed for the C04 AOI;
- no seasonal water envelope is drawn;
- current OSM river width is not used as historical water width;
- no cached RGB Web Map Service tile is treated as analytical history data.

## Hard boundary

`SOURCE EXISTS ≠ AOI PIXELS MATERIALIZED`  
`VIEWER / WMS RGB ≠ ANALYTICAL RASTER`  
`NO PIXEL READBACK = HOLD`  
`HOLD ≠ PERMISSION TO INVENT`

## Next action

Replace only ENV-03 / ENV-04 after a real COG/STAC/WCS/download path can be materialized, hashed, cropped to the correct AOI, independently reopened, and reconciled with source metadata.