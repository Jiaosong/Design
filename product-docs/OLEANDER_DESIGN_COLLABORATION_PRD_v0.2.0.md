# OLEANDER 设计协作系统｜Product Requirements Document v0.2.0

**Product:** OLEANDER Human–AI Co-Design System  
**Document type:** Master Product Requirements Document  
**Revision:** `v0.2.0`  
**State:** `WORKING PRODUCT BASELINE / NON-AUTHORITY / PRE-EXTERNAL-USER-VALIDATION`  
**Date:** 2026-09-26  
**Product owner:** Jiaosong  
**Supersedes for public product-definition use:** `OLEANDER_DESIGN_COLLABORATION_PRD_v0.1.md`  
**Does not supersede:** OLEANDER Current Architecture, Current Project State, Governance, Runtime, Knowledge Authority, Professional Process, Execution Receipt, Native Artifact Authority, Design Review Authority, PAP, Promotion or Sync owners.

> **PRD ≠ Project State ≠ Architecture Authority.**  
> 本文定义“产品应该解决什么问题、用户如何使用、需要什么功能、功能如何验收”。当本文与 owner-native Current architecture 冲突时，**Current authority wins; PRD must be revised.**

---

# 0｜为什么需要 v0.2.0

v0.1 已经建立了产品经理可读的背景、MVP、Human–AI Session Kernel、FR-01–20、指标和路线图，但颗粒度仍然偏“产品概述 + 核心机制”。

OLEANDER 之前的产品发现和系统工程工作已经达到更细层级：

```text
DESIGN ACTIVITY
→ DESIGN JUDGMENT / DECISION MOMENT
→ CURRENT BEHAVIOUR / WORKAROUND
→ FRICTION / PAIN
→ USER NEED
→ USER STORY
→ EXPERIENCE REQUIREMENT
→ PRODUCT REQUIREMENT
→ SYSTEM REQUIREMENT
→ FUNCTION
→ PRODUCT AREA / FEATURE
→ USER FLOW
→ INFORMATION / OBJECT
→ INTERFACE
→ VERIFICATION / VALIDATION
```

v0.2.0 的任务是把这些已有成果和 2026-09 Human–AI Co-Design Session Kernel 合并成一个真正可执行、可评审、可验收的产品 PRD。

## 0.1 v0.2.0 的三个修正

### 修正 A｜Session Kernel 不是整个产品
Session Kernel 是跨产品的交互与连续性机制。OLEANDER 产品本体仍然包含 Focus、Studio、Map、Artifacts、Review、Knowledge、History 等设计工作面。

### 修正 B｜产品进度不是 Feature 完成率
OLEANDER 的进度仍以设计问题、关系、证据、成熟度和真实 artifact 的 resolution 为核心，不把 task count / file count / agent activity 当成设计进度。

### 修正 C｜PRD 必须可验收
每一个重要产品 Feature 都必须能够回答：
- 谁在什么情境使用；
- 要解决什么 Job；
- 输入是什么；
- 系统行为是什么；
- 用户看到什么；
- 什么属于 Human authority；
- 什么可以自动；
- 失败时如何降级；
- 如何验证；
- 对应什么 metric / event。

---

# 1｜产品定义

OLEANDER 暂定义为：

> **一个由人主导、面向复杂专业设计工作的 Human–AI Design Operating System。它帮助设计者持续维护设计问题、价值、关系、真实可编辑产物、证据、专业协同、审查与连续性，同时把系统内部复杂性尽量留在后台。**

OLEANDER 的核心不是“完成任务”，而是：

> **帮助设计者持续形成更好的设计判断，并把这些判断推进成更成熟、更完整、更可信的设计。**

## 1.1 产品不是

- Chat UI 本身；
- Prompt Library；
- 文件管理器；
- Notion / GitHub 包装层；
- 单一 CAD / BIM / Figma / 3D / IDE 替代品；
- 单一工作流 checklist；
- Agent 监控面板；
- 自动替代设计师或专业人员的系统；
- 只做检索、不推进设计的知识库；
- 只做项目管理、不理解设计关系的软件；
- 把所有专业统一为一套 CoDesign stage 的流程产品。

## 1.2 产品必须最终证明的价值

1. 真实设计工作被推进；
2. 中断后可以恢复真实设计 frontier；
3. Current Design Question 与 Current Direction 可识别；
4. 用户不需要重复解释仍有效的项目背景；
5. 真正 editable / native artifact 被维护；
6. 设计关系和意图跨迭代不丢失；
7. 方案探索产生实质差异而非表面 variation；
8. critique 可以变成下一步 design action；
9. tool execution 不冒充 readback / design success；
10. verification 与 validation 分开；
11. 失败只重开受影响范围；
12. 多专业保持真实专业过程；
13. AI 自动化不越过 Human authority；
14. 项目经验可以回流，但不自动变成伪规律。

---

# 2｜目标用户与角色

## 2.1 Direct Users

| ID | 用户角色 | 主要责任 | 产品最重要的结果 |
|---|---|---|---|
| DU-01 | Design Author | 维护作者性、设计价值和整体方向 | 设计意图长期连续 |
| DU-02 | Design Lead | 决定当前设计问题、探索深度与收敛节奏 | 知道下一步最值得解决什么 |
| DU-03 | Domain Designer / Professional | 在真实专业语境中深化设计 | 专业输入真实、边界明确 |
| DU-04 | Integrator | 维护跨专业 / 跨尺度一致性 | 改动后整体仍成立 |
| DU-05 | Reviewer / Critic | 审查真实 artifact、发现问题 | finding 可转成行动 |
| DU-06 | Design Producer | 建模、绘图、编码、模拟、制作 | 判断进入真实可编辑 artifact |
| DU-07 | Knowledge / Research Steward | 维护来源、适用性、反例 | 知识支持设计但不污染项目事实 |
| DU-08 | Client / Limited Collaborator | 阅读、提供要求或有限决策 | 不理解内部治理也能看清项目真相 |

## 2.2 Design-Affected People

最终使用者、访客、居民、儿童、老年人、残障人士、员工、运营、维护、施工、制造、客户、公众、审批/监管主体、后续接手团队等。

**Direct User Need ≠ End-user Need。**

OLEANDER 的直接产品体验服务设计者，但设计 validation 必须最终回到真实使用者和真实情境。

## 2.3 System Actors

AI、Agent、Worker、Validator、Tool、Connector、Authoring App 都是 system actor，不是最终用户。

```text
Agent can execute ≠ Agent owns the need
Agent can recommend ≠ Agent owns the decision
Agent is confident ≠ Human authorization
```

