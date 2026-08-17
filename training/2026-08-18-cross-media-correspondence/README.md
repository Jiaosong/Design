# OLEANDER Training — Cross-media Correspondence

## Training question
How can plan, section, axon/model, and later render views remain recognisable as views of the same design object without forcing identical projection or graphic style?

## Existing-first
This round reuses `oleander-3d-pipeline` as the owner of authoritative model / axon / handoff logic. No parallel Skill is created.

Project trigger: current C04 delivery requires plans, sections, models and renderings to agree. Recent reviews have repeatedly rejected polished derivative views when the spatial relation itself could not be read or verified.

## Practice
Synthetic relational geometry only; no C04 site geometry or field claim.

Stable anchors:

`A_ENTRY → B_JUNCTION → C_R06 → D_RETURN`

### v1 — REJECT
Plan, section and axon carry the same labels, but the section and axon locally redraw anchor positions/order. The labels imply sameness while the geometry contradicts it.

Failure knowledge: **shared IDs do not prove correspondence if adjacency/order/role drift.**

### v2 — REVISE
Shared anchors and order are repaired, but the invariant-vs-reprojectable contract remains implicit and labels are too tight for reliable near-read.

### v3 — KEEP FOR TRAINING
The set now explicitly separates:

- invariant: anchor identity, order, adjacency, role;
- may change: projection, camera, crop, local silhouette, graphic style.

The correspondence rail allows a reviewer to follow the same relation across plan / section / axon without captions doing all the work.

## Design Crit
- first visual: PASS for training; three media read as one comparison set;
- composition: PASS; equal panel weights are intentional because the question is correspondence, not hero hierarchy;
- proportion / hierarchy: PASS; stable anchors are primary review objects;
- typography: PASS after v3 repair; support labels remain subordinate;
- spatial realism: relational only; exact geometry / field scale NOT PROVEN;
- scale: NTS / FIELD OPEN;
- node readability: PASS;
- interaction: N/A;
- narrative: PASS — one design claim translated through three media;
- professional finish: KEEP FOR TRAINING.

## Reusable rule

`SOURCE AUTHORITY → SHARED ANCHORS → INVARIANTS → MEDIA TRANSLATION → SIDE-BY-SIDE READ → MEDIUM-SPECIFIC CRIT`

A model/render may be visually strong and still fail if it depicts a different relation from the plan or section.

## Transfer
Applicable to architectural/landscape plans, sections, axonometrics, 3D models, renders, route sequences, product exploded views and assembly/details.

Not a substitute for survey, field validation, engineering geometry, or project Design PASS.
