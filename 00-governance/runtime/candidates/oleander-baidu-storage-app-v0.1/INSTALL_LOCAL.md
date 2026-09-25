# Local install / test

The selected runtime is the workstation-local COS/Codex plugin using MCP stdio.

## 1. Configure Baidu authorization once

Run:

```powershell
.\configure_baidu_token.ps1
```

The script accepts either the access token itself or copied authorization text containing `access_token=`. It stores only the extracted token using Windows DPAPI at:

`%LOCALAPPDATA%\OLEANDER\secrets\baidu-netdisk-access-token.dpapi`

Do not place the token in Git, plugin archives or chat messages.

## 2. Plugin runtime

`plugin-v0.1.1-candidate/mcp.json` uses `stdio`. Codex/COS launches:

`runtime/run_stdio_secure.ps1 → runtime/stdio_entry.py → FastMCP stdio`

The wrapper decrypts the DPAPI token only inside the child process and clears the environment variable when that process exits.

No localhost server needs to be started before using the plugin.

## 3. Manual HTTP diagnostic mode

If debugging is needed:

```powershell
.\run_local_secure.ps1
```

It binds `http://127.0.0.1:9823/mcp`. The launcher is idempotent: if a healthy OLEANDER Baidu Storage instance already owns port 9823 it exits successfully; if another process owns the port it fails rather than killing that process.

## 4. Validation

Run:

```powershell
py -3.13 -m unittest discover -s tests -q
py -3.13 validate_candidate.py
py -3.13 build_packages.py
.\verify_local_runtime.ps1
```

The expected plugin package is `OLEANDER-Baidu-Storage-Plugin-0.1.1-CANDIDATE.zip`.

`verify_local_runtime.ps1` is the final workstation acceptance check. It verifies the installed/enabled Codex plugin, the resolved stdio MCP binding, the actual installed wrapper, provider connectivity, `/OLEANDER_VAULT`, and a real quota readback. It does not print the Baidu access token.

## Boundary

This is a storage adapter only. Plugin installation or storage success does not create Project State, Current Authority, Design KEEP or Promotion.
