# OLEANDER 设计协作系统｜Product Requirements Document v0.1

**Product:** OLEANDER Human–AI Co-Design System
**Document type:** Product Requirements Document / 产品需求文档
**Status:** `PRODUCT CANDIDATE DEFINITION / NON-AUTHORITY / NO PROMOTION`
**Date:** 2026-09-26
**Owner:** Product / Jiaosong
**Primary audience:** 产品经理、设计负责人、AI/Agent 产品、工程与设计协作方

> 本 PRD 描述“产品应该解决什么问题、用户如何使用、功能如何验收”。
> 它不是新的 OLEANDER Current、Project State、Authority、Checkpoint、Artifact Registry、Professional Process 或 Promotion owner。

---

# 0｜Executive Summary

OLEANDER 设计协作系统是一套面向**长期、复杂、专业设计项目**的 Human–AI Co-Design 产品。

它要解决的不是“如何让 AI 再生成一个更好的答案”，而是：

> **如何让一个能力强、但具有不确定性、上下文限制和执行风险的 AI，在长期项目中成为可持续、可控制、可恢复、可验证的设计协作者。**

传统 AI Chat 的基本范式是：

~~~text
Prompt → Response
~~~

OLEANDER 的目标范式是：

~~~text
Recover Project
→ Understand
→ Explore
→ Make
→ Look
→ Critique
→ Human Steer when needed
→ Develop
→ Readback
→ Update State
→ Continue
~~~

产品的核心价值不是“最大化自动化”，而是：

> **Trustworthy Automation + Meaningful Human Control**

---

# 1｜项目背景

在建筑、产品、空间、视觉、CMF、数字产品与复杂研究项目中，单次 AI 能力已经可以完成大量局部任务，但长期协作仍反复出现以下问题：

| 现象 | 用户表层感受 | 产品层问题 |
|---|---|---|
| 新会话不知道做到哪里 | 每次都要重新解释 | Project Continuity |
| AI 引用旧文件或旧方案 | 不知道哪个才是当前版本 | Project State / Authority |
| AI 太被动 | 用户变成任务调度器 | Agent Autonomy |
| AI 太主动 | 越权修改、错误推进 | Human Control |
| 多方案只是换颜色/换样式 | 没有真正探索 | Design Exploration |
| AI 说“完成了”但产物没检查 | 结果不可相信 | Readback / Validation |
| 事实、推断、设计判断混在一起 | 无法判断可信度 | Knowledge / Evidence |
| 每一步都要确认 | 协作成本高 | Human Stop Precision |
| 每次项目都重复 Prompt | 经验没有沉淀 | Reuse / Evolution |
| AI 过度解释或替用户做决定 | 用户能力与主动性下降 | Designer Agency |

因此，产品问题被重新定义为：

> **Conversation continuity 不是 Project continuity；Model memory 不是 Product state；Tool success 不是 Task success；AI recommendation 不是 Human decision。**

---

# 2｜产品愿景

## 2.1 Vision

让专业设计师可以像与一个持续协作的设计伙伴工作一样使用 AI：

- 系统知道项目当前在哪里；
- AI 可以主动推进低风险、可逆工作；
- AI 能主动探索真正不同的方案；
- 用户不需要预先指定每一个视觉、形式和执行参数；
- 到真正需要价值判断时，系统再把决定交还给人；
- 执行之后必须看到实际结果；
- 失败、拒绝、延期和旧方案都保持可追溯；
- 会话结束、插件替换或工具切换不会让项目状态消失。

## 2.2 Product Positioning

OLEANDER 不是：

- Prompt Library；
- 单一图像生成工具；
- 完全自动化设计 Agent；
- 聊天记录管理器；
- 一个新的专业设计流程替代品；
- 一个把所有领域压成统一 Stage 的系统。

OLEANDER 更接近：

> **AI Workspace for long-term professional Human–AI Co-Design**

---

# 3｜目标用户

## 3.1 Primary User

> **需要与 AI 长期协作完成复杂专业项目的设计与知识工作者。**

第一阶段重点覆盖：

