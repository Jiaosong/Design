---
name: oleander-baidu-storage
description: Use OLEANDER's bounded Baidu Netdisk storage surface to browse, search, review and manage remote OLEANDER project/knowledge replicas without turning cloud storage into Project State or Current Authority.
---

# OLEANDER 百度网盘 v0.1 candidate

This Skill is an interaction binding for the `OLEANDER 百度网盘` MCP app. It does not contain a Baidu access token and cannot create storage connectivity by itself.

Read [storage.md](references/storage.md) before using storage tools.

## Default behavior

Use the app for remote storage operations under `/OLEANDER_VAULT` only.

Prefer read/search before mutation. For project work, resolve the actual owner-native Project State / Current artifact first; a cloud path or modification timestamp never decides Current.

Use storage classes as byte-copy roles only:

`CURRENT_COPY / MILESTONE / REVIEW / ARCHIVE / KNOWLEDGE_BODY / SHARED_ASSET`.

Never infer:

`UPLOAD SUCCESS = DESIGN KEEP`

`/CURRENT/ FOLDER = OLEANDER CURRENT AUTHORITY`

`REMOTE FILE = CURRENT PROJECT ARTIFACT`

For local DWG/SKP/BLEND upload, route to the local COS/stdio uploader. Remote ChatGPT must not claim it read an arbitrary local workstation file.

Deletion and share-link creation remain disabled unless the installed MCP server explicitly enables them. `/CURRENT/` storage mutation and overwrite require the adapter's explicit acknowledgement fields.
