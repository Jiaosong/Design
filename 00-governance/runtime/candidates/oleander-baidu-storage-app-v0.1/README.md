# @OLEANDER 百度网盘 v0.1.1 — Candidate

**Status:** `CANDIDATE / NOT CURRENT / NOT PROMOTED`

This candidate is the bounded local Baidu Netdisk storage adapter for OLEANDER. The selected runtime is local COS/Codex on the workstation; no cloud relay is required.

It does **not** own Project State, Current Authority, Artifact Registry, Design KEEP, professional verdicts, Promotion, KI/OE or Knowledge authority.

## Selected architecture

```text
COS / Codex local plugin
        ↓ stdio
OLEANDER Baidu Storage
        ↓ policy + path/operation guard
Baidu official MCP / API
        ↓
/OLEANDER_VAULT
```

The plugin uses `stdio` and starts its own local MCP process. It reads the Baidu access token from the current Windows user's DPAPI store. A separate localhost HTTP server is retained only for debugging/manual inspection.

## Storage root

All path-addressable operations are restricted to `/OLEANDER_VAULT`.

```text
/OLEANDER_VAULT
├─ PROJECTS/
├─ KNOWLEDGE/
├─ SHARED-ASSETS/
└─ ARCHIVE/
```

`CURRENT` in storage means remote byte-copy class only. It never grants OLEANDER Current Authority.

## Capabilities

Read/search: `file_list`, `file_doc_list`, `file_image_list`, `file_video_list`, `file_meta`, `file_keyword_search`, `file_semantics_search`, `user_info`, `get_quota`.

Bounded writes: `make_dir`, `file_copy`, `file_move`, `file_rename`, plus upstream URL/text upload tools allowed by policy.

Delete is disabled by default. Share-link creation remains unsupported in v0.1.1 until fsid ownership can be preflighted under `/OLEANDER_VAULT` before the side effect occurs. `/CURRENT/` mutation and overwrite require explicit adapter acknowledgements.

## Local install

See `INSTALL_LOCAL.md`.

Final workstation acceptance:

```powershell
.\verify_local_runtime.ps1
```

Expected final marker: `PASS_LOCAL_COS_CODEX_BAIDU_STORAGE`.

For manual HTTP debugging:

```powershell
.\run_local_secure.ps1
```

This binds only to `127.0.0.1:9823` and uses the DPAPI token store.

Storage success still does not prove Project State mutation, Design KEEP, professional PASS or Promotion.
