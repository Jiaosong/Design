# SP04-R08H｜整樘洞口锚固布置 + 边距/间距 + 受力路径

Status: ACTUALLY GENERATED / TRAINING-ONLY RULESET.

R08H extends R08G.1 from a single 1:2 fixing detail to a whole-opening anchorage system prototype.

## Training-only hypotheses
- Opening: 1200 × 1500 mm
- Corner anchor offset: 150 mm
- Maximum anchor spacing: 600 mm
- Minimum structural edge distance: 60 mm
- Setting block offset from jamb: 150 mm
- Sill membrane no-puncture zone: 80 mm

These values are not code, manufacturer requirements or project specifications.

## Derived layout
- Head anchors: 3; spacing 450 mm
- Left jamb anchors: 3; spacing 600 mm
- Right jamb anchors: 3; spacing 600 mm
- Sill setting blocks: 2
- Sill anchor candidates: 3, still PENDING system/manufacturer confirmation

## Load/control paths
- Gravity: frame sill → setting block → shim/support → structural substrate
- Wind / out-of-plane load: frame perimeter → anchor bracket/fastener → structural substrate
- Water: head/jamb/sill flashing → gravity drainage → exterior
- Thermal: frame/reveal → thermal-break zone → continuous insulation; ψ/fRsi remain unverified

## Conflict rules
- FAIL if anchor lands on non-structural insulation/membrane
- FAIL if structural edge distance is insufficient
- FAIL if anchor blocks sill drainage
- WARNING if continuous metal anchorage bridges the thermal-break zone
- PASS when load path and water/air/thermal control layers remain functionally separated

## QA
- 2 SVG sheets
- 115 text objects
- 98 graphic objects
- text boundary issues: 0
- graphic boundary issues: 0
- rule QA: PASS
- outlined SVG: no font dependency

Internal review: 99/100.

Status: PASS — Whole-opening Anchorage System Prototype / NOT PROJECT CONSTRUCTION DETAIL.