---

# 3｜核心使用情境

| ID | 使用情境 | 用户真正的问题 | 主要产品区域 |
|---|---|---|---|
| CTX-01 | 新建项目 | 我们到底为谁解决什么问题？ | FOCUS / KNOWLEDGE |
| CTX-02 | 中断后恢复 | 现在真正做到哪里？ | HOME / HISTORY |
| CTX-03 | 继续设计 | 下一步真实设计动作是什么？ | HOME / STUDIO |
| CTX-04 | 方案探索 | 有哪些真正不同的路线？ | STUDIO / COMPARE |
| CTX-05 | 模糊不满意 | “不对”的根因在哪里？ | REVIEW / MAP / STUDIO |
| CTX-06 | 方向选择 | 我接受什么 trade-off？ | COMPARE |
| CTX-07 | 专业深化 | 概念下一层需要解决什么？ | STUDIO / MAP |
| CTX-08 | 多专业协同 | 改动影响谁、谁负责？ | MAP / PEOPLE |
| CTX-09 | 制作真实产物 | 哪个才是真正 editable master？ | ARTIFACTS |
| CTX-10 | Reality Check | 实际结果和预期一致吗？ | ARTIFACTS / REVIEW |
| CTX-11 | Verification | 声明是否被相匹配证据支持？ | REVIEW |
| CTX-12 | Validation | 真实人/真实情境中有效吗？ | REVIEW |
| CTX-13 | 局部失败 | 哪里失败、哪些不用重做？ | REVIEW / MAP / STUDIO |
| CTX-14 | 人/Agent 交接 | 下一方能否直接继续？ | HOME / HISTORY |
| CTX-15 | 工具不可用 | 能否诚实降级继续？ | ARTIFACTS / INTEGRATIONS |
| CTX-16 | 发布/外部写入 | 现在真的有权执行吗？ | SESSION KERNEL / AUTHORITY |
| CTX-17 | 项目学习回流 | 哪些经验值得跨项目复用？ | HISTORY / KNOWLEDGE |

---

# 4｜Jobs To Be Done

## JOB-01｜恢复真实设计前沿
当我隔几个小时、几天或几周回来，我希望快速知道：
- current problem / question；
- current direction；
- current frontier；
- current native artifact；
- major decisions；
- critical open；
- stale assumptions；
- blocker；
- next high-value action。

## JOB-02｜从模糊问题进入可设计问题
当我只知道“这个不对”“想更开放”“入口有问题”时，我希望系统帮助把模糊感受变成可被设计和验证的问题，而不是逼我先填完整参数表。

## JOB-03｜探索真正不同的可能性
当方向尚未确定，我希望看到少量但 materially distinct 的候选，而不是几十个视觉 variation。

## JOB-04｜把设计判断变成真实产物
当一个方向值得继续，我希望它进入真实、可编辑、可检查的 artifact，而不是停留在说明文字、截图或 AI image。

## JOB-05｜比较并做负责任的决定
当多个方向都可能成立，我希望看清 relation difference、gain/loss、uncertainty、evidence gap、downstream consequence 和 reopen condition。

## JOB-06｜让 AI 自动推进但不越权
当工作低风险、可逆、已有授权时，我希望系统继续做；到真正的 Human value / authority boundary 时再停。

## JOB-07｜审查真实结果
当系统说“完成”，我希望能看到实际 artifact 和 readback，而不是执行者自我报告。

## JOB-08｜局部失败只重开局部
当某个来源、假设、接口、artifact 或专业判断失败，我希望只重开真实依赖范围。

## JOB-09｜保持多专业真实
当建筑、结构、MEP、产品、UX、软件等协同，我希望共享变量和影响清楚，但不把专业方法压成一个统一 checklist。

## JOB-10｜持续形成更好的设计判断
当我比较、批评和选择方案时，我希望系统适度解释真正重要的区别，但不把我变成被测评的“能力画像”。

---

# 5｜User Need Baseline

以下优先级属于产品需求，不等于 OLEANDER P0–P4 Project Axis。

## 5.1 Continuity

| ID | Priority | User Need |
|---|---|---|
| UN-P01 | CORE | 我需要始终知道当前真实设计 frontier。 |
| UN-P02 | CORE | 我需要知道当前 Design Question / Decision Object。 |
| UN-P03 | CORE | 我需要知道下一步真正允许且有价值的动作。 |
| UN-P04 | CORE | 我需要清楚区分 Current / stale / blocked / superseded。 |
| UN-P05 | CORE | 跨会话、跨人、跨 Agent 后不需要重新考古。 |
| UN-P06 | HIGH | 已确认且仍有效的背景不应被反复询问。 |

## 5.2 Design Intent & Judgment

| ID | Priority | User Need |
|---|---|---|
| UN-P07 | CORE | Design Value / Intent 在后续执行中持续可见。 |
| UN-P08 | CORE | Goal / Requirement / Constraint / Assumption / Preference / Decision 不混淆。 |
| UN-P09 | CORE | “我觉得不对”可以先被保留，再逐步形成 finding。 |
| UN-P10 | CORE | 重大设计失败不能被总体分数平均掉。 |
| UN-P11 | HIGH | 我需要看到 whole / local、intent / result、expected / observed 的差异。 |

## 5.3 Exploration & Decision

| ID | Priority | User Need |
|---|---|---|
| UN-P12 | CORE | 候选必须真正改变关系/策略/机制。 |
| UN-P13 | HIGH | 必要时 baseline / no-change / OFF 也应成为选项。 |
| UN-P14 | CORE | 选择前需要看清 trade-off 与 downstream consequence。 |
| UN-P15 | CORE | 关键 decision 需要 basis、uncertainty 和 reopen condition。 |
| UN-P16 | HIGH | rejected / deferred 方向保留 lineage，但不污染 Current。 |

## 5.4 Development & Integration

| ID | Priority | User Need |
|---|---|---|
| UN-P17 | CORE | 我需要知道当前设计成熟度真正缺什么。 |
| UN-P18 | CORE | 概念要能发展到 geometry / behaviour / detail / performance。 |
| UN-P19 | CORE | 专业深化不能让核心设计价值静默丢失。 |
| UN-P20 | CORE | 多专业改动需要看到 change impact。 |
| UN-P21 | HIGH | 设计复杂度需要被综合，而不是只会继续增加。 |

## 5.5 Reality & Evidence

