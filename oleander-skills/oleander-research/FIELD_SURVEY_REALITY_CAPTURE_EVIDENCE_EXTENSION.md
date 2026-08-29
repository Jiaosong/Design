# Field Survey / Reality Capture Evidence Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-research`

Use when a project needs field-derived spatial evidence from photographs, video, manual measurements, GNSS, total station, level, laser scan, lidar, Structure-from-Motion photogrammetry, control points, checkpoints, orthophotos, point clouds or related capture systems, and when the design consequence depends on what the capture can actually prove.

This extension governs **field evidence authority**, not software operation. It does not turn OLEANDER into a licensed survey practice and does not allow a point cloud, mesh, orthophoto or GNSS readout to self-certify positional truth.

## Existing-owner boundary

Use with, not instead of:
- `oleander-research/SKILL.md` for source authority, evidence/inference/unknown separation and research traceability;
- `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md` when quantitative uncertainty materially affects the decision;
- `oleander-data-viz` for geographic/error/coverage visualization, never for creating measurement authority;
- `oleander-3d-pipeline/REALITY_CAPTURE_DERIVED_GEOMETRY_HANDOFF_EXTENSION.md` when field evidence becomes point-cloud/mesh/orthophoto/CAD geometry;
- `oleander-technical-drawing` only after field-corrected geometry has an explicit authority state;
- licensed survey/geodesy/engineering authority where project, jurisdiction or contract requires it.

## Core contract

`SURVEY / FIELD QUESTION → REQUIRED CLAIM + DECISION CONSEQUENCE → REQUIRED POSITION / SCALE / SHAPE / CONDITION AUTHORITY → REFERENCE FRAME / DATUM / CRS / VERTICAL REFERENCE / EPOCH WHEN MATERIAL → CONTROL / SCALE / CHECK STRATEGY → CAPTURE PLAN + COVERAGE → RAW OBSERVATIONS + METADATA → CONTROLLED SOLUTION / REGISTRATION → INDEPENDENT CHECK OR BOUNDED INTERNAL QUALITY → ERROR / UNCERTAINTY + COVERAGE LIMITS → FIELD CLAIM → DESIGN CONSEQUENCE / HOLD`

## Evidence classes

Keep at least these classes distinct:

1. **Observed field evidence** — a directly recorded condition, object, relation or event whose provenance and context are preserved.
2. **Measured field evidence** — a value or coordinate tied to a defined measurand, method, unit/reference, calibration/traceability state and uncertainty appropriate to the claim.
3. **Controlled spatial reconstruction** — a photogrammetric/scan solution tied to explicit scale/control/reference information and evaluated against suitable checks.
4. **Relative reconstruction** — internally coherent shape/relationship evidence without sufficient absolute scale/coordinate authority.
5. **Derived spatial inference** — geometry or condition inferred from the capture but not directly observed/measured at the claimed authority.
6. **Unknown / uncovered** — occluded, unobserved, weakly textured, moving, reflective, vegetated, underwater, temporally changed or otherwise insufficiently supported regions.

`VISUALLY PLAUSIBLE RECONSTRUCTION ≠ MEASURED FIELD TRUTH`.

## Survey-question gate

Before capture, state what the field work must answer. Examples:
- relative geometry only;
- absolute dimension / scale;
- plan position;
- elevation / vertical relation;
- slope/profile;
- deformation/change over time;
- surface/edge/clearance relation;
- contextual visual evidence;
- asset inventory/location;
- design fit-check;
- legal/property/boundary or construction-control question.

The last class and other regulated tasks may require licensed/contractual survey authority. OLEANDER must preserve that HOLD rather than substituting photogrammetry or consumer GNSS.

## Coordinate / reference authority

When position or elevation matters, record as applicable:
- coordinate reference system / projection;
- geodetic datum or reference frame;
- realization / epoch when material;
- horizontal and vertical reference separately where applicable;
- units;
- geoid/ellipsoid/height interpretation when material;
- local site coordinate origin/axes if used;
- transformation from source control to project coordinates;
- control monument / benchmark identity and source authority;
- expected coordinate accuracy relative to the decision.

An `EPSG` identifier alone may be insufficient when epoch, realization, vertical reference or local transformation affects the result.

`WGS84 / GPS COORDINATES EXIST ≠ PROJECT COORDINATE AUTHORITY`.

## Control / scale / checkpoint separation

Do not collapse these roles:

- **Control** participates in constraining the solution/reference frame.
- **Scale evidence** establishes or checks metric scale where the reconstruction would otherwise be scale-ambiguous.
- **Checkpoint / independent check** is withheld from the solution where independent accuracy assessment is required.
- **Tie points / image matches / scan correspondences** support internal registration but are not independent ground truth.

A point used to fit the solution cannot simultaneously be treated as fully independent evidence of the same fit without explicit methodology justifying the claim.

`CONTROL RESIDUAL ≠ INDEPENDENT POSITIONAL ACCURACY`.

## Capture-plan rules

Record before or during capture:
- capture date/time and temporal relevance;
- operator / device / sensor identity;
- calibration state or known limitations when material;
- image/video/scan settings that can affect geometry or evidence;
- station/camera trajectory and coverage intent;
- control/check/scale locations and identifiers;
- environmental conditions that can change evidence;
- expected occlusion / texture / reflectance / motion / vegetation / water limitations;
- repeat/overlap strategy selected for the actual scene and required result;
- safety/access constraints;
- raw-file identity and preservation path.

