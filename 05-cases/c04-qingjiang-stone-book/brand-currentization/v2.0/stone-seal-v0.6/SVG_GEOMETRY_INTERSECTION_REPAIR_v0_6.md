# SVG Material Geometry Repair — v0.6

Two earlier render implementations were rejected during producer readback:
1. `clipPath` with compound-hole geometry produced slivers in CairoSVG.
2. mask-based containment produced rasterization leakage outside the symbol.

CURRENT v0.6 solution:
- no clipPath;
- no SVG mask;
- gradient overlays use the authoritative compound Stone Seal path directly;
- macro mineral fields are geometrically intersected with the Stone Seal polygon;
- mineral/abrasion lines are intersected with the Stone Seal polygon;
- micro grain and edge wear are intersected with the Stone Seal polygon before SVG serialization;
- each embedded material asset uses a unique gradient namespace.

This changes rendering implementation, not the Stone Seal topology.
