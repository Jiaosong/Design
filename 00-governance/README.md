# Governance v1.1.1

Status: ACTIVE
Evidence: E2
Owner: 刘旋 / OLEANDER／织作

## Current architecture authority

- Knowledge Level axis: `L0 System → L1 Branch → L2 Domain → L3 Topic → L4 Integrating Framework / Cluster → L5 Knowledge Object → L6 Source / Evidence / Case → L7 Practice / Output`.
- Knowledge Role is independent from Level: `INDEX / THEORY / METHOD / TOOL / SOURCE / EVIDENCE / CASE / PRACTICE`. `FRAMEWORK` is not a Knowledge Role and `INDEX` is not part of the L5 level name.
- L4 objects additionally declare a functional `Framework Type` such as `NAVIGATION_MAP / CONCEPTUAL_MODEL / METHOD_FAMILY / PROCESS_ORCHESTRATION / PROFESSIONAL_SYSTEM_MAP / TYPOLOGY_FRAMEWORK / APPLICATION_FRAMEWORK / DESIGN_LANGUAGE_SYSTEM / STRATEGY_FRAMEWORK / EVALUATION_FRAMEWORK / HISTORICAL_COMPARATIVE_SYNTHESIS` when resolved. Domain / Topic remains a separate subject axis.
- Application Mapping: `Business / Culture / IP / Spatial`, with `B01–B04 / CU01–CU04 / IP01–IP04 / SP01–SP04`. These codes express where knowledge or project work is applied; they are not a knowledge taxonomy, Project IDs, or delivery-priority labels.
- Project axis: `P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`.
- Case axis: `C01 / C02 / C03 / C04 / C05+`; a bare `Cnn` is a Canonical Case ID and must not substitute for a Project ID.
- Delivery priority: `Priority-0 / Priority-1 / Priority-2 / Priority-3` only.
- Claims: `CLM-*`; IP assets: `IP-[Role]-[NNN]`.
- AI governance: `AIG-01 / AIG-02 / AIG-03`.

GitHub repository paths such as `01-business/`, `02-culture/`, `03-ip/`, `04-spatial/`, `05-cases/` and `06-practice/` are navigation / publication locations. Their folder names do not override the Knowledge, Application, Project or Case axes above.

**Namespace hard rule:** `P0–P4` are reserved for the project axis and must not be reused as current AI-governance identifiers or delivery priorities. Historical AI `P0/P1/P2`, `P2-E...` evidence IDs, PR titles and source filenames remain immutable audit history only. New runtime evidence uses `AIG3-E...`.

**Case / Project hard rule:** `Cnn` is reserved for the Case Axis. The original writable Project Registry has now been recovered in place and separates `Project ID｜项目ID` from `Case ID｜案例ID`. Historical `Cnn`, `Cnn-WS-*` and `Cnn-VAL-*` values remain workflow / compatibility / provenance aliases only; they no longer carry Current Project Axis authority.

**No-loss / no-pollution rule:** preserve history in Git history, `99-archive` or migration records, but maintain only one current authority. Do not create parallel replacement pages/files when an in-place identity, relation or current-file repair is sufficient.

### Global default execution principle｜NO COMPRESSION / NO LOSS

Canonical policy: [`OLEANDER_NO_COMPRESSION_NO_LOSS_POLICY_v1.0.md`](OLEANDER_NO_COMPRESSION_NO_LOSS_POLICY_v1.0.md)

All OLEANDER projects, workstreams, validations, cases, Practice outputs and delivery surfaces inherit by default:

> **NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS**

Global quality separation:
- `Artifact existence ≠ Design quality`;
- `Traceability ≠ Professional finish`;
- `Evidence correctness ≠ Visual excellence`;
- `Process PASS ≠ MAIN KEEP`;
- `Machine PASS ≠ Design PASS`;
- `Executed ≠ Validated`.

This policy does **not** impose one universal chapter count or the C04 12-layer architecture on other projects. Each project keeps its own valid architecture. The hard rule is that independently valid layers, content systems, design outcomes and evidence chains may not be silently collapsed or deleted merely for brevity, page count, cleaner presentation, simpler Web, shorter film or visual minimalism.

