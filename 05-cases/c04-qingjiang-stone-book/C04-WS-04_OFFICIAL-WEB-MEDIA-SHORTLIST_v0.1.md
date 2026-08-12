# C04-WS-04｜Official Web Media Shortlist v0.1

**Project:** `C04｜清江石书｜红花峰林十三印`  
**Workstream:** `C04-WS-04｜视觉阅读与身份`  
**Notion output:** `C04-WS04-OUT-003` — https://app.notion.com/p/3bab86be5c478110bc2adc00a12ad818?pvs=204  
**Status:** `OFFICIAL-WEB RIGHTS PASS / IMAGE-LEVEL NODE REVIEW ACTIVE / FINAL VISUAL PASS NOT TESTED`

## 1. Decision rule

Project-owner decision on 2026-08-12: official/operator website media may be used directly in C04/OLEANDER. Therefore official-web assets are `RIGHTS PASS / PROJECT-USE APPROVED`.

This does **not** auto-pass node identity or technical fitness. Promotion requires:

`RIGHTS PASS + NODE PASS + TECH PASS`.

## 2. Image-level candidates

### `OW-20230616-2a923422a` — R05 high candidate

Source image: https://www.eslygroup.com/uploadfile/image/20230616/2a923422a.jpg  
Source page: https://www.eslygroup.com/scenic_news/2786.html

Observed from the actual image:
- tall peak/rock formation is the first reading;
- cableway line and cabins provide scale/path context but stay secondary;
- vegetation/rock proportion and major contour are legible;
- Qingjiang is not visible.

Decision:
- `R05 = NODE HIGH CANDIDATE / LANDSCAPE-FIRST PASS / EXACT 红花石林 IDENTITY TO REVERIFY`;
- `R01 = HOLD` because Qingjiang relation is absent;
- `R06 = REJECT AS SCIENCE HERO` because the river-valley relation is absent;
- `TECH = ORIGINAL DIMENSION PENDING`.

### `OW-20230711-mnq9o6767b` — R05 high candidate

Source image: https://www.eslygroup.com/uploadfile/image/20230711/mnq9o6767b.jpg  
Source page: https://www.eslygroup.com/scenic_news/2815.html

Observed:
- monumental rock mass dominates;
- cableway remains relatively small;
- sky/vegetation provide useful negative space;
- composition is suitable for near-zero-UI S0 testing.

Decision:
- `R05 = NODE HIGH CANDIDATE / S0 COMPOSITION PASS / EXACT 红花石林 IDENTITY TO REVERIFY`;
- `TECH = ORIGINAL DIMENSION PENDING`.

### `OW-20230718-v0ii0wjlhe` — R06 relation reference, hero hold

Source image: https://www.eslygroup.com/uploadfile/image/20230718/v0ii0wjlhe.jpg  
Source page: https://www.eslygroup.com/media_focus/2830.html

Observed:
- Qingjiang, opposite bank / settlement and cross-river cableway relation are readable;
- large foreground cabin competes with the landscape;
- terrace/elevation layers are not strong enough for the S2 science explanation.

Decision:
- `R06 = VIEW-RELATION PASS / SCIENCE HERO HOLD`;
- suitable for route/service/cross-river chapter reference;
- official JPEG has been captured into the Notion evidence chain; source payload about 158 KB;
- `TECH = ORIGINAL DIMENSION PENDING`.

### `OW-20230619-pbxolmbgx1` — R01 relation high candidate

Source image: https://www.eslygroup.com/uploadfile/image/20230619/pbxolmbgx1.jpg  
Source page: https://www.eslygroup.com/media_focus/2789.html

Observed:
- near-side exposed rock, cableway path, Qingjiang and opposite bank appear together;
- the photograph naturally carries the `cliff edge + river direction + moving viewpoint` relation needed by S1;
- cableway remains context rather than a decorative UI substitute.

Decision:
- `R01 = RELATION HIGH CANDIDATE / RED-ROCK-MOUTH EXACT IDENTITY TO REVERIFY`;
- appropriate for `B｜Photo + Relation Mark` once node identity and Tech close;
- `R06 = HOLD AS SCIENCE HERO` because the view is fragmented by near rock/cabin context;
- `TECH = ORIGINAL DIMENSION PENDING`.

## 3. Priority-0 state after first image audit

| Node | State | Next action |
|---|---|---|
| `R05 红花石林 / S0` | `2 HIGH CANDIDATES` | exact node identity + original-dimension/crop QA; prepare A｜Photo-dominant |
| `R01 红岩嘴 / S1` | `RELATION HIGH CANDIDATE` | exact red-rock-mouth identity + Tech; then B｜Photo + Relation Mark |
| `R06 河谷/多级阶地 / S2` | `VIEW RELATION PASS / SCIENCE HERO HOLD` | continue targeted official search for observation-platform/terrace Hero |
| `R13 一线天 / S0` | `NODE CONTEXT STRONG / IMAGE-LEVEL CANDIDATE PENDING` | lock the actual 2024-05-22 slit/frame image; no substitution |

## 4. Evidence boundary

- official page text supports the viewing relationships and named nodes;
- image-level observations above are based on actual indexed official images;
- exact node identity is not promoted when the image itself/page caption does not uniquely name that node;
- `TECH PASS` is not inferred from search thumbnails or compressed payload size;
- no `C04-VAL-02` exists yet.

## 5. Next gate

`R05/R01 exact identity + Tech QA → first LandscapeSlot replacement → A/B comparison`.

R06 and R13 stay on targeted official-media acquisition until a suitable factual Hero exists.
