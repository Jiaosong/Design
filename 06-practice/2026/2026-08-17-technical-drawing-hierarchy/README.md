# OLEANDER Training｜Technical Drawing Hierarchy

Training ID: `OLEANDER-TRN-2026-08-17-TDH`

## Why this training exists
Recent C04/Qingjiang review repeatedly showed a quality gap between technically present information and professional drawing readability: section/node content can exist while lineweight, annotation, human scale, connection detail and maintenance behavior compete at the same visual level. The target is not to add more geometry or dimensions; it is to make existing technical content read in a disciplined sequence.

Repository duplicate check found no existing reusable training dedicated to `lineweight hierarchy / annotation hierarchy / technical drawing first-read`, so this is a material delta rather than a repeat of the previous negative-space or source-independent visual-QA exercises.

## External professional anchor
- ISO 128-1:2020: general principles for execution of technical drawings across construction, architecture and related fields.
- ISO 128-2:2022: conventions for line types, draughting of lines, leaders and reference lines.

The exercise uses those standards only as a general conventions anchor. It does not claim full ISO conformance and does not invent construction dimensions.

## Practice artifact
`technical_drawing_hierarchy_calibration.svg` is an editable 1800×1200 vector calibration sheet with:
- section first-read;
- node near-read;
- four visual stroke levels;
- human scale;
- explicit leader targets;
- maintenance-action support notation;
- NTS / FIELD OPEN / no-construction-claim boundaries.

Independent CairoSVG render used for visual review. Local v2 render SHA256: `b61f23769043a9d69ca5c11e57d27d46eed5037db769ec5b07bcd1a0a8e21826`.

## Design Crit
Initial render: `REVISE`.
- relation-dimension note sat too close to the primary path and competed with structure;
- foundation callout was too close to the node boundary.

Repair cycle:
- moved dimension note into clear negative space;
- moved foundation leader/text away from the main geometry.

Final v2 verdict: `KEEP / TRAINING ASSET`.

### Final checks
- First visual gate: PASS — cut/primary path read before annotation.
- Composition: PASS — section dominates; node remains secondary but legible.
- Proportion: PASS — line hierarchy remains separated at board scale.
- Typography: PASS — neutral annotation system, no decorative type competition.
- Scale: PASS WITH BOUNDARY — human figures communicate relative scale only.
- Node readability: PASS — connection targets are explicit.
- Material/engineering reality: HOLD BY DESIGN — this is a hierarchy calibration, not a construction detail; bolt/foundation sizing is intentionally non-prescriptive.
- Professional completion: KEEP for training and board/drawing calibration.

## Failure knowledge
Do not solve technical drawing readability by adding more notes, dimensions or linework. When primary form, structure, edge/safety, and annotation use similar graphic weight, the drawing becomes informationally dense but professionally weak.

Mandatory correction order:
`PRIMARY FORM → STRUCTURE / RELATION → EDGE / CONNECTION → DIMENSION / NOTE`

If a note competes with the object it describes, move/reduce the note before adding graphic emphasis to the object.

## Transfer
Applicable to spatial sections, elevations, axons, node drawings, assembly diagrams, product exploded views, maintenance diagrams and board technical figures.

Not sufficient for structural design approval, code compliance, verified construction dimensions, field-measured geometry, fabrication tolerances or engineering sign-off.