| ID | Priority | User Need |
|---|---|---|
| UN-P22 | CORE | Editable/native artifact 必须可识别、可恢复。 |
| UN-P23 | CORE | Preview / export / AI visual 不得冒充 source authority。 |
| UN-P24 | CORE | Tool PASS 不等于 design/professional/readback PASS。 |
| UN-P25 | CORE | 重要 claim 需要实际 readback。 |
| UN-P26 | CORE | Verification 与 Validation 必须分开。 |
| UN-P27 | CORE | Evidence / Inference / Assumption / Decision 必须可区分。 |
| UN-P28 | HIGH | 证据不足应限制 claim，而不是冻结所有设计。 |

## 5.6 Human Agency

| ID | Priority | User Need |
|---|---|---|
| UN-P29 | CORE | AI 不能把 continuation 当成 design steer。 |
| UN-P30 | CORE | 高影响 value / direction / release / promotion 由 Human authority 决定。 |
| UN-P31 | CORE | AI 可自动推进可逆工作，不应每一步都停。 |
| UN-P32 | CORE | 歧义 referent 必须 fail closed。 |
| UN-P33 | HIGH | 多 Human 的 scoped rights 不因最新消息被覆盖。 |
| UN-P34 | HIGH | 系统解释支持可以减少，但不能形成永久能力/审美画像。 |

## 5.7 Failure & Recovery

| ID | Priority | User Need |
|---|---|---|
| UN-P35 | CORE | 失败时明确：哪里失败、什么仍有效、阻止什么、下一步是什么。 |
| UN-P36 | CORE | 局部问题只重开真实依赖范围。 |
| UN-P37 | CORE | stale checkpoint / stale authority 不得继续写。 |
| UN-P38 | HIGH | plugin / UI 替换不破坏项目状态与 native artifact。 |

---

# 6｜Experience Principles

| ID | Principle | Product implication |
|---|---|---|
| XP-01 | Design before Administration | 第一层先显示 design question / frontier，不先显示治理结构 |
| XP-02 | Reality before Assertion | 真 artifact / result 优先于系统声明 |
| XP-03 | Judgment before Automation | 高影响动作不由自动化替代判断 |
| XP-04 | Comparison over Abstract Scoring | 关系比较优于单一总分 |
| XP-05 | Whole and Part Together | 局部和整体可往返 |
| XP-06 | Preserve What Works | revision 默认保护已成立关系 |
| XP-07 | Open is Legitimate | OPEN 有原因、影响、关闭条件 |
| XP-08 | Progress Means Resolution | 进度来自设计成熟，不来自文件数量 |
| XP-09 | Human Authorship | 人保留关键价值与责任 |
| XP-10 | Complexity Must Earn Its Place | 新复杂度必须产生足够设计价值 |
| XP-11 | Proposal before Preference Questionnaire | 先做可比较候选，再问高价值偏好 |
| XP-12 | Progressive Disclosure | governance 只在影响行为时显性出现 |
| XP-13 | Honest Degradation | 能力缺失时降低 claim，不伪造完成 |
| XP-14 | Session ≠ State | 会话投影可丢弃，项目 truth 不依赖会话 |

---

# 7｜产品结构

v0.2.0 恢复并保留既有 Design Operating System 产品骨架，同时把 Human–AI Session Kernel 作为跨 surface interaction layer。

```text
OLEANDER
│
├── HOME        — Re-enter the real design state
├── FOCUS       — Define what matters now
├── STUDIO      — Explore / Develop / Synthesize
├── COMPARE     — Cross-surface decision mode
├── MAP         — Design relations / dependency / impact
├── ARTIFACTS   — Native reality / revision / readback
├── REVIEW      — Critique / Verification / Validation
├── KNOWLEDGE   — Evidence / applicability / design meaning
├── HISTORY     — Design continuity / rationale / handoff
│
├── PEOPLE      — responsibility / scoped authority
├── INTEGRATIONS— authoring / analysis / external systems
├── SETTINGS
└── SYSTEM HEALTH

Cross-product:
HUMAN–AI CO-DESIGN SESSION KERNEL
RESOLVE / RESUME / ROUTE / GUARD / HANDOFF / REPORT
+
UNDERSTAND / EXPLORE / MAKE / LOOK / CRITIQUE / STEER / LEARN
```

## 7.1 Surface Model

### THINK
FOCUS / STUDIO / MAP / COMPARE

### MAKE / SEE
ARTIFACTS / REVIEW

### REMEMBER / UNDERSTAND
HOME / KNOWLEDGE / HISTORY

Session Kernel 横跨三类 surface，不建立独立 Project State。

---

# 8｜一级 Product Area Definition

## 8.1 HOME — Project Home

**Core job:** 重新进入当前真实设计状态。

首屏只回答：
- 我们现在在解决什么？
- 当前方向是什么？
- 真正卡在哪里？
- 当前最相关 artifact 是什么？
- 下一步最值得做什么？

### Core feature inventory
- `HOME-F01` Resume Snapshot
- `HOME-F02` Frontier Card
- `HOME-F03` Critical Open
- `HOME-F04` Active Artifact
- `HOME-F05` Recent Design Moves
- `HOME-F06` Next Design Actions
- `HOME-F07` Resume Confidence / Source Basis
- `HOME-F08` What Changed Since Last Session

详细验收见：[`features/PRD_HOME_FOCUS_v0.2.0.md`](features/PRD_HOME_FOCUS_v0.2.0.md)。

## 8.2 FOCUS — Design Focus

**Core job:** 明确当前真正需要解决什么。

```text
Problem
→ Design Question
→ Value / Intent
→ Scope / Scale
→ Constraints
→ Assumptions
→ Success Condition
→ Frontier
```

### Core feature inventory
- `FOCUS-F01` Problem Statement
- `FOCUS-F02` Current Design Question
- `FOCUS-F03` Design Value / Intent
- `FOCUS-F04` Scope / Scale
- `FOCUS-F05` Constraints / Assumptions
- `FOCUS-F06` Success Condition
- `FOCUS-F07` Reframe
- `FOCUS-F08` Reframe Impact
- `FOCUS-F09` Frontier Definition

## 8.3 STUDIO — Design Studio

三种 mode：
- EXPLORE
- DEVELOP
- SYNTHESIZE

### Explore
- `EXP-F01` Create Direction
- `EXP-F02` Strategy Statement
- `EXP-F03` Relation Difference
- `EXP-F04` Alternative Set
- `EXP-F05` Search-space Gap
- `EXP-F06` Reference Transformation
- `EXP-F07` Hold / Continue / Retire
- `EXP-F08` Baseline / OFF Branch
- `EXP-F09` Material Distinctness Check

