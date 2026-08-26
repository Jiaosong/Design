# oleander-print-production

Status: **CANDIDATE v0.2**

Scope: print-production execution for editable brand/graphic outputs where a visual silhouette must become a real structural/print handoff. This Candidate is intentionally narrow: **die-cut Retail POP / jump card / shelf-talker / hangtag**. It is not a general packaging-CAD or aesthetic-composition Skill.

## Design Type Gate

- Primary domain: Brand / Visual Communication
- Subtype: Packaging & Retail POP / die-cut promotional carrier
- Stage: design development → prototype production handoff
- Viewer task: far-read claim, near-read brand/product, supplier executes intended cut silhouette
- Skill target: `marketing silhouette → production dieline`
- Design vs Engineering boundary: controls vector structure and print handoff; does not certify substrate, die tolerance, adhesive/spring construction, machine capability, structural durability or physical approval.

## Knowledge Status

Current OLEANDER Knowledge = **PARTIAL** for this subtype. `FW-DESIGN-VISUAL-COMM-001` covers MEDIUM/PRODUCTION and project Brand Authority, but no active installed Skill currently supplies a complete die-cut POP execution path. The corresponding DESIGN-TYPE KNOWLEDGE GAP is tracked in Notion K06. This file is therefore a Candidate, not an installed/ACTIVE authority.

## Inputs

Required before drawing:

1. claim hierarchy and first-read object;
2. finished envelope or bounded prototype size;
3. locked brand/logo/portrait/product assets and their source authority;
4. substrate / supplier / finishing information if available;
5. vendor-required bleed, safe-zone, cut/crease conventions if available;
6. whether the carrier is flat die-cut only or includes fold/crease/glue/spring/adhesive structure.

If supplier values are unknown, working values may be used only when explicitly labeled `VENDOR_CONFIRM`; do not promote them as universal production standards.

## Core technique

`CLAIM MASS → FINISHED ENVELOPE → STRUCTURAL SILHOUETTE → CUT → SAFE → BLEED → LOCKED-ASSET SLOT → ARTWORK → HIDE-LAYER TESTS → VECTOR/PDF EXPORT → SUPPLIER/SAMPLE PROOF`

### 1. Structural Claim Silhouette

One bold recognition move may become part of the cut silhouette when it remains mechanically plausible and does not create fragile necks, accidental spikes or asset collisions. A marketing word/number that only appears to protrude inside a decorative cloud does not count.

### 2. Production Layer Separation

Keep these independently editable:

- `CUT_DIE` — structural cut path only;
- `CREASE/FOLD` — only when actually present;
- `BLEED_WORKING` — artwork extension, not a structural line;
- `SAFE_WORKING` — critical-content keep-in zone;
- `ARTWORK` — marketing graphic/text/image content;
- `LOCKED_ASSET_SLOT` — source-bound Logo/portrait/product placement boundary;
- `NONPRINT_NOTES` — production notes, version, truth boundary.

Artwork must not be baked into the die line. The die line must not be used as a visual crutch to make a weak artwork hierarchy readable.

## Operation steps

1. Draw the finished envelope in real units.
2. Convert the primary claim mass into one intentional silhouette move; keep secondary edges calmer.
3. Inspect neck width, acute concavities, isolated tabs and narrow protrusions. If manufacturing limits are unknown, mark them for supplier proof rather than inventing a universal tolerance.
4. Draw `CUT_DIE` as one coherent closed path for a flat die-cut piece.
5. Create `SAFE_WORKING` inward from the cut; keep critical copy, Logo and portrait inside it. Working inset must carry `VENDOR_CONFIRM` unless supplier authority is already known.
6. Extend full-bleed artwork beyond cut using `BLEED_WORKING`; final value follows printer/converter authority.
7. Place locked source assets as slots first; replace placeholders only with authoritative bytes. If a locked asset conflicts with cut/safe, change composition, not the source asset.
8. Execute `ARTWORK-OFF`, `CUT-OFF`, `GRAY50`, and target-size readback.
9. Export editable vector plus print PDF derivative. Keep spot/structural semantics separable for the converter.
10. Physical proof remains mandatory before production approval.

