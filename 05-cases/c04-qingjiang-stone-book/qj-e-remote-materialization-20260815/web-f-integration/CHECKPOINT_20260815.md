# C04｜QJ-E Digital Prototype Checkpoint｜2026-08-15

**State:** `E DIGITAL PROTOTYPE COMPLETE / NO REDO / WEB+F INTEGRATION ONLY`  
**Boundary:** `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`

## Direct reuse
- `QJE-WEB-P01` → `C04_QJE_PORTABLE_SCROLL_v0.1.html`; reusable selectors: `#map / #reading / #state / #charts / #screens`.
- `QJE-WEB-P02` → `C04_QJE_PORTABLE_PROTOTYPE_v0.1.html`; states: Today / Route / Book / Service / Reveal / Silence.
- Runtime JSON → `c04-runtime-data.json`: M0–M7, 8+5 Reading, state axes, sources/limits.
- Video → `C04_QJE_Interaction-Demo_72s_v0.1.mp4`: 72.000s / 1920×1080 / 30fps.
- Frames → `S01…S12`; stable integration IDs `QJE-VID-S01…QJE-VID-S12`.
- PDF → `C04_QJE_Remote-Research-Display_v0.1.pdf`: 8 pages; stable IDs `QJE-PDF-01…QJE-PDF-08`.

## Main vs Appendix
**MAIN REQUIRED:** M0–M7 relation map; 8+5 Reading; Reality×Delivery state simulation; Digital Silence/withdraw; offline prototype; 72s video.  
**MAIN OPTIONAL:** authority-derived charts; they are source-state/count proof, not field measurements.  
**APPENDIX:** 8-page PDF; secondary static frames; authority snapshot; shotlist; decision/limits; QA/provider receipts.

## Reality State × Delivery Modifier
- Reality: `NORMAL / DEGRADED / CLOSED / UNKNOWN`.
- Delivery: `NONE / OFFLINE / RETURN-PRIORITY`.
- Derived optional depth: `FULL / LIGHT / OFF`.
- `UNKNOWN` fail-closed; `OFFLINE != DEGRADED`; `CLOSED` requires bypass/reroute/exit; `RETURN-PRIORITY` closes explanation/memory/share before route/safety/return.

## 8+5 Reading network
Core: `R01 / R05 / R06 / R13 / R02 / R07 / R09 / R12`.  
Companion: geology evidence / ecology-season / route reread / multi-voice narrative / My Stone Book.  
This is a reading network, **not** a 13-stop physical sequence. Main emphasis: `R01/R05/R06/R13`; other core pages are secondary depth.

## Exact bytes / SHA
- Original E delivery ZIP: `4,199,996` bytes — `8cf85b34cfb968e6302969daacd18849503792f8f809949d263f45ac86756f64`.
- Portable Scroll: `37,042` bytes — `e73f3651bbd9bf5a1ac20646c9f7c8be632d80cea551f8a70d60f04d338141f8`.
- Portable Prototype: `27,049` bytes — `d11a30339edf3d1557032c6b2f66b43c151ac3f6c58afcf226add03aff17f5d6`.
- Runtime JSON: `9,863` bytes — `0d208765d195d874dc1eb1168020334db8a7fea984743b70ec06f6aaee3615c6`.
- MP4: `835,519` bytes — `1612f4a34f2458f91361ea4ae10832376893d5d57fd6643d7871a1a6f8eb5c2c`.
- PDF: `504,325` bytes — `c1f649407e7497aa170dbad82479ec895e38068414497c2de884c174a50bda46`.
- Web/F integration ZIP: `1,952,539` bytes — `85605c03f2ede787b5a89ea1d4aca7db48db11ea18324f493fd4b807e2a6bd30`; Drive ID `1A1uveOVgGnnlY_28JrqhTnFLfsSBeI-M`.

## Known browser policy limit
`BROWSER_VISUAL_OPEN_POLICY_BLOCKED`: execution-container Chromium organization policy blocks `file://`, `data:` and private-local navigation. Source/runtime validation remains `31/31 PASS`, HTTP `6/6 200`, PDF render review PASS, MP4 decoded-frame review PASS. Do not relabel the policy-blocked browser visual gate as Browser PASS.

## Freeze
After this checkpoint, E changes **only** for a reproducible Web/F integration blocker. Do not redesign E, add features, fix a physical route order, invent field metrics/GPS/live service/safety, or promote the project.