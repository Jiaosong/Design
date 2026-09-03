# OLEANDER Anti-Pollution Protocol v1.0

Status: CANDIDATE GOVERNANCE / PROJECT-WIDE HARD CONSTRAINT
Effective: 2026-09-04
Scope: Entire OLEANDER project, all Projects / Workstreams / Skills / Knowledge / GitHub / Notion / Drive / generated artifacts / validation systems.
Role: Cross-project anti-pollution constraint. It does not replace the Knowledge Axis, Project Axis, Case Axis, Work Coordination Contract, Artifact Review System, or any project-specific Source Authority.

## 0. Purpose

Prevent OLEANDER from accumulating parallel authorities, duplicate frameworks, stale CURRENT objects, unverified capability claims, orphan assets, transient runtime residue, or knowledge-base contamination while preserving all valid historical evidence.

This protocol makes the existing no-loss / no-pollution rule operational and machine-checkable.

Core rule:

> **ONE LOGICAL OBJECT → ONE CURRENT AUTHORITY → MANY TRACEABLE VERSIONS / EVIDENCE CHILDREN.**

A revision, experiment, validation receipt, render, export, branch, deployment, model derivative, temporary dataset, AI summary, or CI artifact must not become a second Current authority for the same logical object.

## 1. Authority states

Every material OLEANDER object must resolve to exactly one authority state before it may be written into a Current surface:

- `CURRENT` — unique authoritative object currently governing work.
- `CANDIDATE` — proposed replacement/extension; cannot self-promote.
- `EXPERIMENTAL_UNVERIFIED` — implementation or hypothesis exists, but required validation is incomplete.
- `VALIDATION_PENDING` — validation is actively defined/running but not yet closed.
- `VALIDATED_FOR_BOUNDED_SCOPE` — real evidence exists for an explicitly bounded claim; this is not general parity.
- `SUPPORT` — valid supporting evidence/output, not Current authority.
- `PROVENANCE` — immutable historical lineage/evidence.
- `LEGACY` — historical object retained for audit/compatibility only.
- `SUPERSEDED` — replaced by a named successor; no longer writes Current state.
- `REJECTED_WITH_REASON` — explicitly rejected and retained only as traceable evidence.
- `HOLD` — unresolved conflict, ambiguity, missing evidence, or authority collision blocks promotion/mutation.

No object may simultaneously be `CURRENT` and `CANDIDATE`, `CURRENT` and `LEGACY`, or `CURRENT` and `SUPERSEDED`.

## 2. The only permitted promotion chain

Default promotion chain:

`EXPERIMENTAL_UNVERIFIED → VALIDATION_PENDING → VALIDATED_FOR_BOUNDED_SCOPE / REVIEW → CANDIDATE → explicit promotion decision → CURRENT → readback`

A project may omit stages only when they are genuinely not applicable, but it may never skip the evidence or authority checks represented by those stages.

Hard rules:

1. File existence is not validation.
2. Code/CI PASS is not design quality PASS.
3. Render PASS is not artifact review PASS.
4. One bounded test is not general capability parity.
5. Candidate success is not Current promotion.
6. Merge is not enough; Current promotion requires post-merge/readback where applicable.
7. Notion/GitHub/Drive copies do not independently become co-equal Current authorities.

## 3. One Current rule

For every logical object, resolve:

- `PROJECT_ID`
- `OBJECT_ID`
- `OBJECT_TYPE`
- `SOURCE_AUTHORITY`
- `CURRENT_NATIVE_MASTER`
- `CURRENT_LOCATION`
- `CURRENT_OWNER`
- `CURRENT_REVISION`
- `CANDIDATE_FRONTIER` when present
- `SUPERSEDES / SUPERSEDED_BY` when applicable

A new revision must reuse the same `OBJECT_ID` unless the design scope materially changes.

If a repair can be done in place, do not create a parallel replacement page/file/project/database/Skill/framework.

If two objects claim Current authority for the same logical identity, all writes enter `HOLD` until GOVERNANCE resolves the collision.

## 4. Existing Mature First / No duplicate framework