## Parameters / conditions

- Use real document units (`mm` for print carrier unless supplier specifies otherwise).
- Bleed and safe-zone values are job/vendor dependent. A prototype may use explicit working values, but must say `VENDOR_CONFIRM`.
- Cut/fold/glue semantics follow converter conventions. For complex cartons/displays, route to structural CAD/ArtiosCAD-class workflow rather than improvising in a flat artwork Skill.
- Final output should preserve Trim/Cut intent and bleed information in the production PDF/vector handoff.

## Required A/B test

Use the same claim/assets.

- A: decorative irregular silhouette with no structural relationship to claim.
- B: one claim-derived structural silhouette move with separated production layers.

The comparison is invalid if typography, product, portrait and overall hierarchy all change at once.

## Verification

### ARTWORK-OFF
Hide `ARTWORK`. `CUT_DIE` must still describe the intended physical silhouette and remain a coherent structural path.

### CUT-OFF
Hide `CUT_DIE`. Marketing hierarchy must still read correctly; artwork cannot depend on a visible die line to make sense.

### LOCKED-ASSET SAFE
Logo/portrait/product source slots must remain inside the approved critical-content zone. If not, revise layout.

### GRAY50 / COLOR-OFF
Structural hierarchy and first-read cannot collapse merely because production colors are removed.

### TARGET-SIZE
Inspect at intended print size, not only enlarged artboard view.

### SUPPLIER PROOF
Physical/supplier review must confirm substrate, knife/crease capability, tolerances, bleed, safe area, finishing and attachment. This is separate from design Skill execution.

## Retail viewing-distance hierarchy extension

Use this extension only when the carrier has a real consumer viewing sequence such as aisle approach → claim recognition → near-read brand/product proof. It does **not** replace the dieline gate above.

### Objective

Separate information by **decision distance**, not by arbitrary font tiers:

`FAR READ / CLAIM → MID READ / CLAIM + TECHNOLOGY → NEAR READ / BRAND + PORTRAIT + PRODUCT + SUPPORT PROOF`

The far-read layer must answer one commercial question quickly. Near-read evidence remains present; it is deferred, not deleted.

### Inputs

- finished physical size in real units;
- intended installation height/orientation if known;
- plausible far/mid/near viewing distances or an explicit `FIELD/RETAIL TEST OPEN` range;
- primary claim and supporting claim;
- locked Logo / portrait / product source slots;
- actual retail context when available: shelf depth, aisle width, neighboring clutter, glare, lighting, mounting angle.

Do not invent a universal distance standard when the retail context is unknown.

### Operation

1. Keep dieline, palette and asset slots fixed for the A/B whenever possible.
2. Identify one far-read claim carrier. Increase its visual mass before adding more decoration.
3. Reduce secondary objects to near-read roles without deleting them.
4. Test at physical target size and at distance-scaled previews; distance-scaled screen previews are **diagnostic only**.
5. Print a 1:1 mock-up and inspect in a real or reasonably reconstructed shelf/aisle context before claiming retail validation.
6. If the far-read claim depends on hue alone, repeat in grayscale/color-off.
7. If the near-read layer becomes too weak to identify brand/product or verify the claim, revise; distance hierarchy is not permission to erase evidence.

### Required A/B

Hold constant:

- finished envelope / cut silhouette;
- palette;
- source asset slots;
- claim wording;
- product/portrait/logo identity.

Primary variable:

- **claim mass + information release by distance**.

At least one `ONE BOLD MOVE` must shift the first-read hierarchy rather than apply many small refinements.

### Distance readback

Use at least three explicit states:

- `NEAR` — detail/evidence recoverability;
- `MID` — claim + one supporting reason;
- `FAR` — first commercial claim only.

