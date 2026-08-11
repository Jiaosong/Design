# SP02-R03｜Manual Grasshopper Definition Build Contract

本文件只规定**真实 Grasshopper 定义**应如何构造；它本身不是 runtime evidence。

## 1｜Nominal base tree
建立 4 个 zone，每区 6 个点。最终进入一个 Generic Data / Point 参数，NickName 必须设为：

`SP02_BASE`

其真实运行时目标：
- paths `{0}`–`{3}`
- branch count = 4
- 6 items / branch
- total = 24

旁接一个 `Param Viewer`，NickName = `PV_BASE`。

## 2｜Graft
从 `SP02_BASE` 接真实 Grasshopper `Graft Tree` 操作。输出再接一个独立 Generic Data 参数：

`SP02_GRAFT`

目标：
- 24 branches × 1
- path 应成为两级 `{z;i}`

旁接 `Param Viewer`：`PV_GRAFT`。

## 3｜Flatten
从 Base 建独立支路接真实 `Flatten Tree`，输出命名：

`SP02_FLATTEN`

目标：
- `{0}`
- 1 branch × 24

旁接 `Param Viewer`：`PV_FLATTEN`。

## 4｜Transpose by item index
只能使用现行合同：

`SP02_BASE → Graft → Path Mapper {A;B}->{B}`

Path Mapper 后输出命名：

`SP02_TRANSPOSE`

目标：
- paths `{0}`–`{5}`
- 6 branches × 4
- total 24

旁接 `Param Viewer`：`PV_TRANSPOSE`。

**不得**把 Base `{z}` 直接 Path Mapper 当成 transpose，因为 branch 内 item index 尚未进入 path。

## 5｜Adverse case
复制 nominal 输入，但令 zone `{2}` 只有 5 items。按同样 Graft → Path Mapper 运行。

输出命名：

`SP02_ADVERSE_TRANSPOSE`

目标 branch lengths：
`[4,4,4,4,4,3]`

旁接 `Param Viewer`：`PV_ADVERSE`。

该缺口必须可见；不得 Flatten 修补。

## 6｜Evidence capture
真实 Rhino/Grasshopper solve 后必须保留：
- 源 `.gh` 或 `.ghx`
- solved `.ghx`
- `runtime_receipt.json`
- `tree_runtime.json`
- `component_inventory.json`
- `grasshopper_canvas_four_state.png`
- `rhino_viewport_four_state.png`
- `adverse_case_canvas.png`

`SP02_R03_capture_runtime.py` 会自动读取五个命名 sink、真实 solve、保存 solved GHX、尝试 Rhino viewport 与 GH canvas capture。

如果自动 GH canvas capture 不可用，人工打开定义后截取同一画布，要求五个 Param Viewer 的路径信息清晰可读。

## 7｜Hard Gate
- 没有真实 Rhino + Grasshopper solve：CP2 OPEN
- 没有 Param Viewer 可读证据：CP4 OPEN
- JSON 正确但截图不可读：AR-G10 / AR-S01 FAIL
- 截图好看但 tree_runtime 与 contract 不符：CP2 FAIL
