# -*- coding: utf-8 -*-
# SP02-R03 runtime evidence collector.
# RUN ONLY INSIDE A REAL RHINO 8 PROCESS WITH GRASSHOPPER AVAILABLE.
# Written to remain compatible with both Rhino 8 CPython 3 and IronPython-style execution.

from __future__ import print_function
import os
import io
import json
import datetime
import traceback
import platform
import hashlib

OUT = os.environ.get("SP02_EVIDENCE_DIR", os.path.join(os.path.expanduser("~"), "SP02_R03_runtime_evidence"))
GH_FILE = os.environ.get("SP02_GH_FILE")
EXIT_AFTER = os.environ.get("SP02_EXIT_AFTER_CAPTURE", "0") == "1"

if not os.path.isdir(OUT):
    os.makedirs(OUT)

receipt = {
    "exercise": "SP02-R03｜Runtime Closure",
    "runtime_state": "RUNTIME_STARTING",
    "timestamp_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    "gh_file": GH_FILE,
    "machine": platform.platform(),
    "errors": []
}

def path_out(name):
    return os.path.join(OUT, name)

def write_json(name, data):
    with io.open(path_out(name), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, ensure_ascii=False, indent=2))

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

try:
    import Rhino
    import Grasshopper
    from Grasshopper.Kernel import GH_DocumentIO, GH_SolutionMode
    from Grasshopper.GUI.Canvas import GH_CanvasMode

    receipt.update({
        "rhino_version": str(Rhino.RhinoApp.Version),
        "rhino_license_validated": bool(Rhino.RhinoApp.IsLicenseValidated),
        "rhino_is_evaluation": bool(Rhino.RhinoApp.IsEvaluation),
        "rhino_is_running_automated": bool(Rhino.RhinoApp.IsRunningAutomated),
        "rhino_is_running_headless": bool(Rhino.RhinoApp.IsRunningHeadless),
        "grasshopper_component_server_available": Grasshopper.Instances.ComponentServer is not None
    })

    if not GH_FILE:
        raise RuntimeError("SP02_GH_FILE is not set.")
    gh_path = os.path.abspath(GH_FILE)
    if not os.path.isfile(gh_path) or os.path.splitext(gh_path)[1].lower() not in (".gh", ".ghx"):
        raise RuntimeError("SP02_GH_FILE must point to an existing .gh or .ghx file.")

    io_doc = GH_DocumentIO()
    if not io_doc.Open(gh_path):
        raise RuntimeError("Grasshopper failed to open definition: " + gh_path)
    doc = io_doc.Document
    if doc is None:
        raise RuntimeError("GH_DocumentIO returned no document.")

    # A real Grasshopper solve. Silent is explicitly intended by the API for background solutions.
    doc.NewSolution(True, GH_SolutionMode.Silent)

    objects = []
    for obj in doc.Objects:
        objects.append({
            "name": getattr(obj, "Name", None),
            "nickname": getattr(obj, "NickName", None),
            "type": obj.GetType().FullName,
            "instance_guid": str(getattr(obj, "InstanceGuid", "")),
            "component_guid": str(getattr(obj, "ComponentGuid", "")) if hasattr(obj, "ComponentGuid") else None
        })
    write_json("component_inventory.json", {"object_count": len(objects), "objects": objects})

    def find_exact_nickname(nickname):
        hits = [o for o in doc.Objects if getattr(o, "NickName", None) == nickname]
        if len(hits) != 1:
            raise RuntimeError("Expected exactly one object nicknamed %s, got %d" % (nickname, len(hits)))
        return hits[0]

    def structure_from_object(obj):
        if hasattr(obj, "VolatileData"):
            s = obj.VolatileData
        elif hasattr(obj, "Params") and obj.Params.Output.Count > 0:
            s = obj.Params.Output[0].VolatileData
        else:
            raise RuntimeError("Object %s has no readable Grasshopper data structure." % getattr(obj, "NickName", "?"))

        paths = []
        lengths = []
        for i in range(s.PathCount):
            p = s.Path(i)
            paths.append(str(p))
            lengths.append(int(s.Branch(i).Count))
        return {
            "paths": paths,
            "branch_count": int(s.PathCount),
            "data_count": int(s.DataCount),
            "branch_lengths": lengths,
            "topology": str(s.TopologyDescription)
        }

    states = {}
    for label, nickname in {
        "BASE": "SP02_BASE",
        "GRAFT": "SP02_GRAFT",
        "FLATTEN": "SP02_FLATTEN",
        "TRANSPOSE": "SP02_TRANSPOSE",
        "ADVERSE_TRANSPOSE": "SP02_ADVERSE_TRANSPOSE"
    }.items():
        states[label] = structure_from_object(find_exact_nickname(nickname))
    write_json("tree_runtime.json", {"source_definition": gh_path, "states": states})

    required_viewers = ["PV_BASE", "PV_GRAFT", "PV_FLATTEN", "PV_TRANSPOSE", "PV_ADVERSE"]
    viewer_hits = {}
    for nick in required_viewers:
        viewer_hits[nick] = len([o for o in doc.Objects if getattr(o, "NickName", None) == nick])
    write_json("viewer_inventory.json", viewer_hits)
    if any(viewer_hits[n] != 1 for n in required_viewers):
        raise RuntimeError("CP4 viewer inventory incomplete: " + repr(viewer_hits))

    solved_dir = path_out("solved_definition")
    if not os.path.isdir(solved_dir):
        os.makedirs(solved_dir)
    solved_path = os.path.join(solved_dir, "SP02_R03_runtime_solved.ghx")
    solved_io = GH_DocumentIO(doc)
    if not solved_io.SaveQuiet(solved_path):
        raise RuntimeError("Failed to save solved GHX.")

    # Rhino viewport capture.
    try:
        from System.Drawing import Size
        active_doc = Rhino.RhinoDoc.ActiveDoc
        if active_doc and active_doc.Views.ActiveView:
            bitmap = active_doc.Views.ActiveView.CaptureToBitmap(Size(1600, 900), True, True, True)
            bitmap.Save(path_out("rhino_viewport_four_state.png"))
            receipt["rhino_viewport_capture"] = "PASS"
        else:
            receipt["rhino_viewport_capture"] = "NO_ACTIVE_VIEW"
    except Exception as exc:
        receipt["rhino_viewport_capture"] = "FAIL: " + str(exc)

    # Grasshopper canvas capture is opportunistic. GH_DocumentIO may run without a GUI canvas,
    # so absence of ActiveCanvas must remain CP4 OPEN rather than be disguised.
    try:
        canvas = Grasshopper.Instances.ActiveCanvas
        if canvas is not None:
            bitmap = canvas.GetCanvasScreenBuffer(GH_CanvasMode.Export)
            bitmap.Save(path_out("grasshopper_canvas_four_state.png"))
            receipt["grasshopper_canvas_capture"] = "PASS"
        else:
            receipt["grasshopper_canvas_capture"] = "NO_ACTIVE_CANVAS / MANUAL CP4 SCREENSHOT REQUIRED"
    except Exception as exc:
        receipt["grasshopper_canvas_capture"] = "FAIL / MANUAL CP4 SCREENSHOT REQUIRED: " + str(exc)

    receipt["runtime_state"] = "RHINO_GRASSHOPPER_EXECUTED"
    receipt["solution_object_count"] = len(objects)
    receipt["source_definition_sha256"] = sha256_file(gh_path)

except Exception as exc:
    receipt["runtime_state"] = "RUNTIME_FAIL"
    receipt["errors"].append(str(exc))
    receipt["traceback"] = traceback.format_exc()

finally:
    write_json("runtime_receipt.json", receipt)
    if EXIT_AFTER:
        try:
            import Rhino
            Rhino.RhinoApp.Exit(False)
        except Exception:
            pass
