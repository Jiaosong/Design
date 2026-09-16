# EV-PROF-ACOUSTICS-20260916 — Independent Review Packet v001

**Domain:** Building Acoustics / Acoustic Design  
**Controlled Evolution state:** `EV3_EVAL_PASSED / NOT REVIEWED`  
**Exact review input commit:** `23fa652eb3d6f0f4bcb0c433ecb6cc1d97f9a3a8`  
**Authority baseline:** `main@76dbd8d16d09b2d5e57401453e39967b5aa36202`  
**PR:** #644  

> This file is a review packet, not a review verdict. `PRODUCER SELF-CHECK ≠ INDEPENDENT REVIEW`.

## 1｜Immutable reviewed bundle

| Artifact | Blob SHA |
|---|---|
| Professional body `00-governance/building-acoustics-design-process-v1.0.md` | `5bbe1e39c3cfed2ec7cbca49684e926244d0751a` |
| Machine definition `00-governance/schemas/building-acoustics-design-process.v1.json` | `93661f3dccf3eb3e61acca3da9e2fb8fee4fbeed` |
| Candidate workflow binding `.github/workflows/ai-governance-evals.yml` | `e30e2b7a2acf1e376867b610259386b3975ba30c` |
| Historical EV2 receipt `EV-PROF-ACOUSTICS-20260916.json` | `5e26677c9e81cac0d7955d7b2c4f4c4b37676288` |
| EV3 machine-evaluation receipt | `ea623e2691621c6a56aed05fea250394d7e35d6b` |

The exact review input `23fa652e…` has fresh SUCCESS on:

- AI Governance Evals run `4816` / id `35039065875`;
- OLEANDER Project Anti-Pollution Gate run `747` / id `35039065901`;
- OLEANDER Blender Runtime Contract run `576` / id `35039065944`.

The predecessor EV2 input `dc553218…` also passed runs `4815 / 746 / 575` and is retained as historical machine-evaluation provenance.

## 2｜Reviewer eligibility — UNSET

The eventual reviewer must explicitly establish:

- **Reviewer identity:** `NOT RUN`
- **Relevant Building Acoustics competence:** `NOT RUN`
- **Authority to perform this Controlled Evolution review:** `NOT RUN`
- **Independence from candidate production sufficient for the adopted review contract:** `NOT RUN`
- **Conflict / limitation declaration:** `NOT RUN`

No producer, workflow, CI check, model, Notion sync or packet author may fill these fields by inference.

## 3｜Required professional attack surface

The reviewer must fresh-read the exact immutable bundle and test at least the following.

### A. Domain authenticity and process semantics

1. Do `ACO-BASIS → ACO-ROOM → ACO-SEPARATION → ACO-NOISEVIB → ACO-DETAIL → ACO-TEST → ACO-DELIVERY → ACO-INUSE` behave as coherent Building Acoustics carriers rather than disguised Architecture `ADD-*` aliases?
2. Does the process preserve real acoustic-design distinctions among task/criteria, room acoustics, separation/flanking, services noise/vibration, details, verification, construction and in-use diagnosis?
3. Does it avoid presenting one universal project sequence, consultant appointment or numerical target set as mandatory for all building types?

### B. Use / task / source-receiver / criteria basis

4. Is each acoustic claim tied to an actual use/task, source, receiver, room/operating state and applicable metric/method rather than a generic `RT`, `Rw`, `DnT,w`, `LnT,w`, `NR/NC`, dBA or absorption target?
5. Are code/minimum requirements, client aspirations, specialist design criteria and verification acceptance criteria distinguished?
6. Are source spectrum/time behavior, receiver sensitivity, occupancy/operating state and relevant uncertainty/open assumptions preserved where consequential?
7. Can a convenient generic value be silently promoted to a project target without source/applicability evidence? It must not.

### C. Room acoustics

8. Does `ACO-ROOM` treat room volume/geometry, source/receiver positions, frequency dependence, surface distribution and occupied/furnished state as material where relevant?
9. Are reverberation/decay metrics prevented from becoming a proxy for every speech, privacy, music, spatial-variation or background-noise requirement?
10. Is a material absorption coefficient/NRC/αw treated only as an input, not proof of the room result?
11. Are large openings, operable partitions and multiple operating states capable of reopening the room-acoustic claim?
12. Are acoustic prediction/model outputs kept separate from measured room performance?

### D. Airborne / impact isolation and flanking

13. Does `ACO-SEPARATION` explicitly distinguish direct transmission from flanking transmission?
14. Are laboratory element/system ratings prevented from being read as project field isolation without justified configuration transfer?
15. Do door/frame/seal/threshold, glazing, façade mullion, floor/ceiling, structural junction, back-to-back service and penetration paths remain visible?
16. Where impact sound is in scope, are source/floor/ceiling system conditions represented rather than inferred from one material layer?
17. Can a partition rating alone be interpreted as room-to-room privacy or occupied confidentiality? It must not.

### E. Building-services noise and vibration

18. Does `ACO-NOISEVIB` preserve actual equipment operating state and source evidence rather than using generic catalogue values indiscriminately?
19. Are airborne, duct-borne, breakout, regenerated and structure-borne paths distinguished where relevant?
20. Are plant-room construction, bases/inertia, isolators, flexible connections, ducts, pipes, terminals and penetrations coordinated as interfaces rather than being self-approved by Acoustics?
21. Are part-load/full-load/standby/emergency and intermittent/tonal/low-frequency conditions handled when material?
22. Do MEP and Structural Engineering retain their own professional authority?

### F. FLS / façade / architecture / interior interfaces