### Develop
- `DEV-F01` Maturity Gap
- `DEV-F02` Next Development Frontier
- `DEV-F03` Resolution Ladder
- `DEV-F04` Professional Depth
- `DEV-F05` Intent Check
- `DEV-F06` Low-resolution Warning
- `DEV-F07` Development Action
- `DEV-F08` Domain Adapter Binding
- `DEV-F09` Return-to-Whole Check

### Synthesize
- `SYN-F01` Complexity Review
- `SYN-F02` Merge Opportunity
- `SYN-F03` Design Economy
- `SYN-F04` Grammar Consistency
- `SYN-F05` Hierarchy Reinforcement
- `SYN-F06` Simplification Test
- `SYN-F07` Loss Check

详细验收见：[`features/PRD_STUDIO_COMPARE_v0.2.0.md`](features/PRD_STUDIO_COMPARE_v0.2.0.md)。

## 8.4 COMPARE — Cross-surface Compare Mode

COMPARE 是一种工作模式，不要求成为独立主导航。

Compare modes：
- Option / Option
- Before / After
- Intent / Result
- Local / Whole
- Expected / Observed
- Current / Proposed

Features：
- `CMP-F01` Side-by-Side
- `CMP-F02` Relation Difference
- `CMP-F03` Consequence Difference
- `CMP-F04` Trade-off
- `CMP-F05` Uncertainty
- `CMP-F06` Decision Rationale
- `CMP-F07` Reopen Condition
- `CMP-F08` Retained Alternative
- `CMP-F09` Same Comparison World
- `CMP-F10` Artifact Revision Binding
- `CMP-F11` Human Steer Capture

## 8.5 MAP — Design Map

**Core job:** 表达设计中“什么关系重要、什么影响什么”。

Layers：
- Intent
- Problem
- Relation
- Decision
- Dependency
- Artifact
- Review

Features：
- `MAP-F01` Relation Create
- `MAP-F02` Relation Link
- `MAP-F03` Relation Importance
- `MAP-F04` Relation Stability
- `MAP-F05` Change Impact
- `MAP-F06` Whole / Local Filter
- `MAP-F07` Artifact Binding
- `MAP-F08` Issue Binding
- `MAP-F09` Professional Binding
- `MAP-F10` Dependency Traversal
- `MAP-F11` Preserve-Unaffected Scope

详细验收见：[`features/PRD_MAP_ARTIFACTS_v0.2.0.md`](features/PRD_MAP_ARTIFACTS_v0.2.0.md)。

## 8.6 ARTIFACTS — Artifact & Reality

Artifact roles：
- Native Design Source
- Working Source
- Canonical Derivative
- Export
- Preview
- Prototype
- Simulation
- Reference
- AI Visual
- Snapshot

Features：
- `ART-F01` Artifact Register
- `ART-F02` Artifact Role
- `ART-F03` Native Source Link
- `ART-F04` Revision
- `ART-F05` Relation Binding
- `ART-F06` Design Question Binding
- `ART-F07` Readback Entry
- `ART-F08` Cross-Version Compare
- `ART-F09` Fidelity / Claim Ceiling
- `ART-F10` Content Hash / Revision Binding
- `ART-F11` Stale Artifact Warning
- `ART-F12` Degraded Substitute

## 8.7 REVIEW — Review & Validation

Review types：
- Design Critique
- Professional Review
- Readback Review
- Verification
- Validation

Features：
- `REV-F01` Review Target
- `REV-F02` Finding
- `REV-F03` Finding Type
- `REV-F04` Severity / Impact
- `REV-F05` Affected Relation
- `REV-F06` Root-cause Hypothesis
- `REV-F07` Recommended Design Action
- `REV-F08` Recheck Requirement
- `REV-F09` Independent Review
- `REV-F10` Validation Scenario
- `REV-F11` Verification Claim / Evidence
- `REV-F12` Does-not-prove Boundary
- `REV-F13` Revision Re-readback

详细验收见：[`features/PRD_REVIEW_KNOWLEDGE_HISTORY_v0.2.0.md`](features/PRD_REVIEW_KNOWLEDGE_HISTORY_v0.2.0.md)。

## 8.8 KNOWLEDGE — Knowledge & Evidence

Core principle：

> **回答当前设计问题需要知道什么，而不是管理所有知识。**

Features：
- `KNW-F01` Knowledge Need
- `KNW-F02` Source
- `KNW-F03` Evidence Strength
- `KNW-F04` Applicability
- `KNW-F05` Design Meaning
- `KNW-F06` Limitation
- `KNW-F07` Contradiction
- `KNW-F08` Precedent Transfer
- `KNW-F09` Return to Design
- `KNW-F10` Freshness / Staleness
- `KNW-F11` Claim Ceiling

## 8.9 HISTORY — Continuity & History

只记录改变设计理解的重要事件：
- reframe
- direction selection
- major rejection
- key trade-off
- intent change
- major artifact revision
- critical review
- reopened decision
- validation result
- frontier change

Features：
- `HIS-F01` Design Timeline
- `HIS-F02` Decision History
- `HIS-F03` Rejected Direction Memory
- `HIS-F04` Reframe History
- `HIS-F05` Frontier History
- `HIS-F06` Resume Point
- `HIS-F07` Handoff Pack
- `HIS-F08` Human-steer Lineage
- `HIS-F09` Project Learning Candidate

---

# 9｜Human–AI Co-Design Session Kernel

Session Kernel 是跨 surface 的 interaction kernel，不拥有 Project State。

## 9.1 Visible design kernel

```text
UNDERSTAND
→ EXPLORE
→ MAKE
→ LOOK
→ CRITIQUE
→ STEER
→ LEARN
```

## 9.2 Quiet runtime kernel

```text
RESOLVE
→ RESUME
→ ROUTE
→ GUARD
→ HANDOFF
→ REPORT
```

## 9.3 Four-axis interaction model

每条用户输入独立解析：

| Axis | Values |
|---|---|
| Work Intent | START / RESUME / RECOVER / EXPLORE / WILDCARD / REVIEW / REFRAME / SAVE_ROUTE / EXPLAIN / SHOW_WORK / UNRESOLVED |
| Mutation Directive | NORMAL / READ_ONLY / AUTO_ADVANCE_REVERSIBLE |
| Support Mode | AUTO / COMPACT / EXPLAIN / OFF |
| Human Action Level | NONE / FEEDBACK_SIGNAL / ITERATION_STEER / DESIGN_DECISION / DESIGN_KEEP / PROMOTION_DECISION |

规则：

```text
CONTINUE ≠ DEFER
FEEDBACK_SIGNAL ≠ ITERATION_STEER
ITERATION_STEER ≠ DESIGN_DECISION
DESIGN_DECISION ≠ DESIGN_KEEP
DESIGN_KEEP ≠ PROMOTION_DECISION
```

