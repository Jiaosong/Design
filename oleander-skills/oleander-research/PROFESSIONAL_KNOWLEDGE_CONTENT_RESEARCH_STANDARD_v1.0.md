# OLEANDER Professional Knowledge Content & Research Standard v1.0｜专业知识内容与研究标准 v1.0

Status: **EXECUTION CONTRACT / GOVERNANCE EXTENSION**. This document extends the existing OLEANDER Authority, Control Plane, Knowledge Retrieval & Lifecycle, and `oleander-research` Skill. It is **not** a new Authority, Registry, taxonomy, Method family, Project State, or parallel knowledge system.

Sync state｜同步状态：**GitHub execution mirror saved; Notion Current Authority remains the canonical Source of Truth and must carry the corresponding current rule binding before this contract is treated as cross-platform synchronized.**

Authority boundary｜权威边界：

`NOTION CURRENT AUTHORITY → LIVE REGISTRY IDENTITY → CURRENT OBJECT / RELATIONS → THIS EXECUTION CONTRACT → GITHUB SKILL / VALIDATOR`

This standard absorbs mature external research-reporting, knowledge-management, semantic-web, provenance, open-science, technical-documentation and design-research practices, while preserving their boundaries. It does not copy any external system wholesale.

---

## 1. Core principles｜核心原则

1. **Research conduct ≠ research reporting.｜研究做对 ≠ 报告写全。**
2. **Well-written page ≠ well-researched page.｜写得专业 ≠ 研究成立。**
3. **Well-researched document ≠ valid knowledge object.｜研究成立的文档 ≠ 合格知识对象。**
4. **Structure PASS ≠ Content PASS ≠ Research PASS ≠ Knowledge Object PASS ≠ CURRENT.**
5. **Citation count ≠ evidence strength.｜引用数量不等于证据强度。**
6. **Prototype ≠ validation; simulation ≠ field truth; render ≠ performance evidence.**
7. **Precedent similarity ≠ performance proof.｜案例相似不等于性能证明。**
8. **Vendor evidence ≠ independent proof.｜厂商证据不等于独立证明。**
9. **AI-generated participant ≠ participant evidence.｜AI 用户不等于真实参与者证据。**
10. **Bilingual ≠ literal translation.｜双语不等于逐字翻译。**
11. **No critical claim without resolvable evidence**, except claims explicitly typed as `ASSUMPTION / HYPOTHESIS / DECISION / UNKNOWN`.
12. **Absorb principles, preserve boundaries.｜吸收能力，不混淆权限。**

---

## 2. Unified gate architecture｜统一门级结构

Every applicable formal knowledge/research object is reviewed through independent gates:

### R1 — Research Conduct Gate｜研究执行门
Question: Was the research designed and conducted appropriately?

Required when an object materially derives knowledge from research, evidence synthesis, empirical observation, experiment, field work, user research, simulation, modeling, measurement, or structured review.

Minimum fields:
- Research Question｜研究问题
- Decision Question｜决策问题
- Contribution target｜预期知识贡献
- Research Depth Class (`RDC-0..RDC-4`)
- Study Type｜研究类型
- Method–Question Fit｜方法与问题适配性
- Sampling / Case Logic｜采样或案例选择逻辑
- Inclusion / Exclusion｜纳入排除规则
- Ethics / Privacy / Rights｜伦理、隐私、权利
- Risk / Bias｜风险与偏倚
- Analysis Plan｜分析计划
- Validation Plan｜验证计划
- Stop Rule / Saturation Logic when applicable
- Planned-vs-Executed Deviation Log｜计划—实际偏差记录
- Conflict of Interest｜利益冲突
- AI Use Disclosure｜AI 使用披露

R1 hard non-PASS:
- no valid research/decision question;
- method does not fit the question;
- consequential human/field research without appropriate protocol;
- required ethics/privacy/right state unresolved;
- unsupported causal inference;
- material planned-vs-executed deviation hidden;
- research design fundamentally incapable of supporting the intended claim.

