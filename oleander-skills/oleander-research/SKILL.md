---
name: oleander-research
description: Build and maintain the evidence base for the Oleander project in the current Notion knowledge architecture. Use whenever the user mentions Oleander research, precedent studies, reference sourcing, benchmark discovery, site/context analysis, source comparison, interaction/product/visual precedents, how-made deconstruction, interview synthesis, research matrices, claims, citations, assumptions, or turning project knowledge into a traceable brief.
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

## Reference sourcing + how-made deconstruction capability

Use this branch when the task is not only "find evidence" but "find better precedents and understand how they were made".

### 1. Route the reference source by the actual gap

Start from `claim / failure / representation gap / implementation gap`, then choose the strongest source path instead of browsing one inspiration site by default:

- **Curated discovery**: awards, curated galleries, portfolio aggregators. Use for option-space expansion and author discovery only.
- **Original work / studio case**: original project site, agency/studio case study, brand or institution page. Use to recover the complete sequence, role split and project intent.
- **Authorship chain**: follow agency → art director/designer → developer → 3D/motion/photography contributors → talks/interviews/process/repositories. Use to identify repeated design moves and implementation habits.
- **Interaction / pattern sources**: platform HIGs, design systems, real product flows, interaction recordings and pattern libraries. Deconstruct `trigger → action → feedback → state → recovery/return`.
- **How-made / technical sources**: DevTools, source repositories, framework/plugin docs, shaders, WebGL/Three.js, GSAP, SVG/CSS/JS, state machines, asset-loading and responsive implementation. Use when the visual/interaction effect is understood but cannot yet be reproduced.
- **3D / product / industrial sources**: original product pages, patents, teardown/repair manuals, assembly instructions, CAD/technical documentation. Use for structure, access, assembly, hidden relation, exploded/section/body-use/CMF claims.
- **Material / CMF / light sources**: material manufacturers, coating/process suppliers, sample libraries, real product detail pages, lighting/photography documentation. Use for substrate, finish, roughness, reflectance, texture scale, edge/highlight behavior, aging and process limits.
- **Typography / editorial / brand sources**: original identity case studies, editorial systems and documented type usage. Use for hierarchy, measure, scale, rhythm, image–type relation and brand voice.
- **Standards / evidence sources**: official standards, HIGs, accessibility guidance, engineering/vendor documentation. Use to test whether a reference move is valid, not merely attractive.
- **Adjacent-domain sources**: film, game HUD, automotive HMI, exhibition, stage/light, museum and publishing. Use when the same relation/problem is solved better outside the current discipline.
- **Historical / canonical sources**: established design/architecture/product/interaction precedents. Use to distinguish durable mechanisms from current visual fashion.
- **Internal OLEANDER first**: always search existing METHOD / PRACTICE / CASE / EVIDENCE / known failures before external discovery to avoid duplicate learning.

### 2. Follow the source chain to the original mechanism

Default chain:

`DISCOVERY → ORIGINAL WORK → AUTHOR/STUDIO → PROCESS/HOW-MADE → TECHNICAL/STANDARD EVIDENCE → EDITABLE REPRODUCTION → MUTATION → PROJECT-SCOPED REBUILD`

Do not stop at a screenshot, award page, Pinterest-like board, social post, repost or secondary article when the original source is recoverable.

### 3. Deconstruct the mechanism, not just the appearance

Depending on the medium, inspect the variables that actually produce the effect:

- visual/editorial: composition, dominant field, hierarchy, type scale, spacing, crop, image-text binding, color role;
- image: camera/claim, crop, mask, tonal hierarchy, compositing, texture/detail treatment;
- web/UI: DOM/layer structure, responsive rules, state model, navigation, discoverability, loading/error/return, mobile degradation;
- motion: trigger, timing, easing, continuity, state transition, reduced-motion behavior;
- 3D/product: geometry hierarchy, camera, section/exploded/orbit strategy, material response, lighting, scale/body-use relation;
- CMF/light: substrate, finish, gloss/roughness, reflection/highlight flow, texture scale, illumination and viewing condition;
- data/dashboard: task, metric relationships, update/state logic, comparison load and whether a dashboard is actually necessary.

Record `WHAT WORKS → HOW IT IS MADE → WHY IT FITS THE TASK → FAILURE / MISREAD → WHAT IS TRANSFERABLE → WHAT MUST NOT BE COPIED`.

### 4. Reproduce before claiming the capability is learned

A reference becomes reusable OLEANDER learning only after:

`CASE DECONSTRUCTION → SMALL EDITABLE REPRODUCTION → MATERIAL MUTATION → ACTUAL READBACK → PROJECT-SCOPED REBUILD when a real fit exists`.

Prefer HTML/CSS/SVG/JS, Blender/native 3D, editable vector/layout/image-treatment sources. Do not treat screenshots or raster mockups as proof of implementation capability when an editable reconstruction is feasible.

### 5. Imitation boundary

Method-level imitation is allowed and expected when it improves capability: composition logic, sequence, camera strategy, interaction pattern, motion timing, light/material reveal, component structure and technical implementation may be reproduced and mutated for learning.

Do not copy another project's logo, proprietary copy, unique illustration/photography, distinctive branded assets or whole-page pixel structure into a Current project. If the reconstruction remains recognizably dependent on the reference, change claim structure, composition, sequence, asset language or interaction logic before project use.

### 6. Source-strength rule

Curated sites, social media, forums and screenshots are discovery sources, not strong evidence by themselves. Pursue original studio/author/official/technical sources when available. When the chain cannot be verified, label it `REFERENCE ONLY / SOURCE WEAK` and prevent it from becoming a canonical rule.

### 7. Anti-collection rule

Do not write every browsed link into OLEANDER. A reference only earns CASE/EVIDENCE/PRACTICE lineage when it materially enters deconstruction, comparison, reproduction, mutation or project transfer.

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
2. Evidence/reference table with source strength and original-source status
3. Design implications or transferable design moves
4. How-made mechanism when reference deconstruction was requested
5. Risks, contradictions and imitation/evidence boundaries
6. Open questions
7. Current Notion objects/relations created or updated, including their Canonical ID / role / registry location when relevant

## Quality checks

- No unsupported quantitative claim.
- No source without date/provenance when available.
- Facts, interpretations, assumptions and decisions are visibly distinct.
- Conflicting evidence is retained and explained.
- Discovery references are not presented as canonical evidence without source-chain verification.
- Reference study identifies mechanism and failure boundary, not only visual resemblance.
- When how-made learning is claimed, an editable reproduction/readback exists or the missing execution capability is explicitly reported.
- Every Notion write targets a live Current Registry object/relation, not dead or superseded navigation.
- Current hierarchy uses `Canonical Parent / Canonical Children`; legacy hierarchy fields are not used for routing.
- Domain, Source, Method, Project, Related and Supersession semantics remain separate.
- No parallel Notion taxonomy/page tree is created by default.
- The result is usable by `oleander-design-process`, `oleander-data-viz`, `oleander-story-and-board`, `oleander-image-art-direction`, `oleander-web-ui`, `oleander-motion`, and `oleander-3d-pipeline`.
