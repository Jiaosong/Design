# C04 / C22 v3.2 — Skill Retro Review + Rebuild Record

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Current delta: `DRW-C04-C22-01` + `DRW-C04-C22-05`  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`

## 0. Skill routing

Closest repository Skill: `oleander-technical-drawing` in PR #172.

It is the closest semantic match for technical drawing, spatial/landscape drawing, circulation analysis, diagram-to-professional-sheet currentization, TD-G0…TD-G8, source authority, and 3S/30S/near-read review.

Status: `CANDIDATE / DRAFT / NOT MERGED / NOT PROMOTED`.
Therefore it is used here as a strict calibration/gap detector, not as merged Current Authority. C04 Current Authority and installed OLEANDER rules remain binding.

Applied modules/rules:
- `DISCIPLINE_PROFILES` → Landscape/Site + Spatial Analysis + Circulation;
- `GRAPHIC_SYSTEM` → primary drawing field + annotation/evidence rail + metadata rail;
- `ANALYSIS_DRAWING_SYSTEM` → source / evidence / inference / decision / open-state separation;
- `FLOW_DIRECTION_ANALYSIS` → flow carrier must be source-bound; no decorative topology;
- `DETAIL_DENSITY_CALIBRATION` → relation proof, not fake line/detail count;
- `DRAWING_EXECUTION_TEMPLATE` → Drawing Brief / Authority Matrix / View Set / TD-G0…G8.

## 1. v3.1 retro verdict

### DRW-C04-C22-01 v3.1
`REVISE / SUPERSEDED`

Highest-order blocker:
- the candidate manually redrew the south-bank network instead of binding currentization to the strongest existing C22 vector relation source;
- this creates avoidable topology-drift risk;
- cleaner composition cannot override source-authority / geometry-coherence loss.

Mapped gates:
- `TD-G1 SOURCE AUTHORITY` → blocker;
- `TD-G2 GEOMETRY / NETWORK COHERENCE` → blocker;
- `TD-G5 DESIGN QUALITY` → improved appearance cannot compensate for G1/G2.

Repair in v3.2:
- exact path `d` carriers recovered from the existing C22 v3.0 vector page are reused;
- one uniform presentation transform only: `translate(20 135) scale(0.70)`;
- labels/rails do not redefine source geometry.

### DRW-C04-C22-05 v3.1
`REVISE / SUPERSEDED`

Highest-order blockers:
- three equal horizontal strips behave as an explanatory board, not a deliberate section hierarchy;
- SEC-B received equal compositional status although R06 is frozen/finished;
- source section geometry was visually re-authored rather than explicitly retained where useful;
- no controlled annotation/evidence rail separated drawing relation from truth-state support.

Mapped gates:
- `TD-G2` → source/view coherence weak;
- `TD-G5` → equal-strip hierarchy weak at 3S/30S;
- `GRAPHIC_SYSTEM` → no dominant field / rail structure.

Repair in v3.2:
- SEC-A + SEC-C occupy the primary drawing field;
- SEC-B becomes a low-contrast frozen-provenance inset;
- existing SEC-A/SEC-C vector profile carriers are reused;
- public cable figures are detached from drawing scale;
- FIELD OPEN conditions are isolated in the evidence rail.

## 2. Drawing brief / authority matrix

| item | C22-01 | C22-05 |
|---|---|---|
| discipline | Landscape/Site + Spatial Analysis + Circulation | Landscape/Site + Spatial Analysis |
| status | TECHNICAL EXPLANATION | TECHNICAL EXPLANATION |
| primary decision | show two-bank + cable + south-bank multi-branch relation without making Rxx route authority | show Transport/View + frozen R06 context + R13 compression/release without measured-section claims |
| geometry authority | existing C22 v3.0 vector relation page | existing C22 v3.0 vector section page |
| field truth | NOT SURVEY / NOT GEOREFERENCED | NTS / FIELD OPEN |
| prohibited claim | exact coordinates/distance/slope/time/capacity/live state | surveyed terrain/cable structure/R13 width-height/safety |

Authority notes:
- two-bank + cable + south-bank network = evidence-bound macro relation only;
- Rxx = canonical content identities, not route authority;
- R06 = `FROZEN / FINISHED / CONTEXT ONLY / NO REOPEN`;
- 1056 m and `ΔH≈156 m` = existing C22 public-reference facts only, not a section scale or surveyed profile;
- R13 compression/release = design reading; exact geometry/surface/slip/guard/capacity remains FIELD OPEN.

## 3. v3.2 view set

| view_id | type | role |
|---|---|---|
| C22-01-MASTER | relational plan | primary two-bank/cable/network field |
| C22-01-RAIL | evidence rail | authority + semantics + does-not-prove |
| C22-SEC-A | relational section | Transport + View primary section |
| C22-SEC-B-FROZEN | support inset | preserve R06 lineage only |
| C22-SEC-C | relational section | Approach → Compression → Release/Return |
| C22-05-RAIL | evidence rail | reference vs FIELD OPEN separation |

## 4. Flow-network register

Created: `C22_01_FLOW_NETWORK_REGISTER_v3_2.json`.

It records exact recovered C22 source path indices and a SHA-256 per path carrier. Current claim is intentionally bounded:

`FN-C0 NETWORK IDENTIFIED / partial FN-C1 carrier preservation`.

No FN-C2/FN-C3, geographic, survey or route-planning claim is made. Named Rxx labels are project-identity bindings; unlabeled branch-junction semantics are not invented.

## 5. Graphic system / multi-scale readback

### C22-01 v3.2
- 3S: river + cable + south-bank network remains identifiable in the 421×297 far-read derivative.
- 30S: arrival/service → cable → branching walk → Return can be traced without reading the full rail.
- near read: source-derived vs FIELD OPEN / does-not-prove language remains visible.
- no rounded-card wall and no new decorative terrain geometry.

### C22-05 v3.2
- 3S: SEC-A and SEC-C dominate; frozen SEC-B no longer competes.
- 30S: Transport/View and Compression/Release read as distinct technical relationships.
- near read: 1056 m / `ΔH≈156 m` remain reference-only; R13 width/height/surface/slip/guard/capacity remains FIELD VERIFY.
- SEC-C deliberately remains relational; fake construction/detail density was not added.

## 6. TD-G0…TD-G8 producer evidence state

| gate | producer state | evidence / blocker |
|---|---|---|
| TD-G0 Intent & Status | SELF-CHECKED / no known blocker | TECHNICAL EXPLANATION, NTS and prohibited uses explicit |
| TD-G1 Source Authority | SELF-CHECKED / no known blocker | existing C22 vector carriers rebound in v3.2 |
| TD-G2 Geometry / Network Coherence | SELF-CHECKED / no known blocker | uniform source transforms; no manual network replacement |
| TD-G3 Dimensional Intent | SELF-CHECKED / no known blocker | only inherited public cable figures; reference-only / not scaled |
| TD-G4 Operational Logic | SELF-CHECKED / no known blocker for declared scope | Return visible; R06 frozen; no engineering closure implied |
| TD-G5 Design Quality | REVIEW PENDING | actual full-size + far-read derivatives reopened; producer cannot award KEEP |
| TD-G6 Vector / Annotation Integrity | SELF-CHECKED / no known blocker | SVG XML parse PASS; geometry/text remain vector |
| TD-G7 Output / Round-trip | SELF-CHECKED / no known blocker | Inkscape SVG→PNG render PASS; previews reopened |
| TD-G8 Independent Review / Promotion | PENDING | no producer KEEP / MAIN / Professional Finish claim |

## 7. Local artifact evidence

- `C04_C22_01_MACRO_NETWORK_MASTERPLAN_v3_2_SKILL_REBUILT.svg` — 11181 bytes — SHA256 `4c3801c3411d9bb266c8f3aa738ec2d1013f2d3b90ae092b70e34a7ae8e5cf61`
- `C04_C22_01_MACRO_NETWORK_MASTERPLAN_v3_2_PREVIEW.png` — 298329 bytes — SHA256 `fa83f8b14a437858a42691772b372cbce8a0942c9dc260ed29f5af61a266685b`
- `C04_C22_05_RELATIONAL_SECTIONS_v3_2_SKILL_REBUILT.svg` — 12022 bytes — SHA256 `1fecd8a9843cf8d4d69582d882fabc927305ea3fa9778f09230d42b942da4100`
- `C04_C22_05_RELATIONAL_SECTIONS_v3_2_PREVIEW.png` — 302472 bytes — SHA256 `5fee63cbb7187d3e3457166208c8d2caa3a176724101242c572bdbe624dc564e`
- `C22_01_FLOW_NETWORK_REGISTER_v3_2.json` — 5964 bytes — SHA256 `74d34ed64b9584e34c695b0c687d9de6b6f2927b71ac5add0f33fb20bc5694a4`

Additional readback:
- SVG XML parse: PASS;
- Inkscape render: PASS;
- full-size PNG reopened;
- 421×297 far-read derivatives generated/reopened;
- grayscale derivatives generated for color-independent hierarchy check.

These are producer/QC observations only, not independent Design KEEP.

## 8. Current production state

`v3.1 = REVISE / SUPERSEDED PROVENANCE`

`v3.2 = EXECUTED / SOURCE-REBOUND / SELF-CHECKED / INDEPENDENT DESIGN REVIEW PENDING`

No merge, Promotion, `PIXEL KEEP`, `MAIN KEEP`, `PROFESSIONAL FINISH PASS`, engineering approval or field approval is implied.
