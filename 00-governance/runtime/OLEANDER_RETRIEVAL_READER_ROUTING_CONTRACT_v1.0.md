# OLEANDER Retrieval / Reader / Automation / Routing Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P11**. Extends Current Knowledge Retrieval & Lifecycle v1.1 and Current Skill Resolver. It does not create a second search index, a second Skill Registry, or a UI-specific authority model.

## 1. Purpose

After Object Plane, Project semantics, Runtime Control, Knowledge classification and Presentation projection are separated, retrieval must preserve those distinctions.

The Reader/Agent must answer:

- **What plane am I querying?**
- **What type of object do I need?**
- **What authority/retrieval space/state applies?**
- **Which typed relations are legitimate for expansion?**
- **What is stale/open/contradicted?**
- **What source should be returned as Current versus Support versus Provenance?**
- **Which execution owner is the minimum sufficient route?**

Core rule:

`RETRIEVAL RANK ≠ TRUTH RANK ≠ TAXONOMY HEIGHT ≠ POPULARITY ≠ QUALITY`.

## 2. Plane-aware routing first

Every material query should resolve one or more explicit query planes before ranking.

### `KNOWLEDGE_QUERY`
Seeks reusable Theory/Method/Tool/Source/Evidence/Case/Practice/Framework knowledge.

### `PROJECT_QUERY`
Seeks project-specific Requirement/Decision/Variable/Interface/Artifact/Evidence/Baseline/Change/Risk/etc.

### `RUNTIME_CONTROL_QUERY`
Seeks current Project State, packet/register/receipt/gate/snapshot/staleness/promotion/reopen records.

### `PRESENTATION_QUERY`
Seeks audience-facing projection/style/technique/release/readback, while preserving links to source planes.

### `HISTORY_QUERY`
Explicitly seeks provenance, superseded state, prior versions, old decisions/receipts.

A natural-language question may route to multiple planes, but the result groups must remain distinguishable.

## 3. Query intent contract

Resolve the applicable subset:

```yaml
query_id:
raw_query:
query_planes: []
identity_intent:
subject_domain:
project_id:
workstream_id:
object_types: []
knowledge_roles: []
relation_intents: []
authority_requirement:
retrieval_space_requirement:
freshness_requirement:
evidence_requirement:
time_scope:
medium_or_output_intent:
history_intent:
execution_required:
```

Do not infer a Project query as reusable Knowledge merely because the same term exists in both planes.

## 4. Retrieval spaces remain fixed

Use:

- `CURRENT`
- `SUPPORT`
- `PROVENANCE`
- `EXCLUDED`

These answer retrieval/authority position, not taxonomy, maturity or truth by themselves.

### CURRENT
Default authoritative/retrieval owner for its defined scope.

### SUPPORT
Valid supplementary object not selected as default Current truth/rule.

### PROVENANCE
Historical/superseded/snapshot/receipt/legacy material used for lineage/history/conflict explanation.

### EXCLUDED
Retained audit object not eligible to support normal conclusions.

Do not merge CURRENT and PROVENANCE into one undifferentiated ranking pool.

## 5. Search Eligibility

Retain:

`DEFAULT | SCOPED | HISTORY_ONLY | BLOCKED`.

Eligibility and Retrieval Space are separate:
- `CURRENT + SCOPED` may be authoritative only for specific intent/domain/project;
- `SUPPORT + DEFAULT` is still not Current authority;
- `PROVENANCE + HISTORY_ONLY` is legitimate for historical questions;
- `BLOCKED` may surface as conflict/pollution evidence but not as answer support.

## 6. Retrieval pipeline

Default typed pipeline:

`QUERY → PLANE RESOLUTION → EXACT IDENTITY / SOURCE AUTHORITY → METADATA PRE-FILTER → CURRENT SEARCH WITHIN PLANE → TYPED RELATION EXPANSION → SUPPORT EXPANSION IF NEEDED → PROVENANCE ONLY FOR HISTORY/CONFLICT → AUTHORITY/FRESHNESS/EVIDENCE/CONTRADICTION CHECK → RETURN WITH STATE BOUNDARY`.

### Step 0 — Plane resolution

Fail closed to explicit multi-plane grouping when ambiguity matters.

### Step 1 — Exact identity

Prefer:
- Canonical ID/object ID;
- exact Project ID/Workstream ID;
- exact Artifact/Requirement/Decision/etc. identity;
- known Source Authority.

### Step 2 — Metadata pre-filter

Apply applicable:
- Object Plane;
- Governance;
- Retrieval Space;
- Search Eligibility;
- Trust;
- Freshness;
- current/superseded status;
- Project scope;
- Domain/Role/Type;
- rights/access.

### Step 3 — Current retrieval

