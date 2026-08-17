---
name: oleander-3d-pipeline
description: Build, diagnose, exchange, render, and audit OLEANDER 3D assets without collapsing Source Authority, derived execution, rendering evidence, and design quality into one state. Use whenever work involves Blender, Maya, Houdini, Cinema 4D, Unreal, D5, KeyShot, VRED, geometry nodes, procedural modeling, product/CMF surfaces, landscape/architecture models, axonometric or exploded drawings, animation, FBX/glTF/USD/Alembic, render handoff, or 3D design review.
compatibility: Blender-first; also applies to Maya, Houdini, Cinema 4D, Unreal/Epic, D5, KeyShot, VRED and common exchange/render toolchains.
---

# OLEANDER 3D Pipeline

Use this Skill to produce **real 3D assets and verifiable 3D evidence**, not only modeling advice. Reuse the repository's current Modeling Worker, Blender Surface System, render/QC contracts, project state and review system before inventing a local method.

Core separation:

`Source Authority ≠ Derived Execution ≠ Diagnostic Evidence ≠ Render Evidence ≠ Design Quality ≠ Field / Engineering Proof`

A `.blend`, mesh, render, CI PASS, receipt, SHA, export or successful reopen proves only the gate that explicitly tested it. None may be silently promoted to professional design approval.

## Execution grammar used by every section

Each numbered section below is an executable contract with the same six fields:

- **INPUT** — information/assets that must be resolved before the section can pass.
- **MUST CHECK** — checks that cannot be skipped.
- **ALLOWED** — actions permitted at this layer.
- **FORBIDDEN** — shortcuts that invalidate the section.
- **EVIDENCE** — concrete output that must exist when the section is in scope.
- **FAIL** — machine-readable failure code or review state to emit rather than improvising.

When a required input is unavailable, do not manufacture certainty. Use a reversible working copy, explicit uncertainty and the section's FAIL state.

Machine-readable execution contracts:

- `oleander-skills/oleander-3d-pipeline/contracts/BLENDER_3D_AUTHORITY_DIAGNOSTIC_CONTRACT_v1.json`
- `oleander-skills/oleander-3d-pipeline/contracts/BLENDER_3D_RECEIPT_SCHEMAS_v1.json`

The first defines section gates and prohibitions; the second defines the minimum fields for each section's evidence receipt. A receipt with missing required fields is incomplete evidence, not a PASS.

---

## 1. Start from current authority

### INPUT
- current `MASTER PROTOCOL`, `PROJECT STATE`, `SOURCE AUTHORITY`, `CURRENT TASK` when they exist;
- project/asset/scene identity;
- current production asset and revision;
- authoring application/version;
- unit system, scale, origin/up axis and north/CRS where relevant;
- task purpose and requested deliverable;
- explicit `does-not-prove` boundary.

### MUST CHECK
1. Resolve authority in this order:

   `MASTER PROTOCOL → PROJECT STATE → SOURCE AUTHORITY → CURRENT TASK → current production asset`

2. Confirm the source being opened is CURRENT, not merely newest by timestamp.
3. Confirm legacy/provenance assets are not accidentally re-promoted.
4. Confirm task class: `SOURCE_EDIT / DERIVED_EXECUTION / DIAGNOSTIC / VISUALIZATION / ANIMATION / EXCHANGE / DELIVERY / REVIEW`.
5. Confirm whether the task authorizes Source modification.

### ALLOWED
- read legacy assets for provenance/comparison;
- create a branch/copy when authority is unresolved;
- continue reversible derived work that cannot overwrite Source.

### FORBIDDEN
- overwriting a candidate Source because it is easier to open;
- using file recency as authority;
- treating a render/export as Source Authority;
- changing Source when the task is diagnostic-only.

### EVIDENCE
`AUTHORITY_RECEIPT` containing project, asset, source id/path, revision/hash when available, task class, application/version, units, scale, coordinate convention and does-not-prove.

