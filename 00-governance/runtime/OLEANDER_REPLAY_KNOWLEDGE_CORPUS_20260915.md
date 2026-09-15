# OLEANDER Knowledge Corpus Replay — 2026-09-15

Status: **DRAFT KNOWLEDGE/RETRIEVAL REPLAY / NOT CURRENT**.

Purpose: test P9 Knowledge Admission and P11 Retrieval/Reader semantics against the live OLEANDER knowledge-governance program, especially dynamic corpus enumeration, CURRENT/SUPPORT/PROVENANCE separation, graph/content independence, full-body review, bilingual/research gates and migration debt.

This replay does not change Notion/D1/canonical Knowledge objects. It uses the latest known audit state and treats corpus counts as time-scoped census facts only.

---

## 1. Replay snapshot

As-of snapshot used for replay:

- `CURRENT = 56`
- `SUPPORT = 946`
- `PROVENANCE = 213`
- `TOTAL = 1215`

Hard boundary:

`1215 = current census snapshot`, not corpus ceiling, migration denominator for all future time, or completion target embedded in schema.

Content-review evidence snapshot:

- `FULL_BODY_REVIEW_EVIDENCE = 590`
- `GRAPH_ONLY = 412`
- `LINEAGE_ONLY = 213`

Graph-only or lineage-only evidence cannot establish professional content completion.

Current user authority for remediation:

- old Content Review KEEP is invalid as proof of current professional pass;
- all objects are treated as `NOT_PROVEN_PROFESSIONAL_PASS` until reassessed under the integrated professional content/research contract;
- canonical full body must be read page-by-page;
- classification/title/graph state cannot substitute for content review;
- content remediation includes actual research, canonical body strengthening, bilingual parity, claim/evidence boundary, freshness/version handling and independent review;
- execution order for the current snapshot is `CURRENT 56 → SUPPORT 946 → PROVENANCE 213`;
- this order is a current migration/review strategy, not a permanent ontology rule.

Recent audit evidence also shows that 18/18 reviewed CURRENT objects had complete/untruncated body readback and revision/SHA matches, yet `B1 = REVISE` and `IR = HOLD` for all 18, with `exactSafePatchCandidates = 0` in that review slice.

This is a strong real example that:

`FULL BODY READ SUCCESS ≠ BILINGUAL PASS ≠ INDEPENDENT REVIEW PASS ≠ SAFE WRITE EXISTS`.

---

# 2. P0 / identity interaction

## Confirmed

Corpus migration must operate on stable canonical identity, not page order or batch number.

A page may move:

- CURRENT → SUPPORT;
- SUPPORT → CURRENT;
- CURRENT → PROVENANCE;
- one Level/Role → another;

without becoming a new logical object solely because its classification/state changed.

## Result

`CONFIRMED`.

No new P0 semantic type required.

---

# 3. P9 — Dynamic corpus admission and remediation replay

## 3.1 Corpus census is not completion denominator

A migration/review run must bind:

```yaml
as_of:
planes:
retrieval_spaces:
enumeration_query_or_basis:
count_by_space:
selected_population_ids:
```

Completion for a run is:

`enumeration closure for scoped snapshot + per-object decision/readback`,

not:

`counter reached 1215`.

If new Current objects appear after the snapshot, they belong to a later/reopened census.

### Replay rule

`P9/CORPUS-RP01 CORPUS_COUNT_IS_A_TIME_SCOPED_CENSUS_NOT_A_SCHEMA_CEILING`.

---

## 3.2 Graph terminal and Content terminal are independent

The corpus already demonstrates objects with strong graph/identity/classification evidence but insufficient full-body professional review.

Therefore migration needs at least separate axes:

- `graph_state`;
- `content_state`;
- `research_state`;
- `bilingual_state`;
- `independent_review_state`;
- `lifecycle_current_eligibility`.

No graph terminal state may auto-fill content terminal.

### Replay rule

