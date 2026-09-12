# OLEANDER Notion Post-Sync Governance Audit — 2026-09-12

Status: **POST-SYNC GOVERNANCE ACTIVE / READER LAYER LIVE / ACADEMIC MIGRATION 4/7 / NO PERMANENT DELETE**

This audit starts after the `1,184 / 1,184` corpus reconcile closed. It does not create a new knowledge authority. Notion remains canonical; D1/Vectorize are derivative readback surfaces.

## Rules

- Read actual page content before identity, naming, path, duplicate, or lifecycle decisions.
- No bulk rename, move, delete, merge, or dedupe from metadata alone.
- Decision set: `KEEP / MERGE / SUPERSEDE / ARCHIVE / HOLD`.
- First pass is reversible: identity/property corrections and retrieval containment only; no permanent deletion.
- After every Notion mutation: live Notion readback -> normal `syncPage` -> D1/Vectorize readback -> audit receipt.

## Corpus Triage Snapshot

Verified against production D1 after full sync:

- Active documents: `1,184`
- Missing Canonical ID: `40`
- Blank title: `0`
- Missing governance state: `71`
- Missing relation state: `63`
- Duplicate non-empty Canonical IDs: `3 groups`
- Duplicate exact titles: `0 groups`

These are candidate counts only. They are not equivalent to defects until the corresponding page content and role are reviewed.

## Batch 01 — Canonical Collision Review

### A. `MTH-DESIGN-DOUBLE-DIAMOND-001`

Current carrier:

- Page `390b86be-5c47-8121-8748-cb089a5674c3`
- Title: `MTH-DESIGN-DOUBLE-DIAMOND-001｜双钻发散—收敛方法｜Double Diamond`
- `SUPPORT / SCOPED / METHOD / L5`
- Body explicitly defines the Current method boundary and points to the official source carrier.
- Decision: **KEEP canonical identity**.

Historical carrier:

- Page `3c6b86be-5c47-8116-9606-d59a7588bd71`
- Title: `PROVENANCE｜MTH-DESIGN-DOUBLE-DIAMOND-001｜2026-08-24 Duplicate Carrier → Current Canonical`
- `PROVENANCE / HISTORY_ONLY`
- Body explicitly states: “This duplicate carrier no longer owns `MTH-DESIGN-DOUBLE-DIAMOND-001`.”
- Defect: property-level Canonical ID still collides with the Current carrier.
- Shadow decision: **SUPERSEDE identity only; preserve body NO LOSS**.
- Proposed reversible Canonical ID: `LEGACY-MTH-DESIGN-DOUBLE-DIAMOND-001-DUP-20260824`.

### B. `SRC-KANO-1984-001`

Current carrier:

- Page `3c0b86be-5c47-8137-b063-c980aec07e35`
- Title: `SRC-KANO-1984-001｜Kano et al. 1984｜Attractive Quality and Must-Be Quality`
- `CURRENT / DEFAULT / SOURCE / L6`
- Body is the compact current source boundary with DOI/J-STAGE evidence and explicit non-supported claims.
- Decision: **KEEP canonical identity**.

Historical carrier:

- Page `3adb86be-5c47-8164-a89e-f7db5e372ade`
- Title: `A06｜Kano et al. 1984《Attractive Quality and Must-Be Quality》｜原始论文`
- `PROVENANCE / HISTORY_ONLY / SOURCE / L6`
- Body is an earlier evidence carrier with overlapping source facts and old-note corrections.
- Defect: it still owns the same Canonical ID as the Current source page.
- Shadow decision: **SUPERSEDE identity only; preserve evidence/history**.
- Proposed reversible Canonical ID: `LEGACY-SRC-KANO-1984-001-A06`.

### C. `EVD-SKILL-EXTERNAL-BATCH2-DIGEST-20260828`

Carrier 1:

- Page `3cab86be-5c47-8104-a6d9-e8c9660ff21c`
- Title: `...｜Typography + Iconography + IA + Layout + A11y + Wayfinding + Brand Rules`
- Body calls itself `External Skill Digestion Evidence｜Batch 2｜2026-08-28` and records PR #424 / merge `471b4454...`.
- Decision: **KEEP existing Batch2 Canonical ID**.

