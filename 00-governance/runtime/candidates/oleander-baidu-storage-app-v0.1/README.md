# @OLEANDER 百度网盘 v0.1 — Candidate

**Status:** `CANDIDATE / NOT CURRENT / NOT PROMOTED`

This package turns the official Baidu Netdisk MCP server into a bounded OLEANDER storage surface for ChatGPT and COS.

It deliberately does **not** create or own Project State, Current Authority, Project Registry, Artifact Registry, Design KEEP, professional verdicts, Promotion, KI/OE or Knowledge authority.

## Architecture

```text
ChatGPT custom app / COS
        ↓
OLEANDER Baidu Storage MCP
        ↓  policy + path/operation guard
Baidu Netdisk official MCP
        ↓
User's Baidu Netdisk
```

The upstream implementation is the official `baidu-netdisk/mcp` server. This package proxies its tools rather than reimplementing the Baidu storage API.

## Default storage root

All path-addressable operations are restricted to:

`/OLEANDER_VAULT`

Recommended layout:

```text
/OLEANDER_VAULT
├─ PROJECTS/
├─ KNOWLEDGE/
├─ SHARED-ASSETS/
└─ ARCHIVE/
```

`CURRENT` inside that storage layout means **remote byte-copy class only**. It never becomes OLEANDER Current Authority.

## Exposed upstream capabilities

Read/search by default:

- `file_list`
- `file_doc_list`
- `file_image_list`
- `file_video_list`
- `file_meta`
- `file_keyword_search`
- `file_semantics_search`
- `user_info`
- `get_quota`

Bounded write operations by default:

- `make_dir`
- `file_copy`
- `file_move`
- `file_rename`
- URL/text upload tools reported by the upstream server

High-risk operations are disabled unless explicitly enabled by environment policy:

- delete
- share-link creation

Writes into a `/CURRENT/` storage branch or overwrite behavior require explicit OLEANDER acknowledgements in the tool input.

## ChatGPT vs local COS

ChatGPT uses the remote Baidu MCP path through this Streamable HTTP app. The official Baidu server does not expose local-file upload through SSE, so arbitrary local DWG/SKP/BLEND upload remains a COS/local-stdio responsibility.

## Run locally

```powershell
cd 00-governance/runtime/candidates/oleander-baidu-storage-app-v0.1
py -3.13 -m pip install -r requirements.txt
$env:BAIDU_NETDISK_ACCESS_TOKEN="<token>"
py -3.13 -m app.server
```

MCP endpoint:

`http://127.0.0.1:8000/mcp`

Health endpoint:

`http://127.0.0.1:8000/healthz`

See `INSTALL_CHATGPT.md`, `OPENAI_TUNNEL.md` and `COS_LOCAL_UPLOAD.md`.

For a no-chat/no-Git local token setup on Windows, run `configure_baidu_token.ps1` and then `run_local_secure.ps1`. The token is stored through Windows DPAPI under the current user's LocalAppData, not in this repository.
