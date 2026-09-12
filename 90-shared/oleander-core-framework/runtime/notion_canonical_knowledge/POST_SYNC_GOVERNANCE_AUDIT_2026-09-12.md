# OLEANDER Notion Post-Sync Governance Audit — 2026-09-12

Status: **PHASE 2 ACTIVE / READER LAYER LIVE / ACADEMIC MIGRATION STARTED / NO PERMANENT DELETE**

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

1. `D06｜公共建筑、社会基础设施与公共性`
2. `D07｜居住研究、住房与日常生活`
3. `D03｜气候低碳与韧性设计`
4. `D05｜建筑经济、开发策划与全生命周期价值`
5. `D02｜乡村建筑与地方营造`
6. `K05｜建筑研究与实践方向地图` — navigation/IA cleanup only; do not inflate into a paper.

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

The +1 corpus delta from the preceding `1,188 / 1,186 / 2` readback is the intended additive Current carrier, not duplicate pollution. The next academic migration is now D06.
