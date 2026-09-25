# Execution Guide v0.2

This guide makes the Session Kernel executable without creating a second runtime.

## 0. Default surface and local capability routing

The Human stays in **Chat by default**. Do not tell the Human to switch to Codex/COS merely because the requested work needs a workstation-only capability.

Resolve execution separately from interaction intent:

`CHAT -> Session Kernel -> execution_route -> COS local bridge when required -> capability adapter -> readback -> CHAT`.

For a ready local capability and available COS bridge, use `INLINE_COS_BRIDGE`. For an unavailable/offline local surface, use the existing continuity execution-intent carrier and report `PENDING_LOCAL_EXECUTION`; never create a second queue or shadow state store.

Current selected storage adapter:

`BAIDU_STORAGE -> oleander-baidu-storage@oleander-personal v0.1.1 -> stdio -> /OLEANDER_VAULT`.

Read requests may execute immediately through the bridge. Writes still require the normal owner-native guard and authorization path. `execution_route` and `execution-intent` never grant mutation permission.

When the current Chat has the existing COS/local-terminal connector, invoke the repository bridge on the workstation rather than asking the Human to switch surfaces:

`00-governance/runtime/candidates/human-ai-codesign-vnext/codesign_chat_cos_bridge_v0_1.py`

Send one JSON request with `conversation_surface=CHAT`, `capability_id=BAIDU_STORAGE`, the selected `tool_name`, and tool `arguments`. Common read mappings are:

- storage health/state -> `oleander_storage_probe`;
- quota -> `baidu_get_quota`;
- folder/file browse -> `baidu_file_list`;
- exact/keyword search -> `baidu_file_keyword_search`;
- semantic search -> `baidu_file_semantics_search`;
- metadata -> `baidu_file_meta`.

Do not expose the Baidu credential to Chat. The local adapter obtains it from the workstation DPAPI store. For any write tool, pass a current `mutation_context` only after the normal owner-native reread/guard path; if that context is absent the bridge must return `NOT_EXECUTED`.

## 1. Resolve / Resume

For continuation, use owner-native precedence:

`explicit project/task/object key → Current Project/Task → Control Card → active Execution Receipt/checkpoint → actual native artifact + readback`.

Never use chat recency or a newer presentation derivative as authority.

## 2. Ephemeral context

Build `session-context.schema.json` as a temporary projection only. It may contain interaction axes, decision focus, option lineage, projected runtime facts, decision-rights projection, guard outcome, round trace, support budget and version bindings.

It is never Project State, a checkpoint database, artifact registry or preference store.

## 3. One material round

1. Resolve exact decision object and Current owners.
2. Frame the key unknown.
3. Explore materially distinct mechanisms under one comparison world.
4. Make minimum faithful editable/native artifacts.
5. Inspect actual artifacts/runtime.
6. Critique strongest success/contradiction and repair obvious non-value defects.
7. Stop for Human steer only if a consequential value choice remains.
8. Bind actual steer and typed/revisioned referents; preserve multiple clause-scoped Human acts when present.
9. Run mutation guard.
10. Make the steered delta preserving lineage/invariants.
11. Read back again.
12. Route professional/integration/technical/independent review.
13. Persist only through existing triggers.

## 4. Mutation guard

Before material writes check applicable:

`logical object / authority revision+fingerprint / source revision / checkpoint sequence / owner permission / native target / side-effect class / active user constraints`.

For project or external mutation, reread the existing owner-native carrier immediately before the write. Bind `logical_object_identity + authority_revision + source_revision + expected_checkpoint_sequence + observed_checkpoint_sequence + carrier_readback_status + resolver_provenance + decision_rights_status + active_user_constraints`. Require `ACTUAL_READBACK`, `EXISTING_OWNER_RESOLVER`, exact expected/observed sequence equality, explicitly clear/not-applicable decision rights, and a present current user-constraint projection (an empty list is valid). Missing rights/constraint facts fail closed. Caller-provided `ALLOW` or `guard_verdict` is never sufficient.

Possible outcomes: ALLOW; reversible-local-only; READ_ONLY; HOLD authority/checkpoint/native/permission/decision-rights.

## 5. Side-effect classes

`NONE / REVERSIBLE_LOCAL / PROJECT_MUTATION_REVERSIBLE / PROJECT_MUTATION_AUTHORITY_SENSITIVE / EXTERNAL_IRREVERSIBLE_OR_PUBLISHING`.

Auto-advance never grants new authority. Publishing/release/irreversible side effects still require their existing authorization path.

## 6. Second-round proof

Do not claim Human-feedback round two unless all exist:

`EXPLICIT HUMAN SOURCE + OWNER-NATIVE HASH-BOUND DECISION-RIGHTS PROOF + OWNER-RULE REVISION + TYPED/REVISIONED DECISION/REFERENT BINDING + HASH-BOUND EDITABLE/NATIVE DELTA REVISION + ACTUAL READBACK OF THE SAME REVISION AND ARTIFACT CONTENT HASH + INVARIANT-SPECIFIC READBACK BINDING`.

An `ALLOWED_BY_EXISTING_OWNER_RULE` label alone is insufficient: proof must bind owner-rule ref/revision, actor role, decision object and the allowed iteration action, with an `ITERATION_STEER_ONLY` ceiling. Pre-steer probes remain pre-steer. DEFER normally creates no design delta and any named branch must belong to the current pending decision. MIX needs two or more parents.

Comparison readiness also requires each visible option to bind an actual artifact revision/content hash and an actual-readback binding of that same revision **and artifact content hash**. The readback must enumerate any preserved invariants it actually verified in `verified_invariant_refs`; same-revision readback alone is not invariant proof. Presence of a filename/string alone is insufficient evidence.

## 7. Domain adapter

Bind the shared Session Kernel to the actual domain through:

`domain_id / professional_process_status / process_ref / domain_question / native_output_roles / readback_methods / claim_ceiling / hold_conditions`.

If process status is OPEN, do not synthesize a process or award professional PASS.

## 8. Completion

Report separately:

`SESSION_RESULT / DESIGN_CANDIDATE / PROFESSIONAL_STATE / REVIEW_STATE / PERSISTENCE_STATE / PROMOTION_STATE`.

For local capability work, report the execution/readback result separately from those closure dimensions. A local tool call or provider response does not by itself prove Project State mutation, Design KEEP, professional PASS or Promotion.
