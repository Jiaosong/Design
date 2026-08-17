# Independent Design Review Request — Technical Drawing Golden Fixtures / Detail Density Rev C

Status: `REVIEW PENDING`  
Producer is not authorized to assign KEEP-class verdicts.

## Review authority

Use together:

- `00-governance/OLEANDER_INDEPENDENT_DESIGN_VERDICT_POLICY_v1.0.md`
- `00-governance/artifact-review-system-v1.0.md`
- `oleander-skills/oleander-technical-drawing/SKILL.md`
- `oleander-skills/oleander-technical-drawing/references/GRAPHIC_SYSTEM.md`
- `oleander-skills/oleander-technical-drawing/references/DETAIL_DENSITY_CALIBRATION.md`
- `oleander-skills/oleander-technical-drawing/references/REALITY_CHECK.md`

Do not review from this note alone. Reopen the actual SVGs at 1800×1200 and inspect them at three reading conditions.

## Artifacts to reopen

- `GD-01_ARCH_SECTION.svg` — Rev C
- `GD-02_LANDSCAPE_NODE.svg` — Rev C
- `GD-03_PRODUCT_ASSEMBLY_CMF.svg` — Rev C
- `GD-04_CONNECTION_FOUNDATION.svg` — Rev C

GD-05/GD-06 remain visual-hierarchy/analysis fixtures and are outside this density-specific review scope unless a regression is observed.

## Review sequence

Review each drawing in this order:

`3S FIRST READ → 30S SYSTEM READ → NEAR-READ TECHNICAL DEPTH → TRUTH BOUNDARY → PROFESSIONAL FINISH`.

Do not average a first-read failure with strong near-read detail, or a truth failure with visual polish.

## 1. 3-second first-read veto

For each fixture, determine without reading the footer:

- GD-01: does `CUT → LEVEL → INTERFACE` read before notes/dimensions?
- GD-02: does `PATH → SUPPORT → WATER → EDGE` read as one node system?
- GD-03: does assembly order/axis remain dominant before CMF and interface detail?
- GD-04: does member → plate → anchor → substrate read as one continuous connection chain?

Automatic REVISE if professional-density additions turned the sheet back into equal visual noise.

## 2. 30-second system read

Check whether the main technical chain is recoverable from geometry alone plus short labels:

- parent → child detail ownership;
- controlling dimension/datum logic;
- material/build-up/component identity;
- connection/fixing interface;
- drainage/environment/serviceability where applicable;
- explicit unresolved closure.

A reviewer should not need long explanatory prose to reconstruct the system.

## 3. Near-read D0–D6 depth

Use `DETAIL_DENSITY_CALIBRATION.md` as the diagnostic.

### GD-01 / Architecture
Expected depth:
- D0 identity/status;
- D1 section cut + levels;
- D2 controlling span/opening + datum;
- D3 material/finish layers;
- D4 bracket + joint interface;
- D6 engineer/system verify.

Check specifically:
- level symbols and dimension bands are subordinate but immediately traceable;
- material IDs point to actual spatial layers;
- D-02 bracket/joint is graphically present rather than only named;
- no unsupported fire/thermal/waterproofing performance appears.

### GD-02 / Landscape
Expected depth:
- D0 identity/status;
- D1 path/support/water/edge;
- D2 training width/crossfall;
- D3 surface/support build-up;
- D4 local support/outlet interface;
- D5 drainage + maintenance + safety relation;
- D6 FIELD/engineer verify.

Check specifically:
- surface and sub-support are visually separate;
- drainage has direction + outlet + receiving-condition boundary;
- maintenance access is a drawn envelope/path, not prose;
- footing/subgrade/outlet uncertainty does not look resolved.

### GD-03 / Product
Expected depth:
- D0 identity/status;
- D1 assembly sequence;
- D2 datum/fit/service clearance;
- D3 interface stack + CMF state;
- D4 fixing axis;
- D5 removal/tool path;
- D6 fastener/tolerance authority open.

Check specifically:
- DATUM A/B are useful rather than decorative;
- 3.0 gap belongs to the mating detail, not the exploded spacing;
- fixing axis is graphically located but does not masquerade as a released fastener spec;
- service path is physically legible;
- CMF candidate/reference/TBD states remain visually distinct.

### GD-04 / Connection + Foundation
Expected depth:
- D0 identity/status;
- D1 load/connection chain;
- D2 synthetic training envelopes only;
- D3 isolation/contact layers;
- D4 anchor interface;
- D5 water/corrosion/access;
- D6 engineering/field closure.

Check specifically:
- member → isolation → plate → anchor → substrate is actually drawn;
- the load path does not imply structural calculation/approval;
- anchor diameter/embedment/edge distance/reinforcement/foundation depth are not invented;
- water/corrosion/access relations are graphical;
- FIELD/engineer-open state remains visible at near-read and cannot be mistaken for final construction detail.

## 4. Evidence-artifact test

For every technical assertion ask:

`IS THE RELATIONSHIP DRAWN, OR IS IT ONLY WRITTEN?`

REVISE examples:
- `drainage` with no arrow/outlet;
- `removable` with no removal path;
- `bracket` with no interface geometry;
- `anchor` with no anchor/plate/substrate relation;
- `CMF boundary` with no visible layer boundary;
- `FIELD OPEN` footer while the geometry looks final/resolved.

## 5. Density quality

Professional detail density must be **localized**.

Check:
- primary field remains lower-density than detail rail;
- highest density occurs at decision interfaces;
- dimension/annotation bands align rather than forming halos;
- whitespace still protects parent/detail hierarchy;
- no text has been shrunk below intended-size readability to preserve excess information;
- there is no decorative hatch/fastener/dimension whose removal would not weaken technical understanding.

## 6. Truth / promotion boundary

All four fixtures use synthetic training geometry. Exact synthetic values calibrate drawing hierarchy only.

The reviewer must reject any interpretation that treats these values as:
- project recommendations;
- field measurements;
- structural adequacy;
- code compliance;
- fabrication tolerance;
- construction approval.

`DETAIL DEPTH PASS != ENGINEERING PASS != FIELD PASS != CONSTRUCTION/FABRICATION RELEASE`.

## 7. Allowed independent verdicts

Per fixture, record one of:

- `PROFESSIONAL DETAIL DEPTH KEEP CANDIDATE`
- `SUPPORT`
- `REVISE`
- `REJECT`
- `HOLD`

KEEP-class / Golden promotion still requires all current OLEANDER promotion conditions. Structure validator, SVG validity, CI, file existence and producer notes cannot establish KEEP.

## 8. Required review output

For each fixture provide:

- 3S verdict;
- 30S verdict;
- near-read D0–D6 findings;
- graphical-proof gaps;
- over-density/noise removals;
- truth-boundary issues;
- concrete repair instructions for each Major/Critical finding;
- independent artifact verdict.
