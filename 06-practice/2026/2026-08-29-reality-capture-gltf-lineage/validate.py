from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
import pyproj
import trimesh

ROOT = Path(__file__).resolve().parent
A = ROOT / "A_geometry_only.gltf"
B = ROOT / "B_geometry_with_lineage.gltf"
SIDECAR = ROOT / "B_lineage_sidecar.json"

scene_a = trimesh.load(A, force="scene")
scene_b = trimesh.load(B, force="scene")
mesh_a = list(scene_a.geometry.values())[0]
mesh_b = list(scene_b.geometry.values())[0]
va = np.asarray(mesh_a.vertices)
vb = np.asarray(mesh_b.vertices)
side = json.loads(SIDECAR.read_text(encoding="utf-8"))

source = np.array([
    [500000.0, 1500000.0, 100.0],
    [500010.0, 1500000.0, 100.0],
    [500010.0, 1500005.0, 102.0],
    [500000.0, 1500005.0, 102.0],
])
origin = np.asarray(side["source_origin_E_N_H_m"], dtype=float)
reconstructed = np.column_stack([
    vb[:, 0] + origin[0],
    -vb[:, 2] + origin[1],
    vb[:, 1] + origin[2],
])

def sortrows(x):
    return x[np.lexsort((x[:,2], x[:,1], x[:,0]))]

a_text = A.read_text(encoding="utf-8")
crs = pyproj.CRS.from_epsg(side["source_crs"]["code"])
readback = {
    "runtime": {"trimesh": trimesh.__version__, "pyproj": pyproj.__version__},
    "source_crs_exercise": {"epsg": crs.to_epsg(), "name": crs.name},
    "a": {
        "artifact": A.name,
        "reopen_vertex_count": int(len(va)),
        "bounds_m": mesh_a.bounds.tolist(),
        "edge_01_m": float(np.linalg.norm(va[1] - va[0])),
        "contains_crs_metadata": ("EPSG" in a_text or str(crs.to_epsg()) in a_text),
        "contains_source_origin": ("500000" in a_text or "1500000" in a_text),
        "absolute_source_frame_recoverable_from_artifact_alone": False,
    },
    "b": {
        "artifact": B.name,
        "sidecar": SIDECAR.name,
        "reopen_vertex_count": int(len(vb)),
        "bounds_m": mesh_b.bounds.tolist(),
        "reconstructed_source_max_abs_error_m": float(np.max(np.abs(sortrows(reconstructed) - sortrows(source)))),
        "lineage_fields_present": all(k in side for k in ["source_crs", "source_origin_E_N_H_m", "axis_mapping", "inverse_mapping", "claim_ceiling"]),
    },
}
readback["b"]["absolute_source_frame_recoverable_with_sidecar"] = readback["b"]["reconstructed_source_max_abs_error_m"] < 1e-6
readback["verdict"] = "PROVEN_GEOMETRY_SURVIVES_GLTF_REOPEN__PROVEN_ABSOLUTE_FRAME_LOSS_WITHOUT_LINEAGE__HOLD_FIELD_SURVEY_AUTHORITY"
readback["sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [A, B, SIDECAR]}

assert readback["a"]["reopen_vertex_count"] == 4
assert abs(readback["a"]["edge_01_m"] - 10.0) < 1e-9
assert readback["a"]["contains_crs_metadata"] is False
assert readback["a"]["contains_source_origin"] is False
assert readback["b"]["lineage_fields_present"] is True
assert readback["b"]["absolute_source_frame_recoverable_with_sidecar"] is True

print(json.dumps(readback, indent=2))
