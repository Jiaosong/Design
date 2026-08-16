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

`object_id` identifies the governed authority object; `source_id` identifies the exact source/candidate materialization. They are not interchangeable.

Provider order is search/materialization order, not authority rank. Discovery hits remain blocked until Authority Resolution is complete. `UNLOCATED / E0` is a resolution outcome, not an actionable-success exit.

### 2. Authority-bound gate receipts

Plain strings such as `"Machine QA": "PASS"` are insufficient. Required gate receipts bind:

`gate + result + basis + object_id + source_id + authority_sha256 + gate_version + receipt_id + executed_at + evidence_ref`

Two execution modes are explicit:

- `LIVE`: required Gate evidence must use `basis=DIRECT`; replay mappings are inadmissible.
- `REPLAY`: historical evidence may use `basis=REPLAY_MAPPING` when today’s generic Gate name did not exist in the historical record. Such mappings must retain the historical evidence label and cannot execute live post-promotion actions.

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

`Candidate evidence -> replay compatibility -> historical human promotion -> Canonical three-system semantic/freshness scan PASS`

The historical files explicitly support M5–M10 PASS/CLOSED, PAP PASS, Formal Promote Review PASS and Candidate-to-Promotion Execution. Current generic Gate names that are not present verbatim in those historical files are marked `REPLAY_MAPPING`; they are not rewritten as historical DIRECT evidence.

A successful replay returns `replay_only=true`, has no live `post_promotion_actions`, and therefore cannot mutate or promote current state.

### 6. Global NO COMPRESSION / NO LOSS preservation contract

The Control Plane now compiles `00-governance/OLEANDER_NO_COMPRESSION_NO_LOSS_POLICY_v1.0.md` into the existing Control Card rather than creating another Gate or parallel methodology.

For `problem_layer=Architecture`, `preservation_review` is mandatory. It records whether established project objects exist and, where they do, accounts for restructuring through three separate ledgers per object:

`concept_state + presentation_state + truth_evidence_state`

This makes the following machine-visible:

- `CONCEPT KEEP != PIXEL KEEP`;
- `PIXEL FAIL != DESIGN DELETE`;
- `VALIDATION SUBSET != WHOLE PROJECT`;
- `SOURCE / AUTHORITY != DERIVED PRESENTATION`.

Allowed actions remain project-specific and include `PRESERVE / REORDER / SPLIT / GROUP / REWEIGHT / REDRAW / DEMOTE_TO_SUPPORT / DEMOTE_TO_PROCESS / HOLD / CUT`.

Removal rules are fail-closed:

- established objects cannot be left unaccounted for;
- `DEMOTE_TO_SUPPORT` must end in `presentation_state=SUPPORT`;
- `DEMOTE_TO_PROCESS` must end in `presentation_state=PROCESS`;
- `CUT` requires `concept_state=DROP` so a weak pixel cannot silently delete a kept concept;
- compression, page count, cleaner presentation, shorter Web/film, less text or minimalism cannot be the sole removal reason.

`global_fixed_chapter_count_applied` is schema-locked to `false`. The machine contract therefore does **not** encode C04's 12-layer architecture, or any other project's chapter count, as a global template.

This is core validation, not a new system-level Gate. It does not decide which object deserves MAIN, does not manufacture evidence, and does not grant Promotion or Release.

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

Historical hardened baseline: `27/27 PASS` on PR #90 head validation. Any later regression count must be taken from the current CI run, not inferred from this historical baseline.
