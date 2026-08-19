# CH09-P01｜ROUTE-03 Decision Map｜CH14 Rebuild v1

Project: `PRJ-C04-QINGJIANG-SHISHU`

## Decision Question
游客如何先确认路线与 Return，再决定是否继续、进入关系支线或打开可选阅读？

Primary claim: **先知道怎么回来，再决定往哪里走。**

## Authority
- `ROUTE-03 = LOCKED CURRENT`.
- `JOURNEY-04 = PROVENANCE / NON-CURRENT`; this rebuild does not use it as route authority.
- Route upstream: PR #192 / commit `128b9069c686b9a8ab65d6425fa928890f0604dc`.
- Locked SVG SHA256: `44bde5dfd82bcc6435b1aa40fb9a61d3fb99b281c93e7d0e41bdf4a38e4aec75`.
- Runtime source-carrier used for source path extraction: `恩施大清江景区游览路线图_转译版(1).svg`, SHA256 `1acfb9d708a96d9ac59900610fe724413b4b9cea4bddf1b6d0fcc27f8034c5b9`; it remains lineage/source-carrier, not replacement byte authority.

## OLEANDER Resolver / Skills
Consumed current Notion/GitHub authority before production.

Minimum sufficient execution owner set:
- `oleander-data-viz`: source inspection, raw preservation, route/node dataset, spatial-authority preservation, transformation log.
- `oleander-story-and-board`: one primary claim + one primary visual, CH14 editorial composition, existing-mature-design-first.
- `oleander-route-wayfinding-ui` candidate specialist: current-context / choice / load / Return hierarchy; one-world/multiple-readings; Return persistent; no dashboard-like route-mode UI.
- `oleander-delivery-qc`: editable/vector output, responsive carrier, target-size readback, package/persistence checks.

## CH14 visual binding
Current CH14 P04/P05/P06/P07 grammar is used as presentation authority:
- Bone Mist / Deep Water / River Black / Jade Current / Wet Stone / Sediment Sand / Cinnabar;
- CJK Serif Display + Sans Body + Mono Technical;
- `CONTEMPORARY EDITORIAL + LANDSCAPE SPACE`;
- dominant route field + editorial decision rail, not card wall;
- `FUNCTIONAL READABILITY > BRAND DECORATION`;
- Brand presence = `LIGHT`;
- `BRAND COLOR != OPERATIONAL STATUS COLOR`.

## Geometry preservation
- source main / branch / loop `d` strings reused unchanged;
- all 17 source-node coordinates unchanged;
- presentation uses uniform scale `0.78` + translation only;
- no added non-uniform scale;
- no smoothing / straightening / route redraw / node relocation.

First-read labels are reduced to four source anchors: 水布垭 / 蝴蝶崖 / 游船码头 / 游客中心-RETURN. Remaining nodes remain visible as close-read points.

Operational state is `UNKNOWN / NOT BOUND`; the page does not normalize unknown segments to open.

## Actual production
Local production package contains:
- editable full-page SVG;
- editable map-field SVG;
- 1920x1080 PNG;
- responsive HTML/CSS;
- desktop 1920x1080 Chromium readback;
- mobile 390x844 START + RETURN viewport readbacks;
- far-read and grayscale attacks;
- 17-node CSV/data dictionary;
- authority, visual spec, transformation, compliance, review and QC records.

Browser readback:
- desktop width `1920 == 1920`, no horizontal overflow;
- map SVG loaded with natural width 1160;
- mobile route world `940px` inside `390px` viewport and pans from `0` to `550`, preserving one world instead of redrawing/minimizing the route;
- console errors = 0; page errors = 0.
- localhost/file navigation was administrator-blocked, so exact HTML/CSS + embedded same SVG were validated through DOM injection; this is recorded as adapter evidence, not live-navigation PASS.

## Durable package
Google Drive file ID: `1bb89InYkmWgs-4FdHoQcCYfp36OvOhNn`

`C04_CH09_P01_ROUTE03_CH14_REBUILD_v1_PACKAGE.zip`
- bytes: `631841`
- SHA256: `40f6fdf6a15369d8c503480780ee1db955a25c986cf450d705510cb4c09522d5`
- Drive metadata size: `631841`
- independent Drive raw retrieval size: `631841`
- retrieved SHA256: `40f6fdf6a15369d8c503480780ee1db955a25c986cf450d705510cb4c09522d5`
- retrieved ZIP integrity: PASS / no errors.

## Gate state
OLEANDER Compliance producer self-check: complete for authority / geometry / truth / artifact/readback.

Professional Design Gate: **INDEPENDENT REVIEW PENDING**.

Producer does **not** issue `KEEP / MAIN KEEP / DESIGN PASS`.

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS / NOT FOR CONSTRUCTION`.
