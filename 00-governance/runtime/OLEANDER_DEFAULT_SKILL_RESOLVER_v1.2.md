# OLEANDER Default Skill Resolver v1.2

Status: **ACTIVE CURRENT**  
Implementation revision: **1.2.5**  
Decision date: **2026-08-19**  
Runtime extension: **2026-09-09 — Executable Frontier Resolution / Optimistic Checkpoint Concurrency / Verify-Before-Retry**  
Scope: **ALL OLEANDER projects / conversations / agents / media**  
Notion Current Authority: **OLEANDER｜设计知识库（Design） v1.1.1**  
Execution implementation: **GitHub `Jiaosong/Design`**

## 0｜Purpose

v1.2.5 keeps the existing knowledge-first execution architecture and extends the v1.2.4 Chat-first continuation baseline without adding a new state system, lock service or Agent framework:

1. **Sticky Execution Constraint Lock** — explicit negative user constraints are resolved before owner/tool selection and remain active until explicitly revoked.
2. **Flow Completion Gate** — full OLEANDER flow cannot be called complete until every applicable phase is actually closed.
3. **Existing Visual Authority + Image Consumption Gate** — visual work preserves mature/current design artifacts and checks semantic image consumption before binding.
4. **Verified Continuation / Resume Checkpoint** — same-task “继续 / 推进 / 优化 / 修一下” resumes from the last verified checkpoint while Authority and frontier remain valid.
5. **Cross-Context Frontier Discovery** — a new Chat without a reliable local pointer recovers the active frontier from existing Project State / Control Card / active Receipt using stable project/object/authority keys rather than chat memory.
6. **Executable Frontier Resolution** — the Current validator now contains a deterministic pure resolver that filters existing `WORKING/HOLD` candidates, matches stable keys, detects ambiguity/Authority drift, and selects the highest valid checkpoint sequence.
7. **Optimistic Checkpoint Concurrency** — before remote/authority/release mutation, re-read the checkpoint carrier and require `observed_checkpoint_sequence == expected_checkpoint_sequence`; sequence mismatch blocks stale execution and forces `REVALIDATE_CONCURRENT_ADVANCE`.
8. **Verify-Before-Retry** — uncertain remote mutation outcomes are read back against an expected postcondition before retry. Duplicate create-like side effects are forbidden.
9. **Continuous Ready-Node Auto-Advance** — after execution/readback, continue through ready nodes in the current turn while Authority, constraints, sequence guard, side-effect ceiling and stop conditions remain valid.
10. **Capability-Role Adapter Routing** — TOOL/plugin/connector selection follows capability role, native output, Authority, side effect, readback coverage and verified availability, not vendor name.

This is not a new Skill, METHOD, taxonomy, Agent framework, state database, checkpoint database or lock database. It hardens the existing Resolver / Project Control Card / Receipt / DAG / Tool Adapter / CI chain.

Current invariant:

> **CURRENT ROOT → CURRENT TASK / SOURCE AUTHORITY → FRONTIER DISCOVERY WHEN LOCAL POINTER IS MISSING → CONTINUATION CHECKPOINT / AUTHORITY REVALIDATION → STICKY CONSTRAINT LOCK → LIVE REGISTRY / CURRENT KNOWLEDGE → EXISTING METHOD + SKILL READBACK → EXISTING MATURE DESIGN / CURRENT VISUAL AUTHORITY → IMAGE CONSUMPTION LOOKUP → REQUIRED NATIVE OUTPUT → MINIMUM SUFFICIENT OWNER SET / DAG → CAPABILITY-ROLE TOOL ADAPTER ROUTING → CHECKPOINT-SEQUENCE GUARD BEFORE MUTATION → VERIFY UNCERTAIN REMOTE POSTCONDITION BEFORE RETRY → REAL EXECUTION → NATIVE ARTIFACT / HANDOFF → REGRESSION → ACTUAL READBACK → CHECKPOINT UPDATE → AUTO-ADVANCE NEXT READY NODE WHILE ALLOWED → EVIDENCE + INDEPENDENT DESIGN REVIEW → FLOW COMPLETION GATE → EXECUTION RECEIPT → DRIFT / SYNC AS APPLICABLE**

## 1｜Notion current architecture remains upstream

Before historical navigation, method indexes or Skill files, read the Current Root Authority, live Registry and applicable Project State / Source Authority / Current Task.

Notion owns Current knowledge identity, Canonical ID, Domain, L0–L7, hierarchy, dedicated relations and project identity. GitHub owns executable Skill/runtime implementation. Old `00–70` navigation remains provenance/discovery only.

