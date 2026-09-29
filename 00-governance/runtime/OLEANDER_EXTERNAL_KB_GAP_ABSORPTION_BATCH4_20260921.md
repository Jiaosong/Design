# OLEANDER External Mature-KB Gap Absorption — Batch 04 — 2026-09-21

**Status:** `CANDIDATE STRENGTHENING / MATERIAL EXECUTION-EVIDENCE DELTA / NO PROMOTION`

## 1｜Rule

`CURRENT OLEANDER → SEARCH EXISTING OWNER → PRIMARY / FIRST-PARTY SOURCE → DIGEST MATERIAL DELTA → MOUNT INTO EXISTING OWNER → READBACK`.

This batch was deduplicated against Batch 01–03 before creating any new SOURCE or owner.

## 2｜Material gaps selected

### A｜Lighting photometric-data provenance

Existing Lighting Candidate already had photometric calculation, luminaire, substitution, commissioning and field-readback objects, but did not have a first-party SOURCE explicitly binding **electronic photometric file identity** to **measured product/test identity** and subsequent simulation/substitution readback.

New SOURCE:
- `SRC-IES-PHOTOMETRIC-DATA-001`
- Notion: `3e2b86be-5c47-8152-aa64-e2dc17fe8704`
- IES anchors:
  - ANSI/IES LM-63-19(R25) — electronic transfer of photometric data;
  - ANSI/IES LM-79-24 — optical/electrical measurement of SSL products.

Execution delta:

`PRODUCT/OPTIC/OUTPUT → TEST/REPORT IDENTITY → LM-63/OTHER PHOTOMETRY ID → IMPORT/CONVERSION → MODEL INPUT → PLACEMENT/AIMING/CONTROL → RESULT → SUBSTITUTION → INSTALLED/FIELD READBACK`.

Hard boundary:

`LM-63 FILE EXISTS ≠ LM-79 TEST IDENTITY CONFIRMED ≠ EXACT SUPPLIED LUMINAIRE CONFIRMED`.

`RADIANCE RUNTIME PASS ≠ PROJECT PHOTOMETRIC INPUT VALID ≠ LIGHTING PROFESSIONAL PASS`.

Existing owner reused:
- `00-governance/lighting-design-process-v1.0-CANDIDATE.md`;
- Notion `KN-METHOD-LIGHTING-CRITERIA-SUBMITTAL-001`;
- Notion `KN-METHOD-SPATIAL-LIGHTING-PERFORMANCE-001`.

No new Lighting METHOD or process was created.

### B｜MEP measured energy/demand/water savings M&V

Existing Current MEP process already separated design operational-energy estimates from in-use performance through CIBSE TM54, but lacked a first-party measured-savings M&V SOURCE with an explicit meter/baseline/post-period/normalization/uncertainty carrier.

New SOURCE:
- `SRC-ASHRAE-G14-MV-2023-001`
- Notion: `3e2b86be-5c47-81e4-9804-fd6afe4c4603`
- ASHRAE Guideline 14-2023, current published guideline under continuous maintenance; Addendum a published.

Execution delta:

`M&V BOUNDARY → METER/DATA IDENTITY → BASELINE → POST/REPORTING PERIOD → INDEPENDENT VARIABLES/NORMALIZATION → MODEL/ADJUSTMENT → DATA QUALITY/UNCERTAINTY → SAVINGS → EXCEPTIONS → RE-MEASURE/REOPEN`.

Hard boundaries:

`ENERGYPLUS / DESIGN SIMULATION ≠ MEASURED SAVINGS`.

`UTILITY-BILL OR METER DELTA ≠ CAUSAL SAVINGS PROOF`.

Existing owner reused:
- Current `00-governance/building-services-mep-design-process-v1.0.md`;
- Notion `IDX-ARCH-MEP-004`.

No generic Energy M&V METHOD or parallel FM/energy process was created.

## 3｜Deduplication / no-create decisions

No new object was created for:
- Fire/Life Safety commissioning/integrated testing — already absorbed in Batch 03 via `SRC-NFPA-FLS-CX-IST-2027-001` into Candidate #641;
- Building Acoustics field measurement — already absorbed in Batch 03 via `SRC-ISO-ACOUSTIC-FIELD-MEAS-001` into Candidate #644;
- Envelope commissioning — existing `SRC-WBDG-ENCLOSURE-001` + Facade/Environment METHOD already own this relation;
- Lighting commissioning — existing IES process/Cx SOURCE + Schedule/Control/Cx METHOD already own it;
- Accessibility — existing Access Board/ADA chain remains sufficient for current identified gaps;
- Visual/print and Physical Product — prior dedupe found substantive existing owners.

## 4｜Source verification notes

IES official readback 2026-09-21:
- IES Computer Committee lists ANSI/IES LM-63-19 as a current document;
- IES Webstore lists LM-63-19(R25);
- IES Webstore lists ANSI/IES LM-79-24 and describes controlled optical/electrical measurements, intensity distribution, color/spectral quantities, uncertainty and reporting.

ASHRAE official readback 2026-09-21:
- ASHRAE Titles/Purposes/Scopes lists Guideline 14-2023 and states it supersedes 14-2014;
- scope is measured energy, demand and water savings using measured pre/post data;
- ASHRAE Addenda lists Addendum a to Guideline 14-2023.

## 5｜GitHub owner delta

Files:
- `00-governance/lighting-design-process-v1.0-CANDIDATE.md`
- `00-governance/building-services-mep-design-process-v1.0.md`

No new professional stage IDs were created.

## 6｜Promotion boundary

Lighting remains `CANDIDATE / NOT CURRENT / NO PROMOTION`.

MEP remains Current, but the new M&V content only strengthens its evidence/readback contract. It does not make any project M&V claim PASS.

`SOURCE MOUNT ≠ PROFESSIONAL PASS ≠ RUNTIME PASS ≠ PROJECT PERFORMANCE ≠ FIELD TRUTH`.

## 7｜Closure condition

Close Batch 04 only after:
1. branch exact readback;
2. changed-file scope check;
3. OLEANDER CI/governance PASS;
4. Notion SOURCE readback + external-assimilation index sync;
5. merge only after authorized review;
6. post-merge main readback and final receipt update.


## 8｜Live transaction readback

- GitHub Draft PR: **#693** `governance: absorb photometric provenance and measured M&V`.
- PR base at creation: `main@e34ef6366b58749a7f8645f03329c8e7596caf60`.
- Initial candidate head before this receipt update: `87c0324137eebaf3d4f5a4162c4d4f4f4dd209f8`.
- Changed-file scope at PR creation: exactly 3 files — Current MEP owner, Lighting Candidate owner, this Batch 04 receipt.
- Notion source readback PASS:
  - `SRC-IES-PHOTOMETRIC-DATA-001` page `3e2b86be-5c47-8152-aa64-e2dc17fe8704`, relations to existing Lighting Criteria/Submittal and Spatial Lighting Performance owners visible;
  - `SRC-ASHRAE-G14-MV-2023-001` page `3e2b86be-5c47-81e4-9804-fd6afe4c4603`, relation to existing MEP routing owner visible.
- Notion external-assimilation index `IDX-KG-EXTERNAL-ASSIM-001` readback PASS with Batch 04 section and native mentions to both SOURCE pages.
- Trust remains `UNVERIFIED`; SOURCE/index existence does not upgrade KI/OE/professional/project truth.
- Merge remains **not authorized / not performed** at this receipt state.
