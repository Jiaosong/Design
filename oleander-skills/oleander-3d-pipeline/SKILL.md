---
name: oleander-3d-pipeline
description: Build, diagnose, exchange, render, and audit OLEANDER 3D assets while keeping Source Authority, derived execution, diagnostic evidence, render evidence, design quality, and field/engineering proof separate. Use for Blender and other 3D/CAD/DCC workflows, geometry nodes, product/CMF surfaces, landscape/architecture models, reference reconstruction, original form development, axonometric/exploded technical output, animation, exchange, render handoff, and 3D design review.
compatibility: Blender-first shared capability; principles also apply to Maya, Houdini, Cinema 4D, Rhino/CAD, Unreal/Epic, D5, KeyShot, VRED and common exchange/render toolchains when verified per run.
---

# OLEANDER 3D Pipeline

Use this Skill to produce **real editable 3D assets and verifiable evidence**, not only modeling advice.

Before inventing a local method, resolve the current OLEANDER authority, reuse the current Modeling Worker / Surface System / review contracts, and verify the actual runtime capability available in this run.

Core separation:

`Source Authority ≠ Derived Execution ≠ Diagnostic Evidence ≠ Render Evidence ≠ Design Quality ≠ Field / Engineering / Manufacturing Proof`

A `.blend`, mesh, render, CI PASS, receipt, SHA, export, successful reopen, clean topology, or attractive image proves only the gate that explicitly tested it.

## Current routing boundary

This file is the installed human-readable 3D execution owner on the integration branch.

- Merged reusable Surface System on `main`: `90-shared/toolchains/blender-surface-system/v1.20.0/`.
- Blender Surface System v1.21 Source-aware adapter: **CANDIDATE in PR #173**, not implicit `main` capability until merged/currentized.
- Modeling Worker v0.13: **WORKING_SOURCE / REVISE candidate chain**; do not silently promote its Source model to current authority.
- PR #198 is real Blender benchmark validation of the refined 3D Skill, not Design KEEP.
- PR #208 contains a large candidate specialist/reference-reproduction extension. Its protocols are reusable evidence only when the executing branch actually contains them or the current resolver explicitly selects them.
- Camera Claim Gate from PR #227 is incorporated below as a general design-quality rule.
- Interaction-cue and lifecycle-evidence gates from PR #276 belong in `VISUAL_LAYER_BINDING.md`; they do not create separate Skills.

`CURRENT.md` / `CURRENT.json` are the stable cross-system routing pointers. Versioned PRs, old Drive sync reports, and Practice records remain provenance, not CURRENT by recency.

## Execution grammar

For every applicable section record:

`INPUT → MUST CHECK → ALLOWED → FORBIDDEN → EVIDENCE → FAIL`

Missing evidence stays missing. Do not manufacture certainty or widen a narrow PASS.

---

## 1. Resolve current authority before touching geometry

### INPUT
- current `MASTER PROTOCOL → PROJECT STATE → SOURCE AUTHORITY → CURRENT TASK` when they exist;
- asset / scene identity and current production revision;
- task class;
- application/version, units, scale, origin/up axis, north/CRS where spatial;
- requested deliverable and explicit `does-not-prove` boundary.

### MUST CHECK
1. CURRENT is determined by authority, not timestamp.
2. Legacy/provenance assets are not accidentally re-promoted.
3. Task class is explicit: `SOURCE_EDIT / DERIVED_EXECUTION / DIAGNOSTIC / VISUALIZATION / ANIMATION / EXCHANGE / DELIVERY / REVIEW`.
4. Source mutation permission is explicit.
5. For reference reconstruction, lock maker/object/version/variant/revision and separate `REFERENCE_EVIDENCE` from editable `SOURCE_AUTHORITY` before modeling.
6. If exact reproduction is claimed, source bytes/reference frames must be materialized and identity/hash recorded; browser-visible or remembered reference alone is insufficient.

### ALLOWED
- reversible working copies;
- read-only provenance comparison;
- derived work that cannot overwrite Source.

### FORBIDDEN
- file recency as authority;
- render/export as geometry Source;
- diagnostic-only task mutating Source;
- target/candidate self-reference in fidelity metrics.

### EVIDENCE
`AUTHORITY_RECEIPT` + reference identity/materialization record when applicable.

