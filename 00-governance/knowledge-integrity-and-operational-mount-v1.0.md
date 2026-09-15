# OLEANDER Knowledge Integrity & Operational Mount Contract v1.0

**Status:** ACTIVE
**Date:** 2026-09-15
**Scope:** existing and future OLEANDER canonical knowledge objects resolved from the live Knowledge Registry, including `CURRENT / SUPPORT / PROVENANCE / EXCLUDED` retrieval/lifecycle spaces.
**Position:** runtime admission contract between Knowledge Content / Research governance and Design Intelligence / Professional Domain Execution. It does not create a second Knowledge Architecture, retrieval taxonomy, professional process, DD stage system, Project Axis, Gate family or replacement registry.

---

## 1｜Why this contract exists

OLEANDER must not confuse a professionally written page with a clean and operationally trustworthy knowledge object, and must not confuse trustworthy knowledge with developed design or completed professional execution.

Canonical separations:

`BODY COMPLETE ≠ KNOWLEDGE CLEAN`
`KNOWLEDGE CLEAN ≠ OPERATIONALLY ELIGIBLE FOR EVERY CLAIM`
`OPERATIONALLY ELIGIBLE KNOWLEDGE ≠ DQ MATURITY`
`DQ MATURITY ≠ PROFESSIONAL STAGE COMPLETION`
`CURRENT ≠ CLEAN`
`SUPPORT ≠ LOW QUALITY`
`PROVENANCE ≠ FALSE`

The existing corpus may contain useful content together with role drift, authority drift, graph-semantic pollution, duplicate ownership, project contamination, stale sources, unsupported claim promotion or superseded carriers. These defects must not be formalized into `DD-*`, `ADD-*` or another professional process merely because the object already exists in the registry.

---

## 2｜Five independent state families

### A｜Corpus / Retrieval State

Owned by existing Knowledge Retrieval & Lifecycle governance:

`CURRENT / SUPPORT / PROVENANCE / EXCLUDED`.

This answers where and how the object participates in retrieval/lifecycle authority. It does not certify body quality, integrity, operational eligibility, design maturity or professional-stage completion.

### B｜Content Remediation State

Owned by the Knowledge Content Review Layer and Professional Knowledge Content & Research Standard.

Use the existing content vocabulary, including:

`CONTENT_UNREVIEWED / CONTENT_REVIEW_IN_PROGRESS / CONTENT_REVIEWED_KEEP / CONTENT_ACTION_REQUIRED_RESTRUCTURE / CONTENT_ACTION_REQUIRED_ENRICH / CONTENT_ACTION_REQUIRED_MERGE / CONTENT_HOLD / CONTENT_LINEAGE_TERMINAL / CONTENT_ACTION_APPLIED_VERIFY_PENDING / CONTENT_ACTION_APPLIED_VERIFIED`.

This answers whether the current full body is professionally adequate for its declared role and scope.

### C｜Knowledge Integrity State

Runtime integrity view over identity, role, authority, evidence, provenance, graph semantics, duplication and lifecycle findings:

- `KI0 UNKNOWN` — integrity has not been resolved at the required scope;
- `KI1 SUSPECT` — one or more material integrity concerns are identified but not yet dispositioned;
- `KI2 REPAIR` — repair is defined/in progress and the object must not silently inherit verified status;
- `KI3 QUARANTINED` — object may be preserved/discoverable for diagnosis or lineage but must not drive an in-scope decision;
- `KI4 VERIFIED` — applicable integrity obligations are resolved at the declared scope and claim ceiling;
- `KI5 SUPERSEDED / RETIRED` — object is preserved for lineage/history and is not an active decision owner.

`KI4 VERIFIED` is scope-bounded. It is not a universal truth certificate and does not override freshness, jurisdiction, project applicability or a narrower claim ceiling.

### D｜Operational Eligibility

Operational eligibility is a task/claim-scoped admission state, not a new retrieval space:

- `OE0 NOT_EVALUATED`;
- `OE1 NOT_ELIGIBLE`;
- `OE2 CONDITIONAL`;
- `OE3 ELIGIBLE`.

Minimum binding when eligibility is consequential:

```yaml
knowledge_ref:
eligibility_state:
eligibility_scope:
claim_ceiling:
applicability:
conditions:
unresolved_items:
freshness_or_revalidation_trigger:
review_basis:
```

`OE3 ELIGIBLE` means the object may be used for the stated task/claim at the stated ceiling. It does not mean the object is universally applicable.

