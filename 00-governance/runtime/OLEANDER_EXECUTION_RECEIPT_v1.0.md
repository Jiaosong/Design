# OLEANDER Execution Receipt v1.0

Status: **ACTIVE CURRENT**  
Policy revision: **1.1**  
Decision date: **2026-08-18**  
Current extensions: **2026-08-19 — Existing Visual Authority + Image Consumption; 2026-09-09 — Continuation Resume Checkpoint; 2026-09-09 — Cross-Context Frontier Discovery + Adapter Route + Continuous Auto-Advance; 2026-09-09 — Optimistic Concurrency + Verify-Before-Retry**  
Scope: **one material execution unit**

## 0｜Purpose

Use one receipt to record the execution instance of the Current resolver/contracts. The receipt is not a new Project State, review framework or Skill.

Policy revision 1.1 requires two mandatory runtime sections for all new receipts:

1. **Constraint Lock**
2. **Flow Completion**

Image Consumption remains required whenever the execution binds semantic content imagery.

Conditional runtime sections now also include:

- **Continuation Resume Checkpoint** for material cross-turn/handoff continuation;
- **Cross-Context Frontier Discovery** when the current Chat lacks a reliable local pointer;
- **Concurrency Guard** when a resumable checkpoint is about to drive Remote/Authority mutation;
- **Adapter Route Decision** when multiple execution surfaces are materially evaluated;
- **Remote Mutation Idempotency** when a remote write outcome is uncertain or retry is considered;
- **Continuous Execution** when multiple ready nodes execute or auto-advance stops before Flow Completion.

These remain sections inside the existing Receipt. They do not create a new Project State, METHOD, Skill, framework, Agent taxonomy, plugin database, checkpoint database or lock service.

Historical receipts remain immutable provenance; new fields are prospective and conditional.

## 1｜Identity

- `receipt_id`
- `status = WORKING / REVIEW_PENDING / HOLD / CLOSED`
- `execution_type = PROJECT / TRAINING / SKILL_VALIDATION / GOVERNANCE_RUNTIME`
- `task_id`

## 2｜Authority snapshot

Record Current Root, project/scope authority, Source Authority, Design Authority, relevant Canonical IDs, Current GitHub resolver and actual commit/ref. The receipt does not replace Project State.

## 3｜Constraint Lock

Resolve before tool/owner selection and record:

`resolved_from / inheritance_state / active_constraints / revocations / tool_deny / output_deny / creation_deny / required_behaviors`.

Each active constraint records:

`constraint_id / constraint_type / normalized_rule / source / scope / status / revocation_rule`.

Supported normalized rules include:

`NO_IMAGE_GENERATION / NO_NEW_SKILL / NO_NEW_METHOD / NO_NEW_FRAMEWORK / USE_EXISTING_OLEANDER_METHODS_AND_SKILLS / FULL_OLEANDER_FLOW_REQUIRED / NO_PRODUCER_SELF_PROMOTION`.

A generic “继续 / 优化 / 再做” does not revoke anything. Only a later explicit instruction can release the named constraint.

## 3A｜Continuation Resume Checkpoint｜when applicable

Use when the same `task_id` / logical object remains active and execution is expected to continue while Receipt status is `WORKING` or `HOLD`.

Record:

- `checkpoint_state = RESUMABLE / REVALIDATE / BLOCKED / CLOSED`
- `current_node`
- `last_verified_artifact`
- `resume_from`
- `next_allowed_action`
- `authority_fingerprint`
- `stale_reasons`
- `checkpoint_sequence`
- `checkpoint_updated_at`
- `expected_checkpoint_sequence`
- `executor_id`
- `execution_lease_state = NONE / ACTIVE / STALE / CONFLICTED`
- `lease_acquired_at`

`last_verified_artifact` records at minimum:

`artifact_id / hash_or_commit / readback_verdict`.

The Authority fingerprint is a deterministic digest or stable composite over:

`CURRENT_ROOT_VERSION / PROJECT_OR_SCOPE_AUTHORITY / SOURCE_AUTHORITY / DESIGN_AUTHORITY / CURRENT_TASK_ID / CURRENT_NATIVE_MASTER_OR_REF / ACTIVE_CONSTRAINT_LOCK`.

### Cross-context frontier discovery

When a new Chat or compressed context lacks a reliable local task pointer, recover the existing frontier from:

1. project/task/object keys explicitly present in the current request;
2. Current Project State or Current Task pointer;
3. Current Project Control Card;
4. active `WORKING / HOLD` Execution Receipts.

Match on stable keys when available:

`PROJECT_ID_OR_SCOPE_ID / TASK_ID / LOGICAL_OBJECT_OR_CANONICAL_IDS / CURRENT_NATIVE_MASTER_OR_REF / AUTHORITY_FINGERPRINT`.