Search CURRENT objects first within the resolved plane/intent.

### Step 4 — Typed relation expansion

Expand only relations that answer the query.

### Step 5 — Support expansion

Expand SUPPORT only when Current is insufficient, comparison/cases/evidence depth is required, or query explicitly asks for breadth.

### Step 6 — Provenance expansion

Use PROVENANCE for history, why-changed, supersession, prior decision, receipt or conflict investigation.

### Step 7 — validity check

Before consumption, inspect:
- authority conflict;
- staleness/revalidation due;
- evidence ceiling;
- contradictory evidence;
- object/claim scope;
- open critical blockers.

## 7. Plane-specific relation expansion

### Knowledge relations

Use:
`BROADER/NARROWER/PARENT/CHILD`
`REQUIRES_CONCEPT`
`EXTENDS`
`REFINES`
`CONTRASTS_WITH`
`IMPLEMENTS`
`CONSTRAINED_BY`
`SUPPORTS_CLAIM`
`CONTRADICTS_CLAIM`
`BOUNDS_CLAIM`
plus controlled Domain/Application/Lifecycle relations.

### Project relations

Use typed project semantics:
`derived_from / satisfies / verified_by / validated_by / constrained_by / interfaces_via / depends_on / consumes / controlled_by / affects / reopens / baselined_in / supersedes`, etc.

### Runtime Control relations

Use:
`depends_on / stale_if / uses_authority_snapshot / uses_knowledge_snapshot / registers / closes / reopens / routes / promotes`.

### Presentation relations

Use:
`projects / represents / derives_from / uses_evidence / uses_style / uses_technique / adapted_for / released_as / readback_of`.

Never replace a strong typed relation with generic `related_to` for ranking convenience.

## 8. Reader state columns

Any serious Reader/Registry UI should show state dimensions separately rather than compress into one badge.

### Knowledge object reader

Show independently as applicable:
- Object Plane;
- Domain/Topic;
- L0–L7;
- Primary Knowledge Role;
- Framework Type;
- Information Role;
- Retrieval Space;
- Search Eligibility;
- Governance;
- Evidence;
- Trust;
- Freshness;
- Content State;
- Research R1;
- Research R2;
- Bilingual State;
- Graph State;
- Lifecycle/supersession.

### Project object reader

Show:
- Project/P3 context;
- Primary Semantic Class;
- state machine state;
- validity disposition;
- authority owner/change authority;
- baseline/configuration;
- dependencies/interfaces;
- evidence/assurance;
- claim ceiling;
- stale/reopen state.

### Runtime Control reader

Show:
- control-object type;
- authority snapshot/fingerprint;
- source revision;
- status;
- dependencies;
- stale_if;
- blockers;
- readback refs;
- claim ceiling;
- supersession.

### Presentation reader

Show:
- source objects/claims;
- audience/objective;
- medium;
- Style Profile;
- Technique Set;
- E0–E3 truth-risk;
- target-condition readback;
- release status;
- source claim ceiling.

## 9. Forbidden ranking shortcuts

Never use as generic quality/authority ranking:

- higher L-level;
- L4 Framework status;
- document length;
- citation count;
- use count/project frequency;
- newest modified time;
- latest filename/version number;
- ACTIVE governance alone;
- VERIFIED on one state axis;
- AI-generated confidence score;
- number of relations;
- number of artifacts/receipts/CI passes.

Examples:

`L4 ≠ better than L5`.

`CURRENT ≠ verified truth`.

`Frequently reused ≠ Framework`.

`Many citations ≠ strong Claim evidence`.

## 10. Ranking dimensions

Ranking may use different dimensions depending on query intent, but keep them inspectable.

Potential dimensions:
- exact identity match;
- authority fit;
- plane/type fit;
- scope/domain fit;
- semantic relevance;
- retrieval space/eligibility;
- freshness;
- trust/review status;
- evidence applicability;
- claim-level support;
- relation distance through relevant typed edges;
- requested medium/output fit;
- project configuration match.

No opaque composite score should be treated as authority.

## 11. Dynamic corpus rule

Corpus size is a time-scoped census, not a completion denominator.

Every corpus statistic must carry as applicable:

`as_of + scope + enumeration basis + plane + retrieval space + query/filter`.

Do not hard-code `1215`, `1024`, or any historical count into migration completeness, routing or denominator logic.

Completion requires:

`enumeration closure + per-object decision/readback` for the scoped population.

## 12. Exact full-body rule

For classification/content/research judgments, search snippets and graph metadata are navigation only.

Before changing:
- Knowledge Role/Level/Framework Type;
- Content PASS/RESTRUCTURE/ENRICH;
- research state;
- semantic scope;
- canonical merge/split decision;

read the exact Current canonical full body.

