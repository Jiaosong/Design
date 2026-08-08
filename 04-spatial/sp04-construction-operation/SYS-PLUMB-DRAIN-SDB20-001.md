# SYS-PLUMB-DRAIN-SDB20-001｜Silent-db20 Gravity Drainage & Venting System

- Status: SYSTEM HYPOTHESIS / DESIGN-READY FOR FUTURE TEST / NOT COMMISSIONED
- Layer: Spatial / SP04 Construction & Operation
- Canonical source: Notion `SYS-PLUMB-DRAIN-SDB20-001`
- Verified: 2026-08-08

> Stable system logic only. Real project loads, geometry, installed batches, acoustic results, drainage tests, firestop approval, prices and G9 records remain in Notion/project evidence.

## Fact boundary

Geberit China currently publishes Silent-db20 as a high-sound-insulation building drainage system. Published system data include PE-S2 material, linear expansion coefficient 0.17 mm/(m·K), long-term service temperature -20–60°C, and sizes including DN56–DN150.

Concrete China-catalog product used to close the expansion-control gap:

- `310.012.14.1` — Silent-db20 double-flange expansion socket, DN100 / d110 mm;
- manufacturer states it can compensate material expansion for pipe/fitting runs up to 6 m and that insertion-depth dimensions are referenced to 20°C installation temperature.

Other system components confirmed in the China catalog include DN100/d110 cleaning fitting `310.334.14.1`, clamp connection `310.003.14.3`, and DN100 three-dimensional branch fitting `310.083.14.1`.

Catalog availability is not evidence of project stock, price, factory, batch, approval or installed performance.

## System chain

`fixture / floor drain → horizontal branch → branch/fitting interface → DN100 stack → expansion control → cleaning access → venting path → floor penetration/firestop interface → building drain`

Parallel requirements: slope continuity, support/fixed/sliding-point logic, structural acoustic decoupling, maintenance access, later alteration control and G9 feedback.

## Inference: thermal movement

Use `ΔL = α × L × ΔT` with published `α = 0.17 mm/(m·K)`.

For a 6 m exercise segment:

- ΔT 20 K → ΔL = 20.4 mm;
- ΔT 40 K → ΔL = 40.8 mm.

These are calculations, not field measurements.

## Simulation mode

All geometry, drainage loading, slopes, offsets, noise proxies and QC observations are `SIMULATED / EXERCISE ASSUMPTION`.

### NOMINAL

6 m stack segment, installation at 20°C, ΔT 20 K, continuous branch fall, accessible cleaning point, fixed/sliding supports separated as intended.

Result: `SIMULATED PASS UNDER ASSUMPTIONS`.

### ADVERSE

ΔT 40 K, 25 mm local alignment error, one over-tight support, one branch segment approaching zero fall.

Result: `SIM-REWORK`: 40.8 mm movement proxy; rigid support may convert movement into stress/structure-borne sound; flat segment becomes a deposition-sensitive point.

### FAILURE-SEEKING

Expansion socket rigidly locked; cleaning access hidden behind cabinetry; branch reverse-fall; floor penetration rigidly contacts structure; later branch added without hydraulic/vent review.

Result: `SIM-FAIL` through combined blockage, maintenance, thermal-stress, acoustic-bridge and venting risks.

## Simulated QC set

Eight virtual checkpoints Q01–Q08. Deliberate defects:

- Q03: local reverse fall;
- Q06: inadequate cleaning-access clearance;
- Q08: rigid acoustic bridge at floor penetration.

Result: 5 SIM-PASS + 3 SIM-REWORK. This is not a construction pass rate.

## FMEA / Hold Points

1. Reverse fall / low point → deposition and backup. Check every branch before enclosure.
2. Wrong expansion/fixed-point logic → axial stress/interface movement. Record installation temperature, insertion depth and support role.
3. Inaccessible cleaning fitting → maintenance failure. Verify service envelope before cabinetry/ceiling closure.
4. Inadequate venting → trap-seal loss, odor and unstable drainage. Close through applicable code/system calculation.
5. Rigid supports or penetrations → structure-borne sound. A low-noise pipe cannot compensate for an acoustic bridge.
6. Fire penetration without applicable system approval → life-safety HOLD. Manufacturer product information is not project firestop approval.
7. Later alterations without review → capacity, venting, slope and maintenance chain may fail. Record in G9.

## RFQ gate

Request project quotations/evidence for `310.012.14.1`, `310.334.14.1`, `310.003.14.3`, DN100/d110 pipe and required branches/bends. Require China supplier, pack quantity, dated tax-inclusive engineering price, lead time, manufacturing site/batch traceability, TDS/EPD, acoustic report construction applicability and applicable domestic fire-penetration evidence.

Price status: `D / RFQ REQUIRED`. Do not substitute retail marketplace pricing.

## Future real validation

Before enclosure: slope, alignment, supports, fixed/sliding points, expansion insertion, cleaning access, vent continuity and penetration/firestop photo record.

Future field evidence may include drainage observation, appropriate ball/flow tests, leak inspection, trap-seal observation and acoustic measurements with room/background/operating condition/instrument recorded.

## G9

Capture blockage/backflow, cleaning location/frequency, odor/trap-seal complaints, acoustic complaints, interface repairs, expansion/support abnormalities, later alterations, firestop maintenance, service time and access quality.

## Status ceiling

Highest permitted status without field evidence: `DESIGN-READY FOR FUTURE TEST`.
