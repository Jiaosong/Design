# OLEANDER｜SP02-R03 v1.2｜Multi-Provider Runtime Closure

**Handoff Artifact：POST-REVIEW PASS**  
**SP02 Runtime：ACTIVE / RUNTIME GATE OPEN**

## Solve Gate Decomposition
`SG00 Authority → SG01 Native Definition → SG02 Solve Request → SG03 Solve Completion → SG04 Tree Extraction → SG05 Contract Match → SG06 Adverse Visibility → SG07 Repeatability`

- `CP2-CORE = SG00—SG03`
- `CP2-DATA = SG04—SG06`
- `CP2-REPRO = SG07`
- `CP2 = SG00—SG07`

这不是降低最终 CP2 标准，而是把“真实 Grasshopper solve”从黑箱拆成可由不同 Provider 分阶段关闭的证据门槛。

## Provider strategy
- GUI Windows/macOS/Human Authority：可一次关闭 SG00—SG07，并补 CP4。
- Rhino.Compute/headless：可直接关闭 CP2-CORE；若定义显式输出五个 tree signatures，可继续关闭 CP2-DATA；重复 solve 可关闭 CP2-REPRO；CP4 仍不能单独关闭。
- GrasshopperPlayer：可关闭 solve microgates；Data gate 需要 evidence writer；CP4 需要 GUI supplement。
- Provider preflight / Offline Python / Rhino3dm：不能关闭 solve microgate。

## Current truth
当前没有真实 native `.gh/.ghx` solve，因此：
`SG00 OPEN / SG01 OPEN / CP2 OPEN / CP4 OPEN`。

详见：
- `solve_gate/solve_gate_decomposition.json`
- `solve_gate/provider_microgate_capabilities_v1.2.json`
- `validator/validate_solve_microgates_v1_2.py`
- `docs/SOLVE_GATE_DECOMPOSITION_v1.2.md`
- `docs/COMPUTE_HEADLESS_CP2_PROTOCOL_v1.2.md`
- `docs/GUI_CP4_SUPPLEMENT_v1.2.md`
