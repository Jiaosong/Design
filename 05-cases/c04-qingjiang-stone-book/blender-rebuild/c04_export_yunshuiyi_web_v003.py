import bpy
import hashlib
import json
import os
from pathlib import Path

OUT_DIR = Path(os.environ.get("C04_REBUILD_OUT", "/tmp/c04-yunshuiyi-rebuild"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
SOURCE_BLEND = Path(bpy.data.filepath).resolve()
SLUG = "C04_YUNSHUIYI_REBUILD_v003"


def sha256_file(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def source_objects():
    names = ["C04_YUNSHUIYI_PRIMARY_SHELL", "C04_YUNSHUIYI_CONTACT_ZONE"]
    objs = []
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != "MESH":
            raise RuntimeError(f"required Web source mesh missing: {name}")
        objs.append(obj)
    return objs


def evaluated_stats(objects):
    dg = bpy.context.evaluated_depsgraph_get()
    verts = polys = tris = 0
    for obj in objects:
        ev = obj.evaluated_get(dg)
        mesh = ev.to_mesh()
        try:
            mesh.calc_loop_triangles()
            verts += len(mesh.vertices)
            polys += len(mesh.polygons)
            tris += len(mesh.loop_triangles)
        finally:
            ev.to_mesh_clear()
    return {"vertices": verts, "polygons": polys, "triangles": tris}


def duplicate_for_lod(src_objects, lod_name, subd_level):
    col = bpy.data.collections.new(f"WEB_{lod_name}")
    bpy.context.scene.collection.children.link(col)
    out = []
    for src in src_objects:
        dup = src.copy()
        dup.data = src.data.copy()
        dup.animation_data_clear()
        dup.name = f"{src.name}__{lod_name}"
        col.objects.link(dup)
        for mod in dup.modifiers:
            if mod.type == "SUBSURF":
                mod.levels = subd_level
                mod.render_levels = subd_level
        dup["WEB_DERIVATIVE_ROLE"] = lod_name
        dup["WEB_SOURCE_OLE_ID"] = src.get("OLE_ID", "C04_YUNSHUIYI_REBUILD_MASTER_v003")
        out.append(dup)
    return col, out


def export_glb(objects, path):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.hide_render = False
        obj.hide_set(False)
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(
        filepath=str(path),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_texcoords=True,
        export_normals=True,
        export_materials="EXPORT",
        export_image_format="AUTO",
    )
    bpy.ops.object.select_all(action="DESELECT")
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"GLB export failed: {path}")


src = source_objects()
source_identity = {
    "file": SOURCE_BLEND.name,
    "bytes": SOURCE_BLEND.stat().st_size,
    "sha256": sha256_file(SOURCE_BLEND),
    "ole_id": bpy.data.objects["C04_YUNSHUIYI_PRIMARY_SHELL"].get("OLE_ID"),
}

# This rebuilt source is already lightweight. LODs are governed by subdivision
# depth, not arbitrary decimation, to preserve the authored ribbon silhouette.
lod_specs = [("LOD0", 2), ("LOD1", 1), ("LOD2", 0)]
records = []
for lod_name, subd_level in lod_specs:
    col, objs = duplicate_for_lod(src, lod_name, subd_level)
    stats = evaluated_stats(objs)
    out = OUT_DIR / f"{SLUG}_{lod_name}.glb"
    export_glb(objs, out)
    records.append({
        "lod": lod_name,
        "subdivision_level": subd_level,
        "mesh": stats,
        "glb": {"file": out.name, "bytes": out.stat().st_size, "sha256": sha256_file(out)},
        "nodes": [o.name for o in objs],
        "semantic_boundary": "primary shell + BODY_CONTACT_ZONE_DESIGN_ESTIMATE; no mechanical part claim",
    })
    for obj in list(objs):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(col)

manifest = {
    "schema": "oleander.c04.web-derivative.rebuild.v1",
    "project_id": "PRJ-C04-QINGJIANG-SHISHU",
    "object_id": "PRJ-C04-DIGITAL-INTERACTION",
    "source_authority": "C04_YUNSHUIYI_REBUILD_MASTER_v003.blend",
    "source": source_identity,
    "blender_version": bpy.app.version_string,
    "lod_strategy": "subdivision-depth derivative from Blender rebuild; no Meshy decimation",
    "lods": records,
    "holds": [
        "Design KEEP",
        "engineering/field truth",
        "source-image fidelity approval",
        "browser/runtime PASS pending browser carrier",
    ],
}
manifest_path = OUT_DIR / f"{SLUG}_WEB_MANIFEST.json"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OLEANDER_C04_WEB_MANIFEST=" + str(manifest_path))
print(json.dumps(manifest, ensure_ascii=False))
