# OLEANDER Project Control Plane v0.3

Status: `v0.2 REPLAY-COMPATIBLE CORE` + `v0.3 CURRENT EXECUTION CONTRACT / HARDENED ORCHESTRATION`

This directory is subordinate to `00-governance/README.md` and `OLEANDER Current Authority v1.1.0`. It compiles and orchestrates existing governance; it does not create a second authority and never makes the final human Candidate/Canonical/Release decision.

## v0.2 executable core / replay compatibility

- Project Control Card validation;
- Context / namespace resolution;
- EXPLORE / CANDIDATE / AUTHORITY gate-profile routing;
- CB-01 repeated-revise breaker;
- local/registry asset-locator primitive.

The original `control-card.schema.json` remains available for immutable replay/backward compatibility. Current stored Control Cards use `control-card.v0.3.schema.json`; the repository scanner rejects v0.2 cards outside explicit provenance/replay zones.

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

### 6. Global NO COMPRESSION / NO LOSS preservation contract — v0.3 deepening

The Control Plane compiles `00-governance/OLEANDER_NO_COMPRESSION_NO_LOSS_POLICY_v1.0.md` into the existing Control Card rather than creating another Gate or parallel methodology.

The earlier machine contract triggered preservation only from `problem_layer=Architecture`. That was narrower than the policy, which also applies to narrative, Web, boards, PDFs, slides, films, App/digital work, integration and final editing. Current Control Card v0.3 therefore separates **problem layer** from **change scope**.

Every Current v0.3 card declares:

`change_scope.kind = NON_RESTRUCTURE | RESTRUCTURE`

and identifies affected surfaces such as:

`PROJECT_ARCHITECTURE / NARRATIVE / PRESENTATION / WEB / BOARD / PDF_DOCUMENT / SLIDES / FILM_MOTION / APP_DIGITAL / PROTOTYPE / INTEGRATION / FINAL_EDIT / TECHNICAL_PACKAGE / EVIDENCE_PACKAGE / SYSTEM_TOOLCHAIN / OTHER`.

This means a Web or final-delivery restructuring cannot bypass no-loss merely because its `problem_layer` is `Relation`, `Topology`, `Evidence`, or another non-Architecture layer.

#### Established-object baseline

For `RESTRUCTURE`, the card must declare `established_object_baseline` and bind it to `baseline_source`. If the work is genuinely greenfield with no established project objects, that state must be explicit through `greenfield_no_established_objects=true`.

A bare boolean such as “established objects present = false” is no longer sufficient for Current v0.3 restructuring.

`preservation_review.decisions` must account for the baseline exactly:

- every established baseline object has exactly one decision;
- duplicate decisions fail;
- missing baseline objects fail;
- decisions for objects outside the baseline fail;
- a greenfield baseline may legitimately contain zero decisions.

Per-object state remains separated into:

`concept_state + presentation_state + truth_evidence_state`

so the machine contract keeps visible that:

- `CONCEPT KEEP != PIXEL KEEP`;
- `PIXEL FAIL != DESIGN DELETE`;
- `VALIDATION SUBSET != WHOLE PROJECT`;
- `SOURCE / AUTHORITY != DERIVED PRESENTATION`.

#### Structural actions and traceability

Current actions include:

`PRESERVE / REORDER / SPLIT / GROUP / MERGE / REMAP / REWEIGHT / REDRAW / DEMOTE_TO_SUPPORT / DEMOTE_TO_PROCESS / HOLD / CUT`.

`SPLIT / GROUP / MERGE / REMAP` require `target_object_ids`, so restructuring remains traceable rather than disappearing into prose.

All non-CUT actions require `identity_preserved=true`; CUT requires `concept_state=DROP`, `identity_preserved=false`, and no replacement target. A kept concept therefore cannot be silently deleted because its current pixels are weak.

#### Structured removal reasons

Free-text reason matching was too easy to bypass with phrases such as “reduce page count and simplify the website.” Current v0.3 therefore adds structured `reason_code` values for material reduction actions.

`DEMOTE_TO_SUPPORT / DEMOTE_TO_PROCESS / CUT / MERGE` require a substantive design/authority/evidence reason code such as redundancy with no unique function, authority contradiction, project genericity, design weakness after redraw, experience/user-value harm, technical infeasibility, evidence/truth/rights/safety conflict, supersession with provenance, or hierarchy restructuring with identity preserved.

`compression`, `page count`, `cleaner website`, `shorter film`, `less text`, or `minimalism` are not valid reason codes and cannot independently authorize reduction.

#### No fixed global template

`global_fixed_chapter_count_applied` remains schema-locked to `false`.

The machine contract therefore does **not** encode C04's 12-layer architecture, or any other project's chapter count, as a global template. It protects each project’s established objects from silent loss while allowing explicit evidence-based restructuring.

This remains core validation, not a new system-level Gate. It does not decide which object deserves MAIN, does not manufacture evidence, and does not grant Promotion or Release.

### 7. Repository-wide Current Control Card discovery

`scan_control_cards.py` discovers Control Cards by content signature rather than filename. On every PR and every push to `main`, AI Governance CI validates Current stored cards against the current schema and Control Plane rules.

Current cards outside explicit provenance/replay zones must use schema v0.3. v0.2 replay/example/history objects remain readable and are not retroactively rewritten.

The scanner does not create a second registry. The repository checkout remains the discovery surface, and the existing Control Plane remains the validator.

## Commands

```bash
python 00-governance/control-plane/control_plane.py check CARD.json
python 00-governance/control-plane/scan_control_cards.py
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
python 00-governance/control-plane/control_plane.py check 00-governance/control-plane/examples/example-explore.json
python 00-governance/control-plane/scan_control_cards.py
python 00-governance/control-plane/orchestrator.py promotion 00-governance/control-plane/replays/pr85-control-card.json 00-governance/control-plane/replays/pr85-gate-receipts.json
python 00-governance/control-plane/orchestrator.py contradictions 00-governance/control-plane/replays/pr85-contradiction-manifest.json
```

Historical hardened baseline: `27/27 PASS` on PR #90 head validation. Any later regression count must be taken from the current CI run, not inferred from this historical baseline.
