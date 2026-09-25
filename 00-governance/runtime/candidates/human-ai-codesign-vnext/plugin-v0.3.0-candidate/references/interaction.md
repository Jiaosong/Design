# Interaction Guide v0.2

## 1. Resolve four axes, not one intent

Every Human message may carry independent signals:

### Work intent

`START / RESUME / RECOVER / EXPLORE / WILDCARD / REVIEW / REFRAME / SAVE_ROUTE / EXPLAIN / SHOW_WORK / UNRESOLVED`.

### Mutation directive

`NORMAL / READ_ONLY / AUTO_ADVANCE_REVERSIBLE`.

### Support mode

`AUTO / COMPACT / EXPLAIN / OFF`.

### Human action level

`NONE / FEEDBACK_SIGNAL / ITERATION_STEER / DESIGN_DECISION / DESIGN_KEEP / PROMOTION_DECISION`.

Do not use one axis to imply another. One message may contain multiple clause-scoped Human acts; preserve them separately instead of reducing the whole message to the first/strongest verb. The Session Kernel may apply iteration steering, but `DESIGN_DECISION / DESIGN_KEEP / PROMOTION_DECISION` are route-only signals for existing OLEANDER authorities and must never become session-owned authority.

## 2. Natural-language examples

| User says | Correct projection |
| --- | --- |
| `继续 / 接着 / finish the whole task` | `RESUME`; no Human steer |
| `只读继续检查` | `RESUME + READ_ONLY`; no steer |
| `直接做，真正需要我决定时再问` | `AUTO_ADVANCE_REVERSIBLE`; stop only at a real Human boundary |
| `这个不对，太像展馆了` | `FEEDBACK_SIGNAL / NEGATIVE_STEER`; create hypotheses, no durable taste |
| `选 B` | `ITERATION_STEER / SELECT` if B is resolvable |
| `保留 A，结合 B` | `ITERATION_STEER / MIX` only if both parents resolve |
| `不要 A，保留 B，结合 C` | two acts: `REJECT A` + `MIX B,C`; preserve clause scope and lineage |
| `就按这个` | SELECT only if one active object is unambiguous; otherwise ask one minimum referent question |
| `这个决定先暂缓` | DEFER only if one pending decision is resolvable; dependent work HOLD, unrelated reversible work may continue |
| `Design decision: select B` | Preserve as `DESIGN_DECISION`; route to existing project-decision authority; do not apply as session branch mutation |
| `DESIGN KEEP B` | Preserve as `DESIGN_KEEP`; route to existing design-review authority; does not imply Current or promotion |
| `Promote B to Current` | Preserve as `PROMOTION_DECISION`; route to existing promotion authority; Session Kernel does not promote |
| `少解释` | `COMPACT`; no authority change |
| `教我怎么看` | `EXPLAIN`; one distinction + at most one transfer question |

## 3. Proposal before preference questionnaire

When useful alternatives can expose the missing decision, do not ask the Human to pre-author every style/form/layout/execution parameter.

`OUTCOME / DISCOMFORT → CAUSAL HYPOTHESES → MATERIAL OPTIONS → EDITABLE/REAL ARTIFACT → READBACK → HUMAN STEER`.

## 4. Human stop test

Ask/route only when the kernel computes one of these facts as true:

- a consequential steer has ambiguous referent;
- comparable actual artifacts expose a value-dependent choice;
- authority/scope escalation needs Human authorization;
- an irreversible/publishing side effect is next;
- specialist/independent review is required;
- multi-Human decision rights conflict;
- no truthful editable/native substitute can answer the key unknown;
- requested scope is complete or the user asks to stop.

Do not stop because one tool call completed.

Consequential referents must resolve from display label to `ref + kind + revision + lineage_ref` before they can be applied. A branch may also carry `decision_object_ref` where needed to prove it belongs to the current pending decision. Single-letter option labels are case-sensitive aliases; incidental English `a` is not option A. A short alias is usable only when it resolves to exactly one active option; collisions fail closed. Multiple distinct consequential actions against the same referent require clarification unless an explicit sequential-action grammar is defined.

## 5. Designer development

Default `AUTO`. Unsolicited maximum per material round: one insertion.

`关键差异 → 为什么改变这个设计 → 至多一个迁移问题`.

Use `COMPACT/OFF` when requested. Fade only from current-session evidence or explicit instruction; do not persist a skill/taste score.

## 6. Multiple Humans

Designer, client, specialist, independent reviewer, project authority and promotion authority have scoped rights. Message recency is never universal precedence. Route conflicts through existing owner rules.
