# C04｜清江石书｜完整项目架构 v3.1

- 项目：`PRJ-C04-QINGJIANG-SHISHU`
- 角色：`当前项目展示架构修正 / CHAPTER-PAGE SEPARATION`
- 日期：`2026-08-17`
- 继承：`C04-B_PROJECT-ARCHITECTURE_v3.0`
- 本版只修正结构层级与迁移纪律，不删除 v3.0 的任何内容、章节、设计对象或专业深度。

## 0｜最优先结构规则

> **CHAPTER ≠ PAGE。**
>
> **章节是组织容器；页面是独立展示与设计单元。**
>
> **章节数量不得被当成页面数量。章节重组不得压缩、合并或覆盖既有页面。**

C04 的展示层级固定为：

`PROJECT → CHAPTER → PAGE → MODULE / FIGURE / ASSET`

- `PROJECT`：清江石书完整项目。
- `CHAPTER`：CH00–CH18，只负责组织专业内容与阅读顺序。
- `PAGE`：真正进入 Web / PDF / 展板阅读的独立页面，必须拥有稳定 `PAGE-ID`、一个主要设计/分析命题和独立视觉构图。
- `MODULE / FIGURE / ASSET`：页面内部图、表、界面、技术图、照片、模型、文字模块，不得被误算成页面。

## 1｜NO COMPRESSION / NO LOSS

现有 Web v1.4/v1.8 已验证的 `52` 个实际页面/语义 surface 是**页面基线库存**，不是章节数量，也不是可被新架构折叠的素材池。

硬规则：

1. 原有 52 个页面必须逐页保留身份；先分配稳定 PAGE-ID，再做章节归属。
2. 新增的项目问题、场地分析、文化分析、人群分析、游程行为、设计原理、设计方法、总体系统、设计深化、专业判断等内容，只能增加新页面，不能替代原 52 页。
3. `CH00–CH18` 是章节目录，不是 19 页，也不是 21 页。
4. 一个章节可以包含 1 页、5 页、10 页或更多页面；按内容深度决定，不设平均页数。
5. 页面总数必须由实际 PAGE 节点统计，不得由 `<section>` 数、章节文件数、导航点数、viewport 数或截图拼版数推算。
6. 页面重排允许 `MOVE`，视觉重做允许 `REDRAW`，内容补强允许 `EXPAND`，但默认不允许 `MERGE`。
7. 只有独立逐页审查证明两页在“主命题 + 设计作用 + 证据作用 + 视觉内容”上实质重复，才允许提出 `MERGE CANDIDATE`；合并前必须保留两个旧 PAGE-ID 的 provenance，且不得因为“想变短、章节更整齐、页面太多”而合并。
8. 任何 `DROP/ARCHIVE` 都必须有明确的对象级理由；不能因为页面属于旧架构就删除。

## 2｜页面身份规则

### 2.1 既有 52 页

建立基线 ID：

`C04-WEB-P001` → `C04-WEB-P052`

绑定顺序以最后一套经过完整页面 readback 的 52 个 article/page surfaces 的稳定读取顺序为准。每一页至少记录：

- `page_id`
- `legacy_order`
- `source_version`
- `chapter_id`
- `page_type`
- `primary_claim`
- `primary_visual`
- `concept_state`
- `pixel_state`
- `action`
- `does_not_prove`

在完成逐页绑定前，52 个 PAGE-ID 全部默认 `PRESERVE / UNMAPPED`，不得合并。

### 2.2 新增页面

新增内容使用：

`C04-WEB-N001`、`C04-WEB-N002`……

新页面不复用旧 PAGE-ID，不用“章节页”覆盖旧页面，也不把多项分析塞进一张总表来节省页数。

新增页面只有在内容真实成立时创建；不得为增加页数制造 filler。

## 3｜CH00–CH18 与页面的关系

v3.0 的 19 个章节全部保留，角色不变：

- CH00 项目定义
- CH01 项目问题与机会
- CH02 场地与山水分析
- CH03 地域文化与内容分析
- CH04 人群与使用状态分析
- CH05 游程与行为分析
- CH06 设计原理
- CH07 设计方法
- CH08 总体策略与体验系统
- CH09 路线、交通与服务设计
- CH10 十三印内容与互动系统
- CH11 数字陪伴系统
- CH12 关键场景设计
- CH13 实体、身体与感官设计
- CH14 记忆、IP与文化产品
- CH15 设计深化与细节
- CH16 技术、模型与工程证明
- CH17 方案演化与专业判断
- CH18 开放项、回程与结尾

