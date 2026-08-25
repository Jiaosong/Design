# C04｜2026-08-17 Chapter Content Sync Index v0.1

Project: `PRJ-C04-QINGJIANG-SHISHU`

Purpose: preserve the actual chapter/page content authored in the 2026-08-17 conversation without compressing chapters into summaries or treating chapter files as page count.

## Hard rules

- `CHAPTER ≠ PAGE`
- `NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`
- `CONCEPT KEEP ≠ PIXEL KEEP`
- `PIXEL FAIL ≠ DESIGN DELETE`
- `VALIDATION SUBSET ≠ WHOLE PROJECT`
- `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`

## Authoring identity vs final PAGE-ID

Each file contains independent page-content units named `CHxx-Pxx`. These are **authoring identities only**.

They do not replace or pre-assign the protected baseline `C04-WEB-P001...P052`, and they are not automatically `C04-WEB-Nxxx`.

Final mapping requires an exact legacy page register and one-to-one comparison.

## Synced chapter files

| Chapter | File | Base authoring pages | Expansion candidates | Status |
|---|---|---:|---:|---|
| CH00 项目定义 | `CH00_PROJECT-DEFINITION.md` | 2 | 0 | synced |
| CH01 项目问题与机会 | — | — | — | not regenerated in this conversation |
| CH02 场地与山水分析 | `CH02_SITE-LANDSCAPE-ANALYSIS.md` | 5 | 0+ | synced |
| CH03 地域文化与内容分析 | `CH03_CULTURE-CONTENT-ANALYSIS.md` | 4 | 0+ | synced |
| CH04 人群与使用状态分析 | `CH04_AUDIENCE-USE-STATE-ANALYSIS.md` | 6 | 0+ | synced |
| CH05 游程与行为分析 | `CH05_JOURNEY-BEHAVIOR-ANALYSIS.md` | 4 | 0 | synced |
| CH06 设计原理 | `CH06_DESIGN-PRINCIPLES.md` | 5 | 0 | synced |
| CH07 设计方法 | `CH07_DESIGN-METHODS.md` | 4 | 0 | synced |
| CH08 总体策略与体验系统 | — | — | — | not regenerated in this conversation |
| CH09 路线、交通与服务设计 | `CH09_ROUTE-MOBILITY-SERVICE.md` | 5 | 0+ | synced |
| CH10 十三印内容与互动系统 | `CH10_THIRTEEN-IMPRINTS-CONTENT-INTERACTION.md` | 5 | 0+ | synced |
| CH11 数字陪伴系统 | `CH11_DIGITAL-COMPANION-SYSTEM.md` | 8 | 6 | synced |
| CH12 关键场景设计 | `CH12_KEY-SCENE-DESIGN.md` | 7 | 7 | synced |
| CH13 实体、身体与感官设计 | `CH13_PHYSICAL-BODY-SENSORY.md` | 7 | 8 | synced |
| CH14 品牌与视觉识别系统 | `CH14_BRAND-VISUAL-IDENTITY.md` | 8 | 7 | synced / new chapter |
| CH15 记忆、IP与文化产品 | existing architecture content | — | — | renumbered from old CH14; not rewritten here |
| CH16 设计深化与细节 | existing architecture content | — | — | renumbered from old CH15; not rewritten here |
| CH17 技术、模型与工程证明 | existing architecture content | — | — | renumbered from old CH16; not rewritten here |
| CH18 方案演化与专业判断 | existing architecture content | — | — | renumbered from old CH17; not rewritten here |
| CH19 开放项、回程与结尾 | existing architecture content | — | — | renumbered from old CH18; not rewritten here |

## Current authored-unit count

Base authoring units in this sync:

- CH00 2
- CH02 5
- CH03 4
- CH04 6
- CH05 4
- CH06 5
- CH07 4
- CH09 5
- CH10 5
- CH11 8
- CH12 7
- CH13 7
- CH14 8

Total = **70 authoring page units**.

This number is **NOT** the official current Web page count and must not be added mechanically to the old baseline 52. It describes how many independent page-level content units were authored/synced in this round.

Expansion candidates explicitly recorded: CH11 6 + CH12 7 + CH13 8 + CH14 7 = **28 candidates**. Candidates are not created pages until content is materially produced and mapped.

## Architecture authority update

See `../../C04-B_PROJECT-ARCHITECTURE_v3.2.md`.

v3.2 adds CH14 Brand as an independent chapter and shifts former CH14–CH18 to CH15–CH19. No previous chapter content is deleted.

## Missing from this round by design

CH01 and CH08 were not re-authored in this conversation, so this sync deliberately does **not** invent their detailed page copy. Their architectural identities remain valid and should be populated from current authority / existing material or a later dedicated authoring pass.

## Required next operation

Build the exact 52-row legacy PAGE REGISTER, then map each of these 70 authored units as `MAP_TO_LEGACY`, `EXPAND_FROM_LEGACY`, `NEW`, or `PROCESS/SUPPORT` before any final page total is claimed.