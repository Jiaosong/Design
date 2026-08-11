# Compute / Headless CP2 Protocol

## H1｜CP2-CORE
真实 Compute provider receipt + native `.gh/.ghx` hash + solve request + successful completion/output fingerprint。关闭 `SG00—SG03`。

## H2｜CP2-DATA
定义必须显式输出五个 tree signatures：`BASE / GRAFT / FLATTEN / TRANSPOSE / ADVERSE_TRANSPOSE`，每个包含 `paths / branch_count / data_count / branch_lengths`。关闭 `SG04—SG06`。

## H3｜CP2-REPRO
相同 definition hash 与相同输入至少再次 solve 一次，结构签名一致。关闭 `SG07`。

`CP2 = H1 + H2 + H3`。

即使 Compute 已关闭 CP2，`CP4` 仍 OPEN；CP4 必须由真实 GUI Parameter Viewer / Grasshopper canvas 补证。
