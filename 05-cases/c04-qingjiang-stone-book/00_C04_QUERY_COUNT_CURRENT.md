# C04｜QUERY / COUNT CURRENT｜2026-08-19

Project: `PRJ-C04-QINGJIANG-SHISHU`

This file exists specifically to stop search/retrieval systems from confusing chapter count, protected baseline page identities, authoring units, historical Web snapshots, current chapter production surfaces, and canonical PAGE identities.

## Canonical answer to “现在多少页？”

> **当前最终 canonical PAGE count 尚未锁定。**

## Canonical answer to “现在 Web 多少页 / 多少个 surface？”

> **当前完整 integrated Web presentation-surface count 尚未重新登记（`NOT_YET_REGISTERED`）。**
>
> `112` 只是 **v1.11 历史 downstream snapshot**，已被后续章节 currentization / production 与 CH14 multi-surface expansion 超越，不能再回答成“当前 Web 就是112页/112 surfaces”。

Current count semantics:

| term | current value | exact meaning | may be answered as current/final page count? |
|---|---:|---|---|
| `chapter_count` | 20 | `CH00–CH19` organisational chapter containers | **NO** |
| `protected_legacy_page_id_count` | 52 | protected baseline PAGE identities `C04-WEB-P001...P052` used for exact migration/mapping | **NO** |
| `base_authoring_unit_count` | 111 | 70 v0.1 + 41 v0.2 authored-inventory baseline | **NO** |
| `cross_chapter_authoring_candidate_count` | 11 | authoring candidates awaiting PAGE REGISTER mapping | **NO** |
| `prior_expansion_candidate_count` | 28 | previous expansion candidates, not registered pages | **NO** |
| `historical_v1_11_web_snapshot_surface_count` | 112 | stale v1.11 downstream presentation snapshot, pre-latest chapter expansion | **NO** |
| `current_complete_integrated_web_surface_count` | `NOT_YET_REGISTERED` | requires rebuilt by-chapter current surface register | **YES only after explicit registration** |
| `canonical_page_count` | `NOT_YET_LOCKED` | actual registered PAGE identities after migration/mapping | **YES only once explicitly locked** |

## CH14 retrieval guard

CH14 is a known multi-surface chapter and must not be compressed by P-number shorthand:

- authored base = `P01–P08` = 8 authoring/system units, **not 8 pages**;
- main source/executable baseline currently includes P01–P07;
- `P OWNER != ONE PAGE`;
- P07 alone records **12 long-form brand-manual spec surfaces + scoped Web fragment**;
- P08 is authored but dedicated source/materialization mapping is still open;
- Stone Seal v1.0 / PR #238 has a 6-preview producer-candidate family, but it is Draft / review-pending / no-promotion and is not auto-counted as Current PAGE identities;
- Brand Architecture / Naming / Editorial / Motion Identity / Photography / Illustration+Diagram / Material+Print remain explicit expansion candidates until mapped.

Therefore an AI must not infer CH14 page count from the number of `Pxx` owners, and must not use the stale 112 snapshot as proof that CH14's newer multi-page work has been integrated.

## Mandatory semantic guards

`CHAPTER != PAGE`

`AUTHORING UNIT != PAGE`

`AUTHORING UNIT != WEB SURFACE`

`P OWNER != ONE PAGE`

`WEB SURFACE != CANONICAL PAGE`

`PROTECTED BASELINE PAGE ID COUNT != FINAL PAGE COUNT`

`112 = HISTORICAL v1.11 SNAPSHOT, NOT CURRENT COMPLETE WEB COUNT`

A newer screenshot count, viewport count, Web receipt, chapter P-number, long-form manual section count, candidate preview family, or authoring manifest does **not** establish canonical PAGE identity by itself.

Only an explicit newer `C04_CURRENT` / canonical PAGE REGISTER / Count Contract may change the canonical count answer.

## Required resolution sequence

1. preserve and lock `C04-WEB-P001...P052` identities;
2. build the exact 52-row PAGE REGISTER;
3. rebuild the **by-chapter current Web surface register**, including current production/currentization and CH14 multi-surface inventory;
4. map v0.1 + v0.2 authored inventory one-to-one;
5. classify authored/content units as `MAP_TO_LEGACY / EXPAND_FROM_LEGACY / NEW / PROCESS-SUPPORT`;
6. allocate `C04-WEB-Nxxx` only to materially new independent PAGE units;
7. derive `canonical_page_count` from registered PAGE identities;
8. run finished-pixel readback and independent Design Crit separately.

## Query response template

When a user asks **“C04现在多少页 / 清江项目多少页”**:
1. answer `canonical_page_count = NOT_YET_LOCKED` first;
2. explain semantic counts only when useful;
3. never substitute 20 / 52 / 111 / 112 as the final count.

When a user asks **“现在Web多少页 / Web多少个surface”**:
1. answer `current_complete_integrated_web_surface_count = NOT_YET_REGISTERED` first;
2. explain that 112 is a historical v1.11 snapshot;
3. mention current by-chapter expansion/CH14 multi-surface work if relevant;
4. do not invent a replacement total before the register is rebuilt.

Machine source: `C04_COUNT_CONTRACT_CURRENT.json`.

Truth boundary remains:
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
