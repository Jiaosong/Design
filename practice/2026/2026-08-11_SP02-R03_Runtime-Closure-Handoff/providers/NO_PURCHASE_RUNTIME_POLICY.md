# SP02-R03｜No-Purchase Runtime Policy

**Hard constraint：NO_PURCHASE = TRUE**

SP02 不得为了关闭 CP2 / CP4 而要求用户新增购买 Rhino、Rhino.Compute、Cloud VM 或任何其他付费 Runtime Provider。

## Allowed provider priority
1. **EXISTING_LICENSED_MACHINE** — 公司、学校、朋友、工作室或其他已经合法安装并授权 Rhino 8 的机器。
2. **HUMAN_AUTHORITY_GUI** — 由已有 Rhino 8 的协作者运行 `ONE_CLICK_CP2`，回传完整 evidence；口头确认无效。
3. **OFFICIAL_EVALUATION_IF_CURRENTLY_AVAILABLE** — 只有在执行当日重新核验官方条款且无需购买时才允许使用；不得把历史试用政策当成当前事实。
4. **FREE_EXISTING_RUNTIME_PROVIDER** — 仅当 provider 实际可执行且产生真实 Grasshopper evidence 时使用；preflight / disabled service 不算 runtime。
5. **STOP / PRESERVE OPEN** — 如果以上均不可用，SP02 保持 `ACTIVE / RUNTIME GATE OPEN`，停止投入，不为练习闭环产生采购成本。

## Disallowed actions
- 为 SP02 新购 Rhino license。
- 为 SP02 新购 Rhino.Compute licensing / credits。
- 为 SP02 新开付费 Cloud Windows VM。
- 购买第三方代跑服务仅为了提高 Practice 状态。
- 用 offline Python、Rhino3dm、mock GHX、provider preflight 或 synthetic screenshot 替代真实 runtime。

## Gate truth under no-purchase policy
`NO_PURCHASE` 不降低 CP2 / CP4 标准。

如果没有免费或已有授权的真实 provider：
- CP2 保持 OPEN；
- CP4 保持 OPEN；
- SP02 可以作为 `RUNTIME-BLOCKED PRACTICE REFERENCE` 归档，但不得写成 `PRACTICE CLOSED`。

## Existing one-click kit
现有 `ONE_CLICK_CP2/RUN_CP2.cmd` 保留。它只用于**已经有可合法使用 Rhino 8 的机器**，不构成购买建议。