States: `R1 PASS / REVISE / HOLD / REJECT / NOT_APPLICABLE`.

### R2 — Study-Type Reporting Gate｜研究报告门
Question: Is enough information reported for another reviewer to understand, appraise, and reconstruct the work?

First resolve `Study Type → Reporting Profile`. Do not force one generic checklist over all methods.

Minimum fields:
- Reporting Profile + version
- Protocol / preregistration where appropriate
- Methods actually executed
- Results
- Analysis
- Results vs interpretation separation
- Limitations
- Bias / missing data / deviations where applicable
- Data / Code / Materials / Protocol Availability
- Software / model / instrument version where applicable
- Source-search coverage / inclusion-exclusion flow where applicable

States: `R2 PASS / REVISE / HOLD / REJECT / NOT_APPLICABLE`.

**R2 PASS never grants R1 PASS automatically.**

### K1 — Knowledge Content Gate｜知识正文门
Question: Does the page contain defensible, usable knowledge rather than formatted filler?

Required body:
1. Core Question｜核心问题
2. Definition / Object of Study｜定义/研究对象
3. Core Claims｜核心主张
4. Evidence Basis｜证据基础
5. Mechanism / Reasoning｜机制/推理
6. Contradictory / Negative Evidence｜冲突/反证
7. Conditions｜成立条件
8. Uncertainty｜不确定性
9. Limitations｜限制
10. Applicability / Transfer Boundary｜适用与迁移边界
11. Design / Practice Consequence｜设计/实践后果
12. Validation State｜验证状态
13. Open Questions｜开放问题

Controlled claim types:
`FACT / OBSERVATION / ASSOCIATION / INTERPRETATION / INFERENCE / HYPOTHESIS / ASSUMPTION / UNKNOWN / REQUIREMENT / DECISION`.

Forbidden semantic promotion:
- `ASSUMPTION → FACT`
- `REFERENCE → REQUIREMENT`
- `SIMULATION → FIELD VERIFIED`
- `USER QUOTE → UNIVERSAL NEED`
- `PRECEDENT → PERFORMANCE PROOF`
- `CORRELATION → CAUSATION` without a defensible causal design

States: `CONTENT PASS / RESTRUCTURE / ENRICH / RESEARCH REQUIRED / VALIDATION OPEN / HOLD / REJECT-SUPERSEDE`.

### K2 — Knowledge Object Gate｜知识对象门
Question: Is this the correct independent canonical object?

Required:
- Canonical ID
- Preferred EN / 中文 title
- Knowledge Role
- Information Role
- Content Level
- Purpose
- `Scope In / Scope Out`
- Atomicity check
- Canonical carrier
- Owner / maintainer
- Current governance state

Atomicity rule:
A canonical object should have one stable primary knowledge responsibility. Concept, method, procedure, reference, case, evidence and project output must not be mixed merely because they are topically related.

States: `K2 PASS / SPLIT / MERGE / RESTRUCTURE / HOLD / REJECT`.

### K3 — Knowledge Graph Semantics Gate｜知识图谱语义门
Question: Are relations semantically correct?

Controlled relation families:
- hierarchy: `broader / narrower` → OLEANDER `Canonical Parent / Canonical Children`
- semantic adjacency: `related`
- provenance/source: `derivedFrom / 来源文档`
- method invocation: `引用方法`
- project use: Project relations + Project ID
- supersession: `supersedes / isSupersededBy`

Hard rules:
- `related` must not silently become hierarchy;
- Source / Method / Project / Related / Supersession must not be overloaded into Canonical Parent;
- no self-supersession;
- no unresolved supersession cycles;
- superseded carrier cannot remain `DEFAULT CURRENT`.

States: `K3 PASS / REVISE / HOLD / REJECT`.

### K4 — Metadata / Provenance / Retrieval Gate｜元数据、来源链与检索门
Question: Can the object and its claims be found, traced, verified and reconstructed?