`SEARCH HIT ≠ CONTENT REVIEW`.

## 13. Claim-first retrieval

When the user asks a factual/technical/research question and relevant Knowledge Claims are addressable, retrieve at Claim level where possible:

`Question → Claim candidates → supporting/bounding/contradicting Evidence → applicability/freshness → answer`.

Do not answer solely from page-level citation volume.

When Claim objects are not yet materialized, reconstruct the claim ledger from Current full body rather than inventing claim certainty.

## 14. Project query behavior

For project questions, prefer Current Project semantic/runtime objects over distilled general Knowledge when the user asks what is true **in this project**.

Example order:

`Project Authority → Project State → Current Baseline → Project Requirement/Decision/Variable/Interface/Evidence → applicable Knowledge/Method for interpretation`.

Knowledge Method cannot override project-specific Current truth.

## 15. Knowledge query behavior

For reusable “how/why/what generally applies” questions:

`Current Knowledge owner → Claims/Evidence/Boundaries → Support cases/practices → Project examples only as bounded provenance/application`.

Do not convert a current project's choice into general rule merely because it is recent.

## 16. History query behavior

History intent explicitly activates provenance.

Return:
- supersession chain;
- old baseline/version;
- historical decisions/receipts;
- why Current changed;
- what evidence or authority caused the change.

Always label historical status; never let older object silently compete as Current.

## 17. Routing from Knowledge to execution owner

For tasks requiring action:

`Current Authority → Plane/Object resolution → Current Knowledge Method/Tool/Practice when applicable → Required Native Output → Existing Execution Owner Map → minimum sufficient owner set → multi-owner DAG only when required → execution adapter/tool → actual artifact/readback`.

Rules:
- Skill anchor text is retrieval intent, not Current authority;
- `NO_DEDICATED_OWNER` is a legal result;
- no automatic new Skill because an owner is missing;
- use minimum sufficient owner set, not full Skill stack;
- specialist owner selection cannot change Knowledge taxonomy or Project authority;
- execution capability ≠ truth authority.

## 18. Minimum sufficient owner set

Select owners by required responsibility, not keyword count.

Owner set should cover:
- semantic/design owner;
- required native production capability;
- triggered specialist technical/evidence owner;
- independent review owner when required;
- delivery/QC owner when delivery is material.

Avoid redundant owner activation when one Current owner already covers the responsibility.

## 19. Automation permission boundary

Automation may:
- check IDs/collisions;
- validate allowed enums/state transitions;
- detect missing typed relations/required fields;
- compute hashes/version differences;
- detect stale fingerprints/pointers;
- validate units/numbers/dates/schema;
- flag possible bilingual mismatch;
- flag unsupported promotion/state inference;
- route readback/evals;
- surface contradictions for review.

Automation may **not self-certify**:
- professional truth;
- design quality KEEP;
- research-method validity;
- semantic bilingual equivalence;
- field/operational validity;
- certification/legal approval;
- stakeholder acceptance;
- aesthetic excellence;
- causal truth merely from co-occurrence.

Those require their applicable evidence/authority/review gates.

## 20. Fail-closed behavior

When a material retrieval/routing fact is unresolved:

- unresolved Current owner → SUPPORT/HOLD rather than invent Current;
- missing Retrieval Space → do not assume CURRENT;
- conflicting Current objects → collision/authority HOLD;
- stale mutable object → flag/restrict according to freshness contract;
- blocked Search Eligibility → do not use as conclusion support;
- unknown Project configuration → do not reuse old assurance as Current;
- missing execution owner → `NO_DEDICATED_OWNER`/capability HOLD, not auto-create owner;
- insufficient evidence → lower claim/answer boundary, not fabricate certainty.

## 21. Reader provenance / return-to-source

Every material answer/view should retain a path back to source:

- canonical object ID;
- source carrier/URI where accessible;
- version/revision/baseline;
- Claim/Evidence IDs when used;
- current/supported/provenance status;
- generated presentation derivative link back to upstream source;
- date/freshness boundary when material.

A summary is not a replacement carrier unless explicitly promoted.

## 22. Contradiction presentation

Reader should not hide contradictions by selecting one high-ranked source.

When material contradiction exists:
- show the competing Claims/Evidence;
- show configuration/scope/date differences;
- identify current authority if resolved;
- otherwise mark `UNRESOLVED / HOLD / BOUNDED ANSWER`.

Contradiction visibility is a quality feature, not noise.

## 23. Stale/revalidation visibility

For mutable knowledge/project/runtime objects, Reader should make visible:
- last verified/reviewed;
- verification due/revalidation trigger;
- stale/reopen reason;
- impacted Claim/object;
- current replacement if any.

Do not silently rank stale data lower without telling the user why when the stale state affects the answer.

