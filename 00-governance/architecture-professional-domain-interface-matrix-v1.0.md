# OLEANDER Architecture × Professional Domain Interface Matrix v1.0

**Status:** CURRENT INTEGRATION VIEW
**Architecture owner:** `architecture-design-development-process-v1.0.md`
**Interface-semantics owner:** `cross-disciplinary-design-integration-v1.0.md`
**Shared design-development owner:** `design-quality-and-design-development-specification-v1.0.md`
**Generic professional-process envelope:** `professional-domain-process-contract-v1.0.md`
**Authority position:** subordinate view under `complex-project-master-runtime-v1.0.md`; not a second process, integration authority, code matrix or professional approval system.

---

## 1｜Purpose

This matrix answers one operational question:

> At each Architecture `ADD-00 ... ADD-17` decision, which professional interfaces must exist, what must they exchange, what maturity is required for the current architectural claim, and what changes reopen the work?

It does **not** align professions by stage number.

```text
Architecture ADD-07
≠ Structural stage 07
≠ MEP stage 07
≠ Interior stage 07
```

The source side of every interface must resolve the **actual Current professional milestone / artifact / authority** of that domain. Where a domain-native OLEANDER process is not yet Current, this matrix uses descriptive input names only. Those descriptions are interface requirements, not invented professional stages.

---

## 2｜Domain keys used in this view

| Key | Domain / responsibility |
|---|---|
| `STR` | Structural Engineering |
| `MEP` | Building Services / MEP |
| `INT` | Interior Design |
| `LAN` | Landscape Architecture |
| `FLS` | Fire / Life Safety professional or authority input |
| `ACC` | Accessibility professional / specialist input |
| `LGT` | Lighting Design |
| `ENV` | Facade / Envelope |
| `ACO` | Acoustics |
| `COST` | Cost / QS |
| `FM` | Facilities Management / Maintenance / Operations |

Other triggered domains may be added through the same Integration contract. This table is not a closed profession registry.

---

## 3｜Interface semantics reused from Current Integration authority

This matrix reuses, without redefining:

```text
Maturity
IDENTIFIED → DEFINED → COORDINATED → EXERCISED → VERIFIED

Disposition
OPEN / BLOCKED / CLOSED / OUTSIDE_CLAIM

Coupling
INFORMATIVE / DEPENDENT / RECIPROCAL / TIGHTLY_COUPLED

Criticality
ROUTINE / MATERIAL / MAJOR / CRITICAL
```

`VERIFIED` always means verified against the current Interface Acceptance Contract and claim ceiling. It does not automatically mean statutory approval, signed engineering design, field verification, commissioning or construction acceptance.

---

## 4｜How to read required maturity

Two maturity thresholds are shown:

- **Enter** — minimum interface maturity needed before Architecture may responsibly execute the stage at the stated claim ceiling.
- **Close** — minimum maturity needed before the architectural decision can close for the current claim.

These are **floors**, not automatic closure. Higher criticality, tighter coupling, stronger promoted claims or project-specific Acceptance Contracts can require a higher maturity.

An interface may remain `OPEN` after an ADD stage only when:

1. the stage's required maturity has already been met;
2. the remaining work belongs to a later or explicitly excluded claim;
3. no controlling-authority conflict remains;
4. the open item and later owner are explicit;
5. the Architecture claim is not widened to imply the unresolved professional result.

---

## 5｜Architecture stage coverage overview

| Architecture stage | Primary architectural decision | Typical professional interfaces | Normal close floor for architecture claim | OPEN allowed? |
|---|---|---|---|---|
| ADD-00 | scope / authority / claim ceiling | all triggered domains | IDENTIFIED; authority conflicts resolved | Yes, if explicitly outside current claim |
| ADD-01 | site / context / arrival | LAN, FLS, ACC, MEP, FM, ENV | DEFINED; critical access constraints COORDINATED where they control planning | Yes, later technical verification may remain open |
| ADD-02 | users / operations / time states | INT, FM, FLS, ACC, MEP | DEFINED | Yes, detailed technical responses may remain open |
| ADD-03 | program / room brief | INT, MEP, LGT, ACO, FLS, ACC, STR, ENV, FM | DEFINED | Yes, detailed systems may remain open if room requirements are explicit |
| ADD-04 | adjacency / separation | INT, MEP, ACO, FLS, FM, ACC | DEFINED; controlling separations COORDINATED where material | Yes, later details may remain open |
| ADD-05 | zoning alternatives / selection | STR, MEP, LAN, FLS, ACC, ENV, LGT, ACO, COST, FM | COORDINATED for variables driving option selection | Only if non-controlling for selection |
| ADD-06 | multi-flow systems | FLS, ACC, INT, MEP, LAN, FM | COORDINATED for critical route/control boundaries | Yes, later capacity/compliance proof may remain open |
| ADD-07 | horizontal / vertical circulation | FLS, ACC, STR, MEP, INT, LGT, FM | COORDINATED; EXERCISED where geometry interaction must be read back | Limited; in-claim MAJOR/CRITICAL pinches cannot remain unresolved |
| ADD-08 | life-safety / accessibility-aware planning | FLS, ACC, STR, MEP, INT, LGT | COORDINATED; current design-path readback EXERCISED where needed | Formal approval may remain open; architectural reserve conflicts may not |
| ADD-09 | service / hygiene / supervision / security | MEP, INT, FM, FLS, ACC, LAN, COST | COORDINATED for service/hygiene/security boundaries | Yes, detailed equipment engineering may remain open |
| ADD-10 | structure / MEP / envelope fit-back | STR, MEP, ENV, INT, FLS, ACC, LGT, ACO, FM, COST | COORDINATED; critical assembled geometry EXERCISED | No for in-claim fit-back conflicts |
| ADD-11 | climate / daylight / acoustics / environment | MEP, ENV, LGT, ACO, LAN, INT, FM, COST | COORDINATED; analysis-to-design consequence EXERCISED | Performance verification may remain open if claim stays bounded |
| ADD-12 | landscape / external space | LAN, MEP, LGT, FLS, ACC, STR, FM, COST | COORDINATED; route/drainage/level interfaces EXERCISED where material | Limited |
| ADD-13 | FF&E / equipment / room usability | INT, MEP, LGT, ACC, FLS, STR, ACO, FM | EXERCISED in representative critical rooms | Detailed procurement may remain open |
| ADD-14 | area / cost / lifecycle | COST, FM, STR, MEP, ENV, INT, LAN | COORDINATED for cost/lifecycle drivers | Yes, market pricing may remain open if assumptions explicit |
| ADD-15 | existing building / phasing | STR, MEP, ENV, FLS, ACC, INT, LAN, FM, COST | COORDINATED; hazardous/retention assumptions may require VERIFIED source evidence | Unknown existing conditions may remain OPEN but cap the claim |
| ADD-16 | jurisdictional code / standard matrix | FLS, ACC, STR, MEP, ENV + other regulated domains | DEFINED / COORDINATED design responses; VERIFIED only where actual authority evidence supports it | Yes, but status must remain OPEN / BLOCKED, never implied compliant |
| ADD-17 | independent plan / section review | all triggered domains + Integration | current required maturity satisfied per interface | Only outside-claim or later-stage items that do not contradict architectural PASS |

