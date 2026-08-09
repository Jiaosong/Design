# 2026-08-09｜SP02｜Grasshopper Data Tree 关系拓扑训练

Status: TRAINING PROTOTYPE / GRASSHOPPER EXECUTION PENDING

## Objective
把“空间关系”编码为稳定的数据树，而不是先做造型。训练对象为 4 个区域 × 每区 6 个节点的练习拓扑；所有尺寸、数量与参数均为练习用假设参数，不代表项目数据。

## Structure contract
- `{zone}` = 空间区域分支。
- `[item]` = 区域内节点。
- 初始结构：4 branches × 6 items。
- Graft 后：24 branches × 1 item，用于逐节点操作。
- Flatten 后：1 branch × 24 items，只允许用于明确需要全局集合的操作；不得作为默认修复手段。
- Path Mapper 练习：从按区域分组切换到按节点序号跨区域配对。

## Grasshopper reproduction
1. 建立 4 组点，每组 6 点；用 Entwine/Merge 形成 `{0}`–`{3}` 四个分支。
2. 用 Param Viewer/TStats 检查 branch count、paths 与每分支 item count。
3. A 方案保持原树，分别对每个 zone 建立 Polyline。
4. B 方案 Graft：每个 item 成为独立 branch，观察下游组件匹配变化。
5. C 方案 Flatten：比较拓扑丢失后 Polyline/连接逻辑如何改变。
6. 用 Path Mapper 重组路径，使同序号节点跨 zone 成组，再建立横向连接。
7. 保存 `.gh`，并截图 Parameter Viewer、A/B/C 输出与最终重组结构。

## Checkpoints
- CP1 输入路径必须明确，不接受“看起来对”。
- CP2 每次 Graft/Flatten/Path Mapper 后记录 paths 与 item counts。
- CP3 几何输出必须能追溯到数据结构变化。
- CP4 不得用 Flatten 掩盖未知的 tree mismatch。

## Official basis
McNeel Grasshopper Guides: Advanced Data Structures; Grasshopper DataTree API. Accessed 2026-08-09.

## Runtime boundary
当前自动化环境未运行 Rhino/Grasshopper，因此 `.gh`、Rhino viewport 和真实 Grasshopper Parameter Viewer 截图均为 PENDING。仓库中的脚本与参数说明是复现材料，不得描述为已在 Grasshopper 中执行。