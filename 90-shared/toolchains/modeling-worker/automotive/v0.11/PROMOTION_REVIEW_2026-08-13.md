# OLEANDER Modeling Worker｜Automotive v0.11 Promotion Review

Date: 2026-08-13
System: `SYS-MODELING-WORKER`
Benchmark: `Automotive v0.11`
Candidate: `R29A｜Shoulder-Fed Monotonic Fender Crown`
Source hash: `d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

## Decision

`HOLD / PROMOTION_INTEGRATION_GATE / PERSISTENCE_GATE`

Authority remains:

`MODELING_WORKER_v0.11_CANDIDATE_AUTHORITY`

This is **not** a Modeling Quality REVISE and does not reopen M5–M10.

## Why this is not RE-ENTER

The validated production chain is intact:

- M5 Primary Geometry / Surface QA — PASS
- M6 Component Architecture — PASS
- M7 Secondary Geometry — PASS
- M8 Detail / Instances — PASS
- M9 Material Binding — PASS / NOT FINAL CMF
- M10 Multi-Scale QA — PASS

No current evidence identifies a geometry, topology, component-routing, secondary-geometry, instance, material-binding or multi-scale defect that requires reopening a passed gate.

Therefore the Candidate is retained exactly as validated.

## Why this cannot PROMOTE yet

### H1｜Mainline integration is not closed

At review time PR #85 is Draft and GitHub reports it as not mergeable.

The benchmark branch has diverged from `main`:

- branch ahead of main: 158 commits;
- branch behind main: 23 commits;
- current main: `3a1399655bf6bf40d1bf4fc55d37ef33bc4bd7e8`;
- merge base: `295d31cca5f8d7347bc05c4a3954e7bcc0bb2d98`.

The 23 newer main commits include governance changes to `00-governance/oleander-project-flow-v0.3.md`, namespace validation and related governance files. A Candidate may not be promoted against an outdated governance baseline when the current branch cannot yet enter main safely.

Classification:

`INTEGRATION HOLD / NOT MODELING REVISE`

### H2｜Production Asset Persistence Gate is triggered

Current `main` governance activates:

`00-governance/production-asset-persistence-gate-v1.0.md`

Its scope explicitly includes non-trivial native authoring binaries and canonical models such as `.blend` files.

Automotive v0.11 generated native Blender production scenes during M5–M10. The recorded evidence currently points to GitHub Actions artifacts with finite retention. Under PAP v1.0, expiring Actions artifacts, signed URLs, Markdown receipts and hashes are evidence only and are not a durable production copy.

Connected Google Drive search at Promotion Review did not locate an R29A / M10 durable binary object. Therefore a qualifying durable copy and independent retrieval verification are not currently evidenced.

Promotion status:

`PERSISTENCE FAIL / DURABLE PRODUCTION BINARY NOT YET VERIFIED`

This persistence classification does not revoke any M5–M10 design or execution evidence. It blocks Promotion only.

## HOLD exit conditions

Promotion may be reviewed again only after all of the following are true.

### E1｜Governance integration

- reconcile the branch with current `main`;
- resolve merge conflicts / integration incompatibilities;
- PR becomes mergeable against the current governance baseline;
- AI Governance and Blender Runtime Contract remain PASS after reconciliation.

### E2｜PAP asset inventory

Identify the required production set for the Candidate Authority:

1. native source / authoring binary — required `.blend`;
2. canonical interchange/model authority — provide a project-defined binary such as `.glb`, or explicitly record `N/A` with a governance-valid reason if the benchmark intentionally has no separate interchange authority;
3. immutable production ZIP;
4. checksum records for contents and production ZIP.

### E3｜Durable upload

Store every required binary in a PAP-qualified durable location with stable provider file/object IDs. Google Drive is acceptable.

### E4｜Independent retrieval and integrity

Re-download/re-materialize the durable copies and verify:

- SHA-256;
- byte size;
- ZIP open/test;
- `.blend` parse/open where practical;
- canonical model parse/open where applicable.

### E5｜Persistence manifest / receipts

Record PAP-G0—PAP-G6 evidence including provider, stable IDs, paths/references, retention class, upload/retrieval timestamps, expected/retrieved SHA and open-test status.

GitHub and Notion governance receipts must point to the same persistence manifest/status.

### E6｜Promotion decision

Only after E1–E5 pass may authority advance:

`CANDIDATE_AUTHORITY → CANONICAL_AUTHORITY`

Promotion then triggers the normal canonical Artifact Registry / GitHub / Notion / Drive synchronization required by the current OLEANDER flow.

## Locked during HOLD

The following remain locked and must not be changed merely to satisfy the Promotion HOLD:

- R29A Source geometry / Source hash;
- canonical 0.700 m wheel HP contract;
- M6 routing architecture;
- M7 secondary identities;
- M8 linked-instance families;
- M9 neutral benchmark material bindings;
- M10 Human PASS decision.

Any change to these is a separate Revision Proposal and may require the relevant modeling gate to re-enter.

## Final review state

`DESIGN STATE = CANDIDATE / HOLD_FOR_PROMOTION`

`AUTHORITY STATE = CANDIDATE_AUTHORITY`

`MODELING GATES = M5–M10 PASS / CLOSED`

`PROMOTION = BLOCKED BY INTEGRATION + PAP`

`PR #85 = DRAFT / DO NOT MERGE YET`

`NOTION / DRIVE CANONICAL PROMOTION SYNC = BLOCKED UNTIL PAP + INTEGRATION PASS`
