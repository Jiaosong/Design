# OLEANDER｜SP02-R03｜Runtime Closure Handoff

**Current status: RUNTIME HANDOFF READY / REAL RHINO-GRASSHOPPER NOT EXECUTED**

本包不是 Rerun 03 的离线替代品，而是 SP02 的最后一个真实运行交接层。当前环境没有 Rhino 8，因此 CP2 / CP4 仍 OPEN。

## Why this package exists
SP02-R01/R02 已经把离线 Data Tree contract 做到足够成熟；继续增加 Python 图表没有项目价值。R03 只解决：

1. 真实 Rhino 8 + Grasshopper 是否实际 solve；
2. Base / Graft / Flatten / Graft→Path Mapper 是否与离线合同一致；
3. Parameter Viewer 是否能在真实组件图中证明 path provenance；
4. adverse case 是否被真实 Grasshopper 暴露而不是被 Flatten 隐藏。

## Execute
### Windows
`runner/run_windows.ps1 -GhFile C:\path\SP02_R03.gh`

### macOS
`runner/run_macos.sh /path/SP02_R03.gh`

两者都要求本机已安装并能正常授权 Rhino 8。

## Required definition nicknames
Data sinks:
- SP02_BASE
- SP02_GRAFT
- SP02_FLATTEN
- SP02_TRANSPOSE
- SP02_ADVERSE_TRANSPOSE

Parameter Viewers:
- PV_BASE
- PV_GRAFT
- PV_FLATTEN
- PV_TRANSPOSE
- PV_ADVERSE

## Truth rules
- 公共 compute preflight ≠ runtime。
- Rhino3dm ≠ Grasshopper solve。
- `.ghx` 文件存在 ≠ 已执行。
- workflow green ≠ artifact PASS。
- Runtime JSON PASS ≠ final artifact PASS。

官方 Rhino 8 支持 `GrasshopperPlayer` 执行 `.gh/.ghx`、`/runscript` 启动脚本；Grasshopper API 提供 `GH_Document.NewSolution` 与 `GH_DocumentIO.SaveQuiet`。本包采用这些真实 API 路径，但当前包自身没有执行 Rhino。

## Closeout
只有：
`CP2 PASS + CP4 PASS + Runtime↔Offline Contract PASS + AR-G01—G10 + AR-S01/S04/S07/S09 POST-REVIEW PASS`
才允许 SP02 `PRACTICE CLOSED`。
