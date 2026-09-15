# OLEANDER P11 Reader / Retrieval / Automation Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P11 SECOND PASS**. Semantic owner remains `OLEANDER_RETRIEVAL_READER_ROUTING_CONTRACT_v1.0.*`.

## 1. Purpose

P11 second pass compiles the stabilized semantic model into retrieval and reader behavior without turning search ranking, UI convenience or automation into authority.

Core invariant:

`CANDIDATE GENERATION → AUTHORITY / PLANE / SCOPE FILTER → TYPED EXPANSION → APPLICABILITY CHECK → PRESENTATION`,

not:

`one opaque score → top result = truth`.

---

## 2. Query Plane Resolution Matrix

| Query intent | Primary plane | Secondary planes |
|---|---|---|
| “what is true/current in this project?” | `PROJECT_QUERY` | Runtime Control, then Knowledge for interpretation |
| “what are we doing / what is blocked / what gate?” | `RUNTIME_CONTROL_QUERY` | Project objects that explain state |
| “what generally applies / how should we do X?” | `KNOWLEDGE_QUERY` | Project examples as bounded application |
| “show/present/explain for audience X” | `PRESENTATION_QUERY` | source Project/Knowledge/Evidence mandatory |
| “why did this change / what was previous?” | `HISTORY_QUERY` | original plane objects in PROVENANCE |
| “verify this requirement” | `PROJECT_QUERY` | Assurance/Evidence + Runtime control |
| “research this method” | `KNOWLEDGE_QUERY` | Source/Evidence/Project cases as support |
| ambiguous project/general wording | explicit multi-plane grouping | no mixed undifferentiated ranking |

Plane resolution may return N planes, but result groups retain plane labels.

---

## 3. Candidate Pool Separation

Create candidate pools before ranking:

1. `CURRENT_EXACT` — exact ID/source/current object match;
2. `CURRENT_SEMANTIC` — Current objects matching plane/type/scope;
3. `SUPPORT` — supplementary evidence/cases/practice;
4. `PROVENANCE` — historical only when history/conflict intent applies;
5. `BLOCKED_OR_EXCLUDED` — never normal conclusion support; may surface as conflict/pollution evidence.

Do not let a high semantic-similarity PROVENANCE object outrank a valid CURRENT owner by one blended score.

---

## 4. Ranking Decomposition Matrix

Ranking dimensions may influence order **inside a valid candidate pool**.

| Dimension | Meaning | Can create authority? |
|---|---|---:|
| `IDENTITY_MATCH` | exact canonical/project/object identity | NO; confirms target |
| `AUTHORITY_FIT` | object is valid owner for question/property | determines eligibility, not quality score |
| `PLANE_TYPE_FIT` | semantic object type matches intent | NO |
| `SCOPE_CONFIG_FIT` | project/domain/configuration/time matches | NO; may exclude invalid candidate |
| `SEMANTIC_RELEVANCE` | content addresses question | NO |
| `RETRIEVAL_STATE` | CURRENT/SUPPORT/PROVENANCE | routing/eligibility only |
| `FRESHNESS` | mutable object still valid | NO; stale may trigger boundary |
| `TRUST_REVIEW` | review state | NO independent truth rank |
| `EVIDENCE_APPLICABILITY` | evidence applies to current claim | may bound claim, not taxonomy |
| `RELATION_DISTANCE` | typed graph distance from target | NO |
| `MEDIUM_OUTPUT_FIT` | suitable output/reader format | NO |

Forbidden generic rank features:
`L_LEVEL_HEIGHT / FRAMEWORK_STATUS / PAGE_LENGTH / CITATION_COUNT / PROJECT_USE_COUNT / MODIFIED_TIME / RELATION_COUNT / RECEIPT_COUNT / AI_CONFIDENCE`.

---

## 5. Ranking Decision Policy

Use **lexicographic eligibility before relevance**:

1. exact identity / authority owner if query is identity-specific;
2. plane/type/scope eligibility;
3. Current/retrieval eligibility;
4. configuration/freshness applicability;
5. typed semantic relevance;
6. evidence/trust dimensions appropriate to question;
7. relation distance / presentation fit.

