# C04｜QUERY / COUNT CURRENT｜2026-08-18

Project: `PRJ-C04-QINGJIANG-SHISHU`

This file exists specifically to stop search/retrieval systems from confusing chapter count, protected baseline page identities, authoring units, and downstream Web surfaces.

## Canonical answer to “现在多少页？”

> **当前最终 canonical PAGE count 尚未锁定。**
>
> Do **not** answer `20`, `52`, `111`, or `112` as the final project page count.

Current count semantics:

| term | current value | exact meaning | may be answered as final project page count? |
|---|---:|---|---|
| `chapter_count` | 20 | `CH00–CH19` organisational chapter containers | **NO** |
| `protected_legacy_page_id_count` | 52 | protected baseline PAGE identities `C04-WEB-P001...P052` used for exact migration/mapping | **NO** |
| `base_authoring_unit_count` | 111 | 70 v0.1 + 41 v0.2 chapter-content authoring units | **NO** |
| `cross_chapter_authoring_candidate_count` | 11 | authoring candidates awaiting PAGE REGISTER mapping | **NO** |
| `prior_expansion_candidate_count` | 28 | previous expansion candidates, not registered pages | **NO** |
| `downstream_web_carrier_surface_count` | 112 | C04 Web v1.11 implemented presentation surfaces | **NO** |
| `canonical_page_count` | `NOT_YET_LOCKED` | actual registered PAGE identities after migration/mapping | **YES, once explicitly locked** |

## Mandatory semantic guards

`CHAPTER != PAGE`

`AUTHORING UNIT != PAGE`

`WEB SURFACE != CANONICAL PAGE`

`PROTECTED BASELINE PAGE ID COUNT != FINAL PAGE COUNT`

A newer timestamp, Web receipt, preview package, chapter file, `<section>` count, screenshot count, viewport count, or authoring manifest does **not** override these semantics by itself.

Only an explicit newer `C04_CURRENT` / canonical PAGE REGISTER / Count Contract may change the canonical count answer.

## Required resolution sequence before a final page count can exist

1. preserve and lock `C04-WEB-P001...P052` identities;
2. build the exact 52-row PAGE REGISTER;
3. map v0.1 + v0.2 authored inventory one-to-one;
4. classify every authored unit as `MAP_TO_LEGACY / EXPAND_FROM_LEGACY / NEW / PROCESS-SUPPORT`;
5. allocate `C04-WEB-Nxxx` only to materially new independent PAGE units;
6. derive `canonical_page_count` from the registered PAGE identities;
7. run finished-pixel readback and independent Design Crit separately.

## Query response template

When a user asks “C04现在多少页 / 清江项目多少页 / Web多少页”, answer in this order:

1. `canonical_page_count = NOT_YET_LOCKED`;
2. explain `20 chapters`;
3. explain `52 protected baseline PAGE IDs`;
4. explain `111 authoring units`;
5. if relevant, explain `112 downstream Web carrier surfaces`;
6. never collapse these numbers into one “page count”.

Machine source: `C04_COUNT_CONTRACT_CURRENT.json`.

Truth boundary remains:
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
