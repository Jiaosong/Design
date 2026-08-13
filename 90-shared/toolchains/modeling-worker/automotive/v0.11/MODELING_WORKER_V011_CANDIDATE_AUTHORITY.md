# OLEANDER Modeling Worker｜Automotive v0.11 Candidate Authority

Authority state: `CANDIDATE_AUTHORITY / PAP_PASS / READY_FOR_PROMOTE_REVIEW / NOT PROMOTED / DRAFT PR`

Promotion review: `PROMOTION_REVIEW_2026-08-13.md`
PAP manifest: `PAP_MANIFEST_v1.json`
PAP receipt: `PAP_RECEIPT_2026-08-13.md`

## Canonical benchmark identity

System:
`SYS-MODELING-WORKER`

Benchmark:
`Automotive v0.11`

Primary Source candidate:
`R29A｜Shoulder-Fed Monotonic Fender Crown`

Canonical executed Source hash:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Wheel hard-point contract:
`wheel_hp_contract.py / OD 0.700 m`

## Passed gate chain

- M0 Decision Question — PASS
- M1 Hard Points — PASS after wheel-display implementation correction
- M2 Envelope / Package — retained
- M3 Section Network — retained
- M4 Primary Geometry — R29A current candidate
- M5 Construction & Surface QA — PASS
- M6 Component Architecture — PASS
- M7 Secondary Geometry — PASS
- M8 Detail / Instances — PASS
- M9 Material Binding — PASS / NOT FINAL CMF
- M10 Multi-Scale QA — PASS
- PAP-G0—PAP-G6 — PASS

## Load-bearing evidence

### M5
Run `31619362019`
Artifact `9150618297`
Digest `sha256:5fd16c8c38eb32a03c182bd86b0e11c558076536b17654eabe2cb79cecef9df0`

### M6
Run `31621035044`
Artifact `9151237407`
Digest `sha256:3ecb7c092a88b00ce3e96ffeb5359e241eb9b52829018239dcc90ca1dabd688e`

### M7
Run `31621603164`
Artifact `9151463754`
Digest `sha256:05b4136fac444e1b683d4f53c71bf1403ecec2a85f891a72577c913201945a97`

### M8
Run `31622289173`
Artifact `9151727429`
Digest `sha256:da85cf98a575b06bfe13e598541f6004a75aac91c910ae49d8ede5b125a74fe9`

### M9
Run `31622919537`
Artifact `9151984130`
Digest `sha256:ba3234f0e4912f41d42079fe50c873c7a9be237996f57eda574e21c852a82ee7`

### M10
Run `31623379139`
Artifact `9152168778`
Digest `sha256:01b39f726ff943f9db2bca2d089cd197a3b23ce35a7ca277c2740cfe0448e6ac`

## PAP durable authority evidence

Google Drive PAP root:
`1PLXbsvK81vLrfkcukaYD_Ks7P1SmLPk3`

Native Blender source:
- Drive ID `1KQP_SJU11teCutdBLDSaF1D29aD2Fp2H`
- size `248834` bytes
- SHA-256 `f8f800360a61392592262f89e3f6a6ca5ec6e76eda9211911530bd257939d8e1`
- independent retrieval PASS
- byte-identical to executed M10 Blender scene

Production ZIP:
- Drive ID `1xQhmz5_RBwfK5iQFODiIM2jFn_ZGJw4D`
- size `3861986` bytes
- SHA-256 `3dd304dd94e6493e01e1a4e436339949cc82851cef1ce007eacbf02f226ef204`
- independent retrieval PASS
- ZIP test PASS
- internal checksums PASS

Canonical interchange:
`N/A` — editable Blender Source is the benchmark Geometry Authority; no separate GLB/STEP/OBJ authority was created or validated.

Cross-system receipt:
- Drive manifest `1STqH_YWQ8o3jR3AzOSctkVdMuGyVmK-P`
- Drive receipt `1xyWEfsBd2H4Yayj8CxlfKf_fdsxJahoi`
- Notion page `3bbb86be-5c47-81c0-adf7-f9d8c5f16924`
- GitHub `PAP_MANIFEST_v1.json` + `PAP_RECEIPT_2026-08-13.md`

## Retained construction authority

- R09 rearward cabin / wheel package;
- R11 non-wheel transverse tension;
- R12 PCHIP-like longitudinal interpolation;
- R18 / R20 structured terminations;
- R25 rounded wheel-opening scale and shared-endpoint topology family;
- canonical 0.700 m wheel hard-point contract;
- R29A shoulder-fed crown relation;
- M6 routing IDs / dependencies;
- M7 secondary identities;
- M8 linked prototype/instance families;
- M9 neutral binding registry.

## Superseded / audit-only evidence

- v0.7 — execution benchmark only;
- v0.8 — working source / modeling quality revise;
- v0.9 / v0.10 — superseded audit only;
- R24 pointed local arch law;
- R26 lateral expansion-only solution;
- R27A-E circumferential attachment experiments;
- R28A-C full local U-boundary patch family;
- R29 inward-rising shelf relation;
- pre-HP-correction visual judgments materially affected by the incorrect ~1.0792 m wheel Z envelope.

## Explicit non-authority

This candidate does not claim:
- Class-A surfacing;
- automotive engineering CAD;
- validated structural / crash / aero performance;
- production panel architecture;
- tooling or assembly feasibility;
- supplier capability;
- homologation;
- final CMF.

## Current promotion state｜2026-08-13

The previous `HOLD / PERSISTENCE_GATE` is closed.

Current persistence classification:

`PERSISTENCE PASS / PAP-G0—PAP-G6 PASS`

No M5–M10 gate is reopened and Candidate Authority is not downgraded.

The next allowed action is a **new explicit Promote Review**. Before `CANDIDATE_AUTHORITY → CANONICAL_AUTHORITY`, recheck PR #85 mergeability, AI Governance Evals, Blender Runtime Contract, PAP consistency and the explicit non-authority boundary.

Until that decision:
- PR #85 stays Draft;
- no automatic merge;
- downstream reuse cites `CANDIDATE_AUTHORITY`, not `CANONICAL_AUTHORITY`;
- no final-CMF / engineering / manufacturing authority is implied.