Reorder / split / add / regroup / reweight / redraw are allowed when unique information and design function are preserved. Any genuine removal must be explicit `DEMOTE TO SUPPORT / DEMOTE TO PROCESS / HOLD / CUT` with a concrete design reason. `Compression` by itself is never a valid design reason.

Current migration record: [`migration/OLEANDER_SYS_GOV_Architecture-Realignment_v1.1.0_ACTIVE_E2_20260811.md`](migration/OLEANDER_SYS_GOV_Architecture-Realignment_v1.1.0_ACTIVE_E2_20260811.md).

## Registry Recovery / Current physical identity

Notion Registry Recovery is complete for the original core registry lineage. The original `90｜System Databases` and Notes / Domain / Project data sources were restored with their existing IDs; no parallel registry was created.

Current physical identity contracts:

- Knowledge hierarchy: `Canonical Parent｜层级上位 / Canonical Children｜层级子级`. Historical `上位笔记 / 子级笔记` are migration / provenance fields only and must not drive Current hierarchy or AI routing.
- Project identity: `Project ID｜项目ID + 项目层级` for the full `P0–P4` axis.
- Case identity: `Case ID｜案例ID`, resolved independently from Project ID.
- Source, Method, Project, Related and Supersession relations remain semantically separate from structural hierarchy.

Current Portfolio / Program identities:

- P0 `PF-00` — OLEANDER Design System Portfolio.
- P1 `PG-10` — Knowledge & Governance.
- P1 `PG-20` — Brand & Identity.
- P1 `PG-30` — Cases & Practice.
- P1 `PG-40` — BAOJIAJIE Brand & Cleaning Innovation.

`PRJ-XJ01-CMF` remains an independent P2 and now resolves `PF-00 → PG-40 → PRJ-XJ01-CMF`. Baojiajie brand research, cleaning-industry/tool research, CMF research and rights/asset evidence remain Knowledge / Evidence inputs; they are not additional P2 projects.

## Application Mapping
- Business: B01 Positioning & Value; B02 Model & Offering; B03 Operation & Partnership; B04 Metrics & Governance.
- Culture: CU01 Source & Context; CU02 Knowledge & Interpretation; CU03 Participation & Rights; CU04 Continuity & Renewal.
- IP: IP01 Identity & Naming; IP02 Narrative & Content; IP03 Visual & Verbal System; IP04 Application & Licensing.
- Spatial: SP01 Site & Evidence; SP02 Program & Relations; SP03 Space & Experience; SP04 Construction & Operation.

These mappings are assigned after a Knowledge Object has a `Domain / L0–L7` position, or when a project needs to state where knowledge is being applied. `PRIMARY / SUPPORTING / CONDITIONAL / N/A` describes application emphasis only.

## Cases
- C01: 一脉广渡. Current P2: `PRJ-C01-YIMAI-GUANGDU`. Legacy: CASE/GD, old 03 and P00 pages. Application emphasis: Culture + Spatial. Status: RESEARCH + PROPOSAL / EVIDENCE REVIEW.
- C02: 忘也 Daylily. Current P2: `PRJ-C02-DAYLILY`. Legacy: CASE/DY, old 03C. Application emphasis: Business + IP + Spatial. Status: INDEPENDENT PORTFOLIO / PROTOTYPED / TEST PLANNED / NOT RUN.
- C03: The Light Collection / Reno CMF independent concept proposal. Current P2: `PRJ-C03-LIGHT-COLLECTION`. Legacy: CASE/LC, old 03D. Application emphasis: IP. Status: PORTFOLIO CONCEPT / VISUALIZED / SAMPLE TEST PENDING. Do not imply OPPO commission, adoption, production, or endorsement.
- C04: 清江石书｜红花峰林十三印. Current P2: `PRJ-C04-QINGJIANG-SHISHU`. Legacy working names include 清江十三印 / 清江三十印 and historical QJ13 / WS identifiers. Application emphasis: Culture + Spatial, with IP / Business support. Field / professional survey and implementation claims remain evidence-gated.

C04 current explicit P3/P4 identities are `PRJ-C04-GOV-SITE`, `PRJ-C04-EXPERIENCE-SPATIAL`, `PRJ-C04-DIGITAL-INTERACTION`, `PRJ-C04-VISUAL-READING` and `PRJ-C04-RUNTIME-RESPONSIVE`. Historical `C04-WS-* / C04-VAL-*` remain compatibility aliases only.

