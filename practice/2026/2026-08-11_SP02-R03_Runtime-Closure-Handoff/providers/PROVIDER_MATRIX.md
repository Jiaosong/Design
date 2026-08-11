# SP02-R03 v1.1｜Multi-Provider Runtime Closure Matrix

核心：**Provider 不按“能不能运行”分类，而按“能关闭哪个 Gate”分类。**

| ID | Provider | CP2 | CP4 | 关键边界 |
|---|---|---:|---:|---|
| P01 | GUI_WINDOWS_DESKTOP | YES | YES | provider preflight 不能替代 runtime |
| P02 | GUI_MACOS_DESKTOP | YES | YES | provider preflight 不能替代 runtime |
| P03 | HUMAN_AUTHORITY_GUI | YES | YES | verbal confirmation without artifacts 无效 |
| P04 | CLOUD_WINDOWS_VM | YES | CONDITIONAL_GUI | CP4 requires readable Parameter Viewer/canvas evidence |
| P05 | RHINO_COMPUTE_HEADLESS | YES | NO | CP2 requires exact real solve; CP4 cannot close alone |
| P06 | GRASSHOPPER_PLAYER_DESKTOP | YES | NO_UNLESS_GUI_SUPPLEMENT | CP4 需单独 GUI/Parameter Viewer 证据 |
| P07 | FUTURE_COMPATIBLE_PROVIDER | CONDITIONAL | CONDITIONAL | 必须先有 adapter + authority proof |

## Gate Rule
- **CP2** = real Rhino + Grasshopper solve + exact tree contract match.
- **CP4** = readable real Parameter Viewer / Grasshopper canvas provenance evidence.
- Headless Compute 可以关闭 CP2，但**不能单独关闭 CP4**。
- Human Authority 是有效 Provider，但口头确认不是证据。
- Cloud VM 的“云”不是证据；仍需 Rhino/Grasshopper runtime receipt。
- 任何 provider preflight 都只能证明 provider reachability，不能证明 Grasshopper solve。
