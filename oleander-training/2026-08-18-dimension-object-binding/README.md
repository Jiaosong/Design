# OLEANDER Training — Dimension-to-Object Binding

## Trigger

C04 Mountain Fluid Rest v1.4 was explicitly rejected because dimensions were not sufficiently attached to the model read. The values existed, but their measured intervals were not visually unambiguous. v1.5 repaired this by annotating 5400 / 740 / 445 / 455+740 mm directly against the model.

This training reuses that failure as a general 3D/presentation skill gap rather than inventing a parallel framework.

## Existing Skill reused

`oleander-3d-pipeline` already owns units, scale, camera, axonometric output, model handoff and derived-view discipline. The missing gate was visual dimension binding: a correct numeric register could still leave the object interval ambiguous.

## External calibration

ISO 129-1:2018 establishes general principles for presentation of dimensions and associated tolerances for 2D drawings and notes that the principles can also be applied to 3D applications. This training uses it only as a presentation reference; it does not claim full ISO compliance, tolerance validity, construction validity, accessibility compliance or engineering approval.

## Real practice

Training values are current C04 scale-test values only:

- overall: `5400 mm`
- SIT: `445 mm`
- LEAN: `740 mm`
- HALF-RECLINE: `455 mm hip + 740 mm back rise`

These are reused as a calibration object; they are not field/site measurements.

### v1 — REJECT

Detached dimension register. Values are readable, but the reviewer must mentally map each number back to the model. `VALUE PRESENT != OBJECT INTERVAL LEGIBLE`.

### v2 — REVISE

Dimensions are attached with extension lines/leaders, but the vertical stack competes with the human silhouette and makes the main object read more like a technical sheet.

### v3 — KEEP FOR TRAINING

- overall dimension remains directly attached to the full object span;
- SIT and LEAN critical heights stay on-object with short numeric labels;
- recline relation uses an explicit leader tied to the back-rest;
- repeated semantic descriptions move to a compact secondary scale-test rail;
- source/truth boundary remains adjacent;
- the model and human-scale silhouette return to first-read.

## Candidate rule

`SOURCE VALUE → MEASURED OBJECT / INTERVAL → ATTACHMENT CARRIER → FIRST-READ MODEL → NEAR-READ DIMENSION → TRUTH BOUNDARY`

## Failure knowledge

- a dimension table is not a substitute for visual attachment;
- adding every dimension directly to the object can also fail when annotation buries the model;
- critical dimensions and secondary parameter rails need different visual rights;
- model-scale/scenario values must not acquire field or engineering authority simply because they are dimensioned on a polished sheet;
- full-size export success is not enough: first-read and near-read must be reviewed separately.

## Cross-project transfer

Applicable to product models, furniture/ergonomic studies, architectural/landscape axons, exploded views, node assemblies, equipment layouts and any 3D presentation where dimensions are used to prove scale or relation.

Not a substitute for CAD/GD&T/engineering dimensioning, survey/field measurement, accessibility standards, fabrication tolerances or construction documentation.

## State

`KEEP FOR TRAINING / MATERIAL DELTA VALID / PROJECT DESIGN PROMOTION NOT CLAIMED`