A screen simulation may scale the finished carrier by visual angle, but it is not a substitute for a printed 1:1 mock-up. Record the simulation method and keep `PHYSICAL RETAIL READBACK = OPEN` until printed/context proof exists.

### Attack tests

- `FAR-READ` — at the far diagnostic scale, what remains readable first?
- `MID-READ` — can the supporting technology/reason appear without competing with the claim?
- `NEAR-READ` — are Logo / portrait / product / proof still recoverable?
- `GRAY50` — does first-read survive without brand hue?
- `CLUTTER` — does neighboring visual noise destroy the claim hierarchy?
- `LOCKED-ASSET` — did hierarchy repair distort or redraw protected assets?
- `PRINT-1:1` — has the actual-size print been inspected?

### Hard failures

- every object receives equal visual weight because all content must be present;
- far-read is “solved” by deleting product/brand/proof rather than deferring it;
- screen zoom or thumbnail is reported as physical retail validation;
- large type is used without a specific first-decision purpose;
- portrait or Logo is enlarged until it competes with the commercial claim without a documented brief reason;
- the design only works because of brand color and collapses in grayscale;
- a generic distance number is treated as a universal retail standard.

### Promotion test

`At the intended physical size, the far read must expose one claim, the mid read may add one reason, and the near read must recover brand/product/proof without changing or deleting locked source assets.`

Physical shelf/aisle readback is required before this extension can support `VALIDATED` status.

## Failure symptoms

- arbitrary cloud/starburst die used only to look irregular;
- protruding headline does not actually change the cut silhouette;
- fragile spikes/narrow necks/acute internal notches have no production justification;
- locked Logo/portrait is intersected by cut/safe zones;
- CUT and ARTWORK are flattened into one inseparable graphic layer;
- working bleed/safe values are stated as universal facts;
- printer/converter must redraw the structure to infer design intent;
- a complex folded/glued display is treated as a simple flat die-cut because Illustrator/SVG is convenient.

## Counterexamples / transfer boundary

Applicable:
- flat die-cut jump cards;
- shelf-talkers and retail POP cards;
- hangtags and irregular promotional cards;
- packaging add-on cards and simple display faces.

Not sufficient:
- folding cartons with full crease/glue/fold sequence;
- corrugated/FSDU structural displays;
- rigid multi-component POP;
- inserts requiring product fit calculations;
- engineering/manufacturing validation;
- pure screen graphics with no physical cut.

Those require structural packaging CAD / converter-specific production methods.

## Professional calibration sources

- Esko Packaging Prepress: dielines communicate cut/fold/glue; bleed extends artwork beyond trim/cut; safe area protects critical content.
- Esko ArtiosCAD: structural packaging/POP uses dedicated 2D/3D structural design and manufacturing workflows; graphics integrate with structural data.
- Adobe Illustrator / Print Production: bleed is artwork outside the trim/printing bound and its required extent depends on the job/print provider.
- SEGD wayfinding practice: information and viewing distance affect graphic size and sign build; retail/physical-environment legibility must be checked in the actual context rather than inferred from a studio artboard.

These sources calibrate production and viewing-context concepts only; they do not supply OLEANDER aesthetics or project-specific dimensions.

## Skill Record contract

Record every run as:

`Problem / Trigger / Inputs / Visible Symptoms / Cause / Technique / Operation Steps / Parameters or Conditions / Expected Result / Verification / Failure Condition / Counterexample / Transfer Boundary / Applicable Domains / Application Mapping / Evidence Gate / Design Quality Gate / Version / Status`

State path: `OBSERVATION → CANDIDATE → VALIDATED → ACTIVE → DEPRECATED/SUPERSEDED`.

This file remains **CANDIDATE**. The die-cut handoff has one real project application; the viewing-distance extension has diagnostic vector/raster proof but no printed shelf/aisle validation or cross-project validation yet.
