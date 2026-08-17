# C04 Web v1.9｜中文完整项目架构 successor

## 角色
- 下游 Web / 展示载体；不替代 C04 项目 Authority。
- 继承 v1.8 的 52 个可见语义对象作为无损资产库存。
- 绑定 `C04-B_PROJECT-ARCHITECTURE_v3.0` 的中文项目架构。

## 构建
`python build.py`

构建顺序由 `chapters/*.html` 文件名控制；CSS 由 `style_parts/*.css` 顺序合并。

## 当前修改
- 中文主导航与中文章节状态。
- 新增项目问题、场地分析、人群分析、游程行为、设计原理、设计方法、总体策略、设计深化、方案演化等专业深度页面。
- 现有 Hero、ROUTE-03、十三印、Game Map、App、关键场景、Physical、Memory、Technical、Motion、Return 继续复用。
- v1.7 的 Scene / Physical / Technical 成熟 delta 继续作为当前下游源；Journey 使用 v1.8 ROUTE-03 lock rebind。

## 无损与边界
- 不把 52 页作为上限；新增真实专业内容允许增加页面/semantic surface 数量。
- 不删除 R01–R13、App、Physical/Sensory、Memory/IP、Audience、C22/C23/Model。
- `ROUTE-03` 保持锁定当前；`JOURNEY-04` 不恢复为 CURRENT。
- R06 体验冻结，不重开。
- P02 / PHY-01 / Fluid Rest / Qingfengyin 等继续服从当前 KEEP/HOLD 状态。
- `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`。

本源码提交证明架构和内容源已改变，不证明 finished-pixel Design PASS 或 Browser PASS。
