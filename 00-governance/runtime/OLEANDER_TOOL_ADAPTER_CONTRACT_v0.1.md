# OLEANDER Tool Adapter Contract v0.1

Status: **ACTIVE_CURRENT**  
Decision date: **2026-08-18**  
Scope: **Notion TOOL → GitHub execution adapter**

## 0｜Purpose

This contract defines the stable interface between a Current Notion `TOOL` object and GitHub execution owners. A TOOL may expose operators, parameters, adapters, fixtures and fallbacks. It must not silently become a hidden Skill.

Required adapter fields:

`adapter_id / canonical_tool_id / notion_object_id / implemented_revision / implementation_commit / adapter_owner / supported_operator_classes / parameter_schema / runtime / renderer / fallback / unsupported_operations / output_permissions / regression_baseline / last_verified / does_not_prove`.

## 1｜Shared Tool boundary

A shared TOOL may own:
- operator vocabulary;
- parameter contracts;
- adapter/runtime selection;
- deterministic fixtures;
- compatibility/fallback rules.

A shared TOOL must not own:
- the final project artifact;
- independent design methodology outside its TOOL role;
- project Design Authority;
- evidence promotion;
- final Design Review verdict;
- a new Notion Domain.

If a router/TOOL begins owning final artifacts, lifecycle, autonomous methods and project decisions, trigger the dedupe/hidden-Skill audit instead of normalizing the expansion.

## 2｜Operator selection

Do not resolve from software menus. Use:

`DESIGN INTENT → EFFECT / OPERATOR ROLE → MINIMUM SUFFICIENT OPERATOR SET → PARAMETER BOUNDS → EFFECT BUDGET → EFFECT-OFF BASELINE → ACTUAL READBACK`.

`effect_budget` records the maximum justified operator families or layers required to communicate the intended hierarchy/material/state. More operators require explicit incremental value.

## 3｜Current Image Ops adapter

Current Notion TOOL:

`T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑`.

Current adapter consumers are the 11 Skill visual-layer bindings already merged through PR #246:

`oleander-research / oleander-data-viz / oleander-3d-pipeline / oleander-story-and-board / oleander-motion / oleander-delivery-qc / oleander-ui-visual-composition / oleander-ui-interaction / oleander-route-wayfinding-ui / oleander-game-ui / oleander-mobile-game-ui`.

The Notion TOOL remains the operator semantics authority. Each Skill binding owns only its task-specific permission/boundary.

## 4｜Static versus temporal boundary

Hard split:

`STATIC EFFECT STATE SPEC → T-VISUAL-IMAGE-OPS-001 / image adapter`

`STATE TRANSITION / TEMPORAL BEHAVIOUR → oleander-motion / Motion Effect Atlas`

Image Ops may define start/end static parameter states such as opacity, mask, blur amount, grade or texture state. It must not own easing, timing, transition sequencing, interruption/re-entry or Reduced Motion theory.

## 5｜Version binding

Every reusable recipe/fixture must answer:
- which `canonical_tool_id` it implements;
- which Notion `implemented_revision` or verification date it targets;
- which GitHub implementation commit contains it;
- which runtime/renderer produced the baseline;
- which regression baseline validates it.

A recipe without this binding is `UNBOUND_IMPLEMENTATION` and must not be treated as Current reusable authority.

## 6｜Proprietary / proxy behavior

When Adobe or another proprietary implementation cannot be reproduced exactly, adapters must declare `PROXY / NOT PIXEL-IDENTICAL` and preserve the Current TOOL truth boundary.

## 7｜Does not prove

Adapter success proves only that an operator implementation is callable and bounded. It does not prove visual quality, semantic correctness, evidence truth, geometric truth, physical material truth or project promotion.

## 8｜Connected execution surfaces are adapters, not ontology

When the Resolver uses a connected plugin, connector, browser surface, deployment surface, scheduler, native runtime or heavy executor, treat that surface as an **execution capability adapter** under the existing owner/authority model. Do not create a new Skill, METHOD, Framework, Project State, Current or Notion TOOL merely because a connector exists.

Hard boundaries:

- connector availability does not grant mutation authority;
- a tool response is not Knowledge, Project State, Source Authority or Design Authority by default;
- a deployment target is not Design Authority;
- a browser observation is runtime/readback evidence, not project truth unless the applicable Evidence/Authority gate promotes the fact;
- an automation wake-up is a trigger, not a material delta;
- a heavy executor is a producer/runtime surface, not the Completion Gate or independent reviewer;
- existing authority contracts may assign a surface a specific role, but this adapter contract does not expand that role.

Use `OLEANDER_SHARED_EXECUTION_SURFACES_v0.1` for the Current persistent surface registry. Prefer role/capability routing over adding vendor-specific ontology.