---

## 6｜Detailed stage interface contracts

### ADD-00｜Scope, authority and claim ceiling

**Architecture decision:** what this cycle is allowed to decide and prove.

| Interface | Incoming to Architecture | Outgoing from Architecture | Controlled/shared variables | Direction / coupling | Typical criticality | Enter → Close | Acceptance / readback | Change / reopen |
|---|---|---|---|---|---|---|---|---|
| ALL triggered domains | domain scope, current authority, available evidence, unresolved approvals, current professional claim ceiling | project scope, architecture decision objects, architectural claim ceiling, expected interface dates | jurisdiction, survey basis, occupancy/capacity, baseline geometry, program, project datum, authority refs | BIDIRECTIONAL / RECIPROCAL | MATERIAL; CRITICAL where safety/authority basis controls claim | IDENTIFIED → IDENTIFIED/DEFINED | authority map + claim-ceiling readback | any authority/source/baseline change reopens ADD-00 and affected downstream stages |
| FLS / ACC | applicable authority route and whether specialist/statutory review is triggered | architecture scope and explicit non-compliance boundary | occupancy assumptions, accessible population/use, jurisdiction | BIDIRECTIONAL / DEPENDENT→RECIPROCAL | CRITICAL when in claim | IDENTIFIED → DEFINED | named authority route and OPEN status | jurisdiction/occupancy/use change |

**Can remain OPEN:** yes, where the professional result is outside the current architecture claim.
**Does not prove:** any discipline approval, code compliance, field/survey truth or Design KEEP.

---

### ADD-01｜Site, context and arrival systems

**Architecture decision:** how the building/site is reached, serviced and related to external conditions.

| Interface | Incoming to Architecture | Outgoing from Architecture | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance / native readback | Reopen trigger |
|---|---|---|---|---|---|---|---|---|
| LAN | topography/levels, retained landscape constraints, outdoor-use logic, drainage/soil/tree constraints at current evidence ceiling | building entries, external program, hardscape/threshold zones, desired arrival sequence | site levels, paths, grades, tree protection, external program zones | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | IDENTIFIED → DEFINED/COORDINATED | site plan + access/level diagram | entry/location/level/tree/drainage strategy change |
| FLS | fire-service access assumptions / hard constraints | building perimeter, entry, fire-service interface reserves | access route, turning/stand-off assumptions, fire-service entry points | IN to Architecture / DEPENDENT | CRITICAL when applicable | IDENTIFIED → COORDINATED for controlling geometry | code-aware site plan; status remains bounded | occupancy, building extent, fire-service route change |
| ACC | accessible approach requirements and current evidence | accessible arrival/entrance concept | path gradient, level change, threshold, accessible drop-off | BIDIRECTIONAL / RECIPROCAL | CRITICAL where accessible route is in claim | IDENTIFIED → COORDINATED | continuous site-to-entry route readback | level/entrance/path relocation |
| MEP | utility entry / major site service / drainage constraints where known | plant/service entry zones, roof/site discharge intentions | utility corridors, drainage points, plant access | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | IDENTIFIED → DEFINED | coordinated site/service diagram | service entry or drainage strategy change |
| FM | delivery, waste, maintenance, after-hours access requirements | service yard / route / maintenance access concept | service gate, loading, waste, maintenance paths | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED | service flow readback | operational model change |
| ENV | orientation / exposure / facade access constraints | building orientation, perimeter and opening intent | facade exposure, maintenance access, ground interface | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED | site-envelope relationship diagram | mass/orientation/perimeter change |

**Can remain OPEN:** detailed civil/drainage/fire/accessibility verification may remain open if Architecture keeps the claim at design-reserve level.
**Does not prove:** civil approval, fire appliance compliance, accessible-route certification or verified survey.

---

### ADD-02｜Brief, users and operational states

**Architecture decision:** who uses the project, in which operating states, with what control boundaries.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| FM | staffing, opening hours, cleaning, servicing, maintenance, after-hours operations | proposed spatial/temporal operational states | operating states, access zones, staffing assumptions | BIDIRECTIONAL / RECIPROCAL | MAJOR | IDENTIFIED → DEFINED | `USER_OPERATION_MATRIX` + operational scenario review | hours/staffing/community-use/service model change |
| INT | user activity / furniture-intensive behavior / privacy needs | room-use and spatial experience requirements | user groups, activity states, privacy/control levels | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED | user/activity matrix | brief/use model change |
| FLS | emergency-use assumptions tied to occupancy/use | declared emergency state and occupancy assumptions | occupancy categories, peak use, emergency state | BIDIRECTIONAL / RECIPROCAL | CRITICAL | IDENTIFIED → DEFINED | explicit assumptions + OPEN statutory items | occupancy/use/event strategy change |
| ACC | participation/use requirements | inclusive operational states and access assumptions | user capability assumptions, assisted/independent use, after-hours access | BIDIRECTIONAL / RECIPROCAL | CRITICAL where in claim | IDENTIFIED → DEFINED | operational accessibility scenario | user cohort / operational state change |
| MEP | operational constraints affecting conditioning/services | occupancy schedules / special-use periods | schedules, loads assumptions, after-hours zones | OUT to MEP / DEPENDENT | MATERIAL | IDENTIFIED → DEFINED | schedule/load assumption handoff | operational schedule change |