Minimum metadata:
- Identifier
- preferred EN / 中文 labels
- aliases / abbreviations
- type / role / level
- creator / contributor / reviewer
- created / modified / last verified
- sources and evidence refs
- source locators (page/section/table/figure/timecode where available)
- provenance chain
- rights / license / access restrictions
- language
- stable artifact locators
- digest / SHA for hashable critical artifacts
- availability states

Provenance should distinguish `Entity → Activity → Agent` or an equivalent explicit derivation chain.

Availability maturity:
- `T0 UNKNOWN`
- `T1 DISCLOSED`
- `T2 AVAILABLE`
- `T3 SHARED + CITED + HASHED`
- `T4 INDEPENDENTLY VERIFIED`

States: `K4 PASS / REVISE / HOLD / REJECT`.

### K5 — Lifecycle / Reuse / Staleness Gate｜生命周期、复用与时效门
Question: Is the object still current, and has real project reuse produced feedback?

Required where applicable:
- Governance state
- Trust state
- Freshness state
- Retrieval space
- Search eligibility
- Verification due / update trigger
- Reuse Receipts｜复用回执
- correction log
- contradiction/update log
- supersession state

Triggers for revalidation include:
- new regulation / standard / code;
- software/product/version change;
- new field measurement;
- project scope change;
- credible contradictory evidence;
- time-based expiry;
- post-occupancy/prototype/test evidence.

Past-due mutable content must not silently retain VERIFIED status.

States: `K5 PASS / CURRENT / SCOPED / REVALIDATE / SUPERSEDE / HOLD`.

### B1 — Bilingual Semantic Parity Gate｜中英双语语义一致性门
Default formal-body rule: **English｜中文 at equivalent knowledge level**, not Chinese body + English summary.

Required parity:
`Same Claim / Same Evidence / Same Confidence / Same Boundary / Same Status / Same Numbers / Same Units / Same Version`.

First-use terminology format:
`Post-Occupancy Evaluation (POE)｜使用后评价`

B1 checks:
- both languages contain the same material facts;
- modality matches (`may` ≠ `will`; `可能` ≠ `证明`);
- confidence/uncertainty matches;
- limitations are not omitted from one language;
- numbers/units/dates/versions match;
- controlled terminology is stable;
- citations support both language versions.

Semantic/LLM checking may generate a REVIEW SIGNAL, but may not self-award B1 PASS.

States: `B1 PASS / REVISE / HOLD`.

### IR — Independent Review Gate｜独立审查门
For high-impact CURRENT objects, the final reviewer must be independent from the producer for the same review scope.

Review record:
- reviewer / role / date
- reviewed gates
- objections (`CRITICAL / MAJOR / MINOR`)
- author response
- changes made
- unresolved items
- actual verification performed (source opened, data opened, code executed, artifact readback, bilingual check)
- final decision

Unresolved Critical/Major objection blocks promotion.

States: `IR PASS / REVISE / HOLD / REJECT / NOT_APPLICABLE`.

---

## 3. Claim–Evidence Ledger｜主张—证据账本

Claim Ledger is the mandatory bridge between body content and provenance for consequential claims.

Minimum schema:

```yaml
claim_id:
object_id:
claim_en:
claim_zh:
claim_type: FACT|OBSERVATION|ASSOCIATION|INTERPRETATION|INFERENCE|HYPOTHESIS|ASSUMPTION|UNKNOWN|REQUIREMENT|DECISION
supports:
  - evidence_id:
    locator:
    role: DIRECT|INDIRECT|CONTEXTUAL
contradicts:
  - evidence_id:
    locator:
evidence_strength: STRONG|MODERATE|WEAK|DISCOVERY_ONLY
confidence: HIGH|MODERATE|LOW|INSUFFICIENT|UNKNOWN
conditions:
uncertainties:
does_not_establish:
design_consequence:
  type: REQUIREMENT|CONSTRAINT|OPPORTUNITY|HYPOTHESIS|REFERENCE_MOVE|FIELD_OPEN|NONE
validation_state: OPEN|PARTIAL|VERIFIED|FALSIFIED
reviewed_by:
last_verified_at:
supersedes:
```

