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
4. **Semantic relation metric must match the claim.** A coarse proxy such as FRONT gross-profile RMSE may screen FRONT mass distribution, but it may not be relabeled as proof of a different semantic relation such as hood-center vs fender-crown hierarchy, lamp-in-fender integration, shoulder-to-greenhouse relation or aperture-host ownership. If the semantic relation is not directly measured or otherwise evidenced, its state is `HOLD`, not `SCREENED`.
5. **Terminal form** — front/rear/top/bottom terminations cannot be accepted from an otherwise good mid-body RMSE.
6. **Primary skin quality before apertures/details** — measure connectedness, face folding and local edge stretch on the pre-aperture primary skin so legal booleans, caps and trim do not create false surface failures.
7. **Finite measurement coverage** — exact extrema that are degenerate for ray/triangle intersection may be screened by official hard-point locks plus near-terminal samples; finite coverage must be reported and may not silently drop below 90%.
8. **Visual first-read** — if the object reads as the wrong type/generation/model in the first broad view, stop detail work even when machine metrics pass.

## Semantic claim → evidence rule

Every `identity_relations[]` entry must name the evidence that actually evaluates that relation.

Allowed examples:
- `FASTBACK_GESTURE` ← final evaluated SIDE silhouette;
- `REAR_HIGH_MASS_TAPER` ← final evaluated REAR mass/profile + held-out rear 3/4;
- `FRONT_GROSS_PROFILE` ← final evaluated FRONT width-by-height profile;
- `HOOD_FENDER_HIERARCHY` ← a direct final-surface hood-center vs fender-crown relation metric and/or controlled held-out front view;
- `LAMP_IN_FENDER_INTEGRATION` ← lamp center/diameter + host-surface/crown relationship, not lamp presence alone.

Forbidden substitution:

`FRONT gross-profile PASS → HOOD_FENDER_HIERARCHY SCREENED`

unless a separate metric/evidence item actually tests the hierarchy.

If the semantic metric is missing:
- keep the broad proxy result under its own id;
- emit the semantic identity relation as `HOLD`;
- `MACHINE_SCREENED_VISUAL_HOLD` is forbidden while any required identity relation is `HOLD` or `FAIL`.

## FAILURE ROUTING
- SIDE gesture fails, FRONT/REAR acceptable → edit longitudinal gesture only.
- FRONT fails, SIDE acceptable → edit front section hierarchy; do not reopen wheelbase/length.
- REAR fails, SIDE/FRONT acceptable → edit rear Y/Z or equivalent cross-section envelope only.
- surface QA fails before apertures → repair primary control grid/topology before trim.
- metrics improve but broad/3Q visual identity regresses → keep LKG; reject experiment.
- candidate-derived target is used to generate geometry → resulting low error is `CONSTRAINT_COMPLIANCE`, not independent fidelity evidence.
- semantic relation is claimed from an unrelated proxy metric → invalidate that relation result and rerun with direct evidence.

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
- using exact-endpoint intersection failure to hide a terminal-form mismatch;
- relabeling a broad/profile/silhouette metric as proof of a different identity-specific semantic relation.

## EVIDENCE
`PRIMARY_FORM_IDENTITY_RECEIPT.json` containing:
- `candidate_revision`;
- `reference_revision`;
- `gesture_metric`;
- `front_profile_metric`;
- `rear_profile_metric`;
- `front_semantic_identity_metric` or equivalent claim-specific semantic evidence when the identity relation requires it;
- `identity_relations`, with each relation bound to its actual evidence id;
- `finite_measurement_coverage`;
- `pre_aperture_surface_state`;
- `regression_decision`;
- `visual_review_state`;
- `machine_identity_state`;
- `does_not_prove`.

Machine state may be only `MACHINE_SCREENED_VISUAL_HOLD` or `MACHINE_REJECT`; it may never be plain `PASS` or `KEEP`.

`MACHINE_SCREENED_VISUAL_HOLD` additionally requires every required `identity_relations[]` item to be `SCREENED`. A required semantic relation in `HOLD`/`FAIL` keeps the machine identity state at `MACHINE_REJECT` even when coarse projection metrics are all under threshold.

## FAIL
- `REVISE_PRIMARY_FORM_GENERIC`
- `REVISE_DOMINANT_GESTURE`
- `REVISE_FRONT_SECTION_HIERARCHY`
- `REVISE_REAR_SECTION_HIERARCHY`
- `FAIL_IDENTITY_SEMANTIC_PROXY_SUBSTITUTION`
- `FAIL_PRIMARY_SKIN_TOPOLOGY`
- `FAIL_IDENTITY_MEASUREMENT_COVERAGE`
- `KEEP_LKG_REJECT_EXPERIMENT`

## Does not prove
This protocol does not prove manufacturer CAD, Class-A/G2/G3 continuity, tooling, homologation, production panel architecture, physical CMF, or commercial IP clearance.