## Identity
- IP-NM-001 v1.0.0 ACTIVE E2
- IP-IA-001 OPEN E1; the recovered v0.4 source is LEGACY / READ-ONLY evidence only.
- IP-WM-001 OPEN E0; Wordmark v0.8.1 is DEPRECATED / LINK_ONLY and does not define the current object.
- IP-SM-001 OPEN E0; rejected v0.5 remains excluded.
- IP-LK-001 OPEN E0; R4C-G2 is DEPRECATED / LINK_ONLY and must not be reconstructed from previews.
- v0.7 and v0.7-R1 remain LEGACY comparison inputs.

## Migration
- Migration-level HOLD from v1.0.1: 0.
- v1.1.0 realignment separated Knowledge Architecture, Application Mapping, Project Axis, Case Axis, delivery priority and AIG governance identifiers without renumbering immutable historical evidence.
- v1.1.1 records the original-registry restoration, Current structural hierarchy fields, complete P0/P1 Project IDs and Baojiajie `PG-40` registration.
- Current-object design, recognition, physical reproduction and E4 rights/release gates remain open where previously open.
- See `00-governance/migration/`.

## Status Codes
OPEN / WIP / PROTO / CAND / REVIEW / ACTIVE / APPROVED / RELEASED / HOLD / REJECTED / DEPRECATED / LEGACY / ARCHIVED

## Evidence Codes
E0 unlocated; E1 source located; E2 internal validation; E3 real-world validation; E4 approved release with rights, hash, and rollback record.

## Artifact Review System v1.0

Canonical system: [`artifact-review-system-v1.0.md`](artifact-review-system-v1.0.md)

所有审查统一分为两层：

- **A｜Common Review：AR-G01—AR-G10** — 所有文件无条件执行。
- **B｜Specific Review：AR-S01—AR-S09** — 按 Drawing / Model / Data / Code / GIS / Visual-CMF / Documentation / Presentation / Release Package 类型触发。

最终成品必须把 **Occlusion｜遮挡** 与 **Scale / Proportion｜技术比例 + 构造比例**作为独立审查项，并继续独立检查 Geometry ↔ Dimension、View Appropriateness、Cross-view Consistency、Construction / Functional Logic。关键硬 FAIL 不能由总分平均抵消。

一个文件只有 `Common PASS + 对应 Specific PASS` 才能标记 `POST-REVIEW PASS`；一个交付包只有全部触发 Gate + AR-S09 通过才允许 `PACKAGE RELEASE PASS`。历史审查未按 v1.0 重跑时只保留为 `LEGACY REVIEW RESULT`。

### Built-asset High-Fidelity Gate

For spatial / architecture / built-environment models that claim high-fidelity constructive completeness, construction-aware, near-as-built or digital-twin-ready representation, the canonical acceptance owner is `high-fidelity-built-environment-model-gate-v1.0.md`. The 3D execution / receipt binding is `oleander-skills/oleander-3d-pipeline/BUILT_ASSET_HIGH_FIDELITY_ACCEPTANCE_EXTENSION.md`.

`BA0-BA4` describes built-asset representation maturity and is independent from Project Flow execution/render `FID0-FID3`, external BIM LOD, FIELD state and engineering/code/fabrication authority. Render quality, object count, reopen PASS, CI PASS or a BIM/LOD label cannot independently grant built-asset acceptance.

## Complex Project Master Runtime v1.0

Canonical system: [`complex-project-master-runtime-v1.0.md`](complex-project-master-runtime-v1.0.md)

这是 OLEANDER 复杂项目的**薄 Master Runtime**：位于唯一 Current Authority 之下、Design Intelligence / Cross-Disciplinary Integration / Canonical Project Flow / Control Plane 等现有运行模块之上。它只负责跨模块 `Invocation / Precedence / State Propagation / Handoff / Claim Ceiling / Promotion Eligibility / G9 Re-entry / Version-Supersession`，不复制各模块正文，也不创建第二套 L0–L7、P0–P4、Gate、Evidence 或 Discipline taxonomy。

