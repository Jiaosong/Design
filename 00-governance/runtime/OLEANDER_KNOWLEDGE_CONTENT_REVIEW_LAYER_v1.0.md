# OLEANDER Knowledge Content Review Layer v1.0

Status: ACTIVE_CURRENT

## Purpose

This layer makes body-level semantic review a first-class completion requirement for the OLEANDER knowledge graph. Graph correctness and content correctness are separate obligations.

An object is not complete merely because its Level, Knowledge Role, Framework Type, Domain routing, typed relations, hierarchy, or derivative readback are correct.

Every knowledge-graph object must have both:

1. a **Graph Terminal** state; and
2. a **Content Terminal** state.

No object may be reported as globally complete until both are terminal.

## Authority and evidence rules

- Review the current canonical body, not the title, prefix, Canonical ID, page length, role, maturity, source count, or graph position alone.
- If the canonical body is unavailable, empty, materially truncated, corrupt, or semantically insufficient, fail closed to `HOLD`.
- A prior classification decision is not automatically a content review.
- A graph mutation receipt is not content evidence.
- A Reader/D1 relation readback is not content evidence.
- Existing full-body audits may be reused only when they record that the actual body was read and provide an object-level semantic disposition.
- Do not invent facts to make a thin page look complete. External evidence enrichment is a separate bounded action with source provenance.
- Preserve Canonical IDs. Do not create duplicate pages to solve content quality.

## Content review dimensions

Every body review must inspect these dimensions:

1. **Body completeness** — empty/truncated/stub/fragment vs usable whole.
2. **Semantic integrity** — whether the body actually says what the object claims to own.
3. **Factual integrity** — unsupported assertions, obsolete claims, internal contradictions, false precision, or unsafe overclaiming.
4. **Structure and usability** — whether the content is readable, scoped, navigable, and organized for reuse.
5. **Duplication and pollution** — duplicate ownership, copied residue, project-specific contamination, reader/runtime chatter, obsolete migration notes, or mixed authority layers.
6. **Source / evidence adequacy** — whether externally dependent claims have sufficient authority, versioning, applicability, and traceability for the page's role.
7. **Staleness** — whether time-sensitive standards, product facts, software behavior, regulations, or version-dependent statements require refresh.
8. **Graph-content coherence** — whether the body meaning agrees with Domain, Level, Role, Framework Type, and typed relations.

## Content decision vocabulary

`contentDecision` is one of:

- `KEEP` — body is adequate for its current scope; no content mutation required.
- `RESTRUCTURE` — existing information is substantively adequate but organization/readability/contamination must be repaired without information loss.
- `ENRICH` — body is materially thin or lacks evidence required for its claims; add bounded evidence/content before terminal status.
- `MERGE` — current body duplicates or fragments another canonical owner; a merge/supersession decision is required before terminal status.
- `HOLD` — body cannot be safely decided because required content/evidence is unavailable, empty, truncated, conflicting, or authority is unresolved.
- `LINEAGE_ONLY` — provenance object is preserved for history/supersession and does not require Current-style enrichment, but its lineage body has been checked for integrity/preservation.

## Content state vocabulary

`contentState` is one of:

- `CONTENT_UNREVIEWED`
- `CONTENT_REVIEW_IN_PROGRESS`
- `CONTENT_REVIEWED_KEEP`
- `CONTENT_ACTION_REQUIRED_RESTRUCTURE`
- `CONTENT_ACTION_REQUIRED_ENRICH`
- `CONTENT_ACTION_REQUIRED_MERGE`
- `CONTENT_HOLD`
- `CONTENT_LINEAGE_TERMINAL`
- `CONTENT_ACTION_APPLIED_VERIFY_PENDING`
- `CONTENT_ACTION_APPLIED_VERIFIED`

Terminal states are:

- `CONTENT_REVIEWED_KEEP`
- `CONTENT_HOLD`
- `CONTENT_LINEAGE_TERMINAL`
- `CONTENT_ACTION_APPLIED_VERIFIED`

`RESTRUCTURE`, `ENRICH`, and `MERGE` are **not terminal merely because the decision was made**. They become terminal only after the required action is applied to the canonical object and independently read back/verified.

## Completion contract

For each object, the progress ledger must expose at minimum:

- `canonicalId`
- `pageId`
- `graphState`
- `graphTerminal`
- `contentState`
- `contentDecision`
- `contentTerminal`
- `bodyReadStatus`
- `bodyEvidenceRef`
- `reviewedAt`
- `reviewConfidence`
- `contentIssues`
- `requiredContentAction`
- `overallTerminal`

`overallTerminal = graphTerminal && contentTerminal`.

No aggregate completion percentage may count an object as complete when only one side is terminal.

## Review order

Default production order:

1. `CURRENT_AUTHORITY_LAYER`
2. `SUPPORT_EXTENSION_LAYER`
3. `PROVENANCE_LINEAGE_LAYER`

Within each layer, review one object at a time or in small auditable batches. Store an object-level decision for every page.

### Current

Read the complete current body. Check all eight content dimensions. `KEEP` requires affirmative body evidence, not lack of detected errors.

### Support

Apply the same body-level review, but judge adequacy against the object's bounded support role. Do not force support objects to become broad framework pages.

### Provenance

Check that lineage/history content is intact, non-corrupt, non-duplicative in a way that breaks supersession, and correctly preserved. Do not force historical objects into Current taxonomy or enrich them merely to resemble Current objects.

## Mutation discipline

- Content review itself is read-only.
- `KEEP`, `HOLD`, and `LINEAGE_ONLY` decisions may update only the progress/audit ledger unless a canonical state field explicitly requires change.
- `RESTRUCTURE`, `ENRICH`, and `MERGE` require a separate exact mutation plan with before-state guards.
- Apply canonical content mutations serially or in small bounded batches.
- Stop on first drift/failure.
- After mutation: canonical readback, derivative sync/reconcile when relevant, and independent body verification are mandatory before `CONTENT_ACTION_APPLIED_VERIFIED`.

## No-loss rule

`RESTRUCTURE` means reorganize without semantic loss. Existing valid content may be moved, split, normalized, or decontaminated, but must not be deleted merely to make the page look cleaner.

## Relationship to existing review systems

This layer does not replace Artifact Review, Design Review, Evidence Gate, Technical Review, Graph Migration validation, or the Complex Project Master Runtime. It is the body-level quality gate for the Knowledge Plane.

Graph PASS != Content PASS.

Content PASS != Design KEEP.

Content review completeness must therefore remain independently visible in the Master Runtime knowledge-plane readback.