Before adding a new Skill, framework, workflow, database, registry, template, validation gate, project axis, naming system, automation, runtime subsystem, or knowledge taxonomy:

1. Search existing OLEANDER GitHub and Notion authorities.
2. Identify whether an existing object already covers the function.
3. Prefer in-place extension, adapter, composition, migration, or repair.
4. Create a new framework only when the existing object cannot absorb the requirement without semantic corruption.
5. Record the reason for the new object and what existing object it does not duplicate.

Default decision rule:

> If an existing mature OLEANDER object covers the same authority role or approximately 60%+ of the required capability, extend/adapt it instead of creating a parallel system.

A new name does not justify a new framework.

## 5. Candidate isolation

Candidate work must be isolated from installed Current authority.

Candidate requirements:

- explicit Candidate location/branch/page state;
- explicit upstream Current authority;
- explicit claim boundary;
- explicit validation requirement;
- explicit promotion gate;
- no automatic overwrite of Current;
- no automatic propagation into knowledge summaries as established fact;
- no Notion Current status update based only on Candidate evidence;
- no production deployment replacing Current without explicit promotion.

Candidate branches may contain experiments, but all unvalidated frontier items must be listed in a machine-readable frontier registry or equivalent project control card.

## 6. Unverified work isolation

`EXPERIMENTAL_UNVERIFIED` and `VALIDATION_PENDING` material must never be mixed indistinguishably with validated Current content.

At minimum it must expose:

- `STATE`
- `OWNER`
- `UPSTREAM_MASTER`
- `CLAIM`
- `NON_CLAIMS`
- `VALIDATION_REQUIRED`
- `PROMOTION_ALLOWED = false`

Until validation closes, it may not:

- appear in Current capability matrices as validated;
- create a final validation receipt;
- replace an existing Current object;
- be copied into Notion as established knowledge;
- be used to remove an existing blocker;
- be presented as general parity or production readiness.

## 7. Receipt discipline

A validation receipt is evidence, not a new framework and not a new Current.

A receipt may be created only after the referenced validation has actually completed.

Every receipt must bind:

- logical object/capability ID;
- tested revision/commit/source hash;
- tool/kernel/runtime versions where relevant;
- validation run/job or equivalent evidence locator;
- PASS/FAIL/HOLD result;
- bounded scope;
- non-claims;
- invalidation rule;
- downstream status change, if any.

No receipt may claim more than the validation proved.

## 8. GitHub pollution controls

GitHub rules apply project-wide:

- one logical capability must not generate an indefinitely growing family of one-off workflows when a reusable runner/matrix fits;
- diagnostic workflows are temporary and must be removed or archived after the root cause is resolved;
- feature branches that materially diverge from `main` must not be promotion-ready until synchronized and read back;
- PR titles/bodies must reflect the actual Current candidate scope; stale PR authority text is a governance failure;
- generated runtime residue, temporary archives, caches, local-only binaries, screenshots without purpose, and duplicate exports must not be committed into authoritative paths;
- historical evidence remains in Git history, receipts, or archive rather than duplicated as parallel Current files;
- workflow PASS cannot silently update a professional/design capability to PASS without the governing status file and bounded receipt rules.

## 9. Notion / knowledge-base pollution controls

Notion and other knowledge surfaces must preserve semantic identity.

Do not create a new page/database when the logical object already exists and can be repaired in place.

Forbidden Current pollution includes:

- raw chat transcripts;
- prompt text;
- temporary AI summaries treated as canonical knowledge;
- CI logs copied as knowledge prose;
- duplicate pages with slightly different names;
- empty placeholder pages without a declared purpose/state;
- orphan pages without canonical parent/path;
- Candidate claims written as established facts;
- old and new taxonomies both presented as Current;
- migration remnants left active after a replacement is authoritative.

Valid provenance may be preserved in dedicated evidence/migration/archive fields or locations without deleting information.

Before a page is `CLEAN`, apply the Work Coordination Contract cleanup criteria and verify Current / Support / Practice / Provenance / Legacy / Superseded relationships.

## 10. Asset pollution controls

Every material asset must have a role:

- Native Master
- Current Derivative
- Validation Evidence
- Support
- Provenance
- Temporary / Disposable

Temporary files must not be promoted merely because they exist.

Do not keep multiple indistinguishable exports when one canonical export plus hash/version history is sufficient.

Binary production assets follow the Production Asset Persistence Gate; `/tmp`, sandbox, signed URLs, CI artifacts, previews, or checksum-only records are not durable Current storage.

## 11. Project / case / naming pollution controls

The existing Knowledge, Application, Project, Case, Delivery Priority, Claims, IP, and AI Governance namespaces remain authoritative.

Do not invent a new ID axis for a local task when an existing axis applies.

Historical aliases may remain immutable provenance but must not regain Current authority.

Project-specific shorthand must not silently become a new cross-project ontology.

## 12. Automation / training pollution controls

Recurring automations and training must update existing systems rather than create a new page/framework each run.

A recurring run must prefer:

`read Current → identify delta → repair/extend in place → validate → write only material delta`

If there is no material delta, do not create a new artifact merely to prove the automation ran.

Training findings remain Candidate until validated by project use/evidence; training must not silently rewrite Current professional claims.

## 13. Cross-surface synchronization

GitHub, Notion, Drive, deployment surfaces, and local/native masters may hold different representations, but only one Source Authority governs each claim/object type.

When a Current authority changes:

1. update the authoritative source;
2. update dependent indexes/registries;
3. mark old representations `SUPERSEDED / SUPPORT / PROVENANCE` as appropriate;
4. read back downstream surfaces;
5. resolve stale links/aliases;
6. only then close the handoff.

`SYNCED COPY ≠ CO-EQUAL AUTHORITY`.

## 14. Mandatory anti-pollution preflight

Before every material write, ask:

1. What existing OLEANDER object already owns this function?
2. What is the one Current authority?
3. Am I editing the existing logical object or accidentally inventing a duplicate?
4. Is this Current, Candidate, Experimental, Evidence, Support, or Provenance?
5. Has the claimed result actually been validated?
6. Does this change create a new framework/workflow/database/page when extension would suffice?
7. Does it introduce a new ID/name/axis that conflicts with existing namespace authority?
8. Will it leave an orphan, stale duplicate, empty placeholder, or parallel Current?
9. If it changes authority, what must be superseded/read back?
10. Is there a material delta worth persisting?

Any unresolved answer that can affect authority or identity results in `HOLD` rather than a speculative write.

## 15. Promotion blockers

Promotion to Current is blocked if any applicable condition is true:

- more than one Current authority exists for the logical object;
- Candidate is stale against its upstream Current;
- unverified frontier work is mixed into the promoted package;
- required validation/readback is pending;
- PR/control-card/registry authority text is stale;
- receipt is absent or overclaims the evidence;
- duplicate framework/workflow/database/page was introduced without explicit justification;
- unresolved Notion/GitHub identity mismatch exists;
- required native master/durable asset is missing;
- supersession relationship is unresolved;
- material blockers were removed only because a test artifact exists.

## 16. Repair, not deletion

Anti-pollution cleanup follows NO COMPRESSION / NO LOSS.

When pollution is found:

1. identify the canonical logical object;
2. preserve unique valid information;
3. merge/repair identity in place where possible;
4. demote duplicates to `PROVENANCE / LEGACY / SUPERSEDED` or archive them;
5. remove only redundant transient infrastructure after its evidence value is preserved;
6. repair links/relations/indexes;
7. rerun validation/readback;
8. record the migration/audit result.

Do not solve pollution by deleting unique evidence or collapsing independent design content.

## 17. Default enforcement

This protocol is inherited by all OLEANDER projects and all future work unless a later explicit Master Governance revision supersedes it.

Project-specific rules may be stricter but may not weaken:

- one Current authority;
- Candidate isolation;
- unverified-work isolation;
- no duplicate framework by default;
- bounded-claim discipline;
- no-loss cleanup;
- explicit promotion/readback.

When project instructions conflict, the newest explicit Master Governance / user instruction wins, and the conflict must be recorded rather than silently creating a parallel rule set.
