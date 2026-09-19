# 2026-09-19｜Systems Engineering Candidate Adoption｜C04 Digital Companion

Status: `CANDIDATE R-E PROCESS / MACHINE DEFINITION ALREADY CURRENT-IN-MAIN AS CANDIDATE / C04 PROJECT REAPPLICATION ADDED / REQUIREMENT→ARCHITECTURE→V&V TRACE EXERCISED / HOLD PRESERVED / NO PROMOTION`

## Existing-first finding

The repository already contained:
- `00-governance/systems-engineering-design-process-v1.0-CANDIDATE.md`;
- `00-governance/schemas/systems-engineering-design-process.v1.candidate.json`;
- Requirement Verification Traceability extension;
- Information Requirement / Exchange Contract extension;
- System Interface / Coupling extension;
- AIG-02 failures for verification-vs-validation collapse and Systems Engineering super-authority.

Therefore this batch does **not** add another Systems Engineering process.

The material gap was candidate adoption evidence:

`CANDIDATE PROCESS EXISTS → PROJECT INSTANCE → REQUIREMENT TRACE → CONFIGURATION-BOUND VERIFICATION → VALIDATION SEPARATION → INTERFACE FAILURE → CHANGE/REOPEN → CI`.

---

# C04 system of interest

Bounded system:

`C04 DIGITAL COMPANION SYSTEM`

Inside current exercise:
- digital interaction/state logic;
- APP_GAME_MAP prototype;
- local-device memory;
- route/read/book/service presentation;
- browser runtime required for actual interaction.

Outside / external authority:
- physical route/landscape;
- paper signage/map;
- human service;
- official operating-status source;
- field safety;
- survey/GPS authority;
- HCD/user research/accessibility.

System invariant:

`DIGITAL SUPPORT LAYER ≠ ROUTE / SAFETY / FIELD / OFFICIAL-SERVICE AUTHORITY`.

---

# Requirement baseline exercised

Produced:

`C04_SYSENG_REQUIREMENT_TRACE_VV_v0.1.json`

Six bounded requirements:

## C04-SYSREQ-001 — UNKNOWN fail-closed

Source:
- Digital-Off state rule;
- current APP SERVICE/RETURN representation.

Verification:
`PASS` by source/static artifact inspection.

Validation:
`NOT_RUN`.

Boundary:
live/representative operational use is not proven.

## C04-SYSREQ-002 — Digital must not be a single point of failure

Route / safety / return / core observation are allocated outside the app.

Digital-side allocation:
supported.

Integrated physical/paper/human fallback:
`HOLD`.

Validation:
`NOT_RUN`.

This is the primary project example that:

`COMPONENT / ALLOCATION PASS ≠ INTEGRATED SYSTEM PASS`.

## C04-SYSREQ-003 — No pseudo-live status

Current prototype:
- official interface required for live service;
- pseudo-live status prohibited;
- current UI reports UNKNOWN / unconfirmed.

Verification:
`PASS` within the explicit non-live prototype claim.

Future official live integration:
outside current claim / must reopen.

## C04-SYSREQ-004 — Map remains relational / NTS

Current map explicitly states:
- relational / not survey;
- no measured distance / slope / precise coordinate claim;
- no GPS authority.

Verification:
`PASS` for claim boundary.

User interpretation validation:
`NOT_RUN`.

## C04-SYSREQ-005 — My Book remains local-only prototype

Current source:
- localStorage;
- no login/cloud/GPS claim;
- no reviewed fetch/geolocation route.

Verification:
`PASS` at source-inspection ceiling.

Privacy/security/user comprehension:
`NOT_RUN`.

## C04-SYSREQ-006 — Actual browser/runtime required

Static/source checks are insufficient for an interactive release claim.

Current evidence:
`actual_live_browser = HOLD_ENVIRONMENT_ADMIN_BLOCK`.

Verification:
`HOLD`.

Validation:
`NOT_RUN`.

---

# Configuration-bound change / reopen

A bounded real change path was recorded across the existing app lineage.

Predecessor evidence:
- app-game-map-v1 source/QC.

Successor:
- app-game-map-v1.2.

v1.2 records material changes including:
- route-filter binding repair;
- separate map-purpose and travel-focus controls;
- localStorage My Book;
- print/no-phone fallback.

Affected requirements:
- SYSREQ-002;
- SYSREQ-005;
- SYSREQ-006.

Reopen logic:

`CONFIGURATION CHANGE → AFFECTED REQUIREMENTS → SOURCE/STATIC REVERIFY → ACTUAL BROWSER RERUN → HCD RETEST WHEN INTERACTION CHANGES`.

Observed result:
- relevant v1.2 static/source checks exist;
- actual browser verification remains HOLD rather than being inherited from the predecessor.

This satisfies the adoption requirement that change does not silently preserve stale V&V.

---

# Interface / integration evidence

Four interfaces were made explicit:

## IF-STATUS-OFFICIAL
Current:
`NOT_IMPLEMENTED / HOLD`.

Consequence:
no live-status system claim.

## IF-DIGITAL-FALLBACK
Current:
`DEFINED / NOT_FIELD_VERIFIED`.

Consequence:
digital allocation coherence does not prove integrated route resilience.

## IF-BROWSER-RUNTIME
Current:
`BLOCKED`.

Consequence:
source/static PASS cannot become implementation PASS.

## IF-HCD-VALIDATION
Current:
`NOT_RUN`.

Consequence:
verification cannot become validation.

---

# Process instance

Produced:

`C04_SYSENG_PROCESS_INSTANCE_v0.1.json`

Stage disposition:

- SYSENG-DP0 — Current evidence / professional HOLD
- SYSENG-DP1 — Current design-derived operational evidence / HCD validation HOLD
- SYSENG-DP2 — capability/function/state architecture exists / review HOLD
- SYSENG-DP3 — interfaces defined / integration HOLD
- SYSENG-DP4 — bounded requirement/V&V baseline exists / validation HOLD
- SYSENG-DP5 — logical architecture extracted / formal alternative trade study NOT_RUN
- SYSENG-DP6 — physical/configuration realization identified / integration HOLD
- SYSENG-DP7 — `BLOCKED / HOLD`
- SYSENG-DP8 — `NOT_STARTED / NOT_RUN`

Overall:

`BLOCKED / HOLD`.

No independent Systems Engineering professional PASS is claimed.

---

# V&V separation

Current requirement counts:

- total requirements: 6;
- bounded verification PASS: 4;
- verification HOLD: 2;
- validation PASS: 0;
- validation NOT_RUN: 5;
- validation N/A: 1;
- integrated interfaces VERIFIED: 0.

Therefore:

`REQUIREMENT TRACE EXISTS ≠ SYSTEMS ENGINEERING PASS`.

`VERIFICATION PASS ≠ VALIDATION PASS`.

`STATIC/SOURCE PASS ≠ BROWSER RUNTIME PASS`.

`DIGITAL ALLOCATION DEFINED ≠ PHYSICAL JOURNEY INTEGRATION VERIFIED`.

---

# Regression delta

Existing:
- FAIL-043 — verification/validation collapse;
- FAIL-044 — Systems Engineering as domain super-authority.

Added:
- FAIL-049 — V&V evidence reused for the wrong configuration;
- FAIL-050 — component/subsystem PASS promoted to integrated-system PASS;
- FAIL-051 — orphan requirement enters authoritative baseline without source/rationale/criterion/verification route.

These are domain-general Systems Engineering failures, not C04-specific wording.

---

# Professional granularity assessment

The Candidate process already met the **definition-side** professional execution floor:
- domain-native practitioner objects;
- requirement/control registers;
- configuration/change objects;
- verification and validation objects;
- integration/interface verification;
- operations/change/retirement;
- claim ceilings and does-not-prove boundaries.

Before this batch it lacked **adoption-side** execution evidence.

This reapplication closes:
- one real system-of-interest boundary;
- one requirements baseline;
- one requirement→architecture→verification trace;
- one integration failure/HOLD;
- one verification-vs-validation separation;
- one configuration/change reopen path.

Still open:
- task/claim Systems Engineering Knowledge Mount;
- independent Systems Engineering professional review;
- actual browser verification closure;
- physical/paper/human integrated field verification;
- representative HCD validation;
- live operations/support evidence.

---

# Promotion boundary

Keep Systems Engineering process Candidate/Open until:
1. C04 instance passes existing process schema validation;
2. CI/AIG regression pass;
3. independent Systems Engineering review confirms practitioner realism;
4. at least one material integrated-interface verification is actually executed;
5. verification and validation both have real evidence on an applicable system scenario;
6. authorized Current promotion updates Architecture Map / owner pointer.

`PROJECT REAPPLICATION ≠ CURRENT PROMOTION`.