**Does not prove:** capacity calculations, emergency compliance, accessibility certification or system sizing.

---

### ADD-03｜Program and room-level brief

**Architecture decision:** what each room must actually support beyond area.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| INT | activity/furniture/equipment/use requirements | room dimensions, use envelope, storage/interface brief | room dimensions, clear zones, equipment/furniture envelopes | BIDIRECTIONAL / RECIPROCAL | MAJOR | IDENTIFIED → DEFINED | `ROOM_BRIEF_REGISTER` | room use/equipment/furniture basis change |
| MEP | water, drainage, exhaust, ventilation, power/data, plant/service adjacency needs | room loads/use schedules, wet/exhaust/equipment locations | wet points, exhaust, loads, service zone, riser adjacency | BIDIRECTIONAL / RECIPROCAL | MAJOR | IDENTIFIED → DEFINED | room data requirements; no detailed design claim | room type/equipment/occupancy change |
| LGT | task/ambient/daylight integration requirements | room function, visual tasks, ceiling/opening intent | task planes, daylight dependence, ceiling zones | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED | room lighting criteria | activity/ceiling/opening change |
| ACO | noise generation/sensitivity and isolation requirements | room adjacency/use and volume assumptions | noise class, reverberation intent, partitions/doors | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | IDENTIFIED → DEFINED | acoustic criteria in room brief | use/adjacency/partition strategy change |
| FLS | use/hazard/occupancy implications | room occupancy/use/hazard assumptions | occupancy, hazard, compartment implications | BIDIRECTIONAL / RECIPROCAL | CRITICAL when applicable | IDENTIFIED → DEFINED | explicit fire-aware brief status | occupancy/use/hazard change |
| ACC | maneuvering/use/participation needs | room clearances and inclusive-use requirements | turning/transfer/approach zones, accessible fixtures/equipment | BIDIRECTIONAL / RECIPROCAL | CRITICAL | IDENTIFIED → DEFINED | room accessibility criteria | room/equipment layout basis change |
| STR / ENV | special span/load/height/perimeter constraints | room heights/spans/opening/environmental needs | span, imposed load assumption, clear height, opening intent | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | IDENTIFIED → DEFINED | flagged special rooms | room volume/load/perimeter need change |
| FM | cleaning, storage, replacement and maintenance needs | room service/maintenance access requirements | maintenance clearance, storage, replacement route | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED | maintainability entries in room brief | maintenance strategy change |

**Does not prove:** engineered services, structural adequacy, acoustic performance or code compliance.

---

### ADD-04｜Adjacency and separation logic

**Architecture decision:** which spaces must connect, see, share, separate or avoid.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| INT / FM | operational adjacency, supervision, shared support, privacy/service requirements | selected adjacency/separation model | adjacency class, visual relation, controlled boundary | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → DEFINED/COORDINATED | `ADJACENCY_MATRIX` with rationale | operational/user/security relation change |
| MEP | wet-stack, exhaust, plant/service adjacency constraints | wet/service clustering intent | wet adjacency, riser/exhaust proximity | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | IDENTIFIED → DEFINED | services-aware adjacency graph | system strategy change |
| ACO | noise source/sensitive receiver relationships | acoustic separation intent | source-receiver pairs, buffer zones | BIDIRECTIONAL / RECIPROCAL | MAJOR | IDENTIFIED → DEFINED | acoustic adjacency flags | room use/location change |
| FLS | compartment/hazard separation drivers | room relationship response | fire/hazard separation concept | BIDIRECTIONAL / RECIPROCAL | CRITICAL where controlling | IDENTIFIED → COORDINATED for controlling relation | fire-aware relationship graph | use/hazard/compartment basis change |
| ACC | accessible support-room and route relationship requirements | adjacency response | accessible route/fixture/support adjacency | BIDIRECTIONAL / RECIPROCAL | MAJOR | IDENTIFIED → DEFINED | accessibility-aware adjacency check | use/route change |

**Does not prove:** partition rating, detailed MEP routing, final acoustic isolation or fire approval.

---

### ADD-05｜Zoning alternatives and selection

**Architecture decision:** which zoning option should continue and why.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| STR | feasible structural order, span/transfer constraints at concept level | option grids/massing/voids and major span intents | grid, span, transfers, cores, large openings | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED for selection drivers | option-by-option structure consequence | structural feasibility basis changes |
| MEP | plant/distribution/wet/exhaust zoning constraints | option cores/risers/plant reserves and zoning | risers, plant, wet stacks, service zones | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | MEP consequence per option | system concept changes |
| LAN | external program / levels / site sequence | building placement/courts/outdoor relationships | courtyards, external zones, levels, access | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | DEFINED → COORDINATED when option driver | integrated site option readback | site/landscape premise change |
| FLS / ACC | critical distribution/accessibility implications | stair/core/route/entry reserves per option | cores, exits, accessible vertical route, travel topology | BIDIRECTIONAL / TIGHTLY_COUPLED where option viability depends on it | CRITICAL | DEFINED → COORDINATED | option cannot be retained if known hard reserve conflict is unresolved | occupancy/core/route assumption change |
| ENV / LGT | orientation/daylight/envelope-depth constraints | massing/orientation/opening/atrium intent | perimeter depth, orientation, openings, shading | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | DEFINED → COORDINATED if design driver | comparative environmental consequence | massing/orientation change |
| ACO | noise zoning / sensitive-source separation constraints | noisy/quiet zoning | source-receiver distribution | BIDIRECTIONAL / RECIPROCAL | MATERIAL | DEFINED → COORDINATED if selection driver | option acoustic consequence | use/location change |
| COST / FM | major cost/maintenance/operational implications | option quantities, complexity, access concept | GFA, envelope ratio, core count, plant access, operational boundaries | BIDIRECTIONAL / RECIPROCAL | MAJOR where option selection depends on it | DEFINED → COORDINATED | comparative cost/lifecycle consequence with assumptions | budget/operating model change |

