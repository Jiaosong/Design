import bpy
import json
import os
import sys

OUT = os.environ.get("OLEANDER_JOB_OUTPUT_DIR") or os.environ.get("C04_REBUILD_OUT", "/tmp/c04-fluid-seat-rebuild")
RECEIPT = os.path.join(OUT, "C04_FLUID_SEAT_REBUILD_MASTER_v001_reopen_receipt.json")
required = [
    "C04_FLUID_SEAT_PRIMARY_SEAT",
    "C04_FLUID_SEAT_BACKREST",
    "C04_FLUID_SEAT_CONTACT_ZONE",
    "C04_FLUID_SEAT_LUMBAR_ZONE",
    "C04_FLUID_SEAT_SUPPORT_PROXY",
]
missing = [n for n in required if bpy.data.objects.get(n) is None]
primary = bpy.data.objects.get("C04_FLUID_SEAT_PRIMARY_SEAT")
back = bpy.data.objects.get("C04_FLUID_SEAT_BACKREST")
contact = bpy.data.objects.get("C04_FLUID_SEAT_CONTACT_ZONE")
lumbar = bpy.data.objects.get("C04_FLUID_SEAT_LUMBAR_ZONE")

passed = bool(primary and back and contact and lumbar) and not missing
if primary:
    passed = passed and len(primary.data.vertices) > 0 and len(primary.data.polygons) > 0
    passed = passed and primary.get("OLE_ID") == "C04_FLUID_SEAT_REBUILD_MASTER_v001"
    passed = passed and primary.get("PROJECT_ID") == "PRJ-C04-QINGJIANG-SHISHU"
    passed = passed and primary.get("CHILD_ITEM") == "流体座椅人体工"
    passed = passed and primary.get("DIMENSION_AUTHORITY") == "DESIGN_ESTIMATE"
    passed = passed and primary.get("FIELD_STATE") == "FIELD_OPEN"
    passed = passed and primary.get("ENGINEERING_CLAIM") is False
    passed = passed and primary.get("DESIGN_KEEP_CLAIM") is False
    modifier_types = {m.type for m in primary.modifiers}
    passed = passed and {"SOLIDIFY", "BEVEL", "SUBSURF"}.issubset(modifier_types)

receipt = {
  "schema_version":"1.0",
  "project_id":"PRJ-C04-QINGJIANG-SHISHU",
  "child_item":"流体座椅人体工",
  "blender_version":bpy.app.version_string,
  "open_file":bpy.data.filepath,
  "required_objects":required,
  "missing_objects":missing,
  "primary_vertices":0 if primary is None else len(primary.data.vertices),
  "primary_polygons":0 if primary is None else len(primary.data.polygons),
  "back_vertices":0 if back is None else len(back.data.vertices),
  "contact_vertices":0 if contact is None else len(contact.data.vertices),
  "lumbar_vertices":0 if lumbar is None else len(lumbar.data.vertices),
  "primary_modifier_stack":[] if primary is None else [[m.name,m.type] for m in primary.modifiers],
  "ole_id":None if primary is None else primary.get("OLE_ID"),
  "dimension_authority":None if primary is None else primary.get("DIMENSION_AUTHORITY"),
  "field_state":None if primary is None else primary.get("FIELD_STATE"),
  "engineering_claim":None if primary is None else primary.get("ENGINEERING_CLAIM"),
  "design_keep_claim":None if primary is None else primary.get("DESIGN_KEEP_CLAIM"),
  "verdict":"PASS_BOUNDED" if passed else "FAIL",
  "truth_boundary":"Native reopen verifies persisted Blender-native object identity, editable geometry and declared design-estimate boundaries only; not ergonomic, engineering, field or manufacturing approval."
}
with open(RECEIPT,"w",encoding="utf-8") as f: json.dump(receipt,f,ensure_ascii=False,indent=2)
print("OLEANDER_C04_REOPEN_RECEIPT="+RECEIPT)
if not passed:
    sys.exit(3)