### E｜Design and Professional Execution States

These remain external to Knowledge Integrity:

- Design Quality maturity: `DQ0 ... DQ5` owned by `Design Quality & Design Development Specification v1.0`;
- Architecture professional stages: `ADD-00 ... ADD-17` owned by `Architecture Design Development Process v1.0`;
- future professional domains retain their own authentic stage semantics.

A knowledge object never acquires DQ maturity or an ADD stage merely because it is mounted into a project.

---

## 3｜Existing corpus mount: no migration-by-copy

The existing live canonical Knowledge Registry remains the source corpus. Do not duplicate pages into Architecture, DD, ADD, Structural, MEP or project folders merely to make them available to a process. Machine-readable mount view: `runtime/OLEANDER_EXISTING_KNOWLEDGE_MOUNT_v1.0.json`.

Canonical mount relation:

`LIVE CANONICAL KNOWLEDGE → runtime resolution → integrity / eligibility filter → Design Intelligence knowledge inputs → DD responsibility scope → Professional Domain Stage`.

The process references the canonical object; it does not own a copy of the object.

### 3.1 Discovery mount

Discovery may surface eligible search results from existing `CURRENT`, `SUPPORT` and, when explicitly useful for history/lineage, `PROVENANCE`, subject to existing `search_eligibility` and retrieval governance.

Discovery does not grant decision authority.

### 3.2 Decision mount

A knowledge object may drive a consequential design/professional decision only when its operational eligibility is resolved for that use.

Default admission logic:

```text
CURRENT/SUPPORT/PROVENANCE resolution
+ current full-body content state
+ applicable K1–K5 / R1–R2 / B1 / IR findings
+ integrity disposition
+ freshness/applicability check
+ explicit claim ceiling
→ OE1 / OE2 / OE3
```

A `KI3 QUARANTINED`, materially stale, unresolved duplicate, wrong-role, wrong-authority or graph-corrupt object cannot become `OE3` for the affected claim merely because its prose is strong.

### 3.3 Conditional mount

`OE2 CONDITIONAL` is appropriate when the object remains useful under explicit limitations, for example:

- a SOURCE is authoritative for product identity but not independent performance proof;
- a precedent supports a reference move but not a performance claim;
- a standard is valid but project jurisdiction/applicability remains OPEN;
- a method is reusable but one project-specific parameter remains unverified;
- a SUPPORT object is adequate for a bounded sub-question but not as the canonical owner of a broader claim.

The condition and `does_not_prove` boundary must travel with the mount.

---

## 4｜Contamination routing

Do not repair every defect in one mutation surface. Route by defect type:

| Finding | Primary remediation owner | Runtime consequence until closed |
|---|---|---|
| thin / incomplete / role-inadequate body | Content Remediation | may remain `OE1/OE2`; no fabricated completion |
| role / identity mismatch | Knowledge Object governance | no affected `OE3` |
| claim exceeds evidence | Claim–Evidence / research review | lower claim ceiling or `OE1/OE2` |
| provenance / locator / version gap | K4 / source governance | conditional or ineligible for affected claim |
| graph semantic pollution | Graph remediation | do not infer authority from bad edge |
| duplicate canonical ownership | Merge / supersession governance | no parallel CURRENT decision owners |
| project-specific contamination in reusable knowledge | Content + object governance | decontaminate or scope to project |
| stale regulation/product/software/source | K5 lifecycle | revalidate before affected use |
| superseded/legacy carrier | Lifecycle / provenance | lineage use only unless explicitly reactivated |

Body workers may record graph/governance findings but must not silently mutate unrelated authority surfaces. Graph workers may repair relation semantics but must not use graph repair as proof of body quality.

---

## 5｜Runtime relation to DD maturity and Professional Stage

The four concepts must be visible simultaneously but never collapsed:

```text
1. BODY / CONTENT REMEDIATION
   Is the knowledge page substantively complete for its role?

2. KNOWLEDGE INTEGRITY + OPERATIONAL ELIGIBILITY
   Can this canonical object be trusted for this task/claim, at what ceiling?

3. DD MATURITY / DESIGN QUALITY
   Has the design itself been developed and resolved across applicable DD responsibilities?

4. PROFESSIONAL DOMAIN STAGE
   Has the authentic professional work of the relevant stage been executed/read back?
```

Example:

```text
Knowledge object: accessibility source
Corpus: SUPPORT
Content: CONTENT_ACTION_APPLIED_VERIFIED
Integrity: KI4 VERIFIED for source identity/version/scope
Eligibility: OE2 CONDITIONAL until project jurisdiction/applicability is resolved

Architecture project:
DD-05 Human Relation: developing
DQ maturity: DQ2
ADD-08 Life-safety/accessibility-aware planning: IN_PROGRESS
```

None of these states upgrades another.

---

## 6｜Professional-stage knowledge-input contract

Each Professional Domain Stage should resolve knowledge by question, not by folder membership.

Minimum stage-side mount record:

```yaml
professional_process:
professional_stage:
professional_question:
knowledge_inputs:
  - knowledge_ref:
    use_role: PRIMARY|SUPPORTING|CONDITIONAL|CONTEXT|COUNTEREVIDENCE
    operational_eligibility: OE1|OE2|OE3
    claim_ceiling:
    applicability:
    does_not_prove:
    freshness_state:
required_dd_responsibilities:
native_outputs:
interfaces:
readback:
review_owner:
reopen_triggers:
```

A stage may discover many candidate objects but should mount the minimum sufficient set needed to support the actual decision.

---

## 7｜Architecture binding example

For `ADD-07 Horizontal and Vertical Circulation`:

```text
Professional question
→ does circulation work as real geometry and behavior?

Candidate knowledge resolution
→ circulation methods
→ accessibility sources
→ egress/life-safety sources
→ human movement evidence
→ precedents/cases
→ project-specific evidence

Operational mount
→ admit only objects with task-scoped OE2/OE3 and carry conditions/claim ceilings

Triggered shared DD responsibilities
→ DD-03 Experience
→ DD-04 Form / Composition
→ DD-05 Human Relation
→ DD-08 Detail / Craft

Professional outputs
→ real plan/model geometry
→ stairs/ramps/lifts/landings
→ door/queue/pinch-point reserves
→ CIRCULATION_READBACK
```

`KNOWLEDGE MOUNT PASS ≠ ADD-07 PASS` and `ADD-07 PASS ≠ DQ4`.

---

## 8｜Existing-corpus adoption rule

For the existing OLEANDER corpus, including the current 1215-object remediation lineage:

1. preserve Canonical IDs and current physical carriers;
2. continue current full-body review in the user-authorized order (`CURRENT → SUPPORT → PROVENANCE` when that order is active);
3. record content remediation independently from graph/governance findings;
4. derive `KI*` only from applicable integrity evidence, not from prose quality alone;
5. derive `OE*` only for a concrete task/claim scope;
6. do not batch-fill all objects with invented domain/stage eligibility;
7. professional/domain bindings may begin as candidate routing, but only task-scoped operational mounts may drive design/professional decisions;
8. no knowledge object is copied into `DD-*` or `ADD-*`; stages hold refs to canonical objects;
9. G9 project outcomes return as lesson candidates and must pass existing knowledge validation before reusable promotion.

This contract therefore mounts the existing corpus without legitimizing existing pollution.

---

## 9｜Machine / human boundary

Machines may check:

- referenced knowledge object resolves;
- current retrieval/corpus state;
- declared content/integrity/eligibility fields exist where required;
- `KI3 → OE3` is prohibited;
- superseded/retired object is not an active primary decision owner;
- stale object does not silently retain unconditional eligibility;
- claim ceiling / applicability / `does_not_prove` travel with conditional mounts;
- professional stage refs resolve to the actual domain process;
- DD refs resolve to the shared DD contract.

Machines may not self-award:

- `KI4 VERIFIED` where semantic/professional judgment is required;
- `OE3 ELIGIBLE` for a consequential claim solely from metadata completeness;
- `DQ3–DQ5`;
- Design KEEP;
- professional-stage PASS;
- statutory / engineering / field acceptance.

---

## 10｜Canonical runtime summary

The knowledge-to-design relation is:

`Live Corpus → Full-body Content Review → Integrity Resolution → Task/Claim-scoped Operational Eligibility → Design Intelligence Knowledge Inputs → Shared DD Responsibilities → Authentic Professional Domain Stage → Native Execution → Actual Readback → Independent Reviews → Promotion → G9 bounded knowledge return`.

The governing rule is:

> **OLEANDER must preserve the existing canonical knowledge corpus while preventing its unresolved pollution from becoming professional execution authority. Content completion, knowledge integrity, operational eligibility, DD maturity and professional-stage completion are independent states that must remain separately visible and separately reviewed.**