Carrier 2:

- Page `3cab86be-5c47-8172-897f-d3361f5dcbda`
- Title: `...｜Curation + Product Form + UI Tokens + OpenSCAD + Design Language`
- Body calls itself `External Skill Digestion Evidence｜Round 2｜2026-08-28` and records PR #427 / merge `a5d58f27...`.
- Defect: distinct evidence run incorrectly reuses Batch2 Canonical ID.
- Shadow decision: **KEEP page/content; correct identity only**.
- Proposed reversible Canonical ID: `EVD-SKILL-EXTERNAL-ROUND2-DIGEST-20260828`.

All three groups are already fail-closed outside accidental Current retrieval, so identity correction can be performed without deleting or merging content.

### Batch 01 Applied Readback

Applied through the bearer-protected governance route; each mutation returned `HTTP 200` and immediately ran normal `syncPage` readback.

- Double Diamond historical carrier -> `LEGACY-MTH-DESIGN-DOUBLE-DIAMOND-001-DUP-20260824`; content preserved; `PROVENANCE / HISTORY_ONLY` unchanged.
- Kano historical A06 carrier -> `LEGACY-SRC-KANO-1984-001-A06`; content preserved; `PROVENANCE / HISTORY_ONLY` unchanged.
- External Skill Batch 2 typography/IA evidence -> explicit `PROVENANCE / HISTORY_ONLY`; Canonical ID retained.
- External Skill Round 2 curation/product/OpenSCAD evidence -> `EVD-SKILL-EXTERNAL-ROUND2-DIGEST-20260828` + explicit `PROVENANCE / HISTORY_ONLY`.
- D1 canonical-collision re-query after writeback: **0 duplicate non-empty Canonical ID groups**.

The Round 2 page title still contains the former Batch2 ID prefix. That title mismatch is queued for the later Naming/Path pass; it is not silently rewritten during identity-only Batch 01.

## Batch 02 Queue — Zero-Body Candidates

D1 readback found `13` active pages with zero indexed body chunks. `unknown_block_ids=[]` and `markdown_truncated=0`, but zero body is not automatically “delete/blank”: index carriers and relation-only records can be legitimate.

Priority review classes:

- Two orphan design-history titles with no Canonical ID or governance metadata: `北欧设计：有机现代主义与人文温度`; `意大利设计：从理性主义到孟菲斯的造型革命` -> **HOLD for live-role/parent review**.
- Ten evidence/case carriers across `EVD-HERITAGE-*` and `EVD-STATEEXHIBITION-*` -> **HOLD for source/content completeness review; no false-completion promotion**.
- `PRAC-BJ-XJ01-20260812-01｜XJ01 CMF Foundation｜Business Practice` -> role is `INDEX`; **HOLD judgment until relation graph is read**.

### Batch 02 Live Readback

All 13 candidates were re-read from live Notion through `/v1/governance-page`:

- `markdown_length=0`
- `markdown_truncated=false`
- `unknown_block_ids=[]`

Therefore they are genuinely body-empty pages, not a markdown recovery failure.

The ten `EVD-HERITAGE-*` / `EVD-STATEEXHIBITION-*` pages retain real Source + Primary Domain relations, so they are evidence shells rather than disposable blanks. They were changed reversibly to:

- `governance_state=HOLD`
- `retrieval_space=PROVENANCE`
- `search_eligibility=HISTORY_ONLY`
- existing `relation_state=REVIEW` retained
- body and relations preserved

The two orphan design-history pages (`北欧设计：有机现代主义与人文温度`, `意大利设计：从理性主义到孟菲斯的造型革命`) have no body, Canonical ID, domain/source/replacement relations, role, or content level. They were contained as:

- `governance_state=HOLD`
- `relation_state=REVIEW`
- `retrieval_space=PROVENANCE`
- `search_eligibility=BLOCKED`

Their immediate sync result is `EXCLUDED`; the pages remain in Notion and were **not deleted**.

`PRAC-BJ-XJ01-20260812-01｜XJ01 CMF Foundation｜Business Practice` remains unchanged because `knowledge_role=INDEX`, `SUPPORT / SCOPED`, and an empty body can be legitimate for an index carrier. It requires relation/owner review before any mutation.

