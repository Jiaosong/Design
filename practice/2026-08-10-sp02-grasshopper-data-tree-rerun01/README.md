# OLEANDER SP02｜Grasshopper Data Tree 关系拓扑训练｜Rerun 01

日期：2026-08-10  
来源训练：2026-08-09｜SP02｜Grasshopper Data Tree 关系拓扑训练

## 状态
`OFFLINE STRUCTURE EXECUTED / RHINO-GRASSHOPPER RUNTIME NOT AVAILABLE`

本次真实执行 Python 数据树复现、branch/item count 断言、关系拓扑生成、DXF/SVG/PNG 输出与 failure-seeking。  
**没有运行 Rhino / Grasshopper，因此没有 `.gh`、Parameter Viewer 截图或 Rhino viewport 证据；不得标记为 Grasshopper TESTED/VERIFIED。**

## 练习用假设参数
- zones = 4
- items per zone = 6
- DX = 2.4
- DY = 3.6

以上均为 `SIMULATED / EXERCISE ASSUMPTION`，不代表实际项目尺寸或数据。

## 实际执行结果
- Base：4 branches × 6 items = 24
- Graft：24 branches × 1 item = 24
- Flatten：1 branch × 24 items
- Transpose by item：6 branches × 4 items = 24

所有离线结构断言均通过。

## 关系判断
- Base path `{z}` 表示 **zone identity**；下游几何默认在 zone 内匹配。
- Graft `{z;i}` 把每个 item 升级为独立 branch，适合逐元素匹配。
- Flatten 把全部 item 变成全局集合，**会删除 zone identity**，只能在明确需要全局集合时使用。
- Transpose `{i}` 把同一 item index 的 4 个 zone 节点聚成一支，直接表达跨 zone 对位关系。

## Failure-seeking
1. ADVERSE：zone 2 少一个 item，Transpose 的 `{5}` 只有 3 个成员。应显式暴露 mismatch，不得补丁式 Flatten。
2. FAILURE-SEEKING：存在空 branch + null item；若先 Flatten，会掩盖 zone 级缺失，因此状态为 `SIM-FAIL / REWORK REQUIRED`。

## 训练结论
本次真正训练的是 **关系拓扑先于几何外观**。Path 是设计语义，不只是 Grasshopper 技术细节。  
下一步必须在 Rhino / Grasshopper 中用 `Param Viewer / Panel / TStats` 复核本次结构，再生成 `.gh` 和 viewport 截图，才能关闭昨天的运行时 PENDING。
