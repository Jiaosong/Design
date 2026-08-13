# OLEANDER Modeling Worker｜Automotive v0.11 Candidate Authority

Authority state: `CANDIDATE_AUTHORITY / HOLD_FOR_PROMOTION / NOT PROMOTED / DRAFT PR`

Promotion review: `PROMOTION_REVIEW_2026-08-13.md`

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

## Promotion review result｜2026-08-13

Decision:

`HOLD / PERSISTENCE_GATE`

The HOLD does **not** reopen M5–M10 and does not downgrade the Candidate Authority.

Current integration state is not a blocker: PR #85 is Draft but GitHub currently reports it as mergeable, and the latest AI Governance Evals and Blender Runtime Contract are PASS. The branch remains 23 commits behind current `main`; final mergeability and CI must be rechecked immediately before Promotion, but this does not require a modeling re-entry.

Promotion is blocked because current `main` activates `Production Asset Persistence Gate v1.0`; Automotive v0.11 generated native `.blend` production assets, while the recorded production binaries remain represented by expiring GitHub Actions artifacts rather than a PAP-qualified durable copy with independent retrieval verification.

Connected Google Drive search during Promotion Review did not locate an R29A / M10 durable production binary.

Current persistence classification:

`PERSISTENCE FAIL / DURABLE PRODUCTION BINARY NOT YET VERIFIED`

Promotion may be reviewed again only after the exit conditions in `PROMOTION_REVIEW_2026-08-13.md` are closed: PAP asset inventory, durable upload, independent retrieval + SHA/size/open verification, aligned GitHub/Notion persistence receipts, followed by a final mergeability/CI check.

Until then:
- PR #85 stays Draft;
- no automatic merge;
- no canonical Notion/Drive promotion sync;
- downstream reuse must cite `CANDIDATE_AUTHORITY`, not `CANONICAL_AUTHORITY`;
- R29A Source and M5–M10 passed gates remain locked unless a separate Revision Proposal explicitly reopens them.