A connector that is currently exposed to Chat but is not yet represented as a persistent shared surface may still be used **ephemerally** when its capability role, authority ceiling, native-output boundary and readback contract fit the task. One-off use does not auto-create a registry entry, TOOL, Skill, Method, Framework or Project State.

### 8A｜Machine-local execution-surface readback

`Chat On Steroids` MCP registration, local source/deployment paths, host-process state, endpoint ownership and runtime health are **dynamic execution evidence**, not another Control Plane or Current registry.

The persistent role/eligibility owner remains `OLEANDER_SHARED_EXECUTION_SURFACES_v0.1`. When the `chat_on_steroids_local_execution_bridge` surface is selected, the machine-local readback may be consumed from the Current runtime registry at `.mcp-runtime/registry/OLEANDER_INTEGRATION_REGISTRY_CURRENT.json` (or the equivalent workspace-local path).

Hard separation:

- persistent Shared Execution Surface registration/role/eligibility → GitHub Current contract;
- machine-local registration/transport/host/endpoint/health → local runtime readback;
- Project / Source / Design / Knowledge Authority → existing upstream OLEANDER authority contracts;
- runtime deployment states such as `STAGED / VALIDATED / LIVE_CURRENT / DEGRADED / SUPERSEDED / RETIRED / STALE / QUARANTINED` apply only to the execution surface or deployment object and must not overwrite Job, Design, Skill, Project, Evidence or Authority state machines;
- an account connector or MCP appearing in inventory does not make it a canonical shared execution surface or authorize mutation.

## 9｜Side-effect classification

Before execution, classify the minimum sufficient side effect:

- `READ_ONLY` — inspect/search/fetch/readback only;
- `LOCAL_MUTATION` — mutate an isolated/local working artifact without changing a shared remote frontier;
- `REMOTE_MUTATION` — change a shared repository/file/app frontier within already-resolved authority;
- `AUTHORITY_MUTATION` — change a Current/authority-bearing object or pointer;
- `RELEASE_MUTATION` — publish/merge/release/deploy to a production-facing frontier when that action itself changes release state.

Select the **lowest sufficient class**. A higher-capability adapter must not be selected merely because it is available. Authority and release mutations require the corresponding existing authority/persistence gates; this section creates no new approval gate.

## 10｜Runtime adapter routing and bounded fallback

Default routing:

`CURRENT OWNER → REQUIRED NATIVE OUTPUT → ACTIVE CONSTRAINTS → CURRENT EXECUTION SURFACES → MINIMUM RELIABLE ADAPTER → SIDE-EFFECT CLASS → REAL EXECUTION`.

Rules:

- probe only capabilities relevant to the required native output;
- prefer an already-connected, agent-executable or approved shared runtime that can produce the required native result and readback;
- do not introduce a parallel task manager or state store when Notion/GitHub/Project Control already own that state;
- retries must be bounded and evidence-driven; repeated blind retries are forbidden;
- fallback must preserve the required native-output truth boundary and declare any capability loss;
- adapter failure does not authorize a new Skill/METHOD/Framework. Exhaust Current legal adapters first, then record the exact capability boundary or HOLD.

### 10A｜Unified capability-role router

The router is an execution rule inside this existing contract, not a new Plugin Framework.

Capability roles are:

- `AUTHORITY_READ_WRITE`
- `REPO_SOURCE_MUTATION`
- `ASSET_ARCHIVE_DELIVERY`
- `NATIVE_PRODUCTION`
- `RUNTIME_READBACK`
- `DEPLOYMENT`
- `HUMAN_COORDINATION`
- `SCHEDULED_WAKEUP`
- `HEAVY_EXECUTION`

Selection precedence is fixed:

`CURRENT AUTHORITY + OWNER BOUNDARY → REQUIRED NATIVE OUTPUT + MUTATION CAPABILITY → ACTIVE CONSTRAINTS + PERMISSION → LOWEST SUFFICIENT SIDE EFFECT → ACTUAL READBACK COVERAGE → CURRENT VERIFIED AVAILABILITY / RELIABILITY → LOWER EXECUTION OVERHEAD → DECLARED FALLBACK`.

Do not choose by vendor/brand name. “GitHub / Notion / Browser / Vercel / Slack / Work / another connector” is only a surface identity after the capability role has been resolved.

For a material routed execution, the route decision may record:

`required_capability_roles / candidate_surfaces / selected_surface / selection_reasons / availability_state / authority_ceiling / side_effect_class / readback_surface / fallback_surface`.

Unused route candidates are not persistent project state.

### 10B｜Probe discipline and liveness

Surface liveness states are:

`AVAILABLE / UNAVAILABLE / DEGRADED / UNKNOWN`.

Probe only when:

- the selected surface requires runtime confirmation;
- the previously selected surface failed;
- a fallback must be evaluated.

