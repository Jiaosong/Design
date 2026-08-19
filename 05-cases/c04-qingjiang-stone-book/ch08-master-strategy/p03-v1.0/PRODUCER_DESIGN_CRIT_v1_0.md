# CH08-P03 v1.0｜Producer Design Crit

Role: `PRODUCER-SIDE FINISHED-PIXEL CRIT / NOT INDEPENDENT PROFESSIONAL DESIGN VERDICT`.

## First-read contract
P03 must read as:
`BEHAVIOR CONDITION → CONTENT ADMISSION → STOP ≠ READ → DESIGN RESPONSE`.

It must not read as:
- a dwell-time trigger model;
- a behavior surveillance dashboard;
- a fatigue scoring UI;
- six equal content cards;
- a route or task flow.

## R0 actual-pixel failure
At 1920×1080 the authored H1 contained one semantic break after `不是每次停下，`, but the left column was too narrow and the font too large. The rendered title became four accidental fragments:

`不是每次停 / 下，/ 都要变成内 / 容。`

This failed the first visual gate despite the behavior-condition field itself rendering correctly.

## R1 repair
- hero left column widened to `minmax(600px,.84fr)`;
- right condition field kept at `minmax(700px,1.16fr)`;
- desktop H1 cap reduced to `72px`.

R1 first read:
`不是每次停下， / 都要变成内容。`

## R1 objective readback
1920×1080:
- scrollWidth 1920;
- horizontal overflow 0;
- scrollHeight 3414;
- one PAGE article / one H1;
- 0 console/page errors.

390×844:
- scrollWidth 390;
- horizontal overflow 0;
- scrollHeight 5267;
- one PAGE article / one H1;
- 0 console/page errors.

## Design finding after repair
- first screen now contains one large behavioral proposition and one structured condition field;
- six conditions are expressed as lanes, not a card wall;
- OBSERVE is visually the only lane with strong content-admission eligibility;
- RECOVER / CHOOSE / PASS visibly suppress optional content and return authority to body, service or route;
- `STOP ≠ READ` receives its own second-screen visual proposition rather than being buried in a note;
- no pseudo-measured thresholds, scores or probabilities were introduced.

## Producer disposition
`PRODUCER CANDIDATE / R0 FIRST-VISUAL DEFECT REPAIRED / NO SELF-KEEP`.

This does not constitute independent Professional Design PASS, MAIN KEEP, behavior validation, field validation, live-browser navigation PASS or implementation approval.

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
