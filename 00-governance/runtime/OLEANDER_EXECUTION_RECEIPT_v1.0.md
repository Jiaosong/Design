# OLEANDER Execution Receipt v1.0

Status: **ACTIVE CURRENT**  
Decision date: **2026-08-18**  
Scope: **one material execution unit**

## 0｜Purpose

Use one receipt to record the execution instance of the Current resolver/contracts. The receipt is not a new Project State, review framework or Skill.

Only sections that actually apply are executed. Prefer `NOT_APPLICABLE` to fake process.

## 1｜Identity

- `receipt_id`
- `status = WORKING / REVIEW_PENDING / HOLD / CLOSED`
- `execution_type = PROJECT / TRAINING / SKILL_VALIDATION / GOVERNANCE_RUNTIME`
- `task_id`
- date/time

## 2｜Authority snapshot

Record:

- Notion Current Root page ID + authority version;
- project/scope Current Authority;
- Source Authority;
- Design Authority;
- relevant Canonical IDs;
- Current GitHub resolver;
- actual GitHub commit/ref consumed.

The receipt does not replace Project State.

## 3｜Required native output

Record:

`artifact_class / native_format / editable_required / target_runtime / derived_formats`.

A preview, screenshot or chat explanation cannot replace a required editable/native master.

## 4｜Minimum sufficient owner set / DAG

Record the selected `PRIMARY_OWNER` and only the supporting nodes actually needed.

Node roles:

`PRIMARY_OWNER / SUPPORTING_OWNER / READ_ONLY_CONSUMER / VALIDATOR / INDEPENDENT_REVIEWER`.

Also record omitted-owner reasoning so `NO COMPRESSION / NO LOSS` cannot be misread as “run every Skill”.

Default cross-owner permission is `READ_ONLY`.

## 5｜Native artifacts and handoffs

Every material handoff records the Native Artifact Contract fields, including:

`artifact_id / artifact_role / producer_owner / authority_source / authority_state / native_format / editable_state / semantic_layers / provenance_state / dependencies / hashes_or_commit / runtime / renderer / permission / current_state / does_not_prove`.

Material derivatives receive a new artifact ID.

## 6｜TOOL adapter section

Only when a TOOL is used, record:

`adapter_id / canonical_tool_id / implemented_revision / implementation_commit / operator_role / minimum_sufficient_operator_set / effect_budget / fallback / regression_baseline`.

For Image Ops:

- static effect state → `T-VISUAL-IMAGE-OPS-001` adapter;
- temporal transition/easing/timing → `oleander-motion`.

## 7｜Real execution

Record actual runtime/tool action, result, failures, repairs and re-execution state.

Do not infer EXECUTED from a plan, prompt or file path alone.

## 8｜Actual readback

Record actual target/runtime, observed result, blockers, warnings and verdict.

`Artifact existence ≠ actual readback`.

## 9｜Four-layer regression

Record each applicable layer independently:

- `STRUCTURAL`
- `SEMANTIC`
- `VISUAL_ROI`
- `RUNTIME`

Each uses `PASS / FAIL / HOLD / NOT_APPLICABLE`.

Regression PASS does not grant Design KEEP.

## 10｜Independent review

Record:

`producer_id / reviewer_id / review_input_artifact_id / review_input_hash_or_commit / reviewer_independence_state / evidence_gate / design_quality_gate / promotion_authority`.

Producer self-check is not an independent verdict.

## 11｜Notion ↔ GitHub drift

Required when a Current cross-platform pointer or implementation changes.

Use:

`GITHUB_STATIC_CHECK` or `LIVE_CROSS_PLATFORM_CHECK`.

A repository-only check cannot report live Notion `CURRENT`.

## 12｜Closure

Record:

`material_delta / branch / commits / pull_request / ci_state / merge_commit / main_readback / notion_writeback / remaining_blockers / final_state`.

Final execution states must remain distinct: `EXECUTED / TRACEABLE / VALIDATED / DESIGN_REVIEWED / MERGED / PROMOTED / HOLD`.

## 13｜Does not prove

A complete receipt does not prove Project State, Design PASS, field/engineering truth, user validation, rights clearance or promotion unless the appropriate independent authority separately establishes it.
