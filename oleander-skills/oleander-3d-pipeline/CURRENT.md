# OLEANDER 3D Pipeline — CURRENT Routing

Status: `CANDIDATE_SYNC / NO_PROMOTION / 2026-08-20`

Integration PR: **#293 — OLEANDER 3D: currentize Skill, camera gate, and cross-system routing**

https://github.com/Jiaosong/Design/pull/293

This file is the stable routing index for the OLEANDER 3D Skill. It prevents old version reports, newer timestamps, stacked PRs, or Drive snapshots from being mistaken for the single CURRENT execution authority.

## Authority order

`OLEANDER Current Authority → Project State → Source Authority → Current Task → oleander-3d-pipeline → selected specialist/runtime adapter`

`Source Authority ≠ Derived Execution ≠ Diagnostic Evidence ≠ Render Evidence ≠ Design Quality ≠ Field / Engineering / Manufacturing Proof`.

## Installed owner

- Skill ID: `oleander-3d-pipeline`
- Human execution contract: `oleander-skills/oleander-3d-pipeline/SKILL.md`
- Capability contract: `oleander-skills/oleander-3d-pipeline/CAPABILITY.json`
- Visual evidence binding: `oleander-skills/oleander-3d-pipeline/VISUAL_LAYER_BINDING.md`
- Machine routing pointer: `oleander-skills/oleander-3d-pipeline/CURRENT.json`

## Current candidate Skill deltas validated on this integration branch

### 1. Stage Capability Routing

Files:
- `STAGE_CAPABILITY_ROUTING_PROTOCOL_v1.md`
- `contracts/STAGE_CAPABILITY_ROUTING_CONTRACT_v1.json`
- `tools/validate_stage_capability_routing.py`
- `00-governance/control-plane/tests/test_oleander_3d_stage_capability_routing.py`

Core rule:

`STAGE → SEMANTIC CAPABILITIES → CONSUMER REQUIREMENTS → EVIDENCE`

A consumer requests a semantic capability rather than a historical Blender object name. Current-stage capabilities may be `AVAILABLE`; intentionally deferred later-stage capabilities may be `NOT_APPLICABLE_STAGE_HOLD`; required missing capabilities fail closed. Required and held sets must be disjoint.

Benchmark provenance: Porsche 911 992.2 V47→V48 in PR #208. A primary-form stage legally held final aperture architecture, while inherited consumers still assumed historical windshield objects and later-stage metrics. The generic routing repair passed AI Governance + Control Plane on PR #293.

### 2. Evidence Carrier Congruence

Files:
- `EVIDENCE_CARRIER_CONGRUENCE_PROTOCOL_v1.md`
- `contracts/EVIDENCE_CARRIER_CONGRUENCE_CONTRACT_v1.json`
- `tools/validate_evidence_carrier_congruence.py`
- `00-governance/control-plane/tests/test_oleander_3d_evidence_carrier_congruence.py`

Core rule:

`CLAIM → REQUIRED CARRIER SCOPE → REFERENCE CARRIER → CANDIDATE CARRIER → METRIC`

A numerically valid measurement cannot support a wider/different claim when the carriers are semantically mismatched. Whole-visible, primary-shell, aperture/interface, local-context and detail carriers remain distinct. A visual proxy may pass only for an explicitly bounded proxy claim and must retain does-not-prove boundaries.

Benchmark provenance: Porsche 911 V51→V54 carrier audit. A whole-vehicle FRONT/REAR profile target and a body-only candidate carrier produced materially different readings; the repair preserves both results instead of overwriting history. This does not make the proxy a final aperture/reference authority.

### 3. Semantic claim → matching evidence

Identity or construction relations must be bound to evidence that actually evaluates the named relation. A broad/profile proxy cannot be relabeled into a narrower semantic claim.

Hard example exposed by the Porsche benchmark:

`FRONT gross-profile PASS ≠ HOOD–FENDER HIERARCHY SCREENED`

A hood-center / fender-crown claim requires a direct final-surface relation metric or equivalent controlled evidence. If that evidence is absent, the semantic relation remains `HOLD` and machine identity cannot self-promote.

### 4. Quality-state / runtime-health separation