### FAIL
`HOLD_AUTHORITY_UNRESOLVED` / `HOLD_REFERENCE_IDENTITY_UNRESOLVED`.

---

## 2. Classify every 3D state

Every edited/read object or file must be one of:

1. `SOURCE_OR_WORKING_SOURCE`
2. `DERIVED_EXECUTION`
3. `DERIVED_DIAGNOSTIC_NOT_AUTHORITY`
4. `VISUALIZATION_OR_RENDER_SCENE`
5. `REFERENCE_EVIDENCE`

### MUST CHECK
Record owner, editable state, regeneration origin, mutation permission, persistence requirement, and does-not-prove.

### FORBIDDEN
- dense evaluated geometry becoming Source because it looks finished;
- visualization assets redefining geometry;
- external scan/GIS/CAD/photo/model promoted to measured truth without evidence;
- diagnostic proxy becoming design authority.

### EVIDENCE
`STATE_CLASSIFICATION_TABLE`.

### FAIL
`FAIL_STATE_CLASSIFICATION_AMBIGUOUS`.

---

## 3. Source non-mutation and Blender discipline

### MUST CHECK
For Source-aware diagnostic work:

1. resolve expected Source set;
2. snapshot names/types, transforms, relevant custom properties and editable control geometry;
3. compute deterministic Source identity/digest when supported;
4. regenerate Derived Execution from Source;
5. create disposable diagnostic proxy where needed;
6. mutate diagnostic materials/rig only on non-authoritative objects;
7. run diagnostics;
8. snapshot Source again;
9. compare before/after;
10. fail closed on unauthorized delta;
11. if the Source edit is intentional, record the exact delta and rollback value.

### CURRENT / CANDIDATE ADAPTER RULE
`main` currently exposes Surface System v1.20. The v1.21 Source adapter in PR #173 may be used only when present in the resolved working tree/runtime. Do not write broken v1.21 paths into a receipt and call that execution.

### FORBIDDEN
- Source owner transfer to Surface System;
- clearing/replacing Source material slots for diagnostic-only work;
- destructive modifier on the only editable Source without authorization;
- silent transform bake or Source-family replacement;
- AI-generated geometry/render as Source Authority.

### EVIDENCE
`SOURCE_BEFORE / SOURCE_AFTER / SOURCE_DIGEST / SOURCE_DELTA_RECEIPT` as applicable.

### FAIL
`FAIL_SOURCE_OBJECT_SET_MISMATCH`, `FAIL_SOURCE_MUTATED_DURING_DIAGNOSTIC`, `FAIL_DIAGNOSTIC_TARGET_IS_AUTHORITATIVE`, `FAIL_SOURCE_OWNER_TRANSFER_ATTEMPT`.

---

## 4. Select modeling route and representation before detail

Blender is a capability, not a modeling strategy.

### MUST CHECK
Choose the modeling intent first:

- `REFERENCE_RECONSTRUCTION` — a specific existing object/version governs identity.
- `STRUCTURE_TO_FORM` — original design or no governing reference.
- `SPATIAL_TERRAIN / ARCHITECTURAL` — site/terrain/assembly relation owns the problem.
- `HYBRID` — only when the semantic split is explicit.

Choose a representation family deliberately: parametric solid CAD, feature-curve structured SubD, profile/revolve, skeleton/section assembly, soft-material sim/sculpt-retopo, terrain/GIS spatial, or hybrid.

For controlled form work prefer:

`Source controls → Generated construction → Derived evaluated surface`.

Reference-reproduction candidate protocols in PR #208 and the K3 specialist router are **candidate specialist extensions**, not new project gates. Use them only when current resolution makes them available.

### FAIL
`HOLD_MODELING_ROUTE_UNRESOLVED` / `HOLD_RELATION_MODEL_INSUFFICIENT`.

---

## 5. Sparse causal edits before dense repair

Use the smallest authorized change that can plausibly correct the diagnosed defect:

1. locked global proportions/interfaces;
2. existing profile/guide family;
3. existing relation parameter;
4. one new explicit sparse degree of freedom only after existing vocabulary is proven insufficient;
5. Source-family/topology expansion only after representation inadequacy is demonstrated.

For every control delta record source family, semantic name, unit, previous/new value, allowed range, dependencies/locks, predicted effect, sensitive regions, forbidden side effects, and rollback.

