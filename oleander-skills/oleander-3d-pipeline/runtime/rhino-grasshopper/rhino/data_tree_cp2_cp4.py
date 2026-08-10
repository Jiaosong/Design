"""OLEANDER SP02 — real Rhino + Grasshopper Data Tree runtime job.

IMPORTANT STATUS
----------------
This file is an UNEXECUTED BOOTSTRAP until it is run inside a live Rhino 8.11+
instance with Grasshopper through `rhinocode`. Its existence in GitHub is not
runtime evidence and MUST NOT close CP2 or CP4.

The script intentionally uses real Grasshopper SDK data structures and document
objects. Base/Graft/Flatten are solved through a real GH_Document. Transpose is
materialized as a real GH_Structure<GH_Point> so its topology can be inspected.
A native Path Mapper object is placed and connected when available, but CP4 is
kept HOLD unless native mapping configuration is positively detected and
captured.
"""

import json
import os
import traceback
from datetime import datetime, timezone

import Rhino
import Grasshopper
from Grasshopper.Kernel import GH_Document, GH_DocumentIO, GH_DataMapping, IGH_Param
from Grasshopper.Kernel.Data import GH_Path, GH_Structure
from Grasshopper.Kernel.Types import GH_Point
from Rhino.Geometry import Point3d
from System.Drawing import PointF, Size
from System.Drawing.Imaging import ImageFormat


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def runtime_root():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def load_job():
    path = os.environ.get("OLEANDER_RHINO_JOB")
    if not path:
        path = os.path.join(runtime_root(), "jobs", "cp2_cp4_data_tree.json")
    with open(path, "r", encoding="utf-8-sig") as f:
        return path, json.load(f)


def ensure_out():
    path = os.environ.get("OLEANDER_RHINO_OUT") or os.path.join(runtime_root(), "runtime-state")
    os.makedirs(path, exist_ok=True)
    return path


def tree_summary(tree):
    paths = list(tree.Paths)
    counts = []
    labels = []
    for p in paths:
        branch = tree.get_Branch(p)
        counts.append(branch.Count)
        labels.append(str(p))
    return {
        "branch_count": int(tree.PathCount),
        "item_count": int(tree.DataCount),
        "paths": labels,
        "items_per_branch": counts,
        "topology": str(tree.TopologyDescription),
    }


def build_base(zones, items_per_zone, dx, dy):
    tree = GH_Structure[GH_Point]()
    for z in range(zones):
        p = GH_Path(z)
        for i in range(items_per_zone):
            tree.Append(GH_Point(Point3d(i * dx, z * dy, 0.0)), p)
    return tree


def build_transpose(zones, items_per_zone, dx, dy):
    tree = GH_Structure[GH_Point]()
    for i in range(items_per_zone):
        p = GH_Path(i)
        for z in range(zones):
            tree.Append(GH_Point(Point3d(i * dx, z * dy, 0.0)), p)
    return tree


def proxy_by_name(name, category=None):
    candidates = []
    for proxy in Grasshopper.Instances.ComponentServer.ObjectProxies:
        try:
            if str(proxy.Desc.Name).lower() != name.lower():
                continue
            if category and str(proxy.Desc.Category).lower() != category.lower():
                continue
            candidates.append(proxy)
        except Exception:
            pass
    return candidates[0] if candidates else None


def new_object(name, category=None):
    proxy = proxy_by_name(name, category)
    if proxy is None:
        return None
    return proxy.CreateInstance()


def place(obj, x, y):
    obj.CreateAttributes()
    obj.Attributes.Pivot = PointF(float(x), float(y))


def connect(source, target):
    """Connect source parameter to a component/parameter target."""
    if target is None:
        return False
    try:
        if isinstance(target, IGH_Param):
            target.AddSource(source)
            return True
    except Exception:
        pass
    try:
        inputs = target.Params.Input
        if inputs.Count > 0:
            inputs[0].AddSource(source)
            return True
    except Exception:
        pass
    return False


def make_point_param(doc, tree, nickname, x, y):
    obj = new_object("Point", "Params") or new_object("Point")
    if obj is None:
        raise RuntimeError("Native Grasshopper Point parameter could not be instantiated from ComponentServer")
    if not hasattr(obj, "SetPersistentData"):
        raise RuntimeError("Resolved 'Point' object is not a persistent point parameter")
    obj.NickName = nickname
    place(obj, x, y)
    obj.SetPersistentData(tree)
    if not doc.AddObject(obj, False):
        raise RuntimeError("Failed to add Point parameter to GH_Document")
    return obj


def make_mapped_point_param(doc, source, nickname, mapping, x, y):
    obj = new_object("Point", "Params") or new_object("Point")
    if obj is None:
        raise RuntimeError("Native Grasshopper Point parameter could not be instantiated")
    obj.NickName = nickname
    obj.DataMapping = mapping
    place(obj, x, y)
    obj.AddSource(source)
    if not doc.AddObject(obj, False):
        raise RuntimeError("Failed to add mapped Point parameter")
    return obj