An honest `PROJECTION_MACHINE_SCREENING_FAIL`, `REFERENCE_FIDELITY_REJECT`, or Design `REVISE/REJECT` is not itself a broken runtime. CI fails for invalid execution/evidence/provenance or false promotion; a weak design remains recorded as the quality result.

### 5. Blender 5.2 LTS Runtime Contract｜2026-08-19 training delta

Files:
- `BLENDER_5_2_LTS_RUNTIME_PROTOCOL_v1.md`
- `contracts/BLENDER_RUNTIME_CONTRACT_v1.json`
- `tools/validate_blender_runtime.py`
- `00-governance/control-plane/tests/test_oleander_blender_runtime_contract.py`
- expanded `evals/evals.json` with Blender 5.2 runtime / CMF / Asset Library / Geometry Nodes / color pipeline / I/O / migration failure tests.

Core rule:

`CLAIM → SOURCE STATE → BLENDER VERSION / BUILD / PLATFORM / DEVICE → EXTENSIONS / DEPENDENCIES → PROCEDURAL STATE → COLOR PIPELINE → ENGINE / DEVICE → I/O CAPABILITY → OUTPUT READBACK → MACHINE / EVIDENCE / DESIGN STATUS`

The contract closes runtime gaps that the general 15-section Skill did not bind strongly enough: exact Blender version and runtime identity; color-management drift; remote Asset Library / Packed Data recoverability; Geometry Nodes and simulation state; Cycles / EEVEE and denoise/postprocess comparison boundaries; actual I/O operator/bridge verification; headless/script execution logs and output readback.

Machine validation evidence on commit `038d0e574f6ebc9399286113169d022d7849134b`:
- AI Governance Evals workflow run `32267478540`: **SUCCESS**.
- OLEANDER Control Plane v0.3 workflow run `32267479047`: **SUCCESS**.
- Control Plane unit/regression suite: **69 tests PASS**, including all **8** `test_oleander_blender_runtime_contract` cases.

Current contract state: `CANDIDATE_CONTRACT_MACHINE_VALIDATED`.

The current ChatGPT agent container still has no local Blender executable, so it has no local Blender runtime receipt. However, the Porsche benchmark supplies independent external execution provenance from GitHub Actions: PR #208 run `32271258341` executed V58 and V59 under **Blender 5.2.0 LTS**, persisted native `.blend` + JSON + six-view renders, and produced artifact digest `sha256:49a709070d18b4053d7a50927e8184cb2b7d54dde6b6b655dc089593e42caa64`. This is benchmark execution evidence; it does not silently close every field of the generic Blender runtime contract.

Blender 5.2 LTS is the preferred baseline for new work as of 2026-08-19, but project-pinned Blender 4.5 LTS or another verified version remains valid when compatibility/dependency evidence requires it. Version recency does not overwrite an established production environment.

Hard boundaries:
- no network-only required Blender dependency in CURRENT production;
- no generic format list used as proof of a working Blender import/export operator;
- no Geometry Nodes/physics visualization promoted to ergonomic, engineering, manufacturing, or physical truth;
- no AgX/ACES/view-transform drift inside a controlled CMF/surface comparison;
- no CI/contract PASS promoted to actual target-script execution or Design PASS.

### 6. Benchmark Execution Evidence｜2026-08-19 training delta

Files:
- `BENCHMARK_EXECUTION_EVIDENCE_PROTOCOL_v1.md`
- `contracts/BENCHMARK_EXECUTION_EVIDENCE_CONTRACT_v1.json`
- `tools/validate_benchmark_execution_evidence.py`
- `00-governance/control-plane/tests/test_oleander_3d_benchmark_execution_evidence.py`

Core separation:

`IMPLEMENTED ≠ INVOKED ≠ EXECUTED ≠ RECEIPT_VALID ≠ EXPERIMENT_SUCCESS ≠ EVIDENCE_PASS ≠ DESIGN_PASS`

PR #208 exposed the gap directly: `run_reference_repro_v59.py` existed in the branch while the Porsche workflow still executed only V58. A green workflow therefore could not be cited as V59 runtime evidence. Commit `5db053b1a07b9fef824b77cb2d20e5838502f3ca` repaired the benchmark workflow to invoke V59 explicitly under Blender 5.2, bind the exact target revision, read back receipts, keep the V49/V58 baseline separate, and retain negative/held design outcomes without rewriting them as infrastructure failures.

