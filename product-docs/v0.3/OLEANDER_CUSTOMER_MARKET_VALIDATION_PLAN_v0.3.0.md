# OLEANDER Customer & Market Validation Plan v0.3.0

[← v0.3 Package](README.md)

**State:** `RESEARCH PLAN / NOT YET EXECUTED`

> 当前产品证据强在 owner-led real projects、系统机制与真实 artifact；弱在外部用户和商业市场。本文把这一缺口显式化，而不是用技术完成度替代市场验证。

---

# 1｜Research Questions

## Customer problem
1. 多会话 continuity 在目标用户痛点中排第几？
2. 用户当前为了恢复项目付出多少时间和认知成本？
3. 错误 Current / wrong artifact / repeated prompting 的真实代价是什么？
4. 用户最希望 AI 主动做什么？
5. 哪类 AI 行为最容易造成失控感？

## Product value
6. Resume Snapshot 是否显著减少重新解释？
7. Human stop 是否发生在用户认为“该停”的位置？
8. Material alternatives 是否比普通 AI variations 更有决策价值？
9. Readback 是否提高信任，还是只增加延迟？
10. Design Map / relation semantics 是否产生价值还是维护负担？

## Adoption
11. 用户愿意把 OLEANDER 放到哪个现有工作流旁边？
12. Chat-first、desktop workspace、browser workspace 哪个最自然？
13. 用户愿意导入哪些项目数据？
14. 哪些数据绝不愿交给系统？

## Business
15. 谁是 user、buyer、approver？
16. 价值更像 individual productivity、design quality、risk reduction 还是 team continuity？
17. 付费单位更可能是 seat、project、usage 还是 organization？
18. 哪类项目具有最高 willingness-to-pay？

---

# 2｜Segmentation Hypotheses

## Segment A — Independent / Lead Designer
High-frequency AI use, multi-day project, self-owned decision process.

**Why first**
- access to complete workflow；
- fewer organization dependencies；
- can test continuity quickly。

## Segment B — Small Design Team
Designer + reviewer / collaborator.

**Why second**
- tests handoff and shared truth；
- higher coordination value。

## Segment C — Professional Multidisciplinary Team
Architecture / engineering / specialist or product / engineering / research.

**Why later**
- high value；
- high authority/security/integration complexity。

## Segment D — Enterprise Design Organization
Potential high willingness-to-pay but requires:
- admin；
- security；
- governance；
- support；
- procurement；
- compliance。

Not initial validation target.

---

# 3｜Recruitment Screener

Candidate qualifies when most are true:
- active professional design work；
- project normally lasts >1 day；
- uses AI repeatedly；
- works with multiple artifacts/revisions；
- has experienced “AI forgot where we were”；
- can show a real non-confidential or consented project；
- owns or materially contributes to design decisions；
- willing to resume same project in later session。

Exclude from core study:
- one-shot image generation only；
- casual AI usage；
- no editable artifact；
- purely administrative PM use case。

---

# 4｜Research Program

## R1 Problem Interviews
Goal: validate pain before showing product.

Capture:
- recent concrete example
- current workaround
- frequency
- consequence
- emotional / cognitive cost
- existing tools
- what user already tried

Evidence label:
`USER_REPORTED`

## R2 Workflow Observation
Observe:
- reopen project
- find Current
- identify next step
- use AI
- switch tools
- compare versions

Evidence:
`OBSERVED`

## R3 Concept Test
Show:
- Resume Snapshot
- Current Question
- Next Action
- Human stop example
- Readback example

Ask:
- what do you think this does?
- what feels useful?
- what feels like admin?
- what would you remove?

## R4 Task-based Prototype
User performs:
- resume
- explore
- compare
- steer
- readback
- continue

Measure metrics defined in Metrics Plan.

## R5 Longitudinal Pilot
Same user / same project across multiple days.

This is required before claiming continuity value.

---

# 5｜Interview Guide

Do not lead with “Do you want better continuity?”

Ask:
1. Tell me about the last complex project where you used AI repeatedly.
2. What happened when you returned the next day?
3. How did you know which output/version was current?
4. When did AI do too little?
5. When did AI do too much?
6. Tell me about a time AI said something was done but you still had to check.
7. How do you compare alternatives today?
8. What happens to rejected ideas?
9. How do you work with real CAD/Figma/code/model artifacts?
10. What would make you stop trusting an AI collaborator?

Then test product concept.

---

# 6｜Evidence Repository Structure

Every research finding should preserve:
- participant / anonymized ID
- segment
- project context
- observation vs report
- raw note / clip ref
- synthesized finding
- confidence
- counterevidence
- affected product assumption
- decision consequence

Do not store unsupported “persona truths” as facts.

---

# 7｜Competitive / Alternative Analysis Plan

Initial comparison categories:
- General AI Chat
- AI coding / agent workspace
- Design authoring AI
- Project / task management
- Knowledge / documentation
- Workflow automation
- Version / file management

For each evaluate:
- project continuity
- explicit Current
- artifact identity
- Human authority
- reversible autonomy
- option comparison
- readback
- cross-tool support
- professional boundaries
- team handoff

Named competitor claims require fresh source verification before publication.

---

# 8｜Business Validation

Do not estimate TAM/SAM/SOM without sourced market data.

First validate:
- frequency of problem
- severity
- repeat usage
- retention intent
- willingness to switch
- willingness to pay
- buyer/user mismatch
- security procurement barriers
- implementation/support cost

Only then build market sizing.

---

# 9｜Research Decision Gates

## Problem validated
Multiple independent users describe continuity/control/reality problems without prompting.

## Solution signal
Users complete core workflow and prefer it over current workaround on defined tasks.

## Retention signal
Users voluntarily return to same project/workflow.

## Business signal
At least some target users/buyers express concrete willingness to pay or adopt under specified conditions.

No single interview can close these gates.