**Can remain OPEN:** only non-controlling detailed design. A known option-killing interface cannot be deferred and still support selection.
**Does not prove:** engineered feasibility, cost certainty, fire/accessibility compliance or Design KEEP.

---

### ADD-06｜Flow systems

**Architecture decision:** whether multiple user/service/emergency flows can coexist coherently across operational states.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| FLS | evacuation/emergency movement constraints | emergency path topology/reserves | origins, exits, protected paths, door/control points | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → COORDINATED | `FLOW_SYSTEM_MATRIX` with emergency path explicitly separated from normal flow | occupancy/exit/core/door change |
| ACC | continuous accessible movement requirements | accessible route topology | accessible path, vertical transition, thresholds | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → COORDINATED | continuous route readback | level/core/door/room relocation |
| INT | user movement + furniture/queue occupation | internal flow hierarchy and conflict zones | furniture encroachment, queues, thresholds | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | flow/furniture conflict readback | furniture/use/space change |
| MEP / FM | service, waste, food, maintenance routes | service flow and controlled interfaces | delivery, waste, replacement, service corridors | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | separate operational flow diagrams | plant/service/operating strategy change |
| LAN | external arrival / accessible / emergency / service paths | building-to-site flow continuity | site path nodes, entrances, service/emergency access | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | site/building flow continuity | entry/site route change |

**Does not prove:** egress capacity, accessibility certification, operating staffing sufficiency or detailed service logistics.

---

### ADD-07｜Horizontal and vertical circulation

**Architecture decision:** whether circulation works as real geometry, not diagrammatic residual space.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance / native readback | Reopen |
|---|---|---|---|---|---|---|---|---|
| FLS | stair/exit/door/travel constraints and current design basis | stair/core/corridor/door geometry | clear widths, stairs, landings, doors, dead ends, path topology | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → COORDINATED; EXERCISED where geometric chain is claimed | measured plan/section circulation readback; no name-based continuity | stair/door/path/occupancy change |
| ACC | maneuvering, ramp/lift, threshold requirements | accessible circulation geometry | clear width, turning, lift lobby, ramp/landing, door approach | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → EXERCISED for claimed continuous route | actual geometry chain readback | geometry/level/lift/door change |
| STR | structural core/opening/slab constraints | openings, stairs, voids and support geometry | stair/void openings, landing support, column conflicts | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | plan+section overlay / coordinated native model | grid/opening/core change |
| MEP | riser/shaft/ceiling/service conflicts | circulation/service zone geometry | shafts, ceiling zones, plant access, corridor services | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | corridor/shaft/ceiling fit readback | riser/service-zone change |
| INT | furniture/queue/wayfinding occupation | usable circulation and threshold zones | queue reserve, furniture, informal learning, door swing | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → EXERCISED for critical zones | furnished circulation readback | FF&E/use/door change |
| LGT / FM | wayfinding/safe-use/maintenance needs | lighting/wayfinding zones and maintenance access | visual hierarchy, lighting positions, maintenance route | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED/COORDINATED | representative circulation experience/readback | ceiling/lighting/operation change |

**Can remain OPEN:** later statutory capacity proof can remain open, but an in-claim broken route, false stair chain, unresolved pinch or inaccessible discontinuity cannot support Architecture PASS.
**Does not prove:** fire compliance, accessibility certification or structural engineering approval.

---

### ADD-08｜Life-safety-aware and accessibility-aware planning

**Architecture decision:** whether the plan reserves a credible path for later professional/statutory closure.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| FLS | current code/professional design basis for egress, compartment, smoke-sensitive conditions | travel/stair/exit/compartment/opening design response | occupancy, travel path, exits, stairs, compartment/opening topology, atrium/void | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → COORDINATED; EXERCISED for geometry-dependent path claims | explicit life-safety-aware plan/section readback + OPEN compliance boundary | occupancy, openings, stairs, compartment, atrium change |
| ACC | current accessibility requirements / specialist basis | continuous accessible route and participation response | entry, door clearance, maneuvering, lift/ramp, toilet/changing, participation zones | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → EXERCISED for route geometry | route/room readback; certification remains separate | route/level/room/equipment change |
| STR / MEP | structural and system implications of protected/vertical movement / smoke or lift zones | reserved geometry / service zones | core, shafts, smoke/service zones, lift/stair openings | BIDIRECTIONAL / RECIPROCAL | MAJOR–CRITICAL | DEFINED → COORDINATED | coordinated reserves | core/system strategy change |
| INT / LGT | door/finish/fixture/emergency-lighting interface constraints | door/threshold/finish/lighting intent | doors, thresholds, visual guidance, emergency-lighting zones | BIDIRECTIONAL / RECIPROCAL | MAJOR | IDENTIFIED → DEFINED/COORDINATED | coordinated key details at design ceiling | door/finish/lighting strategy change |

**Can remain OPEN:** formal calculations, authority approval and certification may remain open; architecture may claim only `life-safety-aware / accessibility-aware planning` at its actual evidence ceiling.
**Does not prove:** FIRE PASS, ACCESSIBILITY CERTIFICATION, statutory approval.

---

### ADD-09｜Service, hygiene, supervision and security