Hard rules:
- a consequential factual/empirical claim must resolve to evidence;
- contradictions cannot be deleted to simplify the narrative;
- source strength and claim confidence are separate;
- several weak sources do not automatically become strong evidence;
- a `REQUIREMENT` cannot be derived solely from a precedent or `REFERENCE_MOVE`;
- absence claims must state the actual search coverage.

---

## 4. Professional body contract｜专业正文合同

A formal METHOD / THEORY / FRAMEWORK / PRACTICE / CASE / SOURCE / EVIDENCE / TOOL / STANDARD / PROJECT RESEARCH object must use the minimum sections appropriate to its role.

Default professional paragraph pattern:
`Claim → Evidence → Interpretation → Boundary`.

Avoid:
- decorative headings with no content;
- one-sentence paragraph spam;
- large undifferentiated paragraphs;
- citation lists without synthesis;
- unsupported marketing language;
- generic AI filler.

Controlled strong words require evidence:
`VALIDATED / VERIFIED / SYSTEMATIC REVIEW / EVIDENCE-BASED / USER-TESTED / FIELD-VERIFIED / COMPLIANT / SAFE / OPTIMAL / PROVEN / BEST PRACTICE`.

If evidence is insufficient, downgrade wording to:
`SUPPORTED BY / INDICATED BY / PRELIMINARY / PREDICTED / REFERENCE / CANDIDATE / ASSUMED / VALIDATION OPEN`.

Professional language should prefer explicit boundaries:
- `Evidence indicates...｜现有证据表明……`
- `Current evidence supports...｜当前证据支持……`
- `Under the stated conditions...｜在已声明条件下……`
- `This does not establish...｜该结果不能证明……`
- `Applicability remains limited to...｜当前适用范围仍限于……`

---

## 5. Study-Type Reporting Profiles｜研究类型专项报告合同

R2 must route each study to one or more appropriate profiles.

Minimum OLEANDER profiles:

1. `RP-TARGETED-REVIEW`
2. `RP-STRUCTURED-EVIDENCE-REVIEW`
3. `RP-SYSTEMATIC-REVIEW`
4. `RP-SCOPING-REVIEW`
5. `RP-QUANTITATIVE`
6. `RP-QUALITATIVE`
7. `RP-MIXED-METHODS`
8. `RP-SURVEY`
9. `RP-EXPERIMENT`
10. `RP-OBSERVATIONAL`
11. `RP-CASE-PRECEDENT`
12. `RP-USER-RESEARCH`
13. `RP-RESEARCH-THROUGH-DESIGN`
14. `RP-SIMULATION-MODELING`
15. `RP-FIELD-MEASUREMENT`
16. `RP-POE`
17. `RP-TECHNICAL-VERIFICATION`
18. `RP-BENCHMARK-COMPARISON`

External reporting standards are calibration/profile inputs, not automatic OLEANDER Authority.

### Qualitative / interview minimum
- researcher role and reflexivity;
- sampling logic;
- recruitment and non-response;
- setting/context;
- ethics/privacy/consent;
- guide/instrument version;
- capture/transcription process;
- coding/analysis process;
- data adequacy / saturation only when actually operationalised;
- negative/deviant cases;
- theme/claim → excerpt/evidence binding;
- transfer boundary;
- AI use in transcription/coding/translation/summarisation.

### Quantitative minimum
- population/sample and denominator;
- variables/measures/instruments;
- prespecified vs exploratory analysis;
- missing data handling;
- estimate/effect size when appropriate;
- uncertainty interval / measurement uncertainty;
- assumptions;
- sensitivity/robustness where material;
- practical/design significance distinct from statistical significance.