- 产品设计师；
- UX / UI / Digital Product Designer；
- 建筑 / 空间 / 室内 / 景观设计者；
- 品牌 / 视觉 / CMF 设计者；
- 跨专业设计负责人；
- 使用 AI 进行复杂研究和方案开发的知识工作者。

## 3.2 用户共同特征

- 项目持续数天、数周或数月；
- 不是一次 Prompt 可以完成；
- 同时存在多个版本、文件和对象；
- 用户本身拥有专业判断；
- AI 可承担大量分析和执行，但不能拥有全部决策权；
- 需要在“快速探索”与“可信执行”之间平衡；
- 输出常包含图、模型、页面、代码、数据等真实 artifact。

## 3.3 Secondary Users

- Client / Stakeholder
- Specialist
- Independent Reviewer
- Project Authority
- Promotion / Release Authority

这些角色可以参与同一项目，但**最新发言者不自动拥有最高决策权**。

---

# 4｜Jobs To Be Done

## JTBD-01｜继续项目

当我重新进入一个长期项目时，
我希望系统能够恢复当前真实进度、版本和下一步，
这样我不需要重新解释全部历史。

## JTBD-02｜探索可能性

当我只知道目标、问题或不满意的感觉时，
我希望 AI 主动提出真正不同的设计机制和候选，
而不是要求我先把所有细节都指定清楚。

## JTBD-03｜比较并做决定

当多个方案都可能成立时，
我希望看到可比较的真实 artifact、关键 trade-off 和失败风险，
这样我可以在有信息的情况下做决定。

## JTBD-04｜放心让 AI 推进

当任务是低风险、可撤销且已有授权时，
我希望 AI 自动继续完成，
而不是每一步都停下来问我。

## JTBD-05｜保留最终控制

当任务涉及价值取舍、专业责任、发布、不可逆操作或权限升级时，
我希望系统明确停下来，
而不是替我做决定。

## JTBD-06｜知道“做对没有”

当 AI 修改了文件、模型、页面或系统时，
我希望它实际打开并检查结果，
而不是把工具成功等同于设计成功。

## JTBD-07｜从项目中成长

当我比较和选择设计方案时，
我希望系统适度解释一个真正重要的区别，
帮助我提高判断能力，但不把产品变成教学软件。

---

# 5｜核心用户痛点

## P1｜Context Fragmentation

项目知识存在于不同对话、文件、版本、工具和平台中。

## P2｜State Ambiguity

用户无法快速判断 Current、Candidate、旧版本和展示副本。

## P3｜Over-prompting

用户需要逐步告诉 AI 做什么，AI 实际退化成自然语言遥控器。

## P4｜Over-autonomy

AI 把“继续”理解为“替用户决定”，或把建议直接变成正式项目状态。

## P5｜Premature Convergence

AI 过早围绕用户第一个想法优化，缺少真正发散。

## P6｜False Completion

生成、工具调用、CI、导出或文件存在被错误解释为任务完成。

## P7｜Decision Ambiguity

“这个”“保留那个”“不要 A 结合 B”这类自然语言在复杂上下文中容易绑定错误对象。

## P8｜Governance Overload

为了保证严谨性，如果把所有内部治理结构暴露给用户，会造成高认知负担。

---

# 6｜产品目标

## G1｜连续

用户进入新会话后，可以恢复到可信的项目 frontier。

## G2｜主动

AI 可以在授权范围内自主完成探索、分析、可逆执行和明显缺陷修复。

## G3｜可控

关键价值决策、权限升级、不可逆操作和发布不会被 AI 静默执行。

## G4｜可比较

AI 生成的是 materially distinct alternatives，而不是 cosmetic variants。

## G5｜可验证

材料变更后有 actual readback，Human-steered second round 有真实第二轮 artifact 与 readback。

## G6｜可恢复

会话、插件或界面可以被替换，但项目状态、checkpoint、native artifact 和 authority 不丢失。

## G7｜低认知负担

内部 governance 默认保持安静，只有当它影响可做、可写、可发布或可晋级时才显性出现。

---

# 7｜Non-goals

当前产品不以以下目标作为 MVP：

