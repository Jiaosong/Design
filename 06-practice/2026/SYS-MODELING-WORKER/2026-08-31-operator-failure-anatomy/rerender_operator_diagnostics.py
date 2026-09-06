#!/usr/bin/env python3
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def set_visible(names):
    wanted = set(names)
    for name in ('BEVEL_SAFE','BEVEL_HIGH_CLAMP','SOLIDIFY_UNAPPLIED','SOLIDIFY_APPLIED'):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_render = name not in wanted


def set_camera(location, target, lens=58):
    cam = bpy.data.objects.get('CAMERA')
    cam.location = location
    aim(cam, target)
    cam.data.lens = lens


def render(path):
    scene = bpy.context.scene
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    args = ap.parse_args(argv)
    out = Path(args.out).resolve()

    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 900
    scene.render.resolution_y = 620
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False

    world = scene.world
    if world and world.use_nodes:
        bg = world.node_tree.nodes.get('Background')
        bg.inputs['Color'].default_value = (0.055,0.055,0.065,1)
        bg.inputs['Strength'].default_value = 0.48

    # Existing lights were created for provenance but were not aimed at the carriers.
    # Aim them explicitly; this changes only the diagnostic readback, not evaluated geometry.
    key = bpy.data.objects.get('KEY')
    if key:
        key.data.energy = 3200
        key.data.size = 34
        key.location = (5,-50,62)
        aim(key, (0,0,0))
    fill = bpy.data.objects.get('FILL')
    if fill:
        fill.data.energy = 1900
        fill.data.size = 26
        fill.location = (-52,-5,38)
        aim(fill, (0,0,0))

    rim_data = bpy.data.lights.get('RIM') or bpy.data.lights.new('RIM', type='AREA')
    rim_data.energy = 2400
    rim_data.size = 24
    rim = bpy.data.objects.get('RIM') or bpy.data.objects.new('RIM', rim_data)
    if rim.name not in bpy.context.collection.objects:
        bpy.context.collection.objects.link(rim)
    rim.location = (52,35,52)
    aim(rim, (0,0,0))

    # Raise diffuse albedo only for diagnostic visibility; roughness and geometry stay unchanged.
    material_targets = {
        'BEVEL_SAFE_MAT': (0.62,0.68,0.76,1),
        'BEVEL_HIGH_CLAMP_MAT': (0.62,0.68,0.76,1),
        'SOLIDIFY_UNAPPLIED_MAT': (0.78,0.62,0.42,1),
        'SOLIDIFY_APPLIED_MAT': (0.78,0.62,0.42,1),
    }
    for name, rgba in material_targets.items():
        mat = bpy.data.materials.get(name)
        if mat and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get('Principled BSDF')
            if bsdf:
                bsdf.inputs['Base Color'].default_value = rgba
                bsdf.inputs['Roughness'].default_value = 0.38

    # Combined overview.
    set_visible(['BEVEL_SAFE','BEVEL_HIGH_CLAMP','SOLIDIFY_UNAPPLIED','SOLIDIFY_APPLIED'])
    set_camera((82,-96,78), (0,0,0), 52)
    render(out / 'BLENDER_OPERATOR_DIAGNOSTIC.png')

    # Close-up A: safe vs clamped high-width bevel.
    set_visible(['BEVEL_SAFE','BEVEL_HIGH_CLAMP'])
    set_camera((68,-62,45), (0,12,0), 64)
    render(out / 'BLENDER_BEVEL_DIAGNOSTIC.png')

    # Close-up B: same requested Solidify thickness with unapplied vs applied source scale.
    set_visible(['SOLIDIFY_UNAPPLIED','SOLIDIFY_APPLIED'])
    set_camera((50,-68,25), (0,-20,3), 72)
    render(out / 'BLENDER_SOLIDIFY_DIAGNOSTIC.png')

    # Restore all carriers visible and persist the diagnostic state separately from the original evidence master.
    set_visible(['BEVEL_SAFE','BEVEL_HIGH_CLAMP','SOLIDIFY_UNAPPLIED','SOLIDIFY_APPLIED'])
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'BLENDER_OPERATOR_DIAGNOSTIC_READBACK.blend'))


if __name__ == '__main__':
    main()
