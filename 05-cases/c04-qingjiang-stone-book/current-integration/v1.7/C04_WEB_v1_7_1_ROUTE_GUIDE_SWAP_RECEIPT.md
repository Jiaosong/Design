# C04 Web v1.7.1 — Route Guide SVG Swap Receipt

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Role: `DOWNSTREAM WEB / PRESENTATION CARRIER`

## Exact material delta
- User-supplied `恩施大清江景区游览路线图_转译版.svg` is bound natively as `assets/qingjiang_route_guide_translated.svg`.
- It replaces the prior synthetic Journey relation-path card only.
- App ROUTE, Game Map interaction, Culture, R06/R13, Technical and upstream official raw-guide authority are not replaced by this edit.
- The SVG remains vector in Web; no PNG substitution is used for runtime.

## Responsive behavior
- Desktop: complete SVG overview is the Journey first-read map surface; click control retains near-read/zoom affordance.
- 390px: complete map overview appears first. `近读地图 / SWIPE TO READ` opens a 980px horizontally pannable vector close-read, preventing the mobile first read from becoming an arbitrary left-side crop.

## Readback
- source: 1448×1086 / 35,617 bytes / SHA256 `1acfb9d708a96d9ac59900610fe724413b4b9cea4bddf1b6d0fcc27f8034c5b9`.
- old synthetic Journey route card: 0 remaining.
- runtime asset references: 30 unique / 0 missing.
- desktop document width: 1920 = client width 1920.
- mobile document width: 390 = client width 390; close-read container is intentionally internally scrollable 980→352px.

## Persistence
Full recoverable runtime including the exact SVG is persisted in Library CURRENT as `C04_WEB_v1_7_1_ROUTE_GUIDE_SVG_SWAP.zip`.
Package SHA256: `20ea54704f6e85dc428f0e270f89fe49831b01f0f2f10e63ffb582dd96c0d1ee`.

Direct file/localhost navigation remains blocked on this execution surface; targeted finished-pixel previews were rendered with Playwright `page.set_content`. This does not claim live-navigation Browser PASS or independent Design PASS.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / FIELD PASS=NONE / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
