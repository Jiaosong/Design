# OLEANDER Tool Adapter Contract v0.1

Status: **CANDIDATE_FOR_CURRENT**  
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
