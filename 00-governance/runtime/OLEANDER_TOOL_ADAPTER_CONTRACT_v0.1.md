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

Use `OLEANDER_SHARED_EXECUTION_SURFACES_v0.1` for the Current surface registry. Prefer role/capability routing over adding vendor-specific ontology.

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

Search results, tool logs, failed attempts, console output, temporary screenshots, intermediate deployment URLs and transient adapter state are **EPHEMERAL by default**.

They may be promoted to an existing persistent surface only after the applicable sequence:

`ACTUAL READBACK → REVIEW / VALIDATION AS APPLICABLE → MATERIAL DELTA → EXISTING PERSISTENCE TRIGGER`.

Therefore:

- plugin output ≠ Knowledge;
- runtime trace ≠ Project State;
- temporary screenshot ≠ Design Authority;
- scheduler run ≠ material delta;
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
