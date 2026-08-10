# Path Mapper Contract｜SP02 Rerun 02

Status: `OFFLINE EXECUTABLE SPEC / GRASSHOPPER RUNTIME OPEN`

关键校正：

- Base tree 的路径只有 `{z}`，item index 仍存在于 branch 内部顺序。
- **Path Mapper 只重写 path，不会自动读取 branch 内 item index。**
- 因此要得到“同 item index 跨 zone 分组”的 `6 × 4`，Grasshopper 可执行路径应为：

```text
Base {z}
  -> Graft
     {z;i}
  -> Path Mapper
     {A;B} -> {B}
  -> Transpose target {i}
```

目标：
- Graft 后：`{0;0}` ... `{3;5}`，共 24 branches × 1 item。
- Path Mapper `{A;B}->{B}` 后：`{0}` ... `{5}`，共 6 branches × 4 items。
- 若不先 Graft，单纯 `{A}->{...}` 无法根据 branch 内 item 序号产生 `{i}`。

CP4 仍 OPEN：此文档只是 Grasshopper 构造规格。只有真实 Grasshopper 中 Path Mapper 前后 Parameter Viewer / Panel / TStats 证据才能关闭 CP4。
