# Reality Capture → Derived Geometry Handoff Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-3d-pipeline`

Use when field observations or controlled reality capture are converted into point clouds, meshes, orthophotos, DEM/DSM surfaces, sections, CAD references or other editable/derived spatial geometry that will influence design.

This extension governs **source→derivative geometry lineage and transfer integrity**. It does not create field measurement authority; upstream field evidence authority remains with `oleander-research/FIELD_SURVEY_REALITY_CAPTURE_EVIDENCE_EXTENSION.md` and any required licensed survey/professional owner.

## Core contract

`FIELD EVIDENCE AUTHORITY → RAW CAPTURE / CONTROL ID → SOURCE CRS / DATUM / VERTICAL REFERENCE / EPOCH + UNITS → RECONSTRUCTION / REGISTRATION SOLUTION → EXPLICIT TRANSFORM LINEAGE → POINT CLOUD / MESH / ORTHO / SURFACE → CLEAN / FILTER / CROP / DECIMATE / REPAIR LOG → DERIVED DESIGN GEOMETRY → TARGET TOOL IMPORT / REOPEN → SOURCE↔DERIVATIVE CHECK → CONFIDENCE / UNKNOWN REGIONS → CLAIM CEILING → DESIGN / DRAWING HANDOFF`

## Source authority classes

Do not let downstream geometry erase the upstream evidence class. Tag each imported reality-capture object as one of:
- `FIELD_CONTROLLED` — tied to governed field reference/control with an explicit claim ceiling;
- `METRIC_LOCAL` — scale is bounded but absolute site coordinates remain open;
- `RELATIVE_RECONSTRUCTION` — internal geometry only; scale/position not authoritative;
- `VISUAL_CONTEXT` — useful as image/context/reference, not dimension authority;
- `DERIVED_INFERENCE` — generated/interpolated/filled geometry that is not directly observed;
- `UNKNOWN / LOW-CONFIDENCE` — unsupported or materially ambiguous regions.

`POINT CLOUD DENSITY ≠ DIMENSION AUTHORITY`.

## Coordinate and transform handoff

Before any field-derived asset becomes a design reference, record as applicable:
- source coordinate system/projection;
- datum/reference frame and realization/epoch where material;
- horizontal and vertical reference;
- source units;
- local project origin/axes;
- translation/rotation/scale transform;
- geoid/ellipsoid/height conversion when material;
- any best-fit/ICP/manual registration step;
- target application units/axes/origin;
- transform order and reversible parameters;
- source and target object IDs/revisions.

A visually aligned import is not enough. If target-tool coordinates are intentionally simplified for numerical stability or modeling convenience, retain the reversible relation to the authoritative field frame.

`BEST-FIT ALIGNMENT ≠ FIELD DATUM`.

## Derivative lineage rules

Every material derived object must keep a lineage such as:

`RAW CAPTURE → RECONSTRUCTION VERSION → CONTROL / CHECK SET → DENSE CLOUD → CLEAN CLOUD → MESH / ORTHO / SURFACE → DESIGN REFERENCE → CAD / DRAWING DERIVATIVE`.

For each processing step record:
- source object/version;
- operation/tool/version when material;
- parameters only where they materially affect geometry/evidence;
- removed/filled/interpolated regions;
- scale/coordinate changes;
- output object ID;
- known loss of fidelity or evidence;
- whether the operation is reversible.

Do not promote a derivative to source authority merely because it is easier to edit.

## Cleaning / filtering / decimation

Reality-capture cleanup can alter design evidence. Treat these as evidence-changing operations when material:
- isolated-point removal;
- statistical denoising;
- smoothing;
- hole filling;
- surface reconstruction;
- remeshing;
- decimation;
- crop/mask;
- vegetation/object removal;
- plane fitting;
- best-fit primitive replacement;
- manual sculpt/retopo;
- texture or orthophoto seam repair.

Rules:
1. Preserve the unmodified reconstruction or reproducible source state.
2. Mark interpolated or manually repaired geometry as derived.
3. Do not smooth away a feature that may carry dimensional/design significance.
4. Do not fill occlusion and present the fill as observed.
5. Keep a path back to the source region used for a critical dimension/section.
6. If decimation materially shifts edges/surfaces, the reduced mesh cannot carry the original precision claim.

## Point cloud / mesh / orthophoto semantics

### Point cloud
May carry sampled 3D observations/reconstruction, but quality varies spatially. Do not assume every point shares one uniform uncertainty.

### Mesh / surface
Adds interpolation/topology assumptions. A watertight or smooth mesh can look more complete than the evidence. Filled holes and bridged gaps must remain identifiable.