- 完全无人设计；
- AI 替代专业设计师最终判断；
- 自动获得 Design KEEP；
- 自动进行 Promotion；
- 用一个 universal CoDesign Stage 替代建筑、HCD、产品等专业流程；
- 建立用户永久人格／审美／能力评分；
- 让每个新项目都产生一个新 Skill；
- 把所有专业工具重做进 OLEANDER；
- 在缺失现场／工程／专业证据时伪造专业 PASS。

---

# 8｜产品原则

1. **Conversation ≠ Project State**
2. **Artifact existence ≠ Design quality**
3. **Process PASS ≠ Design KEEP**
4. **Machine PASS ≠ Professional PASS**
5. **Proposal before preference questionnaire**
6. **Comparable artifacts before consequential choice**
7. **Auto-advance reversible work; stop at real Human boundaries**
8. **Human feedback is not automatically a durable preference**
9. **No loss / no silent compression**
10. **Domain authenticity over universal workflow**

---

# 9｜MVP 定义

OLEANDER 的第一性 MVP 只验证一件事：

> **AI 能否恢复一个长期项目的正确 frontier，在不越权的情况下继续工作，并让 Human steer 真正作用到下一轮可检查 artifact。**

## 9.1 MVP Core

~~~text
Context Recovery
+ Decision Object
+ Material Exploration
+ Editable / Native Artifact
+ Human Steer
+ Mutation Guard
+ Readback
+ Continuation
~~~

## 9.2 MVP 必须具备

- 恢复 Current / checkpoint / artifact frontier；
- 区分继续工作与设计 steering；
- 生成至少 2 个 materially distinct 方案（适用时含 baseline / OFF）；
- 提供可编辑或真实可运行 artifact；
- 对 artifact 做实际 readback；
- Human action 可以 SELECT / MODIFY / MIX / REJECT / REOPEN / DEFER；
- consequential steer 必须绑定明确对象；
- 可逆工作可继续推进；
- authority-sensitive / irreversible 操作停在真实 Human boundary；
- 第二轮必须重新生成／修改并重新 readback；
- 会话结束后不产生独立 plugin-owned project truth。

---

# 10｜核心用户旅程

## Journey A｜从零开始一个设计问题

~~~text
User states outcome / problem / discomfort
→ System identifies decision object + key unknown
→ AI explores materially distinct mechanisms
→ AI makes comparable artifacts
→ System readbacks artifacts
→ Human steers
→ AI develops selected/mixed/modified branch
→ Readback
→ Continue / route review / save
~~~

## Journey B｜继续长期项目

~~~text
User says '继续'
→ Resolve project/task/object key
→ Recover Current Project / Control Card / Execution Receipt
→ Recover actual native artifact + readback
→ Identify next allowed reversible action
→ Continue
~~~

用户不应该先回答“你上次做到哪里”。

## Journey C｜用户不满意但说不清

~~~text
'这个不对 / 太像展馆 / 太重'
→ classify as FEEDBACK_SIGNAL
→ generate causal hypotheses
→ produce materially different repair directions
→ show artifacts
→ ask for steer only after difference is visible
~~~

系统不能把一次“不喜欢”写成永久审美偏好。

## Journey D｜复杂决策

~~~text
'不要 A，保留 B，结合 C'
→ REJECT A
→ MIX B + C
→ preserve all lineage
→ bind exact revisions
→ create second-round delta
→ readback
~~~

## Journey E｜用户暂缓一个决策

~~~text
DEFER current decision
→ dependent mutations HOLD
→ unrelated reversible work continues
~~~

DEFER 不应默认冻结整个项目。

---

# 11｜Interaction Model

Session Kernel 不把一条自然语言输入压成一个 intent，而是解析四个独立轴：

| Axis | 值 | 回答的问题 |
|---|---|---|
| Work Intent | START / RESUME / RECOVER / EXPLORE / WILDCARD / REVIEW / REFRAME / SAVE_ROUTE / EXPLAIN / SHOW_WORK | 用户想完成什么工作？ |
| Mutation Directive | NORMAL / READ_ONLY / AUTO_ADVANCE_REVERSIBLE | 可以改变什么？ |
| Support Mode | AUTO / COMPACT / EXPLAIN / OFF | 解释多少？ |
| Human Action Level | NONE / FEEDBACK_SIGNAL / ITERATION_STEER / DESIGN_DECISION / DESIGN_KEEP / PROMOTION_DECISION | 用户的这句话具有什么决策级别？ |

