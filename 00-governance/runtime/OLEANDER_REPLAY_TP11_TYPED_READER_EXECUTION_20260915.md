# OLEANDER TP11 Executable Reader Replay — 2026-09-15

Status: **DRAFT EXECUTION REPLAY / NOT CURRENT**.

Purpose: prove that the Reader can project independent OLEANDER state axes without synthesizing a false single project/knowledge PASS badge.

Executable assets:

- `render_typed_reader.py`
- `test_typed_reader.py`
- `OLEANDER_TYPED_READER_FIXTURES_v0.1.json`

The Reader is deliberately a **projection/routing layer**, not a truth engine. It must not promote, reclassify or aggregate away source states.

---

# 1. Reader execution model

Current prototype flow:

```text
query plane
→ eligible object selection
→ exact ID / semantic-key resolution
→ independent state projection
→ per-target result projection
→ typed related-support traversal
→ warnings/boundaries
→ output projection
```

It does not calculate a generic quality/relevance/truth score.

Output contains:

- identity;
- plane / semantic class;
- independent state axes;
- target results;
- related bounded support;
- warning conditions;
- explicit reader boundary;
- `single_aggregate_pass_badge = false`.

---

# 2. Fixture A — CURRENT + NOT_PROVEN_PROFESSIONAL_PASS

Fixture:

`READER-FX-001-CURRENT-UNPROVEN`

Expected simultaneous output:

```text
retrieval_space = CURRENT
is_current = true
professional_state = NOT_PROVEN_PROFESSIONAL_PASS
content_state = ENRICH
bilingual_state = REVISE
independent_review_state = HOLD
allowed_use = USE_WITH_RECHECK
```

The Reader must emit:

`CURRENT_RETRIEVAL_DOES_NOT_IMPLY_PROFESSIONAL_PASS`.

### Result

`SEMANTIC PROJECTION MODEL = CONFIRMED_BY_DETERMINISTIC FIXTURE`.

### Rule

`P11/READ-RP03 READER_MUST_ALLOW_CURRENT_RETRIEVAL_IDENTITY_AND_UNPROVEN_PROFESSIONAL_CONTENT_STATE_TO_COEXIST_WITHOUT_CONTRADICTION_OR_GREEN_BADGE_FLATTENING`.

---

# 3. Fixture B — support PASS + parent design REVISE

Fixture:

`READER-FX-002-SUPPORT-PASS-PARENT-REVISE`

Parent:

```text
KH46-V008-SELECTED-A
Authority = WORKING_DESIGN_CANDIDATE_NO_PROMOTION
Design review = REVISE
G1/G2/G3/G6 = REVISE
G4/G5 = PASS
```

Related support:

```text
KH46-P37-SUPPORT-OVERLAY
Result = PASS_SUPPORT_ONLY_PROGRAM_OVERLAY
Does not establish = DESIGN_QUALITY_KEEP / PROFESSIONAL_VALIDITY / FIELD_VALIDITY / OPERATIONAL_ADJACENCY
```

The Reader must preserve both records rather than choosing a winner.

Expected warnings:

- `BOUNDED_SUPPORT_RESULT_COEXISTS_WITH_UNRESOLVED_PARENT_DESIGN_STATE`;
- `MIXED_TARGET_RESULTS_PRESERVED`.

### Result

`SCOPED RESULT PROJECTION = CONFIRMED_BY_DETERMINISTIC FIXTURE`.

### Rule

`P11/READ-RP04 READER_MUST_PROJECT_BOUNDED_SUPPORT_PASS_AND_PARENT_REVISE_AS_SEPARATE_COMPATIBLE_FACTS_AND_PRESERVE_PER_TARGET_RESULTS`.

---

# 4. Reader warning is not state mutation

Warnings such as:

- Current does not imply professional pass;
- mixed results preserved;
- bounded support coexists with unresolved parent state;

are projection annotations.

They must not write back:

- HOLD;
- REVISE;
- promotion;
- classification;
- authority.

### Rule

