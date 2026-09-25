# OLEANDER PRD Feature Spec｜STUDIO + COMPARE v0.2.0

[← Feature Specs](README.md) · [← Master PRD](../OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

**Scope:** Exploration, design development, synthesis, comparison, trade-off, Human steering, decision rationale.  
**State:** WORKING PRODUCT SPEC / NON-AUTHORITY.

---

# 1｜STUDIO — Design Studio

STUDIO 是 OLEANDER 的主要设计工作面。

它不是 native authoring tool replacement，而是：

> **组织设计动作、候选、发展前沿和判断。**

三种 mode：

```text
EXPLORE
DEVELOP
SYNTHESIZE
```

这些是工作模式，不是强制线性 stage。

---

# 2｜EXPLORE

## 2.1 Product job

当 Design Question 尚未收敛时，形成少量真正不同的方向，并把差异做成可比较的机制与 artifact。

核心原则：

```text
MORE OPTIONS ≠ BETTER EXPLORATION
MATERIAL DIFFERENCE > COSMETIC VARIATION
```

---

## EXP-F01｜Create Direction

**Purpose**  
建立一个候选 Design Direction。

**Required fields**
- direction ID
- strategy statement
- linked Design Question
- linked Design Value
- mechanism signature
- expected consequence
- parent refs if derivative
- branch status
- key unknowns

**Acceptance**
每个 Direction 必须解释“它改变了什么关系”，不能只有 mood / style 名称。

**Priority** P0

---

## EXP-F02｜Strategy Statement

**Required form**
- what changes
- why
- which problem it addresses
- what value it protects
- what trade-off it introduces

**Bad**
“方案 B 更现代。”

**Good**
“方案 B 把共享支持从中央节点改成边缘分布，使主空间连续性增强，但增加服务路径长度。”

**Priority** P0

---

## EXP-F03｜Relation Difference

**Purpose**  
把方向差异从视觉描述提升到 Design Relation。

**Possible relation families**
- spatial
- functional
- structural
- material
- interaction
- behavioural
- visual
- sequence
- interface
- operational

**Acceptance**
两个方向如果只有表面形式变化、relation / mechanism signature 相同，不算 distinct option。

**Priority** P0

---

## EXP-F04｜Alternative Set

**Purpose**  
把多个方向放进同一 comparison world。

**Required conditions**
- same decision object
- same key question
- comparable fidelity
- same locked invariants
- explicit differences
- explicit unknowns

**Acceptance**
不同 fidelity 的 hero render 与低保真草图不能直接作为无说明的公平 comparison。

**Priority** P0

---

## EXP-F05｜Search-space Gap

**Purpose**  
识别当前 alternatives 是否都集中在同一策略区域。

**System behaviour**
- detect mechanism similarity；
- suggest missing strategy families；
- may suggest baseline / no-change / OFF；
- must not automatically declare exploration sufficient。

**Allocation**
A3 SYSTEM-ASSISTED；Human decides whether exploration is enough.

**Priority** P1 / research-sensitive

---

## EXP-F06｜Reference Transformation

**Purpose**  
使用 precedent 的关系，而不是复制结果。

**Required output**
- source precedent
- transferable relation
- similar conditions
- different conditions
- non-transferable elements
- current project consequence

**Acceptance**
如果只记录“参考某项目”，不算有效 transfer。

**Priority** P1

---

## EXP-F07｜Hold / Continue / Retire

**Actions**
- CONTINUE
- HOLD
- RETIRE

**Rules**
- RETIRE 是 consequential human decision；
- HOLD 不等于 reject；
- retired branch 保留 lineage / rationale；
- branch 状态不等于 Project Current。

**Priority** P0

---

## EXP-F08｜Baseline / No-change / OFF

**Purpose**  
在 causally relevant 时把“什么都不做 / 保持现状 / 关闭功能”作为真实 option。

**Acceptance**
系统不得默认“增加一个设计介入”总是更优。

**Priority** P1

---

## EXP-F09｜Material Distinctness Check

**Minimum checks**
- relation difference
- mechanism difference
- consequence difference
- artifact expression difference

**Failure**
如果 A/B/C 仅颜色、字体、装饰或轻微 geometry 变化 → 标记 shallow variation，不计 exploration coverage。

**Events**
- `option_space_created`
- `cosmetic_duplicate_detected`
- `material_distinctness_reviewed`

**Priority** P0

---

# 3｜DEVELOP

## 3.1 Product job

把已选择方向从 concept 推向专业设计：

```text
concept
→ relation
→ geometry / behaviour
→ dimension / state
→ detail / implementation
→ performance / operation
```

而不让核心 Design Value 在深化中静默丢失。

---

## DEV-F01｜Maturity Gap

**Purpose**  
显示“当前还缺什么”，而不是显示单一 completion %。

**Dimensions may include**
- Problem / Brief
- Intent / Value
- Concept
- Spatial / Formal
- Human / Experience
- Material / Craft
- Technical / Professional
- Integration
- Prototype / Evidence
- Communication / Representation

**Acceptance**
某个 artifact 可以 representation complete，但 professional depth / evidence 仍 low。

**Priority** P1

---

## DEV-F02｜Next Development Frontier

**Purpose**  
识别当前最值得深化的设计层。

**Inputs**
- Current Question
- maturity gaps
- bottleneck relation
- findings
- dependencies
- active artifact

**Visible result**
- target relation
- required resolution increase
- artifact target
- expected readback
- domain lens

**Priority** P0

---

## DEV-F03｜Resolution Ladder

**Purpose**  
帮助用户理解“继续深化”具体意味着什么。

**Acceptance**
系统不得把更多页面 / 更多 feature / 更多文字当作 higher resolution。

**Priority** P1

---

## DEV-F04｜Professional Depth

**Purpose**  
把专业问题嵌回设计，而不是作为独立 checklist。

**Behaviour**
- bind relevant domain process；
- expose professional unknown；
- preserve professional authority；
- avoid universal CoDesign stage。

**Priority** P0

---

## DEV-F05｜Intent Check

**After material development**
系统支持判断：
- strengthens
- retains
- transforms
- weakens
Design Value。

**Authority**
System provides candidate signal; Human interprets significance.

**Priority** P1

---

## DEV-F06｜Low-resolution Warning

**Trigger**
artifact looks complete but key relations remain:
- generic
- undimensioned
- untested
- unintegrated
- low-fidelity
- unprofessionalized

**Acceptance**
warning 必须指出具体 relation / missing evidence，不允许 generic “需要继续深化”。

**Priority** P1

---

## DEV-F07｜Development Action

每个 Development Action 至少包含：
- target relation
- intended improvement
- artifact target
- expected readback
- domain owner if relevant
- reversibility
- affected dependencies

**Priority** P0

---

## DEV-F08｜Domain Adapter Binding

**Purpose**  
选择 authentic professional process。

**Required fields**
- domain_id
- process status
- process reference
- current domain question
- required native output
- readback method
- claim ceiling
- HOLD conditions

**Acceptance**
若 domain process = OPEN，可做 bounded exploration，但不能 award professional PASS。

**Priority** P0

---

## DEV-F09｜Return-to-Whole Check

局部深化完成后重新看：
- whole coherence
- value continuity
- cross-domain impact
- local optimization damage

**Priority** P1

---

# 4｜SYNTHESIZE

## 4.1 Product job

> **减少不必要复杂度，提高 design economy。**

系统不是“feature 增加器”。

---

## SYN-F01｜Complexity Review

分类：
- core
- supporting
- redundant
- duplicated
- incidental

**Priority** P1

---

## SYN-F02｜Merge Opportunity

识别多个局部机制是否可由更强核心 relation 替代。

**Priority** P1

---

## SYN-F03｜Design Economy

**Question**
一个 relation 是否同时解决多个重要问题？

**No automatic score requirement**
系统可辅助分析，但不需输出伪精确单一评分。

**Priority** P2 / research-sensitive

---

## SYN-F04｜Grammar Consistency

检查不同局部语言是否互相冲突或产生无意义例外。

**Priority** P1

---

## SYN-F05｜Hierarchy Reinforcement

强化：
- primary
- secondary
- tertiary
relations。

**Priority** P1

---

## SYN-F06｜Simplification Test

删除 / 合并前后比较：
- value lost?
- clarity gained?
- professional function lost?
- downstream effect?
- maintenance / operation effect?

**Priority** P1

---

## SYN-F07｜Loss Check

简化不能违反 NO COMPRESSION / NO LOSS。

**Acceptance**
如果独立有效信息或 relation 被删除，必须有明确 design rationale，而不是“为了更简洁”。

**Priority** P0

---

# 5｜COMPARE — Cross-surface Compare Mode

## 5.1 Product job

COMPARE 是 OLEANDER 最核心的判断工作面之一。

它不负责自动选择 winner。

Compare 支持：
- Option / Option
- Before / After
- Intent / Result
- Local / Whole
- Expected / Observed
- Current / Proposed

---

## CMP-F01｜Side-by-Side

**Requirement**
用户应能并列查看真正用于同一判断的对象。

**Acceptance**
不同 version / fidelity / source 时必须显式标注，避免伪公平比较。

**Priority** P0

---

## CMP-F02｜Relation-level Difference

显示：
- changed relation
- unchanged relation
- new relation
- removed relation

而不只显示视觉差异。

**Priority** P0

---

## CMP-F03｜Consequence Difference

每个 option 显示：
- direct benefit
- direct cost
- downstream consequence
- affected domains
- reversibility

**Priority** P0

---

## CMP-F04｜Trade-off View

至少允许：
- gain
- loss
- uncertainty
- conflict
- value affected

**Rule**
System may expose trade-off; Human decides whether it is worth it.

**Priority** P0

---

## CMP-F05｜Uncertainty View

区分：
- known
- supported
- inference
- assumption
- evidence gap
- unknown

**Priority** P0

---

## CMP-F06｜Decision Rationale

Human 可记录：
- why selected
- why rejected/held
- accepted cost
- unresolved concern

**Rule**
Human 未提供 rationale 时系统不得伪造。

**Priority** P0

---

## CMP-F07｜Reopen Condition

记录：
- which new evidence
- context change
- failure
- professional conflict
会触发 decision reopen。

**Priority** P1

---

## CMP-F08｜Retained Alternative

“现在不选”但仍有潜力的方向可保持 HOLD / RETAINED，不污染 Current。

**Priority** P1

---

## CMP-F09｜Same Comparison World

Comparable set 必须共享：
- decision object
- key unknown
- relevant locked invariants
- comparison assumptions
- sufficient comparable fidelity

**Priority** P0

---

## CMP-F10｜Artifact Revision Binding

每个 option 必须绑定实际 artifact revision / content identity。

**Acceptance**
display label A/B/C 不能成为唯一 proof。

**Priority** P0

---

## CMP-F11｜Human Steer Capture

支持：
- SELECT
- MODIFY
- MIX
- REJECT
- REOPEN
- DEFER

并保留 exact referent / revision / lineage。

**Priority** P0

---

# 6｜STUDIO + COMPARE End-to-End

```text
CURRENT DESIGN QUESTION
→ EXPLORE
→ materially distinct directions
→ MAKE minimum faithful artifacts
→ COMPARE
→ LOOK / CRITIQUE
→ Human action?
  NONE → continue exploration / repair
  SELECT → develop branch
  MODIFY → create revised branch
  MIX → preserve all parents + new branch
  REJECT → rejected-preserved
  DEFER → dependent HOLD / unrelated continue
  REOPEN → active again
→ DEVELOP
→ READBACK
→ RETURN TO WHOLE
→ SYNTHESIZE when complexity accumulates
```

---

# 7｜Human Steering Acceptance

## SC-01 SELECT
Given A/B/C bound to exact revisions, “选 B” creates SELECT B only.

## SC-02 MODIFY
“保留 B 的空间关系，但把入口开放度提高” → B is parent; changed variable explicit.

## SC-03 MIX
“保留 A 的操作逻辑，结合 B 的空间关系” → both parent refs required.

## SC-04 REJECT
“不要 A” → A becomes rejected-preserved, not deleted.

## SC-05 REOPEN
“把刚才放弃的 A 再拿回来” → existing branch reopened; no duplicate new branch unless content changes.

## SC-06 DEFER
“这个决定先放着” → requires pending decision; dependent mutations HOLD.

## SC-07 Compound
“不要 A，保留 B，结合 C” → at minimum REJECT A + MIX B,C if grammar/context makes B,C parents unambiguous.

---

# 8｜Failure / Degraded Scenarios

## SD-E01 Cosmetic-only A/B/C
System flags low material divergence and may generate new mechanism families.

## SD-E02 One option has hero render, another only text
Comparison must show fidelity mismatch or request comparable artifact.

## SD-E03 Human chooses by vague “这个”
If multiple objects visible → minimum clarification.

## SD-E04 User asks to auto-finish during value choice
AUTO_ADVANCE does not cross Human-only design decision.

## SD-E05 Domain tool unavailable
Create truthful bounded prototype if it can answer current question; hold native completion claim.

## SD-E06 Exploration never converges
Show critical unknowns / diminishing return / remaining strategy gap; Human decides converge.

## SD-E07 Early option becomes anchoring bias
Search-space Gap may propose at least one structurally different branch or baseline.

---

# 9｜Events

- `design_direction_created`
- `mechanism_signature_recorded`
- `option_space_created`
- `search_space_gap_detected`
- `cosmetic_duplicate_detected`
- `comparison_opened`
- `tradeoff_exposed`
- `human_steer_bound`
- `branch_rejected`
- `branch_deferred`
- `branch_reopened`
- `development_frontier_selected`
- `intent_drift_candidate`
- `synthesis_move_created`

---

# 10｜Metrics

- Material Divergence Rate
- Cosmetic Duplicate Rate
- Time to Comparable Artifact
- Human Steer Clarification Rate
- Wrong Referent Mutation Rate
- Accepted Option Rationale Capture Rate
- Reopen Rate
- Development Frontier Correction Rate
- Low-resolution Completion Detection Rate
- Synthesis Loss Rejection Rate

---

# 11｜Verification

At minimum：
- TEST
- DEMONSTRATION
- USER_EVALUATION
- PROJECT_EXERCISE
- DESIGN REVIEW

必须使用真实 design artifact，而不是仅用文字 fixture 验证所有体验要求。
