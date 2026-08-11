# SP01-R02｜GIS Reality Gate

Status before workflow execution: **QGIS RUNTIME PENDING**.

## Purpose
Close the missing software-runtime evidence from SP01-R01 without pretending that synthetic training coordinates are real project evidence.

## Truth split
- **QGIS Runtime Gate**: can be closed by an actual `qgis_process` / PyQGIS run.
- **Projected CRS workflow**: exercised in an explicit metric CRS, but EPSG:3857 remains a runtime placeholder.
- **Project CRS Gate**: OPEN until a real site and appropriate projected CRS are selected.
- **Project Data Gate**: OPEN because the 24 points are exercise-only synthetic coordinates.
- **Candidate promotion**: prohibited until Project CRS + Project Data gates close.

## Actual runtime matrix
The GitHub Actions runner must execute `qgis:heatmapkerneldensityestimation` for:

- bandwidth radius: 75 / 150 / 300 m
- pixel size: 10 / 25 / 50 m
- weight field: `weight`
- kernel: Quartic (`KERNEL=0`)
- output: raw KDE (`OUTPUT_VALUE=0`)

This produces **9 real QGIS GeoTIFF outputs**.

## Reality checks
`analyze_qgis_outputs.py` reads the actual GeoTIFFs and records:

- raster CRS / dimensions / extent / pixel size;
- weighted centroid and high-density area;
- 50% peak hotspot component count;
- pixel-size sensitivity for each bandwidth;
- density spill outside the exercise 0–1000 m study box as an edge-effect observation.

The edge metric is not a correction model and must not be promoted to a project criterion.

## Release logic
A successful workflow may set:

`QGIS RUNTIME VERIFIED / PROJECT REALITY OPEN`

It may **not** set Project Reality PASS.

## Review
After the workflow succeeds, the artifact must still undergo OLEANDER Artifact Review System v1.0:

- AR-G01—G10 Common;
- AR-S03 Data;
- AR-S04 Code / Parametric;
- AR-S05 GIS;
- AR-S07 Documentation;
- AR-S09 Release.

For AR-S05 explicitly review CRS, distance units, source/date, geometry validity, KDE parameters, pixel sensitivity, edge effects, legend/scale semantics if a map is later produced, and evidence-to-conclusion limits.
