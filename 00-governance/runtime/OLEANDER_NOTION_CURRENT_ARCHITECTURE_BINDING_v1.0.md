# OLEANDER Notion Current Architecture Binding v1.0

Status: **ACTIVE CURRENT MIRROR**  
Source authority version: **OLEANDER Current Authority v1.1.1**  
Decision date: **2026-08-18**  
Scope: **GitHub execution routing into the current Notion knowledge architecture**

## 0｜Purpose

This file does not define a second knowledge architecture. It is a GitHub-side execution mirror of the current Notion authority so that reusable Skills, agents, automations and validators write to the correct Notion object, relation and location.

The binding rule is:

> **NOTION CURRENT ROOT AUTHORITY → LIVE REGISTRY IDENTITY → CURRENT DOMAIN / L0–L7 → KNOWLEDGE ROLE + CANONICAL ID → CANONICAL PARENT / CHILDREN → DEDICATED SOURCE / METHOD / PROJECT RELATIONS → GITHUB EXECUTION SKILL**

GitHub skill folders are execution handles. They are not Notion taxonomy nodes and must not create a parallel Notion directory tree.

## 1｜Current authority and registry

### Current root authority

- Page: `OLEANDER｜设计知识库（Design)`
- Page ID: `9150e089-9a7d-4b29-b026-175fca3a41b3`
- Role: unique current root authority / namespace lock / cross-platform routing authority.

This root must be read before historical `00–70` navigation pages or recovery manifests.

### Current registry control surface

- Page: `SYS-REGISTRY｜Current System Registries｜ACTIVE v1.0`
- Page ID: `3bbb86be-5c47-8164-b2ea-fee7d29ed2c0`
- Contract: the original Notes / Domain / Project / People / Inspiration / Resources registries are restored and remain the only live registries. Do not duplicate or import a second data source.

Current data-source identities are preserved:

- Notes: `collection://4668fc63-45a6-496e-a2cc-f9542928b9e8`
- Projects: `collection://d0f8f709-91b0-4c9b-bc0a-3ab05ec4a447`
- Domains: `collection://86d64b60-c5fd-4261-95e6-074cc45a344c`
- People: `collection://e2480d27-6fe7-454c-85ad-09c6b1ad52cc`
- Inspiration: `collection://9fb91568-2d06-4ee4-8b11-761b34b73daa`
- Resources: `collection://07b6f8f3-3e7a-434d-b536-4d823422b329`

## 2｜Current knowledge location contract

Current storage and hierarchy are relation-driven, not page-tree-driven.

### L0–L3｜Domain identity / taxonomy

Primary store: **Domain Registry**.

Use it for stable System / Branch / Domain / Topic identity and routing. Domain identity, domain content and canonical parent authority are separate questions.

For a knowledge object:

- `主领域` = exactly one current L2 Domain when resolved;
- `关联领域` = secondary / cross-domain support;
- Application Mapping `B / CU / IP / SP` must not be used as Domain identity.

### L4–L7｜Knowledge objects / evidence / practice / output

Primary store: **Notes Registry**.

- L4 = Framework / Cluster
- L5 = Knowledge Object / Index
- L6 = Evidence / Case
- L7 = Practice / Output

Methods, theories, tools, sources, cases, evidence, indices and practices stay as Notes Registry knowledge objects with the correct `知识角色` and evidence/governance state.

### Project use

Primary store: **Project Registry**.

Project Axis is separate from the knowledge axis. Use current `Project ID｜项目ID + 项目层级`; Case ID is a separate context/filter axis. Do not use Project/Case identity to replace Domain or Knowledge identity.

## 3｜Current hierarchy fields

Current physical structural hierarchy uses only:

- `Canonical Parent｜层级上位`
- `Canonical Children｜层级子级`

Rules:

- one-way structural meaning;
- a child normally has 0–1 Canonical Parent;
- children may be multiple;
- Source / Method / Project / Related / Supersession semantics must use their dedicated relations;
- legacy `上位笔记 / 子级笔记` are migration provenance only and are forbidden for current AI routing or new writes.

## 4｜Method identity and invocation

A current reusable method is a Notes Registry knowledge object, not a GitHub folder and not an old navigation page.

Resolve method identity through:

1. `Canonical ID` — normally `MTH-*` for method objects;
2. `知识角色 = METHOD`;
3. current governance / relation state;
4. content level, normally L5 unless it is a real L4 method framework;
5. exact `主领域` and optional `关联领域`;
6. `Canonical Parent / Canonical Children` when a live structural framework exists;
7. `方法家族` as classification metadata, never as hierarchy parent;
8. current Source relation / evidence state.

Method use is expressed through:

- `引用方法`
- `引用该方法的文档`

A Practice, Case, Project Output or other knowledge object using a METHOD must not make that METHOD its hierarchy parent merely to record use.

## 5｜Source, project, adjacency and version relations

Use dedicated relations:

- Source/provenance: `来源文档 / 引用该来源的文档`
- Method invocation: `引用方法 / 引用该方法的文档`
- Project use: current project relations and Project ID fields
- Semantic adjacency: `相关笔记`
- Version replacement: `替代文档 / 被替代文档`

Do not overload Canonical Parent with any of these semantics.

## 6｜Naming authority

For current routing, resolve identity in this order:

1. Current root Authority / explicit Current Closure or Override
2. live registry identity
3. Canonical ID / Project ID
4. governance + relation state
5. L0–L7 / P0–P4 level
6. Primary Domain / Project Parent
7. Knowledge Path / Project Path
8. Knowledge Role / runtime fields / evidence state
9. human-readable title
10. physical page position

A title may change. A page may move. Stable identity and current relations must survive both.

## 7｜Legacy navigation boundary

Historical physical navigation such as old `00–70` pages, including old `20｜General Design Knowledge` and `50｜Methods & Design Intelligence`, remains searchable provenance but is **not a default current write target or structural-routing authority**.

Exception: an old page may contain a later explicit `Current Override` or current resolver/index block. Such a block may be used as a discovery/index surface only after the current root authority is read. It still does not replace live registry fields, Canonical Parent/Children or current Domain routing.

Recovery manifests are also historical snapshots unless a later explicit Current Closure/Override or fresh live-registry contradiction reopens them.

## 8｜GitHub Skill binding contract

Every GitHub reusable or candidate Skill that reads/writes Notion must follow this order:

1. read current root authority;
2. resolve live registry identity;
3. resolve current Domain / level / role / Canonical ID;
4. retrieve current knowledge objects;
5. use dedicated relations rather than inventing navigation pages;
6. execute the production capability;
7. write Practice / Evidence / Project usage back to the correct registry and relation;
8. perform readback.

GitHub Skill names such as `oleander-research`, `oleander-data-viz` or `oleander-motion` are stable execution identifiers only. They must not be copied into Notion as L1/L2/L3 taxonomy unless Notion independently establishes that domain identity.

## 9｜Forbidden parallel structures

Do not create generic Notion page trees such as:

- `Research index / Sources / Precedents / Insights / Decisions`
- `Skill → Methods → Cases` page folders
- one Notion page or database per GitHub Skill
- one GitHub Skill per Notion METHOD

unless the current Notion registry/relations explicitly require such an object.

Prefer the existing six registries, current Domain routing, one Canonical knowledge object and relation/MOC/index views.

## 10｜Does not prove

This binding proves only that GitHub execution knows where and how to resolve current Notion knowledge. It does not prove:

- a method is validated;
- a candidate Skill is promoted;
- a project is Design PASS;
- a Source is sufficient for a specific claim;
- field / engineering / manufacturing reality is closed.
