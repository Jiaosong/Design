# 2026-09-18｜External Visual Execution Skills Digestion

Status: `DIGESTED / EXISTING-OWNER MAPPED / MACHINE CONTRACT DELTA / NO NEW SKILL / NO NEW METHOD / NO NEW FRAMEWORK`

## Sources reviewed

1. `TwentyfiveBTea/ink-wash-poster`
2. `wnby/paper-spirit-zine`
3. `luckdvr/photo-riso-poster`
4. `wnby/photo-relic-editorial`
5. `zhu930824/poetic-line-zine-poster`
6. `dacnay816y62-hub/photo-revival`
7. `TanShilongMario/visual-memory-translator-SKILL`
8. `TwentyfiveBTea/8bit-pixel-art`
9. `yangcodingmaster/photo-distill`
10. `wnby/travel-photo-soft-abstraction`
11. `JustinQiuck/dynasty-aesthetics`
12. `zhouaria28-cloud/photo-ink-echo`

Deep code review focused on `photo-distill`, `travel-photo-soft-abstraction`, `poetic-line-zine-poster` and `visual-memory-translator-SKILL`.

No third-party code is copied into OLEANDER. Repositories without a clear root license are treated as research references only; AGPL repositories are not copied into the OLEANDER runtime. The accepted delta is mechanism-level and is implemented in OLEANDER-owned contracts.

## Existing-first finding

OLEANDER already owns most of the useful reasoning:

- `oleander-design-process` already carries `SOURCE / OBSERVATION → FINDING → RELATION / FAILURE MODE → DESIGN CONSEQUENCE → TESTABLE DESIGN VARIABLE`;
- `oleander-image-art-direction` already requires real source identity, derivative records, truth-preserving crop/tone/composite operations and rejects silent generative replacement;
- `oleander-visual-design` already requires editable/vector formal text where delivery control matters;
- `oleander-delivery-qc` already separates export/release inspection from Design Review;
- Native Artifact / Execution Receipt / Resolver already separate artifact existence, readback, regression, Design Review, Current and Promotion.

Therefore the external repositories do **not** justify a new visual-translation Skill, a new execution kernel Skill, a new router, a new Project State or a new aesthetic framework.

## Material mechanisms accepted

### 1. Source-integrity level must be explicit

External implementations exposed several materially different meanings of “preserve the source”:

- source informs the design but does not appear in the output;
- source is transformed only by reproducible crop/resize/coordinate operations;
- source is normalized first and the resulting raster must remain pixel-exact;
- source file bytes must remain hash-exact.

Accepted OLEANDER vocabulary:

`EVIDENCE_ONLY / DETERMINISTIC_TRANSFORM / NORMALIZED_RASTER_EXACT / BYTE_EXACT`.

A path is not identity. A source-preservation claim needs an authority reference and/or hash plus an actual verification record.

Owner: `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1`.

### 2. Intermediate and deliverable are different dimensions

The strongest external pipeline pattern is:

`source → bounded intermediate → deterministic composition → validation → finalization`.

Generated panels, temporary renders, image-model outputs, textures and atmosphere images are support artifacts unless the explicit task itself requires a generated-image final.

Accepted prospective delivery vocabulary:

`INTERMEDIATE_ONLY / CANDIDATE_ONLY / ELIGIBLE_AFTER_REQUIRED_GATES / DELIVERY_DERIVATIVE`.

This is independent of `CURRENT / SUPERSEDED / HISTORY / HOLD`. Current does not mean delivery-ready, and delivery-ready does not grant Promotion.

Owner: `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1`.

### 3. Deterministic-first remains the production default

Useful external separation:

- non-deterministic generation may produce a bounded visual subasset;
- typography, dimensions, grid, labels, composition, source placement and final export should use deterministic/native production when those properties must be exact.

This is a reinforcement of existing OLEANDER native-output/editability rules, not a new method.

Owners: `oleander-design-process`, `oleander-visual-design`, `oleander-image-art-direction`, `oleander-delivery-qc`.

### 4. Fail-closed finalization is useful only inside the existing gates

The external `photo-distill` and `travel-photo-soft-abstraction` implementations correctly prevent a failed candidate from silently surviving as the deliverable.

OLEANDER transfer:

`candidate → technical validation → actual readback → applicable review → finalization`.

A failed required check cannot become the final native output. This does **not** mean a machine finalizer can award Design KEEP, Field PASS or Promotion.

Owner: existing Resolver + Native Artifact + Execution Receipt + downstream QC.

### 5. Validation needs typed non-success states

External code exposed a dangerous failure mode: a missing comparison or optional input can become boolean `true`, even though the claimed condition was never verified.

Accepted result vocabulary:

