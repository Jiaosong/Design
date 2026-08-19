# SURFACE PATCH ASSEMBLY PROTOCOL

Status: reusable OLEANDER 3D Skill extension.

## Principle
Automotive/product/architectural surfaces often need multiple semantic patches. Object count is not a continuity metric.

`One object ≠ one continuous surface`
`Multiple objects ≠ discontinuous form`

What matters is explicit boundary ownership, shared anchors / boundary rails, gap evidence and final visual/reflection continuity.

## Trigger
Use when the final visible shell is intentionally decomposed into lower body / roof / pillar / sail / rail / glass / deck or equivalent semantic patches.

## MUST CHECK
- every visible patch has a declared semantic role;
- opaque vs glazing/infill roles are explicit;
- boundary pairs are named (e.g. `ROOF↔A_PILLAR`, `A_PILLAR↔WINDSHIELD`, `C_PILLAR↔REAR_GLASS`);
- each boundary pair has a measurable maximum gap from evaluated geometry or shared anchor coordinates;
- floating/orphan visible patches are forbidden;
- patch overlap/interpenetration must not be used to hide gaps;
- machine assembly state remains visual HOLD until broad/3Q reflection/readback is reviewed.

## ALLOWED
- separate Blender objects for semantically distinct surface patches;
- identical shared anchor coordinates across separate patches;
- Source semantic boundaries regenerated as denser Derived patches;
- independent glass/infill surfaces.

## FORBIDDEN
- claiming continuity from object naming or object count;
- claiming a shared boundary because two objects visually overlap;
- using wide overlap to conceal mismatch;
- promoting a machine-clean assembly without visual/reference review.

## EVIDENCE
`SURFACE_PATCH_ASSEMBLY_RECEIPT.json`:
- `candidate_revision`;
- `opaque_patch_count`;
- `glass_patch_count`;
- `patches[]` with role and authority;
- `boundary_pairs[]` with pair ID and `max_gap_m`;
- `max_shared_boundary_gap_m`;
- `floating_visible_patch_count`;
- `machine_assembly_state`;
- `visual_review_state`;
- `does_not_prove`.

Allowed machine states: `MACHINE_ASSEMBLED_VISUAL_HOLD` or `MACHINE_ASSEMBLY_REJECT`.

## Failure routing
- large gap at one semantic boundary → fix that pair only;
- no gap but visible crease/poor highlight flow → route to Derived Surface Finish, not boundary position;
- glass fits but host silhouette wrong → route to Primary Form Identity;
- assembly clean but first-read generic → do not add detail; return to primary form.

## Does not prove
Class-A/G2/G3 continuity, manufacturer CAD, sealing/flange engineering, tooling, manufacturability, homologation, physical CMF or commercial IP clearance.