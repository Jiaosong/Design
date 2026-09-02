import bpy
import json
import os
import sys

out_dir = os.environ.get("C04_REBUILD_OUT", "/tmp/c04-yunshuiyi-rebuild")
receipt_path = os.path.join(out_dir, "C04_YUNSHUIYI_REBUILD_MASTER_v002_reopen_receipt.json")
required = [
    "C04_YUNSHUIYI_PRIMARY_SHELL",
    "C04_YUNSHUIYI_CONTACT_ZONE",
    "DATUM_LONGITUDINAL_CENTER",
]
missing = [name for name in required if bpy.data.objects.get(name) is None]
primary = bpy.data.objects.get("C04_YUNSHUIYI_PRIMARY_SHELL")
mods = [] if primary is None else [(m.name, m.type) for m in primary.modifiers]
passed = (
    not missing
    and primary is not None
    and len(primary.data.vertices) > 0
    and len(primary.data.polygons) > 0
    and primary.get("OLE_ID") == "C04_YUNSHUIYI_REBUILD_MASTER_v002"
    and primary.get("DIMENSION_AUTHORITY") == "DESIGN_ESTIMATE"
    and primary.get("FIELD_STATE") == "FIELD_OPEN"
)
receipt = {
    "schema_version": "1.0",
    "blender_version": bpy.app.version_string,
    "open_file": bpy.data.filepath,
    "required_objects": required,
    "missing_objects": missing,
    "primary_vertices": 0 if primary is None else len(primary.data.vertices),
    "primary_polygons": 0 if primary is None else len(primary.data.polygons),
    "modifier_stack": mods,
    "ole_id": None if primary is None else primary.get("OLE_ID"),
    "dimension_authority": None if primary is None else primary.get("DIMENSION_AUTHORITY"),
    "field_state": None if primary is None else primary.get("FIELD_STATE"),
    "verdict": "PASS_BOUNDED" if passed else "FAIL",
    "truth_boundary": "Native reopen proves Blender persistence only; not engineering, field, or design approval."
}
with open(receipt_path, "w", encoding="utf-8") as f:
    json.dump(receipt, f, ensure_ascii=False, indent=2)
print("OLEANDER_C04_REOPEN_RECEIPT=" + receipt_path)
if not passed:
    sys.exit(3)
