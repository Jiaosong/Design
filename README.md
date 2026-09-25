# OLEANDER／织作

**AI Product · Human–AI Collaboration · Product & Design Systems**

OLEANDER 是我持续设计、实现与验证的一套 **Human–AI Co-Design System**。  
它既是一项 0→1 AI 产品实践，也是我用真实设计项目验证长期人机协作机制的工作仓库。

我的正式背景是 **产品设计**，实践覆盖交互、视觉、CMF、三维、空间／建筑研究与 AI 协同工作流。  
我长期关注的不是“AI 能不能再多生成一个结果”，而是：

> **如何把能力很强、但存在不确定性与上下文限制的 AI，设计成一个用户可以长期、连续、可控地协作的产品。**

[个人主页](https://github.com/Jiaosong) · [产品文档 / PRD](product-docs/v0.3/README.md) · [案例目录](05-cases/) · [评估体系](evals/) · [Governance](00-governance/README.md)

---

## TL;DR｜先用 1 分钟理解

**OLEANDER 要解决的问题**

传统 AI Chat 擅长单次回答，但复杂项目需要长期状态、知识、决策、版本、文件、验证和人工控制。OLEANDER 尝试把这些能力组织成一个持续协作系统。

**它不是**

- 单纯的 Prompt 集合
- 只负责生成图片或文本的工具
- 完全自动化替代设计师的 Agent
- 把聊天记录直接当项目状态的系统

**它更接近**

> AI Chat → AI Workflow → AI Workspace → Long-term Human–AI Collaboration

**核心产品原则**

> **Conversation is an interface. Project State is the product reality.**

> **Trustworthy Automation + Meaningful Human Control**

---

# 01｜项目背景：为什么做 OLEANDER

长期使用通用 AI 进行建筑、视觉、空间、研究和复杂知识工作时，我发现很多失败并不来自“模型不够聪明”，而来自产品层。

典型问题包括：

| 现象 | 更底层的产品问题 |
|---|---|
| 新会话里 AI 不知道项目做到哪里 | Project Continuity |
| 聊天记忆、事实、旧版本混在一起 | Project State |
| AI 太被动，需要一步步提示 | Agent Autonomy |
| AI 太主动，会擅自推进关键决定 | Human Control / Decision Rights |
| 文件、来源、判断、推断混在一起 | Knowledge & Evidence |
| 多方案只是同一个方案的表面变体 | Design Exploration |
| 工具执行结束就默认任务成功 | Readback / Validation |
| 项目经验难以进入下一项目 | System Evolution |

因此，我把最初的问题：

> “怎样让 AI 回答得更好？”

逐步重新定义成：

> **怎样设计一个能够在长期项目里维持状态、权限、知识、验证和人类决策权的 AI 产品？**

这成为 OLEANDER 的产品起点。

---

# 02｜目标用户与使用场景

OLEANDER 第一阶段并不面向所有用户，而是聚焦于：

> **需要和 AI 长期协作完成复杂专业项目的知识工作者。**

目前主要通过以下真实场景验证：

- 产品与服务设计
- 视觉与品牌设计
- CMF 与材料研究
- 空间与建筑设计
- 文化与设计研究
- 数字界面与网页
- 多文件、多版本、长周期专业项目

这些场景共同具有几个特征：

- 项目不会在一个 Prompt 内完成
- 用户本身拥有专业判断
- 需要处理多个版本与多个对象
- AI 可以承担大量工作，但不能拥有所有决策权
- 输出是否“存在”与是否“正确”是两回事
- 项目价值往往来自长期积累，而不是一次生成

---

# 03｜核心产品假设

OLEANDER 当前围绕七个核心假设持续验证。

### H1｜Project Continuity
一个长期 AI 产品必须知道“项目现在在哪里”，而不是只记得“用户以前说过什么”。

### H2｜Project State
聊天历史不能直接承担正式项目状态。Current、Candidate、Evidence、Decision、Artifact 等对象需要有明确身份与关系。

### H3｜Autonomy × Control
Agent 产品不能只做“全自动 / 全手动”二分。不同动作需要不同权限等级。

### H4｜Knowledge & Evidence
事实、来源、推断、设计判断与开放问题必须保持可区分，否则 AI 很容易把“可能”变成“已经确认”。

### H5｜Design Exploration
真正有价值的多方案不是数量更多，而是候选方案之间存在实质差异，并能被比较、批评和淘汰。

### H6｜Validation
工具调用成功、文件生成成功、脚本通过，都不能独立证明任务完成。执行之后必须存在 Readback。

### H7｜System Evolution
系统演进应优先复用、组合、参数化与重构现有能力，而不是每遇到问题就创建新的 Skill。

---

# 04｜Human–AI 协作闭环

~~~mermaid
flowchart TD
    A[Understand Current Project] --> B[Recover State / Knowledge / Evidence]
    B --> C[Explore Alternatives]
    C --> D[Compare / Critique / Filter]
    D --> E{Human decision required?}
    E -- Yes --> F[Human Decision]
    E -- No --> G[Authorized AI Action]
    F --> G
    G --> H[Execute / Produce Artifact]
    H --> I[Readback / Validate]
    I --> J{Result valid?}
    J -- No --> K[Repair / Re-enter]
    K --> C
    J -- Yes --> L[Update Project State]
    L --> M[Continue]
~~~

这套闭环强调三个差异：

**不是 Generate → Done**  
而是 **Generate → Validate → State Update**

**不是 AI 决定一切**  
而是 **AI autonomy 受任务风险、可逆性、影响范围和决策权约束**

**不是聊天越长越“懂项目”**  
而是 **正式状态独立于对话历史**

---

# 05｜产品对象模型

OLEANDER 将长期协作拆成一组相互独立但可关联的产品对象。

~~~mermaid
flowchart LR
    U[Human] --> D[Decision]
    A[AI / Agent] --> T[Task]
    T --> X[Execution]
    X --> R[Readback]
    R --> S[Project State]

    K[Knowledge] --> T
    E[Evidence] --> K
    E --> D

    D --> S
    S --> T
    X --> AR[Artifact]
    AR --> R

    R --> V[Validation]
    V --> S
~~~

### Project State
描述项目“当前真实状态”，包括当前阶段、有效版本、开放问题、阻塞项和下一步。

### Knowledge
可以被项目调用的结构化知识，但不等于事实本身。

### Evidence
来源、证据、测试、现场信息或可追溯依据，用来限制 Claim Ceiling。

### Decision
明确谁做了什么决定、针对哪个对象、在哪个版本上生效。

### Task
系统当前需要完成的工作，不等同于项目阶段。

### Artifact
图纸、模型、网页、视觉、文档、数据、代码等实际产物。

### Validation
判断执行结果是否满足相应质量、证据或流程要求。

这些对象的核心价值是：

> **避免把整个产品状态压缩进聊天记录。**

---

# 06｜Human-in-the-loop 权限设计

OLEANDER 不把“AI 是否自动执行”看成单一开关，而是区分不同层级。

| 层级 | 典型行为 | AI 权限 |
|---|---|---|
| Explore | 搜索、发散、建立候选 | 可自主 |
| Analyze | 对比、批评、风险识别 | 可自主 |
| Recommend | 给出推荐与 trade-off | 可提出，不直接改变关键状态 |
| Reversible Execute | 可撤销、低风险执行 | 满足条件时可执行 |
| Confirmed Execute | 影响正式状态或外部系统 | 需要明确授权 |
| Human-only Decision | 设计取舍、专业责任、最终发布等 | AI 不得替代 |

这套设计针对的是 Agent 产品中一个很实际的问题：

> AI 太被动，用户会承担全部过程管理；  
> AI 太主动，产品又不可控。

所以目标不是“最大化自动化率”，而是：

> **把人类保留在真正有价值的决策位置。**

---

# 07｜MVP 是什么

OLEANDER 的第一性 MVP 不是完整知识库、完整多 Agent 平台，也不是所有设计工具都接入。

它验证的是一个更窄的问题：

> **AI 能否在长期项目中恢复正确状态，在不越权的情况下继续工作，并把执行结果可靠地写回项目状态？**

因此 MVP 的核心链条可以压缩成：

~~~text
Project State
+ Context Recovery
+ Human Decision
+ AI Action
+ Readback
~~~

其他能力——知识库、云端文件、更多 Skill、多工具、多端协作——只有在这条链成立之后才有意义。

完整产品工作包见：[OLEANDER Product Operating Package v0.3.0](product-docs/v0.3/README.md)。详细的 141 项 Feature / Flow / Acceptance / Traceability 基线仍保留在 [PRD v0.2.0](product-docs/OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)。

---

# 08｜产品架构：公开仓库如何对应系统能力

~~~mermaid
flowchart TB
    A[Public Entry / README] --> B[Cases]
    A --> C[Evals]
    A --> D[Governance]
    A --> E[Skills]
    A --> F[Practice]

    B --> G[Real Project Evidence]
    C --> H[Behavior Validation]
    D --> I[Authority / State / Quality Rules]
    E --> J[Reusable Capabilities]
    F --> K[Small-scale Experiments]

    G --> L[OLEANDER Product Learning]
    H --> L
    I --> L
    J --> L
    K --> L
~~~

仓库中的不同目录并不是“文件分类习惯”，而是承担不同证据角色。

---

# 09｜仓库地图｜Repository Map

| 路径 | 作用 | 建议什么时候读 |
|---|---|---|
| [00-governance/](00-governance/) | 系统架构、状态、权威、质量、晋级、审计与专业流程 | 想深入理解 OLEANDER 如何保持可靠性 |
| [01-business/](01-business/) | 商业定位、价值、模式、运营、指标与治理 | 想看设计如何进入商业语境 |
| [02-culture/](02-culture/) | 来源、文化、设计史、解释、参与与延续 | 想看文化研究如何进入设计 |
| [03-ip/](03-ip/) | Identity、Narrative、Visual / Verbal、Application / Licensing | 想看品牌与视觉系统 |
| [04-spatial/](04-spatial/) | Site、Program、Space、Construction / Operation | 想看空间与建筑工作流 |
| [05-cases/](05-cases/) | C01–C04 真实案例 | 想最快看真实项目 |
| [06-practice/](06-practice/) | 练习、训练、小尺度实验 | 想看新机制怎样低成本验证 |
| [evals/](evals/) | AI workflow 的结构化评估与回归 | 想判断系统是否只有概念 |
| [oleander-skills/](oleander-skills/) | 可复用工作流与能力模块 | 想看能力如何封装与复用 |
| [tests/](tests/) | 自动化／结构化实现测试 | 想看实现层回归 |
| [tools/](tools/) | runtime、Blender surface 等工具 | 想看执行与工具层 |
| [website/](website/) | Web 呈现、Release Gate、可访问性等 | 想看公开数字体验 |
| [90-shared/](90-shared/) | 跨项目共享协议、资产与工具链 | 想看公共支撑层 |
| [99-archive/](99-archive/) | 历史、Legacy、非 Current 内容 | 追溯旧版本时阅读 |

---

# 10｜推荐阅读路线

## 路线 A｜招聘者 / 产品经理面试官

建议先看：

**本 README → 05-cases → evals → 00-governance**

你可以重点观察：

- 我如何把模糊问题重新定义为产品问题
- 如何定义 MVP 和核心产品对象
- 如何设计 Agent Autonomy × Human Control
- 如何把失败案例转成产品规则
- 如何通过真实项目而不是纯 Demo 验证假设

如果时间只有 10 分钟，不需要先读治理协议。

---

## 路线 B｜AI / Agent 产品方向

建议：

**核心产品假设 → evals → 00-governance → oleander-skills → cases**

重点入口：

- [evals/runtime/](evals/runtime/)
- [evals/trust/](evals/trust/)
- [evals/cross-context/](evals/cross-context/)
- [evals/failure/](evals/failure/)
- [evals/provenance/](evals/provenance/)
- [evals/change-control/](evals/change-control/)

这里更适合观察：

**state / authority / trust / provenance / failure / regression**

---

## 路线 C｜产品、视觉、CMF、空间与建筑设计

建议：

**05-cases → 04-spatial / 03-ip / 02-culture → 06-practice**

重点观察：

- 研究如何进入设计判断
- 设计对象之间如何建立关系
- 方案如何发散、比较与收敛
- AI 如何承担研究与执行，而不替代专业判断
- 真实设计资产如何经过 Post-Generation Review

---

## 路线 D｜系统架构与治理

建议：

**00-governance/README → canonical policies → runtime → audits**

优先入口：

- [Governance README](00-governance/README.md)
- [Anti-Pollution Protocol](00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md)
- [No Compression / No Loss](00-governance/OLEANDER_NO_COMPRESSION_NO_LOSS_POLICY_v1.0.md)
- [Post-Generation Review Gate](00-governance/post-generation-review-gate.md)
- [Architecture Design Development Process](00-governance/architecture-design-development-process-v1.0.md)

这部分不是对外产品叙事的第一层，但它解释了系统为什么不会把一次运行、一次生成或一个新文件直接晋级为正式结论。

---

# 11｜Evals：如何验证 OLEANDER

[evals/](evals/) 的目标不是评估“模型是否聪明”，而是：

> **评估 OLEANDER AI workflow 作为系统是否保持正确行为。**

当前评估方向包括：

| 目录 | 主要关注 |
|---|---|
| change-control | 变更是否受到正确约束 |
| cross-context | 跨会话／跨上下文是否保持正确状态 |
| failure | 失败、异常与恢复路径 |
| golden | 稳定基准案例 |
| provenance | 来源、证据与追溯 |
| retrieval | 是否调用正确知识与权威来源 |
| runtime | 运行行为是否符合契约 |
| trust | 权限、控制与可信执行 |

当前 Eval philosophy 明确要求：

- 真实 OLEANDER 任务优先于抽象 benchmark
- blocker failure 可以覆盖高平均分
- 证据权威、truth state、版本与 scope 与语言流畅度同样重要
- “写得很好但捏造证据”属于失败
- 模型、Prompt、Skill、Retrieval、Parser、Tool 变化都应做回归比较
- 安全、权利、文化权威和最终设计决策仍需要 Human Review

详细说明见 [evals/README.md](evals/README.md)。

---

# 12｜Selected Works｜真实案例

## C01｜一脉广渡
[进入案例](05-cases/c01-yimai-guangdu/)

**方向：Culture + Spatial**

当前公开状态：**RESEARCH + PROPOSAL / EVIDENCE REVIEW**

适合观察：

- 文化证据如何影响设计
- 空间、叙事、视觉如何组织
- 设计判断与证据边界如何区分
- Human–AI 长流程如何处理复杂设计对象

---

## C02｜忘也 Daylily
[进入案例](05-cases/c02-daylily/)

**方向：Business + IP + Spatial**

当前公开状态：**INDEPENDENT PORTFOLIO / PROTOTYPED / TEST PLANNED / NOT RUN**

该状态刻意区分：

> 原型已经存在 ≠ 用户测试已经执行

---

## C03｜The Light Collection
[进入案例](05-cases/c03-the-light-collection/)

**方向：CMF / IP / Visual**

当前公开状态：**PORTFOLIO CONCEPT / VISUALIZED / SAMPLE TEST PENDING**

这是个人独立概念研究，不代表 OPPO 的委托、采用、量产或背书。

---

## C04｜Qingjiang Stone Book
[进入案例](05-cases/c04-qingjiang-stone-book/)

**方向：Culture + Spatial + Digital Interaction**

这是一个更复杂的多资产长期项目，可用于观察：

- 空间与文化研究
- 数字交互与网页
- 视觉阅读
- 三维资产
- runtime / responsive workstream
- 多工作流之间的状态与证据管理

---

# 13｜设计能力如何进入产品能力

我的正式背景是**产品设计**，同时长期进行交互、视觉、CMF、三维和空间／建筑方向实践。

这些并不是产品经理之外的“额外技能”，而是我处理复杂产品问题的方法来源。

设计训练让我持续处理：

- 模糊需求
- 用户行为
- 功能关系
- 空间关系
- 材料与工艺
- 多重约束
- 多方案比较
- 信息层级
- 视觉表达
- 从概念到实施的连续迭代

因此，我在产品工作中更倾向于同时考虑：

> **User Need + System Constraint + Interaction + Implementation + Validation**

而不是只处理 Feature List。

---

# 14｜我的产品经理能力在仓库中的对应证据

| 能力 | 仓库中的对应表现 |
|---|---|
| Problem Discovery | 从 AI “不好用”拆解到 continuity / state / authority / trust |
| Product Definition | OLEANDER 的系统对象、边界与核心原则 |
| MVP | Project State + Context Recovery + Human Decision + AI Action + Readback |
| Interaction Design | Human-in-the-loop 与分级 autonomy |
| Workflow Design | 长周期、多状态、多对象协作 |
| Product Architecture | Governance / Cases / Evals / Skills / Practice 的职责分层 |
| Validation | evals、tests、Readback、Post-Generation Review |
| Iteration | failure-driven repair、regression、版本与 migration |
| Domain Understanding | 产品、视觉、CMF、空间、建筑与研究案例 |

---

# 15｜OLEANDER 的设计探索机制

传统 AI 使用经常是：

**用户给一个方向 → AI 沿该方向继续优化**

OLEANDER 更希望形成：

~~~text
Constraint Understanding
→ Divergent Exploration
→ Materially Distinct Alternatives
→ Critique
→ Compare Trade-offs
→ Filter Weak / Redundant Options
→ Human Decision
→ Development
~~~

这里的重点不是“多生成几张图”，而是：

> **候选方案之间是否真的代表不同的设计判断。**

因此，生成数量本身不是评价指标。

---

# 16｜Skills：能力如何复用，而不是无限增殖

[oleander-skills/](oleander-skills/) 当前包含 3D pipeline、data visualization、delivery QC、design process、image art direction、motion、research、story & board、visual design、web UI 等能力方向。

但 OLEANDER 当前并不把“Skill 数量更多”视为系统进步。

优先顺序是：

> **Reuse → Compose → Parameterize → Benchmark → Refactor**

只有当重复证据证明现有能力无法在不失真的情况下表达某个稳定需求时，才应形成新的能力模块。

这也是为了避免 Agent 系统最终变成不可维护的工具碎片集合。

---

# 17｜如何理解状态、证据和质量

OLEANDER 中几个非常重要的区分是：

> **CURRENT ≠ CLEAN**  
> **Artifact existence ≠ Design quality**  
> **Traceability ≠ Professional finish**  
> **Evidence correctness ≠ Visual excellence**  
> **Process PASS ≠ MAIN KEEP**  
> **Machine PASS ≠ Design PASS**  
> **Executed ≠ Validated**

也就是说：

文件存在，不代表设计成立。  
自动测试通过，不代表专业判断通过。  
AI 找到来源，不代表结论已经充分证明。  
一个 Candidate 产生，不代表它自动成为 Current。

### 常见证据状态

**VERIFIED / FACT**  
已有明确可验证依据。

**SUPPORTED**  
有证据支持，但强度或覆盖范围有限。

**INFERRED**  
合理推断，但不能伪装成事实。

**OPEN**  
尚未解决或需要进一步验证。

---

# 18｜Post-Generation Review

OLEANDER 的设计输出不会因为“生成完成”自动被视为完成。

基本闭环是：

~~~text
Generate
→ Automated QA
→ Open Final Artifact
→ Post-Generation Review
→ Fix
→ Re-review
→ Persist / Archive
~~~

根据产物类型，会继续检查：

- 视觉质量
- 遮挡与信息可读性
- 比例与尺度
- 几何与标注一致性
- Cross-view consistency
- 构造／功能逻辑
- 数据与来源
- 可访问性
- 发布边界

Canonical rule：

[Post-Generation Review Gate](00-governance/post-generation-review-gate.md)

---

# 19｜One Current Authority

OLEANDER 执行：

> **One Logical Object → One Current Authority → traceable Candidate / Evidence / Provenance children**

它解决的是复杂系统中一个非常实际的问题：

当 Notion、GitHub、Drive、本地文件、部署环境和 AI 对话都存在副本时，哪个才是当前权威？

核心规则包括：

- 不因为方便就创建平行 Current
- Candidate 不得 self-promote
- 实验状态不能直接冒充正式能力
- Authority 变化必须经过适用的 decision / receipt / readback
- 历史信息进入 provenance / legacy / archive，而不是静默删除
- 同步副本不自动获得共同 Source Authority

详细规则：

[Anti-Pollution Protocol](00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md)

---

# 20｜NO COMPRESSION / NO LOSS

复杂项目在“整理”“重构”“做得更简洁”时，很容易把有效信息一起删掉。

OLEANDER 的默认原则是：

> **NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS**

允许：

- 重排
- 拆分
- 合并展示
- 改变视觉权重
- 重新绘制
- 改变导航

但真正删除一个独立有效层级或信息对象时，应明确说明为什么删除，而不能仅以“更简洁”为理由。

这条原则也用于保护复杂设计项目中的：

- 专业逻辑
- 研究证据
- 方案差异
- 历史判断
- 未解决问题

---

# 21｜当前阶段与边界

OLEANDER 目前更准确的描述是：

> **持续研发与真实项目验证中的独立 Human–AI Co-Design 产品／系统。**

它不是一个已经证明大规模商业化的 SaaS，也不应通过 GitHub 文件数量推断用户规模、商业成熟度或生产级可靠性。

当前仓库更能证明的是：

- 产品问题定义
- 系统架构设计
- Human–AI 交互机制
- 长周期真实项目实践
- 治理与状态设计
- 验证与回归意识
- 设计与 AI 工作流整合

尚需进一步通过外部用户验证的内容包括：

- 更广泛用户群的可用性
- 跨用户泛化
- 稳定的产品指标基线
- 商业模式与规模化运营
- 多人协作体验

这也是后续产品化真正需要验证的部分。

---

# 22｜如果把它当成产品经理 Case Study

可以用下面这条主线阅读：

~~~text
Problem
→ User / Scenario
→ Product Hypothesis
→ MVP
→ Product Objects
→ Agentic Interaction
→ Workflow
→ Real Project
→ Eval / Failure
→ Iteration
→ Governance
~~~

这比从文件树逐层阅读更接近 OLEANDER 的产品逻辑。

---

# 23｜最短阅读路径

**只想快速判断我在做什么：**  
README → 核心产品假设 → Human–AI 协作闭环 → Selected Works

**想判断我的产品经理能力：**  
项目背景 → MVP → Human-in-the-loop → 产品对象 → Evals → 当前阶段与边界

**想判断系统有没有真实验证：**  
05-cases → evals → tests → 06-practice

**想判断我的设计能力：**  
05-cases → 04-spatial → 03-ip → 02-culture → 06-practice

**想研究 OLEANDER 系统本身：**  
00-governance/README → runtime → canonical policies → evals

---

## About

**Jiaosong / 刘旋**

Product Design background · AI Product · Human–AI Collaboration · Complex Professional Workflows

[GitHub Profile](https://github.com/Jiaosong)