## 24. Plane-aware navigation

Recommended navigation pattern:

`OBJECT → PRIMARY PLANE VIEW → TYPED RELATIONS → EVIDENCE/PROVENANCE → PRESENTATION/DERIVATIVES`.

Examples:
- Knowledge METHOD → claims/sources/practices → project applications;
- Project INTERFACE → shared variables/requirements/evidence/change history → integration receipts;
- Runtime AUTHORITY_SNAPSHOT → source authorities/configuration → affected packets/receipts;
- Presentation VIEW_UNIT → source Claims/Evidence → style/technique/readback.

Do not flatten all neighboring objects into one “related” list.

## 25. Search and UI facets

Useful facets should map to real semantics:
- Object Plane;
- Domain/Topic;
- L-level;
- Knowledge Role;
- Project/Workstream;
- Project semantic class;
- Runtime Control type;
- Retrieval Space;
- Search Eligibility;
- Governance/Trust/Freshness;
- Evidence type/strength;
- assurance type/state;
- interface criticality/maturity;
- risk/issue status;
- baseline/configuration;
- presentation medium/style/truth-risk.

Facet existence does not imply all combinations are valid.

## 26. Reader views by task

Provide task-specific compositions without changing source data.

Examples:
- **Research view** — Claims/Evidence/Contradictions/Methods/Source freshness;
- **Project decision view** — Decision Question/Requirements/Variables/Interfaces/Risks/Evidence;
- **Integration view** — subsystem/interfaces/shared variables/change/reopen;
- **Assurance view** — target/configuration/method/evidence/per-target result/decision;
- **Knowledge maintenance view** — classification/content/research/trust/freshness/retrieval;
- **Presentation view** — audience/argument/proof/style/technique/source truth/readback;
- **History view** — supersession/old baselines/receipts/change rationale.

A view is projection; it does not become a new canonical object unless independently needed.

## 27. Recommendation/routing transparency

When the system recommends a Method/Skill/Knowledge object, retain a compact routing reason:

`query need → plane/type → current owner → scope match → evidence/freshness → selected relation/path → why alternatives were not primary`.

Do not expose private chain-of-thought; store inspectable decision factors/receipts only.

## 28. Regression / validation scenarios

Minimum tests:

1. same title exists in Current and Provenance → Current default, provenance only history;
2. L4 Support vs L5 Current → no generic L4 preference;
3. Current object stale and Support object fresh → surface stale boundary; do not silently promote Support;
4. project-specific Requirement conflicts with generic Method → Project Authority wins inside valid scope;
5. search hit points to summary but canonical full body differs → classification/content judgment uses full body;
6. synthetic presentation image has strong visual match → remains E3 and cannot become Project evidence;
7. two Current candidates share Canonical ID → HOLD collision, no rank winner;
8. Skill docs call object “Current” but live Retrieval Space says SUPPORT → live state wins;
9. missing dedicated execution owner → NO_DEDICATED_OWNER, no auto-new Skill;
10. user asks history → superseded/provenance intentionally included and clearly labeled;
11. current count changes beyond 1215 → retrieval/migration still works without fixed denominator;
12. high citation page has weak claim-level evidence → answer bounded at claim level.

## 29. Validator floor

- `RET-001` material query resolves query plane(s) before mixed ranking;
- `RET-002` CURRENT and PROVENANCE do not share undifferentiated default ranking;
- `RET-003` Search Eligibility enforced;
- `RET-004` higher L-level/usage/citation count cannot be generic quality rank;
- `RET-005` typed relation expansion preferred over generic related links;
- `RET-006` stale/conflicted object cannot silently answer as Current-valid;
- `RET-007` content/classification judgment requires exact Current full body;
- `RET-008` corpus counts require as_of/scope/enumeration basis and cannot hard-code migration denominator;
- `RET-009` project truth query prioritizes Project Authority/Current configuration over generic Knowledge;
- `RET-010` history intent labels provenance status;
- `ROUTE-001` execution routing uses existing Current owner map + minimum sufficient owner set;
- `ROUTE-002` NO_DEDICATED_OWNER does not auto-create Skill;
- `AUTO-001` automation cannot self-certify professional/design/research/bilingual/field truth;
- `SRC-001` material Reader view preserves return-to-source/version/state;
- `CONTRA-001` material contradiction cannot be hidden by ranking;
- `VIEW-001` Reader task view remains projection, not new truth authority.

## 30. P11 closure condition

P11 is sufficiently refined for draft review when plane-aware retrieval, typed expansion, state-separated Reader UI, dynamic corpus handling, claim-first evidence retrieval, project-vs-knowledge routing, automation limits, fail-closed behavior, provenance return path and regression scenarios are machine-readable.
