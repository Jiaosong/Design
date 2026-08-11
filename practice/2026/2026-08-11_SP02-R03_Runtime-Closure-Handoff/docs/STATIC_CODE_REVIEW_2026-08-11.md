# SP02-R03｜Static Code Review｜2026-08-11

Status after correction: **HANDOFF POST-REVIEW PASS / RUNTIME GATE OPEN**

## Issue found
Initial handoff used `ActiveCanvas.GetCanvasScreenBuffer()` with no argument.

Current McNeel Grasshopper API requires:
`GetCanvasScreenBuffer(GH_CanvasMode modeOverride)`.

That initial handoff revision is therefore **NEEDS REVISION / SUPERSEDED**.

## Correction
- import `Grasshopper.GUI.Canvas.GH_CanvasMode`
- call `GetCanvasScreenBuffer(GH_CanvasMode.Export)`
- rewrite capture script without `pathlib` so it remains compatible with Rhino 8 Python 3 and legacy IronPython-style `RunPythonScript` execution
- preserve `NO_ACTIVE_CANVAS` as an explicit CP4 OPEN condition; do not invent a canvas screenshot
- keep `adverse_case_canvas.png` as a distinct required human/GUI evidence artifact

## Verified API contracts
The current McNeel API documents:
- `GH_Document.NewSolution(Boolean, GH_SolutionMode)`
- `GH_DocumentIO(GH_Document)`
- `GH_DocumentIO.SaveQuiet(String)`
- `GH_Canvas.GetCanvasScreenBuffer(GH_CanvasMode)`
- `GH_CanvasMode.Export`
- `RhinoView.CaptureToBitmap(Size, Boolean, Boolean, Boolean)`

## Review outcome
AR-S04 for the handoff source: PASS after correction.
This does **not** close CP2 or CP4 because no real Rhino / Grasshopper runtime has executed.