四个轴互不自动推导。

例如：

- “继续检查，不要改” = `RESUME + READ_ONLY`；
- “继续并做完，真正需要我决定时再问” = `RESUME + AUTO_ADVANCE_REVERSIBLE`；
- “这个不对” = `FEEDBACK_SIGNAL`；
- “选 B” = `ITERATION_STEER / SELECT B`；
- “DESIGN KEEP B” = route to Design Review Authority，不等于 Session Kernel 自己 KEEP；
- “Promote to Current” = route to Promotion Authority，不由 Session Kernel 执行。

---

# 12｜Human Steering Model

## 12.1 Iteration Actions

- SELECT
- MODIFY
- MIX
- REJECT
- REOPEN
- DEFER

## 12.2 Referent Binding

任何 consequential steer 必须解析到：

~~~text
REF
+ KIND
+ REVISION
+ LINEAGE_REF
~~~

必要时还要绑定 `decision_object_ref`。

### Acceptance

- “选 B”且当前唯一 B 可解析 → 可进入 steer；
- “就这个”且只有一个 active object → 可解析；
- “就这个”且有多个 active object → 只问一个最小澄清问题；
- `MIX` 少于两个 parent → 不执行；
- `DEFER` 不存在 pending decision → 不执行；
- Generic “继续” → 不得转换成任何 steer。

---

# 13｜Human Stop Policy

产品不能因为“AI 做完一个工具调用”就停止。

只在以下情况停止或路由：

1. consequential steer 的 referent 不明确；
2. 已有可比较 artifact，且出现 AI 无权替代的人类价值判断；
3. scope / authority 升级；
4. 下一步是不可逆或发布行为；
5. specialist / independent review 必须介入；
6. multi-human decision rights 冲突；
7. 没有 truthful editable/native substitute 可以回答关键未知；
8. 用户明确要求停止；
9. 用户请求的 scope 已完成。

---

# 14｜Core Features

## F01｜Project Resume & Recovery

系统恢复：

~~~text
explicit project/task/object key
→ Current Project / Task
→ Control Card
→ active Execution Receipt / checkpoint
→ actual native artifact + readback
~~~

Chat memory 不能成为 authority。

## F02｜Design Question Framing

把当前工作压缩到：

- decision object；
- current actor / user；
- target outcome；
- guardrails；
- key unknown；
- what is genuinely open。

## F03｜Material Option Exploration

生成真正不同的 mechanism family，而不是样式变体。

每个 option 至少包含：

- mechanism signature；
- parent refs；
- artifact refs；
- preserved invariants；
- strongest benefit；
- strongest failure risk；
- sensitive unknowns；
- branch status。

## F04｜Comparable Artifact Making

优先制作最小但忠实、可编辑或可运行的 artifact。

可以是：

- SVG；
- HTML/CSS/JS；
- CAD / drawing；
- 3D model；
- code；
- data / visualization；
- physical test carrier；
- 其他 owner-native output。

## F05｜Look / Readback

每次 material making 后必须检查实际 artifact。

Readback 至少回答：

- 实际生成了什么；
- 关键设计差异是否真的存在；
- 有没有明显 defect；
- 是否保持 locked invariant；
- 哪些结论仍不能证明。

## F06｜Human Steering

让 Human 在 consequential choice point 进行 SELECT / MODIFY / MIX / REJECT / REOPEN / DEFER。

## F07｜Second-round Delta

Human steer 不能停在文本确认。

必须：

~~~text
Human steer
→ permission / decision-rights proof
→ bound revision
→ actual artifact delta
→ actual readback
~~~

## F08｜Auto-advance

可逆、已授权的工作继续自动推进。

## F09｜Mutation Guard

项目写入前重新读取 owner-native Current carrier，避免 stale write。

