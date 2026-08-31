#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def box_mesh(name, dims):
    lx, ly, lz = dims
    x, y, z = lx / 2.0, ly / 2.0, lz / 2.0
    verts = [
        (-x,-y,-z),( x,-y,-z),( x, y,-z),(-x, y,-z),
        (-x,-y, z),( x,-y, z),( x, y, z),(-x, y, z),
    ]
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata(verts, [], faces)
    me.update()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    return obj


def plane_mesh(name, sx=10.0, sy=10.0):
    x, y = sx / 2.0, sy / 2.0
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata([(-x,-y,0),(x,-y,0),(x,y,0),(-x,y,0)], [], [(0,1,2,3)])
    me.update()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    return obj


def evaluated_mesh(obj):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps)
    me = bpy.data.meshes.new_from_object(ev, depsgraph=deps, preserve_all_data_layers=True)
    return me


def world_vertices(obj, me):
    return [obj.matrix_world @ v.co for v in me.vertices]


def bbox_size(obj, me):
    pts = world_vertices(obj, me)
    mins = [min(p[i] for p in pts) for i in range(3)]
    maxs = [max(p[i] for p in pts) for i in range(3)]
    return [maxs[i] - mins[i] for i in range(3)]


def nearest_corner_clearance(obj, me, dims):
    target = Vector((dims[0]/2.0, dims[1]/2.0, dims[2]/2.0))
    return min((obj.matrix_world @ v.co - target).length for v in me.vertices)


def mesh_topology(me):
    edge_lookup = {tuple(sorted((e.vertices[0], e.vertices[1]))): i for i, e in enumerate(me.edges)}
    counts = [0] * len(me.edges)
    for poly in me.polygons:
        vs = list(poly.vertices)
        for i, a in enumerate(vs):
            b = vs[(i + 1) % len(vs)]
            idx = edge_lookup.get(tuple(sorted((int(a), int(b)))))
            if idx is not None:
                counts[idx] += 1
    nonmanifold = sum(1 for c in counts if c != 2)
    me.calc_loop_triangles()
    volume6 = 0.0
    for tri in me.loop_triangles:
        a, b, c = [me.vertices[i].co for i in tri.vertices]
        volume6 += a.dot(b.cross(c))
    return {
        "vertices": len(me.vertices),
        "edges": len(me.edges),
        "polygons": len(me.polygons),
        "triangles": len(me.loop_triangles),
        "nonmanifold_edge_count": nonmanifold,
        "signed_volume_local": volume6 / 6.0,
    }


def remove_obj(obj):
    if obj and obj.name in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)


def run_bevel(cfg):
    dims = [cfg["box"][k] for k in ("length","width","height")]
    results = []
    for clamp in (False, True):
        for width in cfg["bevel_widths"]:
            obj = box_mesh(f"BEVEL_{'CLAMP' if clamp else 'RAW'}_{width:g}", dims)
            mod = obj.modifiers.new("BEVEL", "BEVEL")
            mod.width = float(width)
            mod.segments = int(cfg["bevel_segments"])
            mod.limit_method = 'NONE'
            mod.affect = 'EDGES'
            mod.use_clamp_overlap = clamp
            me = evaluated_mesh(obj)
            clearance = nearest_corner_clearance(obj, me, dims)
            topo = mesh_topology(me)
            results.append({
                "requested_width_mm": float(width),
                "clamp_overlap": clamp,
                "corner_clearance_mm": clearance,
                "bbox_mm": bbox_size(obj, me),
                "topology": topo,
                "requested_over_half_min_dimension": bool(float(width) >= min(dims)/2.0),
            })
            bpy.data.meshes.remove(me)
            remove_obj(obj)
    return results