### FAIL
`HOLD_AUTHORITY_UNRESOLVED` if current authority cannot be resolved safely.

---

## 2. Classify every 3D state before acting

### INPUT
All objects/files that will be read, edited, regenerated, rendered or exported.

### MUST CHECK
Every object/file must be explicitly classified as one of:

1. `SOURCE_OR_WORKING_SOURCE`
2. `DERIVED_EXECUTION`
3. `DERIVED_DIAGNOSTIC_NOT_AUTHORITY`
4. `VISUALIZATION_OR_RENDER_SCENE`
5. `REFERENCE_EVIDENCE` when an external scan/GIS/CAD/photo/model is evidence but not editable design authority.

### ALLOWED
- regenerate Derived Execution from Source;
- discard/rebuild Derived Diagnostic freely;
- change visualization rig without changing Source;
- bind reference evidence without promoting it.

### FORBIDDEN
- implicit state changes;
- dense geometry becoming Source because it looks finished;
- visualization assets redefining geometry;
- external reference geometry being treated as measured truth without evidence.

### EVIDENCE
`STATE_CLASSIFICATION_TABLE` with object/file id, class, owner, editable?, regenerated-from, may-mutate?, persistence requirement and does-not-prove.

### FAIL
`FAIL_STATE_CLASSIFICATION_AMBIGUOUS` if any edited target has no explicit state.

### State definitions

**SOURCE / WORKING SOURCE** — editable geometry or sparse relational controls that own the current design definition: NURBS/Bezier curves, profile/guide curves, section/control cages, explicit scalar relation parameters, designated terrain/CAD authority.

**DERIVED EXECUTION** — dense/application-specific geometry generated for evaluation, display, simulation, export or rendering: tessellated bodies, remeshes, baked Geometry Nodes, triangulated GLB, render meshes.

**DERIVED DIAGNOSTIC** — disposable diagnostic geometry. In the current Blender v1.21 line the proxy role is `DERIVED_DIAGNOSTIC_NOT_AUTHORITY`.

**VISUALIZATION / RENDER SCENE** — cameras, lights, worlds, presentation materials, post-processing and staging.

**REFERENCE EVIDENCE** — external evidence used to constrain or compare but not automatically promoted to Source.

---

## 3. Blender Source Authority discipline

### INPUT
- authoritative Blender Source collection;
- expected Source object set;
- Source-aware adapter/contract when available;
- task mutation permission.

Current v1.21 implementation:
- `90-shared/toolchains/blender-surface-system/v1.21.0/source_authority_adapter.py`
- `90-shared/toolchains/blender-surface-system/v1.21.0/SOURCE_AUTHORITY_ADAPTER_CONTRACT_v1.21.0.json`

### MUST CHECK
For Source-aware diagnostic work execute in this order:

1. resolve Source collection and expected object set;
2. snapshot names/types, transforms, relevant custom properties and editable control geometry;
3. compute deterministic Source digest when supported;
4. regenerate Derived Execution from Source;
5. create disposable diagnostic proxy;
6. assign diagnostic materials only to the proxy;
7. run diagnostics;
8. snapshot Source again;
9. compare before/after digest;
10. fail closed on unauthorized Source delta;
11. if a Source edit was intentional, record the exact authorized delta and new digest.

### ALLOWED
- read and bind Source context;
- evaluate dependency graph;
- create non-authoritative proxy/evaluated mesh;
- perform an authorized Source edit with explicit delta receipt.

### FORBIDDEN
- Source owner transfer to Surface System;
- clearing/replacing Source material slots for diagnostic-only work;
- destructive modifiers on the only authoritative editable object without Source-edit authorization;
- unrecorded transform bake;
- silent topology/source-family replacement;
- AI-generated geometry/render as Source Authority.

### EVIDENCE
`SOURCE_BEFORE.json`, `SOURCE_AFTER.json`, deterministic digest(s), proxy identity/role, `SOURCE_DELTA_RECEIPT` when edited, and `.blend` persistence artifact when native validation is in scope.

