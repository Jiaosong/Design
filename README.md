# OLEANDER／织作

**AI Product · Human–AI Collaboration · Product & Design Systems**

这里既是我的个人设计作品与研究成果公开档案，也是 **OLEANDER Human–AI Co-Design System** 的主要公开项目仓库。

我的正式背景是 **产品设计**，实践覆盖交互、视觉、CMF、三维／空间设计与 AI 协同工作流。我目前重点关注一个产品问题：

> **如何把“能力很强但不稳定的 AI 模型”，设计成一个用户可以长期、连续、可控地协作的产品。**

GitHub 在这个项目中的作用不是单纯存代码，而是承担三件事：

1. **产品证据**：记录 OLEANDER 的产品机制、交互规则、验证与迭代；
2. **设计证据**：公开作品、研究、原型、视觉／空间／CMF 等设计成果；
3. **可追溯证据**：保留来源、状态、测试、失败、版本与治理边界，避免把“存在”误写成“已经验证”。

仓库不是内部任务管理首页。治理版本、迁移状态、Legacy 映射和底层机器记录存在于仓库中，但不作为外部访客的第一阅读层。

---

# 先看这里｜3 分钟理解这个仓库

如果你第一次进入，不需要从 00-governance 开始阅读。

建议先理解下面四件事：

### 1. 我在做什么

我在探索 **AI Product + Human–AI Collaboration + Professional Workflow**。

重点不是“让 AI 生成更多内容”，而是解决长期专业项目中的：

- 上下文连续性
- 正式项目状态
- AI 自主性与用户控制
- 决策权
- 知识与证据可信度
- 多方案探索
- 执行后的验证
- 长期系统学习

### 2. OLEANDER 是什么

OLEANDER 是一个持续演进的 **Human–AI Co-Design System**。

它将传统：

**Prompt → Output**

重新组织为：

**Understand → Explore → Compare → Decide → Execute → Readback → Update State → Continue**

### 3. 仓库里有什么

这里同时包含：

- OLEANDER 产品与治理体系
- AI 产品机制与测试
- 可复用设计工作流／Skills
- 真实设计案例
- 设计研究与练习
- 视觉、品牌、CMF、空间、建筑与交互方向成果
- 评估、回归与失败证据

### 4. 如何判断内容成熟度

本仓库不会把“文件存在”“AI 生成”“原型完成”自动等同于“已经验证”。

你会看到 **RESEARCH、CONCEPT、PROTOTYPED、VISUALIZED、TEST PLANNED、NOT RUN、VALIDATION PENDING、PASS** 等状态。它们用于明确区分：

**研究 → 判断 → 原型 → 测试计划 → 实际验证 → 当前有效结果**

---

# 推荐阅读路线

不同读者不需要按照同一个顺序阅读。

## A｜如果你是招聘者 / 产品经理面试官

建议阅读顺序：

**README → OLEANDER 产品问题 → Selected Works → evals → 00-governance**

重点看：

1. 我如何定义问题；
2. 如何把模糊 AI 问题拆成产品机制；
3. 如何处理 Agent Autonomy × Human Control；
4. 如何通过真实项目与测试验证产品；
5. 如何从失败反推下一轮产品迭代。

推荐入口：

- 本 README：产品定位与整体结构
- [05-cases/](05-cases/)：真实项目如何承载产品验证
- [evals/](evals/)：产品机制如何被测试
- [00-governance/README.md](00-governance/README.md)：需要进一步理解系统架构时再进入

**不建议第一步直接阅读大量治理协议。**

这些文件是系统可靠性的底层证据，但不是理解产品价值的最短路径。

---

## B｜如果你是 AI / Agent 产品方向读者

建议阅读：

**产品问题 → evals → governance → skills → cases**

重点关注：

- Project State
- Context Recovery
- Human Decision Rights
- Agent Autonomy
- Readback
- Provenance
- Cross-context continuity
- Failure handling
- Runtime / Trust / Change Control

推荐入口：

- [evals/README.md](evals/README.md)
- [evals/runtime/](evals/runtime/)
- [evals/trust/](evals/trust/)
- [evals/cross-context/](evals/cross-context/)
- [evals/failure/](evals/failure/)
- [evals/change-control/](evals/change-control/)
- [00-governance/](00-governance/)

---

## C｜如果你是设计师 / 建筑 / 空间 / 视觉方向读者

建议阅读：

**Selected Works → 04-spatial → 02-culture / 03-ip → 06-practice**

重点看：

- 设计问题如何被定义
- 方案如何发散、比较和收敛
- 设计证据与开放问题如何区分
- 图纸、空间、视觉、CMF、文化研究如何进入同一工作流
- AI 如何辅助设计，而不是替代设计判断

推荐入口：

