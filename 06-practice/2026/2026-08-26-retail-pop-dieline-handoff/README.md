# 2026-08-26｜Retail POP / Print Production / L5｜Die-cut Handoff

Status: **CANDIDATE / REAL PROJECT APPLICATION EXECUTED / PHYSICAL SAMPLE HOLD**

## Design Type / Skill Target

- Primary Design Domain: Brand / Visual Communication
- Design Subtype / Output: Packaging & Retail POP / die-cut jump card
- Stage / Purpose: design development → prototype production handoff
- Viewer/User Task: consumer far-read claim; near-read brand/person/product; supplier executes the intended die-cut silhouette
- Skill Target: `marketing silhouette → production dieline`
- Design vs Engineering Boundary: vector structure and print handoff only; no material thickness, die tolerance, spring/adhesive construction, machine capability or physical durability claim

## Knowledge Status

**PARTIAL**.

Current OLEANDER Visual Communication knowledge already includes MEDIUM / PRODUCTION and Baojiajie project locks, but no active installed Skill defines a complete Retail POP die-cut execution path. A `DESIGN-TYPE KNOWLEDGE GAP` was registered in Notion K06 for later knowledge completion.

## Existing Skill / Method Reuse

- `FW-DESIGN-VISUAL-COMM-001`: content × task × medium × production
- Baojiajie Program: Logo/portrait source locks, retail POP workstream, claim/evidence boundary
- `oleander-delivery-qc`: only the release/readback separation, not the design technique itself

## Professional calibration

- Esko Packaging Prepress: dielines communicate cut/fold/glue; bleed extends artwork beyond the cut/trim boundary; safe area protects critical content.
- Esko ArtiosCAD: dedicated structural packaging/POP workflow links structural data with graphics and manufacturing.
- Adobe Illustrator / print production: bleed is artwork outside trim/crop; the required extent depends on the job/print provider.

These references calibrate execution concepts, not OLEANDER aesthetics or project-specific dimensions.

## Actual A/B exercise

Same claim family and same locked-asset roles.

### A / REJECT — Decorative cloud die

- irregular cloud outline is decorative rather than claim-derived;
- `100` appears visually prominent but does not structurally determine the die;
- portrait/logo zone has no predictable safe relation to the cut;
- supplier would have to reinterpret the structure.

### B / KEEP candidate — Structural Claim Silhouette

- ONE BOLD MOVE: `100` becomes the top structural crest;
- prototype finished envelope = 140 × 180 mm;
- working bleed = 3 mm, `VENDOR_CONFIRM`;
- working safe inset = 5 mm, `VENDOR_CONFIRM`;
- locked Logo/portrait remain source slots; if they conflict with the cut, layout changes, not source assets;
- `CUT / BLEED / SAFE / ARTWORK / LOCKED-ASSET SLOT` remain independently editable.

## Real project application

Applied to **BAOJIAJIE retail jump card / 欧科棉 direction** using the existing marketing structure:

- `欧科棉黑科技`
- `100天不发硬`
- locked Logo slot
- locked portrait slot
- product slot

No Logo or portrait was generated/redrawn. The practice changes only the die-cut structure and production-layer handoff.

## Visual / Functional readback

First rendered preview exposed a real finished-pixel defect: the production-parameter sentence in the B panel crossed into the right panel. The line was split/reflowed and the final PNG/Gray50 were re-rendered.

Final producer readback:

- first-read difference A/B is visible without reading the explanation;
- CUT-off: marketing hierarchy still reads;
- ARTWORK-off: B's cut path still carries the intended silhouette;
- Gray50: separation logic does not depend on color alone;
- physical die/sample, substrate, tolerance, adhesive/spring construction and supplier approval remain HOLD.

## Skill Record

- Problem: irregular visual concept does not reliably become supplier-executable dieline
- Trigger: Baojiajie jump-card iterations exposed weak die shape, insufficient jump-card character, protruding claim not integrated with structure
- Inputs: claim hierarchy, locked Logo/portrait authority, prototype envelope, supplier-confirm production variables
- Visible Symptoms: arbitrary lobes, narrow necks/acute concavities, unstable safe zone, source assets close to cut, CUT/Artwork mixed together
- Cause: silhouette driven by decorative irregularity instead of claim hierarchy + production handoff
- Technique: Structural Claim Silhouette + Production Layer Separation
- Operation Steps: claim mass → envelope → cut silhouette → safe inset → bleed → locked source slots → layer-off tests → vector/PDF export → supplier/sample proof
- Parameters or Conditions: 140×180 mm training envelope; 3 mm bleed / 5 mm safe are working values only
- Expected Result: claim recognition and cut silhouette align; source assets protected; converter can read intended structure without redesign
- Verification: ARTWORK-OFF / CUT-OFF / GRAY50 / pixel readback
- Failure Condition: artwork only works when CUT is visible; cut only makes sense because artwork is visible; or working production values are presented as universal facts
- Counterexample: rectangular non-die-cut screen or paper graphic does not require this gate
- Transfer Boundary: flat die-cut POP/hangtag/shelf-talker; not full folding-carton/corrugated/FSDU CAD
- Applicable Domains: Retail POP / Packaging / Hangtag / Shelf-talker / Event display
- Application Mapping: BAOJIAJIE jump card = executed candidate; cross-project validation pending
- Evidence Gate: VECTOR + PDF EXECUTED / SUPPLIER + PHYSICAL SAMPLE HOLD
- Design Quality Gate: producer readback complete; independent design verdict not established in this skill-training run
- Version: v0.1
- Status: CANDIDATE

## Artifact

- `OLEANDER_BJ_JUMPCARD_DIELINE_HANDOFF_R01.svg`

Local execution additionally produced a mm-based production SVG, print-PDF derivative, PNG and Gray50 readback. Binary derivatives are execution evidence but are not used to promote the Candidate.

## Truth boundary

`TRAINING / PROJECT APPLICATION EXECUTED / NO AI IMAGE / PROTOTYPE PRODUCTION PARAMETERS / SUPPLIER CONFIRM REQUIRED / PHYSICAL SAMPLE HOLD / STATUS=CANDIDATE`.