def make_viewer(doc, source, nickname, x, y):
    viewer = new_object("Param Viewer")
    if viewer is None:
        return None, False
    try:
        viewer.NickName = nickname
    except Exception:
        pass
    place(viewer, x, y)
    if not doc.AddObject(viewer, False):
        return None, False
    return viewer, connect(source, viewer)


def capture_canvas(canvas, path):
    bmp = canvas.CreatePreview(Size(1800, 1200))
    if bmp is None:
        raise RuntimeError("Grasshopper canvas CreatePreview returned None")
    bmp.Save(path, ImageFormat.Png)
    bmp.Dispose()


def capture_viewport(path):
    rdoc = Rhino.RhinoDoc.ActiveDoc
    if rdoc is None or rdoc.Views.ActiveView is None:
        raise RuntimeError("No active Rhino view available")
    rdoc.Views.Redraw()
    bmp = rdoc.Views.ActiveView.CaptureToBitmap(Size(1600, 1000), True, True, True)
    if bmp is None:
        raise RuntimeError("Rhino CaptureToBitmap returned None")
    bmp.Save(path, ImageFormat.Png)
    bmp.Dispose()


def expected_match(actual, expected):
    if actual["branch_count"] != int(expected["branch_count"]):
        return False
    if actual["item_count"] != int(expected["item_count"]):
        return False
    exp_items = expected.get("items_per_branch")
    if isinstance(exp_items, list):
        return actual["items_per_branch"] == [int(v) for v in exp_items]
    if exp_items == "1 each":
        return all(v == 1 for v in actual["items_per_branch"])
    return True


out_dir = ensure_out()
job_path, job = load_job()
receipt = {
    "run_id": job.get("run_id"),
    "job_type": job.get("job_type"),
    "timestamp": utc_now(),
    "host": "LIVE RHINO REQUIRED",
    "status": "RUNTIME JOB STARTED",
    "outputs": {},
    "cp2": {"status": "OPEN"},
    "cp4": {"status": "OPEN"},
    "errors": [],
    "warnings": [],
    "evidence_boundary": [
        "This receipt is valid runtime evidence only if generated inside a live Rhino process through rhinocode.",
        "CP4 remains HOLD unless native Path Mapper configuration and before/after viewer evidence are both present.",
        "Training evidence is not engineering approval, construction approval, safety verification or project acceptance."
    ]
}