## Post-Batch Readback

- Duplicate non-empty Canonical IDs: `0 groups`.
- Missing Canonical ID among active retrieval documents: `38`, all `effective_space=PROVENANCE`; there is no missing-ID `CURRENT` page.
- Missing governance state: `69`.
- Missing relation state: `61`.
- Two fully orphan body-empty pages are now excluded from the derivative retrieval plane while retained canonically in Notion.
- Large counts of null explicit Retrieval Space / Search Eligibility are **not** treated as bulk defects; many pages intentionally rely on authority fail-closed behavior and require content review before explicitization.

## Next Queue

1. Batch 03: inspect the `38` remaining missing-Canonical pages in content-sized batches; all are currently PROVENANCE, so no emergency bulk mutation is required.
2. Prioritize large legacy architecture/domain pages (`D01–D08`, `K03`, `K05`, source Axx pages) by content/authority rather than by title alone.
3. Perform a separate Naming/Path pass after identity decisions; do not combine title cleanup with authority changes.
4. Continue missing governance/relation candidates in small content-read batches, with mutation -> live readback -> D1 readback receipts.

## Phase 2 — Human Reader Layer

The user-facing problem was not only metadata correctness. The live Notion workspace exposed governance, provenance, evidence, practice, Current knowledge, migration logs and machine IDs on the same visual plane. A read-only audit found that the existing database views were predominantly audit/governance views rather than a human-first library; L6 Evidence objects also numerically dominate the corpus, so a flat table naturally feels like a warehouse rather than a knowledge system.

One navigation-only root child was therefore created without duplicating the Notes database:

- Page: `知识阅读台｜Knowledge Reader`
- Page ID: `3d9b86be-5c47-81e7-9acd-d05c6d25ad7b`
- Core Knowledge view: `L4/L5 + ACTIVE + VALID`
- Methods view: `METHOD + ACTIVE + VALID`
- Evidence view: `L6 + ACTIVE + VALID`
- Practice view: `L7 + ACTIVE`
- History view: `PROVENANCE` or `LEGACY / ARCHIVED / HOLD`

The initial Core view intentionally does not require explicit `Retrieval Space=CURRENT`. Most migrated knowledge objects still rely on inferred authority and have null explicit Retrieval Space; a strict CURRENT-only view would falsely make the library appear nearly empty. As migration progresses, a strict Current tab can be promoted later.

## Phase 2 — Academic Quality Gate

The D01–D08 / K03 / K05 audit confirmed that high word count was being mistaken for research quality. Common defects included strong `必须 / 应 / 不能` statements without claim-level citations, literature lists disconnected from argument, repeated G0–G9/POE material across pages, coarse A/B/C evidence grades, and missing independent `Limitations / Applicability` sections.

New Current METHOD owner:

- `MTH-KNOWLEDGE-ACADEMIC-NOTE-001｜论文级知识页：论点、证据、反例与适用边界`
- `CURRENT / DEFAULT / ACTIVE / VALID / L5 / METHOD`
- Requires testable/conditional thesis, claim-level evidence, rival/counterevidence, reproducible method where relevant, explicit limitations, and reader-first placement of system/provenance notes.
- Separates `FACT / INTERPRETATION / NORMATIVE RULE / HEURISTIC / HYPOTHESIS / DECISION` so normative rules are not laundered into facts.
- Evidence quality is treated as multi-axis (`Authority / Type / Quality / Applicability / Confidence`) rather than one scalar letter grade.

L6 Source/Evidence and L7 Practice are exempt from essay-style inflation. Their quality comes from identity, boundary, source precision and execution readback, not academic prose length.

## Phase 2 — First Academic Migration

### D01 urban regeneration

New Current carrier:

- Page ID: `3d9b86be-5c47-81b9-afdd-ea21838fdc16`
- Canonical ID: `KN-ARCH-URBAN-REGEN-001`
- Human title: `城市更新：空间改善、产权治理与反置换机制`
- `CURRENT / DEFAULT / ACTIVE / VALID / L5 / THEORY`
- Live markdown readback: `6,440` characters, `18` indexed chunks, not truncated.
- Structure: abstract -> research question/boundary -> property/value/power -> displacement/gentrification -> participation -> public/green-space distribution -> six-dimension evaluation -> research-to-design evidence chain -> limitations/applicability -> conclusion/references.