但每个章节下面必须是**页面序列**，而不是“把章节做成一张长页”。

示例：

`CH04 人群与使用状态分析`
- PAGE：人群分析变量总览
- PAGE：儿童/亲子行为与认知负担
- PAGE：青年探索行为
- PAGE：成年深读行为
- PAGE：长者/低体力与恢复需求
- PAGE：R06 同场景四种深度对照
- PAGE：R13 高压缩空间的人群优先级
- PAGE：无手机/低数字熟悉度路径

这些页面可以根据实际内容增减，但不能因为都属于 CH04 就压成一张 Persona/矩阵页。

同理：
- CH06 的十条设计原理可以形成多页，不要求压成一张十宫格；
- CH07 的方法可以形成多个方法页，并用真实项目案例证明；
- CH11 App 必须保留独立页面/状态/交互深度，不压成“6屏拼图”；
- CH13 Physical/Sensory 各对象、身体行为、方案比较与构造可分别成页；
- CH15 Detail 允许平面、剖面、人体、材料、连接、维护分开近读；
- CH16 Technical 不把多个技术图缩成卡片墙。

## 4｜Web 源码与页面结构

Web 实现必须显式区分：

- `<section data-chapter="CHxx">` = 章节容器；
- `<article data-page-id="C04-WEB-Pxxx">` 或 `<article data-page-id="C04-WEB-Nxxx">` = 页面；
- 页面内部的 figure/card/grid = 模块，不计页。

构建与 readback 必须输出两个不同计数：

- `chapter_count`
- `page_count`

禁止再输出“21 个章节载体 = 21 页”这类结果。

浏览器/导出审查必须逐 PAGE-ID 截取或记录，而不是每个 `<section>` 截一张总图。

## 5｜迁移动作

原 52 页逐页只能先使用：

- `KEEP`
- `MOVE`
- `REWRITE`
- `REDRAW`
- `EXPAND`
- `PROCESS`
- `ARCHIVE CANDIDATE`

`MERGE` 不再作为默认动作。

如确需合并，必须经过独立设计审查后标为：

`MERGE CANDIDATE → INDEPENDENT REVIEW → APPROVED / REJECTED`

没有独立批准 = 不合并。

## 6｜页面增加规则

当前目标不是“保持52页”，而是**先完整，再编辑**：

`52页基线 + 缺失专业页面 = 新的实际页面总数`

允许并要求补充：
- 场地/山水/路线/环境分析
- 地域文化与内容来源分析
- 人群与行为分析
- 设计原理
- 设计方法
- 总体系统
- App信息架构、状态、组件、离线与退场
- 十三印深入示例
- Physical/Sensory 人体、CMF、构造、维护
- Memory/IP 产品与使用细节
- R01/R05/R06/R13关键场景
- 平面/立面/剖面/轴测/爆炸/节点
- 技术证明
- 方案演化与选择依据

只有在这些内容补齐后，才允许对真正重复或弱的页面做独立逐页编辑。

## 7｜预览与交付规则

任何“全部预览”必须满足：

1. 以 PAGE-ID 为单位展示全部页面；
2. 章节标题可以作为分隔页/导航，但不能替代其内部页面；
3. 总览图必须能看到全部 PAGE 缩略图，不得只显示章节封面；
4. 导出 ZIP 必须包含逐页 PNG/PDF 页或可对应 PAGE-ID 的浏览器截图；
5. 报告同时写明 `chapter_count` 与 `page_count`；
6. 页面新增后，旧的 52 数字不得继续被冒充为当前总页数。

## 8｜当前边界保持

本修正不改变：
- `ROUTE-03 = LOCKED CURRENT`；
- `JOURNEY-04 = PROVENANCE / NON-CURRENT`；
- R06 = `FINISHED / FROZEN / NO REOPEN`；
- R01–R13完整保留；
- App、Physical/Sensory、Memory/IP、Audience、C22/C23/Model、Motion 全部保留；
- Physical KEEP/HOLD 状态不因页面增加改变；
- `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`。

## 9｜当前执行顺序

1. 锁定原 52 PAGE-ID，不删除、不合并；
2. 将 52 页逐页绑定到 CH00–CH18；
3. 建立缺页清单；
4. 新增 N-series PAGE-ID；
5. 用页面而非章节重建 Web 顺序；
6. 对每个 PAGE-ID 做 finished-pixel readback；
7. 独立设计审查；
8. 最后才处理真正重复页面。

**本版的核心不是“页数更多”，而是恢复正确结构：章节管理页面，页面承载设计。**
