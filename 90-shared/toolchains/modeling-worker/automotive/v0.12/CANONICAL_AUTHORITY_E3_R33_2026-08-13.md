# OLEANDER Modeling Worker v0.12｜E3 R3.3｜Canonical Authority Receipt

Status: `CANONICAL_AUTHORITY / PROMOTED / CROSS_SYSTEM_SYNC_PENDING / NOT RELEASED`.

Object: `SYS-MODELING-WORKER-v0.12-E3-AUTO`.

## Promotion basis

- PR #91 merged Candidate Authority into `main` at `b83419c6d34e4a16413fc8d79cd289981f24741a`.
- Post-Merge Readback / Receipt Closure: PASS.
- R3.3 Machine / Visual / Project QA: PASS.
- PAP-G0—G6: PASS.
- Candidate Authority GitHub / Notion / Drive readback: PASS.
- Canonical Promotion Review: PASS.

## Authority transition

This receipt travels with the dedicated Canonical Promotion PR. The transition becomes executed only when that PR is merged into `main`.

Target transition:
`CANDIDATE_AUTHORITY / CANDIDATE → CANONICAL_AUTHORITY / PROMOTED`.

Control Plane target:
`mode=AUTHORITY`; `authority_source.state=CANONICAL_AUTHORITY`.

## Source binding

- accepted R3.3 source snapshot: `5782c039562e723705b6f46537fea7efa0936b29`.
- integrated Candidate merge: `b83419c6d34e4a16413fc8d79cd289981f24741a`.
- native Blender SHA-256: `3d49b6ece3272781e42521e2420f609fc5b608387d1ab9a166cecbdbb5ddf430`.
- Production ZIP SHA-256: `96a4601b458c9c6bf6872627ebf176ce04db50d5b386b44b3917aaaf4d1ef7b4`.
- PAP root: `1NqK4452BlZom84nX8UdmJh4Ga1GUcrWd`.

## Supersession

Automotive v0.11 remains immutable historical Canonical Authority evidence for its validated benchmark state. After this transition completes, Modeling Worker v0.12 becomes the current system authority; v0.11 is superseded as current authority but is not deleted or rewritten.

## Required immediate closure

After merge of the Canonical Promotion PR:
1. create and read back Notion Canonical Authority receipt;
2. create and read back Drive Canonical Authority receipt inside the v0.12 PAP root;
3. write GitHub Canonical Authority cross-system sync receipt;
4. run post-Canonical semantic/freshness contradiction scan;
5. update this receipt with the executed promotion merge SHA and cross-system receipt IDs.

## Boundary

This authority is limited to the validated OLEANDER Modeling Worker v0.12 relationship-driven freeform-surface benchmark and E3 R3.3 application-benchmark scope.

It does not establish Class-A automotive surfacing, engineering CAD, crash/aero validity, manufacturing/tooling feasibility, supplier capability, homologation, final Automotive styling, final CMF, Release, or GLB/STEP/OBJ interchange authority.