机器运行状态复用现有 `00-governance/control-plane/orchestration.schema.json` 的 `MASTER_RUNTIME_STATE`，由 `orchestrator.py master-runtime` 检查。状态可到 `RUNNABLE / READY_FOR_HUMAN_DECISION`，但机器不得自动授予 `DESIGN KEEP` 或 `PROMOTED`。

复杂项目主链统一为：

`Resolve Authority -> Route Current Knowledge -> Compile Design Intelligence -> Compile Shared Design Quality & Design Development Scope -> Run Authentic Professional Domain Process -> Resolve Integration when coupled -> Execute / Prototype -> Actual Readback -> Close Triggered Reviews -> Independent Whole-System Design Decision -> Persist when required -> Human Promotion Decision -> G9 bounded re-entry`.

## Knowledge Content Review Layer v1.0

Canonical system: runtime/OLEANDER_KNOWLEDGE_CONTENT_REVIEW_LAYER_v1.0.md

Knowledge objects require two independent terminal states: Graph Terminal + Content Terminal. Correct taxonomy and relations do not imply body completion. Every canonical body must be read and receive KEEP / RESTRUCTURE / ENRICH / MERGE / HOLD / LINEAGE_ONLY. RESTRUCTURE / ENRICH / MERGE become terminal only after the action is applied and independently read back. Global completion requires graphTerminal && contentTerminal; classification evidence must never substitute for body review.

## Design Intelligence Routing & Review System v1.0

Canonical system: [`design-intelligence-routing-and-review-v1.0.md`](design-intelligence-routing-and-review-v1.0.md)

OLEANDER 的设计知识层不建立第二套知识树。当前 `L0–L7`、Domain / Topic、METHOD / THEORY / SOURCE / EVIDENCE / CASE / PRACTICE 关系继续承担知识所有权；项目在 `P0–P4` 下通过 **Design Intelligence Packet** 解析当前设计问题、Design Intent、需要调用的既有知识对象、专业 Review Lens、技术/Evidence Gate 触发条件与 Claim Ceiling。

设计审查与技术审查保持分离：`Machine PASS ≠ Design KEEP`、`Technical Validation ≠ Design Quality`、`Evidence Correctness ≠ Visual Excellence`、`Process PASS ≠ MAIN KEEP`。专业设计 Lens 负责空间、产品、视觉、品牌、交互、服务、展陈、导视、CMF、数据、动效、Presentation 等设计判断；其知识由当前知识库关系路由，不把这些 Lens 固化成新的 L2 Domain 或平行 `DKE-*` 分类。

项目级闭环统一为：

`Knowledge Route -> Design Question / Intent -> Explore / Compare -> Candidate -> Shared Design Quality & Development Scope -> Triggered Professional Domain Process -> Cross-Disciplinary Integration when coupled -> Execute / Prototype -> Actual Readback -> Artifact + Professional + Design + Technical/Evidence Review -> Independent Design Decision -> Promotion -> Observe -> G9 Knowledge Candidate`.

G9 经验只有在适用范围、证据状态、反例/失败条件与成熟度明确后，才允许进入或修订 L4/L5 知识对象；项目经验本身不自动成为通用设计规则。

## Integrated Runtime Structure v1.0

Canonical runtime view: [`runtime/OLEANDER_INTEGRATED_RUNTIME_STRUCTURE_v1.0.md`](runtime/OLEANDER_INTEGRATED_RUNTIME_STRUCTURE_v1.0.md)

This document is the operator/integration view subordinate to `Complex Project Master Runtime v1.0`. It expands existing Authority, Knowledge, Design Intelligence, Shared Design Quality & Design Development, Professional Domain Process, Cross-Disciplinary Integration, Skill / Capability / Tool Runtime, Native Execution, Actual Readback, Review, Persistence / Promotion / Sync and G9 into one runtime view. It creates no second Master, taxonomy, Gate or Project Axis. Current relation: `Authority -> Master Runtime -> Knowledge Resolution -> Design Intelligence -> Shared DD Contract -> Professional Domain Process -> Integration when coupled -> Capability / Skill / Tool -> Native Artifact -> Actual Readback -> Independent Reviews -> Persistence / Promotion / Sync -> G9`.

