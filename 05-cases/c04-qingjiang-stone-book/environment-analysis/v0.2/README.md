# C04 GIS Analysis Redo v0.2

Project: `PRJ-C04-QINGJIANG-SHISHU`  
State: `EXECUTED / PRODUCER READBACK COMPLETE / INDEPENDENT DESIGN REVIEW PENDING`  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`

This package supersedes the earlier synthetic proxy map package for MAIN consideration. It follows the current `oleander-research`, `oleander-data-viz`, `oleander-delivery-qc` and Artifact Review discipline.

## Figure status

- `ENV-01｜DEM slope/aspect` — EXECUTED / SOURCE-GROUNDED / independent Design Review pending.
- `ENV-02｜Drainage accumulation` — EXECUTED / DERIVED EVIDENCE / independent Design Review pending.
- `ENV-03｜Land cover` — HOLD. ESA WorldCover source exists, but local AOI analytical pixels were not read back. No substitute pixels were fabricated.
- `ENV-04｜Water history` — HOLD. JRC Global Surface Water source exists, but local AOI occurrence/seasonality pixels were not read back. No synthetic water-history envelope was fabricated.
- `ENV-05｜Solar exposure` — EXECUTED / DERIVED SCENARIO / independent Design Review pending.
- `ENV-06｜Current operations conflict` — EXECUTED / `ROUTE-03` preserved 1:1 + current reported operations overlay / independent Design Review pending.

## Binary authority

The complete binary/data package is stored in Google Drive as `C04_GIS_REDO_SPLIT_v0.2.zip`, Drive file id `1ZU_c8U7DBIo2xqsZpNcSczN082QBTuMS`.

Independent retrieval + rebuild byte comparison:
- bytes: `1,587,551`
- SHA256: `0ce26c1573b9fcf989fc5af507d2a9e2d5d90ad6c12855ffc14323a47ff6b7b7`
- byte equivalence: `true`
- persistence state: `PASS`

Persistence PASS proves recoverability/byte parity only. It does **not** prove Professional Design PASS.

## Included text authority in GitHub

- `SOURCE_NOTE.md`
- `TRANSFORMATION_LOG.md`
- `GEOMETRY_AUTHORITY_NOTE.md`
- `EVIDENCE_BOUNDARY.md`
- `FIGURE_STATUS_REGISTER.csv`
- `DATA_DICTIONARY.csv`
- `MACHINE_QC.json`
- `DRIVE_PERSISTENCE_READBACK.json`
- `INDEPENDENT_REVIEW_REQUEST.json`

## Hard boundary

`REGIONAL DATA ≠ SITE OBSERVATION`  
`REMOTE TERRAIN ≠ FIELD MEASURED`  
`ROUTE TOPOLOGY ≠ SURVEY GEOMETRY`  
`DERIVED DRAINAGE ≠ HYDRAULIC DESIGN`  
`SOLAR SCENARIO ≠ MEASURED RADIATION`  
`SOURCE EXISTS ≠ AOI PIXEL READBACK`  
`EXECUTED ≠ DESIGN PASS`
