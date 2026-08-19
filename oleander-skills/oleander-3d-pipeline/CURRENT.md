# OLEANDER 3D Pipeline — CURRENT Routing

Status: `CANDIDATE_SYNC / NO_PROMOTION / 2026-08-19`

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

## Merged / CURRENT-compatible baseline

- Repository: `Jiaosong/Design`
- Integration base main SHA at sync start: `b18f90b67c039485df234d74c3a4530e2295b382`
- Merged reusable Blender Surface System: `90-shared/toolchains/blender-surface-system/v1.20.0/`
- Shared Blender runtime remains capability-probed per run; no local executable path is permanent authority.

## Candidate extensions — do not silently promote

- PR #173 — Blender Surface System v1.21 Source-aware adapter + receipt/validator layer. `OPEN / DRAFT / CANDIDATE`.
- PR #198 — real R29A refined-Skill Blender validation. `OPEN / DRAFT / MACHINE-EXECUTION EVIDENCE`, not Design KEEP.
- PR #208 — Porsche 911 reference-reproduction benchmark and specialist protocol set. `OPEN / DRAFT / CANDIDATE SPECIALIST EXTENSION`; reference fidelity/design approval remain separate. V47 onward is being used to failure-test stage routing, representation selection, sparse-source/dense-evaluation separation, gate-local baselines, semantic identity evidence, carrier congruence and fold localization/repair.
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

This routing repair does not prove professional design quality, Class-A continuity, manufacturer CAD fidelity, physical CMF, usability, field geometry, engineering validity, manufacturability, or MAIN KEEP.