23. Can acoustic seals, linings, resilient systems or modified partitions invalidate fire-rated/FLS assemblies without reopening the FLS interface? They must not.
24. Are façade external-noise/glazing/junction assumptions routed to the Facade/Envelope owner where appropriate?
25. Are Architecture/Interior geometry, materials and visual intent treated as coordinated inputs rather than acoustic authority?
26. Does R-F remain sole owner of interface maturity/disposition/coupling/criticality?

### G. Critical detail and constructability

27. Do representative project details cover junctions, doors, ceilings, floors, glazing, operable partitions, penetrations, access panels, resilient layers and vibration paths where consequential?
28. Are gaps, seals, workmanship, tolerance and construction sequence treated as potential acoustic failure mechanisms?
29. Can a generic manufacturer detail or isolated product certificate substitute for the actual project acoustic path where configuration differs? It must not.
30. Are concealed acoustic conditions inspectable/readable before closure where the claim depends on them?

### H. Model / laboratory / field measurement boundaries

31. Does `ACO-TEST` preserve the distinction among prediction/model, laboratory evidence, mock-up/sample evidence, field measurement and occupied/in-use outcome?
32. Are method/edition, instruments/calibration where required, source/receiver positions, room/equipment state, occupancy/furnishing condition, frequency treatment, corrections/averaging and uncertainty/limitations recorded as applicable?
33. Can ISO 3382-2, ISO 16283-1 or ISO 717-1 be misused outside their actual method/rating role or as universal project targets? They must not.
34. Are failed measurements, repairs and retests retained rather than overwritten by a later PASS?
35. Is one room/sample prevented from proving unmeasured rooms or the whole building?

### I. Construction QA / delivery

36. Does `ACO-DELIVERY` distinguish submittal review, concealed-work inspection, field measurement, defect repair and retest?
37. Are late penetrations, boxes, access panels, service rerouting, ceiling interruptions and substitutions explicit reopen events?
38. Are resilient layers/isolation systems and perimeter seals vulnerable to workmanship bridging/gaps in the process logic?
39. Are unobserved/unmeasured areas prevented from inheriting sampled PASS status?

### J. In-use observation / diagnosis / causation

40. Does `ACO-INUSE` separate complaint/symptom, measured condition, operating state, candidate cause, diagnostic intervention, repair and post-intervention verification?
41. Can one complaint or one abnormal/normal measurement be treated as confirmed causation without diagnostic evidence? It must not.
42. Do use, furniture, partition, finish, MEP, operating-hours and other material changes reopen affected acoustic assumptions?
43. Can one project's success/failure become a reusable universal rule without the existing R-K/G9 transfer/counterevidence route? It must not.

### K. Knowledge / evidence / authority firewalls

44. Does the candidate consume only the Acoustics route of `IDX-ARCH-SPECIALTY-008` while preserving Smart Building, Corrosion/Durability and Roof/Ancillary as separate tracks?
45. Does the L4 `INDEX` remain Knowledge routing rather than becoming Professional Process authority?
46. Are Knowledge/Evidence/KI/OE states separate from acoustic professional-process state?
47. Are `ACOUSTIC PROCESS PASS`, R-F Integration PASS, Architecture Design KEEP, MEP/Structural/FLS PASS, statutory approval, whole-building field truth and Promotion kept separate?

### L. Native/editable asset and AI boundary

48. Does the process require native/editable plans/details/models/registers/calculations and actual measurement records where those are the professional source of truth?
49. Can generative imagery or AI-generated acoustic diagrams substitute for measured/model/project evidence? They must not.
50. Are simulation/measurement-processing outputs tied to method/version/input/configuration and claim ceiling?

### M. Change propagation / stale truth

51. Do use/task, geometry, adjacency, assembly, penetration, MEP source/routing, structural support, product/substitution, workmanship, method and in-use changes reopen affected scope?
52. Does stale propagation preserve valid unrelated predecessor evidence rather than erase all history?
53. Are EV2/EV3 receipts historical and immutable after later changes?

## 4｜Source / freshness checks required of reviewer

The reviewer must independently confirm source applicability/freshness before relying on it. At packet creation, producer evidence recorded:

- `ISO 3382-2:2008` as current confirmed method context for reverberation-time measurement in ordinary rooms where applicable;
- `ISO 16283-1:2014` plus applicable amendment as current confirmed field airborne-sound-insulation measurement context where applicable;
- `ISO 717-1:2020` as current confirmed airborne sound-insulation rating context;
- Institute of Acoustics Building Acoustics Group as current professional context spanning room acoustics, sound insulation, HVAC acoustics and vibration isolation.

These references do not replace project jurisdiction, brief, exact source/receiver/configuration/operating state, specialist appointment or responsible professional/statutory authority.

## 5｜Required reviewer output

The reviewer must return one evidence-bound outcome against the **exact input `23fa652e…`**:

- `PASS_EV4_ALLOWED` only if the Controlled Evolution review contract is actually satisfied; or
- `HOLD / REVISE` with concrete material defects and affected scope.

The reviewer must not issue:

- project acoustic approval or field acceptance;
- Architecture Design KEEP;
- MEP / Structural / FLS / R-F PASS;
- statutory approval;
- whole-building or occupied-building acceptance;
- EV5 or Promotion.

## 6｜Verdict — NOT RUN

**Independent reviewer:** `NOT RUN`  
**Competence / authorization / independence check:** `NOT RUN`  
**Verdict:** `NOT RUN`  
**EV4:** `BLOCKED PENDING ELIGIBLE INDEPENDENT REVIEW`  
**EV5 / Current adoption / Promotion:** `BLOCKED`  

This packet may enter a review queue only after the packet-head itself passes fresh repository CI and the Current authority baseline remains compatible.
