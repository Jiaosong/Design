# COS local-file upload route

The official Baidu Netdisk MCP repository states that local-file upload is available only through its local stdio implementation because it needs direct filesystem access.

The reference implementation used for this candidate was checked out at:

`D:\Desgin\.mcp-runtime\baidu-netdisk-mcp-official`

Reference server:

`src\baidu-netdisk\fileupload_tool.py`

Do not put the Baidu token into repository files. Supply it through `BAIDU_NETDISK_ACCESS_TOKEN`.

Typical local MCP configuration shape:

```json
{
  "mcpServers": {
    "baidu-netdisk-local-uploader": {
      "command": "python",
      "args": [
        "D:/Desgin/.mcp-runtime/baidu-netdisk-mcp-official/src/baidu-netdisk/fileupload_tool.py"
      ],
      "env": {
        "BAIDU_NETDISK_ACCESS_TOKEN": "<SECRET_FROM_LOCAL_SECRET_STORE>"
      }
    }
  }
}
```

OLEANDER execution rule:

`owner-native artifact → exact local revision/hash → local upload → Baidu provider readback → storage binding → owner-native Project State writeback only when that project mechanism requires it`.

The official uploader itself does not know OLEANDER Project State. The caller must enforce the `/OLEANDER_VAULT` target and the current/overwrite policy before invoking it.
