# SP01-R02｜GIS Reality Gate

Current status: **QGIS RUNTIME VERIFIED / PROJECT REALITY OPEN**.

Artifact review: **POST-REVIEW PASS** for the training/runtime package.  
Project candidate promotion: **NO**.

## What was actually executed
GitHub Actions run **#5 / 31454788861** executed the exercise with real QGIS/PyQGIS on Ubuntu 24.04:

- QGIS 3.34.4-Prizren
- PyQGIS 3.34.4-Prizren
- GDAL 3.8.4
- PROJ 9.4.0
- algorithm: `qgis:heatmapkerneldensityestimation`
- 24 synthetic training points
- numeric `weight` field verified as Integer
- radii: 75 / 150 / 300 m
- pixel sizes: 10 / 25 / 50 m
- 9 real QGIS GeoTIFF outputs
- native PyQGIS `.qgz` project
- 3 A3 QGIS Layout PNGs for radius 75 / 150 / 300 at pixel 25 m

Final workflow artifact ID: `9087641476`  
Artifact digest: `sha256:68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`

## Truth split
- **QGIS Runtime Gate**: PASS / VERIFIED.
- **Metric processing workflow**: VERIFIED in an explicit metric CRS.
- **Project CRS Gate**: OPEN. EPSG:3857 is a runtime-only placeholder, not a site-appropriate project CRS.
- **Project Data Gate**: OPEN. The 24 points are exercise-only synthetic coordinates.
- **Candidate promotion**: prohibited until real project CRS + authoritative project data close.

Therefore the correct status is:

`QGIS RUNTIME VERIFIED / PROJECT REALITY OPEN`

not `PROJECT REALITY PASS`.

## Runtime matrix
`qgis_process` executed Quartic raw KDE for all 9 combinations:

- bandwidth radius: 75 / 150 / 300 m
- pixel size: 10 / 25 / 50 m
- weight field: `weight`
- kernel: Quartic (`KERNEL=0`)
- output: raw KDE (`OUTPUT_VALUE=0`)

## Pixel-size sensitivity observed from actual QGIS rasters
These are exercise observations, not project acceptance criteria.

- **75 m radius**: component count stable at 4; max centroid shift ≈ 6.15 m; 50%-peak area spread ≈ 4.82%; inside-integral spread ≈ 0.091%.
- **150 m radius**: component count varies 1 ↔ 2 across pixel sizes; max centroid shift ≈ 2.20 m; 50%-peak area spread ≈ 5.56%; inside-integral spread ≈ 0.123%. This is the clearest resolution-sensitive case in the exercise.
- **300 m radius**: component count stable at 1; max centroid shift ≈ 3.60 m; 50%-peak area spread ≈ 5.30%; inside-integral spread ≈ 0.435%.

## Edge-effect observation
The 0–1000 m dashed box is an exercise study boundary. Spill fraction outside that box is measured from the real QGIS raster outputs; it is **not** a corrected edge-bias estimate.

- 75 m: 0% in this exercise.
- 150 m: about 0.02–0.13% depending on pixel size.
- 300 m: about 4.00–4.41% depending on pixel size.

This makes the 300 m bandwidth visibly more sensitive to the chosen study boundary.

## Final GIS layout review
The first successful runtime was not released automatically. Post-generation review found and corrected:

1. **Data type issue** — first GPKG import left `weight` as String. Rebuilt with `AUTODETECT_TYPE=YES` and a numeric-field hard assertion.
2. **Missing final GIS artifact** — initial runtime had GeoTIFF/QGZ but no QGIS Layout page for visual review. Native QGIS Layout export was added.
3. **Cross-view scale failure** — initial maps zoomed to each raster extent, causing different map scales across 75/150/300 m sheets. Rejected and rebuilt with a common extent `[-150,-150,1200,1200]` and identical map scale ≈ 1:5510.204.
4. **Legend semantics** — automatic raster legend showed renderer values that could be mistaken for KDE values. Replaced with explicit per-sheet stretch semantics: dark=higher, light=lower; shade is not comparable as an absolute density value between bandwidth sheets.
5. **Edge-effect visibility** — added the dashed 0–1000 m exercise study boundary to all maps.
6. **Scale bar** — unified to 0–300 m on all three maps.
7. **North arrow** — intentionally omitted because the synthetic XY plane has no asserted geographic orientation; this omission is documented on-sheet rather than silently implying north.

Final A3 layouts were manually reopened after the last runtime and passed occlusion, clearance, hierarchy, common-scale, study-boundary and evidence-semantics review.

## Cross-run reproduction
Runs #4 and #5 used the same executable GIS sources. The three p25 GeoTIFFs and all metric/gate JSON/CSV outputs are byte-identical across runs. QGIS Layout PNG file hashes differ because of PNG metadata, but decoded pixels are identical. GPKG/QGZ binaries are not required to be byte-identical because container/project metadata can change; their semantic/runtime checks remain consistent.

## Artifact Review System v1.0
Final gate result for the training/runtime package:

- AR-G01—G10 Common: PASS
- AR-S03 Data: PASS
- AR-S04 Code / Parametric: PASS
- AR-S05 GIS: PASS WITH PROJECT REALITY OPEN
- AR-S07 Documentation: PASS
- AR-S09 Release: PASS

Hard truth boundary remains:

**Software Reality closed. Project Reality remains open.**

## Reopen condition
SP01 should not be promoted by adding more synthetic KDE variants. Reopen the Reality Gate only when there is:

1. a real site/location;
2. an appropriate site/projected CRS chosen from actual geography;
3. authoritative project point/event data with source/date/schema;
4. a project-defined study boundary and evidence-based interpretation question.

At that point rerun the same bandwidth / pixel / edge review against real project evidence and perform AR-S05 again.