## F10｜Multi-human Decision Rights

Designer、Client、Specialist、Reviewer、Authority 的权限作用域分开。

## F11｜Designer Development

默认最多每个 material round 一次：

~~~text
ONE KEY DISTINCTION
→ WHY IT CHANGES THIS DESIGN
→ AT MOST ONE TRANSFER QUESTION
~~~

## F12｜Cross-domain Adapter

Session Kernel 可以跨建筑、HCD、产品等复用交互逻辑，但专业过程保持 domain-native。

## F13｜Plugin-off Survival

移除或替换插件后：

- Project State 仍存在；
- Checkpoint 仍存在；
- Native Artifact 仍存在；
- Authority 仍存在。

## F14｜Separated Closure

结束时分开报告：

~~~text
SESSION_RESULT
/ DESIGN_CANDIDATE
/ PROFESSIONAL_STATE
/ REVIEW_STATE
/ PERSISTENCE_STATE
/ PROMOTION_STATE
~~~

不能压成一个 PASS。

---

# 15｜Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-01 | 新会话可恢复 verified frontier | P0 | 不依赖 chat summary 作为 authority；能定位 Current/checkpoint/native artifact |
| FR-02 | continuation 与 steering 分离 | P0 | “继续”不会变成 SELECT/DEFER/MIX |
| FR-03 | READ_ONLY 独立生效 | P0 | RESUME + READ_ONLY 时零 mutation |
| FR-04 | 可生成 materially distinct options | P0 | 至少两种不同 mechanism signature；cosmetic duplicate 不计数 |
| FR-05 | 支持 baseline/no-change/OFF | P1 | 因果上 relevant 时作为真实 branch |
| FR-06 | consequential steer 必须绑定 revisioned referent | P0 | unresolved / ambiguous fail closed |
| FR-07 | compound Human actions 不折叠 | P0 | `REJECT A + MIX B,C` 保留为两个 acts |
| FR-08 | MIX 保留 parent lineage | P0 | second-round option 可追溯所有 parent |
| FR-09 | REJECT / DEFER 不删除 branch | P0 | branch 进入 preserved lineage |
| FR-10 | 每次 material making 必须 actual readback | P0 | 没有 readback 不允许声称 implemented/validated |
| FR-11 | Human-steered second round 必须生成真实 delta | P0 | 有新 artifact revision + same-revision/hash readback |
| FR-12 | stale checkpoint mutation 被阻止 | P0 | stale write HOLD，先 revalidate Current |
| FR-13 | reversible authorized work 可自动推进 | P0 | 不在每个 tool call 后停顿 |
| FR-14 | irreversible / publish 操作要求授权 | P0 | 无授权不执行 |
| FR-15 | 多 Human 权限冲突局部 HOLD | P1 | 只阻塞 affected effect，不冻结无关工作 |
| FR-16 | support mode 可调整 | P1 | AUTO / COMPACT / EXPLAIN / OFF 生效且不改变 authority |
| FR-17 | 不持久化 taste/ability profile | P0 | session fade 不转成 durable competence claim |
| FR-18 | domain adapter 不制造 universal stage | P0 | OPEN domain 不允许 professional PASS |
| FR-19 | plugin-off continuity | P1 | 卸载插件后仍能从 owner-native carriers resume |
| FR-20 | closure dimensions 分开报告 | P0 | 不出现“一切 PASS”式合并结论 |

---

# 16｜Permission / Autonomy Matrix

| 行为 | 默认 AI 行为 | Human 要求 |
|---|---|---|
| 信息检索 / 整理 | 自动 | 无 |
| 问题重构 / 假设 | 自动 | 无 |
| 方案发散 | 自动 | 无 |
| 低风险本地原型 | 自动 | 只需符合已有 guard |
| 可逆项目修改 | 条件自动 | 已有 owner rule 允许 |
| 关键设计选择 | 停止并呈现比较 | Human steer |
| 权限升级 | 停止 | 明确授权 |
| 外部不可逆操作 | 停止 | 明确授权 |
| 发布 / 对外提交 | 停止 | 明确授权 |
| Design KEEP | 路由 | 现有 Design Review Authority |
| Promotion | 路由 | 现有 Promotion Authority |