详细要求见：[`features/PRD_SESSION_KERNEL_CONTINUITY_v0.2.0.md`](features/PRD_SESSION_KERNEL_CONTINUITY_v0.2.0.md)。

---

# 10｜Human Steering

Iteration actions：

```text
SELECT
MODIFY
MIX
REJECT
REOPEN
DEFER
```

## 10.1 Consequential referent binding

任何会改变设计 branch 的 steer 必须绑定：

```text
REF
+ KIND
+ REVISION
+ LINEAGE_REF
(+ DECISION_OBJECT_REF when required)
```

## 10.2 Required behaviour

- “选 B”且 B 唯一可解析 → SELECT；
- “就这个”且只有一个 active object → 可绑定；
- “就这个”且多个 active object → 问一个 minimum clarification；
- MIX 少于两个 parent → fail closed；
- DEFER 无 pending decision → fail closed；
- Generic “继续” → no steer；
- “不要 A，保留 B，结合 C” → 保留 `REJECT A` + `MIX B,C` 两个 clause-scoped actions；
- Human 未提供 reason → 不伪造 reason。

## 10.3 Second-round proof

Human steer 真正“被实现”至少需要：

```text
EXPLICIT HUMAN SOURCE
→ DECISION RIGHTS / OWNER RULE
→ TYPED + REVISIONED REFERENT
→ NEW EDITABLE / NATIVE DELTA
→ SAME REVISION + CONTENT HASH READBACK
→ INVARIANT-SPECIFIC READBACK
```

文本确认本身不算第二轮实现。

---

# 11｜Human Stop Policy

系统只在真实边界停下：

1. consequential referent ambiguous；
2. 可比较 artifact 已经暴露 Human-only value choice；
3. scope / authority escalation；
4. irreversible external action；
5. publish / release；
6. specialist / independent review required；
7. multi-human decision rights conflict；
8. 无 truthful editable/native substitute；
9. 用户要求停止；
10. requested scope complete。

不应该因为以下原因停止：

- 一个 tool call 完成；
- 一个文件保存；
- 一个 Agent 返回；
- 一个低风险 reversible step 即将发生；
- 存在与当前 reversible question 无关的 OPEN。

---

# 12｜Core Object Model

```text
Project
├── ProjectContext
├── Constraint
├── Assumption
├── DesignProblem
├── DesignQuestion
├── DesignValue
├── DesignDirection
├── DesignRelation
├── DevelopmentFrontier
├── DesignDecision
├── Finding
├── Disagreement
├── Artifact / DesignRealization
├── RealizationChange / Revision
├── Readback
├── Observation
├── Evidence
├── VerificationClaim
├── VerificationResult
├── ValidationScenario
├── ValidationResult
├── RevisionScope
├── ResponsibilityAssignment
├── CurrentTruth
├── SupersessionRecord
├── ProjectObservation
├── ProfessionalLearningCandidate
├── TransferCondition
├── Counterevidence
└── HandoffInterpretation
```

## 12.1 Core interaction rules

1. 同一 active scope 应有明确 Current Design Question；
2. 一个 Question 可以有多个 Direction；
3. 一个 Direction 由多个 Design Relation 构成；
4. 一个 consequential Decision 必须影响真实 Relation；
5. Artifact 必须说明服务哪个 Question / Relation / Validation purpose；
6. important Revision 应触发新的 Readback；
7. Finding 必须指向 Artifact、Relation 或 Decision；
8. Validation 可以重开 Problem / Question；
9. History 只记录设计逻辑变化，不记录所有系统事件；
10. Assumption 永远不静默升级成 Fact；
11. Representation recency 不自动改变 native authority；
12. Session-local branch 不自动成为 Project Current。

---

# 13｜Information Architecture

Primary IA：

```text
PROJECT
│
├── NOW
│   ├── Current Question
│   ├── Current Direction
│   ├── Current Frontier
│   ├── Critical Open
│   └── Next Action
│
├── DESIGN
│   ├── Problem
│   ├── Value / Intent
│   ├── Alternatives
│   ├── Relations
│   ├── Decisions
│   └── Trade-offs
│
├── REALITY
│   ├── Artifacts
│   ├── Revisions
│   ├── Readbacks
│   ├── Reviews
│   ├── Verification
│   └── Validation
│
├── CONTEXT
│   ├── People
│   ├── Evidence
│   ├── Knowledge
│   ├── Constraints
│   └── Assumptions
│
└── CONTINUITY
    ├── History
    ├── Rationale
    ├── Handoff
    └── Learning
```

主导航建议：

```text
Home
Focus
Studio
Map
Artifacts
Review
Knowledge
History
```

Compare 作为跨 Studio / Review / Artifacts 的工作模式。

---

# 14｜核心 User Flows

## FLOW-01 Resume Design

```text
ENTER PROJECT
→ RESOLVE owner-native Current
→ HOME
→ Current Question
→ Current Direction
→ Frontier
→ Critical Open
→ Active Artifact
→ Next Action
→ FOCUS / STUDIO
```

**Success:** 用户不阅读聊天历史即可回答“现在做什么、为什么、用哪个 artifact”。

## FLOW-02 Frame / Reframe

```text
TRIGGER
→ FOCUS
→ Problem
→ Evidence / Assumption
→ Current Question
→ Reframe
→ MAP impact
→ affected Decisions
→ preserve valid work
→ new Frontier
```

## FLOW-03 Explore Alternatives

```text
DESIGN QUESTION
→ STUDIO / EXPLORE
→ 2–N strategy candidates
→ material distinctness
→ artifact prototype
→ COMPARE
→ remove cosmetic duplicates
→ Human steer or continue exploration
```

## FLOW-04 Tacit Critique

```text
REAL ARTIFACT
→ “这个不对”
→ REVIEW
→ preserve FEEDBACK_SIGNAL
→ cause hypotheses
→ MAP affected relation
→ repair alternatives
→ COMPARE
→ Human steer when necessary
```

## FLOW-05 Choose Direction

```text
COMPARE
→ relation differences
→ consequences
→ trade-offs
→ uncertainty
→ Human decision
→ rationale
→ reopen condition
→ selected / held / rejected lineage
```

## FLOW-06 Develop Design

```text
SELECTED DIRECTION
→ STUDIO / DEVELOP
→ Maturity Gap
→ Next Frontier
→ domain lens
→ native artifact
→ edit / make
→ READBACK
→ REVIEW
→ continue / revise / synthesize
```