Old `D01｜城市更新与社区营造` remains intact (`18,701` live markdown characters) and is now:

- `LEGACY-KN-ARCH-URBAN-REGEN-D01-20260807`
- `LEGACY / PROVENANCE / HISTORY_ONLY / VALID`
- Reciprocal replacement relation points to the new Current page.

No old text was deleted.

## Phase 2 — Research Method Owner

New Current METHOD:

- Page ID: `3d9b86be-5c47-8158-bf00-c8aa879f7394`
- Canonical ID: `MTH-ARCH-RESEARCH-001`
- Human title: `建筑研究方法：问题、证据、有效性与伦理`
- `CURRENT / DEFAULT / ACTIVE / VALID / L5 / METHOD`
- Live markdown readback: `5,133` characters, `16` indexed chunks, not truncated.

It now owns research questions, concept operationalization, case/sample selection, fieldwork, research ethics, measurement/simulation boundaries, POE, triangulation, negative cases/rival explanations, validity/auditability/reflexivity and limitations. Topic pages should link this owner instead of copying their own generic POE/sampling/triangulation rules.

Old `D08｜建筑研究方法与批评` remains intact and is now `LEGACY-MTH-ARCH-RESEARCH-D08-20260730 / LEGACY / PROVENANCE / HISTORY_ONLY / VALID`, with a reciprocal replacement relation to the Current method.

## Phase 2 — Evidence Governance Owner

New Current METHOD:

- Page ID: `3d9b86be-5c47-81c6-ac53-fd563117d66c`
- Canonical ID: `MTH-ARCH-EVIDENCE-GOV-001`
- Human title: `建筑证据治理协议：权威、适用性、版本与冲突`
- `CURRENT / DEFAULT / ACTIVE / VALID / L5 / METHOD`
- Live markdown readback: `4,744` characters, `16` indexed chunks, not truncated.

The protocol separates `Authority / Evidence Type / Quality / Applicability / Temporal Validity / Project Closure`, removes the old assumption that one A/B/C/D rank can represent all evidence quality, and treats fixed review periods such as “30-day price review” as project heuristics rather than universal facts. Concrete standard/product/price/version updates no longer belong in the stable protocol body.

Old K03 remains fully preserved as `LEGACY-MTH-ARCH-EVIDENCE-GOV-K03-20260824 / LEGACY / PROVENANCE / HISTORY_ONLY / VALID`. Its historical standard transitions, product evidence, supplier notes and dated update log remain available in History rather than competing with the Current protocol.

## Phase 2 Readback

After the additive migration above:

- Notes/D1 document rows: `1,188`
- Active retrieval documents: `1,186`
- Excluded retrieval documents: `2` (the previously contained orphan empty pages; still retained canonically in Notion)
- Duplicate non-empty Canonical IDs: `0 groups`
- New Current/VALID objects confirmed in D1: `KN-ARCH-URBAN-REGEN-001`, `MTH-KNOWLEDGE-ACADEMIC-NOTE-001`, `MTH-ARCH-RESEARCH-001`, `MTH-ARCH-EVIDENCE-GOV-001`.

The historical 1,184-page full reconcile remains a completed historical run. The current canonical Notes corpus is larger because Phase 2 deliberately adds clean Current carriers while preserving the superseded pages NO LOSS.

## Revised Rewrite Queue

The next academic migrations should use the new two owners rather than independently inventing structure:

1. `D07｜居住研究、住房与日常生活`
2. `D03｜气候低碳与韧性设计`
3. `D05｜建筑经济、开发策划与全生命周期价值`
4. `D02｜乡村建筑与地方营造`
5. `K05｜建筑研究与实践方向地图` — navigation/IA cleanup only; do not inflate into a paper.

Each migration remains additive: clean Current page -> live readback -> relation VALID -> old carrier to Legacy/History -> D1 readback. Naming cleanup is a separate pass and must not be conflated with authority migration.