If a higher-priority eligibility dimension conflicts, do not compensate with higher semantic similarity.

Example:
- stale Current Method may still remain the Current identity but Reader must display stale boundary;
- fresh Support cannot silently become Current because its text matches better;
- it may be recommended as Support with explicit reason.

---

## 6. Typed Traversal Matrix

### Knowledge query traversal
Allowed first-order expansion:
`PARENT/CHILD, REQUIRES_CONCEPT, EXTENDS, REFINES, CONTRASTS_WITH, IMPLEMENTS, CONSTRAINED_BY, SUPPORTS_CLAIM, CONTRADICTS_CLAIM, BOUNDS_CLAIM, DOMAIN, APPLICATION, LIFECYCLE`.

### Project query traversal
Allowed first-order expansion:
`DERIVED_FROM, SATISFIES, CONSTRAINED_BY, CONTROLLED_BY, INTERFACES_VIA, DEPENDS_ON, CONSUMES, VERIFIED_BY, VALIDATED_BY, AFFECTS, REOPENS, BASELINED_IN, SUPERSEDES`.

### Runtime query traversal
Allowed:
`DEPENDS_ON, STALE_IF, USES_AUTHORITY_SNAPSHOT, USES_KNOWLEDGE_SNAPSHOT, REGISTERS, ROUTES, CLOSES, REOPENS, PROMOTES`.

### Presentation query traversal
Allowed:
`PROJECTS, REPRESENTS, DERIVES_FROM, USES_EVIDENCE, USES_STYLE, USES_TECHNIQUE, ADAPTED_FOR, RELEASED_AS, READBACK_OF`.

### Traversal depth rules
- default to shortest sufficient typed path;
- second-order expansion only when the query requires causal/dependency/evidence depth;
- stop expansion when relation no longer answers query intent;
- detect cycles and preserve lineage rather than infinite traversal;
- generic `related_to` is discovery fallback only and cannot support strong semantic inference.

---

## 7. Claim-First Answer Bundle

For consequential factual/research/technical answers, return an inspectable bundle:

```yaml
answer_statement:
answer_scope:
source_plane:
canonical_object_ids: []
claim_ids: []
evidence_support: []
evidence_contradictions: []
evidence_bounds: []
configuration_or_version:
freshness_boundary:
claim_ceiling:
open_uncertainties: []
current_support_provenance_state:
return_to_source: []
```

When Claim IDs are not yet materialized, reconstruct the claim from exact Current full body and label it as reconstructed rather than inventing a permanent Claim ID.

---

## 8. Human Reader View Matrix

### Executive / Decision View
Show:
`Decision Question → Current disposition → critical Requirement/Constraint → major risk/interface → evidence summary → next/reopen obligation`.

Hide low-level runtime detail by default but keep drill-down.

### Project Design View
Show:
`Project State → Workstreams → selected design/variables/interfaces → open decisions/issues → evidence/readback → presentation/release`.

### Integration View
Show:
`subsystems → interfaces → shared variables → coupling/criticality → maturity/disposition → change/reopen`.

### Assurance View
Show:
`target/configuration → assurance type → method/criteria → evidence → per-target result → decision → ceiling/limitations`.

### Research/Knowledge View
Show:
`Core Question → Claims → supports/contradicts/bounds → Method → limitations → Role/Level → content/research/trust/freshness`.

### Maintenance View
Show:
`identity/collision → classification → content state → research states → graph → retrieval → freshness → migration/readback`.

### Presentation View
Show:
`audience/objective → argument → evidence projection → style/technique → E0-E3 risk → source truth → readback/release`.

### History View
Show:
`supersession → old baseline → prior decisions/evidence/receipts → cause of change`.

A Reader view is projection, never a new source of truth.

---

## 9. Agent Retrieval / Execution Matrix

An Agent preparing to act must retrieve more than a human summary.

