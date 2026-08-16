# R06 Authority Resolution v1.3

## Decision
Use a layered authority model rather than flattening every prior file into one version.

### CURRENT geometry layer
`R06_V17_GEOMETRY.json` is later than v1.5 and is used for component geometry/currentized technical drawing where it explicitly provides geometry:
- locked envelope: 1200 × 160 × 975 mm
- timber cap: 1200 × 160 × 40
- cap tray: 1200 × 140 × 3
- face skin: 1080 × 3 × 260
- posts: RHS 60 × 40 × 4 at ±420 mm
- base plate: 220 × 180 × 12 mm
- gusset: 6 mm
- anchors: 4 × M16 / plate, 150 × 110 candidate layout, embedment OPEN
- D01 isolation 2 mm / drain gap 5 mm / concealed M6 @200–250 c/c candidate
- D04 grout 10–20 mm candidate

### Functional / safety / material rationale retained from v1.5
`R06_REALITY_CHECK_v1_5` remains authoritative for:
- interpretive / leaning node role
- NOT sole fall-protection guard
- 1.0 kN/m leaning benchmark as concept robustness screen only
- galvanized structural frame / dark copper coated skin / replaceable timber touch surface
- verified RC vs direct-rock branching
- FIELD verification list

### Superseded detail where conflicting
The v1.5 `240 × 160 × 12` RC base-plate candidate is not used in the current drawing because v1.7 later defines `220 × 180 × 12`.
This is a controlled supersession of one geometry detail, not deletion of v1.5 rationale.

### R7 / R7.1
R7/R7.1 files remain CURRENT support-technical roles by no-loss manifest. Their original pixels were not available in this runtime, so this package is a skill-driven reconstruction/currentization, **not a claim to reproduce original R7 artwork**.
