#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
from xml.etree import ElementTree as ET

try:
    import cairosvg
    from pypdf import PdfReader
except Exception as exc:
    print(json.dumps({"status":"HOLD","reason":"MISSING_VALIDATION_DEPENDENCY","detail":str(exc)}))
    raise SystemExit(78)

ROOT = Path(__file__).resolve().parent
EXPECTED_MM = (120.0, 60.0)

def parse_length(value: str):
    m = re.fullmatch(r"\s*([0-9.]+)\s*([a-zA-Z%]*)\s*", value or "")
    if not m:
        return None, None
    return float(m.group(1)), m.group(2) or "unitless"

def validate(name: str):
    svg = ROOT / f"{name}.svg"
    pdf = ROOT / f"{name}.pdf"
    root = ET.parse(svg).getroot()
    width_v, width_u = parse_length(root.attrib.get("width"))
    height_v, height_u = parse_length(root.attrib.get("height"))
    viewbox = root.attrib.get("viewBox")
    cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
    page = PdfReader(str(pdf)).pages[0]
    wpt, hpt = float(page.mediabox.width), float(page.mediabox.height)
    wmm, hmm = wpt * 25.4 / 72.0, hpt * 25.4 / 72.0
    return {
        "source": svg.name,
        "width_attr": root.attrib.get("width"),
        "height_attr": root.attrib.get("height"),
        "width_unit": width_u,
        "height_unit": height_u,
        "viewBox": viewbox,
        "pdf_page_pt": [wpt, hpt],
        "pdf_page_mm": [wmm, hmm],
        "matches_expected_120x60_mm": abs(wmm-EXPECTED_MM[0]) < 0.01 and abs(hmm-EXPECTED_MM[1]) < 0.01,
    }

results = {"A_unitless": validate("A_unitless"), "B_mm": validate("B_mm")}
results["verdict"] = {
    "A_unitless": "HOLD_PHYSICAL_SIZE_AUTHORITY_NOT_EXPLICIT",
    "B_mm": "PASS_FOR_BOUNDED_PHYSICAL_SIZE_SEMANTICS",
    "rule": "SVG_VIEWBOX_OR_NUMERIC_WIDTH_HEIGHT_DO_NOT_ESTABLISH_MM_PRINT_SIZE; EXPLICIT_PHYSICAL_UNITS_OR_AN_EQUIVALENT_AUTHORITATIVE_OUTPUT_CONTRACT_ARE_REQUIRED."
}
print(json.dumps(results, indent=2))
if results["A_unitless"]["matches_expected_120x60_mm"]:
    raise SystemExit(2)
if not results["B_mm"]["matches_expected_120x60_mm"]:
    raise SystemExit(3)
