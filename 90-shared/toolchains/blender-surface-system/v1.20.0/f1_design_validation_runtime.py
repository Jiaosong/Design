from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import bpy
from mathutils import Vector

SYSTEM_NAME = "OLEANDER Blender Surface System"
SYSTEM_VERSION = "v1.20.0"
FIDELITY = "F1_DESIGN_VALIDATION"
RUNTIME_API = "oleander.blender-surface-system.f1-runtime.v1"
SUPPORTED_RIGS = ("BROAD", "STRIP", "GRAZING")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_binding(binding: dict[str, Any], contract_path: str | Path) -> dict[str, Any]:
    surface = binding["blender_surface_system"]
    runtime = binding["runtime_binding"]
    contract_path = Path(contract_path)
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    checks = {
        "system_name_matches": surface.get("system") == SYSTEM_NAME == contract.get("system"),
        "system_version_matches": surface.get("version") == SYSTEM_VERSION == contract.get("version"),
        "fidelity_matches": surface.get("fidelity") == FIDELITY == contract.get("fidelity"),
        "runtime_api_matches": runtime.get("api") == RUNTIME_API,
        "runtime_mode_executable": runtime.get("mode") == "EXECUTABLE_SHARED_RUNTIME",
        "parallel_local_runtime_forbidden": runtime.get("local_parallel_runtime_forbidden") is True,
        "required_rigs_supported_by_surface_system": set(surface.get("required_lighting_rigs", ())).issubset(set(contract.get("lighting_rigs", ()))),
        "project_profile_has_required_rigs": set(surface.get("required_lighting_rigs", ())).issubset(set(runtime.get("project_rig_profile", {}))),
    }
    for key, ok in checks.items():
        _require(ok, f"Blender Surface System binding failed: {key}")

    return {
        "status": "PASS",
        "system": SYSTEM_NAME,
        "version": SYSTEM_VERSION,
        "fidelity": FIDELITY,
        "api": RUNTIME_API,
        "contract": str(contract_path),
        "checks": checks,
    }


def _tag(block: Any, role: str) -> Any:
    block["OLEANDER_SYSTEM"] = SYSTEM_NAME
    block["OLEANDER_SYSTEM_VERSION"] = SYSTEM_VERSION
    block["OLEANDER_FIDELITY"] = FIDELITY
    block["OLEANDER_RUNTIME_API"] = RUNTIME_API
    block["OLEANDER_ROLE"] = role
    return block


def material(name: str, color: tuple[float, float, float], roughness: float, metallic: float = 0.0):
    old = bpy.data.materials.get(name)
    if old:
        bpy.data.materials.remove(old)
    mat = _tag(bpy.data.materials.new(name), "F1_DIAGNOSTIC_MATERIAL")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    _require(bsdf is not None, "Principled BSDF missing")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = float(roughness)
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = float(metallic)
    return mat


def zebra(name: str = "OLEANDER_MAT_QA_ZEBRA_NORMAL_v1", frequency: float = 18.0):
    old = bpy.data.materials.get(name)
    if old:
        bpy.data.materials.remove(old)
    mat = _tag(bpy.data.materials.new(name), "F1_ZEBRA_NORMAL_FIELD")
    mat.use_nodes = True
    nt = mat.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mul = nt.nodes.new("ShaderNodeMath")
    sine = nt.nodes.new("ShaderNodeMath")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = float(frequency)
    sine.operation = "SINE"
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].position = 0.49
    ramp.color_ramp.elements[0].color = (0.01, 0.01, 0.01, 1.0)
    ramp.color_ramp.elements[1].position = 0.51
    ramp.color_ramp.elements[1].color = (0.96, 0.96, 0.96, 1.0)
    nt.links.new(geo.outputs["Normal"], sep.inputs[0])
    nt.links.new(sep.outputs["X"], mul.inputs[0])
    nt.links.new(mul.outputs[0], sine.inputs[0])
    nt.links.new(sine.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.22
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


def assign(obj: Any, mat: Any) -> None:
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def aim(obj: Any, target: tuple[float, float, float]) -> None:
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def camera(name: str, lens_mm: float, location: tuple[float, float, float], target: tuple[float, float, float], collection: Any):
    data = _tag(bpy.data.cameras.new(name + "_DATA"), "F1_DIAGNOSTIC_CAMERA")
    data.lens = float(lens_mm)
    obj = _tag(bpy.data.objects.new(name, data), "F1_DIAGNOSTIC_CAMERA")
    collection.objects.link(obj)
    obj.location = location
    aim(obj, target)
    return obj


def _area(spec: dict[str, Any], rig: str, target: tuple[float, float, float], collection: Any):
    name = str(spec["name"])
    data = _tag(bpy.data.lights.new(name + "_DATA", "AREA"), f"F1_{rig}_LIGHT")
    data.energy = float(spec["energy"])
    data.shape = "RECTANGLE" if "size_y" in spec else "DISK"
    data.size = float(spec["size"])
    if "size_y" in spec:
        data.size_y = float(spec["size_y"])
    obj = _tag(bpy.data.objects.new(name, data), f"F1_{rig}_LIGHT")
    collection.objects.link(obj)
    obj.location = tuple(float(v) for v in spec["location"])
    obj["OLEANDER_SURFACE_SYSTEM_RIG"] = rig
    aim(obj, target)
    obj.hide_render = True
    return obj


def _negative_card(spec: dict[str, Any], target: tuple[float, float, float], collection: Any):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=tuple(float(v) for v in spec["location"]))
    obj = bpy.context.object
    obj.name = str(spec["name"])
    for existing in list(obj.users_collection):
        existing.objects.unlink(obj)
    collection.objects.link(obj)
    obj.scale = tuple(float(v) for v in spec["scale"])
    aim(obj, target)
    mat = material(str(spec.get("material_name", "R2_NEG_FILL_MAT")), (0.002, 0.002, 0.002), 1.0, 0.0)
    assign(obj, mat)
    _tag(obj, "F1_NEGATIVE_FILL_CARD")
    obj["OLEANDER_SURFACE_SYSTEM_RIGS"] = ",".join(str(v) for v in spec.get("active_rigs", SUPPORTED_RIGS))
    return obj


