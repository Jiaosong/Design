#!/usr/bin/env python3
"""Build a deterministic SVG atlas from an OLEANDER effect recipe register.

Stdlib-only. The atlas is a regression artifact, not a Design KEEP artifact.
"""
from __future__ import annotations
import json
import math
import random
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def color_with_opacity(color: str, opacity: float) -> str:
    return color


def make_linear(inst, box, idx):
    x, y, w, h = box
    p = inst["parameters"]
    gid = f"grad-{idx}"
    stops = []
    for off, color, opacity in p["stops"]:
        stops.append(f'<stop offset="{off*100:.3f}%" stop-color="{escape(color)}" stop-opacity="{float(opacity):.4f}"/>')
    axis = float(p.get("axis_deg", 0.0))
    r = math.radians(axis)
    x1 = 50 - math.cos(r) * 50
    y1 = 50 - math.sin(r) * 50
    x2 = 50 + math.cos(r) * 50
    y2 = 50 + math.sin(r) * 50
    defs = f'<linearGradient id="{gid}" x1="{x1:.2f}%" y1="{y1:.2f}%" x2="{x2:.2f}%" y2="{y2:.2f}%">{"".join(stops)}</linearGradient>'
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#{gid})" stroke="#59615c" stroke-width="1"/>'
    return defs, body


def make_hatch(inst, box, idx):
    x, y, w, h = box
    p = inst["parameters"]
    pid = f"hatch-{idx}"
    spacing = float(p["spacing_px"])
    stroke = float(p["stroke_px"])
    opacity = float(p["opacity"])
    angle = float(p["angle_deg"])
    defs = (
        f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{spacing}" height="{spacing}" '
        f'patternTransform="rotate({angle})">'
        f'<line x1="0" y1="0" x2="0" y2="{spacing}" stroke="#34413b" stroke-width="{stroke}" opacity="{opacity}"/>'
        '</pattern>'
    )
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#e9e6dc" stroke="#59615c"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#{pid})"/>'
    return defs, body


def make_stipple(inst, box, idx):
    x, y, w, h = box
    p = inst["parameters"]
    density = float(p["density"])
    radius = float(p["radius_px"])
    jitter = float(p["jitter"])
    seed = int(p["seed"])
    rng = random.Random(seed)
    target = max(8, int(w * h * density / 28.0))
    circles = []
    for _ in range(target):
        px = x + rng.random() * w
        py = y + rng.random() * h
        rr = radius * (1.0 + (rng.random() - 0.5) * jitter)
        op = 0.18 + rng.random() * 0.36
        circles.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{max(0.18, rr):.2f}" fill="#635c52" opacity="{op:.3f}"/>')
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ddd3c4" stroke="#59615c"/>' + ''.join(circles)
    return '', body


def make_grain(inst, box, idx):
    x, y, w, h = box
    p = inst["parameters"]
    fid = f"grain-{idx}"
    freq = float(p["base_frequency"])
    octv = int(p["num_octaves"])
    seed = int(p["seed"])
    opacity = float(p["opacity"])
    defs = (
        f'<filter id="{fid}" x="-10%" y="-10%" width="120%" height="120%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octv}" seed="{seed}" result="n"/>'
        '<feColorMatrix in="n" type="saturate" values="0" result="mono"/>'
        '</filter>'
    )
    body = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ece7dc" stroke="#59615c"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" filter="url(#{fid})" opacity="{opacity}"/>'
    )
    return defs, body


def make_shadow(inst, box, idx):
    x, y, w, h = box
    p = inst["parameters"]
    fid = f"shadow-{idx}"
    dx = float(p["dx_px"]); dy = float(p["dy_px"]); blur = float(p["blur_px"]); opacity = float(p["opacity"])
    defs = f'<filter id="{fid}" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{blur/2:.3f}" flood-color="#17231f" flood-opacity="{opacity}"/></filter>'
    body = f'<rect x="{x+20}" y="{y+16}" width="{w-40}" height="{h-32}" rx="12" fill="#f8f6ef" stroke="#59615c" filter="url(#{fid})"/>'
    return defs, body