## Knowledge Integrity & Operational Mount Contract v1.0

Canonical runtime admission contract: [`knowledge-integrity-and-operational-mount-v1.0.md`](knowledge-integrity-and-operational-mount-v1.0.md)
Machine-readable existing-corpus mount: [`runtime/OLEANDER_EXISTING_KNOWLEDGE_MOUNT_v1.0.json`](runtime/OLEANDER_EXISTING_KNOWLEDGE_MOUNT_v1.0.json)

The existing live Knowledge corpus is mounted by canonical reference rather than copied into `DD-*`, Architecture `ADD-*`, future professional processes or project folders. It keeps five state families independent: corpus/retrieval (`CURRENT / SUPPORT / PROVENANCE / EXCLUDED`), full-body Content Remediation, Knowledge Integrity (`KI0...KI5`), task/claim-scoped Operational Eligibility (`OE0...OE3`), and downstream Design/Professional states (`DQ0...DQ5`, `ADD-*`, etc.). `CURRENT != CLEAN`; `CONTENT COMPLETE != KNOWLEDGE CLEAN`; `OPERATIONALLY ELIGIBLE KNOWLEDGE != DQ MATURITY`; `DQ MATURITY != PROFESSIONAL STAGE COMPLETION`.

This contract is the bridge from the existing 1215-object remediation lineage into live design/professional execution: `Live Corpus -> Full-body Content Review -> Integrity Resolution -> Operational Eligibility -> Design Intelligence Knowledge Inputs -> Shared DD Responsibilities -> Authentic Professional Domain Stage`. It does not batch-fill domain/stage fields, legitimize unresolved pollution, or create a second knowledge taxonomy.
## Design Quality & Design Development Specification v1.0

Canonical execution specification: [`design-quality-and-design-development-specification-v1.0.md`](design-quality-and-design-development-specification-v1.0.md)

该规范位于 Design Intelligence 下游、各专业设计过程 / Skill / Tool / Artifact 上游，补足 OLEANDER 对“真正把设计发展到专业完成度”的共享执行合同。它把 **Truth / Performance / Design** 三条结果轴保持独立，并把设计开发拆为 `DD-01 Intent → DD-02 Concept → DD-03 Experience → DD-04 Form / Composition → DD-05 Human Relation → DD-06 Sensory → DD-07 Design Language / Style → DD-08 Detail / Craft → DD-09 Prototype / Experiment → DD-10 Adaptation / Variation → DD-11 Meaning / Memory → DD-12 Integration / Coherence`。这些是跨专业的设计责任维度，不是新的知识 taxonomy，也不替代 Architecture ADD、未来各专业真实阶段或 Cross-Disciplinary Integration。`DD-*` 仅属于该共享设计开发合同，不得替代专业 stage ID。

规范同时正式定义 `PROJECT_DESIGN_DNA`、Design Direction / Aesthetic Position、Formal Grammar、Visual Ownership、Signature / System / Exception / Experiment、Variation Envelope、Style Intensity、Content Projection / No-loss、Design Resolution Scale、Design Maturity `DQ0–DQ5`、Genericity Attack、Root Cause / Convergence、Design reopen propagation 与 `DESIGN_QUALITY_DEVELOPMENT_RECEIPT`。机器只能检查结构、引用、stale/receipt 合法性；`DQ3–DQ5`、审美质量、coherence、distinctiveness、craft 与 `DESIGN KEEP` 必须由真实成品 readback + 独立专业设计判断决定。

## Cross-Disciplinary Design Integration v1.0

Canonical system: [`cross-disciplinary-design-integration-v1.0.md`](cross-disciplinary-design-integration-v1.0.md)

复杂跨专业项目在 Design Intelligence 之上增加集成层，但不新增知识分类。它负责 `subsystem / interface / coupling / criticality / shared variable / dependency / authority / maturity / joint decision / change propagation / integrated prototype / integration readback`。治理强度按接口风险与耦合程度分级：`MAJOR / CRITICAL` 接口使用明确的 Acceptance Contract，关键共享变量变更会按影响范围重开相关接口、评审和 Gate；`DISCIPLINE PASS ≠ INTEGRATION PASS`。

跨专业项目的运行关系是：

