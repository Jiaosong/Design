# OLEANDER VALIDATION — PDF Processing Steps semantic boundary

Status: `PRACTICE_EVIDENCE / SUPPORT / SCOPED / NO_PROMOTION`

## Gap

A generic dieline layer/OCG can look structurally meaningful without carrying validated Processing Steps semantics. Prior evidence proved that a generic OCG named `Cutting` survives reopen. This extension tests a narrower material delta: whether a generic OCG and an OCG carrying Processing-Steps-like metadata remain structurally distinguishable after a real save/reopen roundtrip.

## Existing owner / frontier

- Existing validator owner: `oleander-delivery-qc` / `PRINT_PRODUCTION_PREFLIGHT_EXTENSION.md`.
- Existing packaging design intent: `oleander-design-process/PACKAGING_STRUCTURE_DIELINE_EXTENSION.md`.
- Same Practice frontier / PR #446; no parallel validator or Skill identity.
- Project Queue object `PRJ-C04-DIGITAL-INTERACTION` remains outside VALIDATION ownership, so no Project Current is modified.

## Current source state — checked 2026-08-29

- ISO currently exposes Edition 2 as `ISO/PRF 19593-1`, stage 50.20 / approval, planned publication 2026-10; it explicitly states it will replace `ISO 19593-1:2018`. Therefore the PRF is not treated as a published Current standard.
- GWG currently states that its downloadable Processing Steps sample files are fully compliant with ISO 19593-1, and its Processing Steps Test Suite v1 is intended to validate implementations/PDF files.
- An implementation example in public repository `mako-team/GetProcessingSteps` was used only as a supplemental capability reference for field-name discovery. It is not treated as normative authority or a conformance validator. No third-party code or sample binary is copied into this Practice.

## Actual A/B artifact

Runtime:

- PyMuPDF `1.26.7`
- MuPDF `1.26.12`

Fixture A: one generic Optional Content Group named `Test Processing Step`, containing a line.

- `A_generic_ocg.pdf`
- SHA256 `9153870038caa8b7b8042b9d162e9bfe2f654bb56c63a656f6db21dd6f6289ff`

Fixture B: same bounded geometry and OCG plus a **TEST FIXTURE ONLY** metadata dictionary using the discovered field names `GTS_Metadata / GTS_ProcStepsType / GTS_ProcStepsGroup` with exercise values `Cutting / Structural`.

- `B_processing_metadata.pdf`
- SHA256 `a0728d1eae606e2f92b6f5592b058e9e712ec2b069b2fc0f96aeb5a5ac9068db`

The B dictionary is deliberately not described as normative ISO syntax. It is a reproducible structure probe only.

## Reopen / readback

After save/reopen:

- A: OCG present; `OCProperties` present; no `GTS_Metadata` or processing-step type/group terms.
- B: OCG present; `OCProperties` present; `GTS_Metadata` present; `GTS_ProcStepsType /Cutting` present; `GTS_ProcStepsGroup /Structural` present.
- The metadata-bearing object therefore remains machine-distinguishable from the generic OCG in this PyMuPDF roundtrip.

## PROVEN

1. Generic OCG identity and additional metadata-bearing OCG identity are separable validation layers.
2. In this bounded PyMuPDF 1.26.7 / MuPDF 1.26.12 fixture, the added metadata dictionary survives save/reopen.
3. Therefore a validator can defensibly require evidence beyond the human-readable layer name before even attempting a Processing Steps claim.

## NOT PROVEN / HOLD

- ISO 19593-1 conformance: **NOT PROVEN**.
- GWG Processing Steps Test Suite pass: **NOT PROVEN**.
- The hand-authored B dictionary is not an authoritative ISO writer output and must not be promoted as the standard's required syntax.
- RIP/vendor interpretation, PDF/X job compliance, converting-machine behavior, physical cutting/creasing/folding, supplier approval, and project-specific dieline authority remain **HOLD**.

## Transfer / cooldown

Candidate transfer boundary only:

`DIELINE VISUAL/LAYER NAME → GENERIC OCG → PROCESSING-STEP METADATA EVIDENCE → AUTHORITATIVE WRITER/TEST SUITE → PRODUCTION-SPEC COMPARISON`.

Repeating hand-authored metadata fixtures is now cooldown. The next material delta requires an **unmodified official GWG compliant sample**, a real ISO 19593 writer output, or authoritative Processing Steps test-suite execution.

Maturity remains `PRACTICE_EVIDENCE`. KNOWLEDGE retains dedupe, relation closure, migration closure and any Current promotion decision.
