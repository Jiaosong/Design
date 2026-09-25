# OLEANDER Product Brief + Working Backwards FAQ v0.3.0

[← v0.3 Package](README.md)

**State:** `WORKING BACKWARDS / INTERNAL PRODUCT DEFINITION / NON-LAUNCH CLAIM`  
**Date:** 2026-09-26  
**Product Owner:** Jiaosong

> 本文是 Working Backwards 产品定义材料，不是对外发布公告，不表示产品已经商业上线。

---

# 1｜One-page Product Brief

## Customer

第一优先用户：

> **需要持续数天、数周或数月，与 AI 一起完成复杂专业设计工作的设计负责人 / 设计师。**

首批验证领域：
- Architecture / Spatial
- Digital Product / HCD
- Physical Product

后续扩展：
- Visual / Brand / CMF
- Multidisciplinary Design
- Complex knowledge work

## Customer Problem

现有 AI Chat 在长期设计项目中通常出现：

1. 新会话无法可靠恢复真正 Current；
2. 项目状态散落在聊天、文件、工具、模型记忆中；
3. AI 要么太被动，要么越权；
4. 方案多但 mechanism 差异弱；
5. 真实 editable artifact 与讨论脱节；
6. tool success 被误认为 design success；
7. 事实、推断、假设、设计判断混淆；
8. 多专业 change impact 不透明；
9. 失败后容易全局重做；
10. 用户必须承担大量 orchestration / context reconstruction。

## Customer Promise

> **重新进入项目时不用重新解释；需要探索时 AI 主动形成真正不同的方向；需要制作时进入真实 artifact；需要决定时把 trade-off 交给人；执行之后必须 read back；下一次还能准确继续。**

## Product Bet

如果 OLEANDER 能可靠维护：

```text
Design Question
+ Design Value
+ Design Relation
+ Native Artifact
+ Human Decision Boundary
+ Readback
+ Continuity
```

那么长期 Human–AI 协作的核心瓶颈会从“Prompt 写得好不好”转变为“项目能否持续推进”。

## Why Now

- 通用模型已经具备研究、生成、代码、视觉、分析和工具调用能力；
- 当前主要失败不再只是模型“不会做”，而是长期状态、权限、continuity、evaluation 与 real-artifact integration；
- Agent 化提高了自动化能力，也同步放大了错误写入、错误 referent、错误 authority 和 false completion 风险；
- 专业设计工作天然跨文件、跨工具、跨专业、跨时间，适合验证长期 Human–AI collaboration。

## Product Differentiation

OLEANDER 不与 CAD / BIM / Figma / IDE 争夺 authoring surface。

它的差异化在于：

> **把设计判断、关系、真实产物、Human authority、证据和长期 continuity 连成一个协作系统。**

## North Star

**Verified Productive Continuation Rate (VPCR)**

用户重新进入长期项目后：
1. 系统恢复正确 frontier；
2. 用户无需纠正关键状态；
3. 本次 session 至少完成一个与 frontier 一致的 material next step；
4. 如果产生 artifact change，存在有效 readback。

## Current Stage

- Product definition: advanced working baseline
- Candidate implementation: available
- Internal deterministic evaluation: substantial
- Real artifact trials: available
- External user validation: insufficient / OPEN
- Commercial validation: OPEN
- Launch readiness: HOLD

---

# 2｜Product Tenets

## T1 Customer work before system administration
用户首先看到当前设计问题和下一动作，而不是治理结构。

## T2 Project State before conversation memory
Chat memory 可以辅助，不拥有项目 truth。

## T3 Real artifact before assertion
“做了”必须能回到真实 artifact / readback。

## T4 Human authority before maximum automation
自动化最大化不是目标；可信自动化才是。

## T5 Material alternatives before cosmetic variants
方案必须改变机制、关系或 consequence。

## T6 Local recovery before global reset
失败只重开真实受影响范围。

## T7 Domain authenticity before universal workflow
跨领域共享 interaction kernel，不统一专业过程。

## T8 Progress means design resolution
任务数量、文件数量、Agent activity 不代表设计成熟度。

## T9 Evidence limits claim
缺证据降低 claim ceiling，不制造 certainty。

## T10 Reuse before Skill proliferation
优先 compose / parameterize / refactor / benchmark。

---

# 3｜Alternatives Customers Use Today

| Alternative | What it does well | Structural gap for this problem |
|---|---|---|
| General AI Chat | 快速问答、生成、分析 | Conversation ≠ durable Project State |
| Authoring tools | 真实生产、编辑、专业能力 | 不维护跨工具设计判断与 AI collaboration |
| PM / Task tools | 责任、任务、时间管理 | Task closure ≠ design resolution |
| Knowledge bases | 文档沉淀、检索 | Knowledge existence ≠ design applicability |
| Workflow automation | 重复流程、集成 | Rule execution ≠ human design judgment |
| File/version systems | 文件历史、版本 | File history ≠ decision / relation history |
| Design review meetings | 真实专业判断 | rationale / action / continuity 易散失 |

产品机会不是替换这些工具，而是连接它们之间缺失的“设计工作语义”。

---

# 4｜Working Backwards Narrative

## Customer before

一个设计师使用通用 AI 做复杂项目。第一天效果很好；几天后，新会话不知道哪个方案有效、哪个文件是 Current。设计师反复解释背景。AI 根据最后一句话错误理解“继续”，或过早选择方向。生成结果看起来完成，但没有进入 CAD / HTML / model 的真实 editable source。工具调用成功后，系统说“完成”，设计师仍必须自己重新检查。

