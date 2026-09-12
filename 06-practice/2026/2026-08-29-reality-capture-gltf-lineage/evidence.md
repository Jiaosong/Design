# OLEANDER VALIDATION Practice — Reality Capture → glTF Lineage

Status: `TRAINING_MODE / PRACTICE_EVIDENCE / SUPPORT ONLY / NO PROMOTION`

## GAP
`REALITY_CAPTURE_DERIVED_GEOMETRY_HANDOFF_EXTENSION.md` is now on `main` but explicitly has no Practice / cross-context / project usage evidence. The bounded gap tested here is whether a local-origin glTF handoff can preserve metric geometry while losing the reversible relation to the source field/project coordinate frame.

## EXISTING-FIRST
Owner: `oleander-3d-pipeline`.
Candidate extension: `oleander-skills/oleander-3d-pipeline/REALITY_CAPTURE_DERIVED_GEOMETRY_HANDOFF_EXTENSION.md`.

Strong current external sources checked:
- Khronos glTF Registry: current glTF version 2.0 / specification patch 2.0.1; glTF uses a right-handed coordinate system and metres for linear distances.
- NOAA NGS Datums and Reference Frames: a datum/reference frame provides the coordinate reference for known locations; frame/datum identity is not equivalent to mere numeric coordinates.
- ASPRS Positional Accuracy Standards: current standards surface lists Edition 2 / current modular positional-accuracy guidance; this Practice does not claim ASPRS conformance.

## TEST
Synthetic exercise source only; **not field truth**:
- Exercise CRS: EPSG:32648 (`WGS 84 / UTM zone 48N`), validated through pyproj.
- Source origin: E=500000 m, N=1500000 m, H=100 m.
- Four source points define a small bounded surface.
- Rebase / axis mapping to glTF:
  - `glTF X = E - E0`
  - `glTF Y = H - H0`
  - `glTF Z = -(N - N0)`
- A: glTF geometry only.
- B: byte-identical glTF geometry plus an independent lineage sidecar carrying source CRS, source origin, axis mapping, inverse mapping, IDs and claim ceiling.

Runtime:
- trimesh `4.11.1`
- pyproj `3.7.2`

## READBACK
Both glTF files reopen in trimesh with:
- vertex count = 4
- bounds = `[[0,0,-5],[10,2,0]]` metres
- known 10 m edge reopens as exactly 10.0 m

A contains no CRS or source-origin metadata and therefore cannot reconstruct the source absolute frame from the artifact alone.

B + sidecar reconstructs the exercise source coordinates with `max_abs_error_m = 0.0`.

## PROVEN
`METRIC GEOMETRY REOPEN PASS ≠ SOURCE COORDINATE AUTHORITY PASS`.

For this bounded glTF/local-origin fixture:
1. local metric geometry and scale survive target-tool reopen;
2. absolute source/project coordinate relation is not recoverable from the geometry-only glTF;
3. an explicit reversible lineage sidecar is sufficient to reconstruct the exercise source frame exactly.

## NOT PROVEN / HOLD
This does **not** prove:
- field measurement accuracy;
- survey control;
- ASPRS conformance;
- licensed survey signoff;
- datum/epoch correctness for any real project;
- glTF as a geospatial authority format;
- every consumer preserving application-specific metadata;
- any project geometry or C04 field truth.

The EPSG code, origin and geometry are `EXERCISE ASSUMPTION / DESIGN TEST` only.

## TRANSFER RULE
For reality-capture → local-origin 3D exchange, validate two different things:
`LOCAL GEOMETRY / UNIT / AXIS REOPEN`
and
`REVERSIBLE SOURCE-FRAME LINEAGE`.

If the second is absent, keep the derivative below field/survey coordinate authority even when the model looks aligned and known local distances pass.

## MATURITY
`PRACTICE_EVIDENCE`
