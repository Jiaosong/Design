# OLEANDER Practice — Board Focal Hierarchy Without Information Loss

## Training question
How can a board keep all required information while avoiding the equal-grid/template effect that makes every asset compete for MAIN attention?

## Existing problem reused
Recent OLEANDER display work repeatedly exposed a gap between content completeness and portfolio-grade composition: landscape, relation diagram, node drawing and technical proof could all be present, yet equal-sized columns/cards made the page read like a template. This practice does not add content; it only changes visual weighting.

## Artifact
`board_focal_hierarchy_v2.svg` is a 1920×1080 editable vector calibration sheet using the same four information roles in two arrangements:

- A / Equal Grid — REJECT
- B / Focal Field — KEEP

The B version uses one dominant field, a relation bridge, a smaller near-read node, and a compressed but readable proof rail. No information role is deleted.

## Design Crit
### v1 — REVISE
- First visual gate: better than equal-grid, but node still read too close to a co-hero.
- Composition: relation card floated too independently from the dominant field.
- Proof rail: remained larger than necessary for its support role.

### v2 — KEEP / TRAINING ASSET
- First visual gate: PASS — landscape claim reads first.
- Composition: PASS — unequal visual masses establish a clear dominant/support rhythm.
- Proportion: PASS — hero > node > proof rail; support content remains visible.
- Hierarchy: PASS — relation bridges hero and proof rather than acting as a third main.
- Typography: PASS for calibration — neutral type does not compete with the composition variable.
- Material/spatial realism: N/A — abstract vector calibration only.
- Scale/node readability: PASS for near-read role; node is legible without becoming the page's focal point.
- Interaction: N/A.
- Narrative: PASS — landscape → relation → node/proof is visible without explanatory prose.
- Professional finish: KEEP for training, not a project deliverable.

## Failure knowledge
- Equal rectangles often create equal claims, even when the story says one item is primary.
- Adding a large technical panel to prove rigor can accidentally create a second hero.
- A 'clean grid' is not automatically a strong composition; excessive regularity can produce template feel.
- Hierarchy must not be created by deleting evidence. Use area, adjacency, overlap, whitespace, crop, line weight and type scale to redistribute attention while preserving content.
- Technical Proof may be visually subordinate, but it must remain readable and publicly present when the story depends on it.

## Transfer rule
Before polishing a board/page, assign each visible object one role: `DOMINANT FIELD`, `RELATION BRIDGE`, `NEAR-READ PROOF`, or `BACKGROUND/SUPPORT`. If two or more unrelated objects still behave as DOMINANT FIELD at first glance, REVISE before adding decoration.

## Boundary
This is an abstract calibration asset. It does not claim site accuracy, field verification, engineering validity or project-specific visual approval.
