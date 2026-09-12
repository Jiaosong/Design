# OLEANDER 3D Reference Reproduction Fidelity Protocol v1

This protocol extends `oleander-3d-pipeline` for tasks whose explicit purpose is to reproduce an existing physical product or vehicle from reference evidence.

It exists because a model can pass dimensions, topology, persistence and render checks while still being the wrong form.

`Machine PASS ≠ Reference Fidelity PASS ≠ Design Quality PASS`

## R1 — Reference revision lock

### INPUT
- exact maker / product / variant / generation / model year or revision;
- dimensional source(s);
- visual reference source(s);
- explicit reference rights/source note.

### MUST CHECK
- all authoritative dimensions belong to the same frozen reference revision;
- visual references are identified by revision and variant when possible;
- a newer or older facelift may not be mixed silently;
- every conflicting source is listed and resolved before Fidelity PASS.

### FORBIDDEN
- generic family labels such as `Porsche 911 992` when the benchmark actually uses one facelift/year;
- dimensions from one revision and silhouette from another without explicit SUPPORT-only status;
- treating an image search result as dimensional authority.

### EVIDENCE
`REFERENCE_REVISION_LOCK.json`.

### FAIL
`FAIL_REFERENCE_REVISION_MIXED`.

---

## R2 — Multi-view evidence set

### MUST CHECK
Minimum visual set for a form-reproduction benchmark:
1. side profile / near-orthographic side;
2. front or front 3/4;
3. rear or rear 3/4;
4. top / elevated 3/4 or another view that constrains plan width;
5. close reference for identity-bearing lamps / greenhouse / wheel opening when those features matter.

Each reference record must declare `AUTHORITY / SUPPORT`, camera uncertainty, crop uncertainty and whether perspective distortion is expected.

### FAIL
`INSUFFICIENT_REFERENCE_VIEW_COVERAGE`.

---

## R3 — Calibrated hard points before surface work

Lock hard points before aesthetic surface fitting:
- total length / width / height;
- wheelbase;
- front/rear track when available;
- tyre/wheel OD when available;
- axle centres;
- ground plane;
- front/rear extremities.

A hard point may be `OFFICIAL`, `SOURCE_GROUNDED`, or `VISUAL_ESTIMATE`; never silently upgrade a visual estimate to official data.

### FAIL
`FAIL_HARD_POINT_CONTRACT`.

---

## R4 — Silhouette-first reconstruction

Before panel seams, wheel detail, CMF or beauty lighting, fit the primary silhouette in this order:
1. side top envelope;
2. wheel openings and axle relationship;
3. greenhouse/A-C pillar envelope;
4. plan half-width / front-rear shoulder distribution;
5. front and rear end-section envelopes;
6. primary lamp locations.

The candidate must expose these as sparse editable controls or another explicit Source representation.

### FORBIDDEN
- adding micro detail while the silhouette gate is failing;
- dense freehand vertex pushing with no landmark causality;
- using SubD to hide incorrect section placement.

### FAIL
`REVISE_PRIMARY_SILHOUETTE`.

---

## R5 — Landmark manifest and normalized error

Maintain a machine-readable landmark table. At minimum use stable semantic IDs such as:
- `FRONT_AXLE`, `REAR_AXLE`;
- `ROOF_APEX`;
- `A_PILLAR_BASE`, `C_PILLAR_BASE`;
- `FRONT_LAMP_CENTRE_L/R`;
- `REAR_LIGHTBAR_CENTRE`;
- `FRONT_ARCH_APEX`, `REAR_ARCH_APEX`;
- `FRONT_EXTREME`, `REAR_EXTREME`.

For image-derived landmarks, store normalized coordinates and camera/view ID. Use known hard points to calibrate scale where possible.

Default machine thresholds for a controlled reproduction benchmark:
- official hard-point relative error: `<= 0.25%`;
- axle/wheel-centre relative error: `<= 0.5%`;
- primary silhouette landmark normalized error: `<= 1.5%` of vehicle length/height in the relevant axis;
- identity-bearing detail landmark normalized error: `<= 2.0%`;
- no single critical silhouette point may exceed `2.5%`.

Thresholds are machine screening gates, not proof of aesthetic fidelity.

### FAIL
`FAIL_REFERENCE_LANDMARK_ERROR`.

---

## R6 — Multi-view silhouette gate

A side-view match cannot prove 3D fidelity. The same Source revision must be rendered/evaluated from the locked side, front/rear and elevated/plan-constraining views.

### MUST CHECK
- same Source digest across all views;
- no per-view geometry cheats;
- view/camera IDs locked;
- no perspective reference treated as orthographic without calibration/uncertainty note;
- width distribution and shoulder mass are checked independently from side silhouette.