---

# 17｜Product Object Model

PRD 层只引用既有产品对象，不新建 authority family。

| Object | Product role | Owner principle |
|---|---|---|
| Project | 长期工作容器 | Existing Project Axis / Current |
| Decision Object | 当前需要做出选择的对象 | Existing project/owner rules |
| Option Branch | 可比较候选及 lineage | Session projection + artifact owner |
| Artifact | 可编辑/可运行设计载体 | Native owner |
| Readback | 对实际 artifact 的检查证据 | Existing readback owner |
| Human Action | 用户反馈或 steering | Session Kernel classify; authority routes separately |
| Knowledge / Evidence | 支持判断的来源与内容 | Existing Knowledge / Source Authority |
| Checkpoint | 可恢复执行 frontier | Existing Execution Receipt / Control Card |

---

# 18｜Information Architecture

用户第一层应该看到的是：

~~~text
Current Goal
Current Design Object
What AI is doing
Comparable Alternatives
What changed
What needs Human decision
Next action
~~~

默认不暴露：

- R-A…R-K；
- 内部 receipt schema；
- promotion internals；
- 所有 governance terminology。

只有当这些内部规则改变“现在能不能改、能不能写、能不能发布、能不能晋级”时才 progressive disclose。

---

# 19｜Error / Edge Cases

## EC-01｜“继续”被误判为选择

Expected: RESUME only。

## EC-02｜“就这个”同时指向两个对象

Expected: ask one minimum referent clarification。

## EC-03｜用户说“不喜欢”

Expected: feedback signal + causal hypotheses；不创建永久 preference。

## EC-04｜本地 checkpoint 比 Current 旧

Expected: stale mutation blocked；revalidate。

## EC-05｜只有 PPT 比 native master 新

Expected: presentation derivative 不因 recency 取代 native authority。

## EC-06｜专业工具不可用

Expected: 可做 truthful bounded editable prototype；native completion claim HOLD。

## EC-07｜Client 要求违反 Specialist boundary

Expected: affected effect HOLD；latest human message 不覆盖专业 authority。

## EC-08｜AI 已生成文件但无法实际打开检查

Expected: task 不可宣称 validated / done。

---

# 20｜Metrics

> 以下为**产品指标定义**，不是当前已取得的商业结果。

## 20.1 North Star Metric

### Successful Continuation Rate

定义：

> 用户重新进入项目后，系统无需用户重新解释大量历史，即可恢复正确 frontier 并继续正确工作。

建议计算：

~~~text
Successful Continuations
/ Eligible Project Re-entry Sessions
~~~

## 20.2 Primary Metrics

### Context Recovery Success Rate

恢复的 Current / object / revision / next action 是否正确。

### Human Correction Rate

用户需要纠正系统对项目状态、对象或意图理解的频率。

### Unauthorized Action Rate

未经允许发生 authority-sensitive / irreversible mutation 的比例。

产品目标：**0**。

### False Steering Rate

Generic continuation / feedback 被错误解释为 design steer 的比例。

### Readback Completion Rate

Material making 后完成 actual readback 的比例。

### Human Steering Implementation Fidelity

Human steer 与第二轮 artifact 的 changed variables / preserved invariants 是否一致。

### Useful Autonomy Rate

无需 Human 干预、且最终 readback 有效的可逆工作占比。

### Repeated Context Input

用户为恢复项目而重复粘贴／解释上下文的数量或时间。

## 20.3 Design Exploration Metrics

### Material Divergence Rate

候选中具有不同 mechanism signature 的比例。

### Cosmetic Duplicate Rate

只有样式变化但机制相同的候选比例。

### Baseline Consideration Rate

适用时是否包含 baseline / no-change / OFF。

## 20.4 Guardrail Metrics

- Stale Mutation Attempt Block Rate
- Ambiguous Referent Fail-closed Rate
- Unread Artifact Completion Claim Rate
- AI-owned Design KEEP Count
- AI-owned Promotion Count

其中最后三项目标均为 **0**。

---