### FAIL
- `FAIL_SOURCE_OBJECT_SET_MISMATCH`
- `FAIL_SOURCE_MUTATED_DURING_DIAGNOSTIC`
- `FAIL_DIAGNOSTIC_TARGET_IS_AUTHORITATIVE`
- `FAIL_SOURCE_OWNER_TRANSFER_ATTEMPT`

The Surface System may read/bind Source; Modeling Worker/project Source ownership remains authoritative unless current governance explicitly says otherwise.

---

## 4. Sparse-edit preference for controlled surface work

### INPUT
- diagnosed defect region;
- locked interfaces/global proportions;
- current Source families/relations;
- before diagnostic evidence;
- mutation authorization.

### MUST CHECK
Use the smallest authorized change that can plausibly correct the diagnosed defect. Evaluate in this order:

1. locked global proportions/interfaces — confirm they are truly locked;
2. existing profile/guide family;
3. existing relation parameter;
4. one new explicit sparse degree of freedom only if existing controls are proven insufficient;
5. source-family/topology expansion only if relation model inadequacy is demonstrated.

For every changed/new control record:
- owner Source family;
- semantic name;
- unit;
- previous value;
- new value;
- allowed range;
- dependencies/locks;
- predicted geometric effect;
- sensitive regions;
- forbidden side effects;
- rollback value.

### ALLOWED
- one-variable or one-relation-family experiments;
- controlled A/B parameter sweeps;
- rollback to exact previous Source state.

### FORBIDDEN
- unconstrained dense vertex pushing;
- multiple unrelated Source changes in one diagnostic comparison;
- new control families introduced only to chase one highlight symptom;
- local mesh patching that bypasses Source causality.

### EVIDENCE
`SOURCE_EDIT_DELTA.json` plus before/after controlled diagnostic views and rollback value.

### FAIL
- `REVISE_EDIT_CAUSALITY_UNCLEAR`
- `FAIL_DENSE_MESH_PATCH_BYPASSES_SOURCE`
- `HOLD_RELATION_MODEL_INSUFFICIENT` only after existing vocabulary has been tested, not assumed.

---

## 5. Surface diagnostic protocol

### INPUT
- candidate and reference/baseline;
- locked diagnostic camera/rig/material/color management;
- Source digest;
- required defect question.

### MUST CHECK
For professional product/form review, run the full controlled set unless a narrower scope is explicitly justified.

### BROAD
**Question:** Is the primary mass intentional?

**Lock:** same camera, crop, material and broad-area light.

**Inspect:** silhouette, proportion, large-radius reflection flow, unexpected flattening/bulging, primary mass termination, single-volume read.

**Evidence:** `BROAD_REFERENCE` + `BROAD_CANDIDATE`.

**Failure signatures:** `MASS_PROPORTION`, `LARGE_RADIUS_FLOW`, `PRIMARY_TERMINATION`.

### STRIP
**Question:** Where does highlight velocity reveal local instability?

**Lock:** same strip rig width/position/energy between reference and candidate.

**Inspect:** band acceleration/deceleration, pinching, local waviness, unjustified asymmetry, interface/termination discontinuity.

**Evidence:** `STRIP_REFERENCE` + `STRIP_CANDIDATE`.

**Failure signatures:** `LOCAL_WAVINESS`, `PINCH`, `TRANSITION_INSTABILITY`.

### GRAZING
**Question:** Does the form survive shallow-angle lighting?

**Lock:** same grazing angle, light size, energy and material.

**Inspect:** faceting, abrupt normal change, dent/ridge, cap/edge collapse, defects hidden by frontal light.

**Evidence:** `GRAZING_REFERENCE` + `GRAZING_CANDIDATE`.

**Failure signatures:** `FACETING`, `DENT_RIDGE`, `CAP_COLLAPSE`, `NORMAL_INSTABILITY`.

### ZEBRA / REFLECTION-LINE
**Question:** Are reflection lines continuous and intentionally paced?

**Lock:** same stripe field orientation/frequency and camera.

