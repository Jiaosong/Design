# C04｜Qingjiang Thirteen Imprints App / Game Map v1.3

Status: `SINGLE-PROJECT DIGITAL DEEPENING / MAIN CANDIDATE / FIELD OPEN / NO_PROMOTION`

Base: current `main@9dd784dd903fcfd2af42d75ec4bc77c5772025fd` + merged App/Game Map v1.2 + canonical R01–R13 + merged R05/R06 scene systems + global `NO COMPRESSION / NO LOSS` governance.

This revision does **not** change the C04 12-layer Web architecture and does not add a fifth primary App tab. Existing primary IA remains:

`TODAY / ROUTE / READ / MY BOOK` with persistent `SERVICE / RETURN`.

## Material delta from v1.2

### 1. Digital Presence is now behavior, not only copy
- sticky context chip shows `FULL / LIGHT / OFF`;
- default rhythm: TODAY FULL, ROUTE FULL, READ LIGHT, MY BOOK LIGHT, SERVICE FULL;
- pressing the chip enters `DIGITAL SILENCE`, a real interaction state that removes content/task pressure and tells the visitor to look/move/rest/return without the phone;
- scene dialogs override digital presence contextually.

### 2. R05 / R06 / R13 consume merged scene logic
- R05: `SEE → DO(optional) → FEEDBACK(light) → EXIT`, digital LIGHT;
- R06: `LANDSCAPE FIRST → RECOVER → OPTIONAL REVEAL → CONTINUE/RETURN`, digital `OFF → SHORT → OFF`;
- R13: `PLAY OFF`, digital OFF, Body / Safety / Return first;
- R01 remains moving-view observation, no forced UI.

### 3. Reality state is now fail-closed behavior
ROUTE includes explicit **demo-only** state switching:
- NORMAL
- DEGRADED
- CLOSED
- UNKNOWN

CLOSED / UNKNOWN automatically shift the map emphasis to Return and visually de-emphasize walking routes. This is a prototype state machine only and does not claim live operations.

### 4. Return now closes into Recognition before Memory
MY BOOK adds:
`RETURN → RECOGNITION → RECORD`

Visitors can record what they recognized again on the return journey (river/banks, cable direction, peak/scene). This avoids reducing Memory to a completion badge or souvenir inventory.

### 5. No-phone continuity is explicit and usable
`DIGITAL SILENCE` exposes the minimum-complete non-phone journey:
`LOOK → MOVE → REST → RETURN`

Paper map / physical direction / human service remain the fallback carriers. App remains optional depth, never route authority.

## No-loss check
Preserved from v1.2:
- TODAY / ROUTE / READ / MY BOOK;
- Service / Return permanent access;
- BOAT / CABLE / WALK;
- full R01–R13 optional content library;
- audience-depth filters;
- culture / observation / play / body-rest filters;
- local-device My Book writing;
- print fallback;
- no login / no GPS / no cloud dependency;
- UNKNOWN fail-closed;
- FULL / LIGHT / OFF;
- editable HTML/SVG formal UI.

No established App capability was removed for brevity.

## Truth boundary
- relationship map / NTS; not measured geometry;
- no real-time operation or availability claim;
- NORMAL in the selector is a **demo state**, not a live status;
- CLOSED / UNKNOWN do not render as normal access;
- route / safety / Return never depend on Imprint completion;
- R13 PLAY OFF;
- FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NOT FOR CONSTRUCTION.

## Current design judgment
`KEEP_AFTER_REVISION / MAIN CANDIDATE`

Strongest delta: digital retreat and Return priority are now observable interaction behavior rather than policy text.

Remaining design gap: finished mobile/desktop browser readback is still required before any Design PASS / MAIN KEEP claim. This branch has source-level implementation only; no PR/merge/promotion is created by this deepening step.