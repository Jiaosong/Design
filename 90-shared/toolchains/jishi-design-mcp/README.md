# JiShi Design MCP bridge

Purpose: connect **即时设计 / JiShi Design** to the existing Chat On Steroids local MCP execution bridge without creating a second OLEANDER authority or control plane.

## Pinned runtime

- MCP server: `@jiujiang/jishi-mcp-server@1.2.0`
- launcher: `npx -y @jiujiang/jishi-mcp-server@1.2.0`
- local WebSocket: `127.0.0.1:19999`
- JiShi plugin: `九匠即时MCP`
- Node.js: 18+

The JiShi plugin must be open in the target document. Green `已连接` in the plugin panel is runtime evidence; package registration alone is not a live-runtime PASS.

## Authority boundary

This adapter is an execution capability under `chat_on_steroids_local_execution_bridge`.

- `READ_CANVAS`, `READ_SELECTION`: allowed only after target document resolution.
- export: subject to the active OLEANDER output contract.
- canvas mutation: must pass the active OLEANDER resolver/side-effect gate.
- `execute_script`: high-side-effect capability; never treated as default permission.
- local registry state records transport/deployment/health only and must not create or overwrite Project State, Source Authority, Design Authority, Knowledge Authority, Skill routing, promotion state, or completion state.

## Reversible registration

Dry-run first; it changes nothing:

```powershell
powershell -ExecutionPolicy Bypass -File .\90-shared\toolchains\jishi-design-mcp\scripts\register-cos-jishi-mcp.ps1
```

Apply the same reviewed patch:

```powershell
powershell -ExecutionPolicy Bypass -File .\90-shared\toolchains\jishi-design-mcp\scripts\register-cos-jishi-mcp.ps1 -Apply
```

The registrar:

1. verifies Node.js 18+ and `npx`;
2. performs an idempotent upsert rather than replacing unrelated MCP entries;
3. backs up both local JSON files before writing;
4. rolls both files back if either write fails;
5. does **not** restart Chat On Steroids;
6. leaves the runtime entry `STAGED / UNVERIFIED` until live readback succeeds.

Default local targets:

- `%APPDATA%\chat-on-steroids\state\plugins.json`
- `D:\Desgin\.mcp-runtime\registry\OLEANDER_INTEGRATION_REGISTRY_CURRENT.json`

## Validation gate

After registration:

1. Open JiShi Design and run `九匠即时MCP` in the intended document.
2. Confirm its panel is green `已连接`.
3. Read-only probe: `list_plugin_clients`.
4. Resolve the intended `clientId` when more than one document is present.
5. Read-only probe: `get_page_nodes`, then `get_selection` if needed.
6. Only after those readbacks pass may OLEANDER authorize export or mutation.

`Registration PASS != Runtime PASS != Design PASS`.
