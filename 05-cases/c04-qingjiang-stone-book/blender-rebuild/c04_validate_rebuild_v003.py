import bpy
import json
import os
import sys

OUT = os.environ.get("C04_REBUILD_OUT", "/tmp/c04-yunshuiyi-rebuild")
RECEIPT = os.path.join(OUT, "C04_YUNSHUIYI_REBUILD_MASTER_v003_reopen_receipt.json")
required = ["C04_YUNSHUIYI_PRIMARY_SHELL", "C04_YUNSHUIYI_CONTACT_ZONE", "DATUM_LONGITUDINAL_CENTER"]
missing = [n for n in required if bpy.data.objects.get(n) is None]
primary = bpy.data.objects.get("C04_YUNSHUIYI_PRIMARY_SHELL")
passed = bool(primary) and not missing and len(primary.data.vertices) > 0 and len(primary.data.polygons) > 0
passed = passed and primary.get("OLE_ID") == "C04_YUNSHUIYI_REBUILD_MASTER_v003"
passed = passed and primary.get("DIMENSION_AUTHORITY") == "DESIGN_ESTIMATE" and primary.get("FIELD_STATE") == "FIELD_OPEN"
receipt = {
  "schema_version":"1.0",
  "blender_version":bpy.app.version_string,
  "open_file":bpy.data.filepath,
  "required_objects":required,
  "missing_objects":missing,
  "primary_vertices":0 if primary is None else len(primary.data.vertices),
  "primary_polygons":0 if primary is None else len(primary.data.polygons),
  "modifier_stack":[] if primary is None else [[m.name,m.type] for m in primary.modifiers],
  "ole_id":None if primary is None else primary.get("OLE_ID"),
  "dimension_authority":None if primary is None else primary.get("DIMENSION_AUTHORITY"),
  "field_state":None if primary is None else primary.get("FIELD_STATE"),
  "verdict":"PASS_BOUNDED" if passed else "FAIL",
  "truth_boundary":"Native reopen proves Blender persistence only; not engineering, field or design approval."
}
with open(RECEIPT,"w",encoding="utf-8") as f: json.dump(receipt,f,ensure_ascii=False,indent=2)
print("OLEANDER_C04_REOPEN_RECEIPT="+RECEIPT)
if not passed: sys.exit(3)