## FLOW-07 Integrate Change

```text
CHANGE PROPOSED
→ MAP dependencies
→ affected professions
→ shared variables
→ local vs whole compare
→ integrated alternative
→ scoped human/professional decision
→ artifact changes
→ cross-domain readback
```

## FLOW-08 Synthesize

```text
DESIGN TOO COMPLEX
→ identify core / redundant relations
→ synthesis options
→ before / after compare
→ lost-value check
→ whole read
→ keep / reject
```

## FLOW-09 Reality Check

```text
ARTIFACT MADE
→ open actual result
→ READBACK
→ intended vs observed
→ defect?
  NO → continue
  YES → Finding
       → Root cause
       → Revision Scope
       → repair
       → re-readback
```

## FLOW-10 Verify / Validate

```text
DESIGN CLAIM
→ Is the question "implemented as specified"?
  YES → VERIFY → evidence → supported / unsupported
  NO  → Is the question "works for real people/context"?
        → VALIDATE → scenario → behaviour/outcome → design implication
```

## FLOW-11 Revise Without Reset

```text
FAILURE
→ finding
→ root-cause hypothesis
→ MAP dependency
→ affected scope
→ protect unaffected valid work
→ revise
→ readback
→ close / reopen
```

## FLOW-12 Continue with DEFER

```text
Human DEFER pending decision
→ preserve branches
→ dependent mutations HOLD
→ unrelated reversible actions continue
→ decision remains reopenable
```

## FLOW-13 Plugin-off / Session-off Resume

```text
Session UI unavailable
→ explicit project/task/object key
→ Current Project
→ Control Card
→ Execution Receipt / checkpoint
→ native artifact + readback
→ reconstruct ephemeral session view
```

## FLOW-14 Multi-human Conflict

```text
Designer vs Client vs Specialist disagreement
→ preserve each scoped role
→ identify affected effect
→ route through existing decision-right rules
→ HOLD affected effect only
→ unrelated reversible work continues
```

---

# 15｜Human / System Allocation

Automation 不按“AI 能不能做”，而按：

```text
CONSEQUENCE
× VALUE SENSITIVITY
× PROFESSIONAL LIABILITY
× REVERSIBILITY
× UNCERTAINTY
```

## 15.1 Allocation Classes

| Code | Allocation |
|---|---|
| A1 | HUMAN-ONLY |
| A2 | HUMAN-LED |
| A3 | SYSTEM-ASSISTED |
| A4 | AUTOMATABLE |
| A5 | EXTERNAL-TOOL |
| A6 | PROHIBITED-AUTOMATION |

## 15.2 Hard Human authority

Human final authority 至少保留：
- high-impact Design Value；
- high-impact Design Direction；
- legitimate Value Reframe；
- consequential design decision；
- professional responsibility；
- final Design KEEP where current contracts require；
- publication / irreversible external side effect；
- Promotion。

AI 可以 challenge、compare、suggest、detect、make、read back；不能因置信度高而获得这些 authority。

---

# 16｜Interface Principles

每个高影响 interface 至少回答：

```text
WHO PRODUCES?
WHO CONSUMES?
WHAT IS EXCHANGED?
WHY DOES IT MATTER?
WHO HAS AUTHORITY?
WHAT MUST BE ACKNOWLEDGED?
WHAT PROVENANCE IS REQUIRED?
WHAT HAPPENS IF INTERFACE FAILS?
```

## 16.1 Interface Families

- I1 Human Design Interface
- I2 Professional Domain Interface
- I3 Authoring / Analysis Interface
- I4 Evidence / Research Interface
- I5 Execution / Operation Interface
- I6 Organizational Authority Interface
- I7 Professional Learning Interface
- IX-A Change Propagation
- IX-B Readback Return
- IX-C Conflict / Escalation

## 16.2 Critical rule

```text
Producer completion ≠ Consumer acceptance
Analysis result ≠ Design decision
Tool operation complete ≠ Readback complete
Review comment ≠ Authority change
```

---

# 17｜Cross-product Behaviour Rules

## B-01 Progressive disclosure
默认先显示 design question / direction / frontier / artifact / next action。底层 authority / provenance / receipt 仅在影响用户行为时展开。

## B-02 Real artifact priority
有真实 artifact 时，审查和比较优先绑定真实 artifact，而不是生产者摘要。

## B-03 Relation priority
文件只是载体；用户判断应尽量回到 Design Relation / Question / Value。

## B-04 No-repeat valid context
仍有效的显式背景、约束和决定不反复询问。

## B-05 Local reopen
失败默认按 dependency 重开受影响范围。

## B-06 Honest OPEN
OPEN 必须至少有：
- reason；
- impact；
- what it blocks；
- close condition。

## B-07 No silent authority transfer
新消息、最新文件、最新 agent output、最新 presentation 不自动获得 Current authority。

## B-08 Design quality independence
Design / Professional / Evidence / Representation / Execution / Validation verdict 保持独立。

## B-09 No global preference inference
一次选择或 rejection 不创建 durable taste profile。

## B-10 Skill consolidation
优先 reuse / compose / parameterize / benchmark / refactor，不因单个问题就新增 Skill。

---

# 18｜Product Requirements Summary

Master PRD 不重复全部 System Requirements v1.7.0，而把它们转成产品验收要求。

## 18.1 Product Requirement Families

| Family | Focus |
|---|---|
| PR-HOME | Resume / Now |
| PR-FOCUS | Problem / Question / Value |
| PR-EXP | Exploration |
| PR-DEV | Development |
| PR-SYN | Synthesis |
| PR-CMP | Compare / Decision |
| PR-MAP | Relations / Dependency |
| PR-ART | Artifact / Revision / Readback |
| PR-REV | Critique / Verification / Validation |
| PR-KNW | Evidence / Applicability |
| PR-HIS | Continuity / History |
| PR-INT | Session Kernel / Interaction |
| PR-PEO | Human roles / authority |
| PR-XIF | External interfaces / degraded operation |
| PR-NFR | Product quality attributes |

逐项 feature acceptance criteria 见 `product-docs/features/`。

---

# 19｜Error / Edge / Degraded Cases

