# C04｜Open PR Lineage Register｜2026-08-17

Purpose: organize open/candidate PRs without confusing recency with authority.

Rules:
- `OPEN PR ≠ CURRENT`.
- A newer candidate may supersede an older candidate in the same object lineage, but does not replace the original Design Source or merged main authority.
- Web/F presentation PRs are downstream carriers.
- Training/Skill PRs are excluded from C04 object authority unless explicitly transferred.

## A｜Design-object candidate lineages

### App / Digital — DO NOT EDIT IN PROJECT ORGANIZATION
| PR | Role | Organization state |
|---|---|---|
| #140 | App currentization from original Design Source | OLDER CANDIDATE / PROVENANCE |
| #144 | App MAIN pixels + Game Map v2.1 | INTERMEDIATE CANDIDATE / PROVENANCE |
| #162 | App mature design v1.6 | LATEST EXISTING APP CANDIDATE |
| user next App delta | next design authority | USER-OWNED / NOT PRODUCED HERE |

No App PR is promoted or modified by this organization pass.

### Culture / Narrative visual
| PR | Role | Organization state |
|---|---|---|
| #128 | Culture Main v2 | LATEST CULTURE VISUAL CANDIDATE / OPEN DRAFT |

The earlier abstract Culture v1 is recorded by #128 as rejected provenance. #128 remains candidate until authority/merge and independent design judgment.

### R05 / R06 / R13
| PR | Role | Organization state |
|---|---|---|
| #133 | R05/R06 source-bound currentization | OBJECT CURRENTIZATION CANDIDATE |
| #145 | R06/R13 multidisciplinary scene outcome | SCENE CURRENTIZATION CANDIDATE |
| #82 | R05 research runtime evidence | HISTORICAL PROVENANCE / REGISTRY RECOVERY HOLD |
| #92 | R05 case-exploration replay | HISTORICAL PROVENANCE / AUTHORITY REPAIR REQUIRED |

Canonical R05/R06/R13 identities remain `C04_R01-R13_CANONICAL_SCENE_REGISTER_v1.0`; candidate PRs do not replace node identity.

### Physical / Sensory
| PR | Role | Organization state |
|---|---|---|
| #143 | P01/P02/Memory currentization | DESIGN/PRESENTATION CANDIDATE / P05 RETAINED |
| #151 | Fluid Rest v1.2 + 3D body/section/assembly proof | LATEST FLUID-REST MODEL/PROOF CANDIDATE |
| #152 | Qingfengyin v1.2 | LATEST QINGFENGYIN DESIGN CANDIDATE |
| #159 | Physical/Sensory public chapter v1.3 | DOWNSTREAM PUBLIC-PRESENTATION CANDIDATE |

Separation rule:
- P03/P04 source design ≠ #151 model/proof.
- #151 proof ≠ #159 public chapter.
- #159 cannot erase P01/P02/P03/P04/P05 by editorial omission.

### Memory / IP
| PR | Role | Organization state |
|---|---|---|
| #143 | Qingjiang Journal ↔ My Book bridge | EARLIER MEMORY CURRENTIZATION CANDIDATE |
| #153 | Qingjiang Journal × My Book v1.1 | LATEST MEMORY-PAIR CANDIDATE |
| #162 | App-side My Book candidate | APP LINEAGE / USER-OWNED NEXT DELTA |

M01/M02 canonical design roles remain upstream. #153 does not take App editing ownership from the user.

### Audience
| PR | Role | Organization state |
|---|---|---|
| #155 | Audience Depth R06 v1.2 | LATEST AUDIENCE PRESENTATION CANDIDATE / INDEPENDENT VERDICT OPEN |

A01–A04 remain canonical Audience/Accessibility/Context objects. Candidate pixel weakness never deletes the system.

## B｜Downstream Web / Delivery / Motion lineages

These PRs are not allowed to redefine C04 project scope.

### Web
| PR | Role | Organization state |
|---|---|---|
| #127 | Web v2.3 / 12-layer architecture candidate | DOWNSTREAM WEB HISTORY/CANDIDATE |
| #163 | final Web framework v2 candidate | DOWNSTREAM WEB CANDIDATE |
| #164 | Current Web Integration v1.2 + Motion v1.0 | LATEST DOWNSTREAM WEB CANDIDATE SNAPSHOT |

Final Web supersession/merge decision belongs to the separate Web integration lane. Project Organization only provides the canonical object register for consumption.

### F / delivery
| PR | Role | Organization state |
|---|---|---|
| #114 | REV04 delivery/toolchain/current carriers | DELIVERY PROVENANCE / REEDIT |
| #111 | QJ-E remote digital materialization QA | EXECUTION / RUNTIME PROVENANCE |
| #96 | old digital runtime/Penpot candidate | PROCESS / LEGACY COMPATIBILITY PROVENANCE |

## C｜Project-restoration / governance-related C04 PRs

| PR | Role | Organization state |
|---|---|---|
| #138 | restore original design motherboard currentization | IMPORTANT DESIGN-SOURCE RESTORATION PROVENANCE / OPEN |
| #136 | global no-loss Control Plane deepening | GOVERNANCE CANDIDATE; not a C04 design object |

#138 is relevant to Design Source lineage but does not replace the permanent `C04_DESIGN_INVARIANTS` already merged on main.

## D｜Training / Skill PRs — explicitly excluded from C04 asset authority

Examples currently open: #146, #150, #154, #157, #158, #161, #166, #167, #168.

Organization state: `TRAINING / METHOD PROVENANCE ONLY` unless a separate explicit C04 transfer binds a result to a canonical object ID.

The presence of C04-like sample content in a training artifact is not enough to enter the C04 Asset Atlas.

## E｜Cleanup actions — no automatic destructive operations

Recommended project-hygiene actions, to be executed only after owner review:
1. Add `SUPERSEDED CANDIDATE` note to older same-object PRs where the lineage is unambiguous.
2. Keep open PRs that still contain unique recoverable design/proof until their unique material is safely indexed.
3. Never close/delete a PR merely to make the repository look cleaner.
4. Never merge a candidate solely to simplify lineage.
5. When a candidate is selected, update canonical object register first, then downstream Web/F consumers.