Do not use title similarity, chat history or a summary as checkpoint authority.

When materially used, record:

`discovery_trigger / project_or_scope_key / task_key / object_or_canonical_ids / candidate_frontiers / selected_frontier / selection_basis / ambiguity_state`.

Same-task matching checkpoints resolve by highest `checkpoint_sequence`, then latest `checkpoint_updated_at`. Multiple distinct unresolved frontiers use `HOLD_AMBIGUOUS_FRONTIER`.

### Direct resume and revalidation

Direct resume requires same task/object, matching Authority fingerprint, actual readback for the last artifact, no stale dependency/handoff and `checkpoint_state=RESUMABLE`.

Set `REVALIDATE` before mutation when project/task/authority/source/design/native-master changes, a dependency is stale, the last artifact lacks readback, or another executor advances the checkpoint sequence.

A Chat switch or context compression alone is not an Authority change.

### BLOCKED / CLOSED / persistence

A BLOCKED checkpoint re-checks only its declared release condition; no blind retry. A generic “继续” does not reopen CLOSED.

Checkpointing reuses existing Receipt / Control Card state. Write only after material readback, genuine repair-boundary HOLD, or typed handoff ready/accepted.

`NO MATERIAL DELTA = NO NEW RECEIPT JUST FOR CHECKPOINTING`.

## 3B｜Concurrency Guard｜when applicable

Use before `REMOTE_MUTATION / AUTHORITY_MUTATION / RELEASE_MUTATION` when execution is driven by a resumable checkpoint.

Record:

`expected_checkpoint_sequence / observed_checkpoint_sequence / executor_id / execution_lease_state / lease_acquired_at / guard_verdict`.

The concurrency truth is the checkpoint sequence, not the lease metadata.

Canonical guard:

`READ EXPECTED SEQUENCE → RE-READ CURRENT CARRIER BEFORE MUTATION → OBSERVED == EXPECTED = PASS_SEQUENCE_MATCH → OBSERVED != EXPECTED = REVALIDATE_CONCURRENT_ADVANCE / BLOCK MUTATION`.

A stale `ACTIVE` lease cannot override a newer sequence. `executor_id` and lease fields are runtime diagnostics only and grant no mutation authority. No global lock service or lock database is introduced.

## 3C｜Continuous Execution｜when applicable

Use when more than one ready node executes in one material run, or auto-advance stops before Flow Completion.

Record:

`auto_advance_enabled / nodes_executed_in_order / node_readback_verdicts / stop_reason / final_current_node / next_allowed_action`.

Dependent mutations require Actual Readback between nodes. Do not stop after one node without a real boundary.

Allowed stop reasons include:

`FLOW_COMPLETION_GATE_PASS / GENUINE_BLOCKER / AUTHORITY_CONFLICT_OR_AMBIGUOUS_FRONTIER / CONCURRENT_CHECKPOINT_ADVANCE / USER_DESIGN_OR_SCOPE_DECISION_REQUIRED / SIDE_EFFECT_ESCALATION_NOT_AUTHORIZED / MISSING_UNRECOVERABLE_SOURCE / FUTURE_CONDITION_OR_EXTERNAL_WAIT_REQUIRED / REQUIRED_INDEPENDENT_REVIEW_UNAVAILABLE / TOOL_OR_RUNTIME_HARD_LIMIT`.

Continuous execution is current-turn orchestration, not background work.

## 4｜Required native output

Record:

`artifact_class / native_format / editable_required / target_runtime / derived_formats`.

A preview, screenshot or chat explanation cannot replace a required editable/native master.

## 5｜Minimum sufficient owner set / DAG

Record `PRIMARY_OWNER` and only supporting nodes actually needed.

Node roles:

`PRIMARY_OWNER / SUPPORTING_OWNER / READ_ONLY_CONSUMER / VALIDATOR / INDEPENDENT_REVIEWER`.

`NO COMPRESSION / NO LOSS` does not mean every Skill must run.

## 6｜Flow Completion

Record:

`mode / required_phases / phase_results / incomplete_required_phases / completion_gate / completion_claim_allowed`.

Canonical phases remain:

1. `AUTHORITY_PREFLIGHT`
2. `STICKY_CONSTRAINT_RESOLUTION`
3. `EXISTING_KNOWLEDGE_METHOD_SKILL_RESOLUTION`
4. `EXISTING_VISUAL_AUTHORITY_AND_IMAGE_CONSUMPTION_CHECK` when semantic content imagery is bound
5. `REQUIRED_NATIVE_OUTPUT_DEFINITION`
6. `CAPABILITY_AND_MINIMUM_OWNER_SET`
7. `REAL_EXECUTION`
8. `NATIVE_ARTIFACT_AND_TYPED_HANDOFF_RECORD`
9. `ACTUAL_READBACK`
10. `REGRESSION_AS_APPLICABLE`
11. `INDEPENDENT_REVIEW_AS_APPLICABLE`
12. `SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE`