**Inspect:** line continuity, spacing compression, curvature-rate change, pole/termination behavior, loops/hooks.

**Evidence:** `ZEBRA_REFERENCE` + `ZEBRA_CANDIDATE`.

**Failure signatures:** `REFLECTION_KINK`, `SPACING_COMPRESSION`, `POLE_HOOK`, `TERMINATION_LOOP`.

### ALLOWED
- one rig-variable change when that variable is itself under test, explicitly labeled;
- crops/annotations that preserve the uncropped evidence;
- quantitative continuity analysis when the underlying representation supports it.

### FORBIDDEN
- beauty render as sole surface proof;
- different cameras/lighting between A/B without disclosure;
- Zebra-only `G2/G3/Class-A` claim;
- post-processing that removes/softens geometric defects.

### EVIDENCE
`DIAGNOSTIC_MATRIX.json` binding each view to source digest, camera id, rig id, material id, render settings, reference image and candidate image.

### FAIL
`INSUFFICIENT_DIAGNOSTIC_EVIDENCE` when required controlled views are missing or incomparable.

---

## 6. Geometry and topology checks

### INPUT
Source representation, Derived Execution representation and target use/export.

### MUST CHECK

**Source level**
- expected Source objects/families exist exactly once;
- controls are intentional, legible and causally sparse;
- curve degree/order and endpoint behavior are intentional;
- symmetry/asymmetry is explicit;
- interfaces share defined references;
- critical dimensions/relations remain within current constraints.

**Derived mesh level**
- normals/coherent shading;
- no unintended non-manifold edges, holes, duplicates;
- intentional triangulation where required;
- stable modifier order;
- subdivision/remesh boundary drift within tolerance;
- UV/material IDs survive required export;
- plausible bounding box/units;
- no evaluated-mesh artifact is mistaken for Source.

### ALLOWED
- repair derived topology when failure occurs only downstream;
- retessellate without altering Source definition;
- generate comparison statistics.

### FORBIDDEN
- treating clean topology as design-quality evidence;
- editing Source to compensate for an export-only defect before isolating the downstream cause;
- destructive cleanup that erases the only editable Source.

### EVIDENCE
`GEOMETRY_QC_RECEIPT` with source-level and derived-level results separately.

### FAIL
- `FAIL_SOURCE_STRUCTURE`
- `FAIL_DERIVED_TOPOLOGY`
- `FAIL_UNIT_OR_BOUNDS`
- `REVISE_FORM_DESPITE_CLEAN_TOPOLOGY`

---

## 7. Spatial / architectural / landscape models

### INPUT
- site/project coordinate/scale assumptions;
- measured/survey data when available;
- official map/GIS/terrain/reference evidence;
- design proposal geometry;
- FIELD status.

### MUST CHECK
Classify geometry into:
- `FIELD_MEASURED`
- `OFFICIAL_OR_SOURCE_GROUNDED`
- `INFERRED`
- `ASSUMED`
- `DESIGN_PROPOSAL`
- `VISUALIZATION_ENTOURAGE`

For `FIELD=0`, continue with source-grounded ranges and explicit assumptions. Do not downgrade the work to an uninformative grey model solely because field data is missing.

MAIN candidate spatial models must demonstrate at least one property better than 2D alone:
- spatial compression/expansion;
- sequence;
- vertical relation;
- visibility;
- human scale;
- construction relation;
- material/volume behavior.

### ALLOWED
- sourced range modeling;
- scenario variants;
- field-open placeholders;
- explicit replacement slots for later survey data.

### FORBIDDEN
- invented precision presented as measured;
- model beauty standing in for spatial proof;
- `FIELD=0` used as a reason to stop all design development;
- visualization entourage treated as site fact.

### EVIDENCE
`SPATIAL_ASSUMPTION_LEDGER`, scale figure/human reference, section/axon/sequence evidence, and `FIELD_OPEN` labels where applicable.

