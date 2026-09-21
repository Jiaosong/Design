# OLEANDER External Mature-KB Gap Absorption — Batch 05 — 2026-09-21

**Status:** `CANDIDATE STRENGTHENING / ENVELOPE FIELD-EVIDENCE DELTA / NO PROMOTION`

## 1｜Rule

`CURRENT OLEANDER → SEARCH EXISTING OWNER → PRIMARY SOURCE → DIGEST MATERIAL DELTA → MOUNT INTO EXISTING OWNER → READBACK`.

No new Envelope process, test METHOD, Structural inspection METHOD or project acceptance authority was created.

## 2｜Selected gap

Existing WBDG enclosure evidence and the Facade/Envelope Candidate already required mock-up, testing, field QA and installed readback, but the field air/water test carrier remained too generic. It did not explicitly bind installed specimen/configuration, adjacent-construction scope, method/version, apparatus/pressure/state, extraneous leakage, observed path/result and repair/retest identity.

## 3｜New L6 SOURCE

- `SRC-ASTM-ENVELOPE-FIELD-AIR-WATER-001`
- Notion page: `3e2b86be-5c47-8134-97dd-d16d1b3cd777`
- Existing owner relation: `KN-METHOD-ARCH-FACADE-ENVIRONMENT-INTERFACE-001`.

Primary-source anchors:
- ASTM E783-02(2018), active ASTM listing — field air leakage through installed exterior windows and doors.
- ASTM E1105-15(2023 reapproval), active ASTM listing — field water penetration of installed exterior windows/skylights/doors/curtain walls.

The SOURCE remains `L6 / SOURCE / SUPPORT / SCOPED / UNVERIFIED / E4 / A-primary-source / ACTIVE`.

## 4｜Material execution delta

Canonical field-evidence chain:

`PERFORMANCE REQUIREMENT / ACCEPTANCE OWNER → TEST OBJECT / LOCATION → INSTALLED ASSEMBLY + ADJACENT-CONSTRUCTION SCOPE → TEST METHOD / VERSION → APPARATUS / PRESSURE / CYCLE / STATE → ENVIRONMENTAL CONDITION → EXTRANEOUS-LEAKAGE CONTROL → OBSERVED AIR/WATER PATH → RESULT → DEFECT / REPAIR → RETEST → BOUNDED FIELD RECEIPT`.

Hard boundaries:

`LAB TEST ≠ FIELD TEST`

`PRODUCT RATING ≠ INSTALLED PERFORMANCE`

`ONE FIELD SAMPLE PASS ≠ WHOLE FACADE PASS`

`TEST METHOD ≠ PROJECT ACCEPTANCE PRESSURE / SAMPLE RATE`

`FIELD TEST PASS ≠ FACADE PROFESSIONAL PASS ≠ R-F INTEGRATION PASS`

## 5｜Existing Candidate absorption

Existing Facade / Building Envelope Candidate PR #643 was updated in place.

- branch: `agent/v21-facade-envelope-evolution-20260916`
- pre-absorption head: `76aae787db42e28cef557190ff18466db4099a84`
- absorption commit / current head at write: `77f7a07c6e45ed23542c2614d3ea261b8ce0c594`

Changes are additive to:
- professional-source basis;
- `ENV-MOCKUP` installed field-test evidence;
- `ENV-DELIVERY` field-test/defect/repair/retest readback.

Candidate identity and promotion state are unchanged.

## 6｜No-create / collision decisions

Structural inspection was explicitly checked and **not** expanded.

Existing coverage already includes:
- `SRC-AISC-360-22-001`;
- `SRC-AISC-303-22-001`;
- Structural Load Path–Stability–Connection;
- Structural Calculation–Drawing Release;
- Structural Erection & Temporary Stability.

Those objects already carry the current steel inspection/test relation far enough that another Chapter-N-specific SOURCE/METHOD would be duplicate coverage for the identified gap.

No duplicate source was created for:
- generic Envelope commissioning — existing WBDG source remains;
- generic facade testing — the new source is narrow field air/water method identity only.

## 7｜Notion sync/readback state

- New ASTM SOURCE created in the canonical Knowledge DB and related to the existing Facade–Environment METHOD.
- External assimilation index `IDX-KG-EXTERNAL-ASSIM-001` updated with Batch 05 routing, boundaries and Structural no-create decision.
- Source/index existence does not upgrade professional or field truth.

## 8｜Closure / promotion boundary

Batch 05 is a bounded source/process strengthening transaction only.

`SOURCE ABSORBED ≠ ENVELOPE PROCESS CURRENT ≠ PROJECT TEST PASS ≠ WHOLE-BUILDING FIELD TRUTH`.

Close this batch only after:
1. SOURCE and index fresh readback;
2. Batch receipt branch changed-file/readback check;
3. PR #643 exact-head CI/governance readback;
4. Batch receipt PR CI/governance readback;
5. authorized review/merge only where separately approved.


## 9｜Fresh transaction readback

- Notion SOURCE `SRC-ASTM-ENVELOPE-FIELD-AIR-WATER-001` fresh fetch PASS; relation to existing `KN-METHOD-ARCH-FACADE-ENVIRONMENT-INTERFACE-001` visible.
- External assimilation index Batch 05 native mention/readback PASS.
- Facade / Envelope Candidate #643 was clean-rebased onto `main@e34ef6366b58749a7f8645f03329c8e7596caf60`.
- #643 exact candidate head after rebase: `9f7c1095f3dcf29f50ba2240ed41306fcf39c6f6`.
- #643 compare after rebase: `ahead 1 / behind 0`, mergeable.
- Rebase preserved six Candidate files and rebuilt the Envelope validation step on the **current main** AI-governance workflow instead of replaying the stale historical workflow blob.
- Fresh exact-head CI is required before Batch 05 review readiness; no old CI is inherited as proof.