## Phase 3 — D04 Digital Information / BIM Academic Migration

`D04｜数字设计、BIM与智能建造` has completed the additive academic migration. The replacement is intentionally narrower than the old digital-architecture encyclopedia: it treats BIM/digital construction as a traceable information-management and exchange problem rather than a software catalogue.

New Current knowledge object:

- Page ID: `3d9b86be-5c47-81de-a512-d8bfcfbe8d13`
- Canonical ID: `KN-ARCH-DIGITAL-INFO-001`
- Human title: `BIM 与数字建造：信息需求、开放交换与可验证工作流`
- `CURRENT / DEFAULT / ACTIVE / VALID / L5 / THEORY`
- Trust remains `UNVERIFIED`, matching the existing Current academic carriers; `VALID` here is the reviewed relation/governance gate, not a claim that every external source is permanently verified.
- Normal `syncPage` result: `INDEXED`, `38` chunks, `markdown_truncated=0`.

### D04 Academic Quality Gate

The new Current was promoted from `REVIEW` only after a real live-Notion content readback, not from local Markdown existence or HTTP success alone. The live page was checked for the required research structure and contains:

- explicit Research Question and four conditional/testable theses;
- a Method / Evidence Boundary separating current normative sources, peer-reviewed counterevidence, and OLEANDER project rules;
- claim-level source anchors for ISO/buildingSMART version and capability statements;
- empirical counterevidence for IFC interoperability rather than treating formal standardization as proof of implementation success;
- explicit IDS geometry limitation, so `IDS PASS` is not laundered into whole-model/design compliance;
- four Rival / Counterevidence sections, including native-platform, discovery-first modelling, machine-checking, and Digital-Twin alternatives;
- a Claim–Evidence Map plus independent Applicability / Limitations;
- strong project rules identified as `Normative rule｜OLEANDER` rather than presented as ISO facts;
- generic G0–G9 and POE material removed from the topic-level argument and delegated to the established method owners.

The Current version boundary was rechecked on 2026-09-12. The page records ISO 19650-1:2018, -2:2018 and -3:2020 as current published editions with revisions in progress; ISO 19650-5:2020 as current; ISO 7817-1:2024 for Level of Information Need; ISO 16739-1:2024 / IFC 4.3 ADD2 as the relevant current IFC boundary; IDS 1.0 and BCF 3.0 as final; and bSDD as a service rather than a standard. Time-sensitive claims are kept inside the page's explicit version boundary rather than promoted into timeless governance rules.

### D04 NO LOSS / Replacement Readback

Old D04 remains fully present in Notion and indexed as `57` chunks. It is now:

- Canonical ID: `LEGACY-KN-ARCH-DIGITAL-INFO-D04-20260807`
- `PROVENANCE / HISTORY_ONLY / LEGACY / VALID`
- reciprocal `替代文档` relation -> `KN-ARCH-DIGITAL-INFO-001`
- original body retained; no permanent deletion, compression, or overwrite was performed.

The old page therefore remains available for policy history, prior terminology, software/case/tool material and provenance without competing with the Current reader-facing knowledge object.

### Phase 3 D1 Readback

After the D04 authority cutover:

- Notes/D1 document rows: `1,189`
- Active documents: `1,187`
- Excluded documents: `2` (the same two preserved orphan empty pages)
- Duplicate non-empty Canonical IDs: `0 groups`
- New Current row: `KN-ARCH-DIGITAL-INFO-001 / CURRENT / ACTIVE / VALID / INDEXED / 38 chunks / not truncated`
- Old row: `LEGACY-KN-ARCH-DIGITAL-INFO-D04-20260807 / PROVENANCE / HISTORY_ONLY / LEGACY / VALID / INDEXED / 57 chunks / not truncated`

The +1 corpus delta from the preceding `1,188 / 1,186 / 2` readback is the intended additive Current carrier, not duplicate pollution.

## Phase 4 — D06 Public Building / Social Infrastructure Academic Migration