- [05-cases/](05-cases/)
- [04-spatial/](04-spatial/)
- [03-ip/](03-ip/)
- [02-culture/](02-culture/)
- [06-practice/](06-practice/)

---

## D｜如果你想看 OLEANDER 的系统与治理

建议阅读：

**00-governance README → 核心协议 → 专业流程 → 审计 / runtime**

00-governance 是 OLEANDER 的“系统控制层”。

这里不是普通文档归档，而是用于约束：

- Current / Candidate / Evidence / Provenance
- 项目状态与权威来源
- Human / AI 决策权
- 设计质量与流程通过的区别
- 变更、晋级、readback
- No Compression / No Loss
- 多专业工作流
- 成品审查
- 系统演进

推荐从：

- [00-governance/README.md](00-governance/README.md)
- [OLEANDER Anti-Pollution Protocol](00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md)
- [Post-Generation Review Gate](00-governance/post-generation-review-gate.md)
- [Architecture Design Development Process](00-governance/architecture-design-development-process-v1.0.md)

开始，而不是随机打开单个机器记录。

---

## E｜如果你想看“系统是不是只有文档，没有验证”

直接进入：

- [evals/](evals/)
- [tests/](tests/)
- [06-practice/](06-practice/)
- [05-cases/](05-cases/)

evals 当前按不同风险与验证目的拆分，包括：

- change-control
- cross-context
- failure
- golden
- provenance
- retrieval
- runtime
- trust

这些目录用于验证产品机制与系统行为，而不是做展示型 Demo。

---

# OLEANDER｜Human–AI Co-Design System

**角色：独立产品负责人 / Product Designer｜0→1 产品设计与验证**

OLEANDER 是我持续设计与验证的一套 Human–AI 协作系统。它不把 AI 仅作为一次性生成工具，而是研究如何让 AI 在复杂、长期、跨会话的专业项目中成为一个**持续协作者**。

## 项目起点

长期使用通用 AI 做复杂项目时，我反复遇到：

- 对话结束后项目上下文断裂；
- “聊天记忆”与正式项目状态混在一起；
- 文件、知识、证据和决策分散；
- AI 太被动，需要用户不断告诉它下一步；
- AI 太主动，又容易越权；
- 多方案经常只是同一方案的表面变化；
- AI 执行结束后容易默认“任务已经完成”；
- 一次项目的经验难以沉淀成下一次可复用能力。

因此，我将问题从：

> “模型回答得好不好？”

重新定义为：

> **项目连续性、状态、权限、知识可信度、执行验证与长期协作的产品问题。**

---

# 核心产品问题

## 1｜Project Continuity

AI 如何在新会话中正确恢复项目当前状态，而不是依赖用户重新讲述全部历史？

## 2｜Autonomy × Control

什么可以由 AI 自主探索、建议或执行；什么必须由人类确认；什么必须保留为 Human-only Decision？

## 3｜Project State

如何把正式项目状态从聊天历史中独立出来，并保证当前性、版本与可追溯性？

## 4｜Knowledge & Evidence

如何区分事实、来源、推断、设计判断和开放问题，避免未经验证的信息被当成既定事实？

## 5｜Design Exploration

如何让 AI 生成实质差异的候选方案，而不是多个表面变体，并形成探索—比较—批评—筛选—深化的设计过程？

## 6｜Validation

如何通过 Readback、Consistency Check 与 Regression Testing 验证执行结果，而不是假设“做了 = 做对了”？

## 7｜System Evolution

如何通过复用、组合、参数化、Benchmark、重构和证据积累提升系统，而不是每遇到一个问题就新增一个 Skill？

---

# Human–AI 协作闭环

~~~text
Understand Current Project
        ↓
Recover State / Knowledge / Evidence
        ↓
Explore Alternatives
        ↓
Compare / Critique / Filter
        ↓
Human Decision when needed
        ↓
Execute
        ↓
Readback / Validate
        ↓
Update Project State
        ↓
Continue
~~~

OLEANDER 的目标不是“最大化自动化”，而是：

> **Trustworthy Automation + Meaningful Human Control**

另一个核心原则是：

> **Conversation is an interface. Project State is the product reality.**

---

# 产品经理能力映射

## 复杂问题抽象

从“AI 长期不好用”继续拆解为项目连续性、状态管理、决策权、知识可信度、执行风险等可设计问题。

## 0→1 产品定义

从真实工作流出发定义用户问题、核心产品对象、MVP、交互规则和验证路径，而不是直接堆功能。

## Agentic UX / Human-in-the-loop

根据任务风险、可逆性、影响范围和决策权，区分 AI 的自主探索、建议、可逆执行、人工确认和禁止自动执行。

## 复杂工作流产品架构

将 Project State、Knowledge、Decision、Task、Artifact、Validation 等对象组织成连续系统。

