import bpy
import json
import os
import sys

OUT = os.environ.get("OLEANDER_JOB_OUTPUT_DIR") or os.environ.get("C04_REBUILD_OUT", "/tmp/c04-jiangpan-folding-observation")
RECEIPT = os.path.join(OUT, "C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_MASTER_v001_reopen_receipt.json")
required = [
    "C04_JIANGPAN_LEFT_FRAME",
    "C04_JIANGPAN_RIGHT_FRAME",
    "C04_JIANGPAN_FOLDING_SEAT",
    "C04_JIANGPAN_BACK_RAIL_01",
    "C04_JIANGPAN_BACK_RAIL_02",
    "C04_JIANGPAN_BACK_RAIL_03",
    "C04_JIANGPAN_HINGE_PIN_L",
    "C04_JIANGPAN_HINGE_PIN_R",
    "C04_JIANGPAN_DIAGONAL_BRACE_L",
    "C04_JIANGPAN_DIAGONAL_BRACE_R",
    "C04_JIANGPAN_FRONT_EDGE",
]
missing = [n for n in required if bpy.data.objects.get(n) is None]
seat = bpy.data.objects.get("C04_JIANGPAN_FOLDING_SEAT")
left = bpy.data.objects.get("C04_JIANGPAN_LEFT_FRAME")
right = bpy.data.objects.get("C04_JIANGPAN_RIGHT_FRAME")
rails = [bpy.data.objects.get(f"C04_JIANGPAN_BACK_RAIL_{i:02d}") for i in range(1,4)]

passed = bool(seat and left and right and all(rails)) and not missing
if seat:
    passed = passed and len(seat.data.vertices) > 0 and len(seat.data.polygons) > 0
    passed = passed and seat.get("OLE_ID") == "C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_MASTER_v001"
    passed = passed and seat.get("PROJECT_ID") == "PRJ-C04-QINGJIANG-SHISHU"
    passed = passed and seat.get("CHILD_ITEM") == "江畔停泊折叠观"
    passed = passed and seat.get("DIMENSION_AUTHORITY") == "DESIGN_ESTIMATE"
    passed = passed and seat.get("FIELD_STATE") == "FIELD_OPEN"
    passed = passed and seat.get("ENGINEERING_CLAIM") is False
    passed = passed and seat.get("DESIGN_KEEP_CLAIM") is False

# Folding intent must remain explicit and separately addressable after native reopen.
feature_roles = {}
for n in ["C04_JIANGPAN_HINGE_PIN_L","C04_JIANGPAN_HINGE_PIN_R","C04_JIANGPAN_DIAGONAL_BRACE_L","C04_JIANGPAN_DIAGONAL_BRACE_R"]:
    o = bpy.data.objects.get(n)
    feature_roles[n] = None if o is None else o.get("SEMANTIC_ROLE")
    passed = passed and o is not None and "ENGINEERING" in (o.get("SEMANTIC_ROLE") or "")

receipt = {
  "schema_version":"1.0",
  "project_id":"PRJ-C04-QINGJIANG-SHISHU",
  "child_item":"江畔停泊折叠观",
  "blender_version":bpy.app.version_string,
  "open_file":bpy.data.filepath,
  "required_objects":required,
  "missing_objects":missing,
  "seat_vertices":0 if seat is None else len(seat.data.vertices),
  "seat_polygons":0 if seat is None else len(seat.data.polygons),
  "ole_id":None if seat is None else seat.get("OLE_ID"),
  "dimension_authority":None if seat is None else seat.get("DIMENSION_AUTHORITY"),
  "field_state":None if seat is None else seat.get("FIELD_STATE"),
  "engineering_claim":None if seat is None else seat.get("ENGINEERING_CLAIM"),
  "design_keep_claim":None if seat is None else seat.get("DESIGN_KEEP_CLAIM"),
  "feature_roles":feature_roles,
  "verdict":"PASS_BOUNDED" if passed else "FAIL",
  "truth_boundary":"Native reopen verifies persisted Blender-native object identity, editable folding/contact/feature relations and declared design-estimate boundaries only; not source-fidelity, ergonomic, structural, field or manufacturing approval."
}
with open(RECEIPT,"w",encoding="utf-8") as f: json.dump(receipt,f,ensure_ascii=False,indent=2)
print("OLEANDER_C04_REOPEN_RECEIPT="+RECEIPT)
if not passed:
    sys.exit(3)
