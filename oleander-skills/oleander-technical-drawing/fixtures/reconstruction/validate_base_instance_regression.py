#!/usr/bin/env python3
import copy
import json
import subprocess
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE.parent.parent / "tools" / "validate_base_instances.py"
SVG = HERE / "BASE-01_INSTANCE.svg"
REG = HERE / "BASE-01_INSTANCE_REGISTER.json"
NS = "{http://www.w3.org/2000/svg}"


def run(svg, reg, expect_ok):
    p = subprocess.run(["python", str(VALIDATOR), "--svg", str(svg), "--register", str(reg)], capture_output=True, text=True)
    ok = p.returncode == 0
    if ok != expect_ok:
        raise AssertionError(f"unexpected validator result ok={ok} expect={expect_ok}\nSTDOUT={p.stdout}\nSTDERR={p.stderr}")


def write_case(tmp, name, tree, reg):
    svg = tmp / f"{name}.svg"
    js = tmp / f"{name}.json"
    tree.write(svg, encoding="utf-8", xml_declaration=True)
    js.write_text(json.dumps(reg, indent=2), encoding="utf-8")
    return svg, js


def find(root, node_id):
    for n in root.iter():
        if n.attrib.get("id") == node_id:
            return n
    raise KeyError(node_id)


def main():
    run(SVG, REG, True)
    base_tree = ET.parse(SVG)
    base_reg = json.loads(REG.read_text(encoding="utf-8"))
    blocked = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        # 1 raster embedding
        tree = copy.deepcopy(base_tree); reg = copy.deepcopy(base_reg)
        carrier = find(tree.getroot(), "PANEL-A_VISUAL_BASE")
        ET.SubElement(carrier, NS + "image", {"href": "data:image/png;base64,AAAA"})
        s, r = write_case(tmp, "raster", tree, reg); run(s, r, False); blocked.append("raster-embed")

        # 2 text contamination
        tree = copy.deepcopy(base_tree); reg = copy.deepcopy(base_reg)
        carrier = find(tree.getroot(), "PANEL-B_VISUAL_BASE")
        t = ET.SubElement(carrier, NS + "text", {"x": "10", "y": "10"}); t.text = "label"
        s, r = write_case(tmp, "text", tree, reg); run(s, r, False); blocked.append("text-contamination")

        # 3 theme-color contamination
        tree = copy.deepcopy(base_tree); reg = copy.deepcopy(base_reg)
        carrier = find(tree.getroot(), "PANEL-C_VISUAL_BASE")
        ET.SubElement(carrier, NS + "path", {"d": "M1 1h20", "stroke": "#e85b65", "fill": "none"})
        s, r = write_case(tmp, "theme", tree, reg); run(s, r, False); blocked.append("theme-color-contamination")

        # 4 false authority
        tree = copy.deepcopy(base_tree); reg = copy.deepcopy(base_reg)
        reg["panels"][0]["authority"] = True
        s, r = write_case(tmp, "authority", tree, reg); run(s, r, False); blocked.append("false-authority")

        # 5 collapse panel-specific visual carriers to one id
        tree = copy.deepcopy(base_tree); reg = copy.deepcopy(base_reg)
        reg["panels"][1]["visual_carrier_id"] = reg["panels"][0]["visual_carrier_id"]
        s, r = write_case(tmp, "collapsed", tree, reg); run(s, r, False); blocked.append("identical-carrier-collapse")

        # 6 delete semantic master
        tree = copy.deepcopy(base_tree); reg = copy.deepcopy(base_reg)
        defs = next(n for n in tree.getroot() if n.tag == NS + "defs")
        defs.remove(find(tree.getroot(), "BASE-01_GEOMETRY_MASTER"))
        s, r = write_case(tmp, "no-master", tree, reg); run(s, r, False); blocked.append("semantic-master-deleted")

    print("OLEANDER BASE INSTANCE REGRESSION: POSITIVE + NEGATIVE CONTRACT PASS")
    print("blocked=" + ",".join(blocked))
    print("NOTE: regression PASS does not equal pixel fidelity, panel completeness, geometry authority, or Design KEEP.")


if __name__ == "__main__":
    main()