**Architecture decision:** whether backstage/service/hygiene/control functions can operate without corrupting primary use.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| MEP | wet/exhaust/drainage/service/equipment constraints | wet/service room layout and routes | fixtures, wet stacks, exhaust, plant/service access | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | `OPERATIONS_SECURITY_HYGIENE_MATRIX` + wet/service readback | fixture/system/service-route change |
| INT | changing/toilet/storage/reception/controlled-boundary use needs | room layout and privacy/supervision strategy | screens, partitions, lockers, queues, reception | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | representative room/threshold readback | layout/equipment/use change |
| FM | cleaning, waste, delivery, security, after-hours operations | service/security boundaries and flows | service access, waste, lock zones, maintenance route | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | operational-state review | operation/security model change |
| FLS / ACC | applicable requirements at controlled/service/hygiene spaces | architectural response/reserves | doors, accessible toilet/changing, protected/service separation | BIDIRECTIONAL / RECIPROCAL | CRITICAL where applicable | DEFINED → COORDINATED | explicit design response with OPEN authority status | room/door/control change |
| LAN | service yard / waste / delivery external interface | site service boundary | yard, gate, path, screening | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED | site/service integration readback | site/service route change |
| COST | major service-equipment/fitout cost implications | quantities/reserve assumptions | room counts, equipment allowances | BIDIRECTIONAL / DEPENDENT | MATERIAL | IDENTIFIED → DEFINED | cost assumption handoff | budget/equipment strategy change |

**Does not prove:** hygiene compliance, security certification, commissioned MEP or operational staffing sufficiency.

---

### ADD-10｜Structure, MEP and envelope fit-back

**Architecture decision:** whether the chosen architecture still works after real system constraints return into the plan/section/model.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance / readback | Reopen |
|---|---|---|---|---|---|---|---|---|
| STR | current grid/member/core/opening/transfer/movement-joint requirements | architectural grid, openings, voids, room/circulation clearances | grid, columns/walls, spans, transfers, movement joints, openings | BIDIRECTIONAL / TIGHTLY_COUPLED | MAJOR–CRITICAL | DEFINED → COORDINATED; EXERCISED for assembled geometry | native plan/section/model overlay; clashes plus design consequence | structural basis/grid/opening change |
| MEP | risers, plant, distribution, ceiling/service zones, drainage, replacement routes | room/shaft/ceiling/plant reserves and architecture constraints | plant, risers, ceiling zones, wet stacks, routes, replacement access | BIDIRECTIONAL / TIGHTLY_COUPLED | MAJOR–CRITICAL | DEFINED → EXERCISED where spatial fit is claimed | coordinated native geometry + `ARCH_SYSTEM_FITBACK_RECEIPT` | system zoning/equipment/route change |
| ENV | facade depth, opening, thermal/shading/maintenance constraints | facade geometry/opening/shading/edge intent | envelope build-up, openings, shading, parapets, roof edge | BIDIRECTIONAL / TIGHTLY_COUPLED | MAJOR | DEFINED → COORDINATED/EXERCISED | section/detail-scale fit readback | envelope system/opening/depth change |
| INT | ceiling/wall/finish/furniture interface needs | available interior zones and adjusted architecture | ceiling height, partitions, thresholds, service access | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | representative room/ceiling fitback | system/partition/ceiling change |
| FLS / ACC | constraints affected by fit-back | preserved egress/access geometry after fit-back | clear widths, doors, routes, stairs/lifts | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | COORDINATED → EXERCISED for changed critical geometry | re-read critical routes after system fitback | any fitback encroachment |
| LGT / ACO | ceiling/service/acoustic volume constraints | ceiling/void/opening geometry | ceiling zone, fixture/acoustic treatment zones | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | DEFINED → COORDINATED | ceiling/room section readback | ceiling/service strategy change |
| FM / COST | maintainability/replacement/cost consequences | maintenance access + revised quantities/complexity | access zones, replacement routes, high-cost transfers/plant/envelope | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | maintainability/cost consequence record | equipment/system/design change |

**Can remain OPEN:** detailed engineering calculations may remain open, but the architecture cannot call fit-back closed while known system geometry invalidates rooms, routes, heights, openings or primary intent.
**Does not prove:** structural/MEP engineering PASS, envelope performance certification or construction readiness.

---

### ADD-11｜Climate, daylight, acoustics and environmental behavior

**Architecture decision:** how environmental analysis changes architecture rather than merely documenting it.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| MEP | thermal/ventilation/zoning/plant constraints and analysis | orientation/zone/opening/volume response | thermal zones, ventilation mode, internal loads, plant strategy | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED; EXERCISED for claimed behavior | analysis → design consequence trace | system/load/zone change |
| ENV | thermal/solar/opening/shading/condensation design constraints | facade/opening/shading response | glazing ratio, shading, envelope depth, thermal boundary | BIDIRECTIONAL / TIGHTLY_COUPLED | MAJOR | DEFINED → COORDINATED/EXERCISED | facade/environment section readback | facade/opening/orientation change |
| LGT | daylight/glare/task-light analysis | opening/daylight-zone/interior-light response | daylight apertures, task zones, shading, reflectance assumptions | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | DEFINED → EXERCISED for daylight design claim | daylight/lighting readback at relevant conditions | opening/shading/room use change |
| ACO | source/path/receiver and reverberation analysis | zoning/volume/partition/opening response | room volume, separation, absorptive area intent, openings | BIDIRECTIONAL / TIGHTLY_COUPLED where acoustic performance drives form | MAJOR | DEFINED → EXERCISED for design consequence | acoustic model/criteria linked to geometry | use/volume/partition/opening change |
| LAN | wind/shade/outdoor comfort/drainage microclimate inputs | building-landscape response | shade, wind exposure, runoff, outdoor-use zones | BIDIRECTIONAL / RECIPROCAL | MATERIAL | DEFINED → COORDINATED | site/environment consequence | mass/landscape/level change |
| INT / FM / COST | occupant comfort, finishes, controls, operations, lifecycle/cost constraints | material/space/control assumptions | finishes, occupancy schedules, operability, maintenance | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED/COORDINATED | documented assumption/consequence | material/operation/budget change |

**Does not prove:** certified energy/daylight/acoustic performance, commissioning or field comfort.