`D06｜公共建筑、社会基础设施与公共性` has completed the additive academic migration. The new Current removes the old page's encyclopedia pattern (eight-dimension checklist + theory/history + policy/cases + methods + glossary) from the first reading layer and instead tests how built form, service organization and governance jointly distribute access and public value.

New Current knowledge object:

- Page ID: `3d9b86be-5c47-81e9-a88f-ff76e9dcd57a`
- Canonical ID: `KN-ARCH-PUBLIC-SOCIAL-INFRA-001`
- Human title: `公共建筑与社会基础设施：可达性、服务分配与公共性`
- `CURRENT / DEFAULT / ACTIVE / VALID / L5 / THEORY`
- Trust remains `UNVERIFIED`; relation/governance validity was promoted only after live content review.
- Normal `syncPage` result: `INDEXED`, `43` chunks, `markdown_truncated=0`.

### D06 Academic Quality Gate

The new Current was written as `REVIEW` first and promoted only after live Notion readback confirmed the actual page body. The reviewed structure includes:

- one explicit research question and five conditional theses;
- a Method / Evidence Boundary separating rights/authoritative sources, conceptual models, empirical/review evidence and OLEANDER rules;
- publicness treated as multidimensional rather than equated with public ownership;
- social infrastructure treated as a socio-spatial system whose functions depend on organizational, social and physical conditions rather than architectural form alone;
- claim-level evidence from CRPD / WHO plus peer-reviewed publicness, social-infrastructure, building-accessibility, facility-equity, library/social-capital and security research;
- an explicit distinction between compliance evidence, usability evidence and participation evidence;
- five Rival / Counterevidence sections covering ownership, shared-space/social-capital claims, universal-design overreach, security/control and satisfaction/user-selection bias;
- a Claim–Evidence Map and independent Applicability / Limitations;
- non-user / failed-journey evidence treated as potential counterevidence rather than ignored by default;
- the old fixed `八维公共性` retained only as historical provenance, while new diagnostic chains are explicitly marked `Heuristic` rather than universal taxonomy.

The page also removes D06-owned POE duplication: research design and causal claims defer to `MTH-ARCH-RESEARCH-001`; policy/standard/current-source authority defers to `MTH-ARCH-EVIDENCE-GOV-001`.

### D06 NO LOSS / Replacement Readback

Old D06 remains fully present in Notion and indexed as `60` chunks. It is now:

- Canonical ID: `LEGACY-KN-ARCH-PUBLIC-SOCIAL-INFRA-D06-20260807`
- `PROVENANCE / HISTORY_ONLY / LEGACY / VALID`
- reciprocal replacement relation -> `KN-ARCH-PUBLIC-SOCIAL-INFRA-001`
- original body retained, including the old eight-dimension frame, service-journey material, theory/history, China policy/cases, international comparison, methods, glossary and references.

No old body content was compressed, overwritten or permanently deleted.

### Phase 4 D1 Readback

After the D06 authority cutover:

- Notes/D1 document rows: `1,190`
- Active documents: `1,188`
- Excluded documents: `2` (unchanged preserved orphan empty pages)
- Duplicate non-empty Canonical IDs: `0 groups`
- New Current row: `KN-ARCH-PUBLIC-SOCIAL-INFRA-001 / CURRENT / ACTIVE / VALID / INDEXED / 43 chunks / not truncated`
- Old row: `LEGACY-KN-ARCH-PUBLIC-SOCIAL-INFRA-D06-20260807 / PROVENANCE / HISTORY_ONLY / LEGACY / VALID / INDEXED / 60 chunks / not truncated`

The +1 corpus delta from the preceding D04 readback is the intended additive Current carrier. The next academic migration is now D07.

## Phase 5 — Knowledge Reader Visual Dashboard

The user-facing Reader was upgraded from a mostly textual landing page plus five list views into a real, editable Notion visualization surface. This is a presentation-layer change only: the Notes data source remains canonical, and no second knowledge database or dashboard-owned authority was introduced.

Live Reader:

- Page: `知识阅读台｜Knowledge Reader`
- Page ID: `3d9b86be-5c47-81e7-9acd-d05c6d25ad7b`
- Reader intro now opens with a visual reading map and a direct Dashboard entry rather than governance prose.
- Live markdown readback after the upgrade: `3,890` characters, `markdown_truncated=false`, `unknown_block_ids=[]`.

