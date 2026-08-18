# C04｜Count / Query Guard Receipt｜2026-08-18

Project: `PRJ-C04-QINGJIANG-SHISHU`

## Trigger
Repeated retrieval/query failures answered `20 pages` or `52 pages` by collapsing different count semantics.

## Repair
Two CURRENT query/count artifacts now exist at project root:

- `00_C04_QUERY_COUNT_CURRENT.md` — human/retrieval-first canonical answer.
- `C04_COUNT_CONTRACT_CURRENT.json` — machine-readable semantic contract.

Regression cases:
- `C04_COUNT_QUERY_GUARD_TEST.json`.

## Canonical semantics
- `chapter_count = 20` → CH00–CH19 chapter containers; **not page_count**.
- `protected_legacy_page_id_count = 52` → C04-WEB-P001…P052 mapping baseline; **not final page_count**.
- `base_authoring_unit_count = 111` → 70(v0.1)+41(v0.2) authoring inventory; **not page_count**.
- `cross_chapter_authoring_candidate_count = 11` → candidates awaiting mapping; **not page_count**.
- `prior_expansion_candidate_count = 28` → candidates awaiting mapping/production; **not page_count**.
- `downstream_web_carrier_surface_count = 112` → v1.11 presentation carrier surfaces; **not canonical page_count**.
- `canonical_page_count = NOT_YET_LOCKED`.

## Mandatory answer rule
When asked “C04 / 清江项目现在多少页”, answer:

> 当前最终 canonical PAGE count 尚未锁定。

Then explain count semantics by role. Never answer 20, 52, 111, or 112 as the final project page count unless a later explicit Current / PAGE REGISTER contract supersedes this one.

## Resolution dependency
Final page count can only be derived after:
`P001–P052 exact PAGE REGISTER → authored-unit mapping → MAP_TO_LEGACY / EXPAND_FROM_LEGACY / NEW / PROCESS-SUPPORT → N-series allocation → registered PAGE count`.

## Process note
The two Current query/count files were bootstrapped directly at the root to stop active retrieval pollution immediately. This focused branch adds the regression guard and receipt so the hotfix is reviewable and traceable. Future semantic changes must use the normal branch → PR → CI → readback flow.

## Does not prove
This query repair does not establish finished-pixel Design PASS, browser/accessibility PASS, FIELD validation, engineering approval, or project Promotion.

Truth boundary:
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