---

### ADD-12｜Landscape and external-space integration

**Architecture decision:** whether external space is part of the program, circulation, environmental and operational system.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| LAN | developed landscape program, grading, planting/tree, surface/water/maintenance strategy | building edges, thresholds, entrances, external program interfaces | levels, paths, edges, tree zones, drainage, program zones | BIDIRECTIONAL / TIGHTLY_COUPLED | MAJOR | DEFINED → EXERCISED for level/route integration | integrated site plan/sections | building edge/level/path/landscape strategy change |
| ACC | accessible external-route criteria | route/threshold/grade response | grades, landings, surfaces, thresholds | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → EXERCISED | continuous site route readback | grade/path/threshold change |
| FLS | emergency/fire access constraints | site response | fire-service route/standing/entry | BIDIRECTIONAL / RECIPROCAL | CRITICAL where applicable | DEFINED → COORDINATED | fire-aware site plan | building/site access change |
| MEP / LGT | drainage, utilities, external lighting constraints | drainage/utility/light zones and architectural interfaces | inlets, service corridors, light zones, external power | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED/EXERCISED where geometry-dependent | coordinated site services/light plan | level/drainage/utility/light change |
| STR | retaining / canopy / external structural constraints | external structures/loads/interfaces | retaining geometry, canopy supports, slab/edge loads | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | IDENTIFIED → COORDINATED where material | site section / structure interface | grade/external structure change |
| FM / COST | maintenance, replacement, seasonal operation, budget | maintenance access/material/quantity response | maintenance routes, durable surfaces, plant management | BIDIRECTIONAL / RECIPROCAL | MATERIAL | DEFINED → COORDINATED | lifecycle/cost consequence | maintenance/budget/material change |

**Does not prove:** civil/drainage approval, landscape construction readiness, fire/accessibility certification.

---

### ADD-13｜FF&E, equipment and real room usability

**Architecture decision:** whether representative critical rooms function with real/bounded contents rather than empty rectangles.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| INT | current furniture/equipment/layout/finish intent | room shell/clearance response | furniture/equipment footprints, clear zones, storage, teaching/display walls | BIDIRECTIONAL / TIGHTLY_COUPLED | MAJOR | DEFINED → EXERCISED | representative `ROOM_USE_READBACKS` in native plan/model | FF&E/equipment/room geometry change |
| MEP | connection/service/heat/exhaust/maintenance needs | equipment/service reserves | power/data/water/exhaust, access clearances | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → EXERCISED in critical rooms | equipment + services overlay | equipment/service change |
| ACC | approach/transfer/use requirements | clearances/accessible positions | approach, turning, knee/transfer/operating zones | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → EXERCISED | furnished accessibility readback | furniture/equipment/layout change |
| FLS | aisle/door/occupancy/fire-load or egress constraints | furnished-room response | aisles, doors, occupant layout, equipment boundaries | BIDIRECTIONAL / RECIPROCAL | CRITICAL where applicable | DEFINED → EXERCISED | furnished egress-aware readback | furniture/seating/door change |
| LGT / ACO | task-light/acoustic treatment constraints | furniture/ceiling/room-use relationship | task planes, fixture positions, absorptive zones | BIDIRECTIONAL / RECIPROCAL | MATERIAL | DEFINED → EXERCISED in representative rooms | room use + lighting/acoustic readback | layout/ceiling/use change |
| STR / FM | local load/fixing/replacement/maintenance constraints | equipment location / support and replacement route | equipment loads, fixing zones, replacement clearance | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | IDENTIFIED → COORDINATED/EXERCISED where controlling | critical equipment support/access note | equipment/route/support change |

**Does not prove:** procurement, equipment certification, detailed MEP connection design or structural support approval.

---

### ADD-14｜Area efficiency, cost pressure and lifecycle

**Architecture decision:** whether the architecture remains viable when area, budget, durability and maintenance consequences are visible.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| COST | cost plan / rate assumptions / major cost drivers / uncertainty | current quantities, GFA/net area, complexity and option deltas | GFA, NIA, envelope area, structural/system complexity, major materials | BIDIRECTIONAL / RECIPROCAL | MAJOR when budget is controlling | DEFINED → COORDINATED | area/cost reconciliation with dated assumptions | budget/rate/quantity/design change |
| FM | maintenance/replacement/operational burden | access/material/system response | replacement cycle, cleaning, maintenance access, durability | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | lifecycle consequence matrix | operational/maintenance assumption change |
| STR / MEP / ENV | system quantities/complexity/plant/envelope implications | optimization constraints and architectural response | grid/span, plant, service zones, envelope ratio/depth | BIDIRECTIONAL / RECIPROCAL | MATERIAL–MAJOR | DEFINED → COORDINATED for cost/lifecycle drivers | system consequence included in cost/lifecycle view | system basis change |
| INT / LAN | fitout/landscape area/material/maintenance implications | scope and material/area response | finish areas, external works, furnishing scope | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED/COORDINATED | scope/quantity assumption handoff | scope/material change |

**Can remain OPEN:** market pricing and procurement may remain open, but cost/area claims must state date, basis and uncertainty.
**Does not prove:** tender price, whole-life-cost certification or value engineering quality.

---

### ADD-15｜Existing-building, phasing and construction-state logic

