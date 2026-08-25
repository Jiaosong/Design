# OLEANDER Default Skill Resolver v1.1

Status: **SUPERSEDED BY v1.2**  
Decision date: **2026-08-18**  
Scope: **ALL OLEANDER projects / conversations / agents / media**  
Notion Current Authority: **OLEANDER｜设计知识库（Design） v1.1.1**  
Execution implementation: **GitHub `Jiaosong/Design`**

> Current pointer: `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.md/.json`. This v1.1 file remains implementation provenance and must not be used as the Current default after v1.2 promotion.

## 0｜Purpose

This resolver keeps OLEANDER knowledge architecture and execution architecture separate without losing either one.

Notion owns current knowledge identity, naming, location, hierarchy, source relations, method relations and project relations. GitHub owns executable Skills, candidate specialists, runtime adapters, validators, regression fixtures and implementation history.

The v1.1 invariant was:

> **CURRENT ROOT AUTHORITY → LIVE REGISTRY → CURRENT DOMAIN / L0–L7 → KNOWLEDGE ROLE + CANONICAL ID → CURRENT KNOWLEDGE OBJECTS / SOURCES / METHODS / PRACTICE → EXISTING MATURE DESIGN → GITHUB EXECUTABLE SKILL → REQUIRED NATIVE OUTPUT → CAPABILITY PROBE → REAL EXECUTION → ACTUAL READBACK → EVIDENCE GATE + INDEPENDENT DESIGN QUALITY GATE → GAP DIAGNOSIS → OPTIMIZE EXISTING SKILL ONLY IF NEEDED**

v1.2 supersedes this execution order by inserting the Current machine-readable execution contract layer. All remaining sections below are retained as provenance for v1.1 behavior.

## 1｜Notion current architecture is upstream authority

Before any historical navigation page, method index, Skill file or recovery manifest, read the current root authority:

- `OLEANDER｜设计知识库（Design）`
- page ID `9150e089-9a7d-4b29-b026-175fca3a41b3`

Then resolve the current live registry through:

- `SYS-REGISTRY｜Current System Registries｜ACTIVE v1.0`
- page ID `3bbb86be-5c47-8164-b2ea-fee7d29ed2c0`

GitHub implementation of this Notion contract:

- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.md`
- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.json`

### Current physical knowledge location

- Domain Registry: L0–L3 Domain identity / taxonomy / MOC.
- Notes Registry: L4–L7 Framework / Knowledge Object / Evidence / Case / Practice / Output.
- Project Registry: P0–P4 application and validation identity; Project ID and Case ID remain separate axes.
- People / Inspiration / Resources remain relation objects and do not replace knowledge正文.

Current structural hierarchy uses only:

- `Canonical Parent｜层级上位`
- `Canonical Children｜层级子级`

Legacy `上位笔记 / 子级笔记` are migration provenance only and are forbidden for current AI routing or new writes.

### Method identity

A METHOD is a current Notes Registry knowledge object, normally with:

- Canonical ID `MTH-*`;
- `知识角色 = METHOD`;
- current governance / relation state;
- L4 or L5 according to actual structural responsibility;
- exactly one resolved Current L2 `主领域` when taxonomy is closed;
- optional `关联领域`;
- `方法家族` classification metadata;
- source relation and evidence state.

Method use is expressed by `引用方法 / 引用该方法的文档`, not by abusing Canonical Parent.

## 2｜Historical navigation is not current storage authority

Old physical `00–70` navigation pages, including historical `20｜General Design Knowledge` and `50｜Methods & Design Intelligence`, remain searchable provenance and may contain later explicit Current Override/index blocks.

Default rule:

- do not use old navigation ancestry as current hierarchy;
- do not write new current facts into dead/superseded navigation;
- do not infer current Domain from old page title, page parent or `LEGACY｜知识领域标签`;
- an explicit later Current Override may be used as a discovery surface only after root authority is read;
- live registry fields, Canonical ID, Domain, Canonical Parent/Children and dedicated relations remain authoritative.

