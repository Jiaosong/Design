# SPDX-License-Identifier: MIT
"""C04 validated Blender rebuild -> governed Web GLB derivatives.

For the rebuild-first route, .blend input is the Web Source Authority. Existing
rebuild modifiers are evaluated and baked into temporary derivative meshes
before LOD decimation, so the Web decimator never mutates or reorders the
validated rebuild stack. OBJ remains supported only for legacy diagnostics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy


def sha256_file(path: Path, chunk: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def mesh_stats(objects, evaluated=True):
    deps = bpy.context.evaluated_depsgraph_get()
    verts = polys = tris = 0
    for obj in objects:
        if obj.type != "MESH":
            continue
        if evaluated:
            ev = obj.evaluated_get(deps)
            mesh = ev.to_mesh()
            try:
                verts += len(mesh.vertices)
                polys += len(mesh.polygons)
                mesh.calc_loop_triangles()
                tris += len(mesh.loop_triangles)
            finally:
                ev.to_mesh_clear()
        else:
            mesh = obj.data
            verts += len(mesh.vertices)
            polys += len(mesh.polygons)
            mesh.calc_loop_triangles()
            tris += len(mesh.loop_triangles)
    return {"vertices": verts, "polygons": polys, "triangles": tris}


def source_meshes(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".blend":
        if Path(bpy.data.filepath).resolve() != path.resolve():
            bpy.ops.wm.open_mainfile(filepath=str(path))
        geo = bpy.data.collections.get("GEO")
        if geo is None:
            raise RuntimeError("validated rebuild has no GEO collection")
        meshes = [o for o in geo.all_objects if o.type == "MESH"]
        if not meshes:
            raise RuntimeError("validated rebuild GEO collection has no mesh objects")
        return meshes, "BLENDER_REBUILD_CANDIDATE"
    if suffix == ".obj":
        bpy.ops.wm.read_factory_settings(use_empty=True)
        before = set(bpy.data.objects)
        bpy.ops.wm.obj_import(filepath=str(path), forward_axis="NEGATIVE_Z", up_axis="Y")
        meshes = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
        if not meshes:
            raise RuntimeError("OBJ import produced no mesh objects")
        return meshes, "OBJ_SOURCE_REFERENCE"
    raise RuntimeError(f"unsupported source type: {suffix}")


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
        scale = min(1.0, float(max_size) / float(max(width, height)))
        tw = max(1, int(round(width * scale)))
        th = max(1, int(round(height * scale)))
        if (tw, th) != (width, height):
            image.scale(tw, th)
        out = texture_dir / f"{Path(image.name).stem or f'texture_{idx:03d}'}_{tw}x{th}.png"
        saved = None
        warning = None
        try:
            image.filepath_raw = str(out)
            image.file_format = "PNG"
            image.save()
            saved = str(out)
        except Exception as exc:
            warning = repr(exc)
        records.append({"name": image.name, "width": width, "height": height,
                        "derived_width": tw, "derived_height": th,
                        "saved_path": saved, "save_warning": warning})
    return records


def bake_evaluated_objects(source, suffix):
    """Create temporary mesh objects from evaluated rebuild geometry.

    This is deliberately derivative-only: source objects/modifier stacks remain
    untouched. The baked objects contain no inherited modifiers, so LOD
    decimation runs against exactly the evaluated geometry measured here.
    """
    deps = bpy.context.evaluated_depsgraph_get()
    baked = []
    for src in source:
        ev = src.evaluated_get(deps)
        mesh = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=deps)
        obj = bpy.data.objects.new(f"{src.name}__{suffix}", mesh)
        obj.matrix_world = src.matrix_world.copy()
        bpy.context.scene.collection.objects.link(obj)
        baked.append(obj)
    return baked


def apply_decimate(objects, target):
    before = mesh_stats(objects, evaluated=False)
    current = max(1, before["triangles"])
    ratio = min(1.0, max(0.001, float(target) / float(current)))
    if ratio < 0.999:
        for obj in objects:
            if len(obj.data.polygons) < 8:
                continue
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            mod = obj.modifiers.new("OLE_WEB_DECIMATE", "DECIMATE")
            mod.decimate_type = "COLLAPSE"
            mod.ratio = ratio
            mod.use_collapse_triangulate = True
            bpy.ops.object.modifier_apply(modifier=mod.name)
            obj.select_set(False)
    after = mesh_stats(objects, evaluated=False)
    return before, after, ratio


def export_glb(objects, path: Path):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB", use_selection=True,
                              export_apply=True, export_yup=True, export_texcoords=True,
                              export_normals=True, export_materials="EXPORT",
                              export_image_format="AUTO", export_keep_originals=False)
    bpy.ops.object.select_all(action="DESELECT")
    if not path.exists() or path.stat().st_size <= 0:
        raise RuntimeError(f"empty GLB: {path}")


def remove_objects(objects):
    for obj in objects:
        if obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj, do_unlink=True)


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
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
    a = parse_args()
    src = Path(a.input).resolve()
    outdir = Path(a.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        raise FileNotFoundError(src)

    meshes, source_role = source_meshes(src)
    raw = mesh_stats(meshes, evaluated=False)
    evaluated = mesh_stats(meshes, evaluated=True)
    textures = texture_derivative(a.texture_max, outdir)

    outputs = []
    for lod, target in (("LOD0", a.lod0), ("LOD1", a.lod1), ("LOD2", a.lod2)):
        baked = bake_evaluated_objects(meshes, lod.lower())
        before, after, ratio = apply_decimate(baked, target)
        glb = outdir / f"C04_{a.slug}_{lod}.glb"
        export_glb(baked, glb)
        outputs.append({"lod": lod, "target_triangles": target,
                        "decimate_ratio": ratio, "mesh_before": before,
                        "mesh_after": after, "file": glb.name,
                        "bytes": glb.stat().st_size, "sha256": sha256_file(glb),
                        "target_met": after["triangles"] <= max(target, int(target * 1.02))})
        remove_objects(baked)

    manifest = {
        "schema": "C04_WEB_RUNTIME_DERIVATIVE_v3",
        "design_authority": False,
        "source_read_only": True,
        "source_role": source_role,
        "source": {"path": str(src), "bytes": src.stat().st_size,
                   "sha256": sha256_file(src), "mesh_raw": raw,
                   "mesh_evaluated": evaluated},
        "blender": {"version": bpy.app.version_string, "background": bpy.app.background},
        "derivative_method": "BAKE_EVALUATED_GEOMETRY_THEN_DECIMATE",
        "texture_max": a.texture_max,
        "textures": textures,
        "outputs": outputs,
        "holds": ["Design KEEP requires Presentation/Design visual fidelity readback.",
                  "No engineering, field, ergonomics, manufacturing or constructability claim.",
                  "LOD targets are runtime starting points, not universal budgets."]
    }
    mp = outdir / f"C04_{a.slug}_WEB_DERIVATIVE_MANIFEST.json"
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("C04_WEB_DERIVATIVE_MANIFEST=" + json.dumps(manifest, ensure_ascii=False))
    print("C04_WEB_DERIVATIVE_MANIFEST_PATH=" + str(mp))

    unmet = [x for x in outputs if not x["target_met"]]
    if unmet:
        raise SystemExit("LOD target not met: " + json.dumps(unmet, ensure_ascii=False))


if __name__ == "__main__":
    main()
