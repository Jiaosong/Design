# C04 Web v1.9｜中文完整项目架构 successor

## 角色
- 下游 Web / 展示载体；不替代 C04 项目 Authority。
- 继承 v1.8 / v1.4 已完整 readback 的 52 个独立页面/语义 surface 作为**页面基线**。
- 绑定 `C04-B_PROJECT-ARCHITECTURE_v3.0` 的专业内容架构，并服从 v3.1 的 `CHAPTER ≠ PAGE` 无压缩规则。

## 最优先结构规则

> **章节是章节，页面是页面。**
>
> `PROJECT → CHAPTER → PAGE → MODULE / FIGURE / ASSET`

- `chapters/*.html` 文件与 `<section class="chapter">` 只负责章节组织，不代表一页。
- 章节内部 `<article>` 是当前独立页面/surface 单元。
- 原 52 个页面必须保持独立身份；新增分析、原理、方法、人群、细节等只增加页面，不能用章节重组替代旧页。
- 页面总数由实际 PAGE/article 单元统计，不能由章节数、章节文件数、导航点或预览拼版数推断。
- 构建脚本分别输出 `chapter_count` 与 `page_count`，并设置 `page_count >= 52` 的 no-compression floor。

## 构建
`python build.py`

构建顺序由 `chapters/*.html` 文件名控制；CSS 由 `style_parts/*.css` 顺序合并。

构建必须输出：
- `chapter_count`
- `page_count`
- `legacy_page_floor=52`

如果独立页面数低于 52，构建直接失败。

## 当前修改
- 中文主导航与中文章节状态。
- 新增项目问题、场地分析、人群分析、游程行为、设计原理、设计方法、总体策略、设计深化、方案演化等专业深度页面。
- 现有 Hero、ROUTE-03、十三印、Game Map、App、关键场景、Physical、Memory、Technical、Motion、Return 继续复用。
- v1.7 的 Scene / Physical / Technical 成熟 delta 继续作为当前下游源；Journey 使用 v1.8 ROUTE-03 lock rebind。

## 页面迁移纪律
- 原 52 页先锁定独立 PAGE identity，再映射到 CH00–CH18。
- 默认动作：`KEEP / MOVE / REWRITE / REDRAW / EXPAND / PROCESS / ARCHIVE CANDIDATE`。
- `MERGE` 不是默认动作；只有独立逐页审查批准后才允许合并。
- 新增专业内容使用新的 PAGE identity，不复用旧页 ID。
- “21 个章节载体 = 21 页”属于错误计数，禁止再次输出。

## 无损与边界
- 不把 52 页作为上限；新增真实专业内容允许增加页面/semantic surface 数量。
- 不删除 R01–R13、App、Physical/Sensory、Memory/IP、Audience、C22/C23/Model。
- `ROUTE-03` 保持锁定当前；`JOURNEY-04` 不恢复为 CURRENT。
- R06 体验冻结，不重开。
- P02 / PHY-01 / Fluid Rest / Qingfengyin 等继续服从当前 KEEP/HOLD 状态。
- `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`。

本源码提交证明架构和内容源已改变，不证明 finished-pixel Design PASS 或 Browser PASS。