| ID | Case | Required behaviour |
|---|---|---|
| EC-01 | 用户只说“继续” | RESUME；不得产生 steer |
| EC-02 | “就这个”有多个 referent | minimum clarification；zero mutation |
| EC-03 | “这个不对” | FEEDBACK_SIGNAL；不造永久偏好 |
| EC-04 | MIX 只有一个 parent | fail closed |
| EC-05 | DEFER 没有 pending decision | fail closed |
| EC-06 | checkpoint stale | mutation HOLD，re-resolve Current |
| EC-07 | presentation 比 native 更新 | derivative 不覆盖 native authority |
| EC-08 | native tool unavailable | bounded editable substitute；completion claim HOLD |
| EC-09 | artifact created but unreadable | no validated/done claim |
| EC-10 | reviewer 和 producer 同一主体 | 不能冒充 independent review |
| EC-11 | Client 与 Specialist 冲突 | 保留 scoped rights，局部 HOLD |
| EC-12 | evidence stale | 降低 claim ceiling，标记 affected relations |
| EC-13 | partial external write success | 报告 partial，不得整体成功 |
| EC-14 | plugin removed | 从 owner-native carriers resume |
| EC-15 | retry exhausted | 停止该 effect，明确失败位置/剩余有效工作/下一步 |
| EC-16 | no truthful editable substitute | Human stop / HOLD_NATIVE_SURFACE |
| EC-17 | unknown field fact | 保持 OPEN；不得由 remote inference 填充 |
| EC-18 | conflicting Human actions same referent | clarification unless explicit sequence grammar |

---

# 20｜Metrics

> 以下是待验证的产品指标定义，不是已取得的商业结果。

## 20.1 North Star

### Successful Continuation Rate

```text
Sessions that correctly recover frontier
AND complete the next intended design step without state correction
/
Eligible re-entry sessions
```

“成功恢复”不能只看 `frontier_resolved` 事件；必须关联后续 outcome。

## 20.2 Primary Metrics

- Context Recovery Success Rate
- Human Correction Rate
- Repeated Context Input
- Useful Autonomy Rate
- Unauthorized Action Rate
- False Steering Rate
- Ambiguous Referent Safe-stop Rate
- Readback Completion Rate
- Second-round Implementation Fidelity
- Stale Mutation Prevention Rate
- Material Divergence Rate
- Cosmetic Duplicate Rate
- Critical-open Resolution Rate

## 20.3 Guardrail Targets

以下目标为 0：
- AI-owned Design KEEP
- AI-owned Promotion
- Unread Artifact Completion Claim
- Silent Authority Transfer
- Irreversible External Write Without Authorization
- Human feedback persisted as global taste/competence without explicit basis

## 20.4 Outcome metrics

后续真实用户测试至少需要：
- time to resume verified frontier；
- number of repeated context inputs；
- number of Human corrections before productive work；
- number of unnecessary confirmation stops；
- number of meaningful design alternatives；
- time from critique to actionable revision；
- percentage of material changes with readback；
- percentage of failures recovered without full reset；
- user confidence in “what is Current”；
- user confidence in “what AI may do next”。

---

# 21｜Event Instrumentation

| Event | Minimum fields | Outcome link |
|---|---|---|
| project_resume_started | project_ref, actor, entry_surface | continuation session |
| frontier_resolved | question_ref, direction_ref, artifact_ref, source_carriers | later continuation outcome |
| resume_corrected_by_user | correction_type, previous_projection | recovery failure |
| option_space_created | decision_object, option_refs, mechanism_signatures | exploration outcome |
| cosmetic_duplicate_detected | option_refs | divergence quality |
| artifact_made | artifact_ref, revision, role, parent_refs | readback |
| readback_started | artifact_ref, revision | readback completion |
| readback_completed | artifact_ref, revision, content_hash, findings | material outcome |
| human_feedback_received | raw_ref, action_level, support_mode | later steer |
| human_steer_bound | action, referents, decision_object, owner_rule | second-round |
| ambiguity_clarification_requested | candidates, reason | interaction quality |
| mutation_guard_blocked | reason, affected_effect | guardrail |
| second_round_completed | parent_refs, delta_ref, readback_ref | steer fidelity |
| finding_created | finding_type, affected_relation | revision outcome |
| revision_scope_created | affected_refs, preserved_refs | recovery outcome |
| human_stop_triggered | stop_reason | stop precision |
| validation_result_recorded | scenario_ref, outcome | problem/question update |
| session_closed | closure_dimensions | continuity |
| continuation_outcome_evaluated | success, user_correction_count, next_action_completed | North Star denominator/numerator |

事件数据是分析数据，不是 Project State authority。

---

# 22｜Non-functional Product Requirements

## NFR-01 Traceability
高影响 design claim 可回溯到 Question、Decision Basis、Artifact/Readback 和适用 Evidence。

## NFR-02 Recoverability
会话中断、人员切换、插件替换、工具失败后可以恢复关键 relation、decision 和 native artifact identity。

## NFR-03 State Honesty
UNKNOWN / unverified / unread / low-fidelity / conditional 不显示成已验证事实。

## NFR-04 Progressive Complexity
用户不需要理解内部 schema / runtime namespace 才能继续设计。

## NFR-05 Native Editability
持续发展的 artifact 不得被 view-only derivative 静默替换。

## NFR-06 Locality of Change
re-evaluation 优先限制在真实受影响范围。

## NFR-07 Human Intelligibility
关键建议、状态、失败原因能以设计者可理解语言解释。

## NFR-08 Cross-tool Continuity
跨 authoring environment 时 artifact identity / relation / intent 不丢失。

## NFR-09 Performance
常规 Resume Snapshot 应在用户可接受的交互时间内出现；若深层 authority/evidence resolve 仍在进行，应显式显示 provisional/loading，而不是静默阻塞。

## NFR-10 Auditability
重要 mutation / decision / readback / authority-sensitive action 具备可追踪记录。

## NFR-11 Graceful Degradation
缺少 integration / tool / evidence 时保留 truthful bounded workflow。

## NFR-12 Privacy / Confidentiality
产品化前需定义 project / organization / external collaborator 的最小权限和数据边界；当前仍是开放产品需求，不在本 PRD 伪造最终安全架构。

---

# 23｜MVP Scope

真正 MVP 验证的问题：

> **一个 Human–AI design environment 如果能够持续维护 Design Question、Design Relation、真实 Artifact、Human Steer 和 Readback，是否能显著改善复杂设计判断与连续性？**

## 23.1 MVP IN

1. HOME / Resume Snapshot
2. FOCUS / Current Design Question
3. STUDIO / Explore + Develop
4. COMPARE mode
5. MAP / core relation + change impact
6. ARTIFACT binding + revision identity
7. Actual Readback
8. REVIEW / critique → action
9. Human Steering
10. Mutation Guard
11. HISTORY / Resume Point
12. Session Kernel four-axis parsing
13. Reversible auto-advance
14. Separated closure

## 23.2 MVP OUT