### Orthophoto / orthomosaic
A rasterized positional derivative whose geometry depends on camera solution, surface model and projection. Do not use pixel sharpness as positional accuracy evidence.

### DEM / DSM / height surface
Must retain horizontal/vertical reference, cell/resolution meaning, interpolation/surface class and known vegetation/object behavior.

### CAD extraction
Planes, edges, cylinders, centerlines, sections and simplified solids are **model interpretations** of the captured evidence. Bind each critical extracted feature to the source region and extraction method; do not silently convert fitted geometry into field-measured truth.

## Design geometry extraction

When converting capture to design geometry, classify each object/dimension:
- direct controlled feature;
- fitted feature with residual/uncertainty;
- bounded estimate;
- inferred/occluded feature;
- intentionally idealized design reference.

For critical geometry record:
`FEATURE ID → SOURCE REGION / CONTROL → EXTRACTION / FIT METHOD → RESIDUAL / UNCERTAINTY STATE → DESIGN USE → REOPEN TRIGGER`.

A plane fit, cylinder fit or section trace may be appropriate design evidence while still remaining below survey/construction authority.

## Cross-tool exchange

For each material handoff:
1. establish source units/axes/origin/CRS state;
2. choose an exchange format that preserves the needed relation;
3. export a bounded test object or known control relation when practical;
4. reopen in the target tool;
5. verify scale, orientation, origin and one or more known distances/coordinates appropriate to the claim;
6. compare source and target bounding/extents or controlled features;
7. record known losses such as CRS metadata, point attributes, normals, classifications, texture coordinates or precision;
8. retain the authoritative source/master separately.

`IMPORT SUCCESS ≠ GEOMETRY FIDELITY PASS`.

## Required output

- `upstream_field_authority_and_claim_ceiling`;
- `raw_capture_and_reconstruction_ids`;
- `source_crs_datum_vertical_epoch_units`;
- `control_checkpoint_reference`;
- `registration_transform_lineage`;
- `source_object_and_derivative_chain`;
- `clean_filter_crop_decimate_repair_log`;
- `unknown_occluded_inferred_region_map`;
- `extracted_feature_authority_states`;
- `target_tool_units_axes_origin`;
- `exchange_reopen_test`;
- `source_derivative_deviation_check`;
- `known_losses`;
- `design_drawing_claim_ceiling`;
- `field_survey_professional_holds`.

## Failure attacks

Reject or revise when:
- a point cloud/mesh is imported into CAD and immediately becomes Current dimensional geometry;
- CRS or datum is lost but manual alignment is treated as equivalent authority;
- ICP/best-fit hides a systematic coordinate mismatch;
- one reference distance is used to authorize all geometry without spatial evidence;
- source units/target units are omitted;
- local origin rebasing destroys the reversible link to field coordinates;
- denoise/smoothing/decimation modifies a critical edge but no deviation check is run;
- holes are filled or vegetation removed without derivative labeling;
- a raster orthophoto becomes 3D elevation authority;
- fitted planes/cylinders/edges are described as directly measured without fit evidence;
- export/import success substitutes for scale/orientation/coordinate readback;
- the editable CAD derivative replaces raw capture/control/reconstruction provenance;
- target-tool convenience causes the project to abandon a stronger existing survey/control source;
- software-specific cleanup recipes or numerical thresholds become universal OLEANDER rules.

## Source / transfer boundary

Upstream evidence authority:
- `oleander-research/FIELD_SURVEY_REALITY_CAPTURE_EVIDENCE_EXTENSION.md`.

Professional references informing this bounded extension:
- USGS SfM technical manual — source/control/scale/error/processing lineage and context-specific processing evidence;
- ASPRS positional-accuracy standards — independent check and metadata/reporting semantics;
- NOAA NGS datum/reference-frame guidance — coordinate reference authority.

External Skill scan:
- no rights-clear photogrammetry/reality-capture Skill with stronger Material Delta was found in the 2026-08-29 scan;
- no tool-specific RealityCapture/Metashape/CloudCompare house workflow is installed as a Skill.

Rejected as universal:
- fixed cleaning/decimation tolerance;
- fixed ICP threshold;
- one point-cloud file format;
- one mesh reconstruction algorithm;
- one local-origin strategy;
- one CRS/datum;
- one CAD extraction recipe;
- software output as field/survey signoff.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / OFFICIAL-SOURCE-DIGESTED / EXTERNAL-SKILL-NO-DELTA-RECORDED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.