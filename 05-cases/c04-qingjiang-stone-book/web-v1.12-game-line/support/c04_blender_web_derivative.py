# SPDX-License-Identifier: MIT
"""C04 validated Blender rebuild -> governed Web GLB derivatives.

Supports the current rebuild-first route. For .blend input, Blender must already
have opened that file on the command line; geometry is read from the GEO
collection. OBJ input remains supported for legacy diagnostic use.
"""
from __future__ import annotations

import argparse, hashlib, json, sys
from pathlib import Path
import bpy


def sha256_file(path: Path, chunk: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(chunk), b''):
            h.update(block)
    return h.hexdigest()


def evaluated_mesh_stats(objects):
    deps = bpy.context.evaluated_depsgraph_get()
    verts = polys = tris = 0
    for obj in objects:
        if obj.type != 'MESH':
            continue
        ev = obj.evaluated_get(deps)
        mesh = ev.to_mesh()
        try:
            verts += len(mesh.vertices)
            polys += len(mesh.polygons)
            mesh.calc_loop_triangles()
            tris += len(mesh.loop_triangles)
        finally:
            ev.to_mesh_clear()
    return {'vertices': verts, 'polygons': polys, 'triangles': tris}


def raw_mesh_stats(objects):
    verts = polys = tris = 0
    for obj in objects:
        if obj.type != 'MESH' or obj.data is None:
            continue
        verts += len(obj.data.vertices)
        polys += len(obj.data.polygons)
        obj.data.calc_loop_triangles()
        tris += len(obj.data.loop_triangles)
    return {'vertices': verts, 'polygons': polys, 'triangles': tris}


def import_obj(path: Path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=str(path), forward_axis='NEGATIVE_Z', up_axis='Y')
    imported = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in imported if o.type == 'MESH']
    if not meshes:
        raise RuntimeError('OBJ import produced no mesh objects')
    return meshes, 'OBJ_SOURCE_REFERENCE'


def rebuild_blend_meshes(path: Path):
    if Path(bpy.data.filepath).resolve() != path.resolve():
        bpy.ops.wm.open_mainfile(filepath=str(path))
    geo = bpy.data.collections.get('GEO')
    if geo is None:
        raise RuntimeError('validated rebuild has no GEO collection')
    meshes = [o for o in geo.all_objects if o.type == 'MESH']
    if not meshes:
        raise RuntimeError('validated rebuild GEO collection has no mesh objects')
    return meshes, 'BLENDER_REBUILD_CANDIDATE'


def source_meshes(path: Path):
    if path.suffix.lower() == '.blend':
        return rebuild_blend_meshes(path)
    if path.suffix.lower() == '.obj':
        return import_obj(path)
    raise RuntimeError(f'unsupported source type: {path.suffix}')


def texture_derivative(max_size: int, output_dir: Path):
    records = []
    texture_dir = output_dir / 'textures'
    texture_dir.mkdir(parents=True, exist_ok=True)
    for idx, image in enumerate(list(bpy.data.images)):
        if image.type != 'IMAGE' or image.source not in {'FILE', 'GENERATED'}:
            continue
        width, height = map(int, image.size[:2])
        if width <= 0 or height <= 0:
            continue
        scale = min(1.0, float(max_size) / float(max(width, height)))
        tw, th = max(1, round(width * scale)), max(1, round(height * scale))
        if (tw, th) != (width, height):
            image.scale(tw, th)
        safe = Path(image.name).stem or f'texture_{idx:03d}'
        out = texture_dir / f'{safe}_{tw}x{th}.png'
        saved = None
        warning = None
        try:
            image.filepath_raw = str(out)
            image.file_format = 'PNG'
            image.save()
            saved = str(out)
        except Exception as exc:
            warning = repr(exc)
        records.append({'name': image.name, 'width': width, 'height': height,
                        'derived_width': tw, 'derived_height': th,
                        'saved_path': saved, 'save_warning': warning})
    return records