## 2｜Sticky Execution Constraint Lock

Before selecting any execution owner, runtime, TOOL adapter or generation capability, resolve explicit constraints from:

1. latest explicit user instruction;
2. Current Task explicit constraints;
3. active Execution Receipt for the same task;
4. Current Project Authority / recorded user decisions.

Normalize applicable constraints into:

- `TOOL_DENY`
- `OUTPUT_DENY`
- `CREATION_DENY`
- `OWNER_REQUIRE`
- `PROCESS_REQUIRE`
- `REVIEW_REQUIRE`

Current normalized rules include:

- `NO_IMAGE_GENERATION`
- `NO_NEW_SKILL`
- `NO_NEW_METHOD`
- `NO_NEW_FRAMEWORK`
- `USE_EXISTING_OLEANDER_METHODS_AND_SKILLS`
- `FULL_OLEANDER_FLOW_REQUIRED`
- `NO_PRODUCER_SELF_PROMOTION`

### Sticky means sticky

An active constraint survives ordinary follow-ups such as “继续 / 优化 / 再做一下 / 修一下 / 按 OLEANDER 做”. These phrases do **not** revoke a prohibition.

A constraint can be released only by a later explicit instruction that directly changes that named constraint. For example “现在可以生图” releases `NO_IMAGE_GENERATION` only.

### Hard effects

`NO_IMAGE_GENERATION` means do not call image-generation tools or generative-image adapters; use existing source imagery, native vector, HTML/CSS/SVG, 3D, CAD, layout or other non-generative production. If the required native output truly cannot be produced without generation, return **HOLD**.

`NO_NEW_SKILL / NO_NEW_METHOD / NO_NEW_FRAMEWORK` means do not create a sidecar Skill, METHOD, router, framework or parallel schema simply because a gap appears. Compose existing owners, use a bounded fallback, record the gap, or HOLD.

`USE_EXISTING_OLEANDER_METHODS_AND_SKILLS` means the relevant Current METHOD / Skill / `CAPABILITY.json` / runtime material must actually be read. Saying “我会用 OLEANDER” is not execution evidence.

## 2A｜Verified Continuation / Resume Checkpoint

A generic follow-up that does not materially redefine the task, object, constraints or requested output is interpreted as same-task continuation, not a restart.

Resolve an existing continuation state in this order:

1. active Execution Receipt for the same task;
2. Current Project Control Card;
3. Current Task / Project State only when no stronger runtime checkpoint exists.

The checkpoint records runtime continuity:

`checkpoint_state / current_node / last_verified_artifact / resume_from / next_allowed_action / authority_fingerprint / stale_reasons / checkpoint_sequence / checkpoint_updated_at / expected_checkpoint_sequence / executor_id / execution_lease_state / lease_acquired_at`.

It does **not** create another Project State or owner taxonomy.

### Cross-context frontier discovery

When a new Chat or compressed context lacks a reliable local `task_id`, do not use chat history or summary as execution authority. Discover the existing frontier in this order:

1. stable project / task / object keys explicitly present in the current request;
2. Current Project State or Current Task pointer;
3. Current Project Control Card;
4. active `WORKING / HOLD` Execution Receipts.

Match with stable keys when available:

`PROJECT_ID_OR_SCOPE_ID / TASK_ID / LOGICAL_OBJECT_OR_CANONICAL_IDS / CURRENT_NATIVE_MASTER_OR_REF / AUTHORITY_FINGERPRINT`.

Title similarity or chat summary alone is insufficient.

If multiple checkpoints belong to the same task/object and match Current Authority, use the highest `checkpoint_sequence`, then latest `checkpoint_updated_at`; older checkpoints remain provenance.

If multiple **distinct** active frontiers remain and Current Authority does not identify one active task, return `HOLD_AMBIGUOUS_FRONTIER` instead of guessing, merging projects or creating another Current.

### Executable frontier resolver

The Current runtime validator contains `resolve_continuation_frontier(...)` as a side-effect-free deterministic function. It must:

- filter to existing active `WORKING/HOLD` frontier records;
- match exact stable project/task/object/native-ref keys when supplied;
- prefer Authority-fingerprint matches;
- return `REVALIDATE_AUTHORITY_BEFORE_MUTATION` when no candidate matches Current Authority;
- detect multiple distinct unresolved tasks and return `HOLD_AMBIGUOUS_FRONTIER`;
- choose the highest checkpoint sequence, then latest checkpoint time, among legal same-task matches.

Regression must invoke this function against real machine cases. Presence of policy strings alone is not sufficient proof.

### Authority fingerprint and direct resume

