import math, json

RULES = {
    "opening_width_mm": 1200.0,
    "opening_height_mm": 1500.0,
    "corner_anchor_offset_mm": 150.0,
    "max_anchor_spacing_mm": 600.0
}

def positions_along(length, corner_offset, max_spacing):
    usable = length - 2 * corner_offset
    if usable < 0:
        raise ValueError("corner offsets exceed side length")
    segments = max(1, math.ceil(usable / max_spacing))
    spacing = usable / segments
    return [corner_offset + i * spacing for i in range(segments + 1)], spacing

top, top_spacing = positions_along(RULES["opening_width_mm"], RULES["corner_anchor_offset_mm"], RULES["max_anchor_spacing_mm"])
side, side_spacing = positions_along(RULES["opening_height_mm"], RULES["corner_anchor_offset_mm"], RULES["max_anchor_spacing_mm"])

print(json.dumps({
    "top": top,
    "side": side,
    "top_spacing": top_spacing,
    "side_spacing": side_spacing
}, indent=2))
