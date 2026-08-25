# Delivery QC Visual Layer Binding

Status: **BINDING ONLY / INSPECTION, NOT DESIGN AUTHORING**

`oleander-delivery-qc` does not own visual-effect design. Its visual responsibility is to inspect whether the reviewed visual result survived export/package/delivery and whether the actual preview exposes blocking defects.

## Existing sources to inherit

1. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
2. The producing Skill's own visual rules and Current Project Design Source.
3. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for checking the integrity of image-processing derivatives and recoverable masters.

## Existing inspection duties

- Re-open actual final images, boards, PDFs, video frames, 3D previews and interactive outputs.
- Check crop, occlusion, missing fonts/links, overset text, pixel damage, compression, unintended color/profile shifts, scaling, responsive breakage and source/export mismatch.
- For visual deliverables, preserve the distinction between `EXECUTED`, `DESIGN REVIEW PENDING`, `KEEP`, `REVISE`, `REJECT` and `HOLD` from Artifact Review v1.1.
- Do not add glow, grading, sharpening, layout changes, motion or other styling during QC unless the user explicitly asks for a repair derivative.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` as an inspection contract, not an authoring licence. Verify that required layered/vector/linked masters exist when the production contract requires them; check masks/alpha, flattening/rasterization, Smart Object dependencies, profile/resolution changes, destructive retouch, effect-off recoverability and derivative labels. If QC discovers a semantic image edit or generative alteration that is not disclosed, route it back as a provenance/truth-boundary defect rather than silently accepting the export.

## Hard boundary

`Delivery QC PASS ≠ Professional Design PASS`. If the defect is a design-quality problem rather than an export/package defect, route it back to the responsible execution owner and independent design review.