# 21｜Event Instrumentation

建议记录以下产品事件，用于后续真实用户验证：

| Event | 核心字段 |
|---|---|
| project_resume_started | project_ref, source_carriers |
| frontier_resolved | object_ref, revision, checkpoint |
| option_space_created | decision_object, option_count, mechanism_signatures |
| artifact_made | option_ref, artifact_ref, revision |
| readback_completed | artifact_ref, revision, verdict |
| human_feedback_received | action_level, raw_ref, support_mode |
| human_steer_bound | action, referents, decision_object |
| ambiguity_clarification_requested | referent_count, reason |
| mutation_guard_blocked | block_reason |
| second_round_completed | parent_refs, delta_ref, readback_ref |
| human_stop_triggered | stop_reason |
| session_closed | closure_dimensions |

产品分析事件不得变成新的 Project State authority。

---

# 22｜Validation Plan

## Layer 1｜Deterministic Kernel Tests

验证：

- intent / mutation / support / action-level 分离；
- referent binding；
- compound actions；
- branch lineage；
- defer dependency；
- stale mutation guard；
- human-stop computation。

## Layer 2｜Golden Real-artifact Trials

使用真实 editable artifact：

- Spatial；
- Digital / HCD；
- Physical Product。

验证：

- materially distinct options；
- artifact / readback binding；
- real comparison；
- repair；
- domain-specific outputs。

## Layer 3｜Real Human Steering

这是当前产品最关键的未闭合验证层。

需要真实用户完成：

- SELECT；
- MODIFY；
- MIX；
- REJECT；
- REOPEN；
- DEFER。

并验证：

~~~text
Human action
→ correct referent binding
→ correct mutation
→ second-round artifact
→ actual readback
~~~

## Layer 4｜Longitudinal Continuity

跨日／跨会话／插件替换测试：

- resume accuracy；
- stale-state handling；
- plugin-off survival；
- repeated-context reduction。

## Layer 5｜Multi-human Collaboration

验证 Designer / Client / Specialist / Reviewer 冲突时：

- scoped rights 是否保持；
- 无关工作是否仍可继续；
- independent review 是否保持独立。

---

# 23｜Current Candidate Evidence

当前 Human–AI Co-Design 实现仍是 Candidate，不是 Current。

已存在的候选能力包括：

- 三个 view 的单一架构投影；
- Session Kernel v0.2；
- portable plugin / Skill candidate；
- 四轴 interaction model；
- clause-scoped human actions；
- typed/revisioned referent binding；
- branch lineage；
- mutation guard；
- computed Human stop；
- domain adapters；
- spatial / digital / physical real-artifact trials；
- regression suite。

当前 committed candidate evidence 仍明确记录：

- real Human steering second round 尚未闭合；
- 部分 regressions 为 PASS_WITH_PARTIALS；
- plugin removal / reinstall 仍未完成 destructive real test；
- Physical Product domain-native professional process 仍不能被凭空制造；
- Current / Promotion 均未发生。

因此 PRD 将这些能力写成**产品需求与候选实现状态**，不写成已经商业化验证的功能。

---

# 24｜Rollout Plan

## Phase 0｜Product Definition

目标：

- PRD；
- Kernel contract；
- interaction model；
- eval criteria；
- real-case candidates。

## Phase 1｜Single-designer MVP

验证一个设计师在一个真实项目中：

- resume；
- explore；
- compare；
- steer；
- second round；
- readback；
- continue。

## Phase 2｜Cross-domain

至少验证：

- spatial / architecture；
- digital / HCD；
- physical product。

交互模型复用，但专业 process 不统一化。

## Phase 3｜Longitudinal Use

验证：

- 多会话；
- 多天；
- 多工具；
- plugin-off / replacement；
- project recovery。

## Phase 4｜Multi-human

验证：

- client / designer / specialist；
- conflicting decision rights；
- independent review。

## Phase 5｜Productization

只有核心连续性和控制问题验证后，再决定是否扩展：

- cloud files；
- integrations；
- team collaboration；
- richer project UI；
- reusable workspace templates；
- additional external tools。

---

# 25｜Prioritization