### FAIL
`FAIL_MULTI_VIEW_FIDELITY`.

---

## R7 — Surface flow after silhouette

Only after R4-R6 pass, run BROAD / STRIP / GRAZING / ZEBRA diagnostics on the same Source revision.

Questions:
- does roof-to-rear-deck flow read as one intentional gesture where the reference does?;
- do fender crowns and shoulders terminate in the correct zones?;
- are lamp openings integrated into the primary surface rather than floating on it?;
- does highlight velocity reveal loft bands, faceting or section pinches?

### FAIL
`REVISE_SURFACE_FLOW_AFTER_SILHOUETTE`.

---

## R8 — Identity-bearing features

Identity-bearing features must be placed from reference landmarks after primary form is stable. For an automotive benchmark this normally includes greenhouse, lamp apertures, wheel-arch shape, front intake family, rear light graphic, mirrors and wheel stance.

### FORBIDDEN
- floating spheres/discs used as headlamps when the reference lamp is integrated into a body surface;
- trim or materials used to imply a form that geometry does not contain;
- logos/badges used as a shortcut for model recognition.

### FAIL
`REVISE_IDENTITY_FEATURE_INTEGRATION`.

---

## R9 — Fidelity failure routing

On Reference Fidelity REJECT, classify the dominant cause before editing:
- `REVISION_MISMATCH`
- `HARD_POINT`
- `SIDE_SILHOUETTE`
- `PLAN_WIDTH`
- `GREENHOUSE`
- `WHEEL_ARCH`
- `PRIMARY_SECTION`
- `LAMP_INTEGRATION`
- `SURFACE_FLOW`
- `CAMERA_CALIBRATION`

Change one causal family at a time and regenerate all locked views.

### FAIL
`REVISE_FAILURE_CAUSALITY_UNCLEAR`.

---

## R10 — Promotion boundary

Reference reproduction completion requires all of:
- Machine Gate PASS;
- Evidence Gate PASS;
- Reference Revision Lock PASS;
- multi-view silhouette/landmark gate PASS;
- Source stability PASS;
- independent visual/reference review not REJECT.

Even then, the result does not prove original manufacturer CAD, Class-A production surfacing, tooling feasibility, crash/aero validity, homologation, production CMF or commercial IP clearance unless separately evidenced.

`Reference Fidelity PASS` means the reproduction is sufficiently faithful for the declared benchmark, not that it is manufacturer source geometry.

---

## R11 — Last-known-good regression baseline

A locally improved modeling technique may not replace a previously better candidate merely because the new revision is newer, more complex, or passes its targeted local metric.

Before each causal experiment, persist a measured `LAST_KNOWN_GOOD` baseline and convert every previously passed family outside the edit scope into a regression lock.

### MUST CHECK
- baseline revision / commit / Source-control digest is recoverable;
- edit scope names the causal family being changed;
- every out-of-scope passed metric is rerun with the same valid measurement method;
- a changed diagnostic method is classified as `DIAGNOSTIC_TOOL_CHANGE`, not geometry improvement;
- target improvement and regression state are both recorded;
- rejected experiments remain provenance and cannot silently become the next baseline;
- Design / Reference Fidelity REJECT still vetoes MAIN even when all machine locks pass.

### ALLOWED
- `Machine PASS + KEEP_LKG_REJECT_EXPERIMENT`;
- `Machine PASS + KEEP_LKG_HOLD_EXPERIMENT` when evidence/method is not yet comparable;
- reapplying a useful local method on top of the LKG after removing the regressing portion;
- working-candidate promotion while independent Design/Reference review remains explicitly HOLD, provided no claim is widened to MAIN/Design PASS.

### FORBIDDEN
- dropping a previously passed view because the new revision targets another view;
- loosening the old threshold to avoid reporting a regression;
- using an invalid projection/mask result to justify Source edits;
- promoting a candidate with any `REGRESSED` lock;
- treating model sophistication, patch count or object count as fidelity improvement.

### EVIDENCE
`REFERENCE_REGRESSION_PROMOTION_RECEIPT.json`, validated against `reference-reproduction/REGRESSION_BASELINE_PROMOTION_PROTOCOL_v1.md` and `tools/validate_regression_promotion.py`.

### FAIL
- `FAIL_LKG_BASELINE_MISSING`
- `REJECT_REGRESSION_LOCK_BROKEN`
- `FAIL_REJECTED_EXPERIMENT_BECAME_BASELINE`
- `REVISE_FAILURE_SCOPE_TOO_BROAD`
- `HOLD_MEASUREMENT_METHOD_NOT_VALIDATED`
