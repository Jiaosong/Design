#!/usr/bin/env python3
"""Build an OLEANDER SP02 Grasshopper fixture from an official McNeel GHX sample.

This builder does not execute Rhino or Grasshopper. It prepares a GHX definition that
can be submitted to a real Rhino.Compute / Grasshopper headless runtime.
"""
from __future__ import annotations

import argparse
import base64
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

FIXTURE_URL = (
    "https://raw.githubusercontent.com/mcneel/developer.rhino3d.com/"
    "424f4cf8a12a1ba93a3bcf697c26053eede5e46e/"
    "content/en/guides/scripting/_art/python3-component-paramaccess.ghx"
)
PYTHON3_COMPONENT_GUID = "719467e6-7cf5-4848-99b0-c5dd57e5442c"
GROUP_COMPONENT_GUID = "c552a431-af5b-46a9-a8a4-0fcbc27ef596"
NAMESPACE_UUID = uuid.UUID("519c7863-648f-4b49-a9bb-75b0fd459df5")

SP02_SCRIPT = r'''import json
import Rhino
from Grasshopper.Kernel.Data import GH_Structure, GH_Path, GH_GraftMode
from Grasshopper.Kernel.Types import GH_Number

ZONES = 4
ITEMS = 6
DX = 2.4
DY = 3.6

# All values are exercise assumptions. Geometry spacing is carried in the report only;
# the test target is Data Tree topology.
def summarize(tree):
    return {
        "branch_count": int(tree.PathCount),
        "item_count": int(tree.DataCount),
        "paths": [str(p) for p in tree.Paths],
        "items_per_branch": [int(len(branch)) for branch in tree.Branches],
    }

base = GH_Structure[GH_Number]()
for zone in range(ZONES):
    p = GH_Path(zone)
    for item in range(ITEMS):
        base.Append(GH_Number(float(zone * 100 + item)), p)

graft = base.Duplicate()
graft.Graft(GH_GraftMode.GraftAll)

flatten = base.Duplicate()
flatten.Flatten()

transpose = GH_Structure[GH_Number]()
for item in range(ITEMS):
    p = GH_Path(item)
    for zone in range(ZONES):
        value = base.Branches[zone][item].Value
        transpose.Append(GH_Number(float(value)), p)

states = {
    "BASE": summarize(base),
    "GRAFT": summarize(graft),
    "FLATTEN": summarize(flatten),
    "TRANSPOSE_BY_ITEM": summarize(transpose),
}
expected = {
    "BASE": {"branch_count": 4, "item_count": 24, "items_per_branch": [6, 6, 6, 6]},
    "GRAFT": {"branch_count": 24, "item_count": 24, "items_per_branch": [1] * 24},
    "FLATTEN": {"branch_count": 1, "item_count": 24, "items_per_branch": [24]},
    "TRANSPOSE_BY_ITEM": {"branch_count": 6, "item_count": 24, "items_per_branch": [4, 4, 4, 4, 4, 4]},
}
checks = {}
for key in expected:
    checks[key] = (
        states[key]["branch_count"] == expected[key]["branch_count"] and
        states[key]["item_count"] == expected[key]["item_count"] and
        states[key]["items_per_branch"] == expected[key]["items_per_branch"]
    )

report = {
    "marker_version": "OLEANDER-SP02-HEADLESS-REPORT-v1",
    "runtime": "Rhino.Compute / Grasshopper headless",
    "rhino_version": str(Rhino.RhinoApp.Version),
    "grasshopper_assembly_version": str(GH_Path(0).GetType().Assembly.GetName().Version),
    "parameters": {
        "zones": ZONES,
        "items_per_zone": ITEMS,
        "dx": DX,
        "dy": DY,
        "provenance": "SIMULATED_EXERCISE_ASSUMPTION"
    },
    "states": states,
    "checks": checks,
    "cp2_candidate": bool(all(checks.values())),
    "cp4": "OPEN_HEADLESS_NO_GUI"
}
print("OLEANDER_SP02_REPORT::" + json.dumps(report, sort_keys=True, separators=(",", ":")))
'''


def _direct_item(chunk: ET.Element, name: str) -> ET.Element | None:
    items = chunk.find("items")
    if items is None:
        return None
    for item in items.findall("item"):
        if item.get("name") == name:
            return item
    return None


def _direct_chunk(parent: ET.Element, name: str) -> ET.Element | None:
    chunks = parent.find("chunks")
    if chunks is None:
        return None
    for chunk in chunks.findall("chunk"):
        if chunk.get("name") == name:
            return chunk
    return None


def _item(parent: ET.Element, name: str, type_name: str, type_code: str, text: str, index: str | None = None):
    attrs = {"name": name, "type_name": type_name, "type_code": type_code}
    if index is not None:
        attrs["index"] = index
    el = ET.SubElement(parent, "item", attrs)
    el.text = text
    return el


