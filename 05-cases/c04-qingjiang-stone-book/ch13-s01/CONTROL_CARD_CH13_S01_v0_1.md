# C04 CH13 S01｜Short Recovery｜Production Control Card v0.1

Status: **WORKING / SOURCE MATERIALIZED / PIXELS EXECUTED / NO_PROMOTION**  
Project: `PRJ-C04-QINGJIANG-SHISHU`  
Surface: `S01 / CH13-P02`  
Current production-map authority: `CH13_VISUAL_PRODUCTION_MAP_CURRENT.json → v0.2`

## Primary claim
`SHORT RECOVERY ≠ DESTINATION`  
Public line: `恢复之后，继续走。`

## Source authority
Primary source is **ODB-02 / 可拆卸倚靠休息板.png / 红花峰栏杆式可拆卸倚靠休息板** as `USER ORIGINAL DESIGN SOURCE / PHYSICAL-BODY SOURCE / PRESERVE`.

The user uploaded the exact original board into the active runtime on 2026-08-19. Source size: `4530×6038`; SHA256: `e3801e63c725de34e463510c3e3c41ad40e4ece692b4290667c7e06a4085eca6`.

Forbidden dominant substitutions remain:
- `IMG-C04-F01-SCENIC-01` / old F01 scenic render;
- `14_C04_PHYSICAL_RECOVERY_CURRENTIZED_v4.png` as first visual;
- AI replacement;
- redrawn product geometry;
- empty source-slot placeholder.

The accidental generated board produced before source-bound production is explicitly `REJECT / NOT ENTER PROJECT`.

## Image-consumption state｜PR #330 candidate delta
The older `IMG-C04-PHYS-RECOVERY-TECH-01` remains `RESERVED → CH13-01` as a **compatibility lock only** because the Current validator still requires that seed reservation. It is **not bound or displayed** in the source-bound S01 page and remains unavailable to all other surfaces.

The actual displayed source-bound pair is reserved as one consumer unit:

1. `IMG-C04-ODB02-S01-HERO-DEPLOYED`
   - bounds `[1600,360,3370,1325]`
   - size `1770×965`
   - child SHA256 `1d18aa9682f23bbed96e9ee0dd624197e349bfbdad2d2da98e1a71b862b07a6b`
   - role `DOMINANT_FIRST_VISUAL_DEPLOYED_STATE`
2. `IMG-C04-ODB02-S01-FOLDED-SUPPORT`
   - bounds `[3770,4260,4390,5710]`
   - size `620×1450`
   - child SHA256 `6d3d669521daf4e4656c36d81c9510659fd02050a1638376269ac693b499a987`
   - role `SECONDARY_FOLDED_STATE_SUPPORT`

Both displayed figures are locked to `CH13-S01-PAIRED-01`. They may not be reused on S03 or another independent page/surface unless S01 is explicitly rejected and the reservation is released.

## Page execution
- dominant visual: direct original-board exhibit crop; product/rail/scenic relation preserved;
- first viewport image share: dominant field, not dashboard/card wall;
- recovery sequence: `WALK → FATIGUE → LEAN → LOOK → CONTINUE / RETURN` remains secondary;
- static default fully communicates the page;
- no new 3D;
- current candidate uses HTML/CSS with source pixels only; image generation is not part of the current candidate.

## Actual runtime readback
Final local editable carrier: `CH13_S01_SHORT_RECOVERY_SOURCEBOUND_v1.html`.

Chromium readback:
- desktop viewport `1920×1080`: `scrollWidth=1920 / clientWidth=1920 / scrollHeight=1080 / clientHeight=1080`;
- mobile viewport `390×844`: `scrollWidth=390 / clientWidth=390`; semantic reflow full height `1050`; no horizontal page overflow.

Pixel hashes:
- desktop: `7710345bd137ce7558115ba2eb8341337375bb55b4cb4b06d982bb379c1942f3`;
- mobile: `00540e10886617f056eadcad2c513abc8bf4d76dd4f7748cc763d1e31b0ea21a`.

## Persistence
Drive folder `C04_CH13_PAGE_BY_PAGE_v5` now contains:
- `C04_CH13_S01_SOURCEBOUND_v1.zip`;
- desktop PNG;
- mobile PNG;
- editable self-contained HTML;
- source crop register.

## Review state
Producer compliance / artifact review is recorded in `CH13_S01_ARTIFACT_REVIEW_v1.md`.

`PROFESSIONAL DESIGN GATE = NOT CLAIMED`.

No `PIXEL KEEP`, `MAIN KEEP`, merge or promotion is asserted by the producer.

## Truth boundary
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.

Source-board proposal numbers do not become field/engineering truth by appearing in the original board.