Minimum agent preflight:
1. exact object identity;
2. Object Plane;
3. Current Authority Snapshot;
4. Project State / active Decision Object if Project task;
5. Current configuration/baseline;
6. locked/open/protected objects;
7. applicable Requirements/Constraints;
8. dependencies/interfaces/shared variables;
9. existing Knowledge/Method owner;
10. required native output/execution owner;
11. readback/evidence obligation;
12. claim ceiling + stop/reopen conditions.

Agent may use summary views only after the underlying refs are resolved.

---

## 10. Human vs Agent Disclosure Matrix

| Information | Human default | Agent default |
|---|---|---|
| plane/type | compact visible | mandatory explicit |
| authority source | visible for material claims | mandatory |
| full relation graph | on demand | query-scoped typed traversal |
| runtime receipts | normally hidden unless relevant | retrieve when execution/state depends on them |
| claim/evidence contradictions | surface when material | mandatory for decision/promotion |
| hashes/revisions | compact/on demand | mandatory where configuration control applies |
| claim ceiling | plain-language boundary | explicit vector/refs |
| history/provenance | on demand | retrieve if stale/conflict/change analysis |

Do not burden human readers with audit noise, but do not omit material truth boundaries.

---

## 11. State Badge Separation Matrix

Never create one “quality badge”. Display separate fields as appropriate:

### Knowledge
`LEVEL | ROLE | RETRIEVAL | GOVERNANCE | CONTENT | R1 | R2 | EVIDENCE | TRUST | FRESHNESS | B1 | GRAPH`.

### Project
`SEMANTIC_CLASS | NATIVE_STATE | VALIDITY_DISPOSITION | CONFIGURATION | AUTHORITY | ASSURANCE | CLAIM_CEILING`.

### Runtime Control
`TYPE | STATUS | SNAPSHOT_VALIDITY | DEPENDENCY/BLOCKER | READBACK | CLAIM_CEILING`.

### Presentation
`SOURCE_STATE | STYLE_PROFILE | TECHNIQUE_SET | TRUTH_RISK | READBACK | RELEASE`.

Forbidden composite badge examples:
`MATURE`, `SAFE`, `VERIFIED CURRENT`, `PRO QUALITY` unless the UI expands to exact independent states and such phrase is actually authorized.

---

## 12. Current / Support / Provenance Display Rules

- `CURRENT`: primary answer owner for scope; show freshness/trust/evidence separately.
- `SUPPORT`: visually secondary and labeled; may strengthen/contrast but cannot silently replace Current.
- `PROVENANCE`: hidden by default outside history/conflict; when shown, label superseded/historical prominently.
- `EXCLUDED/BLOCKED`: not conclusion support; may appear in diagnostic/pollution/conflict view.

When Current is stale:
- keep identity visible;
- show stale reason and ceiling;
- surface eligible Support alternatives as alternatives, not automatic replacement;
- initiate governance/revalidation path if task requires Current answer.

---

## 13. Contradiction UI Matrix

| Contradiction type | Reader treatment |
|---|---|
| Current vs superseded | Current primary; superseded in provenance with reason |
| Current vs Current collision | HOLD/conflict banner; no silent winner |
| evidence contradiction same config/condition | show both + uncertainty + open resolution |
| apparent contradiction caused by different configs | group by configuration |
| method disagreement | show methods/conditions/evidence basis |
| project vs generic Knowledge | project authority governs project fact; generic Knowledge remains interpretation/support |
| source vs presentation | source governs truth; presentation marked derivative |

Contradictions are first-class information, not search noise.

---

## 14. Freshness / Staleness Display Matrix

Mutable objects should expose:
`last_verified + due/trigger + stale_reason + affected_claim + replacement/current_ref + allowed_use`.

Allowed use labels:
- `CURRENT_VALID`;
- `USE_WITH_RECHECK`;
- `HISTORY_ONLY`;
- `DO_NOT_USE_FOR_CURRENT_CLAIM`.

Do not merely lower ranking for stale material; display why it is stale when it affects the answer.

---

## 15. Automation Permission Matrix

