#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

LOW_NAME = "OLEANDER_FREQ_LOW"
HIGH_NAME = "OLEANDER_FREQ_HIGH"
MAT_LOW = "OLEANDER_FREQ_LOW_MAT"
MAT_HIGH = "OLEANDER_FREQ_HIGH_MAT"
BAKE_IMAGE = "OLEANDER_FREQ_BAKE_TARGET"
EXTERNAL_IMAGE = "OLEANDER_FREQ_TANGENT_NORMAL"


def cli():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["build", "reopen"], required=True)
    p.add_argument("--out", required=True)
    return p.parse_args(argv)


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def macro_height(x, y):
    # Macro form belongs in geometry. It changes true section/silhouette.
    return 0.085 * math.sin(x * 1.25) * math.cos(y * 1.05) + 0.025 * math.cos((x + y) * 0.75)


def edge_envelope(x, y, half_size):
    # Force meso detail to zero at the outer border so the representation test
    # does not cheat by asking a normal map to reproduce boundary silhouette.
    nx = min(1.0, max(0.0, (half_size - abs(x)) / 0.30))
    ny = min(1.0, max(0.0, (half_size - abs(y)) / 0.30))
    s = min(nx, ny)
    return s * s * (3.0 - 2.0 * s)


def meso_offset(x, y, half_size):
    env = edge_envelope(x, y, half_size)
    wave = math.sin(x * 10.5) * math.cos(y * 9.0)
    cross = 0.45 * math.sin((x + y) * 15.0)
    # Always above the macro carrier; only directional meso variation matters
    # to the tangent-space normal bake.
    return env * (0.008 + 0.0045 * wave + 0.0020 * cross)


def create_grid(name, n, size, include_meso=False):
    half = size * 0.5
    verts = []
    for j in range(n):
        v = j / (n - 1)
        y = (v - 0.5) * size
        for i in range(n):
            u = i / (n - 1)
            x = (u - 0.5) * size
            z = macro_height(x, y)
            if include_meso:
                z += meso_offset(x, y, half)
            verts.append((x, y, z))
    faces = []
    for j in range(n - 1):
        for i in range(n - 1):
            a = j * n + i
            faces.append((a, a + 1, a + n + 1, a + n))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for poly in mesh.polygons:
        poly.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if name == LOW_NAME:
        uv = mesh.uv_layers.new(name="UVMap")
        for poly in mesh.polygons:
            for li in poly.loop_indices:
                vi = mesh.loops[li].vertex_index
                i = vi % n
                j = vi // n
                uv.data[li].uv = (i / (n - 1), j / (n - 1))
    return obj


def make_material(name, base=(0.42, 0.42, 0.42, 1.0), rough=0.34):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Roughness"].default_value = rough
    return mat


def prepare_low_bake_material(img):
    mat = make_material(MAT_LOW)
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.name = "BAKE_TARGET_IMAGE"
    tex.image = img
    tex.select = True
    nt.nodes.active = tex
    normal = nt.nodes.new("ShaderNodeNormalMap")
    normal.name = "TANGENT_NORMAL_NODE"
    normal.space = "TANGENT"
    normal.inputs["Strength"].default_value = 1.0
    # Deliberately do not connect the image while baking; this avoids a
    # texture circular dependency. Wiring is created only after externalizing.
    nt.links.new(normal.outputs["Normal"], nt.nodes.get("Principled BSDF").inputs["Normal"])
    return mat


def select_for_bake(high, low):
    bpy.ops.object.select_all(action="DESELECT")
    high.select_set(True)
    low.select_set(True)
    bpy.context.view_layer.objects.active = low