## Customer after

设计师进入 OLEANDER，只看到：
- Current Design Question；
- Current Direction；
- Current Frontier；
- Active Artifact；
- Critical Open；
- Next High-value Action。

AI 在低风险、可逆范围继续探索和制作；当出现真正需要价值判断的 trade-off 时才停止。用户可以说“选 B”“不要 A，结合 B/C”“这个不对”。系统把这些话绑定到明确 revision / lineage。修改后重新打开真实 artifact 做 readback。第二天重新进入时，项目从 owner-native frontier 继续，而不是从聊天历史猜。

## Delight Moment

> 用户第一次在新的会话里只说“继续”，系统准确恢复项目并完成正确的下一步，而不需要用户重新解释“我们上次做到哪里”。

---

# 5｜Internal FAQ

## Q1｜为什么不是把 ChatGPT Memory 做得更强？

Memory 适合保存偏好和长期背景，但专业项目需要：
- explicit Current；
- revision identity；
- authority；
- supersession；
- artifact binding；
- decision lineage；
- verification / validation；
- rollback / reopen。

**User memory ≠ Project State。**

## Q2｜为什么不做一个全自动设计 Agent？

因为设计包含：
- value choice；
- professional responsibility；
- irreversible consequence；
- client / specialist conflict；
- incomplete evidence。

OLEANDER 追求 **Autonomy × Control**，不是 autonomous-at-all-costs。

## Q3｜为什么不直接把所有工作都放到 OLEANDER 里？

因为 CAD、BIM、Figma、IDE、simulation、manufacturing 等已经是专业 authoring system。

OLEANDER 应维护：
- semantic intent；
- relation；
- artifact identity；
- readback；
- decision / evidence；

而不是复制所有 authoring capabilities。

## Q4｜产品最重要的 MVP 假设是什么？

> **如果系统能正确恢复 Design Question / Relation / Artifact frontier，并在不越权的前提下完成 Human-steered second round，用户是否明显减少 context reconstruction 并提高长期协作信任？**

## Q5｜为什么现在不能宣称已经 Product-Market Fit？

当前证据主要来自：
- owner-driven real projects；
- internal fixtures；
- regression；
- real-artifact trials；
- independent technical/governance review。

缺少：
- 外部目标用户 cohort；
- longitudinal retention；
- willingness-to-pay；
- scaled support burden；
- commercial usage telemetry。

## Q6｜第一批外部用户应该是谁？

不是所有 AI 用户。

优先：
- 正在做真实复杂项目；
- 每周多次使用 AI；
- 项目跨多天 / 多文件；
- 有明确 professional judgment；
- 对错误 Current / unauthorized mutation 有真实成本；
- 能提供真实 artifact / workflow feedback 的设计者。

## Q7｜什么会让我们停止做当前方向？

出现以下任一结果需要 reframe：

1. 用户并不认为跨会话 continuity 是核心痛点；
2. Resume 的额外结构负担高于重新解释上下文的成本；
3. 用户更希望 AI 只作为临时 ideation tool；
4. Design Relation / Map 的维护成本过高且无法被系统自动吸收；
5. Human stop / authority 机制显著降低效率且不能通过 progressive disclosure 改善；
6. real-artifact integration 成本使产品无法形成可持续价值。

## Q8｜什么是 v1 的“成功”，不是“做完”？

至少需要：
- VPCR 达到预先冻结的 pilot threshold；
- Unauthorized Action Rate = 0；
- Human corrections 明显低于 baseline workflow；
- 至少两个 domain 证明同一 interaction model 可复用；
- Human-steered second round 可稳定形成真实 delta + readback；
- plugin/session replacement 不破坏 Current；
- pilot 用户愿意在下一项目继续使用。

阈值在外部 pilot 前冻结，当前不伪造具体百分比。

---

# 6｜Top Assumptions to Validate

| ID | Assumption | Risk if false | Validation |
|---|---|---|---|
| A-01 | Long-term continuity is a top pain | Product premise weak | interviews + baseline task |
| A-02 | Users accept explicit Current/Frontier semantics | UX burden too high | prototype test |
| A-03 | Auto-advance reversible work increases value | AI feels unsafe / annoying | controlled workflow test |
| A-04 | Material alternatives improve design decisions | More work, no better decisions | compare study |
| A-05 | Mandatory readback increases trust enough to justify latency | UX becomes slow | task completion study |
| A-06 | Relation/dependency semantics can be mostly system-maintained | Map becomes admin burden | longitudinal pilot |
| A-07 | Cross-domain kernel transfers without flattening domains | universalism failure | ≥2 domain exercise |
| A-08 | Users value project recovery enough to return | no retention signal | longitudinal cohort |

---

# 7｜Non-goals

Not v1:
- replace professional authoring tools；
- fully autonomous design；
- universal professional stage model；
- auto award Design KEEP；
- auto Promotion；
- enterprise org suite；
- generic AI marketplace；
- massive Skill catalog；
- permanent psychological / competence profiling；
- claims of professional compliance without qualified evidence。

---

# 8｜Decision Requested

当前产品团队需要继续验证的核心 decision：

> **是否将“Verified Project Continuity + Human-steered Real Artifact Loop”作为 OLEANDER v1 的第一产品楔子，而把 Team、Cloud、Marketplace、Large-scale Agent Orchestration 延后？**

Current recommendation in this working document: **maintain this as the working product hypothesis until external pilot evidence challenges it.**

这不是 Promotion 或 Current Architecture 决定。