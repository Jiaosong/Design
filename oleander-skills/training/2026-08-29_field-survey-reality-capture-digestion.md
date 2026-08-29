# 2026-08-29 — Field Survey / Reality Capture / Photogrammetry Digestion

Status: `SOURCE DIGESTION / CANDIDATE EXTENSIONS / NO CURRENT L5 PROMOTION`

## Gap

Source map object: `GAP-FIELD-01 — Field Survey / Reality Capture / Photogrammetry`.

Residual problem after Current-first comparison:
- OLEANDER Research already owns evidence/source/unknown truth states but did not yet provide a unified field spatial-evidence contract for control/scale/reference/check/coverage/error;
- OLEANDER 3D Pipeline already owns units/axes/exchange/source-derivative integrity but did not yet preserve survey/photogrammetry coordinate authority through point-cloud/mesh/orthophoto→CAD handoff;
- Data Viz can visualize geographic evidence but must not create field measurement authority;
- Technical Drawing can consume governed field-corrected geometry but must not own capture/control.

## External Skill search

Search surfaces included:
- `K-Dense-AI/scientific-agents` recursive tree and code search for geospatial / remote sensing / survey / photogrammetry;
- `wonsukchoi/domain-experts` recursive tree and code search for surveyor / surveying / geospatial / cartographer / photogrammetry;
- broader GitHub code search for `photogrammetry SKILL.md reality capture point cloud survey`.

Result:
`NO HIGH-QUALITY RIGHTS-CLEAR EXTERNAL SKILL WITH MATERIAL DELTA FOUND`.

The broad search mostly returned README/agent-list/aggregation references rather than a specialist Skill with field-control, geodetic-reference and accuracy semantics strong enough to outrank professional primary sources.

Governance consequence:
- do **not** install a generic agent or software recipe merely to satisfy `find Skill`;
- official professional sources carry this batch;
- record the no-delta search so automation does not repeatedly rediscover the same weak sources.

## Professional source set

### 1. U.S. Geological Survey
Source: *Creating 3D point clouds, digital elevation models, and orthomosaics from historical aerial imagery through structure from motion aided photogrammetry* (USGS Techniques and Methods 11-C11; accessed 2026-08-29).

Accepted bounded mechanisms:
- every measurement carries error;
- tie points, control points, scale measurements and other observations participate differently in adjustment;
- error estimates and adjustment residuals must be interpreted rather than treated as decorative software scores;
- scale/control/capture metadata materially affect what the reconstruction can prove;
- processing/tuning values are contextual, not universal design rules.

Rejected from universalization:
- Metashape-specific preference/tweak values;
- example RMSE/tie-point tuning ranges;
- one image-processing sequence;
- historical-aerial workflow as universal capture workflow.

### 2. ASPRS
Source: *Positional Accuracy Standards for Digital Geospatial Data*, Edition 2 Version 2 (2024), plus official ASPRS standards page.

Accepted bounded mechanisms:
- accuracy requirement is project/specification dependent;
- an external tested positional-accuracy claim requires comparison with suitable independent higher-accuracy reference/check evidence;
- ground control and independent checkpoint roles must not be conflated;
- accuracy metadata/reporting must name the reference, test and achieved result;
- blunders/outliers require investigation, not silent deletion;
- `tested to meet` and process-based `produced to meet` are materially different evidence statements.

Rejected from universalization:
- one fixed RMSE accuracy class;
- one checkpoint count/distribution;
- one statistical threshold/confidence statement;
- one project specification;
- one national/jurisdictional implementation as global OLEANDER truth.

### 3. NOAA National Geodetic Survey
Source: NGS `Datums and Reference Frames` guidance.

Accepted bounded mechanisms:
- datum/reference frame is part of positional authority, not cosmetic metadata;
- horizontal/geometric and vertical references can be distinct;
- WGS 84, ITRF, NAD83 and other frames are not interchangeable names;
- datum/reference-frame realization and epoch can matter where coordinate change over time matters;
- a project/local coordinate transform must preserve its relation to upstream reference authority.

Rejected from universalization:
- U.S. federal datums as universal project defaults;
- WGS84 as an adequate universal design CRS;
- one epoch/reference-frame policy for all project types.

## Material Delta A — Research owner

File: `oleander-skills/oleander-research/FIELD_SURVEY_REALITY_CAPTURE_EVIDENCE_EXTENSION.md`