def build_project_rigs(collection: Any, target: tuple[float, float, float], profile: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for rig in SUPPORTED_RIGS:
        result[rig] = [_area(spec, rig, target, collection).name for spec in profile.get(rig, ())]
    negative = profile.get("NEGATIVE_CARD")
    if negative:
        card = _negative_card(negative, target, collection)
        for rig in negative.get("active_rigs", SUPPORTED_RIGS):
            result.setdefault(str(rig), []).append(card.name)
    result["ZEBRA"] = ["OLEANDER_MAT_QA_ZEBRA_NORMAL_v1"]
    return result


def activate_rig(collection: Any, rig: str) -> None:
    for obj in collection.objects:
        if obj.type == "LIGHT":
            obj.hide_render = obj.get("OLEANDER_SURFACE_SYSTEM_RIG") != rig
    for obj in collection.objects:
        active = str(obj.get("OLEANDER_SURFACE_SYSTEM_RIGS", "")).split(",")
        if obj.get("OLEANDER_ROLE") == "F1_NEGATIVE_FILL_CARD":
            obj.hide_render = rig not in active


def render_setup(scene: Any, runtime_contract: dict[str, Any], resolution: int) -> None:
    scene.render.engine = "CYCLES"
    scene.cycles.samples = int(runtime_contract["cycles_samples"])
    scene.cycles.use_denoising = bool(runtime_contract["denoise"])
    if hasattr(scene.cycles, "use_adaptive_sampling"):
        scene.cycles.use_adaptive_sampling = bool(runtime_contract["adaptive_sampling"])
    scene.render.resolution_x = int(resolution)
    scene.render.resolution_y = int(resolution)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.color = (0.018, 0.018, 0.022)
    scene["OLEANDER_SURFACE_SYSTEM"] = SYSTEM_NAME
    scene["OLEANDER_SURFACE_SYSTEM_VERSION"] = SYSTEM_VERSION
    scene["OLEANDER_SURFACE_SYSTEM_FIDELITY"] = FIDELITY
    scene["OLEANDER_SURFACE_SYSTEM_RUNTIME_API"] = RUNTIME_API

    view = scene.view_layers[0]
    for attr in (
        "use_pass_z",
        "use_pass_normal",
        "use_pass_diffuse_color",
        "use_pass_glossy_direct",
        "use_pass_glossy_indirect",
        "use_pass_glossy_color",
        "use_pass_shadow",
    ):
        if hasattr(view, attr):
            setattr(view, attr, True)


def render(scene: Any, out: Path, stem: str, cam: Any, obj: Any, mat: Any, rig: str, qa_collection: Any) -> str:
    scene.camera = cam
    assign(obj, mat)
    activate_rig(qa_collection, rig)
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "8"
    scene.render.filepath = str(Path(out) / f"{stem}.png")
    bpy.ops.render.render(write_still=True)
    return f"{stem}.png"


def master_exr(scene: Any, out: Path, cam: Any, obj: Any, mat: Any, qa_collection: Any) -> str:
    scene.camera = cam
    assign(obj, mat)
    activate_rig(qa_collection, "BROAD")
    scene.render.image_settings.file_format = "OPEN_EXR"
    scene.render.image_settings.color_depth = "32"
    if hasattr(scene.render.image_settings, "exr_codec"):
        scene.render.image_settings.exr_codec = "ZIP"
    path = Path(out) / "G1_R2_BASELINE_MASTER.exr"
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "8"
    return path.name