| Automation action | Allowed automatically? | Notes |
|---|---:|---|
| ID/collision detection | YES | can block obvious collision |
| enum/state-transition validation | YES | based on current machine contracts |
| relation cardinality/missing required edge | YES | semantic existence, not professional truth |
| hash/version/config difference | YES | identity/delta only |
| stale fingerprint/pointer detection | YES | consequence routing may still need materiality review |
| unit/date/schema validation | YES | syntactic/numeric consistency |
| derivative source/loss metadata check | YES | cannot judge all perceptual/semantic loss automatically |
| potential bilingual mismatch signal | YES as signal | cannot grant B1 PASS |
| potential contradiction detection | YES as signal | human/domain resolution required when material |
| exact full-body presence/readback requirement | YES | can enforce retrieval before decision |
| claim evidence relation completeness | YES structurally | cannot self-award evidence adequacy |
| design KEEP / aesthetic excellence | NO | independent design review |
| research conduct/method validity PASS | NO | applicable research review |
| professional/legal/certification acceptance | NO | authorized authority only |
| field/in-use validity | NO | field evidence/validation required |
| causal truth | NO from correlation/co-occurrence alone | research design required |
| Need universality | NO | stakeholder/research evidence required |
| new L4 admission | NO fully automatic | machine can test fields; governance semantic judgment required |
| Knowledge CURRENT promotion | NO fully automatic | explicit promotion authority/gates |

Automation can **fail closed** on violated hard invariants; it cannot self-create truth it is not authorized to judge.

---

## 16. Routing to Execution Owner Matrix

Select the minimum sufficient owner set by responsibility:

| Need | Owner route |
|---|---|
| semantic/design decision | Current Project/Knowledge design-method owner |
| native artifact production | execution owner capable of required native format |
| specialist technical proof | applicable specialist owner |
| research/evidence method | research/evidence owner |
| cross-disciplinary integration | integration owner + participating discipline owners |
| independent design review | independent review owner |
| delivery/QC | delivery/QC owner |

Rules:
- one owner may satisfy multiple responsibilities;
- do not invoke every Skill by default;
- `NO_DEDICATED_OWNER` is legal and does not authorize new Skill creation;
- tool availability is execution capability, not semantic authority.

---

## 17. Search Failure / Fail-Closed Matrix

| Failure | Required behavior |
|---|---|
| exact Current owner unresolved | HOLD / scoped Support answer with disclosure |
| Canonical collision | HOLD; read both full bodies/authority |
| Retrieval Space missing | do not assume CURRENT |
| Project configuration unknown | no reuse of prior assurance as Current |
| mutable source stale | bound answer/revalidate |
| blocked Search Eligibility | exclude from conclusion support |
| access/right prevents source read | disclose coverage gap; do not invent content |
| only snippets available but full-body judgment requested | retrieve full body or remain OPEN |
| no execution owner | `NO_DEDICATED_OWNER`; manual/alternate route if authorized |
| evidence inadequate | lower answer ceiling; preserve Unknown/HOLD |

---

## 18. Answer Coverage Record

For high-consequence retrieval, optionally record:

```yaml
query_id:
query_planes: []
searched_spaces: []
exact_ids_checked: []
full_bodies_read: []
typed_relations_expanded: []
support_scope:
provenance_scope:
unread_or_inaccessible_sources: []
contradictions_found: []
stale_items: []
coverage_limitations: []
answer_ceiling:
```

This supports absence claims such as “no Current object found” without pretending the entire corpus was searched when it was not.

---

## 19. Regression Eval Matrix

Minimum second-pass scenarios:

