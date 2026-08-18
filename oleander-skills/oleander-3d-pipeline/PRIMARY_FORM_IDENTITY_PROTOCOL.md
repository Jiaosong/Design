# PRIMARY FORM IDENTITY PROTOCOL

Status: reusable OLEANDER 3D Skill extension for reference reproduction and identity-critical form work.

## Purpose
A candidate can be dimensionally plausible, topologically clean and numerically close in one or more orthographic gates while still reading as a generic object. This protocol prevents detail work from masking that failure.

`Hard-point PASS ≠ Primary-form identity PASS ≠ Reference-fidelity PASS ≠ Design KEEP`

## Trigger
Use this gate when reproducing or closely matching an existing object whose identity depends on macro form: vehicle, product shell, furniture, appliance, architectural mass, vessel, footwear or similar.

## INPUT
- locked reference revision;
- official/source-grounded hard points;
- at least SIDE + FRONT + REAR or equivalent orthographic/near-orthographic evidence;
- current primary-form candidate;
- current per-gate LKG baseline;
- explicit `does-not-prove` boundary.

## MUST CHECK
1. **Gesture / dominant silhouette** — the main longitudinal or vertical gesture must be measured from final evaluated geometry, not copied back from Source targets.
2. **Cross-view mass hierarchy** — FRONT/REAR width-by-height or equivalent mass distribution must be compared independently from SIDE.
3. **Identity-specific section hierarchy** — where the reference has a meaningful relation such as hood valley vs fender crown, narrow greenhouse vs wide shoulder, seat pan vs back shell, record and test that relation explicitly.
4. **Terminal form** — front/rear/top/bottom terminations cannot be accepted from an otherwise good mid-body RMSE.
5. **Primary skin quality before apertures/details** — measure connectedness, face folding and local edge stretch on the pre-aperture primary skin so legal booleans, caps and trim do not create false surface failures.
6. **Finite measurement coverage** — exact extrema that are degenerate for ray/triangle intersection may be screened by official hard-point locks plus near-terminal samples; finite coverage must be reported and may not silently drop below 90%.
7. **Visual first-read** — if the object reads as the wrong type/generation/model in the first broad view, stop detail work even when machine metrics pass.

## FAILURE ROUTING
- SIDE gesture fails, FRONT/REAR acceptable → edit longitudinal gesture only.
- FRONT fails, SIDE acceptable → edit front section hierarchy; do not reopen wheelbase/length.
- REAR fails, SIDE/FRONT acceptable → edit rear Y/Z or equivalent cross-section envelope only.
- surface QA fails before apertures → repair primary control grid/topology before trim.
- metrics improve but broad/3Q visual identity regresses → keep LKG; reject experiment.
- candidate-derived target is used to generate geometry → resulting low error is `CONSTRAINT_COMPLIANCE`, not independent fidelity evidence.

## ALLOWED
- sparse causal edits to the failing primary-form family;
- denser Derived control grids when sparse topology is proven inadequate, while Source semantics remain explicit;
- perspective-derived width profiles as gross screening constraints with their bias disclosed;
- per-gate best-known baseline updates from an otherwise globally rejected experiment, provided the metric/provenance remains comparable.

## FORBIDDEN
- lamps, seams, CMF, badges, microdetails or lighting used to rescue a generic primary form;
- promoting a candidate because CI is green;
- promoting from Source-target self-comparison;
- relaxing an LKG threshold merely because a new representation changed;
- calling a single-object mesh continuous when it contains disconnected islands or folded shared edges;
- using exact-endpoint intersection failure to hide a terminal-form mismatch.

## EVIDENCE
`PRIMARY_FORM_IDENTITY_RECEIPT.json` containing:
- `candidate_revision`;
- `reference_revision`;
- `gesture_metric`;
- `front_profile_metric`;
- `rear_profile_metric`;
- `identity_relations`;
- `finite_measurement_coverage`;
- `pre_aperture_surface_state`;
- `regression_decision`;
- `visual_review_state`;
- `machine_identity_state`;
- `does_not_prove`.

Machine state may be only `MACHINE_SCREENED_VISUAL_HOLD` or `MACHINE_REJECT`; it may never be plain `PASS` or `KEEP`.

## FAIL
- `REVISE_PRIMARY_FORM_GENERIC`
- `REVISE_DOMINANT_GESTURE`
- `REVISE_FRONT_SECTION_HIERARCHY`
- `REVISE_REAR_SECTION_HIERARCHY`
- `FAIL_PRIMARY_SKIN_TOPOLOGY`
- `FAIL_IDENTITY_MEASUREMENT_COVERAGE`
- `KEEP_LKG_REJECT_EXPERIMENT`

## Does not prove
This protocol does not prove manufacturer CAD, Class-A/G2/G3 continuity, tooling, homologation, production panel architecture, physical CMF, or commercial IP clearance.