### Simulation / modeling minimum
- model purpose and non-purpose;
- model/solver/library/version;
- governing logic/equations/algorithm;
- inputs + source/unit/date/transformations;
- assumptions;
- boundary/initial conditions;
- scenarios/parameter ranges;
- calibration;
- numerical verification;
- validation against independent/empirical/reference evidence when applicable;
- sensitivity;
- uncertainty;
- executable package/config/seed/environment where reproducibility matters;
- output state: `PREDICTED / CALIBRATED / VALIDATED / FIELD-VERIFIED`.

### Case / precedent minimum
`Problem → Context → Selection rationale → Source hierarchy → Documented facts → Design Move → Mechanism → Outcome → Failure/Limitation → Transferable Principle → Non-transferable Condition → Current Project Binding`.

Always state:
- `WHAT CAN BE LEARNED｜可学习内容`
- `WHAT MUST NOT BE COPIED｜不可照搬内容`

### Research through Design minimum
`Research Question → Why Artifact Is Needed → Artifact/Probe → Variable → Alternative → Encounter → Failure → Annotation → Knowledge Contribution → Transfer Boundary`.

`Prototype ≠ Research through Design` unless this chain exists.

### Architecture / spatial / built-environment minimum
Distinguish:
- `SITE EVIDENCE`
- `DESIGN INTENT`
- `CODE / STANDARD`
- `PREDICTED PERFORMANCE`
- `IMPLEMENTED CONDITION`
- `IN-USE OUTCOME`

Require bidirectional binding for material design-research claims:
`TEXT CLAIM ↔ DRAWING / MODEL / PROTOTYPE / FIELD EVIDENCE`.

A research claim that changes design should identify the affected drawing/model/prototype/decision. A consequential design move should identify its evidence, assumption, hypothesis, professional judgment or authority basis.

---

## 6. Source appraisal｜来源评价

Appraise consequential sources on at least:
- Authority
- Originality
- Directness
- Method transparency/quality
- Context/geographic fit
- Recency / staleness
- Bias / sponsorship / conflict
- Measurement/sample adequacy
- Reproducibility / inspectability
- Consistency with other strong evidence
- Applicability boundary

Source routing is claim-dependent:
- normative claim → law / regulation / official standard;
- product dimensions/version → manufacturer technical documentation may be primary;
- independent performance comparison → vendor-only evidence is insufficient;
- human behavior → real user/field/empirical evidence appropriate to the claim;
- building performance → standards + peer-reviewed/technical/measurement/calibrated model evidence as appropriate;
- precedent authorship/facts → original project/studio/institution source preferred;
- discovery platforms/social/media → discovery/context only unless independently verified.

---

## 7. Reproducibility, availability and integrity｜可复核性、可用性与研究诚信

For consequential research, preserve as applicable:
- protocol + amendments;
- search strings/routes;
- inclusion/exclusion decisions;
- extraction/evidence matrix;
- raw/minimally processed data references;
- transformation/calculation steps;
- code/formulas;
- model/software/version/environment;
- units/coordinate systems;
- file hashes;
- decision log;
- readback;
- permissions/licenses/access restrictions.

Formal research should declare:
- Data Availability
- Code Availability
- Materials Availability
- Protocol Availability
- Funding / sponsorship when material
- Conflict of Interest
- Contributor responsibility when relevant
- AI Use Disclosure

Material AI disclosure should include tool/model where known, purpose, affected research stage, and human verification. AI is not an accountable research author/reviewer/participant.

---

## 8. Knowledge object manifest｜知识对象元数据合同

Minimum machine-readable manifest:

```yaml
canonical_id:
preferred_title_en:
preferred_title_zh:
aliases_en:
aliases_zh:
knowledge_role:
information_role:
content_level:
domain:
purpose_en:
purpose_zh:
scope_in:
scope_out:
canonical_parent:
related:
source_objects:
method_objects:
project_uses:
governance_state:
evidence_state:
trust_state:
freshness_state:
retrieval_space:
search_eligibility:
verification_due:
research_protocol:
reporting_profile:
claim_ledger:
protocol_availability:
data_availability:
code_availability:
materials_availability:
creator:
contributors:
owner:
reviewers:
rights:
license:
ai_disclosure:
created_at:
modified_at:
supersedes:
superseded_by:
```

