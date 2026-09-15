# OLEANDER Typed System Third-Pass Priority Gaps v0.1

Status: **DRAFT POST-REPLAY PRIORITY MAP / NOT CURRENT**.

This document defines the remaining refinement order after:

- P0–P11 first-pass semantic contracts;
- P1–P11 second-pass executable matrices;
- unified validator contract/rule registry;
- KH46 real-project replay for P0–P8;
- OLEANDER Knowledge corpus replay for P9/P11;
- C04 Qingjiang presentation replay for P10.

Core rule:

`NO MORE TAXONOMY EXPANSION UNTIL REPLAY/EXECUTION EXPOSES A REAL SEMANTIC GAP`.

---

## 1. Current maturity by priority

| Priority | Current maturity | Remaining risk |
|---|---|---|
| P0 Identity/Plane | replay-confirmed in KH46 + corpus contexts | needs explicit collision/merge replay across two systems |
| P1 Authority/Scope | replay-confirmed bounded | needs executable authority resolution engine |
| P2 Project State/Decision | replay-confirmed bounded | needs cross-workstream live concurrency replay |
| P3 Requirement/Claim | partially replayed | KH46 legacy source did not expose complete typed Requirement set; needs a requirement-rich replay |
| P4 Interface/Variable | replay-confirmed with dimensional acceptance delta | needs second-domain interface replay outside architecture |
| P5 Baseline/Change | replay-confirmed with derivative-staleness delta | needs rollback/branch/concurrent-change replay with real records |
| P6 Evidence/Assurance | replay-confirmed with aggregation delta | needs actual uncertainty-bound quantitative replay and independent-review case |
| P7 R/I/A/U | replay-confirmed bounded | needs real explicit Risk→Issue and Unknown→Assumption transitions |
| P8 Work/Artifact | replay-confirmed with over-objectification control | needs actual cross-software handoff/loss replay |
| P9 Knowledge Admission | corpus replay-confirmed with lifecycle deltas | needs one full G9 candidate carried through existing-owner comparison and professional content gates |
| P10 Presentation | target-condition replay-confirmed with asset/medium/style deltas | needs target readback implementation against live desktop/mobile/video states |
| P11 Retrieval/Reader | replay-confirmed with badge/census/pool deltas | needs executable retrieval prototype/replay rather than document-only behavior |

---

# 2. Third-pass refinement order

The next order is **not** P0→P11 documentation again. It is ordered by remaining untested consequence.

## TP1 — Executable validator engine

Highest priority.

Why:
- semantic contracts and rule registry now exist;
- without an executable engine, regressions remain declarative;
- human readers may still interpret the same rule differently.

Required minimum:

```text
INPUT normalized object graph/snapshot
→ resolve P0 identity/plane
→ execute rule prerequisites in priority order
→ emit PASS/FAIL/HOLD/REVIEW_SIGNAL/NOT_EVALUATED
→ preserve per-rule evidence/basis
→ short-circuit only affected scope
→ produce reopen/ceiling/promotion effects
→ output machine + human receipt
```

Do not build a monolithic opaque score.

### TP1 hard requirements

- namespaced rule IDs;
- deterministic prerequisite order;
- scoped short-circuiting;
- NOT_EVALUATED distinct from PASS;
- false-positive override only through explicit rule refinement, not manual score adjustment;
- rule receipt links to semantic owner + replay case + input facts;
- no self-award of design/professional/research/bilingual/field truth.

---

## TP2 — Schema normalization / compiler source of truth

Current machine JSONs contain repeated enums and compatibility aliases.

Before production validator code, compile a canonical schema package that references one owner per shared enum.

Examples:

- `Object Plane` owned once;
- P1 owns Mutation/RB/Claim-Ceiling;
- P4 owns Interface maturity/disposition/coupling/criticality;
- P5 owns validity disposition/change impact;
- P6 owns evidence strength/assurance type;
- P10 owns truth-risk/style roles;
- P11 owns retrieval/query-plane semantics.

Compatibility aliases such as `CLAIM → PROJECT_CLAIM`, logical `Formal Assurance` versus physical `P4 Validation`, and legacy `STALE` state must be resolved through migration mapping, not duplicate enums.

---

## TP3 — Requirement-rich real-project replay

P3 is the highest semantic area still only partially tested by KH46.

Need a real case with:

- explicit stakeholder/user/operational Needs;
- derived Requirements;
- hard Constraints;
- acceptance criteria;
- Requirement version change;
- Verification;
- product/system Validation;
- waiver/deviation if available.

Replay goal:

`Need → Requirement → Design → Verification → Validation`

without collapsing any stage.

