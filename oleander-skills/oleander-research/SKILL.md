---
name: oleander-research
description: Build and maintain the evidence base for the Oleander project in the current Notion knowledge architecture. Use whenever the user mentions Oleander research, precedent studies, site/context analysis, source comparison, interview synthesis, research matrices, claims, citations, assumptions, or turning project knowledge into a traceable brief.
compatibility: Requires connected Notion for publishing; browser/PDF/document/spreadsheet tools may be used for evidence gathering.
---

# Oleander Research

Turn heterogeneous research into a decision-ready, traceable knowledge system. Treat the current Notion root Authority and live Registry as canonical; do not introduce Zotero or a parallel Notion page tree.

## Current Notion authority preflight

Before reading or writing research knowledge:

1. Read `OLEANDER｜设计知识库（Design）` Current Authority and any applicable Project State / Source Authority / Current Task.
2. Resolve the live Registry through `SYS-REGISTRY｜Current System Registries｜ACTIVE v1.0`.
3. Use `00-governance/runtime/OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.md/.json` as the GitHub-side execution mirror.
4. Resolve current Domain / L0–L7 / Knowledge Role / Canonical ID / governance and evidence state before choosing a write target.
5. Do not use historical `00–70` page ancestry, old `上位笔记 / 子级笔记`, Legacy labels, or a search-result title as current routing authority.

## Workflow

1. Define the research question, decision it informs, geographic/time scope, and required confidence.
2. Search existing current OLEANDER knowledge objects and live Registry relations before adding material.
3. Register or link each source with title, organization/author, date, URL or file reference, access date, source type, geography, and reliability when applicable.
4. Separate:
   - evidence: directly supported facts;
   - interpretation: analysis derived from evidence;
   - assumption: plausible but unverified;
   - decision: an agreed project direction.
5. Build a comparison matrix when there are three or more cases, repeated attributes, or competing options.
6. Link every important claim to its supporting Source/Evidence object or clearly label it as an inference.
7. End with design implications, unresolved questions, and the next research action.
8. Write back only to the correct live Registry object/relation and perform readback.

## Notion location and relation contract

Do **not** create generic parallel pages/databases such as `Research index`, `Sources`, `Precedents`, `Site and context`, `Insights and hypotheses`, `Decisions`, or `Open questions` merely because this Skill is running.

Use the existing current architecture instead:

- **Domain Registry / L0–L3**: Domain identity, taxonomy and MOC only.
- **Notes Registry / L4–L7**: Frameworks, knowledge objects, METHOD, THEORY, SOURCE, CASE, EVIDENCE, TOOL, PRACTICE and Output正文.
- **Project Registry / P0–P4**: actual project application, workstream and validation identity.
- **People Registry**: author, designer, researcher, institution or authority relations when needed.
- **Inspiration Registry**: unresolved inputs only; mature knowledge must be promoted into the appropriate Notes/Project object rather than left as inspiration.
- **Resources Registry**: reusable assets/templates/tools; resources do not replace knowledge claims.

Current structural hierarchy uses only:

- `Canonical Parent｜层级上位`
- `Canonical Children｜层级子级`

Use dedicated relations for distinct semantics:

- Source/provenance → `来源文档 / 引用该来源的文档`
- Method invocation → `引用方法 / 引用该方法的文档`
- Project use → current project relations + `Project ID｜项目ID`
- Semantic adjacency → `相关笔记`
- Supersession → `替代文档 / 被替代文档`

For a current METHOD or research method object, resolve its existing `Canonical ID`, `知识角色`, current L2 `主领域`, optional `关联领域`, `方法家族`, Source relation and evidence state. Do not create one Notion Domain or one GitHub Skill per method.

## Required output

Provide:

1. Executive synthesis
2. Evidence table
3. Design implications
4. Risks and contradictions
5. Open questions
6. Current Notion objects/relations created or updated, including their Canonical ID / role / registry location when relevant

## Quality checks

- No unsupported quantitative claim.
- No source without date/provenance when available.
- Facts, interpretations, assumptions and decisions are visibly distinct.
- Conflicting evidence is retained and explained.
- Every Notion write targets a live Current Registry object/relation, not dead or superseded navigation.
- Current hierarchy uses `Canonical Parent / Canonical Children`; legacy hierarchy fields are not used for routing.
- Domain, Source, Method, Project, Related and Supersession semantics remain separate.
- No parallel Notion taxonomy/page tree is created by default.
- The result is usable by `oleander-data-viz` and `oleander-story-and-board`.