def locate_tree_script(definition_objects: ET.Element) -> tuple[ET.Element, ET.Element, str]:
    chunks = definition_objects.find("chunks")
    if chunks is None:
        raise RuntimeError("DefinitionObjects/chunks missing")

    candidates = []
    for obj in chunks.findall("chunk"):
        if obj.get("name") != "Object":
            continue
        name_item = _direct_item(obj, "Name")
        guid_item = _direct_item(obj, "GUID")
        if name_item is None or (name_item.text or "") != "Python 3 Script":
            continue
        if guid_item is None or (guid_item.text or "").lower() != PYTHON3_COMPONENT_GUID:
            continue
        container = _direct_chunk(obj, "Container")
        if container is None:
            continue
        access_values = []
        for item in container.findall(".//item[@name='ScriptParamAccess']"):
            try:
                access_values.append(int((item.text or "").strip()))
            except ValueError:
                pass
        if 2 in access_values:
            candidates.append((obj, container))

    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one DataTree Python component; found {len(candidates)}")

    obj, container = candidates[0]
    instance = _direct_item(container, "InstanceGuid")
    if instance is None or not instance.text:
        raise RuntimeError("Python component InstanceGuid missing")
    return obj, container, instance.text.strip()


def replace_script(container: ET.Element):
    script_chunk = None
    for chunk in container.findall(".//chunk"):
        if chunk.get("name") == "Script":
            script_chunk = chunk
            break
    if script_chunk is None:
        raise RuntimeError("Python component Script chunk missing")
    text_item = _direct_item(script_chunk, "Text")
    if text_item is None:
        raise RuntimeError("Python component Script/Text missing")
    text_item.text = base64.b64encode(SP02_SCRIPT.encode("utf-8")).decode("ascii")


def append_rh_out_group(definition_objects: ET.Element, target_instance_guid: str):
    objects_items = definition_objects.find("items")
    objects_chunks = definition_objects.find("chunks")
    if objects_items is None or objects_chunks is None:
        raise RuntimeError("DefinitionObjects items/chunks missing")

    object_count = None
    for item in objects_items.findall("item"):
        if item.get("name") == "ObjectCount":
            object_count = item
            break
    if object_count is None:
        raise RuntimeError("DefinitionObjects/ObjectCount missing")

    current_count = int((object_count.text or "0").strip())
    group_instance = str(uuid.uuid5(NAMESPACE_UUID, "OLEANDER-SP02-RH-OUT"))

    obj = ET.SubElement(objects_chunks, "chunk", {"name": "Object", "index": str(current_count)})
    obj_items = ET.SubElement(obj, "items", {"count": "2"})
    _item(obj_items, "GUID", "gh_guid", "9", GROUP_COMPONENT_GUID)
    _item(obj_items, "Name", "gh_string", "10", "Group")
    obj_chunks = ET.SubElement(obj, "chunks", {"count": "1"})
    container = ET.SubElement(obj_chunks, "chunk", {"name": "Container"})
    items = ET.SubElement(container, "items", {"count": "8"})
    _item(items, "Border", "gh_int32", "3", "1")
    colour = _item(items, "Colour", "gh_drawing_color", "36", "")
    argb = ET.SubElement(colour, "ARGB")
    argb.text = "150;170;135;255"
    _item(items, "Description", "gh_string", "10", "OLEANDER headless output group")
    _item(items, "ID", "gh_guid", "9", target_instance_guid, index="0")
    _item(items, "ID_Count", "gh_int32", "3", "1")
    _item(items, "InstanceGuid", "gh_guid", "9", group_instance)
    _item(items, "Name", "gh_string", "10", "Group")
    _item(items, "NickName", "gh_string", "10", "RH_OUT")
    container_chunks = ET.SubElement(container, "chunks", {"count": "1"})
    ET.SubElement(container_chunks, "chunk", {"name": "Attributes"})

    current_chunks = int(objects_chunks.get("count", str(current_count)))
    objects_chunks.set("count", str(current_chunks + 1))
    object_count.text = str(current_count + 1)


def build(output: Path, source_copy: Path | None = None):
    request = urllib.request.Request(FIXTURE_URL, headers={"User-Agent": "OLEANDER-SP02-fixture-builder/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
    if source_copy:
        source_copy.parent.mkdir(parents=True, exist_ok=True)
        source_copy.write_bytes(raw)

    root = ET.fromstring(raw.decode("utf-8-sig"))
    definition = _direct_chunk(root, "Definition")
    if definition is None:
        raise RuntimeError("Definition chunk missing")
    definition_objects = _direct_chunk(definition, "DefinitionObjects")
    if definition_objects is None:
        raise RuntimeError("DefinitionObjects chunk missing")

    _, container, instance_guid = locate_tree_script(definition_objects)
    replace_script(container)
    append_rh_out_group(definition_objects, instance_guid)

    props = _direct_chunk(definition, "DefinitionProperties")
    if props is not None:
        name_item = _direct_item(props, "Name")
        if name_item is not None:
            name_item.text = "OLEANDER_SP02_FREE_PUBLIC_COMPUTE.ghx"

    output.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(output, encoding="utf-8", xml_declaration=True)
    print(f"fixture={output}")
    print(f"source={FIXTURE_URL}")
    print(f"target_component={instance_guid}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="runtime-state/OLEANDER_SP02_FREE_PUBLIC_COMPUTE.ghx")
    parser.add_argument("--source-copy", default="runtime-state/mcneel_python3_component_paramaccess_source.ghx")
    args = parser.parse_args()
    build(Path(args.output), Path(args.source_copy) if args.source_copy else None)


if __name__ == "__main__":
    main()