### FAIL
- `HOLD_FIELD_DEPENDENT_DIMENSION`
- `REVISE_SPATIAL_PROOF_WEAK`
- `FAIL_INVENTED_SITE_PRECISION`

---

## 8. Materials and CMF

### INPUT
- geometry revision/source digest;
- lighting/camera lock;
- material hypotheses;
- manufacturer/measurement data when making production claims.

### MUST CHECK
Separate:
1. shader/look-development appearance;
2. named material hypothesis;
3. manufacturer/product specification;
4. measured physical material/finish;
5. production CMF decision.

For controlled CMF comparisons keep geometry, camera and lighting constant. Record perceptual approximations separately from physical data.

### ALLOWED
- shader look-dev;
- controlled roughness/IOR/micro-normal comparisons;
- manufacturer-data-backed parameterization;
- provisional visual hypotheses.

### FORBIDDEN
- noise/detail used to conceal poor macro geometry;
- Principled BSDF values presented as measured CMF truth;
- changed geometry/lighting during a material-only comparison;
- production readiness claimed from appearance alone.

### EVIDENCE
`CMF_COMPARISON_MATRIX` with geometry digest, rig id, material id, shader parameters, evidence source/status and does-not-prove.

### FAIL
- `INSUFFICIENT_PHYSICAL_CMF_EVIDENCE`
- `REVISE_MICRODETAIL_MASKS_FORM`
- `FAIL_COMPARISON_NOT_CONTROLLED`

---

## 9. Camera and render controls

### INPUT
Reference/candidate scenes and comparison purpose.

### MUST CHECK
For comparative diagnostics lock:
- camera transform/projection;
- focal length or orthographic scale;
- crop/aspect;
- exposure/view transform/color management;
- world/background;
- light transform/size/energy/shape;
- diagnostic material;
- samples/denoise policy where it affects evidence.

Hash or uniquely identify the lock set when supported.

### ALLOWED
- deliberate one-variable tests;
- beauty rig separate from diagnostic rig;
- render optimization that does not change diagnostic readability.

### FORBIDDEN
- multi-variable drift between A/B comparisons;
- changing crop to hide failure;
- denoising/post that changes reflection evidence;
- beauty render substituted for diagnostic render.

### EVIDENCE
`RIG_LOCK_RECEIPT` and render-setting identity.

### FAIL
- `FAIL_RIG_LOCK_DRIFT`
- `INSUFFICIENT_COMPARISON_CAUSALITY`

---

## 10. Axonometric, exploded and technical outputs

### INPUT
Current geometry, assembly hierarchy, drawing purpose, target scale/page/crop and technical claim.

### MUST CHECK
1. lock camera orientation/scale/crop/reference direction;
2. preserve real component scale except explicitly diagrammatic separation;
3. group geometry by technical meaning;
4. show connection and assembly direction legibly;
5. export vector linework where feasible;
6. use raster passes only as support for material/shadow/depth/AO;
7. keep labels/dimensions as vector 2D unless truly spatial;
8. include human/maintenance/installation scale where it clarifies use;
9. distinguish verified dimensions, recommended ranges and FIELD-open values.

### ALLOWED
- exploded offsets that preserve component proportions;
- vector overlays;
- section cuts and callouts;
- raster support beneath vector technical information.

### FORBIDDEN
- decorative floating parts without assembly logic;
- rasterized labels when editable vector text is required;
- invented fastener/member/foundation precision;
- AI image replacing editable technical geometry/annotation.

### EVIDENCE
`EDITABLE_VECTOR_TECHNICAL_OUTPUT` + linked model revision + dimension/status legend + preview.

### FAIL
- `REVISE_TECHNICAL_HIERARCHY_UNREADABLE`
- `FAIL_DIMENSION_STATUS_AMBIGUOUS`
- `FAIL_DECORATIVE_EXPLODED_NOT_TECHNICAL`

---

## 11. Exchange and round-trip

### INPUT
Source application, receiving application, semantic requirements and delivery purpose.

