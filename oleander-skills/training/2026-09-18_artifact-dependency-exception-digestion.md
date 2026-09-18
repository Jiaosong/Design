# 2026-09-18｜Artifact Dependency / Required-Check Exception Digestion

Status: `DIGESTED / EXISTING OWNERS EXTENDED / MACHINE VALIDATION ADDED / AIG FAILURE REGRESSION ADDED / NO NEW FRAMEWORK`

## Question

Earlier external design-skill digestion exposed several production-integrity mechanisms:

- source identity must not collapse to path;
- generated/intermediate assets must not silently become deliverables;
- validation must distinguish PASS / FAIL / HOLD / NOT_RUN / UNVERIFIED / N/A;
- candidate identity and matched comparison fidelity must stay explicit;
- fonts/toolchain dependencies can silently change output;
- command-line “waive this check” mechanisms can hide required failures.

Existing-first review showed that OLEANDER already owns almost all of this through:

- `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1`;
- `OLEANDER_EXECUTION_RECEIPT_v1.0`;
- `artifact-review-system-v1.0`;
- Production Asset Persistence;
- Execution Integrity / dependency-digest stale propagation;
- Design Process / Computational Option Space;
- Current Architecture Decision Rights.

Therefore this batch does **not** create an execution kernel, finalizer framework, waiver registry or new validation-state family.

---

# External sources reviewed

## 1. yangcodingmaster/photo-distill

Pinned head reviewed:

`e2708aeb7db4344dfb5577b5f12bcf57ded541ec`

No readable root license was found during this review.

Research reference only; no source code/prose copied.

Relevant observed mechanisms:
- deterministic HTML/CSS/SVG source;
- Chrome render;
- machine pixel checks;
- fail/delete behavior;
- command-line `--waive` choices;
- runtime/browser/font dependency assumptions.

OLEANDER transfer:
- the deterministic/fail-closed principles were already owned by Native Artifact / Execution Receipt / Artifact Review;
- the remaining useful delta is **required dependency identity + fallback policy** and an explicit **no waiver-derived PASS** rule.

Rejected:
- free-form command-line waiver as validation authority;
- implicit browser/font environment;
- saturation-only proxy as universal quality metric;
- tool-specific finalizer architecture.

## 2. wnby/travel-photo-soft-abstraction

Pinned head reviewed:

`ae30cd1484b204c0817473f9f8b1a41889ad4fd6`

No readable root license was found during this review.

Research reference only.

Relevant mechanisms:
- original photo vs generated panel role lock;
- deterministic composition;
- source integrity comparison;
- platform-dependent font fallback;
- machine PASS while manual checks remain open.

OLEANDER transfer already owned:
- source-integrity modes;
- generated intermediate ≠ deliverable;
- typed validation;
- technical PASS ≠ Design KEEP.

Remaining useful delta:
- material font/runtime/library fallback must never be silent when reproduction or semantic fidelity is claimed.

## 3. zhu930824/poetic-line-zine-poster

Pinned head reviewed:

`f6452963581eea64f66281038deefc865e830d8a`

No readable root license was found during this review.

Research reference only.

Relevant mechanisms:
- deterministic composition/typography;
- fallback fonts;
- manual score aggregation;
- missing-source fidelity path.

OLEANDER transfer already owned:
- hard gates vs Design Review;
- missing evidence ≠ PASS;
- candidate/option comparison at matched fidelity.

Remaining useful delta:
- dependency fallback identity must be explicit when a font/runtime materially affects the artifact.

---

# Existing OLEANDER mapping

## Already mature — no new mechanism

### Source Contract

Already covered by Native Artifact source-integrity extension:

- `EVIDENCE_ONLY`;
- `DETERMINISTIC_TRANSFORM`;
- `NORMALIZED_RASTER_EXACT`;
- `BYTE_EXACT`.

Existing rule:
`PATH ≠ SOURCE IDENTITY`.

### Intermediate / deliverable boundary

Already covered by:
- `INTERMEDIATE_ONLY`;
- `CANDIDATE_ONLY`;
- `ELIGIBLE_AFTER_REQUIRED_GATES`;
- `DELIVERY_DERIVATIVE`.

Existing rule:
generative output defaults to `INTERMEDIATE_ONLY`.

### Validation result semantics

Already covered by Execution Receipt:

`PASS / FAIL / HOLD / NOT_RUN / UNVERIFIED / NOT_APPLICABLE`.

Only PASS satisfies a required check.

### Candidate identity / matched fidelity

Already covered by:
- Design Process candidate/option identity;
- concept-family distinction;
- Prototype Fidelity Matrix;
- Computational Option Space `candidate_id`;
- matched artifact comparison.

No new candidate registry is needed.

### Current / supersession

Already governed by:
- Native Artifact Contract;
- Architecture Current / Supersession projection;
- one logical object → max one owner-native Current authority.

### Persistence / hashes

Already governed by Production Asset Persistence and Artifact Review.

### Dependency drift / rollback

Already governed by Execution Integrity:
- explicit run inputs/outputs;
- digests;
- STALE / REGEN_REQUIRED / RETEST_REQUIRED / HOLD;
- baseline / rollback / change impact.

---

