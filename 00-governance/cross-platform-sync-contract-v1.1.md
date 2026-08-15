# OLEANDER Cross-platform Sync Contract v1.1

Status: CURRENT / ACTIVE
Effective time: 2026-08-15T09:29:00+08:00
Owner: OLEANDER Governance
Source: user-governance-directive-2026-08-15T09:29:00+08:00
Source SHA-256: `82b02e0f01606ff31f45df3c12d66643b500f01bff80ddd11c8548a6b2b92cdf`
Supersedes: `cross-platform-sync-contract-v1.0.md`

## 0. Authority rule

**Chat summaries are not Project State, Current Task, Source Authority, Validation, Promotion, or Sync evidence.**

State changes must be persisted through the applicable OLEANDER authority surface and its receipt/readback chain. A chat may explain a persisted state, but it cannot create that state by narration.

At every layer, keep these facts distinct:

`Artifact ≠ Commit ≠ PR ≠ Validated ≠ Merged ≠ Promoted`

No later-stage claim may be inferred from an earlier-stage fact.

## 1. Material Delta Gate

Before any write, commit, PR, state receipt, or synchronization action, determine whether a **MATERIAL DELTA** exists.

- `MATERIAL DELTA = YES`: a real object/source/revision/state/decision/evidence change exists; the formal chain may open.
- `MATERIAL DELTA = NO`: do not write, do not commit, do not open a PR, and do not create performative sync noise.

Formatting-only churn, repeated status narration, duplicate receipts, and chat-only restatement are not material deltas unless they repair a real authority/state contradiction.

## 2. Owner Receipt / Run Manifest first

Every real artifact or governed state transition starts with an **owner receipt / run manifest** before cross-line synchronization.

Minimum binding:

- `object`
- `source`
- `revision`
- `time`
- `hash`
- `state`
- `does-not-prove`

The receipt must identify the owner, material-delta reason, intended persistence/validation chain, and authority boundary.

Owner receipt creation does not prove that the artifact exists, validates, syncs, merges, promotes, or releases.

After owner-side persistence/readback, the result is handed to **F cross-line readback**. F readback independently confirms the specified persisted object and state; it does not inherit owner claims without readback.

## 3. Text / schema / code / data GitHub chain

For text, schemas, code and data intended for GitHub authority or repository persistence, the required chain is:

`MATERIAL DELTA → Owner Receipt / Run Manifest → Branch → Artifact Write → Commit → PR → CI → Remote Readback → F Cross-line Readback`

Rules:

1. Write to a branch; do not treat a local or generated file as repository state.
2. A commit proves only that a commit object exists on the branch.
3. A PR proves only that a review/merge proposal exists.
4. CI PASS proves only the checks actually executed by that CI configuration.
5. Remote readback must bind the expected branch/head SHA/path/blob/content/state.
6. F cross-line readback must verify the persisted owner result against the declared object/source/revision/hash/state.
7. Merge and Promotion remain separate transitions with their own authority gates.

### GitHub status vocabulary

Use explicit states such as:

- `OWNER_RECEIPT_CREATED`
- `BRANCH_WRITTEN`
- `COMMITTED`
- `PR_OPEN`
- `CI_PASS` / `CI_FAIL`
- `REMOTE_READBACK_PASS` / `REMOTE_READBACK_FAIL`
- `F_READBACK_PASS` / `F_READBACK_FAIL`
- `MERGED`
- `PROMOTED`

Never collapse them into one generic `DONE` or `SYNCED` claim.

## 4. Native / binary production asset chain

Native models, renders, CAD, packaged websites, editable board sources, video masters and other non-text production assets require a **real recoverable binary/source copy**. Preview images, chat attachments, temporary sandbox files, expiring Actions artifacts, checksums without bytes, or prose descriptions are not sufficient substitutes.

Required minimum record for each governed binary/source asset:

- object / source / revision
- creation or export time
- application/runtime version
- file type
- exact byte size
- SHA-256
- dependencies and linked assets required to reopen/rebuild
- durable storage location / object ID
- independent retrieval result
- independent open / unzip / parse / load result
- state
- `does-not-prove`

Required chain:

