# C04｜R01–R13 Canonical Scene Register v1.0

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Role: `P0 IDENTITY AUTHORITY / NO-LOSS / ROUTE-CONTENT DECONFLICTION`  
Date: `2026-08-16`  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`

## P0 identity rule

**Rxx IDs belong to the Thirteen Imprints content/reading namespace. They do not own route, transport or mandatory-station authority.**

- `R01 = 红岩嘴`, not `索道`.
- `CABLE / 索道` is a Journey / spatial carrier. It may carry the R01 moving-view reading.
- BOAT / CABLE / WALK / Arrival / Return must use Journey/Scene identities, not replace Rxx content identity.
- A source-grounded scenic object may overlap a real visitor scene, but `Rxx` still does not become route sovereignty or an exact survey pin.
- This register overrides any older presentation/scene-binding wording that collapses a Journey carrier into an Rxx identity.

## Canonical register

| ID | 正式场景名 / canonical content identity | 空间载体 | 主要体验角色 | 是否真实路线节点 | 是否十三印内容入口 | 当前证据状态 |
|---|---|---|---|---|---|---|
| R01 | 红岩嘴 | **CABLE moving view / 索道移动视域**；远距离辨认红岩嘴与两岸/河谷关系 | TRANSPORT-adjacent / OBSERVE / VIEW | **NO — not route authority** | YES | SOURCE-GROUNDED moving-view relation / exact cabin side, visible duration, occlusion FIELD OPEN |
| R02 | 华中第一藤 | WALK vegetation observation / 步行植物观察场景 | OBSERVE / WISDOM / PROCESS | NO — not route authority | YES | EXPERT REQUIRED; species, age, “第一” criterion and exact location OPEN |
| R03 | 铁券天书 | WALK rock-face observation / 岩体表面观察 | OBSERVE / WISDOM / PROCESS | NO — not route authority | YES | FIELD + GEOLOGY EXPERT OPEN; no lithology/process inference from name/appearance alone |
| R04 | 母子相望 / 母子峰 | WALK paired-form / named-view relation | CULTURE / OBSERVE / RELATION | NO — not route authority | YES | FIELD NAME / VIEWPOINT OPEN; local naming ≠ scientific fact |
| R05 | 红花石林 | CABLE/WALK broad peak-forest viewing / 峰林整体视域 | OBSERVE / PLAY / VIEW | NO — not route authority | YES | SOURCE-GROUNDED; same-view/weather/precise viewpoint still OPEN |
| R06 | 多级阶地·不对称河谷 | WALK stop / viewing-platform + valley relation | OBSERVE / RECOVER / WISDOM / RELATION | NO — not route authority | YES | SOURCE-PASS relation / FIELD GEOMETRY + geology interpretation OPEN |
| R07 | 仓禀峰 / 仓廪峰 | WALK named-peak viewing / 地名与山体识别 | CULTURE / NAME / FORM | NO — not route authority | YES | operator/public naming evidence exists; dual spelling retained; FIELD SIGN OPEN |
| R08 | 文山天书 | WALK cliff-wall observation / 岩壁线条、层次与地方叙事 | READ / OBSERVE / CULTURE | NO — not route authority | YES | FIELD + GEOLOGY EXPERT OPEN; “天书” may remain cultural reading only |
| R09 | 盐水女神峰 | WALK named-peak/story viewing | LOCAL STORY / CULTURE / READ | NO — not route authority | YES | text/local narrative SOURCE-GROUNDED; ancient-site equivalence prohibited / precise identity OPEN |
| R10 | 绝壁天书 | WALK cliff close-observation from safe position | OBSERVE / WISDOM / FORM | NO — not route authority | YES | FIELD + GEOLOGY EXPERT OPEN; exact safe viewpoint OPEN |
| R11 | 金石为开 | WALK fissure / transition / body-scale relation | OBSERVE / BODY / RELATION | NO — not route authority | YES | FIELD + SAFETY OPEN; no pseudo-scientific force/process claim |
| R12 | 廪君峰 | WALK distant-peak / cultural viewing | CULTURE / READ / VIEW | NO — not route authority | YES | SOURCE-GROUNDED cultural relation; historical-site equivalence prohibited |
| R13 | 一线天 | WALK natural narrow aperture / passage + return view | BODY / OBSERVE / SAFETY / RETURN | NO — not route authority | YES | SOURCE-GROUNDED aperture/view relation / exact passage, bypass and safety FIELD OPEN |

## Current design disposition｜not equal-weight

This is a **design-priority disposition**, not a new route order.

| ID | Current disposition | What to do next |
|---|---|---|
| R01 | `OBSERVE` | Landscape/moving-view first; at most one LIGHT prompt; no mandatory UI. |
| R02 | `OBSERVE + HOLD_EXPLANATION` | Keep plant observation; expert-close species/age before scientific deep read. |
| R03 | `READ + HOLD_SCIENCE` | Keep visual comparison/question; geology explanation remains open. |
| R04 | `READ` | Optional naming/form comparison; no need for a large game scene yet. |
| R05 | `SCENE` | Deepen as a real PLAY/WISDOM scene: see → compare/find → light feedback → exit. |
| R06 | `SCENE` | Deepen as integrated landscape/recovery/wisdom scene; physical + digital + section proof may converge here. |
| R07 | `READ` | Name conflict itself is content; retain dual spelling. |
| R08 | `READ + HOLD_SCIENCE` | Cultural/visual reading allowed; geology stays expert-open. |
| R09 | `READ` | Short local-story carrier; can pair with R12 rather than become a task station. |
| R10 | `OBSERVE + HOLD_SCIENCE` | Safe-distance surface observation; no high-attention game. |
| R11 | `OBSERVE / BODY` | Body-scale transition; safety before interpretation. |
| R12 | `READ` | Cultural story / distant viewing; may pair with R09. |
| R13 | `OBSERVE / BODY` | PLAY OFF; body, light, passage, safety and return dominate. |

## References used to close this identity conflict

- `C04_READING-SYSTEM_v0.8.md`: R01–R13 are Provisional Content Index; `R01 红岩嘴`, not route structure.
- `C04_MEDIA-EVIDENCE-SET_v0.1_REFERENCE-ONLY.md`: `R01｜红岩嘴｜索道视域印`; operator/group sources support cableway moving-view relation.
- `C04_Qingjiang_Story-Spine_Audience_Physical-Outcome_Longpage_v0.1.pdf`: cross-river cable chapter uses `01 红岩嘴 / 05 红花石林`; R01 is content read through moving view.
- `C04_Portfolio_Atlas_FINAL_A3.pdf`: all thirteen are optional reading pages, not 13 stations; exact pin/order does not own route.

