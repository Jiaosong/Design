# Timer R54 Blender 5.2 LTS / Cycles adapter
# STATUS: Blender 5.2 LTS runtime validated; Cycles CPU smoke baseline. Production G3-G5 render not yet promoted.
import hashlib
from pathlib import Path

try:
    import bpy
    from mathutils import Vector
except ImportError as exc:
    raise RuntimeError("Run this script inside Blender 5.2 LTS or a validated compatible Blender runtime") from exc

CANONICAL_SHA = "900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66"
SOURCE_UNITS_TO_METERS = 0.001
EXPECTED_MESHES = {
    "01_Upper_Housing", "02_Formed_Diffuser", "17_Side_Knob",
    "18_Bottom_Cover", "19_Silicone_Foot_Ring", "VISUALIZATION_State_Light"
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def import_authority(glb_path):
    assert sha256(glb_path) == CANONICAL_SHA, "canonical GLB SHA mismatch"
    bpy.ops.import_scene.gltf(filepath=str(glb_path))
    roots = [o for o in bpy.context.scene.objects if o.parent is None]
    for o in roots:
        o.scale = tuple(v * SOURCE_UNITS_TO_METERS for v in o.scale)
    present = {o.name for o in bpy.context.scene.objects if o.type == "MESH"}
    missing = EXPECTED_MESHES - present
    assert not missing, f"missing expected meshes: {sorted(missing)}"

def set_cycles():
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.samples = 1024
    s.cycles.use_adaptive_sampling = True
    s.cycles.adaptive_threshold = 0.005
    s.cycles.max_bounces = 10
    s.cycles.diffuse_bounces = 4
    s.cycles.glossy_bounces = 6
    s.cycles.transmission_bounces = 10
    s.cycles.transparent_max_bounces = 8
    s.cycles.volume_bounces = 4
    s.render.resolution_x = 2400
    s.render.resolution_y = 1800
    s.render.resolution_percentage = 100
    # Blender 5.2 accepts OPEN_EXR for RenderSettings; multilayer output is routed
    # through the compositor File Output node using file_output_items.
    s.render.image_settings.file_format = "OPEN_EXR"
    s.render.image_settings.color_mode = "RGBA"
    s.render.image_settings.color_depth = "16"
    s.render.image_settings.exr_codec = "ZIP"
    s.view_settings.view_transform = "AgX"

def principled_material(name, base, metallic, rough, ior=1.5, coat=0.0, coat_rough=0.5, transmission=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bs.inputs["Base Color"].default_value = (*base, 1)
    bs.inputs["Metallic"].default_value = metallic
    bs.inputs["Roughness"].default_value = rough
    if "IOR" in bs.inputs:
        bs.inputs["IOR"].default_value = ior
    if "Coat Weight" in bs.inputs:
        bs.inputs["Coat Weight"].default_value = coat
    if "Coat Roughness" in bs.inputs:
        bs.inputs["Coat Roughness"].default_value = coat_rough
    if "Transmission Weight" in bs.inputs:
        bs.inputs["Transmission Weight"].default_value = transmission
    nt.links.new(bs.outputs["BSDF"], out.inputs["Surface"])
    return m

def assign_materials():
    # Renderer adapter only. OpenPBR JSON remains the authority material semantics.
    housing = principled_material("R54_Housing_PCABS", (0.55, 0.52, 0.48), 0.0, 0.52, 1.47, 0.035, 0.58, 0.0)
    knob = principled_material("R54_Knob_AnodizedAl", (0.56, 0.57, 0.60), 1.0, 0.23, 1.5, 0.02, 0.34, 0.0)
    diffuser = principled_material("R54_Diffuser_Opal", (0.91, 0.91, 0.88), 0.0, 0.30, 1.49, 0.0, 0.5, 0.82)
    mapping = {"01_Upper_Housing": housing, "17_Side_Knob": knob, "02_Formed_Diffuser": diffuser}
    for name, material in mapping.items():
        obj = bpy.data.objects.get(name)
        if obj:
            obj.data.materials.clear()
            obj.data.materials.append(material)

def add_area(name, size_xy, location, target, energy, color):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size = size_xy[0]
    data.size_y = size_xy[1]
    data.energy = energy
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    look_at(obj, target)
    return obj

def build_studio():
    add_area("R54_KEY_BROAD", (0.32, 0.50), (-0.19, -0.28, 0.18), (0, 0, 0.016), 520, (1.0, 0.94, 0.86))
    add_area("R54_SIDE_STRIP", (0.07, 0.40), (0.20, -0.10, 0.13), (0, 0, 0.014), 180, (0.86, 0.92, 1.0))
    add_area("R54_KNOB_SWEEP", (0.10, 0.22), (0.06, -0.25, 0.07), (0.018, -0.060, 0.011), 240, (0.95, 0.97, 1.0))
    add_area("R54_TOP_DIFFUSER", (0.26, 0.26), (-0.02, -0.04, 0.28), (0, 0, 0.028), 130, (0.90, 0.95, 1.0))

def build_camera():
    camd = bpy.data.cameras.new("R54_CMF_CAMERA")
    camd.lens = 85
    camd.sensor_width = 36
    cam = bpy.data.objects.new("R54_CMF_CAMERA", camd)
    bpy.context.collection.objects.link(cam)
    cam.location = (0.20, -0.30, 0.105)
    look_at(cam, (0.010, -0.025, 0.016))
    bpy.context.scene.camera = cam

def enable_aovs():
    vl = bpy.context.view_layer
    vl.use_pass_normal = True
    vl.use_pass_z = True
    vl.use_pass_shadow = True
    vl.use_pass_diffuse_color = True
    vl.use_pass_glossy_color = True
    vl.use_pass_transmission_color = True
    vl.use_pass_emit = True
    vl.use_pass_cryptomatte_object = True
    vl.use_pass_cryptomatte_material = True

def configure_multilayer_exr(output_exr):
    """Configure Blender 5.2 multilayer EXR through the compositor."""
    s = bpy.context.scene
    out = Path(output_exr)
    ng = bpy.data.node_groups.get("R54_Compositor_5_2") or bpy.data.node_groups.new("R54_Compositor_5_2", "CompositorNodeTree")
    ng.nodes.clear()
    s.compositing_node_group = ng
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.name = "R54_RENDER_LAYERS"
    fo = ng.nodes.new("CompositorNodeOutputFile")
    fo.name = "R54_MULTILAYER_EXR"
    fo.format.file_format = "OPEN_EXR_MULTILAYER"
    fo.format.color_depth = "16"
    fo.format.exr_codec = "ZIP"
    fo.directory = str(out.parent)
    fo.file_name = out.stem
    wanted = [
        "Image", "Depth", "Normal", "Diffuse Color", "Glossy Color",
        "Transmission Color", "Emission", "CryptoObject00", "CryptoObject01",
        "CryptoObject02", "CryptoMaterial00", "CryptoMaterial01", "CryptoMaterial02"
    ]
    for name in wanted:
        sock = rl.outputs.get(name)
        if sock is None:
            continue
        socket_type = {"VALUE": "FLOAT", "VECTOR": "VECTOR", "RGBA": "RGBA"}.get(sock.type, "RGBA")
        fo.file_output_items.new(socket_type, name)
        ng.links.new(sock, fo.inputs.get(name))
    return fo

def set_review_profile(kind="CMF"):
    s = bpy.context.scene
    s.view_settings.view_transform = "Khronos PBR Neutral" if kind == "CMF" else "AgX"
    s.view_settings.exposure = 0.0

def main(glb_path, output_exr, profile="CMF"):
    reset_scene()
    import_authority(Path(glb_path))
    set_cycles()
    assign_materials()
    build_studio()
    build_camera()
    enable_aovs()
    configure_multilayer_exr(output_exr)
    set_review_profile(profile)
    bpy.context.scene.render.filepath = str(Path(output_exr).with_name(Path(output_exr).stem + "_beauty.exr"))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(output_exr).with_suffix(".blend")))
    bpy.ops.render.render(write_still=True)

# Execute main(...) from a validated Blender 5.2 LTS runtime.
