# C04 Web v1.9｜中文 v3.0 架构绑定回执

- 项目：`PRJ-C04-QINGJIANG-SHISHU`
- 角色：`DOWNSTREAM WEB / PRESENTATION CARRIER`
- 架构来源：`C04-B_PROJECT-ARCHITECTURE_v3.0`，main merge `7cb30a03e8c40ea22e264e4f3bad0990dc06147e`
- 上游 Web 基线：v1.8，52 visible semantic objects inventory
- 路线绑定：`ROUTE-03 = LOCKED CURRENT`
- `JOURNEY-04 = PROVENANCE / NON-CURRENT`
- R06：`FINISHED / FROZEN / NO REOPEN`

## 本轮真实源码变化
1. 新建完整 v1.9 `web-src` successor，不覆盖历史 v1.3/v1.7/v1.8。
2. 中文化导航、章节状态与第一阅读文案。
3. 新增：项目问题与机会、场地与山水分析、游程与行为分析、设计原理、设计方法、总体策略与体验系统、设计深化与细节、方案演化与专业判断。
4. 人群章节从简化 persona/动作说明深化为：移动/体力、注意/认知、阅读深度、数字熟悉度、同行关系、回程压力 → 同场景设计回应。
5. 地域文化章节从“文化跟随游程”改为内容适配分析：`来源 → 场景适配 → 游客动作 → 设计载体`，避免重复拥有路线叙事。
6. Hero 与路线章节中文第一阅读；ROUTE-03 几何/锁定关系不改。
7. 继承当前 Game Map / App / 十三印 / Scene / Physical / Memory / Technical / Motion / Return，不因架构重建删除设计对象。

## 源码 readback
- v1.9 `web-src/chapters/` 已写入 21 个按序构建的章节文件；其中 CH11 由 Game Map + App 两个文件承载，CH18 由 Motion + Return 两个文件承载，因此不等于 21 个新的项目章节。
- `page_top.html` 已改为中文主导航与中文章节状态。
- `app.js` 已改为中文章节标签，并保留十三印/地图交互与 lightbox 行为。
- CSS 继承 v1.3 基础 + v1.7 delta + v1.8 ROUTE-03 delta，并新增 v3.0 专业深度样式。

## 当前验证边界
- GitHub branch source readback：PASS。
- 本环境无法直接联网 clone GitHub，因此本轮未在本地浏览器重新执行 finished-pixel 矩阵；不能沿用 v1.8 的 Browser PASS 作为 v1.9 Browser PASS。
- v1.9 Browser / responsive / finished-pixel readback：PENDING。
- 独立 Design Verdict：PENDING。
- 不证明现场、工程、安全、运营、可施工或项目 Promotion。

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
