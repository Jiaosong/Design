# OLEANDER Default Skill Resolver v1.1

Status: **ACTIVE CURRENT CANDIDATE FOR MAIN**  
Decision date: **2026-08-18**  
Scope: **ALL OLEANDER projects / conversations / agents / media**  
Notion Current Authority: **OLEANDER｜设计知识库（Design） v1.1.1**  
Execution implementation: **GitHub `Jiaosong/Design`**

## 0｜Purpose

This resolver keeps OLEANDER knowledge architecture and execution architecture separate without losing either one.

Notion owns current knowledge identity, naming, location, hierarchy, source relations, method relations and project relations. GitHub owns executable Skills, candidate specialists, runtime adapters, validators, regression fixtures and implementation history.

The current invariant is:

> **CURRENT ROOT AUTHORITY → LIVE REGISTRY → CURRENT DOMAIN / L0–L7 → KNOWLEDGE ROLE + CANONICAL ID → CURRENT KNOWLEDGE OBJECTS / SOURCES / METHODS / PRACTICE → EXISTING MATURE DESIGN → GITHUB EXECUTABLE SKILL → REQUIRED NATIVE OUTPUT → CAPABILITY PROBE → REAL EXECUTION → ACTUAL READBACK → EVIDENCE GATE + INDEPENDENT DESIGN QUALITY GATE → GAP DIAGNOSIS → OPTIMIZE EXISTING SKILL ONLY IF NEEDED**

This resolver supplements the Universal Production Environment. It does not create a parallel project-state system, method registry, Notion taxonomy, review framework or tool environment.

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

## 3｜Current capability layers

### Layer A — Installed reusable execution skills

The installed execution registry remains `oleander-skills/REVIEW.md`:

1. `oleander-research`
2. `oleander-data-viz`
3. `oleander-3d-pipeline`
4. `oleander-story-and-board`
5. `oleander-delivery-qc`
6. `oleander-motion`

These are execution capabilities, not Notion taxonomy nodes and not the full knowledge inventory.

### Layer B — Candidate specialist execution skills on main

- `oleander-game-ui`
- `oleander-mobile-game-ui`
- `oleander-ui-visual-composition`
- `oleander-route-wayfinding-ui`
- `oleander-ui-interaction`

`oleander-game-ui-stack` is an aggregation/routing layer, not an extra independent specialist.

Candidate status remains explicit. File existence, merge or CI green does not silently promote a candidate.

### Layer C — Specialist development

Technical Drawing remains a candidate body until explicit independent promotion. Do not report it as installed merely because implementation files or a PR exist.

### Layer D — Notion design intelligence

The live Notion Notes Registry contains the broader reusable METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE inventory. Query live objects and current relations instead of hard-coding a count.

## 4｜Default GPT / Agent behavior

When the user says any equivalent of “按 OLEANDER 做”, “继续项目”, “用已有 Skill”, “审查”, “训练”, “做成实际成果”, or “不要重新发明方法”:

1. Read the current Notion root Authority and applicable Project State / Source Authority / Current Task.
2. Resolve live registry identity before following historical navigation or recovery manifests.
3. Resolve current Domain, L0–L7 position, knowledge role, Canonical ID, Canonical Parent/Children and evidence state.
4. Retrieve task-relevant current METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE objects.
5. Reuse existing mature design, design source and current project assets before inventing replacements.
6. Resolve an existing GitHub reusable Skill or candidate specialist that reasonably owns execution.
7. Define the required native output: editable vector, geometry, HTML/CSS/JS, structured data, PDF, model, video, etc.
8. Probe the current execution surface and choose the best-fit production adapter.
9. Produce the actual artifact instead of stopping at a method description when production is requested.
10. Open/render/run the actual result and perform real readback.
11. Keep Evidence Gate and independent Design Quality Gate separate.
12. Diagnose the root cause of failure.
13. Optimize an existing Skill only when execution/readback proves a reusable capability gap.
14. Create a new Skill only when no existing Skill can reasonably own the capability.
15. Write new Notion knowledge/application evidence back to the correct live registry and dedicated relation; never create a parallel page tree by default.
16. Synchronize material delta and preserve superseded/history provenance.

## 5｜Existing-first rule

Canonical rule:

`CURRENT ROOT AUTHORITY → LIVE REGISTRY / CURRENT KNOWLEDGE → EXISTING MATURE DESIGN / DESIGN SOURCE → CURRENT PROJECT DELTA → EXISTING GITHUB SKILL → REQUIRED NATIVE OUTPUT → REAL EXECUTION → ACTUAL READBACK → GAP DIAGNOSIS → OPTIMIZE EXISTING SKILL IF NEEDED → NEW SKILL ONLY IF NO EXISTING OWNER EXISTS`

Forbidden reasons for creating a new Skill by themselves:

- a case is interesting;
- a new method page exists;
- a new name sounds useful;
- a training note exists;
- a PR or file can be created;
- CI is green;
- a one-off visual problem occurred before trying an existing owner;
- the specialization can be a method/module under an existing execution owner.

One Notion METHOD must not automatically become one GitHub Skill. One GitHub Skill must not automatically become a new Notion Domain.

## 6｜Production-first rule

Design tasks default to real editable/auditable production, not documentation-only or AI-image substitution.

- UI / web / interaction: real editable interface implementation first.
- Spatial / architecture / landscape: real geometry, vector drawings, plans/sections/axonometric or model assets first.
- Product / CMF: real form/material/process assets and editable specifications first.
- Data / information: source-bound data structures and editable vector/interactive outputs first.
- Motion: real state/motion implementation and runtime readback first.

AI-generated images are supplementary visualizations when appropriate. They do not replace design authority, geometry, technical dimensions, editable text or real production assets.

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

A producer/runtime may report execution and self-check evidence, but cannot self-promote its artifact to a KEEP-class verdict where independent review is required.

## 8｜No-loss default

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`

Reorder, split, expand, reweight and change presentation rhythm when needed. Do not delete valid design systems, evidence, audience depth, physical/sensory content, memory/IP, technical proof, return logic or other valid content merely to simplify a project.

The same rule applies to knowledge migration: consolidate duplicates, but preserve Canonical identity, source chain, method boundary, evidence state, project use and Legacy provenance.

## 9｜Truth and relation boundary

Keep these roles distinct:

- Current Authority
- live Registry identity
- Domain identity
- Canonical knowledge identity
- Source Authority
- Design Authority
- Native Source
- Derived Asset
- Diagnostic Asset
- Render / Preview
- Prototype
- Field Evidence
- Promotion State

In Notion, keep Canonical hierarchy separate from Source, Method, Project, Related and Supersession relations.

Derived diagrams, render meshes, websites, videos and previews cannot silently replace source, geometry or design authority.

## 10｜Synchronization rule

For a material resolver/architecture change:

1. resolve and read back the current Notion root authority and live registry state;
2. update GitHub binding/resolver implementation through branch → commit → PR → CI/readback;
3. update Notion only if a new cross-platform pointer or material current fact is required, writing to a live Current Authority/registry object rather than dead lineage;
4. keep one current GitHub default resolver pointer;
5. preserve older resolver files and historical Notion navigation as provenance;
6. do not treat chat summaries as Project State or authority.

## 11｜Does not prove

This resolver being ACTIVE does not promote every Notion method or GitHub candidate Skill. It establishes how OLEANDER resolves current knowledge location and then execution capability. Individual method validation, project evidence, independent design review, engineering/field truth and release/promotion remain separate gates.