The fingerprint inputs remain:

`CURRENT_ROOT_VERSION / PROJECT_OR_SCOPE_AUTHORITY / SOURCE_AUTHORITY / DESIGN_AUTHORITY / CURRENT_TASK_ID / CURRENT_NATIVE_MASTER_OR_REF / ACTIVE_CONSTRAINT_LOCK`.

Direct resume from `next_allowed_action` requires:

- same task and same logical object;
- matching Authority fingerprint;
- `last_verified_artifact` with real Actual Readback;
- no stale or `RETEST_REQUIRED / REGEN_REQUIRED / HOLD` dependency/handoff;
- `checkpoint_state=RESUMABLE`.

Canonical behavior:

`DISCOVER / RESTORE VERIFIED CHECKPOINT → CONFIRM CURRENT AUTHORITY → RESTORE ACTIVE CONSTRAINTS → SKIP VERIFIED COMPLETED NODES → GUARD EXPECTED SEQUENCE → EXECUTE NEXT ALLOWED ACTION → READBACK → UPDATE EXISTING CHECKPOINT`.

### Mandatory revalidation

Do not direct-resume when project/task changed, Authority fingerprint changed, Source/Design Authority changed, native master/write frontier moved externally, a dependency became stale, the checkpoint is missing/corrupt, last artifact lacks actual readback, or another executor advanced the checkpoint sequence.

In those cases use `REVALIDATE`; preserve valid upstream work and restart only from the first invalid node.

### BLOCKED / CLOSED / context switch

BLOCKED re-checks only its declared release condition; no blind retry. CLOSED is not reopened by generic “继续”. A different Chat or context compression alone is not an Authority change.

### Persistence throttle

Reuse existing Control Card fields. Runtime continuation fields are conditional and do not form another state object. Write/update only after material readback, genuine legal repair-boundary HOLD, or typed handoff ready/accepted.

**NO MATERIAL DELTA = NO NEW RECEIPT / PROJECT STATE JUST FOR ANOTHER CHAT TURN.**

## 2B｜Optimistic checkpoint concurrency

Concurrent Chat / Automation / Work / runtime executors must not rely on last-writer-wins.

Before `REMOTE_MUTATION / AUTHORITY_MUTATION / RELEASE_MUTATION` and before persisting an advanced checkpoint:

`READ EXPECTED CHECKPOINT SEQUENCE → RE-READ CURRENT CARRIER → OBSERVED == EXPECTED ? PROCEED : BLOCK + REVALIDATE_CONCURRENT_ADVANCE`.

Runtime fields:

`expected_checkpoint_sequence / executor_id / execution_lease_state / lease_acquired_at`.

Lease states are `NONE / ACTIVE / STALE / CONFLICTED`, but lease metadata is advisory only. The checkpoint sequence is the concurrency truth. A stale `ACTIVE` lease cannot override a newer checkpoint sequence. Lease metadata grants no mutation Authority.

After material execution + readback, a new persisted checkpoint must advance to a sequence greater than the prior sequence using the source adapter's native concurrency mechanism when available.

No global lock service, lock database or second Project State is introduced.

## 2C｜Continuous ready-node auto-advance

For `继续 / 推进 / 执行 / 修复 / 优化`, do not stop after one successful node merely because one tool call completed.

After each material node:

`EXECUTE READY NODE → SELECTIVE READBACK → REPAIR + RETEST WHEN LEGAL → UPDATE EXISTING CHECKPOINT WHEN TRIGGERED → RESOLVE NEXT READY NODE → CONTINUE WHILE ALLOWED`.

Advance only when previous node executed, readback/typed handoff is acceptable, next node is ready, Authority fingerprint remains valid, constraints remain valid, side-effect ceiling is authorized, expected checkpoint sequence is still current for mutation, and no stop condition is active.

Stop on Flow Completion, genuine blocker, Authority conflict/ambiguity, concurrent checkpoint advance, genuine user design/scope decision, unauthorized higher side effect, unrecoverable source, external wait/future condition, unavailable required independent review, or runtime hard limit.

A forced stop reports exact `current_node / next_allowed_action / blocker`; it does not promise background work.

Continuous execution is current-turn orchestration, not background execution, and does not assume generic child-agent spawning.

## 3｜Execution contract layer

Current contracts remain:

- `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1`
- `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1`
- `OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1`
- `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1`
- `OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1`
- `OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1`
- `OLEANDER_EXECUTION_RECEIPT_v1.0`
- `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0`

The constraint lock precedes mutation. Continuation restore cannot override newer explicit constraints or Current Authority.

### Capability-role TOOL/plugin routing

