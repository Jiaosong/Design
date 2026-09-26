# OLEANDER Requirement Delta v0.3.2

[← v0.3 Package](README.md) · [← Master PRD](OLEANDER_MASTER_PRD_v0.3.0.md)

**State:** `WORKING CONTENT DELTA / NON-AUTHORITY`
**Purpose:** 定义 v0.3.2 内容审查后新增的产品需求。v0.2 Feature Specs 继续作为既有详细 baseline，本文件只记录新增/改变的产品行为，不回写历史版本。

---

# 1｜Why this delta exists

内容审查发现 OLEANDER 已经较强地解决 continuity / authority / readback / evidence，但仍需要加强真正的 **co-design capability**：

```text
Design Situation
→ Search Space
→ AI Triage
→ Compare / Persistent Decision
→ Develop / Synthesize
→ Artifact Action
→ Readback
→ Whole-design Check
```

---

# 2｜New / Changed Requirements

| ID | Priority | Requirement | Primary node |
|---|---|---|---|
| FOCUS-F10 | P0 | 新项目或重大 brief 变化必须先形成 Design Situation；Problem 只是 problem/opportunity/ambition/requirement/conflict/unknown 中的一种 framing | N02G |
| EXP-F10 | P0 | Human review 前，AI 应对候选执行 bounded triage：去重、硬约束淘汰、弱证据标记、保留真实 value trade-off | N03A7 |
| SYN-F08 | P0 | AI 可以从多个有效分支/证据/约束形成新的 coherent synthesis，并说明 inherited / transformed / new / discarded / unresolved | N03C3 |
| CMP-F12 | P0 | consequential steer 必须形成或更新 persistent Design Decision object，而不是只存在于 session event/history | N04E |
| ART-F13 | P0 | material artifact action 必须绑定 target/revision、intended delta、actual delta、rollback/recovery（如适用）和 readback | N06G |

---

# 3｜Changed Semantics

## CONTINUE / RESUME / RECOVER

- RESUME = interaction context 丢失后从 owner-native carriers 恢复；
- CONTINUE = 当前有效 session/frontier 沿已授权路径继续；
- RECOVER = failure / partial execution / state conflict 后恢复。

`继续` 不再无条件等于 RESUME。

## Action Guard

原 Mutation Guard 扩展为产品层 **Action Guard**：
- write / mutation；
- sensitive external read / disclosure；
- publish / irreversible external action；
- material cost；
- blast radius / recoverability。

Mutation Guard 可继续作为 write-specific runtime subcheck / migration term。

## Validation

Validation 不再是有/无代表性真实使用的二元状态；按 V0 Analytical → V5 Post-use/Longitudinal 声明实际证据级别，claim ceiling 不得超过实际 level。

## Claim Ceiling

- N06E = artifact-side Fidelity Ceiling；
- N08E = evidence/applicability-side Claim Ceiling；
- effective claim ceiling 取与当前 claim 相关的更严格限制，而不是两套互相竞争的最终结论。

---

# 4｜Does not change authority

本 delta 不创建：
- Project State；
- Current；
- Design KEEP；
- professional PASS；
- Promotion；
- artifact native authority。

它只修订产品行为定义，等待后续系统/runtime 对照落地。

---

# 5｜System Alignment Checklist

> 本表是下一轮系统修订的 product-side contract，不代表当前 runtime 已完成。

| Alignment ID | Product content now requires | System / runtime next proof | Status |
|---|---|---|---|
| SA-01 | RESUME ≠ CONTINUE ≠ RECOVER | fixture proves current-session “继续” does not force full resume; interrupted work resolves RECOVER correctly | `OPEN_SYSTEM_ALIGNMENT` |
| SA-02 | Design Situation / Brief supports problem / opportunity / ambition / requirement / conflict / unknown | new-project path can frame without manufacturing a Problem | `OPEN_SYSTEM_ALIGNMENT` |
| SA-03 | Search-space Map before premature convergence | runtime can represent covered / uncovered / intentionally excluded / unknown exploration regions | `OPEN_SYSTEM_ALIGNMENT` |
| SA-04 | AI Option Triage is reversible presentation triage, not Human REJECT | weak/duplicate options can be hidden from default review while lineage remains recoverable and Project Current unchanged | `OPEN_SYSTEM_ALIGNMENT` |
| SA-05 | Design Synthesis creates new coherent lineage | synthesis fixture proves inherited / transformed / new / discarded / unresolved fields and a new branch identity | `OPEN_SYSTEM_ALIGNMENT` |
| SA-06 | Persistent Design Decision | consequential Human steer creates/updates decision object with actor, rights, rationale when supplied, trade-offs, status, reopen and supersession | `OPEN_SYSTEM_ALIGNMENT` |
| SA-07 | Artifact Action owns intended vs actual delta | real authoring trial binds target revision, intended delta, actual delta, new revision, readback and rollback/recovery when available | `OPEN_SYSTEM_ALIGNMENT` |
| SA-08 | Whole-design Check after material local development | fixture detects a local improvement that causes a whole-design regression and scopes only affected work | `OPEN_SYSTEM_ALIGNMENT` |
| SA-09 | Action Guard is broader than write guard | tests cover write, sensitive external read/disclosure, publish, provider boundary, cost and blast-radius escalation | `OPEN_SYSTEM_ALIGNMENT` |
| SA-10 | Validation evidence levels V0–V5 | system records achieved level + does-not-prove without creating universal professional stages | `OPEN_SYSTEM_ALIGNMENT` |
| SA-11 | Artifact Fidelity Ceiling + Evidence Claim Ceiling compose | claim output uses the stricter applicable boundary without duplicating competing final ceilings | `OPEN_SYSTEM_ALIGNMENT` |
| SA-12 | Designer Development without profiling | support/explanation can adapt session-locally; no durable taste/competence/psychological profile is written from ordinary steering | `OPEN_SYSTEM_ALIGNMENT` |
| SA-13 | VPCR + DRPR outcome pair | telemetry/eval can distinguish correct continuation from actual design-resolution progress; safe HOLD/DEFER is not penalized | `OPEN_SYSTEM_ALIGNMENT` |

## Alignment closure rule

An item may move out of `OPEN_SYSTEM_ALIGNMENT` only when:
1. the actual current system path is identified；
2. implementation/change is reviewable；
3. matching fixture or real-artifact evidence exists；
4. readback proves the intended behaviour；
5. no Project State / professional / Promotion authority is silently moved。