`P11/READ-RP05 READER_WARNING_OR_PROJECTION_ANNOTATION_CANNOT_MUTATE_CANONICAL_OBJECT_STATE_OR_AUTHORITY`.

---

# 5. Query-plane shortlisting

Current prototype uses query plane to limit primary object selection:

```text
KNOWLEDGE_QUERY → KNOWLEDGE
PROJECT_QUERY → PROJECT
RUNTIME_CONTROL_QUERY → RUNTIME_CONTROL
```

Presentation and History queries remain broader projection modes and are not yet fully implemented as ranked traversal.

This means TP11 is executable but not feature-complete.

### Rule

`P11/PLANE-RP03 PRIMARY_OBJECT_SELECTION_MUST_RESPECT_QUERY_PLANE_BEFORE_SEMANTIC_RELEVANCE_OR_RELATED_SUPPORT_EXPANSION`.

---

# 6. Exact identity before semantic expansion

The executable Reader supports direct `object_id` and `semantic_key` lookup.

If semantic-key lookup returns multiple Current-equivalent candidates and no unique authority can be resolved, it fails rather than ranking by recency/page level/popularity.

### Rule

`P11/ID-RP01 AMBIGUOUS_CURRENT_SEMANTIC_IDENTITY_MUST_FAIL_OR_REQUIRE_AUTHORITY_RESOLUTION_BEFORE_GENERIC_RANKING`.

This prevents retrieval from hiding P0 identity collisions.

---

# 7. Support traversal remains typed and bounded

Current prototype follows only explicit support-like relation types:

- `SUPPORTS_BOUNDED_SCOPE`;
- `SUPPORTS_CLAIM`;
- `EVIDENCED_BY`.

It does not treat all graph neighbors as evidence/support.

### Rule

`P11/TRAV-RP02 READER_MAY_EXPAND_RELATED_SUPPORT_ONLY_THROUGH_TYPED_RELATIONS_COMPATIBLE_WITH_THE_QUERY_PURPOSE; GENERIC_GRAPH_ADJACENCY_IS_NOT_SUPPORT`.

---

# 8. Reader output contract

Minimum executable projection:

```yaml
schema: OLEANDER_TYPED_READER_PROJECTION_v0.1
snapshot_id:
as_of:
query:
identity:
states:
target_results:
related_support:
warnings:
single_aggregate_pass_badge: false
reader_boundary: PROJECTION_ONLY_DOES_NOT_PROMOTE_OR_RECLASSIFY_SOURCE_STATE
```

This can later be rendered as UI/cards/views without changing underlying semantics.

---

# 9. Automation boundary

The Reader may automatically:

- resolve exact IDs;
- filter by Plane;
- show independent states;
- preserve target vectors;
- traverse typed support relations;
- surface contradictions/open states;
- show census metadata and provenance.

It may not self-award:

- Design KEEP;
- Professional PASS;
- B1 semantic equivalence;
- research-method validity;
- field validity;
- Knowledge Current promotion;
- one global project PASS.

---

# 10. Remaining TP11 execution gaps

Still open:

1. ranked retrieval over a real large corpus rather than direct fixture lookup;
2. Support/Provenance pool expansion against live knowledge data;
3. contradiction-aware answer composition;
4. Presentation/History query implementations;
5. dynamic census view rendering;
6. permission-aware source disclosure;
7. actual UI/readability layer;
8. integration with the executable validator receipt.

These are next implementation gaps, not semantic blockers for the projection model already tested.

---

# 11. Replay-derived rules

- `P11/READ-RP03`
- `P11/READ-RP04`
- `P11/READ-RP05`
- `P11/PLANE-RP03`
- `P11/ID-RP01`
- `P11/TRAV-RP02`

---

# 12. TP11 disposition

`TP11 EXECUTABLE READER PROTOTYPE = FIRST_EXECUTABLE_PASS / FEATURE_INCOMPLETE`.

The two critical semantic demonstrations are now executable:

1. `CURRENT + NOT_PROVEN_PROFESSIONAL_PASS`;
2. `bounded support PASS + parent design REVISE`.

No governance or Knowledge Current promotion is authorized.