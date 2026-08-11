# OLEANDER｜SP02-R03 v1.1｜Multi-Provider Runtime Closure

**Handoff Artifact：POST-REVIEW PASS**  
**SP02 Runtime：ACTIVE / RUNTIME GATE OPEN**  
**CP2：OPEN｜CP4：OPEN**

本版修正 v1.0 过度绑定 self-hosted Windows 的问题。R03 现在是 provider-neutral closure architecture。

## Provider families
- P01 Windows Rhino 8 GUI → CP2 + CP4 capable
- P02 macOS Rhino 8 GUI → CP2 + CP4 capable
- P03 Human Authority GUI → CP2 + CP4 capable
- P04 Cloud Windows VM → CP2；CP4 取决于 GUI evidence
- P05 Rhino.Compute headless → **CP2 capable / CP4 cannot close alone**
- P06 GrasshopperPlayer desktop → CP2 capable；CP4 需 GUI supplement
- P07 Future provider → 必须先实现 adapter + authority proof

## Shared closure chain
`Provider → provider_receipt → tree_runtime → component inventory / GUI evidence → provider-neutral validator → CP2/CP4 → Final Artifact Review`

## Current truth
本包仍未执行真实 Rhino/Grasshopper，因此不会把 v1.1 架构改写成 Runtime PASS。它只关闭“必须依赖某一台 Windows self-hosted runner”的错误假设。

详见 `providers/PROVIDER_MATRIX.md` 与 `contracts/provider_receipt_schema.json`。