Do not probe every connected surface for inventory curiosity. If one verified sufficient surface is already available, an unrelated `UNKNOWN` surface does not block execution.

Availability is a runtime fact, not Authority. A connector becoming available or unavailable does not rewrite Project State, Source Authority or Design Authority.

### 10C｜Producer / readback separation

Prefer a distinct readback surface when practical, e.g. repository mutation → browser/runtime readback, deployment → browser readback, Notion mutation → re-fetch/drift check.

If the same surface must both mutate and read back because no alternative exists, record the readback as `NOT_INDEPENDENT`. The absence of another surface does not justify silently claiming independent review. This does not create a new reviewer role.

### 10D｜Remote mutation idempotency / verify-before-retry

For `REMOTE_MUTATION / AUTHORITY_MUTATION / RELEASE_MUTATION`, define a stable operation fingerprint and a readable expected postcondition before create-like or otherwise nontrivial writes whenever practical.

Material evidence fields are:

`operation_fingerprint / expected_postcondition / outcome_state / verification_surface / retry_decision`.

`outcome_state = CONFIRMED_SUCCESS / CONFIRMED_FAILURE / UNCERTAIN`.

If a connector times out or otherwise returns an uncertain outcome, do **not** retry the write first. Use:

`UNCERTAIN → READBACK EXPECTED POSTCONDITION → FOUND = NORMALIZE CONFIRMED_SUCCESS / NO RETRY → ABSENT = RETRY ONLY WHEN OPERATION IS IDEMPOTENT OR PROVIDER-KEYED AND RETRY BUDGET REMAINS`.

A create-like operation whose absence cannot be established and which has no safe idempotency mechanism must `HOLD_RETRY_UNSAFE_OR_EXHAUSTED`; it must not create a duplicate PR, page, deployment, upload, message or other remote side effect.

The operation fingerprint is runtime evidence, not another state database. Verification readback remains ephemeral unless an existing persistence trigger applies.

## 11｜Selective readback and validator separation

Readback scope follows the **mutation blast radius**:

`MUTATION SCOPE → AFFECTED DEPENDENCIES / SURFACES → SMALLEST SUFFICIENT ACTUAL READBACK → VERDICT`.

Examples:

- presentation/CSS mutation → affected page/component plus relevant responsive/runtime state;
- code/runtime mutation → affected execution path plus applicable tests/runtime readback;
- Blender/object mutation → affected object/dependencies plus actual geometry/viewport/render readback as applicable;
- Current Authority or cross-platform pointer mutation → authority/drift readback, not a narrow artifact-only check.

If the blast radius cannot be bounded reliably, widen the readback instead of assuming locality.

Where practical, use a different evidence channel for validation than for production, e.g. repository mutation → runtime/browser readback, deployment → browser readback, Notion mutation → re-fetch/drift check. This is evidence-channel separation; it does not create another reviewer role beyond the existing DAG contract.

## 12｜Ephemeral outputs and persistence throttle

Search results, tool logs, failed attempts, console output, temporary screenshots, intermediate deployment URLs, transient adapter state, unused route candidates, surface-liveness probes and idempotency verification readback are **EPHEMERAL by default**.

They may be promoted to an existing persistent surface only after the applicable sequence:

`ACTUAL READBACK → REVIEW / VALIDATION AS APPLICABLE → MATERIAL DELTA → EXISTING PERSISTENCE TRIGGER`.

Therefore:

- plugin output ≠ Knowledge;
- runtime trace ≠ Project State;
- temporary screenshot ≠ Design Authority;
- scheduler run ≠ material delta;
- route candidates ≠ plugin inventory authority;
- idempotency verification readback ≠ a new operation ledger;
- no material delta = no new page, Candidate, receipt instance or commit solely to record that the adapter ran.

## 13｜Heavy executor escalation boundary

A Work-like or other resource-heavy multi-step executor is **escalation-only**, not the default OLEANDER control plane.

Escalation is justified only when a lighter Current adapter is insufficient and the task materially benefits from one or more of:

- long low-judgment repetitive execution;
- substantial cross-application navigation;
- GUI-bound operations that exposed connectors/runtimes cannot legally perform;
- large bounded batches whose execution overhead is lower in the heavy executor than in repeated control-plane turns.

Do not default-escalate when:

- an existing connector/API/runtime can perform the mutation directly;
- the task requires frequent visual/design judgment between steps;
- the work is a small-step continuation of one Current project object;
- validation/readback quality is more important than execution volume.

Heavy-executor output is at most `EXECUTED` until the ordinary OLEANDER readback, regression/review as applicable and Flow Completion Gate are satisfied. It must not self-promote to `VERIFIED`, `DESIGN KEEP`, `CURRENT` or `CLOSED`.
