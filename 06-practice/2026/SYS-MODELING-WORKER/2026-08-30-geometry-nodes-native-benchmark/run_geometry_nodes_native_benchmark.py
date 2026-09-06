#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

OBJ_NAME = "OLEANDER_GN_NATIVE_BENCH"
GROUP_NAME = "OLEANDER_GN_FIELD_INSTANCE_SYSTEM"
ATTR_NAME = "oleander_height"


def cli_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["build", "reopen"], required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--realize", type=int, choices=[0, 1], required=True)
    return p.parse_args(argv)


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def set_input(node, name, value):
    sock = node.inputs.get(name)
    if sock is None:
        raise RuntimeError(f"missing input {name!r} on {node.bl_idname}")
    sock.default_value = value


def link(tree, out_socket, in_socket):
    if out_socket is None or in_socket is None:
        raise RuntimeError("attempted to link a missing socket")
    tree.links.new(out_socket, in_socket)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_material():
    mat = bpy.data.materials.new("OLEANDER_GN_DIAGNOSTIC_MAT")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.19, 0.32, 0.46, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.34
        if bsdf.inputs.get("Metallic"):
            bsdf.inputs["Metallic"].default_value = 0.0
    return mat


def add_interface_socket(ng, name, in_out, socket_type, default=None, min_value=None, max_value=None):
    s = ng.interface.new_socket(name=name, in_out=in_out, socket_type=socket_type)
    if default is not None and hasattr(s, "default_value"):
        s.default_value = default
    if min_value is not None and hasattr(s, "min_value"):
        s.min_value = min_value
    if max_value is not None and hasattr(s, "max_value"):
        s.max_value = max_value
    return s


