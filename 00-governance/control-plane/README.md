# OLEANDER Project Control Plane v0.3

Status: `v0.2 EXECUTABLE CORE / MERGED` + `v0.3 HARDENED ORCHESTRATION CANDIDATE / REVIEW`

This directory is subordinate to `00-governance/README.md` and `OLEANDER Current Authority v1.1.0`. It compiles and orchestrates existing governance; it does not create a second authority and never makes the final human Candidate/Canonical/Release decision.

## v0.2 executable core

- Project Control Card validation;
- Context / namespace resolution;
- EXPLORE / CANDIDATE / AUTHORITY gate-profile routing;
- CB-01 repeated-revise breaker;
- local/registry asset-locator primitive.

The checked-in `control-card.schema.json` is now enforced by the executable validator. Schema presence without runtime enforcement is not accepted.

## v0.3 hardened orchestration

### 1. Authority-bound provider receipts

Authority resolution and materialization are separate. A GitHub/Drive/File Library/runtime hit is actionable only when it matches the resolved authority binding:

`object_id + source_id + authority_state + SHA (when available)`

Provider order is search/materialization order, not authority rank. Discovery hits remain blocked until Authority Resolution is complete. `UNLOCATED / E0` is a resolution outcome, not an actionable-success exit.

### 2. Authority-bound gate receipts

Plain strings such as `"Machine QA": "PASS"` are insufficient. Required gate receipts bind:

`gate + result + object_id + source_id + authority_sha256 + gate_version + receipt_id + executed_at + evidence_ref`

Open/blocked/unknown evidence cannot be hidden by omitting a claim type during Promotion.

### 3. Explicit Promotion transition

Every Promotion declares an allowed transition:

- `WORKING_SOURCE -> CANDIDATE_AUTHORITY`
- `CANDIDATE_AUTHORITY -> CANONICAL_AUTHORITY`
- `CANONICAL_AUTHORITY -> FROZEN_AUTHORITY`
- `CANONICAL_AUTHORITY -> RELEASED` while retaining Canonical authority state

Machine completion stops at `READY_FOR_HUMAN_DECISION`.

### 4. Semantic / freshness contradiction scan

Notion / GitHub / Drive snapshots are checked for:

- object identity;
- snapshot freshness;
- revision binding;
- payload hash binding of `fields + semantic + revision`;
- expected state fields;
- explicit semantic assertions.

Field consistency alone is not enough.

### 5. PR #85 immutable replay

`replays/` contains the Automotive v0.11 R29A promotion replay grounded in existing PR #85 / Canonical Authority evidence. It verifies:

`Candidate evidence -> READY_FOR_HUMAN_DECISION -> historical human promotion -> Canonical three-system semantic/freshness scan PASS`

Replay mappings do not rewrite historical gate names or create new historical claims.

## Commands

```bash
python 00-governance/control-plane/control_plane.py check CARD.json
python 00-governance/control-plane/orchestrator.py providers PROVIDER_RECEIPTS.json
python 00-governance/control-plane/orchestrator.py promotion CARD.json GATE_RECEIPTS.json
python 00-governance/control-plane/orchestrator.py contradictions MANIFEST.json
```

## Non-negotiable boundaries

- `Machine PASS != Design PASS`.
- `Executed != Validated`.
- `Provider FOUND != Authority resolved` unless exact authority binding passes.
- `Cross-system consistent != Physical / Field / Human / Rights / Engineering validated`.
- Derived artifacts cannot replace Source Authority.
- Human judgment owns Candidate retention, root-cause confirmation, Locked Variable reopening and Canonical/Release decisions.
- No new system-level Gate is introduced here.

## Tests

```bash
python -m unittest discover -s 00-governance/control-plane/tests -p 'test_*.py' -v
python 00-governance/control-plane/orchestrator.py promotion 00-governance/control-plane/replays/pr85-control-card.json 00-governance/control-plane/replays/pr85-gate-receipts.json
python 00-governance/control-plane/orchestrator.py contradictions 00-governance/control-plane/replays/pr85-contradiction-manifest.json
```