Machine validation:
- OLEANDER Control Plane v0.3 run `32271427551`: **SUCCESS**.
- AI Governance Evals run `32271427517`: **SUCCESS**.
- 7 benchmark-execution contract tests.

### 7. Derived Edit Host Preservation｜V60 negative benchmark

Files:
- `DERIVED_EDIT_HOST_PRESERVATION_PROTOCOL_v1.md`
- `contracts/DERIVED_EDIT_HOST_PRESERVATION_CONTRACT_v1.json`
- `tools/validate_derived_edit_host_preservation.py`
- `00-governance/control-plane/tests/test_oleander_3d_derived_edit_host_preservation.py`

Core separation:

`OPERATOR_APPLIED ≠ GEOMETRY_CHANGED ≠ LOCAL_EDIT_SUCCEEDED ≠ HOST_PRESERVED ≠ DESIGN_PASS`

Porsche V60 is retained as the decisive negative case: a rear-glass Boolean reported applied + geometry changed while reducing the Derived host from **8,637 faces to 96**. The experiment is valid evidence but the candidate is REJECT.

The gate requires task-specific before/after host witness, protected invariants, Source mutation boundary and preservation budget. Repeated destructive failure must escalate from operator tuning to representation/topology/architecture diagnosis rather than keep changing solver/tolerance.

Machine validation:
- Control Plane run `32272492254`: **SUCCESS**.
- AI Governance run `32272492192`: **SUCCESS**.
- 8 host-preservation regression tests.

### 8. Measurement Coverage Sufficiency｜V59 / V64 training delta

Files:
- `MEASUREMENT_COVERAGE_SUFFICIENCY_PROTOCOL_v1.md`
- `contracts/MEASUREMENT_COVERAGE_SUFFICIENCY_CONTRACT_v1.json`
- `tools/validate_measurement_coverage_sufficiency.py`
- `00-governance/control-plane/tests/test_oleander_3d_measurement_coverage_sufficiency.py`

Core separation:

`CARRIER_CONGRUENT ≠ MEASUREMENT_COVERAGE_SUFFICIENT ≠ CLAIM_PROVEN ≠ DESIGN_PASS`

V59 demonstrated the false-promotion risk directly: SIDE top-envelope RMSE ≈ **13.9 mm** while FRONT body-only ≈ **0.1503**, REAR ≈ **0.1724**, and held-out 3/4 identity remained unacceptable. The SIDE metric is kept as a valid narrow screen, not whole-form reference fidelity.

V64 strengthened the rule: REAR body-only RMSE improved from ≈ **0.1724 → 0.0773**, Source stayed at 20 controls and 0 folds, and SIDE/front locks held; actual rear/rear-3Q preview nevertheless developed a pinched double-ridge C-pillar→haunch relation. V64 is `REJECT_EXPERIMENT_KEEP_EVIDENCE`, proving target-metric improvement does not establish correct relation ownership or Design PASS.

Machine validation:
- Control Plane run `32274708308`: **SUCCESS**.
- AI Governance run `32274708322`: **SUCCESS**.
- 7 measurement-coverage regression tests.

### 9. Destructive Edit Preflight｜V63–V69 training delta

Files:
- `DESTRUCTIVE_EDIT_PREFLIGHT_PROTOCOL_v1.md`
- `contracts/DESTRUCTIVE_EDIT_PREFLIGHT_CONTRACT_v1.json`
- `tools/validate_destructive_edit_preflight.py`
- `00-governance/control-plane/tests/test_oleander_3d_destructive_edit_preflight.py`

Core separations:

`PREDICATE_MATCH ≠ EXCLUSIVE_OWNER ≠ SAFE_TO_EDIT ≠ EDIT_SUCCEEDED ≠ HOST_PRESERVED ≠ DESIGN_PASS`

`FIRST_MATCH_CODE_ORDER ≠ SEMANTIC_OWNERSHIP`

`PRIMITIVE_STRADDLES_CANONICAL_BOUNDARY → SPLIT_OR_PARTITION_BEFORE_OWNER_ASSIGNMENT`

V63 introduced fail-closed preflight before deletion. V65 proved the apparently missing rear-glass target actually overlapped the host; V66 then exposed multi-owner predicate conflict. V67 showed the deeper topology problem: inside the rear cut band there were **12 rear-interior faces, 48 exterior faces and 56 faces straddling the canonical lateral boundary**. Whole-face owner assignment is therefore invalid until topology is partitioned.

