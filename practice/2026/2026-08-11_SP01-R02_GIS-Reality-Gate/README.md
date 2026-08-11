# SP01-R02｜GIS Reality Gate

Current status: **QGIS RUNTIME VERIFIED / PERSISTENCE PASS / PROJECT REALITY OPEN**.

Artifact review: **POST-REVIEW PASS for the training/runtime package, with AR-S09 valid only after PAP rescue**.  
Project candidate promotion: **NO**.

## 1｜What actually ran

GitHub Actions run `31454788861` executed the exercise with real QGIS/PyQGIS on Ubuntu 24.04:

- QGIS 3.34.4-Prizren
- PyQGIS 3.34.4-Prizren
- GDAL 3.8.4
- PROJ 9.4.0
- algorithm `qgis:heatmapkerneldensityestimation`
- 24 synthetic training points
- numeric `weight` field verified as Integer
- radii 75 / 150 / 300 m
- pixel sizes 10 / 25 / 50 m
- 9 real QGIS GeoTIFF outputs
- native PyQGIS `.qgz` project
- 3 A3 QGIS Layout PNGs for radius 75 / 150 / 300 at pixel 25 m

Historical Actions artifact:
- artifact ID `9087641476`
- digest `sha256:68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`

## 2｜Truth split

- **QGIS Runtime Gate:** PASS / VERIFIED.
- **Metric processing workflow:** VERIFIED in an explicit metric runtime CRS.
- **Project CRS Gate:** OPEN. EPSG:3857 is a runtime-only placeholder, not a site-approved project CRS.
- **Project Data Gate:** OPEN. The 24 points are synthetic exercise coordinates.
- **Candidate promotion:** NO.

Correct project state:

`QGIS RUNTIME VERIFIED / PROJECT REALITY OPEN`

not `PROJECT REALITY PASS`.

## 3｜PAP durable rescue

The original Actions artifact was later identified as an expiring provider artifact and therefore insufficient as the sole production-binary authority under `Production Asset Persistence Gate v1.0`.

P0 rescue completed on 2026-08-11:

- source digest: `68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`
- bytes: `759942`
- PAP durable Drive file ID: `12mafNIOtzzrYzIf2HTkjz4XcDq_xjSMI`
- Practice canonical mirror file ID: `1DMpgFdV_vhdRunRqI3GOBD4rFvNI9DJc`
- independent Drive retrieval: SHA exact match
- Practice mirror retrieval: SHA exact match
- ZIP integrity: PASS
- content spot-check: `.qgz`, GPKG, 9 GeoTIFFs, 3 QGIS Layout PNGs and runtime/gate evidence present

Therefore persistence is now:

**`PERSISTENCE PASS / RESCUED`**

This closes durable byte availability only. It does not close Project CRS or Project Data.

## 4｜Runtime matrix

`qgis_process` executed Quartic raw KDE for all 9 combinations:

- bandwidth radius: 75 / 150 / 300 m
- pixel size: 10 / 25 / 50 m
- weight field: `weight`
- kernel: Quartic (`KERNEL=0`)
- output: raw KDE (`OUTPUT_VALUE=0`)

## 5｜Pixel-size sensitivity observed from real QGIS rasters

Exercise observations only; not project acceptance criteria.

- **75 m:** component count stable at 4; max centroid shift ≈ 6.15 m; 50%-peak area spread ≈ 4.82%; inside-integral spread ≈ 0.091%.
- **150 m:** component count varies 1 ↔ 2; max centroid shift ≈ 2.20 m; 50%-peak area spread ≈ 5.56%; inside-integral spread ≈ 0.123%. This is the clearest resolution-sensitive exercise case.
- **300 m:** component count stable at 1; max centroid shift ≈ 3.60 m; 50%-peak area spread ≈ 5.30%; inside-integral spread ≈ 0.435%.

## 6｜Edge-effect observation

The 0–1000 m dashed box is an exercise study boundary. Spill fraction outside it is observed from real QGIS rasters; it is not an edge-bias correction.

- 75 m: 0% in this exercise.
- 150 m: about 0.02–0.13% depending on pixel size.
- 300 m: about 4.00–4.41% depending on pixel size.

## 7｜Final layout review

Post-generation review corrected the following before final evidence was accepted:

1. first GPKG import left `weight` as String → rebuilt with `AUTODETECT_TYPE=YES` plus numeric-field assertion;
2. initial runtime lacked native QGIS Layout review pages → added 3 A3 layouts;
3. initial maps used different raster extents → rejected and rebuilt using common extent `[-150,-150,1200,1200]` and identical map scale ≈ 1:5510.204;
4. renderer-value legend semantics could be mistaken for KDE values → replaced by explicit per-sheet stretch semantics;
5. exercise study boundary made visible;
6. scale bar unified to 0–300 m;
7. north arrow intentionally omitted because the synthetic XY plane has no asserted geographic orientation.

Final layouts passed hierarchy, occlusion, clearance, common-scale, study-boundary and evidence-semantics review.

## 8｜Artifact Review System v1.0

Current gate result:

- AR-G01—G10 Common: PASS
- AR-S03 Data: PASS
- AR-S04 Code / Parametric: PASS
- AR-S05 GIS: PASS WITH PROJECT REALITY OPEN
- AR-S07 Documentation: PASS
- **PAP-G0—G6: PASS / RESCUED**
- **AR-S09 Release: PASS only after PAP rescue**

An expiring Actions artifact by itself would not satisfy current AR-S09.

## 9｜CI governance correction

The original feature-branch workflow used mutable `actions/*@v4` refs and listened only to the old feature branch. The current-main successor corrects this to:

- immutable reviewed action SHAs;
- pull-request execution for relevant changes;
- durable `main` execution for relevant changes;
- `contents: read` least privilege.

This CI correction does not alter the historical runtime evidence identity.

## 10｜Reopen condition

Do not advance by generating more synthetic KDE variants. Reopen the Project Reality Gate only with:

1. a real site/location;
2. a site-appropriate projected CRS selected from actual geography;
3. authoritative project point/event data with source/date/schema;
4. a project-defined study boundary and evidence-based interpretation question.

**Software Reality closed. Persistence closed. Project Reality remains open.**