`PASS / FAIL / HOLD / NOT_RUN / UNVERIFIED / NOT_APPLICABLE`.

Rules:

- only PASS satisfies a required check;
- NOT_RUN means applicable but not executed;
- UNVERIFIED means available evidence cannot establish the claim;
- NOT_APPLICABLE requires a concrete reason;
- missing evidence never defaults to PASS;
- Technical PASS remains separate from Design KEEP and Promotion.

Owner: `OLEANDER_EXECUTION_RECEIPT_v1.0`.

## Mechanisms already present and therefore not duplicated

### Source → relation → design consequence

The external family repeatedly uses variants of:

`SOURCE FACT → RETAINED RELATION → ABSTRACT / DESIGN MARK`.

OLEANDER already has the stronger cross-domain form in `oleander-design-process`. No second visual-specific relation framework is created.

### Source / style / support role separation

External pipelines distinguish user content evidence, style references and generated panels. OLEANDER already has Source Authority, Native Artifact roles, provenance vocabulary and image-consumption identity. No parallel asset-role registry is created.

### Router / preset separation

`visual-memory-translator-SKILL` demonstrates useful parameter separation, but it is largely Markdown-driven rather than a typed execution router. OLEANDER already has the Default Skill Resolver, Capability Contract, Minimum Sufficient Owner Set and Tool Adapter Contract. No new visual router is created.

## External implementation defects retained as failure knowledge

These are useful because they expose what OLEANDER must avoid:

1. **Fail-open source fidelity** — a missing source comparison must not return PASS.
2. **Sampling-driven design distortion** — validator sampling positions must not become hidden composition rules.
3. **Manual score theatre** — a weighted calculator fed by human scores is not an automatic design validator.
4. **Partial corner check bug** — checking the second-lowest corner error can allow two heavily contaminated corners to pass.
5. **Font fallback drift** — Consolas / Menlo / DejaVu fallback means the same command is not cross-environment reproducible typography.
6. **Raster-only “deterministic type”** — deterministic raster text is not an editable/vector master.
7. **Hue circularity bug** — ordinary percentile math across 359°/0° hue wrap can misreport one hue family as extreme variation.
8. **Boolean PASS compression** — machine layout checks, manual aesthetic review and promotion authority cannot share one undifferentiated PASS.
9. **Validator-shaped composition** — implementation convenience must adapt to design requirements, not the reverse.
10. **Style defaults promoted to method** — ivory paper, 3:4/9:16, archive numbering, poetic microcopy, riso/watercolor and extreme whitespace remain style-local, not OLEANDER defaults.

## Style-specific material not transferred into Core

The following remain reference/style knowledge only:

- watercolor / ink-wash / risograph / pixel-art surface language;
- warm ivory paper;
- fixed whitespace percentages;
- fixed 3:4 / 9:16 output ratios;
- archive numbering and fake-document microtype;
- poetic English/Chinese title conventions;
- animal/metaphoric afterimage recipes;
- dynasty-specific palette/composition motifs;
- travel-zine diptych as a universal layout.

They may be useful when a project explicitly calls for them, but they cannot bias unrelated architecture, product, UI, technical drawing or editorial work.

## Current implementation delta

Prospective, no historical rewrite:

- `00-governance/runtime/OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1.md/.json`
  - source-integrity modes;
  - delivery-eligibility boundary;
  - generative output defaults to intermediate-only.
- `00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.md/.json`
  - typed validation result vocabulary;
  - NOT_RUN / UNVERIFIED may not become PASS.
- `00-governance/runtime/validate_execution_contracts.py`
  - machine regression for the new contract semantics.

No Skill count, owner map, lifecycle state, Project State, resolver owner set, Notion domain or Promotion authority is changed.

## Regression targets

The contract must reject or expose:

- path-only identity presented as source proof;
- a source-integrity claim without declared mode/boundary;
- generative intermediate treated as the final editable/native deliverable by default;
- NOT_RUN / UNVERIFIED collapsed to PASS;
- missing source comparison treated as fidelity PASS;
- delivery eligibility treated as Promotion;
- style presets treated as global OLEANDER design rules.

## Maturity boundary

Current state:

`EXTERNAL MECHANISMS DIGESTED → EXISTING OWNER MAPPING COMPLETE → PROSPECTIVE MACHINE CONTRACT DELTA IMPLEMENTED → CI/REGRESSION REQUIRED → REAL PROJECT REAPPLICATION REQUIRED`.

This is not yet a new Golden reusable success claim. Promotion of the absorbed mechanisms requires real project use with an actual artifact chain, readback, at least one typed non-PASS path, repair/retest where available, and confirmation that the added semantics improve execution without adding framework burden.

`CONTRACT PASS ≠ PROJECT USAGE EVIDENCE ≠ DESIGN KEEP`.