### MUST CHECK
Choose format by purpose:
- USD — hierarchy/variants/richer scene interchange;
- glTF/GLB — lightweight realtime review/delivery;
- FBX — animation/compatibility bridge;
- OBJ — simple static fallback;
- Alembic — baked geometry/cache;
- STEP/IGES — CAD/NURBS exchange when receiving workflow preserves required semantics;
- EXR — HDR render/pass delivery.

Before full delivery, round-trip a representative asset and verify:
- units/bounds;
- axis/origin;
- hierarchy/instances;
- normals/smoothing;
- materials/textures;
- cameras/animation where required;
- critical named objects;
- geometry/topology drift where relevant.

### ALLOWED
- multiple export targets for distinct downstream needs;
- derived exchange meshes;
- compatibility fallbacks with explicit semantic loss.

### FORBIDDEN
- one-format-fits-all selection by convenience;
- silent unit/axis changes;
- exported interchange file becoming Source Authority by default;
- unreported semantic loss.

### EVIDENCE
`ROUNDTRIP_REPORT` with source hash, export hash, import target/version, verification results and known losses.

### FAIL
- `FAIL_ROUNDTRIP_SCALE`
- `FAIL_ROUNDTRIP_AXIS_OR_ORIGIN`
- `FAIL_ROUNDTRIP_SEMANTIC_LOSS`
- `FAIL_EXPORT_PROMOTED_TO_SOURCE`

---

## 12. Required production artifacts

### INPUT
Task class and scope.

### MUST CHECK
Emit only artifacts relevant to scope, but never only chat prose for an execution task.

Minimum families:
- authoritative/editable Source or explicit Source reference;
- derived execution/export when requested;
- Source snapshot/digest when supported;
- model manifest;
- dependency/toolchain manifest;
- units/origin/axis record;
- exchange/round-trip report when applicable;
- render/diagnostic rig identity when applicable;
- review evidence;
- machine receipt/log;
- SHA-256 register for retained binaries;
- known limitations and does-not-prove.

For Blender Source-aware diagnostics preserve `.blend` plus machine-readable Source/diagnostic receipts when supported.

### ALLOWED
- scope-specific subsets defined by a task→artifact matrix;
- deterministic regeneration for disposable derivatives;
- compressed delivery package if originals remain recoverable.

### FORBIDDEN
- preview-only delivery when native/editable asset is required;
- hashes without retained files;
- manifest claiming files not actually present;
- binary existence treated as Design PASS.

### EVIDENCE
`PRODUCTION_ASSET_MANIFEST` with path, role, state class, bytes, SHA256, application/version, dependencies, recoverability and validation status.

### FAIL
- `FAIL_REQUIRED_ARTIFACT_MISSING`
- `FAIL_RETAINED_BINARY_UNRECOVERABLE`
- `FAIL_MANIFEST_ASSET_MISMATCH`

---

## 13. Review gates: do not self-promote

### INPUT
Machine evidence, controlled design evidence and independent critic result when MAIN promotion is requested.

### MUST CHECK

**Machine / execution gate**
Question: can the asset open, regenerate, render/export, round-trip and preserve its authority boundary?
Result: `PASS / FAIL`.

**Evidence gate**
Question: does the submitted evidence actually demonstrate the claimed property under controlled conditions?
Result: `PASS / INSUFFICIENT / CONTRADICTED`.

**Design quality gate**
Question: does an independent Design Crit judge proportion, silhouette, curvature/transition, material/form relation, scale, spatial clarity, construction legibility and professional finish at the required level?
Result: `KEEP / REVISE / REJECT / HOLD`.

These gates are independent. The producing process must not self-convert machine success to Design PASS or MAIN KEEP.

### ALLOWED
- Machine PASS + Design REVISE;
- Evidence PASS + Design REJECT;
- Design HOLD when required evidence is genuinely missing;
- independent critic to veto MAIN.

### FORBIDDEN
- owner/self-report as sole MAIN approval;
- `blend + GLB + SHA + manifest = MAIN KEEP`;
- evidence correctness used to waive weak design;
- more receipts used to compensate for weak visual/form quality.