1. `RET-P11-001`: exact Current L5 vs semantically similar L4 Support → Current L5 primary; no L4 bias.
2. `RET-P11-002`: Current stale vs fresh Support → stale Current identity visible, Support offered but not silently promoted.
3. `RET-P11-003`: two active Current same Canonical ID → HOLD collision.
4. `RET-P11-004`: Project Requirement vs generic Knowledge Method conflict → Project/mandate scope governs project fact.
5. `RET-P11-005`: title/snippet suggests METHOD but exact body is runtime receipt → no classification from snippet.
6. `RET-P11-006`: synthetic E3 image formatted with E0 typography → remains E3.
7. `RET-P11-007`: historical baseline has stronger semantic match → HISTORY_ONLY unless history intent.
8. `RET-P11-008`: 1215 corpus grows → no denominator/fixed-completion failure.
9. `RET-P11-009`: high citation count but no Claim-level support → bounded answer.
10. `RET-P11-010`: color-only red/green interface status → accessibility/readability fail until redundant cue exists.
11. `RET-P11-011`: motion-only state transition explanation → fail until static/reduced alternative exists.
12. `RET-P11-012`: no dedicated Skill → return legal NO_DEDICATED_OWNER; no auto-create.
13. `RET-P11-013`: contradictory evidence same configuration → both surfaced; strongest ceiling blocked until bounded/resolved.
14. `RET-P11-014`: contradictory evidence actually different configurations → group by configuration; no false contradiction.
15. `RET-P11-015`: summary claims Project PASS but underlying Assurance per-target has one Critical FAIL → summary cannot hide failure.
16. `RET-P11-016`: Project-specific successful pattern requested as general rule → route through G9/Knowledge admission, not direct Knowledge CURRENT.
17. `RET-P11-017`: user requests history → Provenance intentionally expanded and labels retained.
18. `RET-P11-018`: automated validator sees complete schema but professional approval absent → cannot self-award professional PASS.

---

## 20. Reader Quality Readback

Reader itself needs actual task readback.

Test dimensions:
- can user identify Current owner quickly?
- can user distinguish Current/Support/Provenance?
- can user see why an object is stale or bounded?
- can user return to source?
- are contradictions visible but not overwhelming?
- do separate states remain understandable?
- can user answer current Decision Question without reading audit noise?
- can an Agent recover exact config/authority/readback obligations?
- do mobile/narrow views preserve semantics?
- does long bilingual text preserve hierarchy?

Reader UI success is a Presentation/Usability result, not proof the underlying ontology is correct.

---

## 21. Validator additions for P11 v1.1

- `P11/PLANE-M01`: material query resolves query plane(s) before candidate mixing.
- `P11/POOL-M01`: CURRENT/SUPPORT/PROVENANCE/BLOCKED candidate pools remain separable.
- `P11/RANK-M01`: invalid authority/scope/retrieval candidate cannot compensate with semantic similarity score.
- `P11/RANK-M02`: L-level/framework/use-count/citation-count cannot be generic truth/quality rank.
- `P11/TRAV-M01`: strong semantic inference requires typed relation path; generic related_to insufficient.
- `P11/CLAIM-M01`: consequential answer bundle records source/claim/evidence/bounds/configuration/ceiling as applicable.
- `P11/VIEW-M01`: Reader task view is projection and cannot mutate source authority/state.
- `P11/BADGE-M01`: independent state axes cannot collapse into one quality badge.
- `P11/CONTRA-M01`: material contradiction cannot be hidden by ranking/summarization.
- `P11/STALE-M01`: stale material displays reason/allowed-use, not silent rank penalty only.
- `P11/AUTO-M01`: automation permissions enforce hard boundary against self-certified design/research/professional/field truth.
- `P11/ROUTE-M01`: execution routing uses minimum sufficient owner set and accepts NO_DEDICATED_OWNER.
- `P11/COV-M01`: absence claim requires explicit retrieval coverage record/limitations when consequential.
- `P11/EVAL-M01`: regression suite covers all minimum second-pass scenarios.

## 22. P11 v1.1 closure test

P11 second pass is ready for validator/prototype compilation when:
- plane resolution and candidate-pool separation are machine-readable;
- ranking is decomposed and inspectable;
- typed traversal has intent/depth limits;
- human and agent views preserve independent states;
- Current/Support/Provenance contradictions/freshness are visible;
- automation permissions are explicit;
- routing can return `NO_DEDICATED_OWNER` safely;
- absence claims can report coverage;
- the regression scenarios pass in a concrete Reader/Agent prototype.