def world_thickness_for_plane(scale, apply_scale_geometry, requested):
    sx, sy, sz = scale
    if apply_scale_geometry:
        obj = plane_mesh("SOLIDIFY_APPLIED", 10.0*sx, 10.0*sy)
        obj.scale = (1.0, 1.0, 1.0)
    else:
        obj = plane_mesh("SOLIDIFY_UNAPPLIED", 10.0, 10.0)
        obj.scale = (sx, sy, sz)
    mod = obj.modifiers.new("SOLIDIFY", "SOLIDIFY")
    mod.thickness = float(requested)
    mod.offset = 0.0
    mod.solidify_mode = 'EXTRUDE'
    mod.use_even_offset = True
    mod.use_quality_normals = True
    me = evaluated_mesh(obj)
    bbox = bbox_size(obj, me)
    topo = mesh_topology(me)
    rec = {
        "requested_thickness_mm": float(requested),
        "object_scale": [float(v) for v in obj.scale],
        "source_scale": [float(sx), float(sy), float(sz)],
        "scale_applied_to_geometry": bool(apply_scale_geometry),
        "observed_world_thickness_mm": bbox[2],
        "bbox_mm": bbox,
        "topology": topo,
    }
    bpy.data.meshes.remove(me)
    remove_obj(obj)
    return rec


def make_material(name, base):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*base, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.32
    return mat


def add_diag_box(name, loc, width, clamp, dims=(40,24,12)):
    obj = box_mesh(name, dims)
    obj.location = loc
    mod = obj.modifiers.new("BEVEL", "BEVEL")
    mod.width = width
    mod.segments = 4
    mod.limit_method = 'NONE'
    mod.use_clamp_overlap = clamp
    obj.data.materials.append(make_material(name + "_MAT", (0.42,0.47,0.54)))
    return obj


def add_diag_solidify(name, loc, apply_scale, requested, scale):
    sx, sy, sz = scale
    if apply_scale:
        obj = plane_mesh(name, 10*sx, 10*sy)
    else:
        obj = plane_mesh(name, 10, 10)
        obj.scale = scale
    obj.location = loc
    mod = obj.modifiers.new("SOLIDIFY", "SOLIDIFY")
    mod.thickness = requested
    mod.offset = 0.0
    mod.use_even_offset = True
    mod.use_quality_normals = True
    obj.data.materials.append(make_material(name + "_MAT", (0.58,0.50,0.40)))
    return obj


