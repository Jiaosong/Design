#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy

OBJ_NAME = "OLEANDER_GN_NATIVE_BENCH"


def args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    return p.parse_args(argv)


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out = Path(args().out).resolve()
    obj = bpy.data.objects.get(OBJ_NAME)
    if obj is None:
        raise RuntimeError(f"missing {OBJ_NAME}")

    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps)
    mesh = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=deps)
    if len(mesh.vertices) <= 0 or len(mesh.polygons) <= 0:
        raise RuntimeError("evaluated bake produced empty mesh")

    proxy = bpy.data.objects.new("OLEANDER_GN_GLTF_BAKED_PROXY", mesh)
    bpy.context.collection.objects.link(proxy)
    bpy.ops.object.select_all(action="DESELECT")
    proxy.select_set(True)
    bpy.context.view_layer.objects.active = proxy

    glb = out / "GN_NATIVE_BENCH.glb"
    bpy.ops.export_scene.gltf(filepath=str(glb), export_format="GLB", use_selection=True)
    if not glb.exists() or glb.stat().st_size <= 1024:
        raise RuntimeError(f"GLB export missing/too small: {glb}")

    receipt = {
        "schema": "oleander.3d.geometry-nodes-export-bake.v1",
        "source_object": OBJ_NAME,
        "source_representation": "Geometry Nodes modifier on empty source mesh",
        "export_representation": "explicit evaluated static mesh proxy",
        "baked_vertices": len(mesh.vertices),
        "baked_edges": len(mesh.edges),
        "baked_polygons": len(mesh.polygons),
        "glb_bytes": glb.stat().st_size,
        "glb_sha256": sha256(glb),
        "finding": "glTF export did not implicitly preserve/evaluate the procedural dependency graph from this empty-source GN carrier; explicit evaluated-mesh bake is required for the declared exchange artifact",
        "semantic_boundary": "native GN graph remains in FC blend master; GLB is a derived static geometry carrier",
    }
    (out / "EXPORT_BAKE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")

    blend = out / "GN_NATIVE_BENCH.blend"
    preview = out / "GN_DIAGNOSTIC_PREVIEW.png"
    build_receipt = out / "BUILD_RECEIPT.json"
    files = [blend, glb, preview, build_receipt, out / "EXPORT_BAKE_RECEIPT.json"]
    (out / "BUILD_SHA256.json").write_text(json.dumps({p.name: sha256(p) for p in files}, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
