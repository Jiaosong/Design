from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import bpy


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("oleander_surface_source_adapter_v121", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import adapter: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for item in list(bpy.data.collections):
        bpy.data.collections.remove(item)


def collection(name: str):
    item = bpy.data.collections.get(name)
    if item is None:
        item = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(item)
    return item


def source_curve(name: str, family: str, target_collection, y: float):
    data = bpy.data.curves.new(name + "_DATA", "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 8
    spline = data.splines.new("NURBS")
    points = [(0.00, y, 0.00), (0.06, y * 1.1, 0.02), (0.12, y * 0.9, 0.015), (0.19, y, 0.00)]
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1.0)
        point.weight = 1.0
    spline.order_u = 4
    spline.use_endpoint_u = True
    obj = bpy.data.objects.new(name, data)
    target_collection.objects.link(obj)
    obj["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    obj["OLEANDER_ROLE"] = family
    obj["OLEANDER_EDITABLE"] = True
    obj["OLEANDER_SOURCE_FAMILY"] = family
    return obj


def source_empty(name: str, family: str, target_collection):
    obj = bpy.data.objects.new(name, None)
    target_collection.objects.link(obj)
    obj.empty_display_type = "CIRCLE"
    obj.empty_display_size = 0.012
    obj.location = (0.118, 0.0, 0.045)
    obj["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    obj["OLEANDER_ROLE"] = family
    obj["OLEANDER_EDITABLE"] = True
    obj["OLEANDER_SOURCE_FAMILY"] = family
    obj["u_center"] = 0.62
    obj["u_halfspan"] = 0.26
    obj["theta_center_rad"] = 0.0
    obj["theta_center_semantics"] = "TOP_MERIDIAN"
    obj["theta_halfspan_rad"] = 1.06
    obj["core_fraction"] = 0.29
    obj["depth_m"] = 0.012
    obj["blend"] = "QUINTIC_SMOOTHERSTEP"
    return obj


def build_sources(source_collection):
    source_curve("OL_SRC_GRIP_AXIS", "GRIP_AXIS", source_collection, 0.000)
    source_curve("OL_SRC_PALM_PROFILE", "PALM_PROFILE", source_collection, 0.025)
    source_curve("OL_SRC_THUMB_SIDE_PLAN", "THUMB_SIDE_PLAN", source_collection, 0.031)
    source_curve("OL_SRC_OPPOSITE_SIDE_PLAN", "OPPOSITE_SIDE_PLAN", source_collection, -0.026)
    lower = source_curve("OL_SRC_LOWER_RETURN_PROFILE", "LOWER_RETURN_PROFILE", source_collection, -0.020)
    lower["termination_envelope_exponent"] = 0.34
    lower["termination_envelope_semantics"] = "SHARED_CROSS_SECTION_TERMINATION_ENVELOPE"
    lower["termination_cap_onset_u"] = 0.88
    lower["termination_cap_pole_curvature_scale"] = 0.72
    lower["termination_cap_numeric_dof_count"] = 2
    source_empty("OL_SRC_INTERFACE_DECK_BOUNDARY", "INTERFACE_DECK_BOUNDARY", source_collection)


def build_target(derived_collection):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.08, location=(0.095, 0.0, 0.052))
    target = bpy.context.object
    target.name = "OL_DERIVED_SMOKE_TARGET"
    for old_collection in list(target.users_collection):
        old_collection.objects.unlink(target)
    derived_collection.objects.link(target)
    target["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_NOT_AUTHORITY"
    target["OLEANDER_ROLE"] = "SMOKE_DERIVED_EXECUTION"
    original = bpy.data.materials.new("ORIGINAL_TARGET_MATERIAL")
    target.data.materials.append(original)
    return target, original


def main():
    args = parse_args()
    adapter = load_module(Path(args.adapter).resolve())
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    binding = json.loads(Path(args.binding).read_text(encoding="utf-8"))
    binding_identity = adapter.validate_context_binding(binding, contract)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    reset_scene()
    src = collection(binding["source_authority"]["collection"])
    derived = collection("OLEANDER_DERIVED_EXECUTION")
    qa = collection("OLEANDER_QA_RIG")
    build_sources(src)
    target, original_material = build_target(derived)

    expected_names = binding["source_authority"]["expected_objects"]
    before = adapter.snapshot_source_collection(src, expected_names)
    original_slot_names = [slot.name for slot in target.data.materials]

    proxy = adapter.diagnostic_proxy(
        target,
        qa,
        before,
        name="OL_DERIVED_SMOKE_TARGET__OL_DIAGNOSTIC_PROXY",
    )
    diagnostic_material = bpy.data.materials.new("OLEANDER_DIAGNOSTIC_SMOKE_MATERIAL")
    adapter.assign_diagnostic_material(proxy, diagnostic_material)

    after = adapter.snapshot_source_collection(src, expected_names)
    unchanged = adapter.assert_source_unchanged(before, after)
    target_slots_after = [slot.name for slot in target.data.materials]
    if target_slots_after != original_slot_names or target_slots_after != [original_material.name]:
        raise RuntimeError(f"Target material slots mutated: before={original_slot_names} after={target_slots_after}")

    thumb = bpy.data.objects["OL_SRC_THUMB_SIDE_PLAN"]
    original_y = float(thumb.data.splines[0].points[2].co.y)
    thumb.data.splines[0].points[2].co.y = original_y + 0.003
    bpy.context.view_layer.update()
    edited = adapter.snapshot_source_collection(src, expected_names)
    edit_detected = adapter.source_edit_detected(before, edited)
    if not edit_detected:
        raise RuntimeError("Controlled sparse Source edit did not change authority digest")

    thumb.data.splines[0].points[2].co.y = original_y
    bpy.context.view_layer.update()
    restored = adapter.snapshot_source_collection(src, expected_names)
    adapter.assert_source_unchanged(before, restored)

    scene = bpy.context.scene
    scene["OLEANDER_SURFACE_SYSTEM"] = adapter.SYSTEM_NAME
    scene["OLEANDER_SURFACE_SYSTEM_VERSION"] = adapter.SYSTEM_VERSION
    scene["OLEANDER_SOURCE_ADAPTER_API"] = adapter.ADAPTER_API
    scene["OLEANDER_SOURCE_SNAPSHOT_SHA256"] = before["source_sha256"]
    scene["OLEANDER_SMOKE_STATUS"] = "PASS"

    adapter.write_snapshot(before, out / "SOURCE_AUTHORITY_SNAPSHOT.json")
    receipt = {
        "schema": "oleander.blender-surface-system.v1.21.source-adapter-smoke.v1",
        "status": "PASS",
        "blender_version": bpy.app.version_string,
        "adapter_system": adapter.SYSTEM_NAME,
        "adapter_version": adapter.SYSTEM_VERSION,
        "adapter_api": adapter.ADAPTER_API,
        "context_binding": binding_identity,
        "source_owner": binding["source_owner"],
        "source_object_count": len(src.objects),
        "source_sha256": before["source_sha256"],
        "source_unchanged_during_diagnostic": unchanged,
        "controlled_edit_detected": edit_detected,
        "restored_source_sha256": restored["source_sha256"],
        "target_material_slots_before": original_slot_names,
        "target_material_slots_after": target_slots_after,
        "target_material_slots_preserved": target_slots_after == original_slot_names,
        "diagnostic_proxy": {
            "name": proxy.name,
            "role": proxy.get("OLEANDER_ROLE"),
            "authority": proxy.get("OLEANDER_AUTHORITY"),
            "source_object": proxy.get("OLEANDER_DIAGNOSTIC_SOURCE_OBJECT"),
            "source_snapshot_sha256": proxy.get("OLEANDER_SOURCE_SNAPSHOT_SHA256"),
            "material_slots": [slot.name for slot in proxy.data.materials],
        },
        "boundary": contract["evidence_boundary"],
    }
    (out / "SOURCE_ADAPTER_SMOKE_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    bpy.ops.wm.save_as_mainfile(filepath=str(out / "OLEANDER_Blender_Source_Adapter_v1.21.0_SMOKE.blend"))
    print("SOURCE_ADAPTER_SMOKE_PASS", before["source_sha256"], edited["source_sha256"])


if __name__ == "__main__":
    main()
