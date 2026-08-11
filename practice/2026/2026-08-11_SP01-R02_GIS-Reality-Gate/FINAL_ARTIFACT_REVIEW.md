# SP01-R02｜Final Artifact Review

Review system: **OLEANDER Artifact Review System v1.0**  
Final training/runtime artifact status: **POST-REVIEW PASS**  
Practice status: **QGIS RUNTIME VERIFIED / PROJECT REALITY OPEN**  
Project candidate promotion: **NO**

## Runtime evidence
- Final workflow run: `31454788861` / run #5
- Head SHA: `9dab6e96f4446a0a8c76a7e7c825a6f98957274e`
- Workflow job: `qgis-reality-gate` — success
- Artifact ID: `9087641476`
- Artifact digest: `sha256:68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`
- QGIS: 3.34.4-Prizren
- PyQGIS: 3.34.4-Prizren
- GDAL: 3.8.4
- Actual QGIS KDE outputs: 9 GeoTIFFs
- Native QGIS project: `SP01_R02_QGIS_Runtime.qgz`
- Native QGIS Layout review maps: 3 PNGs

## A｜Common Review
- AR-G01 Identity & Naming — **PASS**
- AR-G02 Version & Status — **PASS**; software/runtime status is kept separate from project reality.
- AR-G03 Completeness — **PASS** for the runtime-evidence package.
- AR-G04 Internal Consistency — **PASS**.
- AR-G05 Cross-file Consistency — **PASS**; CSV → GPKG → GeoTIFF → metrics → gate decision align.
- AR-G06 Evidence & Truth — **PASS**; EPSG:3857 and 24 points remain explicitly synthetic/runtime-only.
- AR-G07 Open & Integrity — **PASS**; GitHub artifact ZIP and QGZ pass archive integrity tests; all nine TIFF signatures valid.
- AR-G08 Reproduction — **PASS at data/pixel/semantic level**; final p25 GeoTIFFs and metric/gate outputs are byte-identical across runs #4/#5; layout decoded pixels are identical although PNG metadata makes file hashes differ.
- AR-G09 Change Traceability — **PASS**; rejected intermediate revisions are recorded below.
- AR-G10 Final Artifact Review — **PASS**; final run #5 maps were reopened and visually reviewed.

## B｜AR-S03 Data
**PASS**

- Feature count = 24.
- `x_m` = Real, `y_m` = Real, `weight` = Integer.
- First successful run exposed `weight` as String; this was treated as a review defect and corrected with `AUTODETECT_TYPE=YES` plus a hard numeric-field assertion.
- All coordinates and weights remain exercise-only inputs.

## B｜AR-S04 Code / Parametric
**PASS**

- QGIS installation and runtime are performed in GitHub Actions, not simulated locally.
- `qgis_process` runs all nine KDE combinations.
- PyQGIS creates the QGZ and final QGIS Layout maps.
- Gate logic is fail-closed: real software execution can close the software gate while Project CRS / Project Data stay OPEN.
- Workflow assertions require 9 TIFFs, 3 layouts, numeric weight, common extent/scale and false candidate promotion.

## B｜AR-S05 GIS
**PASS WITH PROJECT REALITY OPEN**

### CRS / projection
- Runtime raster CRS: EPSG:3857 — **PASS as explicit metric runtime placeholder**.
- Project/site CRS: **OPEN**.
- No claim that EPSG:3857 is appropriate for a real future site.

### Source / date
- Source: 24 synthetic exercise points — correctly labeled.
- Project authoritative dataset: **OPEN**.

### Geometry / fields
- 24 features successfully materialized in GPKG.
- Numeric coordinate/weight schema verified.

### KDE contract
- algorithm: `qgis:heatmapkerneldensityestimation`
- Quartic kernel
- raw output
- radii 75 / 150 / 300 m
- pixels 10 / 25 / 50 m
- 9 outputs verified

### Pixel sensitivity
Observed from real QGIS rasters, but retained as exercise evidence only:
- r75: component count 4; max centroid shift ≈ 6.15 m; area50 spread ≈ 4.82%.
- r150: component count 1↔2; max centroid shift ≈ 2.20 m; area50 spread ≈ 5.56%; marked resolution-sensitive for this exercise.
- r300: component count 1; max centroid shift ≈ 3.60 m; area50 spread ≈ 5.30%.

### Edge effect
Spill outside the exercise 0–1000 m study box:
- r75: 0% in this exercise.
- r150: ≈ 0.02–0.13%.
- r300: ≈ 4.00–4.41%.

This is an observed spill metric, not an edge-bias correction and not a project criterion.

### Layout / visual semantics
- 3 final A3 maps use the identical common extent `[-150,-150,1200,1200]`.
- all three have identical map scale ≈ 1:5510.204.
- all three use a 0–300 m scale bar.
- 0–1000 m exercise study boundary is explicitly dashed.
- per-sheet raster min/max stretch is explicitly disclosed; shade is used for morphology comparison only and cannot be compared as an absolute density value between bandwidth sheets.
- north arrow is intentionally omitted because the synthetic XY plane has no asserted geographic orientation.
- final visual inspection: hierarchy / boundary / occlusion / clearance / scale / cross-view consistency — **PASS**.

## B｜AR-S07 Documentation
**PASS**

Claim Audit confirms:
- QGIS runtime is stated as VERIFIED only after real Actions execution.
- Project CRS and Project Data remain OPEN.
- score/candidate status is not used to override reality evidence.
- no synthetic metric is described as a project requirement.
- rejected intermediate outputs are not treated as final evidence.

## B｜AR-S09 Release
**PASS**

- Actions artifact uploaded successfully.
- Final artifact ZIP can be fully decompressed without CRC errors.
- QGZ archive can be decompressed without errors.
- all nine TIFFs have valid TIFF signatures.
- final run artifact digest is recorded.

## Rejected revisions

### Revision 01 — Runtime successful, review rejected
Real QGIS processing succeeded, but `weight` was imported as String and there was no native QGIS Layout review page. Runtime PASS did not override artifact review.

### Revision 02 — Layout produced, review rejected
Three maps used each raster's own extent. This silently changed map scale between bandwidths. Automatic legend also showed renderer-style 255/0 values that could be misread as KDE values, and scale-bar fit was poor. Cross-view / scale / GIS-semantics review failed.

### Revision 03 — Final
- common map extent and scale;
- numeric weight field;
- explicit study boundary;
- corrected comparison key;
- common 0–300 m scale bar;
- documented north-arrow omission;
- real QGIS Layout output;
- final reopen review PASS.

## Final gate decision

**Software Reality Gate: CLOSED / VERIFIED**  
**Project CRS Gate: OPEN**  
**Project Data Gate: OPEN**  
**SP01 Project Reality: OPEN**  
**Candidate promotion: NO**

Reopen only with a real site, appropriate projected CRS, authoritative project data and an evidence-based spatial question.