`status=CLOSED` requires `completion_gate=PASS`, no incomplete required phases, and no required `FAIL/HOLD`.

A plan, generated/exported file, PR, CI green, self-check, render pass or regression pass is not enough to close a full-flow task.

## 7｜Native artifacts and handoffs

Every material handoff records the Native Artifact Contract fields, including:

`artifact_id / artifact_role / producer_owner / authority_source / authority_state / native_format / editable_state / semantic_layers / provenance_state / dependencies / hashes_or_commit / runtime / renderer / permission / current_state / does_not_prove`.

Material derivatives receive a new artifact ID. A new artifact ID does not automatically create a new semantic-image identity.

## 7A｜Image Consumption｜when applicable

Required whenever a visual execution binds a semantic content image. Record:

`register_path_or_authority / lookup_performed / reservations_or_consumptions / conflicts / blocked_assets / release_actions / verdict`.

The authoritative semantics remain in `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json`.

## 8｜TOOL adapter section

Only when a TOOL is actually used, record:

`adapter_id / canonical_tool_id / implemented_revision / implementation_commit / operator_role / minimum_sufficient_operator_set / effect_budget / fallback / regression_baseline`.

An active Tool Deny is checked before adapter selection.

## 8A｜Adapter Route Decision｜when applicable

For material route selection, record:

`required_capability_roles / candidate_surfaces / selected_surface / selection_reasons / availability_state / authority_ceiling / side_effect_class / readback_surface / fallback_surface`.

The selection reason is capability/authority/readback based, not vendor based. Unused candidates and liveness probes remain ephemeral. The selected surface gains no Authority.

## 8B｜Remote Mutation Idempotency｜when applicable

Use when a Remote/Authority/Release mutation returns `UNCERTAIN`, or a retry is being considered.

Record:

`operation_fingerprint / expected_postcondition / outcome_state / verification_surface / retry_decision`.

`outcome_state = CONFIRMED_SUCCESS / CONFIRMED_FAILURE / UNCERTAIN`.

Canonical rule:

`UNCERTAIN → VERIFY POSTCONDITION BEFORE RETRY`.

If the expected postcondition is found, normalize to `CONFIRMED_SUCCESS` and do not retry. If absence is proven, retry only when the operation is idempotent or provider-keyed and the bounded retry budget remains. Otherwise HOLD rather than risk a duplicate side effect.

Timeout or connector ambiguity is never sufficient evidence to replay a create-like mutation.

`NO MATERIAL DELTA = NO NEW RECEIPT JUST TO RECORD IDEMPOTENCY PROBES`.

## 9｜Real execution

Record actual runtime/tool action, result, failures, repairs and re-execution state. Do not infer EXECUTED from a promise, plan, path, PR or CI state.

## 10｜Actual readback

Record actual target/runtime, observed result, blockers, warnings and verdict.

`Artifact existence ≠ actual readback`.

Readback is also the dependency boundary for checkpoint advancement, continuous mutations, uncertain-outcome verification and cross-system state changes.

## 11｜Four-layer regression

Record each applicable layer independently:

`STRUCTURAL / SEMANTIC / VISUAL_ROI / RUNTIME`, each with `PASS / FAIL / HOLD / NOT_APPLICABLE`.

Regression PASS does not grant Design KEEP and does not independently close the flow.

## 12｜Independent review

Record:

`producer_id / reviewer_id / review_input_artifact_id / review_input_hash_or_commit / reviewer_independence_state / evidence_gate / design_quality_gate / promotion_authority`.

Producer self-check is not an independent verdict. A different technical surface is not automatically an independent design review.

## 13｜Notion ↔ GitHub drift

Required when a Current cross-platform pointer or implementation changes. Use `GITHUB_STATIC_CHECK` or `LIVE_CROSS_PLATFORM_CHECK`.

A repository-only check cannot report live Notion `CURRENT`.

## 14｜Closure

Record:

`material_delta / branch / commits / pull_request / ci_state / merge_commit / main_readback / notion_writeback / remaining_blockers / final_state`.

Closure is allowed only after the Flow Completion Gate passes.

## 15｜Does not prove

A complete receipt, valid checkpoint, concurrency guard, idempotency decision, discovered frontier, adapter route decision or continuous-execution record does not prove Project State, Design PASS, field/engineering truth, user validation, rights clearance or promotion unless the appropriate independent authority separately establishes it.