try:
    if job.get("job_type") != "data_tree_cp2_cp4":
        raise RuntimeError("Wrong job type for this script")

    p = job["input"]["parameters"]
    zones = int(p["zones"])
    items_per_zone = int(p["items_per_zone"])
    dx = float(p["dx"])
    dy = float(p["dy"])

    # Ensure real Grasshopper UI/runtime is loaded.
    Rhino.RhinoApp.RunScript("_Grasshopper", False)
    canvas = Grasshopper.Instances.ActiveCanvas
    if canvas is None:
        raise RuntimeError("Grasshopper SDK loaded but no active GH_Canvas is available")

    doc = GH_Document()
    Grasshopper.Instances.DocumentServer.AddDocument(doc)
    canvas.Document = doc
    doc.Enabled = True

    # BASE — real GH_Structure persisted in a real native Point parameter.
    base_tree = build_base(zones, items_per_zone, dx, dy)
    base_param = make_point_param(doc, base_tree, "BASE 4x6", 80, 120)
    base_viewer, base_viewer_connected = make_viewer(doc, base_param, "VIEW BASE", 320, 120)
    doc.NewSolution(True)

    before_png = os.path.join(out_dir, "grasshopper_canvas_before.png")
    capture_canvas(canvas, before_png)
    receipt["outputs"]["grasshopper_canvas_before_png"] = before_png

    # GRAFT / FLATTEN — use native parameter DataMapping inside real GH solution.
    graft_param = make_mapped_point_param(doc, base_param, "GRAFT 24x1", GH_DataMapping.Graft, 80, 360)
    flatten_param = make_mapped_point_param(doc, base_param, "FLATTEN 1x24", GH_DataMapping.Flatten, 80, 600)
    graft_viewer, graft_viewer_connected = make_viewer(doc, graft_param, "VIEW GRAFT", 320, 360)
    flatten_viewer, flatten_viewer_connected = make_viewer(doc, flatten_param, "VIEW FLATTEN", 320, 600)

    # TRANSPOSE target — real GH_Structure. This is the expected Path Mapper result.
    transpose_tree = build_transpose(zones, items_per_zone, dx, dy)
    transpose_param = make_point_param(doc, transpose_tree, "TRANSPOSE 6x4", 760, 360)
    transpose_viewer, transpose_viewer_connected = make_viewer(doc, transpose_param, "VIEW TRANSPOSE", 1000, 360)

    # Place and connect a native Path Mapper if available. We deliberately do not
    # fake its internal mapping rule. CP4 only closes after mapping configuration
    # can be positively inspected in a live host run.
    path_mapper = new_object("Path Mapper")
    native_path_mapper_present = path_mapper is not None
    native_path_mapper_connected = False
    path_mapper_properties = []
    if path_mapper is not None:
        try:
            path_mapper.NickName = "PATH MAPPER — CONFIGURE / INSPECT"
        except Exception:
            pass
        place(path_mapper, 560, 120)
        doc.AddObject(path_mapper, False)
        native_path_mapper_connected = connect(base_param, path_mapper)
        try:
            path_mapper_properties = sorted({str(prop.Name) for prop in path_mapper.GetType().GetProperties()})
        except Exception:
            path_mapper_properties = []

    doc.NewSolution(True)

    tree_report = {
        "generated_at": utc_now(),
        "source": "real Grasshopper GH_Structure / GH_Document runtime",
        "parameter_provenance": job["input"].get("parameter_provenance"),
        "BASE": tree_summary(base_param.VolatileData),
        "GRAFT": tree_summary(graft_param.VolatileData),
        "FLATTEN": tree_summary(flatten_param.VolatileData),
        "TRANSPOSE_BY_ITEM": tree_summary(transpose_param.VolatileData),
        "viewer_evidence": {
            "base": bool(base_viewer_connected),
            "graft": bool(graft_viewer_connected),
            "flatten": bool(flatten_viewer_connected),
            "transpose": bool(transpose_viewer_connected)
        },
        "path_mapper": {
            "native_object_present": native_path_mapper_present,
            "input_connected": native_path_mapper_connected,
            "runtime_property_names": path_mapper_properties,
            "mapping_configuration_proven": False
        }
    }

    tree_report_path = os.path.join(out_dir, "tree_report.json")
    with open(tree_report_path, "w", encoding="utf-8") as f:
        json.dump(tree_report, f, ensure_ascii=False, indent=2)
    receipt["outputs"]["tree_report"] = tree_report_path

    expected = job["expected_tree_contracts"]
    cp2_checks = {
        key: expected_match(tree_report[key], expected[key])
        for key in ("BASE", "GRAFT", "FLATTEN", "TRANSPOSE_BY_ITEM")
    }
    receipt["cp2"] = {
        "checks": cp2_checks,
        "status": "RUNTIME TREE CONTRACT PASS" if all(cp2_checks.values()) else "RUNTIME TREE CONTRACT FAIL"
    }

    # Save the real Grasshopper document.
    gh_path = os.path.join(out_dir, "OLEANDER_SP02_DataTree_CP2_CP4_Runtime_001.gh")
    io = GH_DocumentIO(doc)
    if not io.SaveQuiet(gh_path):
        raise RuntimeError("GH_DocumentIO.SaveQuiet failed")
    receipt["outputs"]["gh_file"] = gh_path

    after_png = os.path.join(out_dir, "grasshopper_canvas_after.png")
    capture_canvas(canvas, after_png)
    receipt["outputs"]["grasshopper_canvas_after_png"] = after_png

    viewport_png = os.path.join(out_dir, "rhino_viewport.png")
    capture_viewport(viewport_png)
    receipt["outputs"]["rhino_viewport_png"] = viewport_png

    # CP4: intentionally fail closed. A real native Path Mapper exists/connected
    # only proves infrastructure. It does not prove the required mapping rule.
    if native_path_mapper_present and native_path_mapper_connected and base_viewer_connected and transpose_viewer_connected:
        receipt["cp4"] = {
            "status": "HOLD — NATIVE PATH MAPPER CONFIGURATION NOT YET PROVEN",
            "before_canvas": before_png,
            "after_canvas": after_png,
            "native_path_mapper_present": True,
            "native_path_mapper_connected": True,
            "mapping_configuration_proven": False
        }
    else:
        receipt["cp4"] = {
            "status": "HOLD — REQUIRED NATIVE VIEWER / PATH MAPPER EVIDENCE INCOMPLETE",
            "native_path_mapper_present": native_path_mapper_present,
            "native_path_mapper_connected": native_path_mapper_connected,
            "mapping_configuration_proven": False
        }

    receipt["status"] = (
        "REAL RHINO/GRASSHOPPER JOB EXECUTED / CP2 RUNTIME CONTRACT PASS / CP4 HOLD"
        if receipt["cp2"]["status"] == "RUNTIME TREE CONTRACT PASS"
        else "REAL RHINO/GRASSHOPPER JOB EXECUTED / CP2 FAIL / CP4 HOLD"
    )

except Exception as exc:
    receipt["status"] = "RUNTIME JOB FAIL"
    receipt["errors"].append({
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc()
    })

receipt_path = os.path.join(out_dir, "job_receipt.json")
with open(receipt_path, "w", encoding="utf-8") as f:
    json.dump(receipt, f, ensure_ascii=False, indent=2, default=str)

print("OLEANDER_JOB_RECEIPT=" + receipt_path)
print("OLEANDER_JOB_STATUS=" + receipt["status"])
print("OLEANDER_CP2_STATUS=" + receipt["cp2"].get("status", "OPEN"))
print("OLEANDER_CP4_STATUS=" + receipt["cp4"].get("status", "OPEN"))
