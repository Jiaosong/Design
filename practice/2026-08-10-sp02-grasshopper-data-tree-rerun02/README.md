# OLEANDER SP02｜Grasshopper Data Tree 关系拓扑训练｜Rerun 02

日期：2026-08-10  
来源：`2026-08-09｜SP02｜Grasshopper Data Tree 关系拓扑训练`

## 状态
`OFFLINE STRUCTURE EXECUTED / PATH-MAPPER CONTRACT CORRECTED / PUBLIC COMPUTE PREFLIGHT BLOCKED / CP2 OPEN / CP4 OPEN`

本轮真实执行：
- Base / Graft / Flatten / Transpose 离线结构；
- branch / item count 断言；
- 两次独立重复运行哈希一致性检查；
- ADVERSE 与 FAILURE-SEEKING；
- Path Mapper 可执行路径校正；
- 四态 PNG / SVG 与 DXF 拓扑；
- `FREE_PUBLIC_COMPUTE` Run 10 只作为 provider preflight 证据读取。

未执行：
- Rhino / Grasshopper desktop；
- 真实 `.gh`；
- Parameter Viewer / Panel / TStats；
- Rhino viewport；
- 公共 Compute Grasshopper solve（provider disabled 后被 selector 正确跳过）。

## 练习参数
- zones = 4
- items per zone = 6
- DX = 2.4
- DY = 3.6

均为 `SIM / EXERCISE ASSUMPTION`。

## 四态
- Base `{z}` → 4 × 6
- Graft `{z;i}` → 24 × 1
- Flatten `{0}` → 1 × 24
- Graft → Path Mapper `{A;B}->{B}` → 6 × 4

## 关键技术校正
Transpose 目标不能仅写成“Base + Path Mapper”。
因为 Path Mapper 只改 path，不读取 branch 内 item index。要按 item index 跨 zone 重组，应先 Graft 生成 `{z;i}`，再映射 `{A;B}->{B}`。

## Repeatability
- Run 1 hash: baf831e6a8b70201d5020ce764ad5c89818e1c2daba63fbfa5f938ea0a6bb3a9
- Run 2 hash: baf831e6a8b70201d5020ce764ad5c89818e1c2daba63fbfa5f938ea0a6bb3a9
- Equal: `True`

只证明离线规格确定性，不证明 Grasshopper runtime equivalence。

## CP 状态
- CP1：PASS（离线路径语义）
- CP2：OFFLINE PASS / REAL GH OPEN
- CP3：PASS（Flatten 使用边界）
- CP4：OPEN（无真实 Parameter Viewer 前后证据）

## 结论
关系拓扑先于几何外观。
本轮增加的价值不是更多图，而是把 `Transpose` 从抽象描述推进为可直接在 Grasshopper 中搭建的 path contract。
