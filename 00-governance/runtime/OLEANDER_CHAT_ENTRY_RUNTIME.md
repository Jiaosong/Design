# OLEANDER Chat Runtime Entry

**Status:** ACTIVE NON-AUTHORITY RUNTIME ENTRY  
**Purpose:** Hot-updatable Chat → OLEANDER → local execution routing entry.  
**Authority ceiling:** `EXECUTION_ENTRY_AND_ROUTING_INSTRUCTIONS_ONLY`

This file is deliberately **not** Project State, Current Authority, a checkpoint database, an artifact registry, a professional-process owner, Design KEEP authority or Promotion authority.

## 1. Default interaction surface

The Human stays in **Chat by default**.

`CONVERSATION_SURFACE != EXECUTION_SURFACE != MUTATION_PERMISSION`

Do not ask the Human to switch to Codex/COS merely because work needs local files, Git, CAD, SketchUp, Blender, Python, or another workstation capability. Use the available COS/local execution connector behind the same Chat and return actual readback here.

## 2. Runtime resolver

Before consequential continuation/mutation or any completion/KEEP claim, use:

`00-governance/runtime/oleander_chat_runtime_bridge.py`

It consumes fresh owner-native authority/frontier/checkpoint/constraint/flow evidence through the existing resolver. Its result is transient execution guidance and never becomes Project State.

Generic continuation resumes the verified next action. Stale/ambiguous authority, source or checkpoint evidence revalidates/HOLDs. CLOSED does not reopen by chat recency.

## 3. Local capability routing

### BAIDU_STORAGE

Selected local route:

`Chat → COS local execution → codesign_chat_cos_bridge_v0_1.py → oleander-baidu-storage@oleander-personal 0.1.1 → MCP stdio → Baidu → /OLEANDER_VAULT → readback → Chat`

Bridge:

`00-governance/runtime/candidates/human-ai-codesign-vnext/codesign_chat_cos_bridge_v0_1.py`

Common read mappings:

- storage status / health → `oleander_storage_probe`
- quota → `baidu_get_quota`
- browse/list → `baidu_file_list`
- keyword search → `baidu_file_keyword_search`
- semantic search → `baidu_file_semantics_search`
- metadata → `baidu_file_meta`

Ordinary storage work does **not** require explicit `@OLEANDER 百度网盘` invocation.

Reads may execute when the local adapter is ready. Writes must pass the existing owner-native mutation/authorization guard and require follow-up provider/native readback before completion may be claimed.

If the workstation/local route is unavailable, use the existing continuity `execution-intent` carrier and report `PENDING_LOCAL_EXECUTION`. Do not invent a second queue or state store.

## 4. Hard separations

- `EXECUTION ROUTE != AUTHORITY`
- `EXECUTION INTENT != MUTATION PERMISSION`
- `TOOL SUCCESS != ACTUAL READBACK`
- `TOOL SUCCESS != PROJECT STATE MUTATION`
- `TOOL SUCCESS != DESIGN KEEP`
- `TOOL SUCCESS != PROFESSIONAL PASS`
- `TOOL SUCCESS != PROMOTION`

## 5. Hot-update rule

The CoS configuration contains only a stable bootstrap instruction pointing to **this file**. Future OLEANDER routing/runtime updates should modify this file and/or the referenced runtime implementation, validate them, and read them on the next OLEANDER turn.

**Do not rewrite the CoS config or require a CoS restart for ordinary OLEANDER runtime updates.**

Only a change to the bootstrap mechanism itself requires rebinding/restarting CoS.

CoS itself has an independent application lifecycle and may update without OLEANDER owning, pinning, freezing or downgrading it. After a material CoS update, use `00-governance/runtime/validate_cos_update_compatibility.py`. Compatibility drift HOLDs only the affected OLEANDER integration; it must not block the CoS updater. The compatibility probe is non-authority readback and does not grant mutation, Project State, Current, Design KEEP, professional PASS or Promotion.