## P0｜必须先成立

- Project Resume
- Four-axis interaction
- Material option exploration
- Referent binding
- Human steer
- Mutation guard
- Readback
- Second-round verification
- Separated closure

## P1｜核心增强

- Designer development
- Multi-human decision rights
- Cross-domain adapters
- Plugin-off survival
- Longitudinal metrics

## P2｜产品化扩展

- Cloud integrations
- Team workspace
- richer project dashboards
- broader external app connectors
- cross-project reusable patterns

原则：

> **先证明协作模式成立，再增加平台功能。**

---

# 26｜Risks & Mitigations

| Risk | Product impact | Mitigation |
|---|---|---|
| AI 越权 | 用户失去信任 | Mutation Guard + scoped Human stop |
| AI 过度确认 | 产品低效 | Auto-advance reversible work |
| 错误绑定“这个” | 修改错误对象 | typed/revisioned referent binding |
| 多方案同质化 | 假发散 | mechanism signature + dedup |
| Chat memory 覆盖 Current | 状态污染 | owner-native resume precedence |
| Presentation recency 覆盖 native | 错误继续 | artifact role / authority separation |
| 文件生成即完成 | 假完成 | mandatory readback |
| Human feedback 变永久偏好 | 过拟合用户 | session-bounded support / no durable profile |
| Governance 太重 | 用户认知负担 | progressive disclosure |
| 跨专业统一流程 | 专业失真 | domain adapter / native process |
| PRD 自己变第二权威 | 系统架构污染 | PRD explicitly non-authoritative |

---

# 27｜Release Criteria for MVP

一个可对外称为“可验证 MVP”的版本至少需要：

1. continuation / steering 无 action-level collapse；
2. real project resume 成功；
3. 至少一个真实 Human steer 被正确绑定；
4. 至少一个 Human-steered second-round native/editable delta；
5. same-revision / same-content actual readback；
6. stale write 被阻止；
7. irreversible/publish 行为不会自动执行；
8. plugin/session UI 移除不破坏项目 authority；
9. 至少两个不同专业领域复用同一 interaction model；
10. domain-native process 不被统一 stage 取代；
11. closure states 分开报告；
12. 无 AI self-promotion / self-Design-KEEP。

达到这些条件也只证明 MVP 交互机制成立，不自动证明商业化、规模化或所有专业领域生产可用。

---

# 28｜Open Questions

当前仍需要产品层进一步验证的问题：

- 用户是否能理解“AI 自动推进但关键处停下”的边界？
- 哪些任务最适合默认 AUTO_ADVANCE_REVERSIBLE？
- 用户能否稳定区分 FEEDBACK_SIGNAL 与真正设计 steer？
- Comparable artifact 到底需要几种候选才不会造成选择负担？
- 哪些设计领域最适合作为首个 beachhead market？
- Designer Development 的解释强度如何不打断工作流？
- 多人协作时，decision-rights UI 应如何表达才不暴露过多 governance？
- Successful Continuation Rate 的真实基线是多少？
- 用户长期使用后，Repeated Context Input 能减少多少？
- 哪些 capability 真正值得跨项目复用，哪些只是单项目特例？

---

# 29｜PRD 与 OLEANDER Architecture 的边界

本 PRD 描述的是**产品需求视角**。

它不会：

- 新建 Project State；
- 新建 Checkpoint Database；
- 新建 Artifact Registry；
- 新建 Professional Stage family；
- 新建 Preference / Competence authority；
- 覆盖 Current Governance；
- 自动晋级 Candidate。

如果 PRD 与 owner-native Current architecture 冲突：

> **Current authority wins; PRD must be revised.**

---

# 30｜一句话产品定义

> **OLEANDER 设计协作不是让 AI 更会生成设计，而是把“理解项目、探索方案、实际制作、共同判断、可靠继续”设计成一个长期可用的 Human–AI 产品。**

---

## Related Reading

- [OLEANDER Product Docs](README.md)
- [OLEANDER 主 README](../README.md)
- [Cases](../05-cases/)
- [Evals](../evals/)
- [Governance](../00-governance/README.md)
