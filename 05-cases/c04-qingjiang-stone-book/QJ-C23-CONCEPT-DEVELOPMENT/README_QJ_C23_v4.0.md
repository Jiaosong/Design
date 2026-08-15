# QJ-C23 Concept Development v4.0

Status: `CONCEPT DESIGN / FIELD OPEN / G1F HOLD / NO_PROMOTION`

C23 inherits C22 geometry logic and does not redraw the masterplan. It deepens F01/F02/F03, route-navigation estimates, capacity models, boundary/closure logic, risk strategy, material/weathering maintenance, constructability QA, and D/Web/F interfaces.

## Deliverables
- 12 editable SVG drawing sheets
- 12 PNG previews
- 12 individual PDFs + combined PDF
- machine JSON/CSV
- Web JSON Schema + CSS state tokens
- contact sheet
- SHA-256 manifest

## Critical distinction
- `SOURCE FACT`: official scenic/operator material.
- `DESIGN TEST RANGE`: route time, navigation interval, capacity scenario.
- `CONCEPT SIZING`: facility/base/detail initial sizes for design development.
- `FIELD OPEN`: any real site geometry, structural adequacy, compliance, safety, operation threshold.

## Route budget
Target = 182 min; test range = 138-230 min.
This intentionally brackets the official “about 3 h” visit statement and is not a measured segment schedule.

## System capacity
`C_system = min(C_cable, C_station, C_walk, C_node, C_return)`.
Official cable design capacity = 2700 p/h; trail/node capacity must never be inferred from the cable value.

## F01/F02/F03
All three retain C22 roles:
- F01 KEEP / NOT LOCATED
- F02 OPTIONAL / NOT LOCATED
- F03 CONDITIONAL
Permanent footing/connection details are concept options only.

## Construction stop
No drawing in this package may be released for construction until C23 HP-01...HP-08 hold points are closed by field/operations/professional receipts.