## 验证驱动迭代

通过真实项目、异常路径、Fixtures、Readback 与回归测试持续暴露问题并修正产品机制。

---

# 设计背景如何进入产品工作

我的正式背景是**产品设计**，设计实践横跨产品、交互、CMF、视觉、三维和空间／建筑研究。

这些能力并不是与产品经理分开的附加技能，而是我处理复杂产品问题的方法来源。

设计训练让我长期处理：

- 模糊和不完整需求
- 用户行为与体验
- 多重约束之间的取舍
- 功能与空间关系
- 多方案生成与比较
- 信息层级和视觉表达
- 材料、工艺和实现约束
- 从概念到落地的连续迭代

我将同样的方法迁移到数字产品：

> **User Need + System Constraint + Interaction + Implementation + Validation**

---

# Selected Works｜案例入口

## [C01｜一脉广渡](05-cases/c01-yimai-guangdu/)

以 **Culture + Spatial** 为主要研究维度的个人设计研究与提案。

当前状态：**RESEARCH + PROPOSAL / EVIDENCE REVIEW**

适合观察：

- 文化研究如何进入设计判断
- 证据边界如何被保留
- 空间、叙事、视觉如何形成统一系统
- AI 如何参与长期复杂设计而不是只生成效果图

## [C02｜忘也 Daylily](05-cases/c02-daylily/)

品牌／IP、空间与体验关系的独立作品集项目。

当前状态：**INDEPENDENT PORTFOLIO / PROTOTYPED / TEST PLANNED / NOT RUN**

这里明确区分“原型已经存在”和“计划中的真实测试尚未执行”。

## [C03｜The Light Collection](05-cases/c03-the-light-collection/)

以 Reno 产品语境为背景的独立 CMF 概念提案。

当前状态：**PORTFOLIO CONCEPT / VISUALIZED / SAMPLE TEST PENDING**

这是个人概念研究，不代表 OPPO 委托、采用、量产或背书。

## [C04｜Qingjiang Stone Book](05-cases/c04-qingjiang-stone-book/)

包含更复杂的数字呈现、三维／网页资产与持续重构过程，可作为观察 OLEANDER 如何处理设计资产、实现与验证之间关系的案例入口。

---

# 仓库地图｜Repository Map

## [00-governance/](00-governance/)

**OLEANDER 的治理与系统控制层。**

主要负责：

- 系统架构
- 项目状态
- Current / Candidate / Evidence / Provenance
- 权威来源与晋级
- Human / AI 决策边界
- 专业流程
- 设计质量
- 变更控制
- 审计
- 成品复核
- 系统演进

这里是理解“为什么系统不会把一次 AI 输出自动当成事实或正式结果”的关键目录。

---

## [01-business/](01-business/)

**商业与项目语境。**

用于保存与设计项目有关的商业背景、市场、产品语境及项目级约束。它回答的是：

> 为什么做、为谁做、处于什么商业或项目环境中。

---

## [02-culture/](02-culture/)

**文化、历史、理论与解释框架研究。**

用于支持文化类、地方性、叙事性设计项目，避免文化内容只停留在装饰性引用。

---

## [03-ip/](03-ip/)

**品牌、身份、视觉语言与 IP 研究。**

覆盖身份系统、视觉语言、品牌表达等方向，并与实际案例互相引用。

---

## [04-spatial/](04-spatial/)

**空间、建筑、构造与环境设计研究。**

包含空间／建筑方向的方法、研究和专业能力扩展。对于希望理解 OLEANDER 如何进入建筑和空间工作流的读者，这是重要入口。

---

## [05-cases/](05-cases/)

**真实案例与作品主目录。**

当前包括：

- C01 — 一脉广渡
- C02 — 忘也 Daylily
- C03 — The Light Collection
- C04 — Qingjiang Stone Book

这里不是简单作品图片集合，而是用真实项目承载：

- 研究
- 设计决策
- 版本演进
- 原型
- 证据
- 测试
- OLEANDER 工作流验证

---

## [06-practice/](06-practice/)

**练习、实验、训练与小尺度验证。**

这里用于放置尚不需要进入大型项目，但值得被独立验证的设计练习、交互实验、训练任务和方法测试。

适合观察系统如何在低成本场景中验证新机制。

---

## [evals/](evals/)

**OLEANDER 的评估与回归验证层。**

当前包含：

- **change-control** — 变更控制
- **cross-context** — 跨上下文连续性
- **failure** — 失败与异常路径
- **golden** — 基准／Golden Cases
- **provenance** — 来源与证据链
- **retrieval** — 检索与知识调用
- **runtime** — 运行行为
- **trust** — 信任、权限与可信执行

如果你想判断 OLEANDER 是否只是一套概念框架，应优先查看这里。

