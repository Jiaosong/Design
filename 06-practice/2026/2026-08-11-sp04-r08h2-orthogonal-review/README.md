# SP04-R08H.2｜A04 正交视图重构

## 目的
修正 R08H.1 中把“沿窗框周边锚固间距”“结构边距”“锚固深度”和“控制层冲突”混在同一视图的问题。

## 三个视图
- A1｜1:10 角部立面：150 首锚距、450/600 周边间距。
- A2｜1:2 锚固剖面：75 框、12 安装缝、45 锚固深度、30 保温回包、20 局部隔热垫、防水/气密桥接、结构基层。
- A3｜1:5 结构边缘定位：60 结构边距。

## 证据边界
以上数值均为**练习用假设参数**，不是规范、厂家或实际项目要求。
20 mm 局部隔热垫仅用于讨论热桥削弱路径；金属紧固件仍形成热桥，不能将本节点描述为“完全断桥”。

## Mandatory Post-Generation Review Gate｜成品审查硬门槛
任何图纸、模型、分析图、参数表、脚本输出或交付包，在生成与自动 QA 后必须再次打开最终成品执行独立成品审查。自动 QA、脚本 PASS、bbox=0、导出成功不能替代成品审查。

状态：`REVIEW PENDING` → `POST-REVIEW FAIL / NEEDS REVISION` → 修正并重新审查 → `POST-REVIEW PASS`。只有 `POST-REVIEW PASS` 才允许标记 DONE / PASS / Candidate。

## 2026-08-11｜Post-Generation Review｜最终成品审查
**Final Status：POST-REVIEW PASS**

- Visual hierarchy：PASS — A1 / A2 / A3 已按周边间距 / 锚固剖面 / 结构边距拆分。
- Text + Graphic Boundary：PASS — 自动双边界检查 0 / 0；最终成品复核无跑框、阻断阅读的遮挡或版块穿越。
- Geometry ↔ Dimension：PASS — A1 150/450/600 @1:10；A2 12/30/20/45/75 @1:2；A3 60 @1:5，均由参数 × 比例生成。
- Scale：PASS — 不再把不同测量方向混在同一视图。
- Construction Logic：PASS WITH PENDING — 60 结构边距位于 A3 正交视图；45 锚固深度位于 A2；承载型隔热垫仍为 H/P；金属紧固件热桥仍 PENDING。
- Evidence / PENDING：PASS — 所有数值仍是练习用假设参数。
- Reproduction：PASS — 最终 editable SVG 已独立重新轮廓化并输出检查 PNG。

任何后续修改都会使本次 POST-REVIEW PASS 失效，必须重新执行 AUTO QA + 最终成品审查。