Native Notion Dashboard:

- Dashboard view ID: `3d9b86be-5c47-8118-8885-000c3bf5e9eb`
- Core role chart: `3d9b86be-5c47-81a8-b0b5-000ce54c3fdb`
- Evidence structure chart: `3d9b86be-5c47-81e1-893e-000c9b87e4a1`
- Current knowledge gallery: `3d9b86be-5c47-811e-a1f9-000c177a8df7`
- Methods gallery: `3d9b86be-5c47-810e-8e29-000c586b956a`
- Practice gallery: `3d9b86be-5c47-814a-b27a-000c0f9e28f5`

The dashboard uses Notion's first-class `dashboard` view and widget views over the same Notes data source. The dashboard is positioned as the first view; its widget grid gives one-screen orientation, while the existing `Cards / Map / List` views remain available for deeper browsing and exhaustive lookup. History stays visually subordinate rather than competing with Current knowledge on the first screen.

Reader snapshot at this upgrade:

- Core Knowledge: `272`
- Methods: `73`
- Evidence: `341`
- Practice: `34`
- History/Governance: `214`
- Academic migration: `3 / 7`; next = `D07｜居住研究、住房与日常生活`

These five counts are intentionally overlapping analytical slices, not a partition of corpus total. In particular, Methods are included within the L4/L5 Core population where their level/state matches.

### Visual Dashboard Readback / Idempotency

The first dashboard attempt exposed a runtime implementation issue rather than a Notion design failure: hydrating every view that referenced the Notes data source exceeded the Cloudflare Worker per-invocation subrequest ceiling. The implementation was corrected to read existing widget IDs directly from the dashboard's own `configuration.rows[].widgets[].view_id` and retrieve only those few views.

After that correction:

- Worker deployment: `77039331-b8f2-4ce3-bedc-975e135bc462`
- `POST /v1/reader-layer/visualize` returned `HTTP 200`.
- A second live execution returned the exact same Dashboard and five widget IDs, proving the upgrade path is idempotent rather than additive pollution.
- D1 runtime state `reader_visual_v1` stores the same IDs, counts, academic progress, and non-truncated live readback.
- No Note page, history carrier, relation, Canonical ID, retrieval authority or academic content was deleted or demoted by this visualization pass.

## Phase 6 — D07 Housing / Daily Life Academic Migration

`D07｜居住研究、住房与日常生活` has completed the additive academic migration. The new Current keeps the old page's practical housing material available as provenance, while moving the first reading layer from a broad checklist/encyclopedia pattern to a narrower argument about adequate housing, affordability, residential stability, healthy-housing exposure and spatial adaptation over time.

New Current knowledge object:

- Page ID: `3d9b86be-5c47-814c-8ec5-cafebf91551a`
- Canonical ID: `KN-ARCH-HOUSING-DAILY-LIFE-001`
- Human title: `住房与日常生活：适足性、居住稳定与空间适配`
- `CURRENT / DEFAULT / ACTIVE / VALID / L5 / THEORY`
- Trust remains `UNVERIFIED`; no false `VERIFIED` promotion was introduced.
- Normal `syncPage` result after validity promotion: `INDEXED`, `45` active chunks.

### D07 Academic Quality Gate

The new page was created as `REVIEW` first. It was promoted to `VALID` only after both the bearer-protected Worker readback and an independent connected Notion readback confirmed the actual live page body.

The reviewed page uses the required academic sequence:

`Research Question / Thesis → Claim–Evidence Map → Rival / Counterevidence → Method / Evidence Boundary → Arguments → Evaluation / Project Translation → Applicability / Limitations → Conclusion → References`

Quality controls confirmed in the live page:

- one explicit research question and five conditional theses;
- a Claim–Evidence Map separating authoritative rights/health guidance from academic/review evidence and project-level rules;
- authoritative boundary sources from OHCHR / CESCR and WHO (`S1–S4`);
- peer-reviewed / institutional evidence `A1–A9` covering residual-income affordability, renter housing insecurity and mental health, eviction, energy poverty, housing + transport affordability, flexibility and home modification / ageing in place;
- the 2026 renter systematic review is kept at its actual evidence strength: `22` studies, `14` longitudinal; `6/9` affordability and `12/14` instability studies reported significant adverse mental-health associations, while the review's overall GRADE remained `low–very low`;
- six explicit Rival / Counterevidence sections test area-as-quality, fixed affordability ratios, technical-performance determinism, flexibility determinism, universal ageing-in-place preference and architectural overreach into tenure / housing-system causality;
- claims without direct external support are explicitly identified as `Normative rule`, `Heuristic` or `Hypothesis` instead of being presented as sourced facts;
- project research / POE and causal design defer to `MTH-ARCH-RESEARCH-001`;
- policy, standard, version and evidence-authority conflicts defer to `MTH-ARCH-EVIDENCE-GOV-001`;
- the old D07's family types, activity logs, space hierarchy, kitchen/sanitation/storage, health-housing material, adaptation hierarchy, POE timing, theory/history, policy/cases, international comparison, methods, glossary and references remain available in History / Provenance rather than being compressed into the Current.

Final live Notion readback after promotion:

- New Current markdown length: `17,577` characters
- New Current: `markdown_truncated=false`, `unknown_block_ids=[]`
- Old D07 markdown length: `19,559` characters
- Old D07: `markdown_truncated=false`, `unknown_block_ids=[]`

### D07 NO LOSS / Replacement Readback

Old D07 remains fully present in Notion and indexed as `67` active chunks. It is now:

- Canonical ID: `LEGACY-KN-ARCH-HOUSING-DAILY-LIFE-D07-20260807`
- `PROVENANCE / HISTORY_ONLY / LEGACY / VALID`
- reciprocal replacement relation -> `KN-ARCH-HOUSING-DAILY-LIFE-001`
- original body retained; the governance cutover changed identity/retrieval properties only.

No old body content was compressed, overwritten or permanently deleted. The temporary local academic draft files remain outside Git governance and were not added to this migration commit.

### Phase 6 D1 Readback

After the D07 authority cutover:

- Notes/D1 document rows: `1,193`
- Active documents: `1,191`
- Excluded documents: `2` (the same preserved orphan empty pages)
- Explicit `CURRENT`: `49`
- `SUPPORT`: `930`
- `PROVENANCE`: `212`
- Duplicate non-empty Canonical IDs: `0 groups`
- New Current row: `KN-ARCH-HOUSING-DAILY-LIFE-001 / CURRENT / DEFAULT / UNVERIFIED / ACTIVE / VALID / 45 active chunks`
- Old row: `LEGACY-KN-ARCH-HOUSING-DAILY-LIFE-D07-20260807 / PROVENANCE / HISTORY_ONLY / LEGACY / VALID / 67 active chunks`

The +1 document / +1 active-document delta from the preceding academic state is the intended additive Current carrier, not duplicate pollution.

### Reader Readback After D07

The existing Notion Reader / Dashboard was refreshed in place; no second reader or knowledge database was created.

- Core Knowledge: `274`
- Methods: `73`
- Evidence: `341`
- Practice: `34`
- History/Governance: `215`
- Academic migration: `4 / 7`
- Next: `D03｜气候低碳与韧性设计`
- Reader markdown readback: `3,953` characters, `markdown_truncated=false`, `unknown_block_ids=[]`

These Reader counts retain the existing Notion visualization semantics and should not be conflated with the separate live MCP Reader snapshot metrics. The next academic migration is now D03; D04, D06 and D07 must not be reopened as unfinished work.

The separate OLEANDER Visual Knowledge Reader MCP also picked up the D07 cutover dynamically through `/v1/reader-snapshot`, without a Reader redeploy or CoS reload:

- live item count: `1,191`
- Core Knowledge: `274`
- Methods: `92`
- Evidence: `574`
- Practice: `78`
- History: `212`
- canonical authority reported by the Reader snapshot: `Notion`

The MCP metrics follow the Reader snapshot classifier and therefore intentionally differ from the native Notion Dashboard's visualization slices. This readback proves the presentation layer is consuming the existing canonical derivative rather than maintaining a second knowledge corpus.
