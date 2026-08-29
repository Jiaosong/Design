# OLEANDER VALIDATION — Named Dieline Layer vs ISO 19593 Processing Steps

Status: `PRACTICE_EVIDENCE / SUPPORT / SCOPED / NO_PROMOTION`

## Gap

The new Packaging Structure + Dieline Candidate correctly requires semantic panel/cut/crease/glue/lock identity rather than relying on line appearance alone. The unresolved validation question is narrower: does a PDF Optional Content Group (layer) named `Cutting` itself prove standardized packaging-processing semantics?

## Existing owners / current comparison

- Design intent owner: `oleander-design-process/PACKAGING_STRUCTURE_DIELINE_EXTENSION.md`.
- Print/preflight owner: `oleander-delivery-qc/PRINT_PRODUCTION_PREFLIGHT_EXTENSION.md`.
- This Practice does not create a new validator or Skill identity.
- Project Priority Queue remains owned by PRESENTATION for `PRJ-C04-DIGITAL-INTERACTION`; no Project Current was modified.

## Current external source state — 2026-08-29

- Current published ISO source checked: `ISO 19593-1:2018`; ISO states this published version remains current after review/confirmation, while the second edition is still in approval / PRF state and is not treated here as the current published standard.
- Ghent Workgroup (GWG) Processing Steps Test Suite V1.0 is the strongest discovered implementation-oriented validation source. GWG describes the suite as testing application compatibility with Processing Steps and provides interactive/automated tests.
- GWG also describes the pre-standard failure mode: packaging processing information carried ad hoc through layer/separation naming could be misinterpreted; Processing Steps standardizes the communication.
- Rights boundary: GWG retains IP in its sample files; its published terms permit testing/development use but restrict modification. No GWG binary sample was copied, modified, redistributed, or committed in this Practice.

## Capability probe / actual artifact

Runtime used for the executed local probe:

- PyMuPDF `1.26.7`
- MuPDF `1.26.12`
- Poppler `pdfinfo 25.06.0`

`generate_and_validate_named_ocg.py` creates an actual PDF containing one generic Optional Content Group named `Cutting`, draws one line in that OCG, saves the PDF, reopens it, and inspects the OCG object/catalog.

The executed artifact was:

- `A_named_cut_layer_only.pdf`
- SHA256: `1faaf995f003d02b5316e7364d91cb20327d5424c1ab725d8b7cde3c49b70a42`
- The binary is not committed here; the generator and structured readback are committed so the fixture is reproducible without redistributing a third-party sample.

## Reopen / readback

After save/reopen:

- OCG count = `1`
- name = `Cutting`
- intent = `View`
- usage = `Artwork`
- catalog contains `OCProperties`
- the raw OCG object is a normal `/Type /OCG` object with `/Name (Cutting)` and generic artwork usage.

The local raw-term diagnostic found `Cutting` in the PDF, while the tested fixture contained no independently established Processing Steps conformance evidence. The diagnostic term counts are recorded only as fixture observations; they are **not** an invented ISO syntax validator and are not sufficient for conformance checking.

## PROVEN

1. A real generic PDF OCG can be named `Cutting` and survive save/reopen with its layer identity intact.
2. Therefore `LAYER EXISTS + NAME LOOKS STRUCTURAL + ROUNDTRIP PASS` is not sufficient evidence for a standardized Processing Steps claim.
3. The new OLEANDER Candidate boundary is directionally correct: line style or human-readable layer naming cannot substitute for validated semantic processing identity.

## NOT PROVEN / HOLD

- ISO 19593-1 conformance of the generated fixture: **NOT PROVEN**.
- A current compliant Processing Steps `Cutting` object was not synthesized from guessed PDF dictionary keys; the Anti-Invention gate forbids doing so without authoritative syntax/test evidence.
- RIP/vendor interpretation, converting-machine behavior, supplier production approval, physical cutting/creasing/folding, PDF/X job compliance and project-specific dieline authority remain **HOLD**.

## Repair / retest requirement

A PASS-capable A/B retest must use either:

1. an **unmodified official GWG compliant Processing Steps sample/test-suite artifact** under its stated testing-use rights; or
2. an ISO 19593 writer whose output is independently validated with the current GWG test suite or equivalent authoritative validator.

Then compare the generic named-layer fixture against the compliant artifact through real reopen/preflight/tool interpretation. Until that exists, do not promote a layer-name heuristic into OLEANDER Current knowledge or an ACTIVE validator.

## Transfer boundary

Candidate rule for transfer, not Current promotion:

`DIELINE VISUAL/LAYER NAME → GENERIC OCG IDENTITY → PROCESSING-STEP SEMANTIC EVIDENCE → AUTHORITATIVE VALIDATOR/TEST SUITE → PRODUCTION-SPEC COMPARISON`.

Maturity remains `PRACTICE_EVIDENCE`. Formal Knowledge dedupe, Canonical/Source/Method relations, migration closure and any future Current promotion remain with KNOWLEDGE.
