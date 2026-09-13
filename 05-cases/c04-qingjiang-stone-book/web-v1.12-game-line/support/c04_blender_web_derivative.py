# SPDX-License-Identifier: MIT
"""C04 / Enshi high-poly OBJ -> governed Web GLB derivatives.

Run with Blender 5.x:
  blender --background --factory-startup --python c04_blender_web_derivative.py -- \
    --input /path/to/model.obj --output-dir /path/to/out --slug yunshuiyi

This script never edits the source OBJ/MTL/texture files. It imports the MASTER,
creates LOD derivatives in memory, downsizes loaded textures only in the
Blender session, exports GLB files, and writes a machine-readable manifest.

Design authority is intentionally outside this script. Target triangle counts
are runtime starting points only; Presentation/Design must reject a derivative
if silhouette, contact surfaces, proportions, material zoning, or interactive
part readability are damaged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import bpy


def sha256_file(path: Path, chunk: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def mesh_stats(objects):
    verts = 0
    polys = 0
    tris = 0
    for obj in objects:
        if obj.type != "MESH" or obj.data is None:
            continue
        mesh = obj.data
        verts += len(mesh.vertices)
        polys += len(mesh.polygons)
        mesh.calc_loop_triangles()
        tris += len(mesh.loop_triangles)
    return {"vertices": verts, "polygons": polys, "triangles": tris}


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        # Do not remove materials here: OBJ import will recreate them and images
        # may still be referenced during derivative creation.
        if datablocks is bpy.data.materials:
            continue
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def import_obj(path: Path):
    before = set(bpy.data.objects)
    if hasattr(bpy.ops.wm, "obj_import"):
        bpy.ops.wm.obj_import(filepath=str(path), forward_axis="NEGATIVE_Z", up_axis="Y")
    else:
        # Legacy fallback for pre-4.x Blender; harmless in 5.x because wm.obj_import exists.
        bpy.ops.import_scene.obj(filepath=str(path))
    imported = [obj for obj in bpy.data.objects if obj not in before]
    mesh_objects = [obj for obj in imported if obj.type == "MESH"]
    if not mesh_objects:
        raise RuntimeError(f"OBJ import produced no mesh objects: {path}")
    return imported, mesh_objects


def normalize_object_names(objects):
    seen = {}
    for index, obj in enumerate(objects):
        base = (obj.name or f"part_{index:03d}").strip().replace(" ", "_")
        n = seen.get(base, 0)
        seen[base] = n + 1
        obj.name = base if n == 0 else f"{base}__{n:02d}"


def texture_derivative(max_size: int, output_dir: Path):
    records = []
    texture_dir = output_dir / "textures"
    texture_dir.mkdir(parents=True, exist_ok=True)
    for idx, image in enumerate(list(bpy.data.images)):
        if image.type != "IMAGE" or image.source not in {"FILE", "GENERATED"}:
            continue
        width, height = int(image.size[0]), int(image.size[1])
        if width <= 0 or height <= 0:
            continue
        original = {"name": image.name, "width": width, "height": height}
        scale = min(1.0, float(max_size) / float(max(width, height)))
        target_w = max(1, int(round(width * scale)))
        target_h = max(1, int(round(height * scale)))
        if (target_w, target_h) != (width, height):
            image.scale(target_w, target_h)
        safe_name = Path(image.name).stem or f"texture_{idx:03d}"
        out = texture_dir / f"{safe_name}_{target_w}x{target_h}.png"
        try:
            image.filepath_raw = str(out)
            image.file_format = "PNG"
            image.save()
            saved = str(out)
        except Exception as exc:
            # Exporter can still embed the in-memory resized pixels; record save failure.
            saved = None
            original["save_warning"] = repr(exc)
        records.append({
            **original,
            "derived_width": target_w,
            "derived_height": target_h,
            "saved_path": saved,
        })
    return records


def duplicate_mesh_objects(source_meshes, suffix: str):
    duplicates = []
    for src in source_meshes:
        dup = src.copy()
        dup.data = src.data.copy()
        dup.name = f"{src.name}__{suffix}"
        bpy.context.scene.collection.objects.link(dup)
        duplicates.append(dup)
    return duplicates


def apply_decimate(objects, target_total_triangles: int):
    before = mesh_stats(objects)
    current = max(1, before["triangles"])
    ratio = min(1.0, max(0.001, float(target_total_triangles) / float(current)))
    if ratio >= 0.999:
        return before, before, ratio

    for obj in objects:
        if obj.type != "MESH" or obj.data is None or len(obj.data.polygons) < 8:
            continue
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        mod = obj.modifiers.new(name="OLE_WEB_DECIMATE", type="DECIMATE")
        mod.decimate_type = "COLLAPSE"
        mod.ratio = ratio
        mod.use_collapse_triangulate = True
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        finally:
            obj.select_set(False)
    after = mesh_stats(objects)
    return before, after, ratio


def export_glb(objects, out_path: Path):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(
        filepath=str(out_path),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_texcoords=True,
        export_normals=True,
        export_materials="EXPORT",
        export_image_format="AUTO",
        export_keep_originals=False,
    )
    bpy.ops.object.select_all(action="DESELECT")
    if not out_path.exists() or out_path.stat().st_size <= 0:
        raise RuntimeError(f"GLB export failed or empty: {out_path}")


def remove_objects(objects):
    for obj in objects:
        if obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj, do_unlink=True)


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--texture-max", type=int, default=2048)
    p.add_argument("--lod0", type=int, default=160000)
    p.add_argument("--lod1", type=int, default=70000)
    p.add_argument("--lod2", type=int, default=24000)
    return p.parse_args(argv)


def main():
    args = parse_args()
    source = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        raise FileNotFoundError(source)

    clear_scene()
    imported, source_meshes = import_obj(source)
    normalize_object_names(source_meshes)
    source_stats = mesh_stats(source_meshes)
    texture_records = texture_derivative(args.texture_max, output_dir)

    lod_targets = [("LOD0", args.lod0), ("LOD1", args.lod1), ("LOD2", args.lod2)]
    outputs = []
    for lod_name, target in lod_targets:
        dup = duplicate_mesh_objects(source_meshes, lod_name.lower())
        before, after, ratio = apply_decimate(dup, target)
        out = output_dir / f"C04_{args.slug}_{lod_name}.glb"
        export_glb(dup, out)
        outputs.append({
            "lod": lod_name,
            "target_triangles": target,
            "decimate_ratio": ratio,
            "mesh_before": before,
            "mesh_after": after,
            "file": out.name,
            "bytes": out.stat().st_size,
            "sha256": sha256_file(out),
        })
        remove_objects(dup)

    manifest = {
        "schema": "C04_WEB_RUNTIME_DERIVATIVE_v1",
        "design_authority": False,
        "source_read_only": True,
        "source": {
            "path": str(source),
            "bytes": source.stat().st_size,
            "sha256": sha256_file(source),
            "mesh": source_stats,
        },
        "blender": {
            "version": bpy.app.version_string,
            "background": bpy.app.background,
        },
        "texture_max": args.texture_max,
        "textures": texture_records,
        "outputs": outputs,
        "holds": [
            "Design KEEP requires visual fidelity readback.",
            "No field, engineering, ergonomics, manufacturing or constructability claim.",
            "Decimate targets are runtime starting points, not universal budgets.",
        ],
    }
    manifest_path = output_dir / f"C04_{args.slug}_WEB_DERIVATIVE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("C04_WEB_DERIVATIVE_MANIFEST=" + json.dumps(manifest, ensure_ascii=False))
    print("C04_WEB_DERIVATIVE_MANIFEST_PATH=" + str(manifest_path))


if __name__ == "__main__":
    main()