`P9/TERM-RP01 GRAPH_TERMINAL_CANNOT_AUTO_GRANT_CONTENT_RESEARCH_BILINGUAL_OR_IR_TERMINAL`.

---

## 3.3 Review evidence class is provenance of review depth, not truth state

`FULL_BODY_REVIEW_EVIDENCE / GRAPH_ONLY / LINEAGE_ONLY` answer:

`What kind of review evidence exists?`

They do not directly answer:

`Is the object professionally correct/current/trusted?`

Examples:

- FULL_BODY_REVIEW_EVIDENCE may still yield RESTRUCTURE/ENRICH/HOLD;
- GRAPH_ONLY may be sufficient for graph cleanup but not content completion;
- LINEAGE_ONLY may be sufficient for provenance disposition but not reusable Current content.

### Replay rule

`P9/REV-RP01 REVIEW_EVIDENCE_CLASS_MUST_NOT_BE_COLLAPSED_INTO_TRUST_OR_CONTENT_PASS`.

---

## 3.4 Prior KEEP invalidation needs lineage-safe semantics

When a new higher professional standard invalidates prior KEEP as sufficient proof, do not rewrite history as though the old review never occurred.

Represent:

```text
old review decision = historical review result
current professional eligibility = NOT_PROVEN_PROFESSIONAL_PASS
new remediation obligation = OPEN
```

Do not convert the historical KEEP into a false historical FAIL unless evidence actually shows the old review was wrong under its then-defined criteria.

### Replay rule

`P9/KEEP-RP01 STANDARD_UPGRADE_CAN_INVALIDATE_KEEP_AS_CURRENT_PROOF_WITHOUT_REWRITING_HISTORICAL_REVIEW_LINEAGE`.

---

## 3.5 Full-body readback is necessary but not sufficient

The audited 18/18 example demonstrates:

- body complete/untruncated;
- revision/hash matched;
- yet B1 remained REVISE;
- IR remained HOLD;
- no exact safe patch was available from existing evidence alone.

Therefore:

`READBACK PASS` is an admission precondition, not Content/Research/Bilingual/IR PASS.

### Replay rule

`P9/BODY-RP01 FULL_BODY_INTEGRITY_PASS_DOES_NOT_GRANT_CONTENT_RESEARCH_BILINGUAL_OR_IR_PASS`.

---

## 3.6 Safe patch availability is independent from remediation need

An object can clearly need enrichment/restructure while still having:

`exactSafePatchCandidates = 0`

because current body + existing evidence are insufficient for a safe canonical write.

This should trigger:

`EXTERNAL_RESEARCH_REQUIRED / EVIDENCE_RESOLUTION_REQUIRED`,

not forced patch generation.

### Replay rule

`P9/PATCH-RP01 REMEDIATION_REQUIRED_DOES_NOT_IMPLY_SAFE_PATCH_AVAILABLE`.

---

## 3.7 Current-first is operational priority, not quality rank

The current migration order prioritizes CURRENT 56 before SUPPORT/PROVENANCE because errors there have higher execution/retrieval consequence.

This does not mean:

- every CURRENT object is better researched;
- CURRENT implies VERIFIED;
- SUPPORT is lower quality;
- PROVENANCE is unimportant.

### Replay rule

`P9/PRI-RP01 CURRENT_FIRST_REMEDIATION_IS_RISK_PRIORITY_NOT_TRUTH_OR_QUALITY_RANK`.

---

# 4. P11 — Retrieval/Reader replay

## 4.1 CURRENT object may still be professionally unproven

Reader must be able to show simultaneously:

```text
Retrieval Space = CURRENT
Search Eligibility = DEFAULT
Content Professional Pass = NOT_PROVEN
B1 = REVISE or OPEN
IR = HOLD or OPEN
```

No single green `CURRENT` badge can imply professional completion.

### Replay rule

`P11/BADGE-RP02 CURRENT_RETRIEVAL_BADGE_CANNOT_IMPLY_CONTENT_RESEARCH_BILINGUAL_OR_IR_PASS`.