New contract:
`SURVEY / FIELD QUESTION → REQUIRED CLAIM + DECISION CONSEQUENCE → REQUIRED POSITION / SCALE / SHAPE / CONDITION AUTHORITY → REFERENCE FRAME / DATUM / CRS / VERTICAL / EPOCH → CONTROL / SCALE / CHECK STRATEGY → CAPTURE PLAN + COVERAGE → RAW OBSERVATIONS + METADATA → CONTROLLED SOLUTION / REGISTRATION → INDEPENDENT CHECK OR BOUNDED INTERNAL QUALITY → ERROR / UNCERTAINTY + COVERAGE LIMITS → FIELD CLAIM → DESIGN CONSEQUENCE / HOLD`.

Key retained separations:
- `VISUALLY PLAUSIBLE RECONSTRUCTION ≠ MEASURED FIELD TRUTH`;
- `CONTROL RESIDUAL ≠ INDEPENDENT POSITIONAL ACCURACY`;
- `WGS84 / GPS COORDINATES EXIST ≠ PROJECT COORDINATE AUTHORITY`;
- observed / measured / controlled reconstruction / relative reconstruction / derived inference / unknown remain separate evidence states.

## Material Delta B — 3D Pipeline owner

File: `oleander-skills/oleander-3d-pipeline/REALITY_CAPTURE_DERIVED_GEOMETRY_HANDOFF_EXTENSION.md`

New contract:
`FIELD EVIDENCE AUTHORITY → RAW CAPTURE / CONTROL ID → SOURCE CRS / DATUM / VERTICAL / EPOCH + UNITS → RECONSTRUCTION / REGISTRATION → TRANSFORM LINEAGE → POINT CLOUD / MESH / ORTHO / SURFACE → CLEAN / FILTER / CROP / DECIMATE / REPAIR LOG → DERIVED DESIGN GEOMETRY → TARGET TOOL REOPEN → SOURCE↔DERIVATIVE CHECK → UNKNOWN REGIONS → CLAIM CEILING`.

Key retained separations:
- `POINT CLOUD DENSITY ≠ DIMENSION AUTHORITY`;
- `BEST-FIT ALIGNMENT ≠ FIELD DATUM`;
- `IMPORT SUCCESS ≠ GEOMETRY FIDELITY PASS`;
- cleaned/fitted/filled geometry remains a derivative and does not overwrite source evidence.

## Owner boundary

`oleander-research`
→ owns field evidence authority, control/check/reference/coverage/error and claim ceiling.

`oleander-3d-pipeline`
→ owns derivative geometry lineage, transforms, cleanup/extraction semantics and exchange/reopen integrity.

`oleander-data-viz`
→ may visualize coverage, error distribution, checkpoints and geographic relations but cannot establish measurement authority.

`oleander-technical-drawing`
→ may consume controlled field-derived geometry; drawing validity is not survey validity.

External survey/geodesy/engineering authority
→ retains any legal, cadastral, construction-control, safety, certification or professional signoff the project requires.

## Anti-import firewall

Do not promote as OLEANDER defaults:
- fixed GCP/control/checkpoint count;
- fixed image overlap percentage;
- fixed reprojection/RMSE/ICP/cloud-to-cloud threshold;
- fixed camera altitude/angle/path;
- one GNSS accuracy assumption;
- one CRS/EPSG/datum;
- WGS84 as universal design coordinates;
- one photogrammetry/scan application;
- one denoise/decimation/mesh recipe;
- consumer geotag/GNSS as authoritative survey;
- point-cloud/mesh/orthophoto existence as FIELD MEASURED;
- licensed/legal survey replacement.

## Adversarial evals

Prepared local specs:
- `SK-RES-006` — attacks attractive SfM reconstruction with weak control/check/reference/metadata and false field-measured promotion;
- `SK-3D-006` — attacks cleaned/best-fit/decimated cloud-to-CAD handoff that loses CRS/transform/source authority.

Central Golden boundary:
- current `evals/scripts/validate_evals.py` loads `evals/golden/skills.jsonl` directly;
- unless the central JSONL is updated by a no-loss controlled edit, these local specs remain `CENTRAL_GOLDEN_INTEGRATION_OPEN`;
- their existence must not be described as CI execution.

## Maturity

`DOCUMENTED CANDIDATE EXTENSIONS / OFFICIAL-SOURCE-DIGESTED / EXTERNAL-SKILL-NO-DELTA-RECORDED / NO PRACTICE / NO CROSS-CONTEXT / NO PROJECT USAGE / NO PROMOTION`.

Next maturity action after governance merge: a controlled reality-capture practice with at least one known reference/control relation, one independent or explicitly bounded check, one occluded/low-confidence region, and one source→cleaned derivative→target-tool reopen sequence.