def build_node_group(realize: bool, material):
    ng = bpy.data.node_groups.new(GROUP_NAME, "GeometryNodeTree")
    add_interface_socket(ng, "Geometry", "INPUT", "NodeSocketGeometry")
    add_interface_socket(ng, "Geometry", "OUTPUT", "NodeSocketGeometry")
    add_interface_socket(ng, "Grid Size", "INPUT", "NodeSocketFloat", 4.0, 1.0, 20.0)
    add_interface_socket(ng, "Resolution", "INPUT", "NodeSocketInt", 17, 3, 128)
    add_interface_socket(ng, "Amplitude", "INPUT", "NodeSocketFloat", 0.42, 0.0, 2.0)
    add_interface_socket(ng, "Frequency", "INPUT", "NodeSocketFloat", 1.35, 0.1, 10.0)

    nodes = ng.nodes
    nodes.clear()
    group_in = nodes.new("NodeGroupInput")
    group_out = nodes.new("NodeGroupOutput")
    group_in.location = (-1100, 100)
    group_out.location = (1050, 100)

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.location = (-900, 250)
    link(ng, group_in.outputs["Grid Size"], grid.inputs["Size X"])
    link(ng, group_in.outputs["Grid Size"], grid.inputs["Size Y"])
    link(ng, group_in.outputs["Resolution"], grid.inputs["Vertices X"])
    link(ng, group_in.outputs["Resolution"], grid.inputs["Vertices Y"])

    pos = nodes.new("GeometryNodeInputPosition")
    sep = nodes.new("ShaderNodeSeparateXYZ")
    sep.location = (-900, -220)
    link(ng, pos.outputs["Position"], sep.inputs["Vector"])

    mul_x = nodes.new("ShaderNodeMath")
    mul_x.operation = "MULTIPLY"
    mul_x.location = (-700, -330)
    link(ng, sep.outputs["X"], mul_x.inputs[0])
    link(ng, group_in.outputs["Frequency"], mul_x.inputs[1])

    mul_y = nodes.new("ShaderNodeMath")
    mul_y.operation = "MULTIPLY"
    mul_y.location = (-700, -180)
    link(ng, sep.outputs["Y"], mul_y.inputs[0])
    link(ng, group_in.outputs["Frequency"], mul_y.inputs[1])

    sin_x = nodes.new("ShaderNodeMath")
    sin_x.operation = "SINE"
    sin_x.location = (-520, -330)
    link(ng, mul_x.outputs[0], sin_x.inputs[0])

    cos_y = nodes.new("ShaderNodeMath")
    cos_y.operation = "COSINE"
    cos_y.location = (-520, -180)
    link(ng, mul_y.outputs[0], cos_y.inputs[0])

    wave = nodes.new("ShaderNodeMath")
    wave.operation = "MULTIPLY"
    wave.location = (-340, -250)
    link(ng, sin_x.outputs[0], wave.inputs[0])
    link(ng, cos_y.outputs[0], wave.inputs[1])

    height = nodes.new("ShaderNodeMath")
    height.operation = "MULTIPLY"
    height.location = (-160, -250)
    link(ng, wave.outputs[0], height.inputs[0])
    link(ng, group_in.outputs["Amplitude"], height.inputs[1])

    combine = nodes.new("ShaderNodeCombineXYZ")
    combine.location = (20, -220)
    link(ng, height.outputs[0], combine.inputs["Z"])

    set_pos = nodes.new("GeometryNodeSetPosition")
    set_pos.location = (-80, 240)
    link(ng, grid.outputs["Mesh"], set_pos.inputs["Geometry"])
    link(ng, combine.outputs["Vector"], set_pos.inputs["Offset"])

    store = nodes.new("GeometryNodeStoreNamedAttribute")
    store.location = (120, 240)
    store.data_type = "FLOAT"
    store.domain = "POINT"
    set_input(store, "Name", ATTR_NAME)
    link(ng, set_pos.outputs["Geometry"], store.inputs["Geometry"])
    link(ng, height.outputs[0], store.inputs["Value"])

    to_points = nodes.new("GeometryNodeMeshToPoints")
    to_points.mode = "VERTICES"
    to_points.location = (300, 10)
    set_input(to_points, "Radius", 0.05)
    link(ng, store.outputs["Geometry"], to_points.inputs["Mesh"])

    cube = nodes.new("GeometryNodeMeshCube")
    cube.location = (300, -220)
    set_input(cube, "Size", (0.12, 0.12, 0.22))
    set_input(cube, "Vertices X", 2)
    set_input(cube, "Vertices Y", 2)
    set_input(cube, "Vertices Z", 2)

    inst = nodes.new("GeometryNodeInstanceOnPoints")
    inst.location = (500, 10)
    link(ng, to_points.outputs["Points"], inst.inputs["Points"])
    link(ng, cube.outputs["Mesh"], inst.inputs["Instance"])

    instance_geometry = inst.outputs["Instances"]
    if realize:
        realize_node = nodes.new("GeometryNodeRealizeInstances")
        realize_node.location = (670, -20)
        link(ng, instance_geometry, realize_node.inputs["Geometry"])
        instance_geometry = realize_node.outputs["Geometry"]

    join = nodes.new("GeometryNodeJoinGeometry")
    join.location = (780, 150)
    link(ng, store.outputs["Geometry"], join.inputs["Geometry"])
    link(ng, instance_geometry, join.inputs["Geometry"])

    set_mat = nodes.new("GeometryNodeSetMaterial")
    set_mat.location = (900, 150)
    set_mat.inputs["Material"].default_value = material
    link(ng, join.outputs["Geometry"], set_mat.inputs["Geometry"])
    link(ng, set_mat.outputs["Geometry"], group_out.inputs["Geometry"])

    return ng


def make_object(realize: bool):
    mesh = bpy.data.meshes.new("OLEANDER_GN_SOURCE_EMPTY")
    obj = bpy.data.objects.new(OBJ_NAME, mesh)
    bpy.context.collection.objects.link(obj)
    mat = make_material()
    ng = build_node_group(realize, mat)
    mod = obj.modifiers.new("OLEANDER_GN_SYSTEM", "NODES")
    mod.node_group = ng
    return obj, ng