---

## 4.2 Review-depth disclosure

For maintenance/review views, Reader should expose review evidence class:

`FULL_BODY_REVIEW_EVIDENCE | GRAPH_ONLY | LINEAGE_ONLY`.

But this should not clutter normal end-user retrieval unless it materially affects answer confidence or maintenance action.

### Replay rule

`P11/VIEW-RP02 REVIEW_EVIDENCE_CLASS_VISIBLE_IN_MAINTENANCE_CONTEXT_WITHOUT_BECOMING_GENERIC_TRUTH_RANK`.

---

## 4.3 CURRENT/SUPPORT/PROVENANCE remain separate pools

Current replay confirms:

- CURRENT first for default authoritative retrieval;
- SUPPORT expands when needed;
- PROVENANCE activates for history/lineage/conflict;
- no undifferentiated ranking pool.

However a stale/unproven CURRENT object may need a bounded answer with Support evidence, not silent replacement.

### Replay rule

`P11/POOL-RP02 SUPPORT_MAY_BOUND_OR_CHALLENGE_CURRENT_WITH_DISCLOSURE_BUT_CANNOT_SILENTLY_REPLACE_CURRENT_IDENTITY`.

---

## 4.4 Dynamic census visibility

A Reader/maintenance dashboard displaying corpus totals must show:

`as_of + retrieval-space scope + enumeration basis`.

A naked `1215 total` should be treated as incomplete metadata because the number will change.

### Replay rule

`P11/CENSUS-RP01 CORPUS_COUNT_DISPLAY_REQUIRES_AS_OF_SCOPE_AND_ENUMERATION_BASIS`.

---

# 5. Migration semantics replay

The current corpus demonstrates three independent kinds of debt:

1. **classification/graph debt**;
2. **content/research debt**;
3. **migration/field-population debt**.

They must not be conflated.

For example:

- missing new v1.0 field does not prove old body is professionally wrong;
- graph clean does not prove body is professionally adequate;
- body professionally strong does not prove all migration metadata is complete.

### Replay rule

`INT/RP03 GRAPH_DEBT_CONTENT_DEBT_AND_MIGRATION_DEBT_MUST_REMAIN_SEPARATE`.

---

# 6. Over-modeling checks

The replay warns against three over-modeling patterns.

### A. One review row per gate per historical run forever
Keep historical detail where material, but summarize non-material repeated machine checks through receipts/provenance rather than exploding canonical Knowledge objects.

### B. Turning every Claim into a standalone page
Claim should usually be addressable within the canonical Knowledge object/ledger unless it has independent lifecycle/reuse responsibility.

### C. Turning batch numbers into identity
`CURRENT 31–40` is an execution slice, not taxonomy, object identity or permanent collection.

---

# 7. Replay findings

## Confirmed model strengths

- dynamic corpus concept works;
- CURRENT/SUPPORT/PROVENANCE separation works;
- full-body review requirement is necessary;
- independent content/research/bilingual/IR states are justified by real audit results;
- existing-owner-first remains compatible with remediation;
- no fixed 1215 denominator should exist.

## Required refinements

1. Add explicit **review evidence class** separate from Trust/Content.
2. Add lineage-safe handling for prior KEEP invalidated by a standard upgrade.
3. Add `SAFE_PATCH_AVAILABLE` as independent remediation capability state.
4. Reader must support `CURRENT + NOT_PROVEN_PROFESSIONAL_PASS` without semantic contradiction.
5. Maintenance/census views require `as_of/scope/enumeration basis`.
6. Keep graph/content/migration debt independent.

---

# 8. Replay disposition

`P9 KNOWLEDGE CORPUS REPLAY = FIRST_PASS_COMPLETE_WITH_DELTAS`.

`P11 KNOWLEDGE READER REPLAY = FIRST_PASS_COMPLETE_WITH_DELTAS`.

No Knowledge object is promoted or modified by this replay.

Next replay priority after compiling these deltas is P10 target-condition presentation replay.