When multiple connectors/runtimes/plugins can perform a task, route through the existing Tool Adapter Contract instead of vendor-specific project logic.

Selection precedence:

`CURRENT AUTHORITY + OWNER BOUNDARY → REQUIRED NATIVE OUTPUT + MUTATION CAPABILITY → ACTIVE CONSTRAINTS + PERMISSION → LOWEST SUFFICIENT SIDE EFFECT → ACTUAL READBACK COVERAGE → CURRENT VERIFIED AVAILABILITY / RELIABILITY → LOWER EXECUTION OVERHEAD → DECLARED FALLBACK`.

Probe only the selected surface or needed fallback. One-off connector use is ephemeral and does not create a registry entry, TOOL, Skill, Method, Framework or Project State.

Prefer distinct readback surfaces when practical; same-surface readback without alternatives is `NOT_INDEPENDENT`.

Heavy executors remain `ESCALATION_ONLY`.

### Verify-before-retry

For remote/authority/release writes, use the Tool Adapter Contract's operation fingerprint and expected postcondition.

`UNCERTAIN OUTCOME → VERIFY POSTCONDITION BEFORE RETRY`.

If the postcondition exists, normalize to confirmed success and do not retry. If absence is proven, retry only when the operation is idempotent or provider-keyed and bounded retry remains. Otherwise HOLD rather than risk duplicate PR/page/deployment/upload/message or other side effect.

## 4｜Minimum sufficient owner set

`NO COMPRESSION / NO LOSS` protects information. It does not require every Skill to run.

Use the smallest owner set that can produce the required native output and applicable validation/review. Multi-owner work uses explicit DAG roles and typed handoffs.

**Full OLEANDER flow ≠ full Skill stack.**

## 5｜Flow Completion Gate

For production, mutation, training, state-changing review work, or `FULL_OLEANDER_FLOW_REQUIRED`, build an applicable-phase checklist before production.

Canonical phases:

1. `AUTHORITY_PREFLIGHT`
2. `STICKY_CONSTRAINT_RESOLUTION`
3. `EXISTING_KNOWLEDGE_METHOD_SKILL_RESOLUTION`
4. `EXISTING_VISUAL_AUTHORITY_AND_IMAGE_CONSUMPTION_CHECK` when visual content images are involved
5. `REQUIRED_NATIVE_OUTPUT_DEFINITION`
6. `CAPABILITY_AND_MINIMUM_OWNER_SET`
7. `REAL_EXECUTION`
8. `NATIVE_ARTIFACT_AND_TYPED_HANDOFF_RECORD`
9. `ACTUAL_READBACK`
10. `REGRESSION_AS_APPLICABLE`
11. `INDEPENDENT_REVIEW_AS_APPLICABLE`
12. `SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE`

Core phases cannot be skipped. Other phases may be `NOT_APPLICABLE` only with a concrete reason.

### No early completion

Plan written, method explained, artifact created, file exported, PR opened, CI green, producer self-check, render pass or regression pass cannot independently justify “完成 / CLOSED / 已闭环”.

If any required applicable phase is missing, `FAIL` or `HOLD`, the task remains **HOLD / INCOMPLETE**.

## 6｜Default GPT / Agent behavior

1. Read Current Root Authority + applicable Project State / Source Authority / Current Task.
2. If continuation lacks a reliable task pointer, discover the active frontier from Current Project/Task → Control Card → active Receipt using stable keys.
3. Run executable frontier resolution; ambiguous distinct frontiers HOLD.
4. Resolve the latest valid continuation checkpoint.
5. Revalidate Current Authority when required.
6. Resolve sticky execution constraints before owner/tool selection.
7. Enforce tool/output/creation/process locks.
8. Resolve live Registry identity and Current knowledge context.
9. Retrieve relevant Current METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE.
10. Reuse mature design/current assets and actually read required existing Skill/capability material.
11. For visual work, identify strongest current board/design object/native figure.
12. Query Image Consumption before semantic image binding.
13. Block already-reserved/consumed/ineligible semantic image reuse across independent consumers.
14. Reserve an available image before layout production.
15. Define required native output.
16. Build applicable Flow Completion checklist.
17. Resolve Execution Owner Map and Skill Capability Contract.
18. Select Minimum Sufficient Owner Set; build DAG only when necessary.
19. Resolve adapters through capability-role routing; probe only selected/needed surfaces.
20. If resuming, skip verified nodes and restore `next_allowed_action`.
21. Re-read current checkpoint carrier and enforce `observed_sequence == expected_sequence` before mutation.
22. If a previous remote mutation outcome is uncertain, verify expected postcondition before any retry.
23. Execute the real native/editable artifact.
24. Emit Native Artifact records / typed handoffs as applicable.
25. Run applicable structural/semantic/visual/runtime regression.
26. Open/render/run actual result and perform readback.
27. Update the existing checkpoint only when a conditional persistence trigger is met; advance sequence monotonically.
28. If another node is ready and no stop condition is active, continue in the same turn.
29. Run Evidence Gate and independent Professional Design Gate separately where applicable.
30. Verify Flow Completion Gate.
31. Emit/update one Execution Receipt with applicable continuation, concurrency, route, idempotency, continuous-execution and image-consumption evidence.
32. Run Notion↔GitHub drift check where pointers changed.
33. Only after failed execution/readback may reusable Skill gaps be diagnosed; creation denies still take precedence.
34. Sync material delta and preserve provenance.