OLEANDER may serialize this through its own schema/JSON/JSON-LD. SKOS/PROV/DCMI/FAIR are interoperability references, not an instruction to replace the live Notion schema wholesale.

---

## 9. Bilingual controlled terminology｜双语受控术语

Maintain a controlled terminology registry or equivalent current object set.

Minimum term record:
```yaml
term_id:
preferred_en:
preferred_zh:
allowed_alternates_en:
allowed_alternates_zh:
forbidden_or_ambiguous:
definition_en:
definition_zh:
domain:
source:
reviewed_by:
version:
```

Use one preferred term per concept within a domain unless a documented synonym distinction is necessary.

---

## 10. Promotion logic｜晋升逻辑

Recommended promotion equation:

```text
CANONICAL CURRENT
=
Authority / Identity PASS
∧ applicable R1 PASS
∧ applicable R2 PASS
∧ K1 PASS
∧ K2 PASS
∧ K3 PASS
∧ K4 PASS
∧ K5 PASS
∧ B1 PASS
∧ applicable Independent Review PASS
∧ no unresolved Critical contradiction
```

Pure Reference / Index / Redirect objects do not need a fabricated research protocol. Gates are applied only when semantically applicable.

Final states remain compatible with current OLEANDER retrieval governance:
`CURRENT / SUPPORT / PROVENANCE / EXCLUDED`.

---

## 11. Machine-verifiable rules｜可自动校验规则

Minimum validator set:
- `META-001` manifest conforms to current schema;
- `ID-001` Canonical ID exists and is unique;
- `ID-002` no duplicate `ACTIVE + CURRENT + DEFAULT` carrier;
- `R1-001` research object has valid Study Type;
- `R1-002` human study has ethics/privacy state;
- `R1-003` material AI use disclosed;
- `R1-004` planned-vs-executed deviation field exists;
- `R2-001` Study Type resolves to Reporting Profile;
- `CLM-001` consequential factual/empirical claim resolves to evidence;
- `CLM-002` evidence ID resolves;
- `CLM-003` source locator present where obtainable;
- `CLM-004` contradiction state explicitly present;
- `CLM-005` REQUIREMENT cannot derive solely from REFERENCE_MOVE;
- `PROV-001` provenance chain resolvable;
- `AVAIL-001` availability states declared;
- `AVAIL-002` T3 artifact has stable locator + digest when hashable;
- `K2-001` purpose + scope-in + scope-out present;
- `K3-001` hierarchy relation consistency;
- `K3-002` related not used as hierarchy;
- `K3-003` supersession cycle forbidden;
- `K5-001` mutable object has verification_due/update trigger;
- `K5-002` stale past-due object cannot silently retain VERIFIED;
- `K5-003` superseded object cannot remain DEFAULT CURRENT;
- `B1-001` required EN + 中文 segments both exist;
- `B1-002` numeric/unit/date/version parity;
- `B1-003` controlled terminology conformity;
- `B1-004` modality-strength mismatch triggers human review;
- `IR-001` high-risk final reviewer independence;
- `IR-002` unresolved Critical/Major objection blocks promotion.

Automation may validate syntax, identity, links, hashes, values and obvious bilingual differences. It must not self-certify professional truth, methodological validity, semantic equivalence, design quality or field validity.

---

## 12. Existing 1215-object migration contract｜1215 对象逐页治理合同

Do **not** batch-fill fields and call migration complete.

Review each canonical object from its **current full body**, not title alone and not old review evidence when current body has changed.

Independent review states must remain separate:
- `STRUCTURE STATE`
- `CONTENT STATE`
- `RESEARCH STATE` when applicable
- `KNOWLEDGE OBJECT STATE`
- `BILINGUAL STATE`
- `LIFECYCLE / CURRENT ELIGIBILITY`