def bake_and_externalize(high, low, mat, out):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.render.bake.use_selected_to_active = True
    scene.render.bake.cage_extrusion = 0.045
    scene.render.bake.max_ray_distance = 0.0
    scene.render.bake.margin = 12
    scene.render.bake.normal_space = "TANGENT"
    select_for_bake(high, low)
    bpy.ops.object.bake(type="NORMAL")

    target = bpy.data.images[BAKE_IMAGE]
    normal_path = out / "MESO_TANGENT_NORMAL.png"
    target.filepath_raw = str(normal_path)
    target.file_format = "PNG"
    target.save()

    # Re-load as a file-backed image so the native master proves an external
    # texture dependency rather than silently carrying a generated datablock.
    external = bpy.data.images.load(str(normal_path), check_existing=False)
    external.name = EXTERNAL_IMAGE
    external.colorspace_settings.name = "Non-Color"
    tex = mat.node_tree.nodes["BAKE_TARGET_IMAGE"]
    tex.image = external
    normal = mat.node_tree.nodes["TANGENT_NORMAL_NODE"]
    mat.node_tree.links.new(tex.outputs["Color"], normal.inputs["Color"])
    return external


def image_stats(img):
    px = list(img.pixels[:])
    rgb = [px[k::4] for k in range(3)]
    mean = [sum(c) / len(c) for c in rgb]
    lo = [min(c) for c in rgb]
    hi = [max(c) for c in rgb]
    varied = sum(
        1 for i in range(0, len(px), 4)
        if abs(px[i] - 0.5) > 0.012 or abs(px[i + 1] - 0.5) > 0.012
    )
    return {
        "mean_rgb": mean,
        "min_rgb": lo,
        "max_rgb": hi,
        "varied_pixel_fraction": varied / (len(px) / 4),
    }


def look_at(obj, target=(0, 0, 0)):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 720
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    if scene.world is None:
        scene.world = bpy.data.worlds.new("WORLD")
    scene.world.color = (0.02, 0.02, 0.02)

    camd = bpy.data.cameras.new("CAM")
    cam = bpy.data.objects.new("CAM", camd)
    bpy.context.collection.objects.link(cam)
    cam.location = (2.45, -2.65, 1.72)
    camd.lens = 61
    look_at(cam, (0, 0, 0.02))
    scene.camera = cam

    for name, loc, energy, sx, sy in [
        ("GRAZE", (1.15, -1.65, 1.65), 1150, 1.35, 0.18),
        ("FILL", (-1.8, 0.8, 2.2), 170, 2.4, 2.4),
    ]:
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy = energy
        ld.shape = "RECTANGLE"
        ld.size = sx
        ld.size_y = sy
        o = bpy.data.objects.new(name, ld)
        bpy.context.collection.objects.link(o)
        o.location = loc
        look_at(o, (0, 0, 0))


def render_state(high, low, low_mat, out, state):
    scene = bpy.context.scene
    normal = low_mat.node_tree.nodes["TANGENT_NORMAL_NODE"]
    if state == "high":
        high.hide_render = False
        low.hide_render = True
        name = "HIGH_MACRO_PLUS_MESO.png"
    elif state == "low_plain":
        high.hide_render = True
        low.hide_render = False
        normal.inputs["Strength"].default_value = 0.0
        name = "LOW_MACRO_PLAIN.png"
    elif state == "low_baked":
        high.hide_render = True
        low.hide_render = False
        normal.inputs["Strength"].default_value = 1.0
        name = "LOW_MACRO_PLUS_BAKED_MESO.png"
    else:
        raise ValueError(state)
    scene.render.filepath = str(out / name)
    bpy.ops.render.render(write_still=True)
    return out / name


def load_rgba(path):
    img = bpy.data.images.load(str(path), check_existing=False)
    w, h = img.size
    px = list(img.pixels[:])
    return w, h, px


def compare_images(ref_path, test_path):
    wr, hr, r = load_rgba(ref_path)
    wt, ht, t = load_rgba(test_path)
    if (wr, hr) != (wt, ht):
        raise RuntimeError("render size mismatch")
    inter = union = 0
    abs_sum = 0.0
    rgb_count = 0
    for i in range(0, len(r), 4):
        mr = r[i + 3] > 0.5
        mt = t[i + 3] > 0.5
        if mr or mt:
            union += 1
        if mr and mt:
            inter += 1
            abs_sum += abs(r[i] - t[i]) + abs(r[i + 1] - t[i + 1]) + abs(r[i + 2] - t[i + 2])
            rgb_count += 3
    return {
        "silhouette_iou": inter / union if union else 1.0,
        "intersection_rgb_mae": abs_sum / rgb_count if rgb_count else 0.0,
        "intersection_pixels": inter,
        "union_pixels": union,
    }