`MATERIAL DELTA → Owner Receipt / Run Manifest → Generate Native/Production Asset → Local/Native Open Test → Version + Bytes + SHA256 + Dependency Manifest → Durable Upload → Independent Retrieval → Independent Open Test → Persistence Readback → F Cross-line Readback`

Production Asset Persistence Gate remains independently applicable; this contract does not weaken PAP-G0—PAP-G6 or artifact-specific review.

A render PASS does not prove a design PASS. A model opening successfully does not prove geometry/design/engineering validity. A packaged website opening does not prove deployment or field service validity.

## 5. Notion and Drive persistence

### Notion

`MATERIAL DELTA → Owner Receipt / Run Manifest → Canonical Target Check → Notion Write → Notion Readback → F Cross-line Readback`

A write response alone is not `SYNCED`.

### Google Drive

`MATERIAL DELTA → Owner Receipt / Run Manifest → Artifact/Source Open Test → Durable Drive Upload → Drive Readback → Independent Retrieval/Open Test when required → F Cross-line Readback`

For production binaries, Drive readback without byte/hash/open verification does not satisfy the Production Asset Persistence Gate.

## 6. Project State / Current Task

Dynamic progress, Decision, blocker, gate status and next-action changes must be recorded through **Project State / Current Task RECEIPT ONLY**, or the current canonical project-state mechanism where that project already has a more specific authority surface.

Do not create parallel narrative state files merely because a chat has new wording.

A dynamic receipt must bind the same minimum envelope:

`object / source / revision / time / hash / state / does-not-prove`

and must distinguish at least:

- Job State
- Design State
- Authority State
- Validation/Gate State
- Sync/Persistence State
- Promotion/Release State

## 7. One CURRENT per authority surface

Each governed surface may have only one `CURRENT` authority.

- new current object: `CURRENT / ACTIVE` only after its required validation/readback state is reached;
- previous current: `SUPERSEDED / HISTORY` or equivalent provenance state;
- old drafts/working states: `SUPERSEDED / HISTORY / REJECTED / ARCHIVED` as applicable;
- legacy/provenance material must not be revived merely because it is newer by filesystem timestamp or appears in search.

No parallel CURRENT files, pages, models, scene sources, or state records are permitted for the same authority question.

## 8. Failure and partial synchronization

Failure must remain visible.

Use:

- `UNSYNCED` when the required persistence/readback chain has not succeeded;
- `PARTIAL` when some required systems/gates have read back successfully and others have not;
- system-specific status when useful, e.g. `GITHUB READBACK PASS / DRIVE UNSYNCED / NOTION READBACK PASS`.

Do not use a successful result on one system to mask failure on another.

## 9. Cross-line readback rule

F cross-line readback is an independent synchronization/reconciliation step, not a second owner narrative.

F must verify, as applicable:

- object identity
- source identity
- revision
- observed time
- hash / blob SHA / binary SHA-256
- declared state
- CURRENT vs SUPERSEDED/HISTORY relationship
- failed/partial systems
- `does-not-prove`

If any bound field conflicts with owner receipt or persisted authority, record the result as `F_READBACK_FAIL` or `PARTIAL`; do not silently reconcile by prose.

## 10. Does-not-prove boundary

Every receipt/run manifest/readback must state what its evidence does **not** establish.

Common exclusions include, as relevant:

- artifact existence does not prove validation;
- commit does not prove PR/CI/merge;
- PR does not prove CI/merge;
- CI does not prove visual/design/field validation unless that exact gate ran;
- merge does not prove Promotion;
- render does not prove Design PASS;
- prototype does not prove Field PASS;
- persistence does not prove release rights or implementation feasibility.

## 11. Global OLEANDER boundary retained

Unless a separately authorized project transition changes them, the current research/prototype boundary remains:

- `FIELD OBSERVED = 0`
- `FIELD MEASURED = 0`
- `G1F = HOLD`
- `NO_PROMOTION`

This sync contract cannot itself lift Field, G1F, Promotion, Release, engineering, manufacturing, rights, safety or implementation gates.

## 12. Canonical sync principle

**No material delta, no write. No owner receipt, no governed run. No target-system readback, no sync claim. No F readback, no cross-line closure. No explicit Promotion transition, no Promotion.**
