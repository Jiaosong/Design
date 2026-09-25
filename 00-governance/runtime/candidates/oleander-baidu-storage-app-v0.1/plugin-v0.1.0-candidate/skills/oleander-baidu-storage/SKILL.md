---
name: oleander-baidu-storage
description: Use OLEANDER's bounded Baidu Netdisk storage surface to browse, search, review and manage remote OLEANDER project/knowledge replicas without turning cloud storage into Project State or Current Authority.
---

# OLEANDER 百度网盘 v0.1 candidate

This Skill is the workflow binding for the `OLEANDER 百度网盘` MCP app. It contains no Baidu access token and does not create storage connectivity by itself.

Read [storage.md](references/storage.md) before using storage tools.

## Default behavior

Use the app for remote storage operations under `/OLEANDER_VAULT` only.

Prefer read/search before mutation. For consequential project work, resolve the actual owner-native Project State and Current artifact identity first. A cloud path, filename or modification timestamp never decides Current.

Treat storage classes as byte-copy roles only:

`CURRENT_COPY / MILESTONE / REVIEW / ARCHIVE / KNOWLEDGE_BODY / SHARED_ASSET`.

Never infer:

`UPLOAD SUCCESS = DESIGN KEEP`

`/CURRENT/ FOLDER = OLEANDER CURRENT AUTHORITY`

`REMOTE FILE = CURRENT PROJECT ARTIFACT`

For local DWG/SKP/BLEND upload, route to the local COS/stdio uploader. Remote ChatGPT must not claim it read an arbitrary local workstation file.

Deletion is disabled by default. Share-link creation is unsupported in v0.1 until fsid ownership can be preflighted inside `/OLEANDER_VAULT`. `/CURRENT/` storage mutation and overwrite require the adapter's explicit acknowledgement fields.

## Typical workflow

1. Call the storage status/probe tool when connection state is unknown.
2. Resolve the project or Artifact ID from OLEANDER owner-native state when the request is project-current sensitive.
3. Search/list only under `/OLEANDER_VAULT`.
4. Prefer `REVIEW` carriers for remote human review and keep native masters `LOCAL_REQUIRED` where appropriate.
5. Before a write, state the exact storage target and whether it touches `CURRENT_COPY` or overwrite semantics.
6. After a write, read back provider metadata. Storage readback proves only the remote byte-copy state.