暂不要求：
- auto maturity score；
- auto validation；
- universal genericity scoring；
- full enterprise RBAC；
- full cloud file layer；
- every external tool integration；
- large-scale multi-agent topology；
- commercial billing；
- global marketplace；
- complete team workspace；
- auto professional approval。

---

# 24｜MVP Acceptance Gates

## Gate A｜Resume
- 能从 owner-native carrier 恢复；
- Chat summary 不作为唯一 authority；
- user correction 可被观测；
- 下一步真实工作可以继续。

## Gate B｜Explore
- 至少两个 materially distinct mechanisms；
- cosmetic duplicates 不计数；
- 有 causally relevant baseline/OFF 时可保留。

## Gate C｜Make / Readback
- 至少一个真实 editable / native artifact；
- making 后 actual readback；
- readback 与 exact revision/content 绑定。

## Gate D｜Human Steer
- SELECT / MODIFY / MIX / REJECT / REOPEN / DEFER 至少覆盖真实场景；
- ambiguous referent fail closed；
- compound action 不折叠。

## Gate E｜Second Round
- Human source；
- decision-right proof；
- new artifact delta；
- same-revision/hash readback；
- preserved invariant 可核验。

## Gate F｜Authority
- irreversible / publish / promotion 不自动执行；
- latest Human message 不获得 universal authority；
- domain professional boundary 保留。

## Gate G｜Continuity
- 新会话可恢复；
- plugin-off / UI replacement 不破坏 state；
- stale checkpoint write 被拦截。

## Gate H｜Closure
分开输出：
`SESSION_RESULT / DESIGN_CANDIDATE / PROFESSIONAL_STATE / REVIEW_STATE / PERSISTENCE_STATE / PROMOTION_STATE`

---

# 25｜Validation Plan

## V1 Requirements Review
检查 atomicity、ambiguity、implementation bias、duplicate、missing trace、non-verifiable wording。

## V2 Scenario Walkthrough
至少：
- architecture / spatial；
- digital / HCD；
- physical product；
- visual / communication；
- multidisciplinary。

## V3 Interaction Prototype
重点验证：
- Resume；
- “继续” vs steer；
- “就这个” ambiguity；
- negative feedback；
- option compare；
- Human MIX；
- DEFER partition；
- readback；
- critique → revision。

## V4 Real Human Project Exercise
至少验证：
- Human steering；
- continuation；
- correction count；
- unnecessary stop；
- second-round fidelity；
- failure recovery。

## V5 Longitudinal
跨天 / 跨会话 / plugin replacement。

## V6 Multi-human
Designer / Client / Specialist / Reviewer 冲突与 scoped rights。

---

# 26｜Current Candidate Implementation Mapping

当前 Human–AI Co-Design vNext 仍是独立 Candidate，不是 Current。

Candidate 已覆盖的产品机制包括：
- three-view one-architecture projection；
- Session Kernel；
- four-axis interaction；
- compound human actions；
- typed/revisioned referents；
- option lineage；
- mutation guard；
- computed Human stop；
- designer-support fade；
- domain adapter；
- spatial / digital / physical real-artifact trials；
- regression suite。

仍未因此自动证明：
- 商业产品已上线；
- 外部用户已经验证；
- 所有 domain production-ready；
- Current promotion；
- plugin removal destructive trial 已闭合；
- real Human second-round 在所有重要 action 上闭合。

Candidate implementation:
[Human–AI Co-Design vNext](https://github.com/Jiaosong/Design/tree/candidate/oleander-human-ai-codesign-vnext-20260924/00-governance/runtime/candidates/human-ai-codesign-vnext)

---

# 27｜Upstream Trace Strategy

v0.2.0 保留以下来源链，不从当前软件实现反推需求：

```text
Behaviour Research
→ Pure User Needs
→ Experience Requirements
→ Capability / Functional Architecture
→ Information Architecture
→ Human/System Allocation
→ Interface Architecture
→ System Requirements
→ Product PRD / Feature Specs
→ Validation
```

产品 Feature 不复制全部 167 条 System Requirement，而通过 trace matrix 关联。

详见：[OLEANDER_PRD_TRACEABILITY_MATRIX_v0.2.0.md](OLEANDER_PRD_TRACEABILITY_MATRIX_v0.2.0.md)。

---

# 28｜Product Prioritization

## CORE-1 / P0
- Current Design Question
- Current Frontier
- Resume
- Material Alternatives
- Human Steer
- Native Artifact Binding
- Readback
- Critique → Action
- Mutation Guard
- History / Resume Point

## CORE-2 / P1
- Maturity Gap
- Change Impact
- Trade-off
- Intent Drift
- Synthesis
- Verification
- Knowledge Meaning
- Cross-domain relation
- Multi-human rights
- Designer development

## LATER / Research-sensitive
- exploration sufficiency automation
- genericity assistance
- design economy automation
- auto maturity recommendation
- safe-open automation
- behavioural validation automation
- AI critique scoring

---

# 29｜Open Product Questions

1. HOME 在极简 Resume Snapshot 和完整 project context 之间的最佳 progressive disclosure 是什么？
2. Compare 应保持全局 mode 还是在复杂项目中需要独立 workspace？
3. Design Map 对普通设计师的学习成本是否过高？
4. Relation 何时值得成为 first-class object？
5. “Materially distinct” 的 UI 如何表达，不依赖模型自报？
6. AUTO_ADVANCE_REVERSIBLE 的默认边界如何让用户理解但不增加设置负担？
7. Designer development 的提示频率如何不打断 flow？
8. 多 Human scoped rights 的可视化如何避免暴露治理复杂度？
9. Successful Continuation Rate 的真实 baseline 是多少？
10. 外部团队是否真正愿意维护 reopen condition / rationale，还是需要系统自动捕获后由 Human correction？
11. Enterprise privacy / organization boundary 的最低产品要求是什么？
12. Local / offline / native authoring execution 在 v1 中应覆盖到什么程度？

---

# 30｜一句话产品定义

> **OLEANDER 设计协作系统不是让 AI 更会“生成设计”，而是把“发现正确问题、形成真实差异、把判断做进真实产物、共同审查、由人作关键决定，并在下次会话准确继续”设计成一个长期可用的 Human–AI 产品。**

---

## Related Documents

- [Product Docs Index](README.md)
- [Feature Specifications](features/README.md)
- [PRD Traceability Matrix](OLEANDER_PRD_TRACEABILITY_MATRIX_v0.2.0.md)
- [OLEANDER Main README](../README.md)
- [Cases](../05-cases/)
- [Evals](../evals/)
- [Governance](../00-governance/README.md)
