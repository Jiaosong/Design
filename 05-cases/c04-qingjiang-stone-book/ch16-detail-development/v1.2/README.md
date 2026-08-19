# C04 / CH16 Detail + Development v1.2

Project: `PRJ-C04-QINGJIANG-SHISHU`

State: `REPAIR CANDIDATE / NO_PROMOTION / INDEPENDENT EXTERNAL DESIGN GATE PENDING`

## Current chapter mapping

CH16 follows the current v0.2 authoring surface as seven pages:

1. `CH16-P01` — 人体与使用尺度不是装饰性人形
2. `CH16-P02` — 平面与定位：先证明为什么需要落位
3. `CH16-P03` — 剖面：身体—路径—景观关系
4. `CH16-P04` — 材料 / CMF：材料角色先于颜色名称
5. `CH16-P05` — 连接与可逆性：父图→D01子详图注册
6. `CH16-P06` — 排水、防滑、边缘与维护
7. `CH16-P07` — Detail Open Register

## OLEANDER execution

Applied installed skills:
- `oleander-story-and-board`
- `oleander-data-viz`
- `oleander-delivery-qc`

Consumed but **not promoted as an installed Skill**:
- Technical Drawing Current Method
- Detail Callout Registration
- Activity-bearing Scale
- Structural Lineweight

## Authority boundary

- R06 experience remains `FROZEN / NO REOPEN`.
- No new platform, route, railing, node, surveyed terrain or exact field geometry is introduced.
- Shared interface envelope remains `1200 × 160 × 975 mm`, explicitly `DESIGNER ESTIMATE / CONCEPT INTERFACE / NTS / FIELD OPEN`.
- v1.2 corrects the misleading C05 phrase `field-verified existing substrate` to `EXISTING BASE / FIELD VERIFY REQUIRED`.
- P02 is relational only and must not be read as a site plan.
- P03 parent view id = `CH16-P03-SEC-A`.
- P05 child callout = `D01`; same orientation, side and component order; enlarged NTS only.

## Produced in the execution package

- 7 editable 1920×1080 SVG pages
- 7 PNG pixel readbacks
- CH16 long-scroll HTML
- inline-vector HTML source
- component geometry JSON
- QC JSON
- review/repair note
- contact sheet
- ZIP delivery bundle

Runtime package SHA-256: `4dea4a75f9a6a75a18f168887ad32cfad94698e0a59da0211c443f1eda4bf9f4`.

The connected GitHub mutation surface is being used for the project receipt/control-plane text. The recoverable visual package is also delivered separately as the v1.2 ZIP; no GitHub commit is allowed to imply that a raster/browser/field gate passed merely because source metadata exists.

## QC boundary

- SVG parse/render: PASS (7/7)
- 1920×1080 pixel readback: completed
- external SVG href: 0
- v1.2 Browser PASS: **HOLD** — container Chromium headless timed out at D-Bus/zygote; v1.1 browser evidence is not inherited as v1.2 proof.
- independent finished-output professional design verdict: **PENDING**

Truth: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