The existing Notion object `KN-METHOD-OLEANDER-SKILL-RESOLVER-001` is a method-resolution/index aid. It is subordinate to the current root authority and live registry contract; it is not a second knowledge architecture.

## 3｜Current capability layers at v1.1

### Layer A — Installed reusable execution skills

The installed execution registry remains `oleander-skills/REVIEW.md`:

1. `oleander-research`
2. `oleander-data-viz`
3. `oleander-3d-pipeline`
4. `oleander-story-and-board`
5. `oleander-delivery-qc`
6. `oleander-motion`

### Layer B — Candidate specialist execution skills on main

- `oleander-game-ui`
- `oleander-mobile-game-ui`
- `oleander-ui-visual-composition`
- `oleander-route-wayfinding-ui`
- `oleander-ui-interaction`

`oleander-game-ui-stack` is an aggregation/routing layer, not an extra independent specialist.

### Layer C — Specialist development

Technical Drawing remains a candidate body until explicit independent promotion.

### Layer D — Notion design intelligence

The live Notion Notes Registry contains the broader reusable METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE inventory.

## 4｜Default GPT / Agent behavior at v1.1

1. Read the current Notion root Authority and applicable Project State / Source Authority / Current Task.
2. Resolve live registry identity before historical navigation.
3. Resolve current Domain, L0–L7, role, Canonical ID, Canonical Parent/Children and evidence state.
4. Retrieve task-relevant current METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE.
5. Reuse mature design, design source and current project assets.
6. Resolve an existing GitHub reusable Skill or candidate specialist.
7. Define the required native output.
8. Probe the current execution surface and choose the best-fit production adapter.
9. Produce the actual artifact.
10. Perform real readback.
11. Keep Evidence Gate and independent Design Quality Gate separate.
12. Diagnose failure root cause.
13. Optimize an existing Skill only when a reusable capability gap is proven.
14. Create a new Skill only when no existing Skill can reasonably own the capability.
15. Write new Notion knowledge/application evidence to the correct live Registry/relation.
16. Synchronize material delta and preserve provenance.

## 5｜Existing-first rule

`CURRENT ROOT AUTHORITY → LIVE REGISTRY / CURRENT KNOWLEDGE → EXISTING MATURE DESIGN / DESIGN SOURCE → CURRENT PROJECT DELTA → EXISTING GITHUB SKILL → REQUIRED NATIVE OUTPUT → REAL EXECUTION → ACTUAL READBACK → GAP DIAGNOSIS → OPTIMIZE EXISTING SKILL IF NEEDED → NEW SKILL ONLY IF NO EXISTING OWNER EXISTS`

One Notion METHOD must not automatically become one GitHub Skill. One GitHub Skill must not automatically become a new Notion Domain.

## 6｜Production-first rule

Design tasks default to real editable/auditable production, not documentation-only or AI-image substitution.

## 7｜Review default

OLEANDER Artifact Review remains the review authority:

`Gate 1｜Compliance + Gate 2｜Professional Design`

Hard separations:

- `Artifact existence ≠ Design quality`
- `Traceability ≠ Professional finish`
- `Evidence correctness ≠ Visual excellence`
- `Process PASS ≠ MAIN KEEP`
- `Render PASS ≠ Design PASS`
- `Prototype PASS ≠ Field PASS`

## 8｜No-loss default

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`

## 9｜Truth and relation boundary

Keep Current Authority, live Registry identity, Domain identity, Canonical knowledge identity, Source Authority, Design Authority, Native Source, Derived Asset, Diagnostic Asset, Render / Preview, Prototype, Field Evidence and Promotion State distinct.

## 10｜Synchronization rule

For a material resolver/architecture change: read back Current Notion, update GitHub through branch → commit → PR → CI/readback, update Notion only for a Current pointer/fact, keep one Current GitHub resolver pointer, and preserve older resolver/history provenance.

## 11｜Does not prove

This superseded resolver remains historical implementation provenance only. It does not promote any METHOD, candidate Skill, project artifact, field/engineering claim or release state.