### EVIDENCE
`REVIEW_GATE_MATRIX` naming reviewer/system, evidence ids and result for each gate.

### FAIL
- `FAIL_GATE_COLLAPSE`
- `REVISE_DESIGN_QUALITY`
- `REJECT_DESIGN_QUALITY`
- `HOLD_INDEPENDENT_REVIEW_MISSING`

`Artifact existence ≠ Design quality`

`Traceability ≠ Professional finish`

`Evidence correctness ≠ Visual excellence`

`Process PASS ≠ MAIN KEEP`

---

## 14. Failure routing

### INPUT
Observed failure signature plus representation layer where it appears.

### MUST CHECK
Route to the lowest layer that actually owns the cause:

- wrong overall mass/silhouette → Source proportions / primary profiles;
- good silhouette, local reflection kink → existing sparse relation/profile control;
- failure only after tessellation/export → derived topology/export settings;
- good geometry, unreadable render → rig/camera/material;
- material hides dents → geometry diagnostic, disable masking detail;
- spatially plausible but unsupported scale → evidence/assumption correction;
- clean execution but weak design → independent Design Crit `REVISE/REJECT`;
- Source changed during diagnostic-only run → restore Source, invalidate affected evidence, rerun;
- comparison differs in multiple rig variables → repair rig lock before judging form.

### ALLOWED
- isolate with A/B tests;
- rollback and rerun;
- mark evidence invalid;
- escalate to Source-family expansion only after causal tests.

### FORBIDDEN
- fixing the most visible layer rather than causal layer;
- adding geometry when a render rig is the cause;
- relighting to hide Source defects;
- claiming root cause without a controlled isolation test.

### EVIDENCE
`FAILURE_ROUTE_RECEIPT` with symptom, observed layer, hypothesized owner layer, isolation test, chosen edit target, rejected edit targets and result.

### FAIL
`HOLD_ROOT_CAUSE_UNRESOLVED` if causality remains ambiguous after controlled isolation.

---

## 15. Completion condition

### INPUT
Requested task scope and all applicable section evidence.

### MUST CHECK
A 3D task is complete only to the requested level when:
1. actual editable/derived asset exists as required;
2. required evidence exists;
3. retained files can be reopened or machine-checked where possible;
4. Source/derived/diagnostic/render state boundaries remain intact;
5. machine, evidence and design conclusions are separately stated;
6. unresolved native-app, field, engineering, manufacturing or CMF proof is explicitly listed;
7. no missing requirement is disguised as a process PASS.

### ALLOWED
- partial completion with exact residual blockers;
- faithful editable fallback when a native app is unavailable;
- `EXECUTED` without `DESIGN KEEP`.

### FORBIDDEN
- stopping at “workflow established” when execution assets were requested;
- fabricated native-app PASS;
- background/asynchronous promises instead of current artifacts;
- MAIN promotion without the required independent design gate.

### EVIDENCE
`COMPLETION_RECEIPT` referencing all applicable receipts/assets and one explicit status per requested deliverable.

### FAIL
- `PARTIAL_REQUIRED_NATIVE_VALIDATION_MISSING`
- `PARTIAL_REQUIRED_ARTIFACT_MISSING`
- `HOLD_REQUIRED_REVIEW_MISSING`
- `FAIL_FALSE_COMPLETION_CLAIM`

---

## Cross-section invariant

At any point, if a lower-level gate passes but a higher-level claim is not proven, preserve the narrower result. Never widen it by implication.

Examples:
- Source digest unchanged → proves diagnostic non-mutation, **not** surface quality.
- Zebra lines improved → supports a reflection-flow observation, **not** Class-A certification.
- GLB round-trip succeeds → proves that exchange test, **not** Source validity.
- Render is attractive → proves presentation quality only if separately reviewed, **not** geometry correctness.
- FIELD=0 → does not stop design development, but field-dependent claims remain open.
