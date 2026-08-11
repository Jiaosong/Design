# SP01-R02｜Final Artifact Review

Review system: **OLEANDER Artifact Review System v1.0**  
Current training/runtime artifact status: **POST-REVIEW PASS / PAP RESCUED**  
Practice status: **QGIS RUNTIME VERIFIED / PROJECT REALITY OPEN**  
Project candidate promotion: **NO**

## A｜Runtime evidence

Historical final runtime:
- GitHub Actions run `31454788861`
- head SHA `9dab6e96f4446a0a8c76a7e7c825a6f98957274e`
- artifact ID `9087641476`
- artifact digest `sha256:68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`
- QGIS / PyQGIS 3.34.4-Prizren
- GDAL 3.8.4
- 9 QGIS KDE GeoTIFFs
- native `SP01_R02_QGIS_Runtime.qgz`
- 3 native QGIS Layout PNGs

This is valid runtime evidence. The original Actions artifact, however, is an expiring transport and is not a qualified sole persistence authority.

## B｜Persistence review added after PAP v1.0

P0 durable rescue completed on 2026-08-11:

- exact rescued bytes: `759942`
- exact SHA-256: `68ce760293057b3595856b8c935ed3cb51c4c512ea6f9a6ea5eb5614b225d00c`
- PAP durable Drive file ID `12mafNIOtzzrYzIf2HTkjz4XcDq_xjSMI`
- Practice mirror file ID `1DMpgFdV_vhdRunRqI3GOBD4rFvNI9DJc`
- independent PAP Drive re-retrieval SHA: PASS
- independent Practice mirror re-retrieval SHA: PASS
- ZIP integrity: PASS
- required runtime contents spot-check: PASS

Decision:

**`PERSISTENCE PASS / RESCUED`**

PAP closes binary persistence only. It does not change GIS project-reality status.

## C｜Common Review

- AR-G01 Identity & Naming — **PASS**
- AR-G02 Version & Status — **PASS**; runtime, persistence and project reality are separated.
- AR-G03 Completeness — **PASS** for the training/runtime package.
- AR-G04 Internal Consistency — **PASS**.
- AR-G05 Cross-file Consistency — **PASS**; CSV → GPKG → GeoTIFF → metrics → gate decision align.
- AR-G06 Evidence & Truth — **PASS**; EPSG:3857 and 24 points remain explicitly synthetic/runtime-only.
- AR-G07 Open & Integrity — **PASS**; runtime archive/QGZ/TIFF integrity was verified, and durable rescue was independently reopened.
- AR-G08 Reproduction — **PASS at data/pixel/semantic level**; p25 GeoTIFF and metric/gate outputs were reproducible across the recorded runs; layout decoded pixels matched despite PNG metadata differences.
- AR-G09 Change Traceability — **PASS**; rejected intermediate revisions remain documented.
- AR-G10 Final Artifact Review — **PASS**.

## D｜AR-S03 Data

**PASS**

- 24 synthetic features.
- `x_m` Real, `y_m` Real, `weight` Integer.
- initial String-typed `weight` defect was rejected and corrected with `AUTODETECT_TYPE=YES` plus hard numeric assertion.
- no project dataset is claimed.

## E｜AR-S04 Code / Parametric

**PASS**

- real QGIS installation/execution in Actions, not simulated processing;
- all 9 KDE combinations executed;
- PyQGIS created QGZ and layouts;
- gate logic remains fail-closed: software can PASS while Project CRS/Data remain OPEN;
- current successor workflow pins external actions by immutable SHA and runs on relevant PR/main changes.

## F｜AR-S05 GIS

**PASS WITH PROJECT REALITY OPEN**

### CRS
- EPSG:3857 — accepted only as an explicit runtime metric placeholder.
- real project/site CRS — **OPEN**.

### Data
- synthetic exercise points — valid as training input.
- authoritative project data — **OPEN**.

### KDE contract
- `qgis:heatmapkerneldensityestimation`
- Quartic kernel
- raw output
- radii 75 / 150 / 300 m
- pixel sizes 10 / 25 / 50 m
- 9 outputs

### Sensitivity
- r75: 4 components; max centroid shift ≈ 6.15 m; area50 spread ≈ 4.82%.
- r150: 1↔2 components; max centroid shift ≈ 2.20 m; area50 spread ≈ 5.56%; resolution-sensitive in this exercise.
- r300: 1 component; max centroid shift ≈ 3.60 m; area50 spread ≈ 5.30%.

### Edge observation
- r75: 0% exercise spill.
- r150: ≈ 0.02–0.13%.
- r300: ≈ 4.00–4.41%.

These observations are not project criteria or edge-bias corrections.

### Layout
- common extent `[-150,-150,1200,1200]`;
- identical map scale ≈ 1:5510.204;
- 0–300 m scale bar;
- 0–1000 m dashed exercise boundary;
- per-sheet min/max stretch explicitly limited to morphology comparison;
- north arrow intentionally omitted for synthetic orientation.

## G｜AR-S07 Documentation

**PASS**

Documentation distinguishes:
- verified QGIS runtime;
- rescued durable persistence;
- OPEN Project CRS/Data;
- synthetic exercise metrics;
- no candidate promotion.

## H｜PAP-G0—PAP-G6

**PASS / RESCUED**

The exact historical runtime artifact was copied to qualified durable Drive storage, independently re-retrieved, SHA-verified and unzip-tested, with cross-system receipt recorded.

## I｜AR-S09 Release

**PASS AFTER PAP RESCUE**

Historical wording that treated successful Actions upload/decompression alone as sufficient for AR-S09 is superseded by this review.

Current rule:

`Actions runtime artifact + recorded digest` ≠ persistence PASS by itself.

AR-S09 becomes PASS here only because the later PAP-G0—G6 rescue is complete.

This does not authorize project promotion or public release.

## J｜Rejected revisions retained

1. Runtime succeeded but `weight` was String and no native QGIS Layout existed → rejected.
2. Layouts used different map extents/scales and ambiguous renderer-value legend semantics → rejected.
3. Final runtime used numeric weight, common extent/scale, explicit study boundary, corrected key, common scale bar, documented north-arrow omission and final reopen review → accepted as runtime evidence.

## Final decision

**Software Reality Gate: CLOSED / VERIFIED**  
**Production Binary Persistence: PASS / RESCUED**  
**Project CRS Gate: OPEN**  
**Project Data Gate: OPEN**  
**SP01 Project Reality: OPEN**  
**Candidate promotion: NO**

Reopen Project Reality only with real location, appropriate projected CRS, authoritative data and an evidence-based spatial question.
