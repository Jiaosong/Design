# OLEANDER 3D Pipeline — Reference Image Calibration Protocol v1

Use this extension when the target is an **existing real object / vehicle / product / spatial form whose identity must be reproduced**, not merely a generic form benchmark.

Core separation:

`Reference Evidence ≠ Source Authority ≠ Candidate Geometry ≠ Machine Screening ≠ Visual Reference Fidelity ≠ Design Quality`

## 1. Reference Revision Lock

### INPUT
- exact maker / product / generation / variant / model year or revision;
- official hard points where available;
- reference images or licensed/read-only geometry;
- allowed transfer scope for every reference.

### MUST CHECK
- dimension revision and visual revision cannot be silently mixed;
- a nearby variant may constrain only explicitly invariant geometry;
- variant-specific fascia, trim, wheel, graphic or aero detail cannot be transferred without evidence;
- every reference stores URL/source identity, file hash when persisted, revision, role and allowed/forbidden transfer scope.

### FAIL
`FAIL_REFERENCE_REVISION_MIXED` or `HOLD_REFERENCE_TRANSFER_SCOPE_UNRESOLVED`.

## 2. Ground-truth precedence

Use the highest legally and technically available tier:

1. `AUTHORIZED_MEASURED_OR_MANUFACTURER_GEOMETRY`
2. `AUTHORIZED_READ_ONLY_REFERENCE_GEOMETRY`
3. `CALIBRATED_SAME_REVISION_OR_SAME_BODY_SHELL_IMAGERY`
4. `SOURCE_GROUNDED_VISUAL_LANDMARK_ESTIMATE`
5. `DESIGNER_ESTIMATE`

A lower tier may fill a gap but cannot overwrite a higher tier.

Normal public access may be probed. Authentication, paywall, protected viewer/CDN or private asset access must not be bypassed. Emit `HOLD_AUTH_REQUIRED_NO_BYPASS` when the only better reference is access-controlled.

## 3. Calibrated imagery

For a near-orthographic image, calibration must bind at least two independent metric constraints and preferably four longitudinal anchors.

Automotive example:
- rear extreme;
- rear axle;
- front axle;
- front extreme;
- official overall length / wheelbase;
- official height;
- tyre OD or another independent vertical scale cue.

Perspective distortion must not be hidden by one global scale when wheelbase and overall length disagree. Use piecewise/projective calibration or explicitly downgrade confidence.

### EVIDENCE
`REFERENCE_CONTOUR_TARGETS*.json` containing:
- source/hash/revision;
- pixel anchors;
- calibration method;
- metric target contour/landmarks;
- transfer scope;
- thresholds;
- does-not-prove.

## 4. Silhouette-first reconstruction

Before secondary geometry, detail or CMF, the candidate must satisfy all in-scope primary projections:

`SIDE → FRONT → REAR → PLAN / 3Q consistency`

Do not let one view pass by changing geometry per camera.

For automotive/product forms, primary Source must be decomposed into causally meaningful families rather than one generic loft when the reference demands it. Typical families:
- body plan / envelope;
- hood/deck spine;
- fender/shoulder crown;
- rear-quarter/haunch;
- greenhouse/roof;
- rocker/lower body;
- apertures;
- end-form plan curvature.

If repeated parameter tuning cannot satisfy multiple views, emit `HOLD_RELATION_MODEL_INSUFFICIENT` and change the Source representation. Do **not** keep adding detail to a wrong macro form.

## 5. Aperture / exposure chain

Windows, lamps, intakes and openings must be checked as a host relationship:

`host surface → opening/recess → frame/interface → lens/glass → backing/void`

Forbidden:
- floating lamp/glass objects used to fake identity;
- exterior body caps visibly exposed behind glazing;
- dark rectangles covering an incorrect host surface;
- detail density used to hide macro-form failure.

Failures:
- `FAIL_APERTURE_HOST_RELATION`
- `FAIL_EXTERIOR_CAP_EXPOSED`
- `REVISE_IDENTITY_DETAIL_MASKS_FORM`

## 6. Reference target vs candidate measurement

A machine fidelity receipt must keep two independent provenance fields:
- `reference_target_source`
- `candidate_measurement_source`

They may not be identical. The validator recomputes error from `target`, `candidate`, and `normalization`; a caller-supplied `normalized_error` cannot override the computation.

If the candidate is intentionally generated from a calibrated target, that proves **binding / construction compliance only**. It does not independently prove visual fidelity.

## 7. Gates

Keep these states separate:

- `MACHINE_EXECUTION_PASS`
- `REFERENCE_BINDING_SCREENING_PASS`
- `REFERENCE_FIDELITY_REVIEW_KEEP / REVISE / REJECT`
- `SURFACE_QUALITY_KEEP / REVISE / REJECT`
- `DESIGN_QUALITY_KEEP / REVISE / REJECT`

`CI PASS` or low contour error cannot set `REFERENCE_FIDELITY_REVIEW_KEEP` by itself.

## 8. Iteration routing

Route the failure to the earliest causal layer:

- wrong length/track/height → Hard Points;
- wrong silhouette/proportion → Envelope / Section Network;
- one view right, another wrong → Source representation / cross-section family;
- floating windows/lights → Aperture architecture;
- reflection instability on correct mass → Surface controls;
- wheel/mirror/trim only → Secondary/Detail;
- shader problem only → CMF / Render.

Once a failure is identified upstream, downstream detail work stops until that gate is reopened and corrected.

## 9. Knowledge capture

After a real benchmark exposes a reusable failure mode, write the validated transfer rule into the OLEANDER Notion knowledge base (`50｜Methods & Design Intelligence`) and keep executable contracts/tests in GitHub. Notion is the knowledge layer; GitHub is the executable evidence layer. Neither substitutes for the other.
