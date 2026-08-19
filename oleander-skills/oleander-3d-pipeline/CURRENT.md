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

### Stage Capability Routing

Files:
- `oleander-skills/oleander-3d-pipeline/STAGE_CAPABILITY_ROUTING_PROTOCOL_v1.md`
- `oleander-skills/oleander-3d-pipeline/contracts/STAGE_CAPABILITY_ROUTING_CONTRACT_v1.json`
- `oleander-skills/oleander-3d-pipeline/tools/validate_stage_capability_routing.py`
- `00-governance/control-plane/tests/test_oleander_3d_stage_capability_routing.py`

Core rule:

`STAGE → SEMANTIC CAPABILITIES → CONSUMER REQUIREMENTS → EVIDENCE`

A consumer must request a semantic capability rather than a historical Blender object name. Current-stage capabilities may be `AVAILABLE`; intentionally deferred later-stage capabilities may be `NOT_APPLICABLE_STAGE_HOLD`; required missing capabilities fail closed. Required and held capability sets must be disjoint.

This delta was exposed by the Porsche 911 992.2 V47→V48 benchmark in PR #208: primary-form evidence was valid while final aperture architecture was intentionally HOLD, but inherited projection/regression consumers still assumed historical windshield objects and later-stage metric sets. The generic routing repair passed AI Governance + Control Plane tests on PR #293. The Porsche benchmark remains provenance/candidate evidence; it is not Design KEEP.

### Quality-state / runtime-health separation

An honest `PROJECTION_MACHINE_SCREENING_FAIL`, `REFERENCE_FIDELITY_REJECT`, or Design `REVISE/REJECT` is not by itself a broken runtime. CI should fail for invalid execution/evidence/provenance or false promotion, while quality-state failure remains recorded as the quality result.

## Merged / CURRENT-compatible baseline

- Repository: `Jiaosong/Design`
- Integration base main SHA at sync start: `b18f90b67c039485df234d74c3a4530e2295b382`
- Merged reusable Blender Surface System: `90-shared/toolchains/blender-surface-system/v1.20.0/`
- Shared Blender runtime remains capability-probed per run; no local executable path is permanent authority.

## Candidate extensions — do not silently promote

- PR #173 — Blender Surface System v1.21 Source-aware adapter + 15-section receipt/validator layer. `OPEN / DRAFT / CANDIDATE`, stacked on Modeling Worker v0.13.
- PR #198 — real R29A Blender replay/detail validation of the refined 3D Skill. `OPEN / DRAFT / MACHINE-EXECUTION EVIDENCE`, not Design KEEP.
- PR #208 — Porsche 911 reference-reproduction benchmark and large specialist protocol set. `OPEN / DRAFT / CANDIDATE SPECIALIST EXTENSION`; reference fidelity/design approval remains separate. V47→V50 is being used to failure-test stage routing, representation selection, profile inversion, evaluated-grid density and held-out visual review.
- PR #227 — Camera Claim Gate training delta. The reusable gate is incorporated into PR #293; PR #227 remains provenance/training evidence until separately resolved.
- PR #276 — interaction-cue escalation + lifecycle evidence framing training delta. The reusable gates are incorporated into PR #293 `VISUAL_LAYER_BINDING.md`; PR #276 remains provenance/training evidence until separately resolved.
- Modeling Worker v0.13 remains a working/revise candidate chain and does not overwrite current Source Authority by recency.

## Specialist routing

Before detailed geometry, classify the task:

- reference reconstruction → reference-reproduction specialist protocols when current/available;
- original product/form → structure-to-form route when current/available;
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

Drive versioned v1.18/v1.20 sync reports remain immutable provenance. At the time of this sync, no v1.21 CURRENT Drive record was found; do not fabricate one.

## Link discipline

1. CURRENT pointers live in this file, `CURRENT.json`, the Notion P2 owner, and the stable Drive README.
2. Versioned receipts/reports never become CURRENT just because their timestamp is newer.
3. Deleted Notion Practice pages may remain historical references only; they cannot be `Canonical 入口`.
4. Candidate PR links must carry their candidate/draft state.
5. A branch or PR may introduce a better execution method without changing project/Source Authority or Design State.
6. After merge/currentization, update all four pointers in the same synchronization pass.

## Does not prove

This routing repair does not prove professional design quality, Class-A continuity, manufacturer CAD fidelity, physical CMF, usability, field geometry, engineering validity, manufacturability, or MAIN KEEP.