# Material gap 1 accepted｜Required dependency identity + fallback

Prior Native Artifact prose said external sources, fonts, runtimes and library versions should be recorded where applicable.

The missing execution rule was:

> What happens when a material dependency is absent and the producing tool silently falls back?

Implemented prospective extension:

`dependency_identity_extension`

Fields:

`dependency_id / dependency_role / requiredness / identity_or_authority_ref / version_or_revision / hash_when_material / resolution_method / fallback_policy / verification_ref`.

Requiredness:
- `REQUIRED_FOR_REPRODUCTION`
- `REQUIRED_FOR_SEMANTIC_FIDELITY`
- `OPTIONAL`

Fallback policy:
- `FORBID`
- `ALLOW_DECLARED_EQUIVALENT`
- `ALLOW_NONFINAL_PREVIEW`

Accepted invariants:

`SILENT FALLBACK = FORBIDDEN`

`MISSING REQUIRED DEPENDENCY → DELIVERY ELIGIBILITY BLOCKED`

`DECLARED EQUIVALENT → EXPLICIT IDENTITY + ACTUAL READBACK`

`PREVIEW FALLBACK ≠ FINAL NATIVE OUTPUT`

This applies to fonts, runtimes, renderers, libraries, plugins, linked native assets or other material dependencies.

It is prospective only; historical artifacts are immutable.

---

# Material gap 2 accepted｜Required-check exception firewall

Existing Execution Receipt already says only PASS closes a required check.

The missing explicit rule was:

> Can an external tool's “waive” flag or a human note convert a required FAIL/HOLD/NOT_RUN/UNVERIFIED to PASS?

Answer:

`NO`.

Implemented:

`required_check_exception_boundary_extension`.

Allowed exception effects:
- `CRITERION_CHANGED`
- `CLAIM_BOUNDARY_NARROWED`
- `CHECK_DECLARED_NOT_APPLICABLE_BY_AUTHORITY`

A material exception must bind:

`decision_object_id / criterion_ref / decision_class / actor_or_authority_ref / authorization_basis_ref_or_fields / authority_scope / claim_boundary / authority_fingerprint / exception_effect / revalidation_ref`.

Rules:
- no `WAIVED_PASS`;
- no `PASS_WITH_WAIVER`;
- no generic waiver state;
- prior FAIL/HOLD/NOT_RUN/UNVERIFIED remains historical truth;
- Project authority may not waive professional/statutory authority it does not possess;
- changed criterion or narrowed claim requires fresh validation;
- NOT_APPLICABLE requires a reason and material authority basis;
- exception record cannot grant Design KEEP / Professional PASS / statutory approval / Promotion.

This reuses Current Architecture §18 Decision Rights.

No waiver registry or new approval system is introduced.

---

# Machine enforcement

Existing owner:

`00-governance/runtime/validate_execution_contracts.py`

Added checks for:

## Native Artifact
- dependency extension exists;
- exact requiredness vocabulary;
- exact fallback vocabulary;
- prospective + immutable historical boundary;
- silent fallback forbidden;
- missing required dependency blocks delivery;
- declared equivalent requires identity + readback;
- preview fallback cannot satisfy final native output.

## Execution Receipt
- required-check exception extension exists;
- exact exception-effect vocabulary;
- no waiver-derived validation state;
- exception does not mutate prior result;
- Decision Rights basis required;
- changed criterion/claim requires fresh validation;
- exception cannot grant unrelated authority.

---

# AIG-02 regression

Added:

## FAIL-020

Required font/runtime/plugin/linked asset is absent, silent fallback occurs, artifact still claims final/reproducible/fidelity PASS.

Required response:
- identify material dependency;
- restore fallback policy;
- freeze delivery;
- if equivalent is authorized, bind identity and read back.

## FAIL-021

Required FAIL/HOLD/NOT_RUN/UNVERIFIED is converted to PASS by waiver/exception flag/note without authorized criterion/claim change + fresh validation.

Required response:
- restore historical result;
- reject waiver-derived PASS;
- resolve Decision Rights;
- rerun validation.

---

# Explicitly rejected

Do not add:
- `WAIVED_PASS`;
- waiver score;
- waiver registry;
- exception state machine;
- global dependency database;
- global font registry;
- new execution framework;
- tool-specific finalizer contract;
- mandatory atomic-rename implementation for every artifact type.

Atomic/staging behavior remains tool/adapter specific; the governance invariant is that an unvalidated candidate may not silently overwrite validated Current authority and existing rollback / partial-commit / readback rules continue to govern.

---

# Maturity

Current batch target:

`EXTERNAL PRODUCTION MECHANISMS → EXISTING OWNER MAP → TWO MATERIAL GAPS → CURRENT CONTRACT EXTENSION → MACHINE VALIDATION → AIG FAILURE REGRESSION → PR/CI/READBACK`.

No project artifact is retroactively rewritten.

`DEPENDENCY RECORDED ≠ DEPENDENCY VERIFIED`

`EXCEPTION AUTHORIZED ≠ VALIDATION PASS`

`VALIDATION PASS ≠ DESIGN KEEP`

`DELIVERY ELIGIBLE ≠ PROMOTED`.