V69 is the first positive representation result from this branch: a Derived-only piecewise boundary split reduced rear lateral straddles **56 → 0** while Source remained V59, world bounds had **0 drift**, folds stayed **0 → 0**, and non-manifold edges stayed **0 → 0**. This is a representation/topology PASS only; it does not prove aperture closure or reference fidelity. V70 continues the full-loop XZ boundary audit before any deletion is allowed.

Machine validation of the reusable gate:
- base preflight: Control Plane `32276586424` / AI Governance `32276586566`: **SUCCESS**;
- boundary-straddle extension: Control Plane `32277088247` / AI Governance `32277088269`: **SUCCESS**;
- current destructive-preflight test suite: 11 regression cases.

Skill eval set is now 15 cases; the canonical-boundary-straddle eval passed Control Plane `32277434711` and AI Governance `32277434724`.

## Merged / CURRENT-compatible baseline

- Repository: `Jiaosong/Design`
- Integration base main SHA at sync start: `b18f90b67c039485df234d74c3a4530e2295b382`
- Merged reusable Blender Surface System: `90-shared/toolchains/blender-surface-system/v1.20.0/`
- Shared Blender runtime remains capability-probed per run; no local executable path is permanent authority.

## Candidate extensions — do not silently promote

- PR #173 — Blender Surface System v1.21 Source-aware adapter + receipt/validator layer. `OPEN / DRAFT / CANDIDATE`.
- PR #198 — real R29A refined-Skill Blender validation. `OPEN / DRAFT / MACHINE-EXECUTION EVIDENCE`, not Design KEEP.
- PR #208 — Porsche 911 reference-reproduction benchmark and specialist protocol set. `OPEN / DRAFT / CANDIDATE SPECIALIST EXTENSION`; reference fidelity/design approval remain separate. Current training has reached V70 full-boundary audit; V59 remains the primary-body rollback/LKG while aperture representation is trained.
- PR #227 — Camera Claim Gate provenance; reusable rule incorporated here.
- PR #276 — interaction/lifecycle visual-gate provenance; reusable rules incorporated into `VISUAL_LAYER_BINDING.md`.
- Modeling Worker v0.13 remains a working/revise candidate chain and does not overwrite current Source Authority by recency.

## Specialist routing

Before detailed geometry, classify the task:
- reference reconstruction → reference-reproduction protocols;
- original product/form → structure-to-form route;
- landscape/architecture/site → spatial evidence and terrain/assembly route;
- mixed problems → explicit hybrid route.

Candidate specialist files in PR #208 do not become CURRENT merely because this index mentions them.

## Notion CURRENT owner

`SYS-BLENDER-SURFACE｜OLEANDER Blender Surface System`

https://app.notion.com/p/3bab86be5c4781949361f389b3ec102d?pvs=204

The old v1.16 Practice page previously used as `Canonical 入口` is deleted/legacy and must not be used as the current entry.

## Google Drive shared runtime root

Folder:
https://drive.google.com/drive/folders/1DbSzwAkEV1gA0VRs_Mv2VFar9TzlCJew

Stable README:
https://drive.google.com/file/d/1CL6if6pL0Cy__TDOdmEGMdWnPdoQ_p1z/view?usp=drivesdk

Drive versioned v1.18/v1.20 reports remain immutable provenance. No v1.21 CURRENT Drive record is fabricated.

## Link discipline

1. CURRENT pointers live in this file, `CURRENT.json`, the Notion P2 owner and stable Drive README.
2. Versioned receipts never become CURRENT by timestamp alone.
3. Deleted Notion Practice pages cannot be Canonical entry points.
4. Candidate PR links carry candidate/draft state.
5. A better execution method does not change project/Source Authority or Design State by implication.
6. After merge/currentization, update all four pointers in one synchronization pass.

## Does not prove

This routing repair and Blender training delta do not prove professional design quality, Class-A continuity, manufacturer CAD fidelity, physical CMF, usability, field geometry, engineering validity, manufacturability, or MAIN KEEP. External CI benchmark execution is evidence only for the exact invoked revision/runtime/output scope recorded by its receipt.