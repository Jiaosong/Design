"""Headless validation for Stage 3 procedural/relationship foundations.

Validates two narrowly scoped capabilities in real Blender:
1. parameter/constraint metadata can mutate and persist without masquerading as
   a solver or silently changing geometry;
2. a governed Geometry Nodes passthrough group can be created, evaluated and
   reopened with provenance intact.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import bpy

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import oleander_blender
from oleander_blender.geometry_diff import diff_from_baseline, store_baseline
from oleander_blender.parametric import add_constraint, get_constraints, get_parameters, set_constraints, set_parameters, update_parameter
from oleander_blender.procedural import (
    PROCEDURAL_SCHEMA,
    create_passthrough_geometry_nodes,
    describe_geometry_nodes_binding,
    mesh_evaluated_counts,
)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def source_fingerprint():
    paths = [
        path
        for path in ADDON_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}
    ]
    paths.append(SCRIPT)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        rel = path.relative_to(PIPELINE_ROOT).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def add_cube(name):
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def find_by_ole_id(scene, ole_id):
    for obj in scene.objects:
        if getattr(obj, "oleander", None) and obj.oleander.ole_id == ole_id:
            return obj
    return None


def main():
    if hasattr(bpy.types.Object, "oleander"):
        try:
            oleander_blender.unregister()
        except Exception:
            pass
    oleander_blender.register()

    clear_scene()
    obj = add_cube("OLE_STAGE3_PROCEDURAL_SOURCE")
    obj.oleander.ole_id = "OLE_STAGE3_PROCEDURAL_SOURCE"
    obj.oleander.semantic_class = "procedural_test_part"

    # Metadata contract: mutations must serialize deterministically, filter
    # unsupported nested payloads, and remain geometry-neutral without a solver.
    store_baseline(obj)
    set_parameters(obj, {"width_mm": 1200.0, "enabled": True, "nested": {"bad": 1}})
    update_parameter(obj, "spacing_mm", 600.0)
    params = get_parameters(obj)
    assert_true(params == {"enabled": True, "spacing_mm": 600.0, "width_mm": 1200.0}, f"unexpected parameter payload: {params!r}")

    set_constraints(
        obj,
        [
            {"type": "EQUAL_SPACING", "axis": "X", "distance_mm": 600.0, "nested": {"ignored": True}},
            {"axis": "Y"},
        ],
    )
    add_constraint(obj, "LOCK_AXIS", axis="Z", enabled=True)
    constraints = get_constraints(obj)
    assert_true(len(constraints) == 2, f"only typed constraints should persist; got {constraints!r}")
    assert_true(constraints[0] == {"axis": "X", "distance_mm": 600.0, "type": "EQUAL_SPACING"}, f"constraint sanitization mismatch: {constraints[0]!r}")
    assert_true(constraints[1] == {"axis": "Z", "enabled": True, "type": "LOCK_AXIS"}, f"constraint append mismatch: {constraints[1]!r}")

    metadata_diff = diff_from_baseline(obj)
    assert_true(metadata_diff["status"] == "UNCHANGED", "parameter/constraint metadata must not silently mutate geometry without a solver")

    # Geometry Nodes probe: create a traceable passthrough modifier and prove
    # evaluated geometry is unchanged while the procedural binding is real.
    raw_counts = {"vertices": len(obj.data.vertices), "edges": len(obj.data.edges), "polygons": len(obj.data.polygons)}
    modifier, node_group = create_passthrough_geometry_nodes(obj)
    bpy.context.view_layer.update()
    evaluated_counts = mesh_evaluated_counts(obj)
    assert_true(evaluated_counts == raw_counts, f"passthrough Geometry Nodes must preserve mesh counts: raw={raw_counts}, evaluated={evaluated_counts}")
    assert_true(modifier.type == "NODES", "Geometry Nodes binding must use a NODES modifier")
    assert_true(node_group.bl_idname == "GeometryNodeTree", "node group must be a GeometryNodeTree")
    assert_true(node_group.get("oleander_schema") == PROCEDURAL_SCHEMA, "node group must carry governed procedural schema")
    assert_true(node_group.get("oleander_source_ole_id") == obj.oleander.ole_id, "node group provenance must bind source OLE ID")
    assert_true(node_group.get("oleander_solver_claim") is False, "procedural probe must explicitly deny solver claim")

    bindings = describe_geometry_nodes_binding(obj)
    assert_true(len(bindings) == 1, f"expected one governed GN binding; got {bindings!r}")
    binding = bindings[0]
    assert_true(binding["schema"] == PROCEDURAL_SCHEMA, "described binding schema mismatch")
    assert_true(binding["node_count"] == 2 and binding["link_count"] == 1, f"passthrough group topology mismatch: {binding!r}")
    assert_true(not binding["solver_claim"], "described GN binding must not imply solver authority")

    reopen_path = "/tmp/oleander-stage3-procedural-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    assert_true(pathlib.Path(reopen_path).is_file(), "procedural fixture .blend should be written")
    bpy.ops.wm.open_mainfile(filepath=reopen_path)

    obj = find_by_ole_id(bpy.context.scene, "OLE_STAGE3_PROCEDURAL_SOURCE")
    assert_true(obj is not None, "source OLE ID must survive procedural save/reopen")
    assert_true(get_parameters(obj) == params, "parameter metadata must survive save/reopen")
    assert_true(get_constraints(obj) == constraints, "constraint metadata must survive save/reopen")
    reopened_bindings = describe_geometry_nodes_binding(obj)
    assert_true(len(reopened_bindings) == 1, "Geometry Nodes modifier/group must survive save/reopen")
    assert_true(reopened_bindings[0]["source_ole_id"] == "OLE_STAGE3_PROCEDURAL_SOURCE", "reopened node group provenance must retain OLE ID")
    assert_true(reopened_bindings[0]["schema"] == PROCEDURAL_SCHEMA, "reopened node group schema must persist")
    assert_true(mesh_evaluated_counts(obj) == raw_counts, "reopened passthrough GN evaluation must preserve mesh counts")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_PROCEDURAL_FOUNDATION",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "parameter_metadata_mutation_api",
            "parameter_metadata_sanitization",
            "constraint_metadata_mutation_api",
            "constraint_metadata_sanitization",
            "metadata_mutation_does_not_claim_solver_geometry",
            "geometry_nodes_tree_creation",
            "geometry_nodes_modifier_binding",
            "geometry_nodes_passthrough_evaluation",
            "geometry_nodes_ole_provenance",
            "geometry_nodes_explicit_no_solver_claim",
            "geometry_nodes_save_reopen_persistence",
            "parameter_constraint_save_reopen_persistence",
        ],
        "non_claims": [
            "solver_backed_constraints",
            "houdini_equivalence",
            "cad_brep",
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_PROCEDURAL_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
