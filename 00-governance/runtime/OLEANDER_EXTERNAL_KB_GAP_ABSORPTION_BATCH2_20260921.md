# OLEANDER External Mature-KB Gap Absorption｜Batch 2｜2026-09-21

Status: `MATERIAL DELTA / ARCHITECTURE CURRENT STRENGTHENED / NO NEW STAGE / NO PROMOTION CLAIM`

## Gap selection

Second-pass deduplication showed that Physical Product / DFM-DFA / GD&T / Inclusive Design / Human Factors already have substantive owners. New pages there would be duplicate coverage.

Two remaining execution gaps were material:

1. Architecture in-use / post-occupancy evidence was present in scattered methods and G9 language but lacked a first-party professional source explicitly binding early performance targets, risk management, handover, in-use measurement and feedback.
2. Construction specification existed as domain/product content, but there was no narrow reusable METHOD owning requirement writing, responsibility, drawing/model/schedule coordination, classification/versioning, revision, issue and cross-carrier readback.

## New L6 SOURCE objects

- `SRC-RIBA-PLAN-FOR-USE-001` — Notion `3e1b86be-5c47-81af-9a60-e4f08e4151ef`.
- `SRC-NBS-SPECIFICATION-WRITING-2025-001` — Notion `3e1b86be-5c47-81e5-acbd-d07cad373fde`.
- `SRC-NBS-UNICLASS-CURRENT-001` — Notion `3e1b86be-5c47-81c8-969f-ce3e77fc67b9`.

All remain `L6 SOURCE / SUPPORT / SCOPED / UNVERIFIED`.

## Existing owner reused for in-use / POE

`MTH-DESIGN-EVIDENCE-BASED-DESIGN-001` remains the METHOD owner.

Absorbed relation:

`OUTCOME / TARGET → PERFORMANCE RISK → DESIGN / CONSTRUCTION FIDELITY → HANDOVER / USER-OPERATOR READINESS → IN-USE MEASUREMENT → GAP / ALTERNATIVE EXPLANATION → FINE-TUNE / PROJECT REOPEN → G9 LEARNING CANDIDATE`.

Hard boundary: `POE RESULT ≠ CAUSAL PROOF`.

## New narrow L5 METHOD

`KN-METHOD-CONSTRUCTION-SPECIFICATION-COORDINATION-001` — Notion `3e1b86be-5c47-8109-b043-f638e93ba5f2`.

Scope only:

`REQUIREMENT ID → INTENT / PERFORMANCE → RESPONSIBILITY → SPEC TEXT → DRAWING / MODEL / SCHEDULE → EVIDENCE / ACCEPTANCE → REVISION / ISSUE → READBACK`.

It does not own contract interpretation, code compliance, product compliance, technical drawing geometry, domain engineering or field truth.

## Architecture Current delta

File:
`00-governance/architecture-design-development-process-v1.0.md`

Branch-base:
`main@f124939df2a46372bc7559729a1bc0062e20c0d4`.

Delta commit:
`867b1864b8328594b6428b3927457d09e42a495d`.

No `ADD-18` or external stage numbering was created.

Added:
- RIBA Plan for Use / EBD in-use continuity;
- specification responsibility + cross-carrier coordination;
- versioned external classification boundary;
- actual issue/readback/reopen rules for drawing/model/schedule/spec and post-occupancy evidence.

## Deliberately not duplicated

No new Physical Product, Ergonomics, Inclusive Design, POE or Technical Drawing core owner was created.

Existing owners retained:
- Evidence-Based Design for post-use measurement logic;
- Technical Drawing Translation for graphic/native drawing carrier;
- domain professional processes for requirement truth;
- project-authorized CAD/BIM/specification owner for native project information.

## Claim ceiling

`SOURCE ABSORBED ≠ CURRENTIZATION OF SOURCE`  
`PLAN FOR USE ≠ RIBA STAGE ADOPTION`  
`SPECIFICATION COORDINATED ≠ CONTRACT INTERPRETATION ≠ CODE / PRODUCT COMPLIANCE`  
`IN-USE READBACK ≠ CAUSAL PROOF`  
`ARCHITECTURE CURRENT ≠ FIELD / OPERATION / PROFESSIONAL TRUTH WITHOUT REQUIRED OWNER EVIDENCE`

## Closure condition

Close this batch only after:
1. branch exact readback;
2. changed-file scope check;
3. OLEANDER CI/governance PASS;
4. merge;
5. main exact readback;
6. Notion central migration log sync.