Minimum review order:
1. Canonical identity / collision preflight
2. read current full body
3. determine object role and information role
4. determine whether R1/R2 apply
5. identify core claims
6. resolve source/evidence chain
7. check contradiction/negative evidence
8. judge evidence strength/confidence/uncertainty
9. judge atomicity/scope
10. check graph semantics
11. check provenance/availability
12. check lifecycle/freshness/reuse
13. check bilingual parity
14. independent review when required
15. promotion decision

Do not infer missing evidence, confidence, metadata or validation state merely to achieve schema completeness. `UNKNOWN / VALIDATION OPEN / HOLD` are legitimate states.

Current-priority order should be risk-based, not only page order:
`CURRENT + DEFAULT → Current Rule / Method / Framework → Source Authority / Evidence → frequently reused Support → Case / Practice → Legacy / Provenance`.

However, when a user or active batch explicitly specifies object order, preserve that order while applying the same per-object rigor.

---

## 13. External calibration sources｜外部校准来源

These sources informed this standard. They calibrate rigor but do not supersede discipline-specific standards or current OLEANDER Authority.

Knowledge management / architecture:
- ISO 30401:2018 Knowledge management systems — Requirements: https://www.iso.org/standard/68683.html
- KCS v6 Practices Guide: https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide
- OASIS DITA 1.3: https://docs.oasis-open.org/dita/dita/v1.3/
- Diátaxis: https://diataxis.fr/
- W3C SKOS: https://www.w3.org/TR/skos-reference/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- Dublin Core Metadata Terms: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
- FAIR Principles: https://www.go-fair.org/fair-principles/

Research conduct / reporting / integrity:
- EQUATOR Network: https://www.equator-network.org/reporting-guidelines/
- PRISMA 2020: https://www.prisma-statement.org/prisma-2020
- CONSORT/SPIRIT: https://www.consort-spirit.org/
- APA JARS: https://apastyle.apa.org/jars
- COREQ / SRQR via EQUATOR
- UKRIO Code of Practice for Research v3.5: https://ukrio.org/ukrio-resources/publications/code-of-practice-for-research/
- ICMJE Recommendations: https://www.icmje.org/recommendations/
- COS TOP Guidelines 2025: https://www.cos.io/initiatives/top-guidelines
- Nature Portfolio reporting / data / code / materials / protocols: https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards

Design / built environment calibration:
- UCL Bartlett Architecture research guidance: https://www.ucl.ac.uk/bartlett/architecture/study/architecture-phdmphil/architecture-mphilphd-application-guidance
- UCL Bartlett built-environment ethics: https://www.ucl.ac.uk/bartlett/research/ethics-built-environment
- ISO 9241-210:2019 Human-centred design: https://www.iso.org/standard/77520.html
- ISO 9241-11:2018 Usability: https://www.iso.org/standard/63500.html

Version note: external standards are version-sensitive. OLEANDER stores the source/version/access state and does not assume a translation or older edition remains current after an external revision.

---

## 14. Required acceptance test｜最低验收线

A formal professional knowledge page may not be promoted to `CANONICAL CURRENT` merely because it is well structured or bilingual.

Before promotion, it must answer, at the level applicable to its role:

**EN.** What do we know? Why do we know it? How strong is that knowledge? Under what conditions does it hold? What contradicts it? What remains unknown? How was it produced and reviewed? What does it change in design or practice? When must it be revalidated?

**中.** 我们知道什么？为什么知道？知道到什么程度？在什么条件下成立？有哪些反证或冲突？哪里仍然不知道？这些知识如何产生并被审查？它具体改变什么设计或实践决策？什么时候必须重新验证？

If those questions cannot be answered, the object may remain useful as `SUPPORT / PROVENANCE / VALIDATION OPEN`, but it is not Professional Knowledge Content PASS for canonical promotion.