---

## [oleander-skills/](oleander-skills/)

**可复用能力与工作流模块。**

目前可见能力方向包括：

- 3D pipeline
- data visualization
- delivery QC
- design process
- image art direction
- motion
- research
- story & board
- visual design
- web UI

OLEANDER 当前的方向不是无限新增 Skill，而是优先：

**Reuse → Compose → Parameterize → Benchmark → Refactor**

只有在重复证据证明现有能力无法合理表达某种稳定需求时，才值得形成新的可复用能力。

---

## [tests/](tests/)

**自动化或结构化测试。**

用于检查系统实现与已有行为是否发生回归。它与 evals 不完全相同：

- tests 更接近实现层和可重复检查；
- evals 更关注产品／系统行为是否满足预期。

---

## [tools/](tools/)

**支持 OLEANDER 工作流的工具与脚本。**

它们服务于设计、验证、数据处理和自动化，不等于产品本身。

---

## [website/](website/)

**数字呈现与 Web 输出。**

用于承载公开网页、项目展示或相关数字体验实现。

---

## [90-shared/](90-shared/)

**跨项目共享资产与公共组件。**

只有真正具有跨项目复用价值的内容才应进入这里。

---

## [99-archive/](99-archive/)

**历史、旧版本与归档。**

归档不代表内容“没用”，而是表示它不再是当前权威版本。

OLEANDER 强调：

> **No Compression / No Loss**

历史价值应被保存，但不能继续冒充 Current。

---

# 如何理解状态与证据

这个仓库里最重要的阅读规则之一是：

> **Artifact existence ≠ Design quality**  
> **Process PASS ≠ Design KEEP**

也就是说：

- 文件生成了，不代表设计好；
- 自动化测试通过，不代表专业设计判断通过；
- 有图、有网页、有模型，不代表事实已经验证；
- AI 总结过，不代表它成为正式知识；
- Candidate 存在，不代表它已经晋级为 Current。

因此阅读时建议始终区分：

### FACT / VERIFIED

已有明确依据或验证。

### SUPPORTED

有证据支持，但证据强度或覆盖范围有限。

### INFERRED

合理推断，但不能伪装成事实。

### OPEN

尚未解决或仍需验证。

这种区分是 OLEANDER 长期协作可靠性的基础之一。

---

# Mandatory Post-Generation Review

OLEANDER／织作的设计与技术输出执行统一成品审查门槛。

生成、导出、自动 QA 或可复现运行之后，必须实际打开最终成品复核：

- 视觉质量
- 图文边界
- 比例
- 几何—标注一致性
- 构造逻辑
- 信息完整性
- 证据状态

只有完成适用的后验审查，才允许进入相应的 DONE / PASS / Candidate 状态。

Canonical rule: [post-generation-review-gate.md](00-governance/post-generation-review-gate.md)

---

# Project-wide Anti-Pollution Rule

整个 OLEANDER 项目统一执行：

**One Logical Object → One Current Authority → traceable Candidate / Evidence / Provenance children**

核心含义：

- 已有逻辑对象优先原位扩展／修复，不默认新建平行页面、数据库、Skill、workflow、框架或 Current；
- EXPERIMENTAL_UNVERIFIED / VALIDATION_PENDING 不得直接进入 Current；
- CI、文件存在、AI Summary、单次 bounded probe 不能自行晋级；
- Candidate 不得 self-promote；
- Authority 变化必须完成适用的 receipt、promotion decision 与 downstream readback；
- 清理遵循 **NO COMPRESSION / NO LOSS**；
- GitHub、Notion、Drive、Deployment、Native Master 可以存在不同表示，但同步副本不是共同 Source Authority。

Canonical policy: [OLEANDER Anti-Pollution Protocol](00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md)

Machine contract: [OLEANDER Anti-Pollution Contract](00-governance/OLEANDER_ANTI_POLLUTION_CONTRACT_CURRENT.json)

---

# 最短阅读总结

如果只想快速理解 OLEANDER：

**README**
→ 看产品问题
→ 看 Human–AI 协作闭环
→ 看 05-cases 里的真实案例
→ 看 evals 里的验证
→ 最后进入 00-governance 理解为什么系统这样设计

如果想理解我的产品经理能力：

**问题定义**
→ **MVP / 产品对象**
→ **Autonomy × Control**
→ **真实项目**
→ **验证与失败**
→ **系统迭代**

如果想理解我的设计能力：

**05-cases**
→ **04-spatial / 03-ip / 02-culture**
→ **06-practice**
→ 再回到 OLEANDER 看这些专业流程如何被组织进 Human–AI 系统。

---

## Profile

个人定位与更精简的介绍见：

**[Jiaosong GitHub Profile](https://github.com/Jiaosong)**