Do not install one universal overlap percentage, GCP count, camera angle, altitude, scan spacing or acquisition pattern. Coverage must be chosen from scene geometry, sensor, risk and required claim.

## Error / uncertainty rules

1. **All measurements and reconstructions have error.** Record what error metric means before using it as a quality claim.
2. **Precision ≠ accuracy.** Tight internal repeatability or low registration residual does not establish external positional correctness.
3. **Local residual ≠ global truth.** Report where the solution was checked and which regions remain weak or extrapolated.
4. **Internal quality ≠ independent accuracy.** Reprojection error, bundle-adjustment residual, ICP residual, cloud-to-cloud distance or fit residual may diagnose the solution but do not automatically replace independent control/check evidence.
5. **Checkpoints must be fit for the claim.** Their source should be sufficiently independent and more authoritative for the quantity being tested when an external accuracy claim is made.
6. **Blunders are investigated, not silently deleted.** Preserve cause/disposition in metadata.
7. **Coverage limits stay attached.** Unseen or weakly constrained regions cannot inherit the accuracy of well-observed regions by proximity.
8. **Temporal mismatch is an error source.** A geometrically accurate capture may still be stale relative to Current field condition.

Route material quantitative interpretation to Measurement Uncertainty when the decision turns on the uncertainty budget or decision rule.

## Required field evidence ledger

For every material field-derived claim, persist:
- `field_question_and_decision_consequence`;
- `claim_type_position_scale_shape_condition`;
- `capture_date_time_relevance`;
- `raw_observation_ids`;
- `sensor_device_operator_method`;
- `units_reference_frame_datum_crs_vertical_epoch`;
- `control_scale_checkpoint_strategy`;
- `capture_coverage_and_occlusion`;
- `solution_registration_method`;
- `internal_quality_metrics_and_meaning`;
- `independent_check_evidence_when_required`;
- `error_uncertainty_and_spatial_distribution`;
- `temporal_environmental_limits`;
- `field_claim_state`;
- `design_consequence`;
- `licensed_survey_or_professional_hold`.

## Claim ceilings

Typical ceilings:
- photographs without scale/control → visual/relational observation only;
- relative SfM/scan reconstruction → relative shape/topology/coverage evidence only;
- reconstruction with governed scale but no external coordinate control → metric local geometry may be bounded, absolute position remains open;
- controlled reconstruction with independent checks → positional/shape claims bounded to the reference, check method, spatial distribution and uncertainty actually demonstrated;
- consumer GNSS/embedded geotags → contextual location unless verified fit for the project claim;
- authoritative licensed survey/control → use according to its stated datum, scope, date, accuracy and contractual authority.

## Failure attacks

Reject or revise when:
- a dense or attractive point cloud is called accurate because it looks right;
- an orthophoto or mesh is called `FIELD MEASURED` with no scale/control/check lineage;
- GCP/control residual is reported as independent checkpoint accuracy;
- best-fit/ICP registration is used to erase a datum or scale disagreement;
- one tape dimension is used to imply global 3D accuracy without an adequate spatial model;
- coordinate systems are mixed without transformation lineage;
- horizontal/vertical references are conflated;
- WGS84/consumer GPS is accepted as the design datum by default;
- RMSE or another statistic is quoted without the tested population, reference and spatial distribution;
- outliers/blunders are deleted without investigation;
- occluded or low-confidence geometry is filled and presented as observed field truth;
- cleaned/processed products replace raw observations and metadata;
- an old capture is treated as Current field condition without temporal review;
- photogrammetry is used to bypass a licensed/legal survey requirement;
- a software-specific recipe or fixed GCP/overlap/RMSE threshold becomes universal OLEANDER truth.

## Source / transfer boundary

Professional sources studied:
- U.S. Geological Survey, *Creating 3D point clouds, digital elevation models, and orthomosaics from historical aerial imagery through structure from motion aided photogrammetry* — official technical manual; retained principles: measurements have error, scale/control/tie measurements need explicit uncertainty, adjustment/residual interpretation matters, and processing parameters are context-dependent.
- ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 Version 2 (2024) — professional consensus reference; retained principles: project-specific positional accuracy requirements, independent higher-accuracy checks when testing is claimed, metadata/reporting, and explicit distinction between tested and produced-to-meet claims.
- NOAA National Geodetic Survey datum/reference-frame guidance — official reference for datum/reference-frame/vertical-reference authority.

External Skill search result:
- no high-quality, rights-clear survey/photogrammetry/reality-capture Skill was found with a Material Delta stronger than the official sources during the 2026-08-29 scan;
- README/agent-list/aggregation hits were rejected as source authority;
- no external Skill is installed merely to satisfy a search quota.

Rejected as universal:
- one Metashape/RealityCapture/CloudCompare pipeline;
- fixed overlap, GCP/checkpoint count, RMSE or reprojection threshold;
- a single datum/EPSG for all projects;
- software defaults as accuracy criteria;
- legal/engineering survey substitution.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / OFFICIAL-SOURCE-DIGESTED / EXTERNAL-SKILL-NO-DELTA-RECORDED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.