---

## TP4 — Cross-domain Interface / Variable replay

P4 must be tested outside architecture.

Preferred real case characteristics:

- digital + service + content or product + software + physical interface;
- shared token/data/state/measurement variable;
- N-way interface;
- at least one change propagating across owners;
- acceptance dimensions beyond geometry.

Goal: prove `Controlled Variable / Interface / Material Dependency` are genuinely cross-domain and not architecture-shaped abstractions.

---

## TP5 — Configuration/change stress replay

Use a real case with:

- concurrent changes;
- branch/variant baseline;
- rollback;
- evidence carry-forward decision;
- one promotion-breaking change;
- one derivative-only change.

Goal: test P5 partial invalidation versus over-propagation.

---

## TP6 — Evidence/uncertainty stress replay

Need at least:

- quantitative threshold near uncertainty boundary;
- multiple dependent evidence sources;
- contradictory evidence;
- independent-review requirement;
- one simulation/prototype/field distinction.

Goal: prove P6 can return `INCONCLUSIVE / ACCEPTED_WITH_LIMITATIONS / HOLD` correctly instead of forcing PASS/FAIL.

---

## TP7 — R/I/A/U conversion replay

Need real transitions:

- Risk realized → Issue;
- Unknown investigated → evidence/decision;
- Unknown intentionally converted to Assumption with authority;
- Assumption refuted → reopen;
- Issue repaired → retested → closed;
- residual Risk accepted.

Goal: verify lineage and reopen behavior.

---

## TP8 — Cross-software artifact/handoff replay

Use real editable-source delivery involving at least two production surfaces.

Check:

- Source Master;
- Editable Master;
- exchange derivative;
- loss profile;
- protected properties;
- actual downstream reopen/readback;
- whether information loss requires rework or is acceptable for target role.

Goal: prove `file opens ≠ handoff valid` without making all conversions HOLD.

---

## TP9 — Full G9 candidate replay

Take one replay-derived candidate and run it end-to-end:

`Project learning → G9 candidate → existing-owner search → de-project → transfer statement → counterexample → Claim–Evidence → classification → R1/R2/K1–K5/B1/IR → candidate patch/new object decision → readback`.

Recommended first candidate:

`bounded support PASS cannot promote parent/source design authority`.

Reason: it already appeared in a real project and has cross-domain relevance.

Do not create a new Knowledge object if an existing owner can absorb it cleanly.

---

## TP10 — Presentation target-condition execution

C04 replay identified five new machine concepts:

1. semantic visual source identity;
2. semantic visual role;
3. semantic position;
4. medium-specific readback vector;
5. role-scoped Style Profile overrides under invariant axes.

Next test must run actual target-condition readbacks rather than describe them.

At minimum:

- desktop;
- mobile;
- static/PDF;
- reduced motion where motion exists;
- source/derivative trace;
- field/promotion boundary visibility.

---

## TP11 — Reader/Retrieval executable prototype

Implement a small projection layer that can answer, for the same corpus/project:

- Current project truth;
- support evidence;
- provenance/history;
- professional/content state;
- contradictions;
- dynamic census state.

Required demonstration:

`CURRENT + NOT_PROVEN_PROFESSIONAL_PASS` must render coherently.

`bounded support PASS + parent design REVISE` must render coherently.

No one-badge flattening.

---

# 3. Promotion blockers remaining after first replays

Current draft must remain non-Current while any of these remain:

1. no executable validator engine;
2. shared enum/schema duplication unresolved;
3. P3 lacks requirement-rich replay;
4. P4 lacks cross-domain replay;
5. P5 lacks real concurrency/rollback stress replay;
6. P6 lacks uncertainty/contradiction stress replay;
7. P7 lacks actual semantic conversion replay;
8. P8 lacks real cross-software loss replay;
9. no full G9 admission replay;
10. P10 medium-specific target readback not executed in this draft program;
11. P11 Reader behavior remains contract-level, not executable prototype;
12. migration impact on Current Notion/Projects schema not dry-run tested;
13. independent governance review not completed.

---

# 4. What is no longer a priority

Do **not** spend the next cycle on:

- more top-level Object Classes;
- more Knowledge Roles;
- more Style names;
- more generic relation families;
- more badges/status synonyms;
- fixed corpus counts;
- batch page generation;
- expanding P0–P11 numbering.

Those areas are already sufficiently specified for replay-driven refinement.

---

# 5. Current next action

`TP1 EXECUTABLE VALIDATOR ENGINE`.

Everything after TP1 should consume actual validator/replay output rather than manually re-interpreting contracts.

No Current promotion is authorized by this roadmap.