def look_at(obj, target=(0, 0, 0)):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_scene(obj, out: Path):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 720
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    if scene.world is None:
        scene.world = bpy.data.worlds.new("OLEANDER_GN_WORLD")
    scene.world.color = (0.035, 0.035, 0.035)

    cam_data = bpy.data.cameras.new("GN_DIAGNOSTIC_CAMERA")
    cam = bpy.data.objects.new("GN_DIAGNOSTIC_CAMERA", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = (5.2, -5.2, 4.0)
    cam_data.lens = 52
    look_at(cam, (0, 0, 0.15))
    scene.camera = cam

    for name, loc, energy, size in [
        ("KEY", (3.5, -2.0, 5.5), 1150.0, 4.5),
        ("FILL", (-3.0, -1.0, 3.2), 650.0, 3.0),
    ]:
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy = energy
        ld.shape = "DISK"
        ld.size = size
        lo = bpy.data.objects.new(name, ld)
        bpy.context.collection.objects.link(lo)
        lo.location = loc
        look_at(lo, (0, 0, 0))

    scene.render.filepath = str(out / "GN_DIAGNOSTIC_PREVIEW.png")


def evaluated_stats(obj):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps)
    mesh = ev.to_mesh()
    try:
        verts = [v.co.copy() for v in mesh.vertices]
        if verts:
            mins = [float(min(v[i] for v in verts)) for i in range(3)]
            maxs = [float(max(v[i] for v in verts)) for i in range(3)]
        else:
            mins = maxs = [0.0, 0.0, 0.0]
        attr = mesh.attributes.get(ATTR_NAME)
        return {
            "vertices": len(mesh.vertices),
            "edges": len(mesh.edges),
            "polygons": len(mesh.polygons),
            "bbox_min": mins,
            "bbox_max": maxs,
            "named_attribute": {
                "present": attr is not None,
                "domain": getattr(attr, "domain", None) if attr else None,
                "data_type": getattr(attr, "data_type", None) if attr else None,
            },
        }
    finally:
        ev.to_mesh_clear()


def node_contract(ng):
    types = [n.bl_idname for n in ng.nodes]
    return {
        "node_count": len(ng.nodes),
        "node_types": sorted(types),
        "instance_on_points_count": types.count("GeometryNodeInstanceOnPoints"),
        "realize_instances_count": types.count("GeometryNodeRealizeInstances"),
        "store_named_attribute_count": types.count("GeometryNodeStoreNamedAttribute"),
        "field_contract": "Position.x/y -> frequency -> sin/cos -> amplitude -> Set Position Z + Store Named Attribute(point)",
        "instance_contract": "Mesh Grid vertices -> Mesh to Points -> Cube Instance on Points",
        "random_seed_policy": "DETERMINISTIC_NO_RANDOMNESS",
        "attribute": {"name": ATTR_NAME, "domain": "POINT", "data_type": "FLOAT"},
        "parameters": {"grid_size_m": 4.0, "resolution_xy": 17, "amplitude_m": 0.42, "frequency": 1.35},
    }