## 7｜Existing-first / Source Gravity / Visual Authority

Existing-first is not satisfied by locating an old asset and re-authoring it into a weaker carrier.

Default visual order:

`CURRENT SOURCE / MATURE DESIGN / CURRENT BOARD OR NATIVE ARTIFACT → IMAGE CONSUMPTION CHECK → REUSE DIRECT WHEN AVAILABLE → PRESENTATION ADAPTATION → NEW VISUAL ONLY WHEN A REAL GAP REMAINS`.

Hard rules:

- `OBJECT INTEGRITY → FRAME / LAYOUT`.
- carrier adapts to design object, not vice versa;
- valid mature figures are used before inventing substitutes;
- already-consumed figures are unavailable to independent consumers;
- presentation carrier authority never reverses into Source or Design Authority.

New Skill creation remains unauthorized by a project, case, file, PR, CI success or missing convenience helper. `NO_DEDICATED_OWNER` remains valid and does not authorize creation.

## 8｜Image Consumption / Uniqueness Gate

Current allocation rule:

`ONE SEMANTIC CONTENT IMAGE → ONE CONSUMER UNIT`.

States:

`AVAILABLE / RESERVED / CONSUMED / RELEASED / REJECTED_NOT_ELIGIBLE / LEGACY_MULTI_CONSUMED`.

Blocking states prevent another independent consumer from using the image. Presentation derivatives inherit semantic identity. Genuine child figures require parent/source/bounds/hash/semantic-role records. SYSTEM_REUSABLE remains explicit and bounded. Release requires explicit project authority.

Machine/register definition: `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json`.

## 9｜Image-generation boundary

AI imagery remains supplementary when permitted. It never replaces Source Authority, Design Authority, authoritative geometry, technical dimensions, editable text or field truth.

When `NO_IMAGE_GENERATION` is active, no image-generation tool or generative-image adapter is called.

## 10｜Readback, regression and review

- `Artifact existence ≠ Design quality`
- `Traceability ≠ Professional finish`
- `Evidence correctness ≠ Visual excellence`
- `Process PASS ≠ MAIN KEEP`
- `Render PASS ≠ Design PASS`
- `Prototype PASS ≠ Field PASS`
- `Regression PASS ≠ Design KEEP`

Producer self-check cannot become independent Design Review where independence is required.

Continuation advances only from actual readback, genuine repair-boundary HOLD or typed handoff. Plans/chat summaries/producer assertions are not verified artifacts.

Dependent mutations require readback between nodes. Checkpoint sequence must be re-read before remote mutation. Uncertain side effects require postcondition verification before retry.

## 11｜Execution Receipt

The Current `OLEANDER_EXECUTION_RECEIPT_v1.0` remains the single instance carrier. New receipts record active constraints, flow state, continuation when applicable, concurrency guard when applicable, adapter route when applicable, idempotency evidence when applicable, continuous execution when applicable, and image consumption when applicable.

Older receipts remain immutable provenance. Runtime extensions are prospective and conditional; every chat turn is not a material execution unit.

## 12｜Synchronization

A material runtime change follows:

`Current Authority readback → GitHub branch → commit → PR → CI → main readback → minimal Notion Current pointer/fact update when required → live drift check`.

CI proves declared machine checks passed; it does not itself close a design/project task.

Chat/session boundaries, liveness probes and no-delta route/idempotency checks do not trigger Notion writeback.

## 13｜Does not prove

Resolver v1.2.5 being Current does not prove project design quality, field truth, engineering validity, user validation, rights clearance or candidate promotion. Frontier selection, concurrency guards, adapter routing, idempotency decisions and continuous auto-advance prove only their bounded runtime conditions; none independently prove Design PASS, Current, promotion or closure.
