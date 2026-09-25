# OLEANDER PRD Feature Spec｜SESSION KERNEL + CONTINUITY v0.2.0

[← Feature Specs](README.md) · [← Master PRD](../OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

**Scope:** Resume、intent parsing、mutation directive、support mode、Human action level、steering、Human stop、mutation guard、decision rights、plugin-off survival、closure。  
**State:** WORKING PRODUCT SPEC / NON-AUTHORITY.

---

# 1｜Product Role

Human–AI Co-Design Session Kernel 是 OLEANDER 的跨产品交互层。

它负责：

- 理解用户当前想做什么；
- 恢复 owner-native project frontier；
- 决定当前 interaction 是否可自动继续；
- 识别 Human feedback 与真正 steering；
- 在 consequence / authority / reversibility 边界上停止；
- 保护 referent、branch lineage、readback 与 continuation。

它不拥有：

- Project State；
- Project / Source / Current Authority；
- checkpoint database；
- artifact registry；
- professional process；
- independent review；
- persistence authority；
- Promotion。

---

# 2｜Four-axis Input Model

每条 Human message 独立解析四个轴。

## INT-F01｜Work Intent

Allowed values：

- START
- RESUME
- RECOVER
- EXPLORE
- WILDCARD
- REVIEW
- REFRAME
- SAVE_ROUTE
- EXPLAIN
- SHOW_WORK
- UNRESOLVED

**Requirement**
Work Intent 只表示用户希望完成的工作，不自动授予 mutation 权限或 design authority。

**Acceptance**
“继续并完成” = RESUME，不得自动生成 SELECT / DEFER。

**Priority** P0

---

## INT-F02｜Mutation Directive

Allowed values：
- NORMAL
- READ_ONLY
- AUTO_ADVANCE_REVERSIBLE

**Acceptance**
“只读继续检查”必须同时成为：
- RESUME
- READ_ONLY
- no steer

**READ_ONLY hard behaviour**
- zero project mutation；
- zero external write；
- can inspect / compare / report；
- can form candidate analysis without writing owner-native state。

**Priority** P0

---

## INT-F03｜Support Mode

Allowed：
- AUTO
- COMPACT
- EXPLAIN
- OFF

**Rule**
Support Mode 只影响解释与 designer-development 展示，不影响 authority、permission、maturity 或 competence status。

**Acceptance**
“少解释”不能降低 verification / guard 强度。

**Priority** P1

---

## INT-F04｜Human Action Level

Allowed：
- NONE
- FEEDBACK_SIGNAL
- ITERATION_STEER
- DESIGN_DECISION
- DESIGN_KEEP
- PROMOTION_DECISION

**Hard separation**

```text
FEEDBACK_SIGNAL ≠ ITERATION_STEER
ITERATION_STEER ≠ DESIGN_DECISION
DESIGN_DECISION ≠ DESIGN_KEEP
DESIGN_KEEP ≠ PROMOTION_DECISION
```

**Routing**
- FEEDBACK_SIGNAL：session may interpret as design input；
- ITERATION_STEER：session may apply to option branch when valid；
- DESIGN_DECISION：route to existing project-decision authority；
- DESIGN_KEEP：route to design-review authority；
- PROMOTION_DECISION：route to Promotion authority。

**Priority** P0

---

# 3｜Human Feedback vs Steering

## INT-F05｜Affective Feedback

Examples：
- “这个不对”
- “太像展馆”
- “太重了”
- “感觉不够开放”

**System behaviour**
1. preserve raw feedback；
2. generate multiple causal hypotheses；
3. do not create durable taste profile；
4. create materially different repair directions if useful；
5. ask Human to steer only after differences are visible。

**Priority** P0

---

## INT-F06｜Iteration Steer Actions

Allowed：
- SELECT
- MODIFY
- MIX
- REJECT
- REOPEN
- DEFER

**Priority** P0

---

# 4｜Referent Resolution

## INT-F07｜Explicit Referent Binding

Consequential steer 必须解析：

```text
REF
+ KIND
+ REVISION
+ LINEAGE_REF
(+ DECISION_OBJECT_REF if needed)
```

**Acceptance**
Display alias A/B/C 只是人机界面标签，mutation/readback proof 必须绑定 owner-native option/object revision。

**Priority** P0

---

## INT-F08｜Ambiguous Referent

**Example**
“就这个”同时有两个 active objects。

**Required behaviour**
- no mutation；
- ask one minimum clarification；
- preserve all current options；
- do not expand into long questionnaire。

**Event**
`ambiguity_clarification_requested`

**Priority** P0

---

## INT-F09｜Alias Collision Protection

Single-letter alias 必须作为显式 label 处理。

**Acceptance**
英文自然语言中的 “a” 不得误绑 option A。

**Priority** P0

---

## INT-F10｜Compound Human Actions

One message 可以包含多个 clause-scoped acts。

**Example**
“不要 A，保留 B，结合 C。”

Possible projection：
- REJECT A
- MIX B,C

**Rule**
不能取“最强动作”把整句压成一个 action。

**Priority** P0

---

## INT-F11｜Conflicting Actions

如果同一 referent 同时收到互相冲突的 consequential actions，而用户未给 explicit sequence：

- fail closed；
- ask minimum clarification；
- no mutation。

**Priority** P0

---

# 5｜Branch Lineage

## INT-F12｜Parent Preservation

SELECT / MODIFY / MIX 必须保留 parent refs。

MIX 必须至少两个 resolvable parents。

**Priority** P0

---

## INT-F13｜Reject Preservation

REJECTED branch：
- 不再 active；
- 不删除；
- 保留 reason if Human provided；
- 允许未来 REOPEN。

**Priority** P0

---

## INT-F14｜Defer Preservation

DEFER：
- requires current pending decision；
- branch / decision remains available；
- dependent mutation HOLD；
- unrelated reversible work may continue；
- normally no design delta。

**Priority** P0

---

## INT-F15｜Reopen

REOPEN：
- restores existing branch；
- preserves original lineage；
- does not create duplicate branch unless content materially changes。

**Priority** P1

---

# 6｜Auto-advance

## INT-F16｜Reversible Auto-advance

系统默认不因每次 tool call 停止。

Side-effect classes：

1. NONE
2. REVERSIBLE_LOCAL
3. PROJECT_MUTATION_REVERSIBLE
4. PROJECT_MUTATION_AUTHORITY_SENSITIVE
5. EXTERNAL_IRREVERSIBLE_OR_PUBLISHING

**Default**
- NONE / REVERSIBLE_LOCAL → continue；
- PROJECT_MUTATION_REVERSIBLE → only if owner rules permit；
- authority-sensitive / irreversible / publishing → stop / route authorization。

**Priority** P0

---

# 7｜Human Stop

## INT-F17｜Computed Human Stop

Human stop 必须由 projected facts 计算，而不是 caller 提前给一个 `STOP=true`。

Stop reasons：
- ambiguous consequential referent；
- comparable actual artifacts expose value choice；
- authority escalation；
- irreversible/publish next；
- specialist/independent review；
- multi-human decision-right conflict；
- no truthful editable/native substitute；
- scope complete；
- explicit user stop。

**Acceptance**
一个普通 tool success 不得触发 Human stop。

**Priority** P0

---

# 8｜Mutation Guard

## INT-F18｜Pre-write Freshness

Material project write 前必须重新读取 owner-native carrier。

Minimum projected facts：
- logical object identity
- authority revision
- source revision
- expected checkpoint sequence
- observed checkpoint sequence
- owner permission
- native target
- side-effect class
- decision-rights status
- active user constraints
- resolver provenance
- actual carrier readback status

**Acceptance**
stale cache / caller-supplied ALLOW / old permission summary 不足以 authorize write。

**Priority** P0

---

## INT-F19｜Stale Write Block

If:
- authority stale
- source stale
- checkpoint mismatch
- decision rights unclear
- active constraints missing

Then：
- HOLD affected mutation；
- revalidate；
- unrelated reversible exploration may continue。

**Priority** P0

---

## INT-F20｜READ_ONLY Guard

READ_ONLY directive always wins over ordinary auto-advance.

**Acceptance**
No owner-native mutation or external side effect occurs during READ_ONLY session.

**Priority** P0

---

# 9｜Human-steered Second Round

## INT-F21｜Second-round Delta Proof

Truthful Human-feedback second-round claim requires：

```text
EXPLICIT HUMAN SOURCE
→ HASH / REVISION-BOUND DECISION RIGHTS PROOF
→ OWNER RULE REVISION
→ TYPED + REVISIONED REFERENT
→ EDITABLE / NATIVE DELTA REVISION
→ ACTUAL READBACK OF SAME REVISION + CONTENT HASH
→ INVARIANT-SPECIFIC READBACK
```

**Not sufficient**
- pre-steer autonomous probe；
- textual acknowledgement；
- generated artifact without readback；
- same filename；
- same revision string with different content；
- generic owner-rule string；
- unrelated readback。

**Priority** P0

---

## INT-F22｜Preserved Invariants

Second round records：
- changed variables
- preserved invariants

Readback must explicitly verify claimed preserved invariants.

**Priority** P0

---

# 10｜Multi-human Decision Rights

## PEO-F01｜Actor Role

Potential roles：
- DESIGNER
- CLIENT_OR_STAKEHOLDER
- SPECIALIST
- INDEPENDENT_REVIEWER
- PROJECT_AUTHORITY
- PROMOTION_AUTHORITY

**Priority** P1

---

## PEO-F02｜Scoped Rights

Latest message is never universal authority.

Examples：
- Designer can steer design but cannot waive statutory truth；
- Client can change value priority but not manufacture specialist compliance；
- Specialist owns domain claim, not whole design；
- Reviewer does not become producer authority；
- Promotion authority is explicit。

**Priority** P0

---

## PEO-F03｜Conflict Hold

Conflict only HOLDs affected effect.

Unrelated reversible work may continue.

**Priority** P1

---

# 11｜Designer Development

## INT-F23｜Support Insertion

Default AUTO。

Maximum unsolicited support per material round：

```text
ONE KEY DISTINCTION
→ WHY IT CHANGES THIS DESIGN
→ AT MOST ONE TRANSFER QUESTION
```

**Priority** P1

---

## INT-F24｜Support Fade

Fade only if：
- user explicitly asks for less；
- current session shows repeated clear judgment on same distinction。

Do not persist as:
- competence score；
- psychological profile；
- durable taste profile。

**Priority** P1

---

# 12｜Continuity

## INT-F25｜Resume Precedence

Resume order：

```text
explicit project/task/object key
→ Current Project / Task
→ Control Card
→ Execution Receipt / checkpoint
→ actual native artifact + readback
```

Chat memory is not authority.

**Priority** P0

---

## INT-F26｜Ephemeral Session Context

Session context may cache locators / projections, but：
- may disappear；
- must not become plugin-owned project truth；
- must reconstruct from Current carrier next session。

**Priority** P0

---

## INT-F27｜Plugin-off Survival

After plugin/session UI removal：
- Current Project State remains；
- checkpoint remains；
- native artifacts remain；
- authority remains；
- resume path still exists。

**Verification**
real destructive uninstall / replacement test required for full claim。

**Priority** P1

---

# 13｜Domain Adapter

## INT-F28｜Domain-native Process

Shared interaction model may span domains, but professional process stays native.

Adapter fields：
- domain_id
- process status
- process_ref
- current domain question
- native output roles
- readback methods
- claim ceiling
- HOLD conditions

**Acceptance**
OPEN professional process cannot award professional PASS.

**Priority** P0

---

# 14｜Closure

## INT-F29｜Separated Closure Dimensions

Every material session closes with separate dimensions：

- SESSION_RESULT
- DESIGN_CANDIDATE
- PROFESSIONAL_STATE
- REVIEW_STATE
- PERSISTENCE_STATE
- PROMOTION_STATE

**Acceptance**
No single synthetic PASS may collapse these dimensions.

**Priority** P0

---

# 15｜Key Acceptance Scenarios

## SK-A01 Continue
Input：`继续`  
Expected：RESUME / no steer / next allowed reversible action.

## SK-A02 Read-only continue
Input：`只读继续检查`  
Expected：RESUME + READ_ONLY / zero mutation.

## SK-A03 Auto advance
Input：`直接做，真正需要我决定时再问`  
Expected：AUTO_ADVANCE_REVERSIBLE until real Human boundary.

## SK-A04 Negative steer
Input：`这个不对，太像展馆了`  
Expected：FEEDBACK_SIGNAL / causal hypotheses / no durable taste.

## SK-A05 Explicit select
Input：`选 B`  
Expected：SELECT only when B resolves exact revision.

## SK-A06 Ambiguous select
Input：`就这个` with 2 active objects  
Expected：minimum clarification / no mutation.

## SK-A07 Mix
Input：`保留 A 的操作逻辑，结合 B 的空间关系`  
Expected：MIX A,B / both parent refs.

## SK-A08 Compound
Input：`不要 A，保留 B，结合 C`  
Expected：clause-scoped REJECT + MIX if referents resolve.

## SK-A09 Defer
Input：`这个决定先放着`  
Expected：DEFER only if current pending decision exists.

## SK-A10 Stale checkpoint
Expected：write blocked / revalidate / valid reversible work preserved.

## SK-A11 Publish
Expected：Human authorization required.

## SK-A12 Multi-human conflict
Expected：scoped conflict HOLD / no universal latest-message authority.

## SK-A13 Plugin off
Expected：reconstruct session from owner-native carriers.

---

# 16｜Events

- `interaction_axes_resolved`
- `human_feedback_received`
- `human_action_compound_parsed`
- `human_steer_bound`
- `referent_ambiguity_detected`
- `human_stop_triggered`
- `auto_advance_continued`
- `mutation_guard_checked`
- `mutation_guard_blocked`
- `decision_rights_conflict`
- `second_round_started`
- `second_round_completed`
- `session_context_reconstructed`
- `plugin_off_resume_attempted`
- `closure_reported`

---

# 17｜Metrics

- False Steering Rate
- Ambiguous Referent Safe-stop Rate
- Unnecessary Human Stop Rate
- Useful Autonomy Rate
- Unauthorized Action Rate
- Stale Mutation Prevention Rate
- Compound Action Preservation Rate
- Second-round Fidelity
- Plugin-off Resume Success Rate
- Multi-human Conflict Containment Rate
- Explanation Interruption Rate

Targets：
- Unauthorized Action Rate = 0
- AI-owned Design KEEP = 0
- AI-owned Promotion = 0
- READ_ONLY mutation = 0

---

# 18｜Verification

必须组合：
- deterministic TEST；
- real artifact DEMO；
- real Human steering；
- cross-session PROJECT_EXERCISE；
- destructive plugin-off test；
- multi-human scenario；
- at least two domain-native process scenarios。

Machine fixture PASS only validates reference-kernel semantics，不等于产品 UX / professional / external-user validation。