### FORBIDDEN
- unconstrained dense vertex pushing;
- multiple unrelated Source changes inside one A/B diagnostic;
- local mesh patches that bypass Source causality;
- adding detail to hide wrong primary mass.

### EVIDENCE
`SOURCE_EDIT_DELTA` + controlled before/after evidence.

### FAIL
`REVISE_EDIT_CAUSALITY_UNCLEAR` / `FAIL_DENSE_MESH_PATCH_BYPASSES_SOURCE`.

---

## 6. Surface diagnostic protocol

For professional form/surface review use the applicable controlled set. Candidate/reference must share the locked rig unless the rig variable itself is the experiment.

### BROAD — primary mass
Inspect silhouette, proportion, large-radius reflection flow, flattening/bulging, primary termination, single-volume read.

### STRIP — highlight velocity
Inspect acceleration/deceleration, pinching, waviness, transition instability, unjustified asymmetry.

### GRAZING — shallow-angle survival
Inspect faceting, abrupt normal change, dent/ridge, cap/edge collapse, defects hidden in frontal lighting.

### ZEBRA / REFLECTION LINE — continuity and pacing
Inspect line continuity, spacing compression, curvature-rate change, pole/termination loops or hooks.

### HARD BOUNDARIES
- beauty render is not sole surface proof;
- smooth shading, quad topology, dense topology, or readable Zebra do not prove fair surface;
- Zebra alone does not prove `G2/G3/Class-A`;
- post-processing may not soften/remove the defect being judged.

### EVIDENCE
`DIAGNOSTIC_MATRIX` binding Source revision, camera, rig, material, render settings, reference/candidate identity and uncropped evidence.

### FAIL
`INSUFFICIENT_DIAGNOSTIC_EVIDENCE`.

---

## 7. Geometry / topology / evaluated-surface QC

Check Source and Derived layers separately.

### SOURCE
- expected control families exist exactly once;
- controls are sparse, semantic and causally legible;
- boundary/interface ownership is defined;
- symmetry/asymmetry is intentional;
- critical constraints remain within authority.

### DERIVED / EVALUATED
- normals and manifoldness where applicable;
- no unintended holes/duplicates/intersections;
- modifier order and boundary drift controlled;
- UV/material IDs survive required export;
- plausible bounds/units;
- final evaluated geometry is the object measured when a projection/silhouette claim concerns the visible result.

For reference reproduction, `Source target compliance ≠ final evaluated projection ≠ visual reference fidelity`.

### FAIL
`FAIL_SOURCE_STRUCTURE`, `FAIL_DERIVED_TOPOLOGY`, `FAIL_UNIT_OR_BOUNDS`, `REVISE_FORM_DESPITE_CLEAN_TOPOLOGY`, `FAIL_DIAGNOSTIC_MASK_OR_PROJECTION_INVALID`.

---

## 8. Spatial / architectural / landscape models

Classify geometry as:

`FIELD_MEASURED / OFFICIAL_OR_SOURCE_GROUNDED / INFERRED / ASSUMED / DESIGN_PROPOSAL / VISUALIZATION_ENTOURAGE`.

For `FIELD=0`, continue with source-grounded ranges and explicit assumptions; do not stop design development or invent measured precision.

A MAIN candidate model must prove at least one thing better than 2D alone: compression/expansion, sequence, vertical relation, visibility, human scale, construction relation, or material/volume behavior.

### EVIDENCE
`SPATIAL_ASSUMPTION_LEDGER`, human/scale reference, section/axon/sequence proof, FIELD-open legend.

### FAIL
`HOLD_FIELD_DEPENDENT_DIMENSION`, `REVISE_SPATIAL_PROOF_WEAK`, `FAIL_INVENTED_SITE_PRECISION`.

---

## 9. Materials / CMF / visual evidence

Separate:

1. shader/look-development appearance;
2. named material hypothesis;
3. manufacturer/product specification;
4. measured physical material/finish;
5. production CMF decision.

Controlled material comparisons lock geometry, camera and lighting. Roughness/IOR/micro-normal values are representation parameters unless backed by appropriate physical evidence.

Do not use microdetail/noise to camouflage wrong macro geometry.

Physical interaction cues and lifecycle comparisons must additionally follow `VISUAL_LAYER_BINDING.md`.

