# Technical SVG Lab｜Professional Review 01

Date: 2026-08-26
Surface: `browser_technical_svg_lab`
Review scope: finished exported SVG first; runtime/producer receipt read only after artifact judgment.
Verdict: **REVISE / RETEST REQUIRED / ACTIVE NOT GRANTED**

## Artifact reviewed
- `BAOJIAJIE_JUMPCARD_TECHNICAL_MASTER_VALIDATION.svg`
- Baojiajie retail jump-card / 欧科棉 direction

## First-read verdict
The artifact is functionally editable and the CUT/SAFE geometry is visible, but the sheet is **not yet a professional handoff/preflight surface**. The main graphic does not make the two highest-risk production states unmistakable: target-vs-actual size conflict and missing BLEED.

## Findings
### R01｜Critical｜Target vs actual geometry conflict is not graphically explicit enough
The sheet shows `ACTUAL CUT 136.0 mm` and `184.0 mm`, while the dashed target envelope is 140×180 mm, but the target dimensions are not separately dimensioned or called out as a mismatch. A viewer can read the dashed rectangle as an ordinary guide rather than a failed target check.

**Root Cause:** runtime treats target envelope as a quiet reference layer instead of a failure-state annotation when `GEOMETRY_MATCH=false`.

**Feedback Action:** when mismatch exists, add a visible `TARGET 140×180 / ACTUAL 136×184 / MISMATCH` block adjacent to the geometry and style the target envelope as an explicit comparison/error state, not a neutral construction line.

**Retest Evidence:** artifact-first read at full sheet and reduced preview must identify target, actual and mismatch without consulting the side-panel status or receipt.

### R02｜Critical｜BLEED missing state is hidden instead of drawn as OPEN
`BLEED` group exists but is empty. The sheet does not show `BLEED OPEN / PATH REQUIRED`; the only boundary warning is generic footer text. In a preflight context, an empty layer can be mistaken for intentionally disabled or non-required bleed.

**Root Cause:** missing custom path is represented by absence rather than an explicit graphic state.

**Feedback Action:** if custom BLEED is missing, render a non-print warning badge/leader outside the artwork: `BLEED PATH OPEN — SUPPLIER/CONVERTER INPUT REQUIRED`; keep the actual BLEED layer empty so no fake geometry is created.

**Retest Evidence:** exported SVG must retain empty `BLEED` production layer while the non-print notes layer visibly communicates the OPEN state.

### R03｜High｜No legend distinguishes production layers from reference/non-print layers
CUT red and SAFE green are visually different, but there is no compact legend for `CUT / SAFE / BLEED / TARGET REFERENCE / NONPRINT`. This is acceptable for internal debugging, not for a reusable cross-project technical preflight surface.

**Root Cause:** layer semantics exist in IDs/code but not in finished-sheet reading.

**Feedback Action:** add a small non-print legend with line samples and explicit statuses. The legend must not imply vendor approval.

### R04｜High｜SAFE is visible but unqualified
The SAFE path is source-supplied, but the finished sheet does not state its provenance/status near the legend. Because it visually resembles an authoritative offset, the reader can over-trust it.

**Root Cause:** source-state metadata remains in runtime status text instead of final artifact.

**Feedback Action:** legend/status block should state `SAFE: SUPPLIED / UNVERIFIED FOR PRODUCTION` (or equivalent bounded wording).

### R05｜Medium｜Sheet hierarchy is too sparse for handoff use
The sheet has geometry, dimensions and footer, but no document identity, revision, units block, source/status block, or project/object ID. The central `ARTWORK AREA` placeholder dominates more than the risk information.

**Root Cause:** artifact optimized as capability demo rather than production-facing preflight document.

**Feedback Action:** demote placeholder artwork label and add a compact title/status block: object ID, units, revision, target size, actual bbox, CUT/SAFE/BLEED states, vendor-confirm status.

## What is already acceptable
- CUT source geometry is preserved rather than non-uniformly stretched.
- SAFE and BLEED are separate path concepts; missing BLEED is not fabricated.
- Actual CUT dimensions are present.
- Layer IDs are editable (`CUT`, `SAFE`, `BLEED`, `ARTWORK`, `DIMENSIONS`, `NONPRINT_NOTES`).
- `CONCEPT / NTS / NOT FOR PRODUCTION APPROVAL` boundary is visible.

These are necessary but do not offset the handoff-readability failures above.

## Decision
`REVISE`.

Do **not** promote Technical SVG Lab to ACTIVE. Functional browser PASS remains valid, but Professional Design/Handoff PASS is withheld. Required next transaction:

`R01–R05 repair → actual browser/export readback → artifact-first retest → then reconsider ACTIVE`.

Supplier/converter proof, physical sample, print tolerance and production approval remain separate OPEN/HOLD gates.