**Architecture decision:** what is retained/demolished/unknown and how design/operation changes across phases.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| STR | verified/assumed existing structure condition and investigation needs | retention/opening/demolition/temporary-condition intent | retained members, openings, loads, temporary stability assumptions | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | IDENTIFIED → COORDINATED; VERIFIED source evidence required for strong retention claims | existing-condition/retention map with evidence state | survey/investigation/retention design change |
| MEP | existing services condition/capacity/isolation/phasing constraints | retained/replaced system zones and phase interfaces | live services, plant, risers, temporary services | BIDIRECTIONAL / TIGHTLY_COUPLED | MAJOR–CRITICAL | IDENTIFIED → COORDINATED | phased services diagram with unknowns | survey/system/phasing change |
| ENV | existing facade/roof condition and replacement constraints | retention/replacement/enclosure strategy | retained fabric, openings, weather boundary | BIDIRECTIONAL / RECIPROCAL | MAJOR | IDENTIFIED → COORDINATED | envelope condition/phase interface | survey/envelope strategy change |
| FLS / ACC | temporary/phase-specific safety/accessibility requirements | phased routes/compartments/entries | temporary exits/routes, occupied zones, barriers | BIDIRECTIONAL / TIGHTLY_COUPLED | CRITICAL | DEFINED → COORDINATED/EXERCISED for occupied-phase route geometry | phase plan readback; statutory closure separate | phase sequence/occupied area/route change |
| INT / LAN | retained finishes/site fabric/use constraints | phased fitout/site interface | retained elements, temporary access, external work zones | BIDIRECTIONAL / RECIPROCAL | MATERIAL | IDENTIFIED → DEFINED/COORDINATED | phase/retention plan | scope/retention change |
| FM / COST | continuity, decant, logistics, temporary operation, cost risk | phase sequence/logistics and assumptions | occupied zones, shutdown windows, temporary works/logistics | BIDIRECTIONAL / RECIPROCAL | MAJOR | DEFINED → COORDINATED | phasing/operation/cost-risk readback | operational/budget/phase change |

**Can remain OPEN:** unknown existing conditions may remain explicit, but they reduce claim ceiling. Visual similarity/photos cannot establish structural or service retention authority.
**Does not prove:** field condition, structural retention adequacy, temporary works design, contractor methodology.

---

### ADD-16｜Jurisdictional code / standard matrix

**Architecture decision:** whether each applicable requirement has a current source, applicability decision, design response and verification state.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| FLS | current requirement/source/applicability/professional interpretation | architectural design response and evidence refs | occupancy, egress, compartment, access, fire-service interface | BIDIRECTIONAL / DEPENDENT→RECIPROCAL | CRITICAL | DEFINED → COORDINATED for design response; VERIFIED only with actual authority evidence | `ARCHITECTURE_CODE_MATRIX` row status | source/version/use/design change |
| ACC | current accessibility requirements/applicability | architecture response/evidence | routes, dimensions, fixtures, participation | BIDIRECTIONAL / RECIPROCAL | CRITICAL | DEFINED → COORDINATED; VERIFIED only at supported ceiling | code-matrix row + geometry refs | source/version/geometry/use change |
| STR / MEP / ENV | regulated-domain requirements that materially constrain architecture | coordinated architectural response | structural/fire-resistance interfaces, services, energy/environment/envelope requirements | BIDIRECTIONAL / RECIPROCAL | MAJOR–CRITICAL | DEFINED → COORDINATED | domain-owner status + architecture response | source/system/design change |
| other triggered regulated domains | actual Current requirement basis | architectural response / OPEN item | domain-specific controlled variables | BIDIRECTIONAL | per consequence | IDENTIFIED/DEFINED → required contract maturity | explicit owner + source/version/applicability/status | source/applicability/design change |

Allowed row statuses remain those of the Architecture process, including `OPEN`, `DESIGN_RESPONSE_PRESENT`, `VERIFIED_AT_CURRENT_CLAIM_CEILING`, `REVISE`, `BLOCKED_BY_AUTHORITY` and `NOT_APPLICABLE_WITH_REASON`.

**Hard rule:** `DESIGN_RESPONSE_PRESENT ≠ REGULATORY COMPLIANCE`.
**Does not prove:** statutory approval, professional sign-off, authority acceptance.

---

### ADD-17｜Independent plan / section review

**Architecture decision:** whether the current architecture still works as a whole after removing producer explanation and prior PASS/KEEP assumptions.

| Interface | Incoming | Outgoing | Shared variables | Direction / coupling | Criticality | Enter → Close | Acceptance | Reopen |
|---|---|---|---|---|---|---|---|---|
| ALL triggered professional domains | current bounded professional receipts / authoritative interface inputs / explicit OPEN items | current architecture plan/section/model + architectural decision package | every in-claim controlled variable consumed by Architecture | BIDIRECTIONAL / per registered interface | inherited from each interface | current required maturity satisfied → no in-claim maturity deficit | independent fresh read of actual current native outputs + interface register | any material professional/shared-variable change |
| Cross-Disciplinary Integration | current interface register, authority map, open MAJOR/CRITICAL count, current integration receipt when triggered | architecture readback and unresolved architecture impacts | all active interface variables | BIDIRECTIONAL / integrated | MAJOR–CRITICAL | required interface maturity → current integration closure for claim | no fake continuity; no unresolved authority conflict; actual readback refs | interface material / coupled system / promotion-breaking change |
| Design Quality | current Project Design DNA / triggered DD responsibilities / DQ readback state | architecture whole-system design evidence | intent, form, experience, human relation, language, craft, coherence | BIDIRECTIONAL at review boundary; not an Integration interface substitute | MATERIAL–MAJOR | current required DQ state → independent design decision remains separate | fresh plan/section/design reread | intent/DNA/form/content/interface change |

Architecture ADD-17 may return `PASS / REVISE / REJECT / HOLD` only within the Architecture process claim.

**Required OPEN boundary:** an unresolved professional/statutory item may remain only when it is explicit, outside the Architecture PASS claim, and does not invalidate the architecture being passed.

**Does not prove:** Design KEEP, Integration PASS, engineering approval, fire/accessibility certification, statutory approval, field verification or Promotion.

---

## 7｜Controlled-variable families by domain

This section is a retrieval aid for building project interfaces. The actual project register remains authoritative.