### FAIL
`INSUFFICIENT_PHYSICAL_CMF_EVIDENCE`, `REVISE_MICRODETAIL_MASKS_FORM`, `FAIL_COMPARISON_NOT_CONTROLLED`.

---

## 10. Camera / render lock + Camera Claim Gate

A locked camera is not automatically the correct camera.

### COMPARISON LOCK
For controlled diagnostics record and hold the applicable camera transform/projection, focal length or ortho scale, crop/aspect, exposure/view transform/color management, world/background, lights, diagnostic material, samples and denoise policy.

### CAMERA CLAIM GATE
Use:

`CLAIM → PROJECTION → CAMERA DISTANCE / FOCAL LENGTH → FIRST-READ → ROLE VERDICT`

1. Declare camera role before tuning: e.g. `EXPERIENCE_HERO`, `RELATION_PROOF`, `TECHNICAL_ORTHO`, `DETAIL`, `SEQUENCE`.
2. Perspective and orthographic views are different evidence. Perspective communicates experiential depth; orthographic removes perspective size falloff and is often better for relation/technical comparison.
3. For perspective record focal length/FOV **with** camera position/distance and target. Focal length alone is incomplete.
4. `FIT EVERYTHING` is not a design rationale. Wider/closer framing may over-weight foreground and suppress the relation being proved.
5. Camera candidate tests keep authoritative geometry unchanged.
6. Review near/mid/far scale relationships and human-scale cues. Foreground expansion or depth compression that changes the intended claim is `REVISE` even if dramatic.
7. Orthographic/axonometric can prove technical relation but must not be promoted as experiential evidence merely because it is clearer.
8. Use lens shift/off-axis framing deliberately; never distort geometry to fake a camera correction.
9. Review at final crop, responsive frame, board placement or sequence output size.
10. Camera quality does not prove real viewpoint, measured visibility, field perception or lens calibration.

Default fail: if the reviewer cannot state **what the camera proves, why the projection is appropriate, and how distance/focal length changes spatial emphasis**, the view remains `REVISE`.

### EVIDENCE
`RIG_LOCK_RECEIPT` + `CAMERA_CLAIM_RECEIPT`.

### FAIL
`FAIL_RIG_LOCK_DRIFT`, `INSUFFICIENT_COMPARISON_CAUSALITY`, `REVISE_CAMERA_CLAIM_UNPROVEN`.

---

## 11. Axonometric / exploded / technical output

1. lock camera orientation/scale/crop/reference direction;
2. preserve real component scale except explicit diagrammatic separation;
3. group by technical meaning;
4. show connection/assembly direction, access and maintenance logic;
5. export vector linework where feasible;
6. raster passes support material/shadow/depth/AO only;
7. labels/dimensions remain editable vector 2D unless truly spatial;
8. show human/installation/maintenance scale where useful;
9. distinguish verified dimensions, recommended ranges, assumptions and FIELD-open values.

### FORBIDDEN
- decorative floating parts without assembly logic;
- rasterized labels when editable vector text is required;
- invented fastener/member/foundation precision;
- AI image replacing editable technical geometry/annotation.

### EVIDENCE
editable vector technical output + linked model revision + dimension/status legend + preview.

### FAIL
`REVISE_TECHNICAL_HIERARCHY_UNREADABLE`, `FAIL_DIMENSION_STATUS_AMBIGUOUS`, `FAIL_DECORATIVE_EXPLODED_NOT_TECHNICAL`.

---

## 12. Exchange and round-trip

Choose format by purpose, not convenience: USD, glTF/GLB, FBX, OBJ, Alembic, STEP/IGES when semantics are preserved, EXR for render passes.

Round-trip a representative asset before full delivery and verify units/bounds, axis/origin, hierarchy/instances, normals/smoothing, materials/textures, cameras/animation, critical names and known semantic loss.

Interchange output is derived by default; it does not silently become Source Authority.

### EVIDENCE
`ROUNDTRIP_REPORT` with source/export hashes, receiving app/version, checks and losses.

### FAIL
`FAIL_ROUNDTRIP_SCALE`, `FAIL_ROUNDTRIP_AXIS_OR_ORIGIN`, `FAIL_ROUNDTRIP_SEMANTIC_LOSS`, `FAIL_EXPORT_PROMOTED_TO_SOURCE`.