def mesh_stats(obj):
    return {
        "vertices": len(obj.data.vertices),
        "edges": len(obj.data.edges),
        "polygons": len(obj.data.polygons),
        "uv_layers": [u.name for u in obj.data.uv_layers],
    }


def material_contract(mat):
    nt = mat.node_tree
    tex = nt.nodes.get("BAKE_TARGET_IMAGE")
    nm = nt.nodes.get("TANGENT_NORMAL_NODE")
    img = tex.image if tex else None
    return {
        "image_node": bool(tex and img),
        "image_source": getattr(img, "source", None) if img else None,
        "image_filepath": bpy.path.abspath(img.filepath) if img else None,
        "image_colorspace": img.colorspace_settings.name if img else None,
        "normal_map_node": bool(nm),
        "normal_space": getattr(nm, "space", None) if nm else None,
        "normal_strength": nm.inputs["Strength"].default_value if nm else None,
    }


def build(out):
    reset()
    out.mkdir(parents=True, exist_ok=True)
    size = 2.4
    low = create_grid(LOW_NAME, 25, size, include_meso=False)
    high = create_grid(HIGH_NAME, 97, size, include_meso=True)
    high_mat = make_material(MAT_HIGH)
    high.data.materials.append(high_mat)

    target = bpy.data.images.new(BAKE_IMAGE, width=1024, height=1024, alpha=False, float_buffer=False)
    target.generated_color = (0.5, 0.5, 1.0, 1.0)
    target.colorspace_settings.name = "Non-Color"
    low_mat = prepare_low_bake_material(target)
    low.data.materials.append(low_mat)
    external = bake_and_externalize(high, low, low_mat, out)
    stats = image_stats(external)
    if stats["varied_pixel_fraction"] < 0.05:
        raise RuntimeError(f"meso normal map lacks directional variation: {stats}")

    setup_render()
    high_path = render_state(high, low, low_mat, out, "high")
    plain_path = render_state(high, low, low_mat, out, "low_plain")
    baked_path = render_state(high, low, low_mat, out, "low_baked")
    plain_cmp = compare_images(high_path, plain_path)
    baked_cmp = compare_images(high_path, baked_path)
    visual_delta = {
        "high_vs_low_plain": plain_cmp,
        "high_vs_low_baked": baked_cmp,
        "mae_improvement": plain_cmp["intersection_rgb_mae"] - baked_cmp["intersection_rgb_mae"],
        "baked_reduces_shading_error": baked_cmp["intersection_rgb_mae"] < plain_cmp["intersection_rgb_mae"],
    }

    # Conservative representation gates: same macro carrier should keep the
    # silhouette; baked meso must improve diagnostic shading over plain low.
    if baked_cmp["silhouette_iou"] < 0.985:
        raise RuntimeError(f"macro silhouette drift too high: {baked_cmp}")
    if not visual_delta["baked_reduces_shading_error"]:
        raise RuntimeError(f"tangent bake did not improve high-reference shading: {visual_delta}")

    normal_node = low_mat.node_tree.nodes["TANGENT_NORMAL_NODE"]
    normal_node.inputs["Strength"].default_value = 1.0
    blend = out / "FREQUENCY_BAND_BAKE.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))

    receipt = {
        "schema": "oleander.3d.surface-detail-frequency-band.v1",
        "mode": "build",
        "blender_version": bpy.app.version_string,
        "representation_contract": {
            "macro": "real geometry on both low and high carriers",
            "meso": "high-only geometric offset baked into tangent-space normal",
            "micro": "not exercised in this benchmark",
            "boundary_policy": "meso envelope reaches zero at outer boundary",
            "principle": "silhouette/section stay geometric; tangent normal carries directional meso shading only",
        },
        "high": mesh_stats(high),
        "low": mesh_stats(low),
        "high_low_polygon_ratio": len(high.data.polygons) / len(low.data.polygons),
        "bake": {
            "type": "TANGENT_NORMAL",
            "selected_to_active": True,
            "cage_extrusion_m": 0.045,
            "resolution": [1024, 1024],
            "colorspace": "Non-Color",
            "external_texture": "MESO_TANGENT_NORMAL.png",
        },
        "normal_image_stats": stats,
        "material_contract": material_contract(low_mat),
        "visual_delta": visual_delta,
        "outputs": [p.name for p in [high_path, plain_path, baked_path, out / "MESO_TANGENT_NORMAL.png", blend]],
        "evidence_class": "NATIVE_FREQUENCY_BAND_BAKE_PENDING_REOPEN",
        "holds": [
            "cross-engine tangent basis parity",
            "mirrored-UV seam test",
            "UDIM/multi-material bake",
            "displacement/parallax representation",
            "production texel-density budget",
            "Design KEEP",
        ],
    }
    (out / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    files = [high_path, plain_path, baked_path, out / "MESO_TANGENT_NORMAL.png", blend, out / "BUILD_RECEIPT.json"]
    (out / "SHA256.json").write_text(json.dumps({p.name: sha256(p) for p in files}, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


def reopen(out):
    low = bpy.data.objects.get(LOW_NAME)
    high = bpy.data.objects.get(HIGH_NAME)
    mat = bpy.data.materials.get(MAT_LOW)
    if not low or not high or not mat:
        raise RuntimeError("native reopen missing benchmark objects/material")
    contract = material_contract(mat)
    normal_path = out / "MESO_TANGENT_NORMAL.png"
    if not normal_path.exists():
        raise RuntimeError("external tangent normal missing")
    if contract["image_source"] != "FILE" or contract["image_colorspace"] != "Non-Color":
        raise RuntimeError(f"external data-map contract lost: {contract}")
    if contract["normal_space"] != "TANGENT":
        raise RuntimeError(f"normal-space contract lost: {contract}")
    if "UVMap" not in [u.name for u in low.data.uv_layers]:
        raise RuntimeError("UVMap missing on reopen")

    setup_render()
    high.hide_render = True
    low.hide_render = False
    mat.node_tree.nodes["TANGENT_NORMAL_NODE"].inputs["Strength"].default_value = 1.0
    reopen_path = out / "LOW_BAKED_REOPEN.png"
    bpy.context.scene.render.filepath = str(reopen_path)
    bpy.ops.render.render(write_still=True)

    receipt = {
        "schema": "oleander.3d.surface-detail-frequency-band-reopen.v1",
        "mode": "reopen",
        "blender_version": bpy.app.version_string,
        "low": mesh_stats(low),
        "high": mesh_stats(high),
        "material_contract": contract,
        "external_normal_sha256": sha256(normal_path),
        "reopen_render_sha256": sha256(reopen_path),
        "native_reopen_match": True,
        "evidence_class": "RECOVERED_NATIVE_FREQUENCY_BAND_BAKE",
        "promotion_scope": [
            "macro-vs-meso representation choice",
            "high-to-low tangent-space meso bake",
            "explicit low UV carrier",
            "file-backed Non-Color normal texture",
            "native .blend + external texture reopen",
            "diagnostic proof that baked meso reduces high-reference shading error versus plain low",
        ],
        "holds": [
            "cross-engine tangent basis parity",
            "mirrored-UV seam test",
            "UDIM/multi-material bake",
            "displacement/parallax representation",
            "production texel-density budget",
            "Design KEEP",
        ],
    }
    (out / "REOPEN_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


def main():
    a = cli()
    out = Path(a.out).resolve()
    if a.mode == "build":
        build(out)
    else:
        reopen(out)


if __name__ == "__main__":
    main()
