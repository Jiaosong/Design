# P05｜Rhino.Compute Headless Adapter

状态：**ADAPTER READY / PROVIDER NOT CONNECTED**。

Rhino.Compute/Hops-compatible server 可作为真实 headless Rhino + Grasshopper authority：在 exact definition identity、solver response 与 tree contract 都闭合时，可以关闭 **CP2**；但 headless server 没有 Grasshopper canvas / Parameter Viewer GUI，因此**不能单独关闭 CP4**。

Required evidence: provider receipt, definition SHA256, server run/request trace, real solver response, provider-adapted `tree_runtime.json`, schema validation.

HTTP 200、server health check、Hops/provider preflight 均不能替代 solve evidence。