def make_glow(inst, box, idx):
    x, y, w, h = box
    p = inst["parameters"]
    fid = f"glow-{idx}"
    blur = float(p["blur_px"]); opacity = float(p["opacity"])
    defs = (
        f'<filter id="{fid}" x="-80%" y="-80%" width="260%" height="260%">'
        f'<feGaussianBlur stdDeviation="{blur/2:.3f}" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
    )
    cx = x + w/2; cy = y + h/2
    body = (
        f'<circle cx="{cx}" cy="{cy}" r="32" fill="#b95f50" opacity="{opacity}" filter="url(#{fid})"/>'
        f'<circle cx="{cx}" cy="{cy}" r="17" fill="#f3f0e8" stroke="#a74c40" stroke-width="3"/>'
        f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#7b332b">ALERT</text>'
    )
    return defs, body


BUILDERS = {
    "SVG-R01-LINEAR-FIELD": make_linear,
    "SVG-R03-HATCH": make_hatch,
    "SVG-R04-STIPPLE": make_stipple,
    "SVG-R05-GRAIN": make_grain,
    "SVG-R06-SHADOW-DEPTH": make_shadow,
    "SVG-R08-GLOW-EMISSION": make_glow,
}


def main():
    if len(sys.argv) != 3:
        print("usage: build_svg_effect_atlas.py REGISTER OUTPUT.svg")
        raise SystemExit(2)
    register = load(Path(sys.argv[1]))
    output = Path(sys.argv[2])
    canvas = register.get("canvas", {})
    width = int(canvas.get("width", 1200)); height = int(canvas.get("height", 720)); bg = canvas.get("background", "#f3f0e8")
    static = [i for i in register.get("effect_instances", []) if i.get("kind") == "STATIC_SVG"]
    cols = 3
    gap = 24
    margin = 30
    tile_w = (width - margin*2 - gap*(cols-1)) / cols
    tile_h = 270
    defs = []
    groups = []
    for idx, inst in enumerate(static):
        row = idx // cols; col = idx % cols
        tx = margin + col * (tile_w + gap); ty = 78 + row * (tile_h + gap)
        box = (tx+16, ty+46, tile_w-32, tile_h-76)
        builder = BUILDERS.get(inst["recipe_id"])
        if builder:
            d, body = builder(inst, box, idx)
            if d: defs.append(d)
        else:
            body = f'<rect x="{box[0]}" y="{box[1]}" width="{box[2]}" height="{box[3]}" fill="#eee"/><text x="{box[0]+10}" y="{box[1]+30}" font-family="sans-serif" font-size="14">UNIMPLEMENTED DEMO</text>'
        label = escape(inst["recipe_id"])
        role = escape(inst["surface_role"])
        groups.append(
            f'<g id="tile-{idx}"><rect x="{tx}" y="{ty}" width="{tile_w}" height="{tile_h}" rx="14" fill="#faf8f2" stroke="#c8c4b9"/>'
            f'<text x="{tx+16}" y="{ty+22}" font-family="sans-serif" font-size="13" font-weight="700" fill="#17231f">{label}</text>'
            f'<text x="{tx+16}" y="{ty+38}" font-family="sans-serif" font-size="10" fill="#69716c">{role}</text>{body}</g>'
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'<rect width="{width}" height="{height}" fill="{escape(bg)}"/>'
        '<text x="30" y="38" font-family="sans-serif" font-size="22" font-weight="700" fill="#17231f">OLEANDER / Procedural SVG Effect Atlas</text>'
        '<text x="30" y="58" font-family="sans-serif" font-size="11" fill="#69716c">Regression artifact · EFFECT OFF must preserve geometry / relation / state</text>'
        f'<defs>{"".join(defs)}</defs>{"".join(groups)}'
        '<metadata>Generated by build_svg_effect_atlas.py. Regression artifact only; no Design KEEP.</metadata></svg>'
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    ET.parse(output)
    print(f"PASS: generated {output} with {len(static)} static recipe tiles; XML parsed")


if __name__ == "__main__":
    main()
