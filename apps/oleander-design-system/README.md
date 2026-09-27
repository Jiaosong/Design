# OLEANDER Design System Product Shell

This is the first host-agnostic product shell for the OLEANDER Design System successor architecture.

It is intentionally **not** a second Project State, Knowledge Registry, Git authority, or execution runtime. The shell renders and stages user actions; owner-native state and execution must be supplied through the OLEANDER gateway / Host Runtime contracts.

## Current scope

- nine-area navigation: Home / Projects / Design / Knowledge / Sources / Browser / Integrations / Review / System;
- project workspace shell with Project / Git / Workspace separation visible in UI;
- Source Inbox drag/drop with chunked local-host upload, server-side SHA-256, original preservation and truthful ingestion state;
- structured-body extraction for text/Markdown/JSON/CSV, OOXML DOCX/PPTX/XLSX, plus PDF text extraction through available `pypdf` or `pdfplumber` providers;
- video/audio binaries are preserved as Sources; when FFprobe/FFmpeg are available the host extracts media metadata and real source keyframes, but leaves transcription explicitly `TRANSCRIPT_PROVIDER_NOT_BOUND`. Source-owned transcription requests may be persisted and read back without claiming that a provider or transcript exists;
- Surface Reliability R1-R5 visualization without a misleading single `Connected` status;
- integration surfaces remain visible when unavailable;
- Host Runtime probes report the Design System local host, DSH binary availability and COS_NATIVE machine-local snapshot freshness separately; stale CoS evidence never becomes current readiness;
- browser and native design surfaces are placeholders until a Host Runtime binds them;
- command palette for product actions; no provider mutation is issued directly from the UI.

## Run locally

From repository root, start the Design System Local Host:

```powershell
python apps/oleander-design-system/host.py --port 4173
```

Then open `http://localhost:4173`.

The host stores Sources outside the repository by default under `%LOCALAPPDATA%\OLEANDER\DesignSystem`. Override with `OLEANDER_DESIGN_SYSTEM_DATA_ROOT` or `--data-root`.

Static-only fallback is still possible with `python -m http.server 4173 -d apps/oleander-design-system`; in that mode the UI explicitly stays `Host Runtime 未绑定` and Source files are only browser-local staged objects.

## Boundary

```text
Product Shell
→ Product Action
→ OLEANDER ActionRuntime
→ Surface Reliability Boundary
→ Host Runtime / Surface Adapter
→ actual readback
```

The current local host implements project discovery, Source Inbox transport/preservation/basic structured-body extraction and current capability-view readback. Persistent Source transcription-request creation is the first bounded local Product Action that runs through action-scoped R1-R4 preflight → `ActionRuntime` → actual readback → R5 result verification. It persists only the request/receipt while the provider remains unbound. Native design mutations and controls that need DSH/COS_NATIVE/CAD/connector execution remain explicitly unbound.
