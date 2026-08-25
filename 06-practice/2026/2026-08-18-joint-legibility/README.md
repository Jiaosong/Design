# 2026-08-18 Architectural Detail — Joint Legibility

Status: **CANDIDATE / project validation pending**

## Learning object
Carlo Scarpa / Museo di Castelvecchio restoration and museum installation, 1958–1974. The official Carlo Scarpa Archive preserves drawings, photographs, surveys and construction records for the project.

## Visible Fact
Masonry, concrete, metal and timber remain visually differentiated at interfaces rather than being flattened into one continuous surface language.

## Design Inference
A professional detail becomes readable when component identity and the way components meet are established before lineweight and annotations are added.

## Transfer Rule
`COMPONENT IDENTITY → JOINT / REVEAL / SETBACK / TERMINATION → LINE HIERARCHY → NOTE`

## Existing-first
No new reusable Skill is created. This round reuses existing OLEANDER technical/presentation logic and the Universal Production Environment. The change is a bounded practice artifact and review rule candidate.

## Real practice
A/B uses the same generic component stack.
- A: every edge receives heavy outline treatment; the critical interface remains ambiguous.
- B: component identities are separated first, then reveal / setback / termination conditions receive explicit hierarchy; line roles reduce to CUT / JOINT / EDGE / NOTE.

## Readback
- editable SVG: executed;
- CairoSVG: `NATIVE_AVAILABLE`;
- 1600×1000 near-read: executed;
- v1: `REVISE` because the transfer strip and B heading overflowed;
- v2: repaired and reopened;
- 480×300 distance-read: executed;
- training artifact: `POST-READBACK PASS`.

## Counterexample
A dense CAD-like node with complete outlines and many annotations may look technical while still failing to reveal which connection controls assembly, drainage, movement, maintenance or replacement.

## Transfer Boundary
Do not copy Castelvecchio construction details into another project. Do not invent joint width, fastener, substrate, structural capacity or material build-up. Transfer only the hierarchy principle.

## C04 mapping
C04 R06 technical communication only. `R06 DESIGN REMAINS FROZEN`. No new route, platform, railing, dimension or structural claim is introduced. `NTS / FIELD OPEN / NO_PROMOTION`.

## Gates
- Evidence Gate: **PASS** for precedent identity, OLEANDER routing and bounded transfer.
- Design Quality Gate: **POST-READBACK PASS FOR TRAINING ARTIFACT ONLY**.
- Reusable Skill status: **CANDIDATE**, not VALIDATED/ACTIVE.

## Review question
**In grayscale, can reveal, setback, termination and line hierarchy still tell what is primary, attached and critical?**

## Artifact
- `OLEANDER_C04_JOINT_HIERARCHY_AB_20260818.svg`
- SVG SHA256: `eaabbcaad02c5349e536c7063ca192181f2a1c41d2c94c40c590e4fe0c3f7acd`