`Knowledge Route → Design Intelligence Packet → Discipline Lenses → Cross-Disciplinary Integration Packet → Prototype / Execute → Discipline + Technical Review → Integration Readback / Integration Receipt → Independent Whole-System Design Decision → Promotion / G9`。

## Architecture Design Development Process v1.0

Canonical architecture process: [`architecture-design-development-process-v1.0.md`](architecture-design-development-process-v1.0.md)

建筑/学校/公共建筑/改造类项目一旦声明功能分区、空间组织、动线、房间可用性或建筑设计质量已经解决，就必须触发这一层。默认链为：`Site → Brief → Users → Program → Room Brief → Adjacency → Zoning Alternatives → Multi-Flow Systems → Room Planning → Circulation → Life-Safety + Accessibility-Aware Planning → Service/Hygiene/Security → Structure/MEP/Envelope Fit-Back → Climate/Daylight/Acoustics → Landscape → FF&E/Room Use → Area/Cost/Maintenance → Existing/Phasing → Code Matrix → Independent Plan Review`。

该过程明确禁止以下替代关系：`Program Fit ≠ Functional Planning PASS`、`No Overlap ≠ Room Usability`、`Model PASS ≠ Circulation PASS`、`Egress Reserve ≠ Fire Compliance`、`Step-Free Reserve ≠ Accessibility Compliance`。触发后必须形成机器可读 `ARCHITECTURE_DESIGN_DEVELOPMENT_RECEIPT`；关键功能、流线、容量或技术接口变更会使相关 receipt scope 变为 stale 并重开。

## Mandatory Post-Generation Review Gate

Operational gate: [`post-generation-review-gate.md`](post-generation-review-gate.md)

所有设计与技术输出必须在生成/导出/自动 QA 后，再执行一次独立成品审查。未执行时状态为 `REVIEW PENDING`；发现问题为 `POST-REVIEW FAIL / NEEDS REVISION`；只有修正并重审达到 `POST-REVIEW PASS`，才允许升级。

自动 QA、脚本 PASS、bbox=0、文件存在或可复现运行，都不能替代最终成品审查。Code PASS 也不能替代 Generated Artifact PASS。

## High-Fidelity Built-Environment Model Acceptance Gate v1.0

Canonical specialized gate: [`high-fidelity-built-environment-model-gate-v1.0.md`](high-fidelity-built-environment-model-gate-v1.0.md)

当空间/建筑模型声明完整高写实、close constructive completeness、`BA3_HIGH_FIDELITY_CONSTRUCTIVE`、`BA4_NEAR_AS_BUILT_CANDIDATE` 或等价完整建筑系统能力时，除 AR-S02 外必须触发 Built-asset High-Fidelity Gate。它独立检查结构、围护、室内构造、紧固件/接口、给水、排水、电气、HVAC、消防、材料层、缺陷/老化、检修维护以及 clash/penetration/clearance，并要求 `BUILT_ASSET_FIDELITY_ACCEPTANCE_RECEIPT`。

`BA0–BA4` 是 OLEANDER 的 built-environment representation maturity，不是外部 BIM LOD、不是 `FID0–FID3` 渲染/执行精度，也不自动证明 FIELD / engineering / code / fabrication。Beauty render、PBR、对象/面数、可打开、CI PASS 均不能单独升级 BA maturity。

## Production Asset Persistence Gate v1.0

Canonical system: [`production-asset-persistence-gate-v1.0.md`](production-asset-persistence-gate-v1.0.md)

凡生产链触发 native source、canonical model、production ZIP 或其他不可仅凭文本重建的二进制，必须执行 `PAP-G0—PAP-G6`。每个 required binary 至少必须有 **1 个真正的 durable binary copy**，并完成独立重新下载/materialize、byte size + SHA-256 校验以及 open/unzip/parse 验证。

不计入唯一持久化副本：`/mnt/data`、临时 sandbox、signed URL、checksum-only、preview-only、仅 Notion/GitHub 文字记录、会过期且没有第二持久副本的 GitHub Actions artifact。

生产 Promotion 链统一为：

`final artifact review → package/hash → durable upload → independent retrieval → PERSISTENCE PASS → AR-S09 PASS → Promotion / Archive`