---

## 13. Production asset / persistence contract

Execution tasks must return actual artifacts, not only chat prose.

Minimum applicable families:
- authoritative/editable Source or exact Source reference;
- requested derived/export asset;
- Source snapshot/digest when supported;
- model/dependency/toolchain manifest;
- units/origin/axis record;
- render/diagnostic rig identity;
- exchange report when applicable;
- review evidence;
- machine receipt/log;
- SHA-256 register for retained binaries;
- known limitations and does-not-prove.

### FORBIDDEN
- preview-only delivery when native/editable source is required;
- hashes without retained files;
- manifest entries for files that do not exist;
- binary existence treated as Design PASS.

### FAIL
`FAIL_REQUIRED_ARTIFACT_MISSING`, `FAIL_RETAINED_BINARY_UNRECOVERABLE`, `FAIL_MANIFEST_ASSET_MISMATCH`.

---

## 14. Review gates and causal failure routing

### THREE INDEPENDENT GATES
**Machine / Execution:** can it open, regenerate, render/export/round-trip and preserve authority boundaries?

**Evidence:** does the submitted evidence actually demonstrate the claimed property under controlled conditions?

**Design Quality:** does an independent Design Crit judge proportion, silhouette, curvature/transition, material/form relation, scale, spatial clarity, construction legibility and professional finish at the required level?

The producing process must not self-convert Machine PASS into Design PASS or MAIN KEEP.

### FAILURE ROUTING
Route to the earliest layer that owns the cause:
- wrong mass/silhouette → Source proportions / primary profiles / representation;
- good mass, local reflection kink → sparse relation/profile control;
- failure only after tessellation/export → derived topology/export;
- good geometry, unreadable render → camera/rig/material;
- unsupported scale → evidence/assumption layer;
- reference mismatch despite low self-target error → independent evaluated projection/reference fidelity;
- repeated same-question revisions → invoke existing Control Plane repeated-revise breaker and reclassify `Parameter / Relation / Geometry / Topology / Architecture / Evidence` before more tuning.

### EVIDENCE
`REVIEW_GATE_MATRIX` + `FAILURE_ROUTE_RECEIPT` when a failure is being repaired.

### FAIL
`FAIL_GATE_COLLAPSE`, `REVISE_DESIGN_QUALITY`, `REJECT_DESIGN_QUALITY`, `HOLD_INDEPENDENT_REVIEW_MISSING`, `HOLD_ROOT_CAUSE_UNRESOLVED`.

`Artifact existence ≠ Design quality`

`Traceability ≠ Professional finish`

`Evidence correctness ≠ Visual excellence`

`Process PASS ≠ MAIN KEEP`

---

## 15. Completion condition

A 3D task is complete only to the requested level when:

1. actual editable/derived assets exist as required;
2. applicable evidence exists;
3. retained files can be reopened or machine-checked where possible;
4. Source/Derived/Diagnostic/Render boundaries remain intact;
5. Machine, Evidence and Design conclusions are separately stated;
6. unresolved field, engineering, manufacturing, physical CMF or native-app proof is listed;
7. every requested deliverable has an explicit status;
8. no missing requirement is disguised as a workflow/process PASS.

Partial completion is valid when residual blockers are exact.

### EVIDENCE
`COMPLETION_RECEIPT`.

### FAIL
`PARTIAL_REQUIRED_NATIVE_VALIDATION_MISSING`, `PARTIAL_REQUIRED_ARTIFACT_MISSING`, `HOLD_REQUIRED_REVIEW_MISSING`, `FAIL_FALSE_COMPLETION_CLAIM`.

---

## Cross-section invariants

- Source digest unchanged → proves non-mutation, **not** surface quality.
- Clean topology → proves topology checks, **not** professional form.
- Zebra improvement → supports reflection-flow observation, **not** Class-A certification.
- Low error against a curve used to generate the candidate → can be self-reference; it does **not** prove multi-view identity.
- GLB round-trip → proves that exchange test, **not** Source validity.
- Attractive render → does not prove geometry, material truth, field truth or usability.
- FIELD=0 → does not stop design development; field-dependent claims remain open.
- A specialist route/protocol may improve execution without creating a new project gate, Authority state or promotion state.