| Domain | Typical shared / controlled variables consumed by Architecture |
|---|---|
| STR | grid, column/wall/core location, spans, transfers, movement joints, openings, load/deflection-sensitive zones, retained structural status |
| MEP | plant/shaft/riser zones, ceiling/service depth, wet stacks, distribution corridors, equipment access/replacement routes, utility entries, drainage points |
| INT | furniture/equipment envelope, partitions, ceiling, finish build-up, threshold, storage, task/use zones, visual/privacy boundaries |
| LAN | site levels, path alignment/grade, external program, tree/retention zones, drainage/blue-green zones, boundary/maintenance zones |
| FLS | occupancy basis, exits/stairs, travel topology, compartment/opening graph, smoke-sensitive voids, fire-service interface, protected-route reserves |
| ACC | continuous route, gradients, landings, door approaches, maneuvering/turning, lift/ramp, accessible sanitary/changing/participation zones |
| LGT | daylight aperture/shading relation, task planes, fixture/ceiling zones, visual hierarchy, emergency-lighting interface when applicable |
| ENV | envelope build-up/depth, openings, shading, thermal boundary, roof/parapet/edge, maintenance access, retained facade status |
| ACO | source-receiver relationships, room volume, isolation boundary, openings/doors, acoustic treatment zones, plant/noise constraints |
| COST | quantities, areas, structural/system complexity, material/finish scope, cost-plan basis/date, contingencies/uncertainty |
| FM | operating states, staffing/access zones, maintenance clearances, cleaning/waste/delivery, replacement routes, shutdown/phase constraints |

No variable is considered safely shared until its current controlling authority is explicit.

---

## 8｜Change propagation examples

### Example A｜Structural grid shift

```text
STR grid changes
→ ADD-05 zoning fit may reopen
→ ADD-07 circulation pinch/core geometry may reopen
→ ADD-10 fit-back definitely reopens
→ ADD-13 room-use/furniture may reopen where columns move
→ ADD-14 area/cost may reopen
→ affected Integration interfaces become stale
→ ADD-17 independent review becomes stale at affected scope
```

### Example B｜MEP riser relocation

```text
MEP riser changes
→ ADD-03 room brief if usable room envelope changes
→ ADD-04 adjacency if wet/service relation changes
→ ADD-07 circulation if corridor/landing is consumed
→ ADD-09 service/hygiene
→ ADD-10 fit-back
→ ADD-13 room usability where equipment/clearance changes
→ affected Integration receipt stale
```

### Example C｜Accessibility route failure

```text
ACC route discontinuity found
→ ADD-06 accessible flow reopens
→ ADD-07 geometry reopens
→ ADD-08 accessibility-aware planning reopens
→ ADD-12 site route reopens if external
→ ADD-13 room-use readback reopens if furniture/equipment caused failure
→ ADD-16 matrix row returns OPEN / REVISE
→ ADD-17 cannot PASS the affected architecture claim
```

### Example D｜Envelope opening / shading change

```text
ENV opening strategy changes
→ ADD-05 option assumptions may reopen
→ ADD-10 fit-back
→ ADD-11 daylight / climate / acoustic consequences
→ ADD-14 cost/lifecycle
→ ADD-17 design + professional readback at affected facade/room scope
```

---

## 9｜Acceptance-contract rule

For `MAJOR`, `CRITICAL` or `TIGHTLY_COUPLED` interfaces, a generic note such as “coordinated with MEP” is insufficient.

The interface should carry or reference an Acceptance Contract stating:

```text
interface question
current authority / source
shared variables
allowed variation / tolerance when relevant
required maturity for current claim
native artifact / source of truth
validation / readback method
evidence refs
acceptance condition
does-not-prove boundary
change reopen rule
```

This matrix does not replace that project-specific contract.

---

## 10｜Native artifact / source-of-truth expectations

Examples of sufficient architectural interface carriers include:

- editable/native plan, section, elevation and model geometry;
- coordinated room/area schedules;
- `ROOM_BRIEF_REGISTER`;
- `ADJACENCY_MATRIX`;
- `FLOW_SYSTEM_MATRIX`;
- `CIRCULATION_READBACK`;
- `OPERATIONS_SECURITY_HYGIENE_MATRIX`;
- `ARCH_SYSTEM_FITBACK_RECEIPT`;
- representative `ROOM_USE_READBACKS`;
- `ARCHITECTURE_CODE_MATRIX`;
- project `INTERFACE_REGISTER` and Acceptance Contracts.

Screenshots/renders may document readback but cannot silently replace the native source used to make or measure the decision.

---

## 11｜Professional-domain process maturity gap

At the time this matrix is introduced, Architecture has a Current domain-native process (`ADD-00 ... ADD-17`), while several other domains still require their own researched OLEANDER professional-process definitions.

Until those definitions exist:

- do not invent placeholder stage numbers;
- bind the interface to the source domain's real Current artifact / professional milestone / authority;
- keep source-stage identity `OPEN` when it is genuinely unresolved;
- do not downgrade the interface requirement simply because the source process is not yet formalized in OLEANDER;
- prioritize research/definition of the domains with highest interface criticality and error propagation.

Recommended next professional-process priority for built-environment work:

```text
Structural Engineering
→ Building Services / MEP
→ Fire / Life Safety interface process
→ Accessibility interface process
→ Interior Design
→ Landscape Architecture
→ Envelope / Facade
→ Lighting
→ Acoustics
→ Cost / QS / FM / Operations
```

This ordering is an implementation priority, not a universal project sequence.

---

## 12｜Canonical invariants

```text
ARCHITECTURE ADD STAGE ≠ OTHER-DOMAIN SAME-NUMBER STAGE
DESCRIPTIVE INPUT NAME ≠ INVENTED PROFESSIONAL STAGE
COORDINATED ≠ VERIFIED
DESIGN RESPONSE PRESENT ≠ COMPLIANCE
PROFESSIONAL PASS ≠ INTEGRATION PASS
INTEGRATION PASS ≠ DESIGN KEEP
MODEL FIT ≠ ENGINEERING APPROVAL
OPEN ITEM MAY REMAIN ONLY INSIDE AN EXPLICITLY BOUNDED CLAIM
MATERIAL SHARED-VARIABLE CHANGE REOPENS ALL ACTUAL CONSUMERS
NATIVE READBACK PRECEDES ARCHITECTURAL CLOSURE
```
