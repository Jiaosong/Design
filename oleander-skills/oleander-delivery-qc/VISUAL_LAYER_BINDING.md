# Delivery QC Visual Layer Binding

Status: **BINDING ONLY / INSPECTION, NOT DESIGN AUTHORING**

`oleander-delivery-qc` does not own visual-effect design. Its visual responsibility is to inspect whether the reviewed visual result survived export/package/delivery and whether the actual preview exposes blocking defects.

## Existing sources to inherit

1. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
2. The producing Skill's own visual rules and Current Project Design Source.

## Existing inspection duties

- Re-open actual final images, boards, PDFs, video frames, 3D previews and interactive outputs.
- Check crop, occlusion, missing fonts/links, overset text, pixel damage, compression, unintended color/profile shifts, scaling, responsive breakage and source/export mismatch.
- For visual deliverables, preserve the distinction between `EXECUTED`, `DESIGN REVIEW PENDING`, `KEEP`, `REVISE`, `REJECT` and `HOLD` from Artifact Review v1.1.
- Do not add glow, grading, sharpening, layout changes, motion or other styling during QC unless the user explicitly asks for a repair derivative.

## Hard boundary

`Delivery QC PASS ≠ Professional Design PASS`. If the defect is a design-quality problem rather than an export/package defect, route it back to the responsible execution owner and independent design review.
