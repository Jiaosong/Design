# OLEANDER Modeling Worker｜Automotive v0.11 Canonical Authority Receipt

Date: 2026-08-13
System: `SYS-MODELING-WORKER`
Benchmark: `Automotive v0.11`
Authority object: `R29A｜Shoulder-Fed Monotonic Fender Crown`

## Promotion result

`DESIGN STATE = PROMOTED`

`AUTHORITY STATE = CANONICAL_AUTHORITY`

Promotion was executed by merging PR #85 into `main` after an immediate fail-closed recheck of the then-current mainline, PR mergeability, Candidate head and required CI.

Merge commit:
`1ee9d06a54e799a57835e761d32c706644792365`

Merge parents:
1. `eb310049a509d7c48a6bb55d3d1284566aec2908` — pre-promotion main
2. `1d5e3da965aa7e5e75d8c6cd523ea6f301798200` — approved Candidate head

## Locked authority chain

- Source geometry hash: `d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`
- canonical wheel hard-point contract: `OD 0.700 m`
- M5 Primary Geometry / Surface QA: PASS / CLOSED
- M6 Component Architecture: PASS / CLOSED
- M7 Secondary Geometry: PASS / CLOSED
- M8 Detail / Instances: PASS / CLOSED
- M9 Material Binding: PASS / CLOSED / `NOT_FINAL_CMF`
- M10 Multi-Scale QA: PASS / CLOSED

No modeling gate was reopened by Promotion.

## Production Asset Persistence

`PAP-G0—PAP-G6 = PASS`

Native Blender Source:
- Drive ID `1KQP_SJU11teCutdBLDSaF1D29aD2Fp2H`
- bytes `248834`
- SHA-256 `f8f800360a61392592262f89e3f6a6ca5ec6e76eda9211911530bd257939d8e1`
- independent retrieval PASS

Production ZIP:
- Drive ID `1xQhmz5_RBwfK5iQFODiIM2jFn_ZGJw4D`
- bytes `3861986`
- SHA-256 `3dd304dd94e6493e01e1a4e436339949cc82851cef1ce007eacbf02f226ef204`
- independent retrieval PASS
- ZIP open/test PASS
- internal SHA256SUMS PASS

Canonical interchange model remains `N/A`: this benchmark defines the editable Blender Source as Geometry Authority; no separate GLB/STEP/OBJ authority was validated.

## Promotion evidence

Immediate pre-merge state:
- main: `eb310049a509d7c48a6bb55d3d1284566aec2908`
- Candidate head: `1d5e3da965aa7e5e75d8c6cd523ea6f301798200`
- PR #85: `mergeable=true`
- AI Governance Evals run `31657734439`: SUCCESS
- OLEANDER Blender Runtime Contract run `31657734467`: SUCCESS

PR #85 merge result:
- `merged=true`
- merge commit `1ee9d06a54e799a57835e761d32c706644792365`

## Cross-system references

- Drive PAP root: `1PLXbsvK81vLrfkcukaYD_Ks7P1SmLPk3`
- Drive PAP manifest: `1STqH_YWQ8o3jR3AzOSctkVdMuGyVmK-P`
- Drive PAP receipt: `1xyWEfsBd2H4Yayj8CxlfKf_fdsxJahoi`
- Notion PAP receipt: `3bbb86be-5c47-81c0-adf7-f9d8c5f16924`
- Notion Promote Review receipt: `3bbb86be-5c47-81e7-93a3-e28aba991475`
- GitHub PR: `#85`

## Authority boundary

This Canonical Authority is limited to the generic OLEANDER Modeling Worker benchmark authority established by the validated evidence.

It does not claim:
- Class-A automotive surfacing;
- automotive engineering CAD;
- structural / crash / aero validation;
- production panel architecture;
- tooling / assembly feasibility;
- supplier capability;
- homologation;
- final CMF.

`M9` remains a neutral benchmark material-binding mechanism only.

## Canonical state

`R29A = CANONICAL_AUTHORITY`

`Automotive v0.11 = PROMOTED`

`M5–M10 = PASS / CLOSED`

`PAP = PASS`

Future changes must enter a new Decision Question and follow the applicable Re-enter / Candidate / Promotion gates; they must not silently mutate this authority object.