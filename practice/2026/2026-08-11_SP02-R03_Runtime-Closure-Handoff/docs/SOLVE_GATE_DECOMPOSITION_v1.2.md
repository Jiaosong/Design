# SP02-R03 v1.2｜Solve Gate Decomposition

旧 CP2 的“真实 Grasshopper solve”被拆为 8 个可独立验证的微门槛：

1. `SG00 Runtime Authority`
2. `SG01 Native Definition Load`
3. `SG02 Solve Request`
4. `SG03 Solve Completion`
5. `SG04 Tree Extraction`
6. `SG05 Contract Match`
7. `SG06 Adverse Visibility`
8. `SG07 Repeatability`

组合关系：
- `CP2-CORE = SG00—SG03`
- `CP2-DATA = SG04—SG06`
- `CP2-REPRO = SG07`
- `CP2 = SG00—SG07 全部 PASS`

这不是降低标准，而是允许 headless / GUI / Human Authority 等 Provider 分阶段提供真实证据。

当前真实状态仍为 `CP2 OPEN / CP4 OPEN`。
