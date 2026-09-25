# OLEANDER PRD Feature Spec｜HOME + FOCUS v0.2.0

[← Feature Specs](README.md) · [← Master PRD](../OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

**Scope:** Project re-entry, Current Design Question, framing, design value, scope, constraints, assumptions, success condition, frontier.  
**State:** WORKING PRODUCT SPEC / NON-AUTHORITY.

---

# 1｜HOME — Project Home

## 1.1 Product job

HOME 不是 dashboard。它的唯一核心任务是：

> **让用户在最短路径内重新进入当前真实设计状态。**

用户进入 HOME 后，应能够回答：

1. 我们现在真正解决什么？
2. 当前方向是什么？
3. 设计真正卡在哪里？
4. 哪个 artifact 最相关？
5. 最近发生了什么有意义变化？
6. 下一步最值得做什么？
7. 哪些信息仍不确定或 stale？

## 1.2 Primary users

- DU-01 Design Author
- DU-02 Design Lead
- DU-03 Domain Designer
- DU-04 Integrator
- DU-06 Design Producer
- DU-08 Limited Collaborator（只读深度）

## 1.3 Entry conditions

HOME 可从以下入口进入：

- project open；
- new session resume；
- handoff；
- tool return；
- review return；
- plugin/session reconstruction；
- explicit “继续 / resume”。

## 1.4 Exit conditions

用户从 HOME 进入：
- FOCUS：问题需要重新 framing；
- STUDIO：当前问题清楚，可以继续设计；
- ARTIFACTS：需要打开真实 artifact；
- REVIEW：存在关键 finding / unread result；
- KNOWLEDGE：当前 frontier 被 evidence gap 限制；
- HISTORY：需要理解 decision / reframe lineage。

---

# 2｜HOME 信息层级

## Layer A｜NOW

必须优先显示：

- Current Design Question
- Current Direction
- Current Frontier
- Critical Open
- Active Artifact
- Next High-Value Action

## Layer B｜WHAT CHANGED

只显示会改变设计理解的变化：

- design question reframed；
- direction selected / reopened / retired；
- major relation changed；
- meaningful artifact revision；
- critical review finding；
- validation result；
- frontier changed。

## Layer C｜RISK / ATTENTION

- stale assumption；
- unresolved high-impact issue；
- unread artifact；
- intent drift candidate；
- validation gap；
- authority / checkpoint conflict。

---

# 3｜HOME Feature Requirements

## HOME-F01｜Resume Snapshot

**Purpose**  
把项目恢复结果压缩成用户可立即理解的设计上下文。

**User need trace**  
UN-P01 / P02 / P03 / P04 / P05 / P06.

**Trigger**
- enter project；
- resume request；
- handoff open；
- session context reconstruction。

**Inputs**
- owner-native Current carrier；
- Current Project / Task；
- Control Card；
- Execution Receipt / checkpoint；
- active native artifact / readback；
- current Design Question / Direction / Frontier。

**System behaviour**
1. 先 resolve owner-native source；
2. 不以 chat summary 作为唯一 truth；
3. 生成简洁 Resume Snapshot；
4. 每个摘要字段可展开 source basis；
5. 如果 source conflict 未闭合，显示 provisional / conflict，不制造单一确定结论。

**Visible result**
至少包含：
- What we are solving
- Current direction
- Current frontier
- Critical open
- Active artifact
- What changed
- Next action

**Allocation**
A3 SYSTEM-ASSISTED + A4 summarization；Human 可纠正。

**Acceptance**
- 给定跨会话真实项目，用户无需重新粘贴历史即可指出当前问题、artifact 和 next action；
- snapshot 中的 Current / revision 与 owner-native carrier 一致；
- chat memory 与 Current 冲突时，Current 胜出；
- conflict 未解决时不静默合并。

**Failure / degraded**
- source carrier 不可访问 → 明确 `RESUME_PARTIAL`，列出缺失 carrier；
- stale checkpoint → 不继续项目写入；
- artifact missing → 保持 design state，但标记 native surface unavailable。

**Events**
- `project_resume_started`
- `frontier_resolved`
- `resume_corrected_by_user`
- `resume_degraded`

**Priority** P0

---

## HOME-F02｜Frontier Card

**Purpose**  
显示当前真正限制设计成熟度的一个或少量关键 frontier，而不是完整 task list。

**Inputs**
- Current Question；
- unresolved critical relations；
- maturity gap；
- open findings；
- dependencies。

**System behaviour**
- 推荐 1–3 个 frontier；
- 每个 frontier 必须说明 why now；
- 不能以“最近创建”“agent 正在做”替代优先级；
- 用户可以纠正或重新定义 frontier。

**Visible result**
- Frontier statement
- Why it matters
- What blocks it
- What could move it forward
- Related artifact / relation

**Acceptance**
- 用户可以明确解释“为什么下一步做这个，而不是别的”；
- frontier 能回溯至少一个 Design Question / Relation / Finding；
- 不允许只显示 generic “继续深化”。

**Failure**
若不存在足够 evidence 判断最优 frontier，可显示 2–3 个 candidate frontier，并标记 uncertainty。

**Events**
- `frontier_candidate_shown`
- `frontier_confirmed`
- `frontier_reframed`

**Priority** P0

---

## HOME-F03｜Critical Open

**Purpose**  
只显示会影响当前设计推进的 OPEN。

**Required fields**
- open statement
- reason
- affected scope
- what it blocks
- what it does not block
- close condition
- owner if known

**Acceptance**
- OPEN 不等于 FAIL；
- safe-open 不应阻止无关工作；
- critical open 被关闭时必须产生 evidence / decision / readback link。

**Priority** P0

---

## HOME-F04｜Active Artifact

**Purpose**  
让用户知道当前判断应回到哪个真实 artifact。

**Required fields**
- artifact name / ID
- role
- revision
- source / native status
- last readback
- fidelity / does-not-prove
- related Design Question

**Acceptance**
- preview/export 不得默认成为 active native master；
- artifact recency 不自动改变 authority；
- Active Artifact 必须能跳转到 ARTIFACTS surface。

**Priority** P0

---

## HOME-F05｜Recent Design Moves

**Purpose**  
记录真正改变设计理解的最近动作。

**Included**
- reframe
- direction selection / reject / reopen
- relation change
- meaningful revision
- critical finding
- validation result
- frontier shift

**Excluded**
- file opened
- agent started
- tool call success
- formatting change
- routine save
- log event

**Acceptance**
最近列表不能退化为 system activity feed。

**Priority** P1

---

## HOME-F06｜Next Design Actions

**Purpose**  
提供 1–3 个下一步高价值动作。

**Each action must contain**
- target
- intended design consequence
- artifact / surface
- Human requirement if any
- reversibility
- expected readback

**Acceptance**
“生成更多方案”只有在 exploration gap 存在时才可出现；“继续”必须可执行到具体对象。

**Priority** P0

---

## HOME-F07｜Resume Confidence / Source Basis

**Purpose**  
让用户需要时知道 Resume Snapshot 从哪里恢复，不强迫默认查看治理。

**Visible by progressive disclosure**
- source carrier
- revision
- checkpoint
- artifact readback basis
- conflict / staleness

**Acceptance**
默认折叠；只有 conflict / stale / low-confidence 时自动提升可见性。

**Priority** P1

---

## HOME-F08｜What Changed Since Last Session

**Purpose**  
帮助用户快速识别跨会话 delta。

**Acceptance**
- 只报告 material delta；
- 必须区分 Human decision、AI reversible work、external/tool change、review finding；
- “没有 material change”是合法结果。

**Priority** P1

---

# 4｜FOCUS — Design Focus

## 4.1 Product job

FOCUS 回答：

> **我们现在真正需要解决什么？**

它不是 issue form，也不是 brief storage。

## 4.2 Information structure

```text
Design Situation
→ Problem
→ Design Question
→ Design Value
→ Scope / Scale
→ Constraints
→ Assumptions
→ Success Condition
→ Frontier
```

---

# 5｜FOCUS Feature Requirements

## FOCUS-F01｜Problem Statement

**Purpose**  
保存 broader problem condition，而不是把用户最初提出的解决方案当成问题。

**Required semantics**
- observed / reported condition
- affected actor/context
- impact
- evidence status
- unknowns

**Acceptance scenario**
客户说“入口要加大屏”。系统允许保留这个 request，但 Problem Statement 可以表达为“首次到达者无法快速理解入口与主空间组织”，且两者不混为一谈。

**Priority** P0

---

## FOCUS-F02｜Current Design Question

**Purpose**  
维护当前可通过设计行动和现实反馈逐步回答的问题。

**Required fields**
- question statement
- linked problem
- scope
- scale
- linked values
- related directions / findings
- lifecycle semantic
- current relevance

**Local lifecycle**
- ACTIVE
- PAUSED
- ANSWERED
- REFRAMED
- SUPERSEDED
- REOPENED

这些只是 Question 局部语义，不是 Project State。

**Acceptance**
- active design scope 必须有一个可识别 Current Question；
- question 不能只是 task，例如“做三张图”；
- Question 应能解释什么 evidence / artifact / comparison 可以帮助回答。

**Priority** P0

---

## FOCUS-F03｜Design Value / Intent

**Purpose**  
表达设计希望创造或保护的核心价值。

**Required distinction**
```text
VALUE = why it matters
RELATION = how value is carried
IMPLEMENTATION = how it is currently realized
```

**Human/System allocation**
- final value definition：A1 HUMAN-ONLY；
- system may surface conflict / vagueness / prior rationale。

**Acceptance**
- “使用木材”不能直接当 Design Value；
- Value change 必须保留 rationale；
- system 不得静默改写 Value。

**Priority** P0

---

## FOCUS-F04｜Scope / Scale

**Purpose**  
标记当前判断发生的尺度。

**Supported semantics**
- local
- subsystem
- whole design
- contextual/systemic
- coupled multi-scale

**Acceptance**
系统可以建议 scale，但不能因为当前打开的是局部 artifact 就默认问题只在局部。

**Priority** P1

---

## FOCUS-F05｜Constraints & Assumptions

**Constraint semantics**
- HARD
- SOFT
- UNKNOWN

**Assumption semantics**
- statement
- reason
- scope
- consequence if false
- reversibility
- evidence trigger

**Acceptance**
- Assumption ≠ Fact；
- UNKNOWN constraint 可以限制 claim，但不能被静默当 Hard；
- assumption 被推翻后必须触发 impact analysis。

**Priority** P0

---

## FOCUS-F06｜Success Condition

**Purpose**  
定义什么可以让当前 Question “足够解决”，而不是把完成标准写成产物数量。

**Examples**
好：
- 首次使用者能在入口处理解主空间组织；
- 三个候选的关系机制已通过真实 section compare。

不好：
- 完成 5 张图；
- Agent 跑完；
- 页面全部填满。

**Priority** P1

---

## FOCUS-F07｜Reframe

**Trigger**
- new evidence
- repeated failure
- validation contradiction
- stale assumption
- context change
- Human explicit reframe

**Human authority**
最终 reframe 为 HUMAN-ONLY / HUMAN-LED。

**System may**
- propose alternative framing；
- show why current framing may fail；
- identify hidden assumption。

**Priority** P0

---

## FOCUS-F08｜Reframe Impact

**Required output**
- remains valid
- must be revisited
- becomes irrelevant
- new unknowns
- affected decisions
- affected artifacts
- affected validation

**Acceptance**
Reframe 不默认 project reset。

**Priority** P0

---

## FOCUS-F09｜Frontier Definition

**Purpose**  
把 Question 转成下一步高价值 design frontier。

**Required fields**
- target relation / unknown
- why this is bottleneck
- artifact / evidence needed
- expected judgment after action
- dependencies
- Human stop if expected

**Priority** P0

---

# 6｜HOME + FOCUS Core Flow

```text
PROJECT ENTRY
→ HOME RESOLVE
→ Resume Snapshot
→ Current Question clear?
   YES → Frontier → Studio / Artifact / Review
   NO  → FOCUS
        → Problem
        → Value
        → Constraint / Assumption
        → Question
        → Success Condition
        → Frontier
        → Studio
```

---

# 7｜Key Failure Scenarios

## HF-E01｜Chat history says A, Current carrier says B
Display B as Current; optionally surface conflict provenance. No merge by recency.

## HF-E02｜No Current Question found
Do not invent one as truth. Present candidate framing and require Human confirmation before consequential design direction decision.

## HF-E03｜Question too broad
System may propose smaller decision objects, but preserve whole-design relation.

## HF-E04｜Question too local
If repeated revision fails, suggest scale escalation / reframe.

## HF-E05｜Constraint source unknown
Mark UNKNOWN; do not upgrade to HARD.

## HF-E06｜User says “继续” while Current is stale
Resume intent remains valid, but mutation guard blocks stale write until re-resolve.

---

# 8｜Metrics

- Time to Verified Resume
- Resume Correction Rate
- Repeated Context Input
- Current Question Clarity Rating
- Frontier Correction Rate
- Stale Assumption Detection
- Percentage of HOME actions that lead to productive design surface
- Percentage of sessions that begin by browsing files/logs because resume failed

---

# 9｜Verification

Minimum:
- INSPECTION
- DEMONSTRATION
- TEST
- USER_EVALUATION
- PROJECT_EXERCISE

Scenarios must include：
- long-gap resume；
- stale checkpoint；
- reframe without reset；
- unknown constraint；
- one valid Current artifact + newer presentation derivative；
- project with multiple open issues but only one critical frontier。