def select_only(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def export_glb(obj, path: Path):
    select_only(obj)
    bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB", use_selection=True)


def roundtrip_glb(path: Path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    total_v = sum(len(o.data.vertices) for o in meshes)
    total_p = sum(len(o.data.polygons) for o in meshes)
    has_nodes_modifier = any(any(m.type == "NODES" for m in o.modifiers) for o in meshes)
    world_pts = []
    for o in meshes:
        for v in o.data.vertices:
            world_pts.append(o.matrix_world @ v.co)
    if world_pts:
        mins = [float(min(v[i] for v in world_pts)) for i in range(3)]
        maxs = [float(max(v[i] for v in world_pts)) for i in range(3)]
    else:
        mins = maxs = [0.0, 0.0, 0.0]
    return {
        "mesh_objects": len(meshes),
        "vertices": total_v,
        "polygons": total_p,
        "bbox_min": mins,
        "bbox_max": maxs,
        "geometry_nodes_modifier_preserved": has_nodes_modifier,
        "semantic_loss": "GLB carries evaluated/static geometry; Blender Geometry Nodes graph is not preserved" if not has_nodes_modifier else "UNEXPECTED_GN_PRESERVED",
    }


def build(out: Path, realize: bool):
    clear_scene()
    obj, ng = make_object(realize)
    setup_scene(obj, out)
    stats = evaluated_stats(obj)
    if stats["vertices"] <= 0 or stats["polygons"] <= 0:
        raise RuntimeError(f"empty evaluated geometry: {stats}")
    if not stats["named_attribute"]["present"]:
        raise RuntimeError(f"named attribute {ATTR_NAME!r} missing from evaluated mesh")

    blend = out / "GN_NATIVE_BENCH.blend"
    glb = out / "GN_NATIVE_BENCH.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.render.render(write_still=True)
    export_glb(obj, glb)

    receipt = {
        "schema": "oleander.3d.geometry-nodes-native-benchmark.v1",
        "mode": "build",
        "blender_version": bpy.app.version_string,
        "object": OBJ_NAME,
        "node_group": GROUP_NAME,
        "realize_instances_policy": bool(realize),
        "native_master": blend.name,
        "exchange": glb.name,
        "preview": "GN_DIAGNOSTIC_PREVIEW.png",
        "node_contract": node_contract(ng),
        "evaluated": stats,
        "evidence_class": "NATIVE_EXECUTED_PENDING_REOPEN",
        "does_not_prove": ["Geometry Nodes design quality", "target-runtime parity", "performance fitness", "plugin superiority"],
    }
    (out / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    hashes = {p.name: sha256(p) for p in [blend, glb, out / "GN_DIAGNOSTIC_PREVIEW.png", out / "BUILD_RECEIPT.json"]}
    (out / "BUILD_SHA256.json").write_text(json.dumps(hashes, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


def reopen(out: Path, realize: bool):
    obj = bpy.data.objects.get(OBJ_NAME)
    if obj is None:
        raise RuntimeError(f"missing object {OBJ_NAME}")
    mods = [m for m in obj.modifiers if m.type == "NODES"]
    if len(mods) != 1 or mods[0].node_group is None:
        raise RuntimeError("expected exactly one Geometry Nodes modifier")
    ng = mods[0].node_group
    contract = node_contract(ng)
    expected_realize_count = 1 if realize else 0
    if contract["realize_instances_count"] != expected_realize_count:
        raise RuntimeError({"expected_realize_count": expected_realize_count, "contract": contract})

    reopened = evaluated_stats(obj)
    build_receipt = json.loads((out / "BUILD_RECEIPT.json").read_text())
    built = build_receipt["evaluated"]
    for key in ["vertices", "edges", "polygons"]:
        if reopened[key] != built[key]:
            raise RuntimeError(f"reopen topology mismatch {key}: {reopened[key]} != {built[key]}")
    for key in ["bbox_min", "bbox_max"]:
        if any(abs(a - b) > 1e-6 for a, b in zip(reopened[key], built[key])):
            raise RuntimeError(f"reopen bbox mismatch {key}: {reopened[key]} != {built[key]}")

    glb = out / "GN_NATIVE_BENCH.glb"
    glb_roundtrip = roundtrip_glb(glb)
    if glb_roundtrip["geometry_nodes_modifier_preserved"]:
        raise RuntimeError("unexpected Geometry Nodes modifier survived GLB roundtrip")
    if glb_roundtrip["vertices"] <= 0 or glb_roundtrip["polygons"] <= 0:
        raise RuntimeError(f"empty GLB roundtrip: {glb_roundtrip}")

    receipt = {
        "schema": "oleander.3d.geometry-nodes-native-reopen.v1",
        "mode": "reopen",
        "blender_version": bpy.app.version_string,
        "realize_instances_policy": bool(realize),
        "node_contract": contract,
        "native_reopen": reopened,
        "glb_roundtrip": glb_roundtrip,
        "native_reopen_match": True,
        "evidence_class": "RECOVERED_NATIVE_WITH_DCC_ROUNDTRIP",
        "promotion_scope": [
            "Geometry Nodes fields/attribute-domain/instance-policy native execution",
            "native .blend reopen stability for declared benchmark",
            "GLB semantic-loss readback: evaluated geometry survives while GN graph does not",
        ],
        "holds": ["browser/engine target runtime", "performance profiling", "visual Design KEEP"],
    }
    (out / "REOPEN_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


def main():
    args = cli_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.mode == "build":
        build(out, bool(args.realize))
    else:
        reopen(out, bool(args.realize))


if __name__ == "__main__":
    main()
