# OLEANDER PRD Feature Spec｜REVIEW + KNOWLEDGE + HISTORY v0.2.0

[← Feature Specs](README.md) · [← Master PRD](../OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

**Scope:** Critique、Finding、Independent Review、Verification、Validation、Evidence、Knowledge Applicability、History、Resume、Handoff。  
**State:** WORKING PRODUCT SPEC / NON-AUTHORITY.

---

# 1｜REVIEW — Review & Validation

## 1.1 Product job

REVIEW 不是“打分页面”。

它负责把真实 artifact、真实结果、专业判断、证据和用户/情境结果重新转化为下一步设计判断。

必须始终保持：

```text
DESIGN CRITIQUE
≠ PROFESSIONAL REVIEW
≠ EVIDENCE REVIEW
≠ REPRESENTATION REVIEW
≠ EXECUTION REVIEW
≠ VERIFICATION
≠ VALIDATION
```

---

# 2｜REVIEW Feature Requirements

## REV-F01｜Review Target

**Purpose**
任何正式 review 必须绑定真实对象。

**Target may be**
- Artifact + revision
- Design Relation
- Design Direction
- Design Decision
- Verification Claim
- Validation Scenario

**Acceptance**
不能只审查 producer summary。

**Priority** P0

---

## REV-F02｜Finding

**Purpose**
把 observation / critique 转成可以推动设计的 finding。

**Required fields**
- finding statement
- finding type
- affected object
- evidence/readback basis
- impact
- uncertainty
- suggested next action if appropriate

**Rule**
Finding 不自动改变 Current。

**Priority** P0

---

## REV-F03｜Finding Type

至少支持：
- design
- professional
- evidence
- representation
- execution
- validation

**Acceptance**
render 很差但空间成立时，允许记录 representation failure，而不是整体否定 design。

**Priority** P0

---

## REV-F04｜Severity / Impact

表达真实影响，而不是单一总分。

可包括：
- blocking
- high-impact
- material
- local
- cosmetic

**Rule**
严重问题不能被多个小 PASS 平均掉。

**Priority** P1

---

## REV-F05｜Affected Relation

Finding 应尽可能绑定受影响 relation。

如果当前只能表达“整体不对”，先保留 concern，再逐步定位，不强制用户假装知道原因。

**Priority** P0

---

## REV-F06｜Root-cause Hypothesis

允许一个 finding 有多个 candidate root causes。

**Rule**
Hypothesis ≠ verified cause。

**Acceptance**
repair 应明确针对哪个 hypothesis；readback 后才能判断 hypothesis 是否被支持。

**Priority** P0

---

## REV-F07｜Recommended Design Action

Finding 转成下一 design action 时必须包含：
- target relation
- intended repair
- affected scope
- artifact target
- expected readback

**Priority** P0

---

## REV-F08｜Recheck Requirement

记录什么必须在修复后重新检查。

Examples：
- same view / state
- related interface
- whole-design coherence
- specialist verification
- accessibility
- browser breakpoint
- physical use

**Priority** P0

---

## REV-F09｜Independent Review

**Purpose**
允许独立 reviewer 保持独立判断。

**Hard rules**
- producer critique 不等于 independent review；
- latest review 不自动 supersede older unresolved disagreement；
- independent reviewer 不能因为“reviewer”角色自动获得 project authority。

**Priority** P1

---

## REV-F10｜Validation Scenario

**Required fields**
- who
- context
- task / behaviour
- expected outcome
- artifact / prototype fidelity
- observation method
- success / failure interpretation
- limitation

**Acceptance**
不能把 design team 自评当 end-user validation。

**Priority** P0

---

## REV-F11｜Verification Claim / Evidence

每个高影响 claim 至少记录：
- claim
- requirement / criterion
- evidence
- evidence fidelity
- applicability
- result
- does-not-prove

**Priority** P0

---

## REV-F12｜Does-not-prove Boundary

**Purpose**
防止低强度 evidence 支持高强度 claim。

Examples：
- browser dry-run does not prove representative-user usability；
- render does not prove material performance；
- structural file existence does not prove structural adequacy；
- remote research does not prove field condition。

**Priority** P0

---

## REV-F13｜Revision Re-readback

修复重要 finding 后，问题关闭前必须重新 readback。

**Acceptance**
“已修改代码/文件”不能直接关闭 finding。

**Priority** P0

---

# 3｜Verification vs Validation

## Verification

回答：

> **是否按照已经声明的 requirement / design condition 正确实现？**

可能检查：
- geometry
- dimension
- state
- behaviour
- interface
- requirement
- performance criterion

## Validation

回答：

> **即使实现正确，它在真实用户、真实情境和真实目标中是否真正有效？**

可能检查：
- understanding
- behaviour
- usability
- comfort
- operational value
- desirability
- real problem resolution

**Hard rule**

```text
VERIFICATION PASS ≠ VALIDATION PASS
```

---

# 4｜KNOWLEDGE — Knowledge & Evidence

## 4.1 Product job

KNOWLEDGE 不是“管理所有知识”。

它只回答：

> **为了当前设计判断，我们需要知道什么？这些信息能证明什么、不能证明什么？**

---

## KNW-F01｜Knowledge Need

由 Design Question / Finding / Verification / Validation 触发。

**Required fields**
- question
- why needed
- affected relation
- required confidence
- deadline / decision point if applicable

**Priority** P0

---

## KNW-F02｜Source

记录：
- source identity
- provenance
- date/freshness
- jurisdiction/context
- creator/authority when relevant

**Priority** P0

---

## KNW-F03｜Evidence Strength

不需要单一通用 score，但至少能表达：
- direct / indirect
- strong / limited
- observed / reported
- primary / secondary
- verified / unverified

**Priority** P0

---

## KNW-F04｜Applicability

说明：
- where applies
- conditions
- population / jurisdiction
- project fit
- non-transferable part

**Priority** P0

---

## KNW-F05｜Design Meaning

每条 material knowledge 尽量转成：
- opportunity
- constraint
- risk
- design consequence
- unresolved question
- no-action relevance

**Acceptance**
source summary 没有 design meaning 时，不应默认进入主设计工作面。

**Priority** P0

---

## KNW-F06｜Limitation

说明：
- what source cannot establish
- known gaps
- outdated risk
- conflict
- required follow-up

**Priority** P0

---

## KNW-F07｜Contradiction

多个来源冲突时：
- preserve each source
- show disagreement
- identify affected design question
- do not average into fake consensus

**Priority** P1

---

## KNW-F08｜Precedent Transfer

必须区分：
- transferable
- conditional
- non-transferable

**Acceptance**
precedent 不能只以“参考图”存在；应说明 relation / mechanism 如何转译。

**Priority** P1

---

## KNW-F09｜Return to Design

Knowledge 必须能回到：
- Question
- Relation
- Direction
- Decision
- Verification / Validation

**Priority** P0

---

## KNW-F10｜Freshness / Staleness

当来源版本、规范、运营状态等可能过期：
- 标记 freshness；
- affected claim / relation 可被提示；
- stale 不自动删除历史。

**Priority** P1

---

## KNW-F11｜Claim Ceiling

证据强度只允许支持相匹配的 claim。

**Rule**
Missing evidence narrows claim ceiling; it does not automatically freeze unrelated reversible design.

**Priority** P0

---

# 5｜HISTORY — Continuity & History

## 5.1 Product job

HISTORY 不记录所有系统事件。

它只记录：

> **改变设计理解的重要事件。**

---

## HIS-F01｜Design Timeline

事件包括：
- problem reframe
- direction selected / retired / reopened
- major relation change
- key trade-off
- major artifact revision
- critical finding
- validation result
- frontier change

**Priority** P1

---

## HIS-F02｜Decision History

保存：
- decision
- actor / authority
- basis
- accepted cost
- uncertainty
- reopen condition
- affected relations

**Priority** P0

---

## HIS-F03｜Rejected Direction Memory

保存：
- branch identity
- why rejected
- what was still valuable
- reopen condition if any

**Rule**
Rejected ≠ deleted.

**Priority** P1

---

## HIS-F04｜Reframe History

保存：
- old framing
- trigger
- new framing
- valid preserved work
- invalidated work
- impact

**Priority** P1

---

## HIS-F05｜Frontier History

记录每一阶段“真正限制设计成熟”的 frontier，而不是 task completion。

**Priority** P2

---

## HIS-F06｜Resume Point

**Purpose**
为 session / person / agent handoff 提供 owner-native locator。

**Minimum**
- Current Question
- Current Direction
- Current Frontier
- Critical Open
- active artifacts
- next allowed action
- source carriers

**Boundary**
Resume Point 不能成为 plugin-owned alternative Project State。

**Priority** P0

---

## HIS-F07｜Handoff Pack

给下一设计者 / Agent：
- current question
- current direction
- key values
- key relations
- decisions
- open issues
- artifact refs
- readbacks
- next frontier
- authority / claim limits

**Acceptance**
接收方可以 challenge upstream interpretation；handoff 不等于 acceptance。

**Priority** P1

---

## HIS-F08｜Human-steer Lineage

保存：
- Human action
- exact referents
- parent branches
- changed variables
- preserved invariants
- second-round artifact/readback

**Priority** P0

---

## HIS-F09｜Project Learning Candidate

项目 lesson 可以形成 candidate：
- observation
- condition
- outcome
- counterevidence
- transfer condition

但不能自动晋级 reusable professional rule。

**Priority** P2

---

# 6｜Review / Knowledge / History Core Loop

```text
REAL ARTIFACT
→ READBACK
→ OBSERVATION
→ FINDING
→ ROOT-CAUSE HYPOTHESIS
→ KNOWLEDGE / EVIDENCE if needed
→ DESIGN ACTION
→ REVISION
→ RE-READBACK
→ VERIFY / VALIDATE when appropriate
→ HISTORY records material learning / decision
→ CONTINUE
```

---

# 7｜Key Edge Cases

## RKH-E01｜AI says “looks good”
No effect unless bound to actual artifact/readback; still not Design KEEP.

## RKH-E02｜Two reviewers disagree
Preserve disagreement; route authority separately.

## RKH-E03｜Strong evidence but wrong population
Mark applicability mismatch; do not generalize.

## RKH-E04｜Field evidence missing
Keep OPEN / narrow claim ceiling; do not turn remote evidence into field fact.

## RKH-E05｜Verification PASS but users fail task
Validation failure remains material; product must reopen relevant design question.

## RKH-E06｜Old rejected option becomes relevant after context change
Allow REOPEN with existing lineage.

## RKH-E07｜Knowledge source updated
Identify affected claim / relation; do not silently overwrite history.

## RKH-E08｜Handoff summary loses nuance
Recipient can open rationale / evidence / readback progressively; summary is not authority by itself.

---

# 8｜Events

- `review_started`
- `finding_created`
- `disagreement_recorded`
- `root_cause_hypothesis_created`
- `recheck_required`
- `verification_result_recorded`
- `validation_scenario_created`
- `validation_result_recorded`
- `knowledge_need_created`
- `evidence_linked`
- `evidence_contradiction_detected`
- `decision_recorded`
- `branch_reopened`
- `handoff_pack_created`

---

# 9｜Metrics

- Finding-to-Action Conversion Rate
- Finding Reopen Rate
- Revision Re-readback Rate
- Verification / Validation Confusion Rate
- Evidence Applicability Correction Rate
- Critical Claim with Does-not-prove Coverage
- Handoff Correction Rate
- Resume after Handoff Success Rate
- Rejected Branch Recoverability
- Percentage of high-impact decisions with rationale/reopen condition

---

# 10｜Verification

Minimum scenarios：
- good design / bad render；
- bad design / technically valid artifact；
- contradictory evidence；
- stale source；
- real user validation contradicting internal review；
- independent reviewer disagreement；
- rejected branch reopened；
- cross-session handoff；
- field evidence missing but bounded design continues。
