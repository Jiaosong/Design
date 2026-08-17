# OLEANDER Training — Small-mark optical size

Status: `KEEP FOR TRAINING / PROJECT BRAND PASS NOT CLAIMED`

## Trigger

Current C04 Brand v1.0 independent review explicitly requires `24 / 32 / 48 / 96 px` behavior. Existing OLEANDER Story/Board rules preserve logo authority but did not distinguish mechanical scaling from size-specific optical compensation.

## Existing-first

- Reuse `oleander-story-and-board` as the owner.
- Do not create a parallel brand/logo Skill.
- Use the current C04 River Folio candidate structure only as a training object.
- Do not modify or promote the project logo source.

## External calibration

Apple SF Symbols guidance is used only for the transferable optical principle: symbols provide different scales/weights for context, and Apple notes that simply scaling a symbol changes perceived weight; optical weight compensation is used to keep small/large scales visually matched.

This does not imply that SF Symbols may be used as logos, nor that Apple symbol geometry is copied.

## Practice

`mark_master.svg` preserves the current candidate structure:
- primary valley/page stroke;
- river stroke;
- two low-opacity secondary traces;
- focal dot.

`mark_optical_small.svg` is a bounded training derivative for 24/32 px:
- preserves the identity skeleton and dominant silhouette;
- removes the two 38% secondary traces that become pixel chatter;
- increases main/river optical stroke weight;
- enlarges the focal dot;
- slightly shortens the far-right tail to reduce low-pixel chatter.

At 48/96 px the master is retained.

## Design Crit

- Mechanical 24 px: `REVISE` — secondary traces break into low-value raster noise and the mark reads optically light.
- Mechanical 32 px: `REVISE` — improved, but the same micro-detail is still weaker than the primary silhouette.
- Optical 24 px: `KEEP FOR TRAINING` — primary silhouette and focal relation survive with less noise.
- Optical 32 px: `KEEP FOR TRAINING` — hierarchy is clearer without creating a different mark.
- 48/96 px: master retained; no justification for a simplified variant.

## Failure knowledge

1. `vector scalable` does not mean `optically equivalent at every raster size`.
2. A small-size variant must preserve identity topology/silhouette; clarity is not permission to redesign the mark.
3. Faint detail that only exists at zoomed vector scale should not be forced into 24/32 px.
4. Do not rescue small-size weakness with glow, extra color, or blur.
5. Native-size raster is the recognition test; nearest-neighbor zoom is only a pixel diagnostic.

## Candidate transfer rule

`IDENTITY SKELETON → TARGET PIXEL SIZE → SURVIVING DETAIL → OPTICAL WEIGHT → RASTER REOPEN`

## Boundary

Training derivative only. No trademark approval, official-logo replacement, operator approval, field validation, or C04 Brand Design PASS is implied.
