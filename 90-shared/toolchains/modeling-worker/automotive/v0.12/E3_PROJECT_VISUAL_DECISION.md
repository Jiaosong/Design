# Modeling Worker v0.12｜E3 Automotive Application Project / Visual Decision

Status: `E3 MACHINE PASS / VISUAL REVISE / PROJECT REVISE / ROOT CAUSE = ARCHITECTURE / PAP BLOCKED / PROMOTION BLOCKED`

## Control Plane state

This is the first live application of merged `OLEANDER Project Control Plane v0.3` to an active system candidate.

Control Card object: `SYS-MODELING-WORKER-v0.12-E3-AUTO`  
Authority state entering review: `WORKING_SOURCE`  
Mode: `CANDIDATE`  
Decision Question: can v0.12 consume an Automotive application with independently controllable hood, cabin, shoulder, rear-haunch, lower-body and termination volumes while preserving fairness **and** improving application-level proportion/form?

`Machine PASS != Design PASS` remains enforced.

## Immutable machine evidence

GitHub Actions run: `31665641314` / Modeling Worker v0.12 run #22  
Head SHA: `737c6e3485d2f9be77946ba222ddd7e6bb2ce40d`  
AI Governance Evals: run #510 — `SUCCESS`  
E3 artifact ID: `9167914831`  
Artifact digest: `sha256:b6bde5b84ad6243a8c9293218515f0172b45f90f21c90d3c7fda69b4fbcf9758`

Machine result:
`MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED`.

Machine checks retained as PASS:
- generic precision-aware v0.12 compiler consumed;
- base surface fairness passed existing thresholds;
- four semantic source edits changed exactly their declared source indices;
- all four derived variants retained the existing C2 / interior-fairness checks;
- editable Surface Source remained separate from derived execution geometry;
- front/rear terminations remained surface patches rather than mesh-closure caps;
- execution topology remained downstream of Surface Source compilation.

No generic C2 threshold was relaxed. Compiler-space second-derivative threshold remains `1e-6`; Blender runtime residual evidence remains a separate bounded representation class.

## Human Visual QA

### Hero — `REVISE`

The surface is continuous and technically clean enough for review, but first reading is still a single broad shell / central mound. Hood, cabin, shoulder and rear-haunch do not read as independently controlled low-frequency masses. The visible cage can be segmented semantically, but the evaluated shape does not express the intended application hierarchy strongly enough.

### Side — `REVISE`

The side silhouette remains close to a symmetric single-bubble profile. There is no sufficiently distinct hood-to-cowl event, cabin gesture, shoulder acceleration or rear-haunch buildup. The far front/rear boundaries curl upward and still read as open benchmark terminations rather than controlled application volumes.

### Top — `REVISE`

Plan reading remains broadly symmetric and capsule/rectangular. Front/rear distinction, shoulder-to-haunch hierarchy and termination mass are under-resolved. This is compatible with a continuity benchmark, but insufficient as evidence that an Automotive application Relationship Graph is controlling proportion/form.

### Zebra — `REVISE FOR APPLICATION`, seam continuity retained

Center and compiled seams remain continuous; no seam crease was observed. However, stripe compression / convergence remains strong at both far termination zones. This is consistent with the machine evidence and does not invalidate C2 seam execution, but it confirms that termination styling and application-level volume control remain open.

### Semantic-edit variants — `REVISE`

`VOL-HOOD`, `VOL-CABIN`, `VOL-SHOULDER` and `VOL-LOWER-BODY` edits are machine-isolated correctly, but their visible effects are too weak and too coupled to a single 4×4 center cage to demonstrate application-level independent volume control. The variants prove **source-edit compatibility**, not the Decision Question's stronger claim of independently controllable Automotive volume architecture.

## Project QA

Result: `REVISE`.

The benchmark answers only the first half of the Decision Question:

> explicit semantic source edits can be bounded while the existing generic C2/fairness compiler remains stable.

It does **not** yet answer the application-level half:

> independently controllable hood / cabin / shoulder / haunch / lower-body / termination volumes produce a convincing and intentionally differentiated Automotive proportion/form hierarchy.

Therefore E3 is not eligible for M4.5 application PASS, PAP, system Promotion review or Candidate→Canonical transition.

## Root-cause reclassification

`Relation → Architecture`.

Reason: the failure is not a small parameter error and should not be treated by increasing edit deltas. Seven declared semantic volume names are currently projected onto one sparse center cage plus two generic termination patches. The source architecture therefore does not provide enough independent low-frequency degrees of freedom for the intended Automotive volume hierarchy.

This is a Control Plane CB-02 case:

`Machine PASS + Visual/Project REVISE → retain machine receipt, do not upgrade design state, do not rerun at higher fidelity as a substitute.`

CB-01 is not triggered: this is the first E3 Project/Visual REVISE at the reclassified Architecture layer.

## Next allowed action

Rebuild only the E3 **application Surface Source architecture** so that the declared low-frequency volumes become genuinely independent source structures before they compile into derived execution geometry.

Minimum requirement for the next E3 revision:
- hood/cowl source must be independently adjustable from cabin crown;
- cabin source must move without simply lifting the same center dome;
- shoulder/rear-haunch source must have an independent longitudinal acceleration control;
- lower-body/rocker source must visibly counter or support shoulder mass;
- front/rear termination sources remain independent and retain existing C2/fairness evidence;
- fixed comparison views must make each semantic edit visually legible at first reading;
- no secondary wheel/detail/CMF work may be added to hide unresolved low-frequency architecture.

Existing E1/E2 PASS evidence remains valid and is not downgraded by this application-level REVISE.
