# 2026-08-29｜Design Process / Spatial / L5｜Maintainability → Spatial Access Architecture

STATUS: `TRAINING_MODE / CROSS_CONTEXT_EVIDENCE (STRENGTHENED) / SUPPORT / SCOPED / UNVERIFIED / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
Recent DESIGN Practice covered repairability→product disassembly architecture, situated orientation media, and program→massing. This run attacks a materially different scale: whether maintenance intent changes equipment-room adjacency, service faces and removal circulation, or remains a hatch/label added after equipment placement.

## KNOWLEDGE READ STATE
Current authority read first: Notion root Current Authority; `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.0`; GitHub main Registry / REVIEW / Work Coordination / Priority Queue / Human Professional Voice; current `oleander-design-process/SKILL.md`; current `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md`.

Priority Queue currently contains `PRJ-C04-DIGITAL-INTERACTION`, owned by `PRESENTATION`; DESIGN therefore remains in TRAINING_MODE and does not mutate C04 production. No K06 / chronology / Legacy / Snapshot object is used as current authority. Repository search did not resolve files literally named `Current Owner Map` or `Capability Contract`; Registry/REVIEW execution-owner authority is retained without inventing missing content.

## EXTERNAL DISCOVERY
### Source A
Whole Building Design Guide / NIH Design Requirements Manual Rev. 2.1 (8/2/2024)
https://www.wbdg.org/FFC/NIH/nih_design_requirements_rev_2.1_2024.pdf
Accessed 2026-08-29. Official WBDG index text states that defined access/service zones should be provided for equipment and clear/safe access should support servicing, removing and replacing equipment.

### Source B
WBDG — Reliability-Centered Maintenance (RCM)
https://stg.wbdg.org/resources/reliability-centered-maintenance-rcm
Accessed 2026-08-29. Material delta: maintenance can only preserve reliability inherent in design; maintenance feedback can improve original design.

### Source C
WBDG — Research Laboratory
https://legacy.wbdg.org/building-types/research-facilities/research-laboratory
Accessed 2026-08-29. Material delta: building systems can be organized/exposed/centralized to support maintenance access.

Rights boundary: factual professional references only, independently paraphrased. No source diagram, plan, template, visual identity, copyrighted wording or fixed technical dimension is copied.

## CAPABILITY MAPPING / MATERIAL DELTA
Existing OLEANDER already covers >60%: requirement→design consequence, spatial organization/circulation, serviceability/lifecycle review, target-part trace, deletion/adverse tests. New bounded delta is cross-scale: product serviceability must add `service face + removal route + unaffected-neighbor check` when transferred to space. Decision: EXTEND/COMPOSE existing design-process evidence; no parallel Skill or Current Rule.

Rejected: fixed equipment clearances, aisle/door dimensions, lifting-device requirements, shutdown rules, NIH/lab-specific mandatory procedures, code/safety/accessibility/engineering approval, or a universal requirement to expose equipment.

## DESIGN QUESTION / E-I-A-D
Synthetic object: mechanical equipment room, NTS.

Question: can target unit E2 receive routine service and full replacement without disturbing unrelated equipment or routing the task through an unrelated/public path?

EVIDENCE: official facility guidance treats servicing/removal/replacement access as design concerns.
INFERENCE: a room that merely fits equipment may still be unmaintainable if maintenance depends on unrelated equipment/circulation.
ADVERSE: E2 replacement while neighbors remain operating; routine service and full replacement are different tasks.
DESIGN CONSEQUENCE: reserve service face and removal spine before compaction; keep replacement out of unrelated operational paths.

## ARTIFACT / OPTIONS
Editable: `OLEANDER_MAINTAINABILITY_SPATIAL_ACCESS_R01.svg`.

- A / REJECT — Fit-first Equipment Room: footprints compacted first; E2 removal snakes through unrelated aisles.
- B / KEEP candidate — Service Face + Removal Spine: routine access and full-unit removal own an explicit maintenance path to a service door; neighboring service faces remain available.
- C / REVISE — Access Hatch Only: routine hatches exist, but full replacement still exits through a public corridor. `access panel ≠ maintainable spatial architecture`.

## A/B / ATTACK
1. `TARGET-UNIT TRACE` — trace spaces/routes disturbed by E2 routine service and full replacement.
2. `NEIGHBOR-ON` — neighboring units remain operating.
3. `DOOR / TURN TEST` — replacement owns a path to an exit; exact geometry remains VALIDATION.
4. `HATCH-OFF` — C loses routine access.
5. `HATCH-ON` — C still fails replacement routing.
6. `E2 DELETE / REPLACE` — B preserves neighboring service/operating zones.
7. `GRAY50` — route ownership must survive without hue.

## READBACK / FAILURE / REPAIR / RETEST
First full-size readback found two representation defects: C's replacement-route stroke crossed the `PUBLIC CORRIDOR` label; B's removal-spine label sat directly on the heavy route stroke.

Root cause: `correct relation ≠ readable relation`; path evidence loses authority when its labels compete with the same visual channel.

Repair: moved C's corridor label above the route and moved B's removal-spine label off the stroke; regenerated full-size and Gray50 and reopened the final PNG.

Retest: A/B/C remain materially distinct; B's service face and removal spine read separately; C still demonstrates routine-access/full-replacement mismatch; no technical dimensions were introduced.

## TRANSFER RULE
`TARGET SERVICE OBJECT → SERVICE TASK → REQUIRED ACCESS FACE → DISASSEMBLY / REMOVAL DEPENDENCIES → REPLACEMENT ROUTE → UNAFFECTED-NEIGHBOR CHECK`

The product-scale chain `target part → access → dependencies → reassembly` survives at spatial scale only after adding route/adjacency ownership. A hatch, access panel or generic “maintenance clearance” label is not by itself evidence that full replacement is spatially resolved.

Boundary: applicable to equipment rooms, plant/service spaces, lab support zones and replacement-route planning before technical dimensioning. Not sufficient for manufacturer clearances, equipment weights, rigging/lifting, structure, code/egress, accessibility, safety, shutdown sequencing or construction approval.

## KNOWLEDGE WRITE HANDOFF
Write state: `CROSS_CONTEXT_EVIDENCE / SUPPORT / SCOPED / UNVERIFIED`.

Suggested Existing Owner: `oleander-design-process`, related to `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md`.

Relations for KNOWLEDGE closure: Source=WBDG/NIH DRM Rev.2.1 + WBDG RCM + WBDG Research Laboratory; Domain=design process/spatial planning/maintainability; Method=`oleander-design-process`; Evidence=editable SVG + PNG/Gray50 readback + repair; Freshness=checked 2026-08-29; Trust=UNVERIFIED; Project relation=none; Transfer relation=product repairability Practice → spatial maintainability Practice.

Do not migrate directly to Current Rule. KNOWLEDGE owns Migration Closure / Relation Closure.

## STATUS
`CROSS_CONTEXT_EVIDENCE (STRENGTHENED) / EXTERNAL-SOURCE-CALIBRATED / UNVERIFIED`

No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE`, or `ACTIVE`.
