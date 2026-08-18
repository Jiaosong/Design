#!/usr/bin/env python3
from __future__ import annotations
import sys,xml.etree.ElementTree as ET
from pathlib import Path

def tile(x,y,w,h,title,body):
    return f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#faf8f2" stroke="#c9c5b8"/><text x="{x+14}" y="{y+24}" font-family="sans-serif" font-size="12" font-weight="700" fill="#17231f">{title}</text>{body}</g>'

def main():
    if len(sys.argv)!=2:
        print('usage: build_svg_effect_extension_02.py OUTPUT.svg'); raise SystemExit(2)
    out=Path(sys.argv[1]); W,H=1200,700; tw,th=270,255; gap=20; xs=[30,320,610,900]; ys=[82,357]
    defs='''
<filter id="blur"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="fiber"><feTurbulence type="fractalNoise" baseFrequency=".38 .85" numOctaves="2" seed="23"/><feColorMatrix type="saturate" values="0"/></filter>
<linearGradient id="hill" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#8a8f88" stop-opacity=".15"/><stop offset=".48" stop-color="#28342f" stop-opacity=".42"/><stop offset="1" stop-color="#f5f2e8" stop-opacity=".1"/></linearGradient>
<linearGradient id="depth" x1="0" x2="1"><stop offset="0" stop-color="#1d2824" stop-opacity=".52"/><stop offset="1" stop-color="#1d2824" stop-opacity=".04"/></linearGradient>
<pattern id="half" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(15)"><circle cx="4" cy="4" r="2.5" fill="#537f7b" opacity=".65"/></pattern>
<clipPath id="safeclip"><rect x="930" y="414" width="205" height="132" rx="9"/></clipPath>
'''
    items=[]
    x,y=xs[0],ys[0]; body=f'<g transform="translate({x+18} {y+46})"><rect width="232" height="165" fill="#cbd7d1"/><g filter="url(#blur)" opacity=".55"><circle cx="55" cy="78" r="36" fill="#986354"/><rect x="115" y="36" width="90" height="90" fill="#6e8d83"/></g><rect x="88" y="55" width="74" height="60" rx="8" fill="#f3f0e8" stroke="#17231f" stroke-width="2"/><text x="125" y="90" text-anchor="middle" font-family="sans-serif" font-size="12">FOCUS</text></g>'
    items.append(tile(x,y,tw,th,'SVG-R11 / BLUR-FOCUS',body))
    x,y=xs[1],ys[0]; body=f'<rect x="{x+18}" y="{y+46}" width="232" height="165" rx="9" fill="#e6e0d3"/><rect x="{x+18}" y="{y+46}" width="232" height="165" rx="9" fill="url(#half)"/><text x="{x+28}" y="{y+195}" font-family="sans-serif" font-size="10" fill="#5c6761">SYNTHETIC DENSITY FIELD</text>'
    items.append(tile(x,y,tw,th,'SVG-R12 / HALFTONE',body))
    x,y=xs[2],ys[0]; body=f'<rect x="{x+18}" y="{y+46}" width="232" height="165" rx="9" fill="#eee7d9"/><rect x="{x+18}" y="{y+46}" width="232" height="165" rx="9" filter="url(#fiber)" opacity=".07"/><path d="M{x+28} {y+92} H{x+238} M{x+28} {y+126} H{x+238} M{x+28} {y+160} H{x+238}" stroke="#a89b87" stroke-width=".6" opacity=".38"/>'
    items.append(tile(x,y,tw,th,'SVG-R13 / PAPER-FIBER',body))
    x,y=xs[3],ys[0]; body=f'<rect x="{x+18}" y="{y+46}" width="232" height="165" rx="9" fill="#bad0ca"/><circle cx="{x+116}" cy="{y+126}" r="70" fill="#aa765c" opacity=".58" style="mix-blend-mode:multiply"/><path d="M{x+30} {y+180} C{x+90} {y+130},{x+160} {y+205},{x+240} {y+112}" fill="none" stroke="#17231f" stroke-width="3"/>'
    items.append(tile(x,y,tw,th,'SVG-R14 / BLEND-OVERLAY',body))
    x,y=xs[0],ys[1]; body=f'<path d="M{x+24} {y+120} C{x+75} {y+75},{x+145} {y+190},{x+245} {y+90}" fill="none" stroke="#455d57" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 7"/><text x="{x+24}" y="{y+205}" font-family="sans-serif" font-size="10" fill="#5c6761">CONDITIONAL RELATION / NO DIRECTION ENCODED</text>'
    items.append(tile(x,y,tw,th,'SVG-R15 / DASH-RHYTHM',body))
    x,y=xs[1],ys[1]; body=f'<path d="M{x+18} {y+185} C{x+58} {y+90},{x+120} {y+60},{x+250} {y+135} L{x+250} {y+210} L{x+18} {y+210} Z" fill="#cad4c4"/><path d="M{x+18} {y+185} C{x+58} {y+90},{x+120} {y+60},{x+250} {y+135} L{x+250} {y+210} L{x+18} {y+210} Z" fill="url(#hill)"/><text x="{x+24}" y="{y+226}" font-family="sans-serif" font-size="10" fill="#9b4e43">SYNTHETIC MECHANISM DEMO / NOT DEM</text>'
    items.append(tile(x,y,tw,th,'SVG-R16 / HILLSHADE-PASS',body))
    x,y=xs[2],ys[1]; body=f'<g transform="translate({x+28} {y+72})"><polygon points="25,55 110,18 190,54 105,94" fill="#e5dfd3" stroke="#17231f"/><polygon points="25,55 105,94 105,145 25,105" fill="#c9c0b1" stroke="#17231f"/><polygon points="105,94 190,54 190,105 105,145" fill="#b9b1a4" stroke="#17231f"/><polygon points="25,55 110,18 190,54 105,94" fill="url(#depth)" opacity=".35"/></g><text x="{x+24}" y="{y+226}" font-family="sans-serif" font-size="10" fill="#9b4e43">SYNTHETIC AO/DEPTH PASS / NOT LIGHTING TRUTH</text>'
    items.append(tile(x,y,tw,th,'SVG-R17 / AO-DEPTH-PASS',body))
    x,y=xs[3],ys[1]; body=f'<g clip-path="url(#safeclip)"><rect x="{x+18}" y="{y+46}" width="232" height="165" fill="#e5ddcd"/><path d="M{x+25} {y+175} C{x+75} {y+105},{x+150} {y+95},{x+242} {y+145}" stroke="#4d8d92" stroke-width="9" fill="none"/><text x="{x+32}" y="{y+76}" font-family="sans-serif" font-size="13" font-weight="700">SOURCE FIGURE</text><text x="{x+32}" y="{y+94}" font-family="sans-serif" font-size="10">STATUS / SCALE / SOURCE PRESERVED</text></g><rect x="{x+30}" y="{y+57}" width="205" height="132" rx="9" fill="none" stroke="#a45449" stroke-width="1.5"/>'
    items.append(tile(x,y,tw,th,'SVG-R18 / SOURCE-CLIP',body))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#f3f0e8"/><text x="30" y="38" font-family="sans-serif" font-size="22" font-weight="700" fill="#17231f">OLEANDER / Effect Extension 02</text><text x="30" y="58" font-family="sans-serif" font-size="11" fill="#68716c">Synthetic mechanism regression atlas — project evidence not implied</text><defs>{defs}</defs>{"".join(items)}<metadata>SYNTHETIC MECHANISM DEMO / NO DESIGN KEEP / NO MATERIAL OR FIELD TRUTH</metadata></svg>'
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(svg,encoding='utf-8'); ET.parse(out); print(f'PASS: generated {out}; 8 extension effect tiles; XML parsed')
if __name__=='__main__': main()