def duplicate_mesh_objects(source, suffix):
    out = []
    for src in source:
        dup = src.copy()
        dup.data = src.data.copy()
        dup.name = f'{src.name}__{suffix}'
        bpy.context.scene.collection.objects.link(dup)
        out.append(dup)
    return out


def apply_decimate(objects, target):
    before = evaluated_mesh_stats(objects)
    current = max(1, before['triangles'])
    ratio = min(1.0, max(0.001, float(target) / float(current)))
    if ratio < 0.999:
        for obj in objects:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            mod = obj.modifiers.new('OLE_WEB_DECIMATE', 'DECIMATE')
            mod.decimate_type = 'COLLAPSE'
            mod.ratio = ratio
            mod.use_collapse_triangulate = True
            bpy.ops.object.modifier_apply(modifier=mod.name)
            obj.select_set(False)
    after = evaluated_mesh_stats(objects)
    return before, after, ratio


def export_glb(objects, path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(filepath=str(path), export_format='GLB', use_selection=True,
                              export_apply=True, export_yup=True, export_texcoords=True,
                              export_normals=True, export_materials='EXPORT',
                              export_image_format='AUTO', export_keep_originals=False)
    bpy.ops.object.select_all(action='DESELECT')
    if not path.exists() or path.stat().st_size <= 0:
        raise RuntimeError(f'empty GLB: {path}')


def remove_objects(objects):
    for o in objects:
        if o.name in bpy.data.objects:
            bpy.data.objects.remove(o, do_unlink=True)


def parse_args():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output-dir', required=True)
    p.add_argument('--slug', required=True)
    p.add_argument('--texture-max', type=int, default=2048)
    p.add_argument('--lod0', type=int, default=160000)
    p.add_argument('--lod1', type=int, default=70000)
    p.add_argument('--lod2', type=int, default=24000)
    return p.parse_args(argv)


def main():
    a = parse_args()
    src = Path(a.input).resolve()
    outdir = Path(a.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        raise FileNotFoundError(src)
    meshes, source_role = source_meshes(src)
    raw = raw_mesh_stats(meshes)
    evaluated = evaluated_mesh_stats(meshes)
    textures = texture_derivative(a.texture_max, outdir)
    outputs = []
    for lod, target in [('LOD0', a.lod0), ('LOD1', a.lod1), ('LOD2', a.lod2)]:
        dup = duplicate_mesh_objects(meshes, lod.lower())
        before, after, ratio = apply_decimate(dup, target)
        glb = outdir / f'C04_{a.slug}_{lod}.glb'
        export_glb(dup, glb)
        outputs.append({'lod': lod, 'target_triangles': target, 'decimate_ratio': ratio,
                        'mesh_before': before, 'mesh_after': after,
                        'file': glb.name, 'bytes': glb.stat().st_size,
                        'sha256': sha256_file(glb)})
        remove_objects(dup)
    manifest = {
        'schema': 'C04_WEB_RUNTIME_DERIVATIVE_v2',
        'design_authority': False,
        'source_read_only': True,
        'source_role': source_role,
        'source': {'path': str(src), 'bytes': src.stat().st_size,
                   'sha256': sha256_file(src), 'mesh_raw': raw,
                   'mesh_evaluated': evaluated},
        'blender': {'version': bpy.app.version_string, 'background': bpy.app.background},
        'texture_max': a.texture_max,
        'textures': textures,
        'outputs': outputs,
        'holds': ['Design KEEP requires Presentation/Design visual fidelity readback.',
                  'No engineering, field, ergonomics, manufacturing or constructability claim.',
                  'LOD targets are runtime starting points, not universal budgets.']
    }
    mp = outdir / f'C04_{a.slug}_WEB_DERIVATIVE_MANIFEST.json'
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print('C04_WEB_DERIVATIVE_MANIFEST=' + json.dumps(manifest, ensure_ascii=False))
    print('C04_WEB_DERIVATIVE_MANIFEST_PATH=' + str(mp))

if __name__ == '__main__':
    main()