def render_diagnostic(out, cfg):
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    add_diag_box("BEVEL_SAFE", (-25, 12, 0), 3.0, True)
    add_diag_box("BEVEL_HIGH_CLAMP", (25, 12, 0), 8.0, True)
    sc = tuple(float(v) for v in cfg["solidify_unapplied_scale"])
    a = add_diag_solidify("SOLIDIFY_UNAPPLIED", (-20,-20,4), False, float(cfg["solidify_requested_thickness"]), sc)
    b = add_diag_solidify("SOLIDIFY_APPLIED", (20,-20,4), True, float(cfg["solidify_requested_thickness"]), sc)
    a.rotation_euler = (math.radians(58), 0, math.radians(-8))
    b.rotation_euler = (math.radians(58), 0, math.radians(8))

    world = bpy.data.worlds.new("WORLD")
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.025,0.025,0.03,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.25
    bpy.context.scene.world = world

    key_data = bpy.data.lights.new("KEY", type='AREA')
    key_data.energy = 1600
    key_data.shape = 'RECTANGLE'
    key_data.size = 28
    key = bpy.data.objects.new("KEY", key_data)
    key.location = (0,-45,55)
    key.rotation_euler = (math.radians(28),0,0)
    bpy.context.collection.objects.link(key)

    fill_data = bpy.data.lights.new("FILL", type='AREA')
    fill_data.energy = 900
    fill_data.size = 20
    fill = bpy.data.objects.new("FILL", fill_data)
    fill.location = (-45,20,30)
    fill.rotation_euler = (math.radians(60),0,math.radians(-55))
    bpy.context.collection.objects.link(fill)

    cam_data = bpy.data.cameras.new("CAMERA")
    cam = bpy.data.objects.new("CAMERA", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = (82,-96,78)
    direction = Vector((0,0,0)) - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z','Y').to_euler()
    cam.data.lens = 52
    bpy.context.scene.camera = cam

    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 720
    scene.render.resolution_y = 520
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(out / "BLENDER_OPERATOR_DIAGNOSTIC.png")
    scene.render.film_transparent = False
    bpy.ops.wm.save_as_mainfile(filepath=str(out / "BLENDER_OPERATOR_FAILURE_ANATOMY.blend"))
    bpy.ops.render.render(write_still=True)


def reopen(out, cfg_sha):
    path = out / "BLENDER_OPERATOR_FAILURE_ANATOMY.blend"
    bpy.ops.wm.open_mainfile(filepath=str(path))
    names = ["BEVEL_SAFE","BEVEL_HIGH_CLAMP","SOLIDIFY_UNAPPLIED","SOLIDIFY_APPLIED"]
    present = {n: (n in bpy.data.objects) for n in names}
    receipt = {
        "schema": "oleander.3d.operator-failure-anatomy.blender-reopen.v1",
        "blender_version": bpy.app.version_string,
        "config_sha256": cfg_sha,
        "objects_present": present,
        "native_reopen_valid": all(present.values()),
    }
    (out / "BLENDER_REOPEN_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    if not receipt["native_reopen_valid"]:
        raise SystemExit(9)


def build(out, cfg_path):
    cfg_all = json.loads(cfg_path.read_text())
    cfg = cfg_all["blender"]
    cfg_sha = sha256(cfg_path)
    reset_scene()
    bevel = run_bevel(cfg)
    scale = tuple(float(v) for v in cfg["solidify_unapplied_scale"])
    requested = float(cfg["solidify_requested_thickness"])
    unapplied = world_thickness_for_plane(scale, False, requested)
    applied = world_thickness_for_plane(scale, True, requested)

    clamp_hi = [r for r in bevel if r["clamp_overlap"] and math.isclose(r["requested_width_mm"], 8.0)][0]
    raw_hi = [r for r in bevel if not r["clamp_overlap"] and math.isclose(r["requested_width_mm"], 8.0)][0]
    safe = [r for r in bevel if r["clamp_overlap"] and math.isclose(r["requested_width_mm"], 3.0)][0]
    contract = {
        "safe_bevel_manifold": safe["topology"]["nonmanifold_edge_count"] == 0,
        "high_width_clamp_changes_realized_corner_clearance": clamp_hi["corner_clearance_mm"] < 8.0 * 0.95,
        "clamped_and_raw_high_width_are_not_equivalent": abs(clamp_hi["corner_clearance_mm"] - raw_hi["corner_clearance_mm"]) > 0.05,
        "solidify_unapplied_scale_changes_world_thickness": abs(unapplied["observed_world_thickness_mm"] - requested * scale[2]) < 1e-4,
        "solidify_applied_scale_restores_requested_world_thickness": abs(applied["observed_world_thickness_mm"] - requested) < 1e-4,
    }
    overall = all(contract.values())
    receipt = {
        "schema": "oleander.3d.operator-failure-anatomy.blender.v1",
        "blender_version": bpy.app.version_string,
        "config": cfg_path.name,
        "config_sha256": cfg_sha,
        "bevel": bevel,
        "solidify": {"unapplied_scale": unapplied, "applied_scale_geometry": applied},
        "contract": contract,
        "overall_pass": overall,
        "claim_boundary": cfg_all["claim_boundary"],
    }
    (out / "BLENDER_OPERATOR_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    render_diagnostic(out, cfg)
    print(json.dumps(receipt, indent=2))
    if not overall:
        raise SystemExit(8)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['build','reopen'], default='build')
    parser.add_argument('--out', required=True)
    parser.add_argument('--config')
    script_argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    args = parser.parse_args(script_argv)
    out = Path(args.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    if args.mode == 'build':
        if not args.config:
            raise SystemExit('--config required for build')
        build(out, Path(args.config).resolve())
    else:
        cfg_sha = sha256(Path(args.config).resolve()) if args.config else "UNKNOWN"
        reopen(out, cfg_sha)


if __name__ == '__main__':
    main()
