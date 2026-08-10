# Failure-seeking Report

## NOMINAL
4×6 → Graft 24×1 → Flatten 1×24 → Transpose 6×4。  
状态：`OFFLINE STRUCTURE PASS`

## ADVERSE
`{2}` 从 6 items 降为 5 items。Transpose `{5}` 只有 3 items。  
状态：`EXPECTED MISMATCH DETECTED`

**修正原则：** 返回上游恢复 branch contract，或显式接受不等长 branch；不得用 Flatten 隐藏 mismatch。

## FAILURE-SEEKING
`{1}` 为空 branch，`{3}` 含一个 null item。  
状态：`SIM-FAIL / REWORK REQUIRED`

**修正原则：** 在任何全局聚合前检查 empty branch / null item，并保持 zone provenance。
