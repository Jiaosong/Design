from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def rounded(values, digits: int = 6):
    return [round(float(x), digits) for x in values]


def bbox_world(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    mins = [min(c[i] for c in corners) for i in range(3)]
    maxs = [max(c[i] for c in corners) for i in range(3)]
    return {
        "min": rounded(mins),
        "max": rounded(maxs),
        "center": rounded([(mins[i] + maxs[i]) / 2 for i in range(3)]),
        "dims": rounded([maxs[i] - mins[i] for i in range(3)]),
    }


def plan_gap(a, b):
    ab = bbox_world(a)
    bb = bbox_world(b)
    x_gap = max(0.0, bb["min"][0] - ab["max"][0], ab["min"][0] - bb["max"][0])
    y_gap = max(0.0, bb["min"][1] - ab["max"][1], ab["min"][1] - bb["max"][1])
    x_overlap = max(0.0, min(ab["max"][0], bb["max"][0]) - max(ab["min"][0], bb["min"][0]))
    y_overlap = max(0.0, min(ab["max"][1], bb["max"][1]) - max(ab["min"][1], bb["min"][1]))
    return {
        "x_gap_m": round(x_gap, 6),
        "y_gap_m": round(y_gap, 6),
        "euclidean_gap_m": round(math.hypot(x_gap, y_gap), 6),
        "plan_overlap_area_m2": round(x_overlap * y_overlap, 6),
    }


def scene_fingerprint_payload():
    rows = []
    for obj in sorted(bpy.context.scene.objects, key=lambda o: o.name):
        rows.append(
            {
                "name": obj.name,
                "type": obj.type,
                "location": rounded(obj.location),
                "rotation_euler": rounded(obj.rotation_euler),
                "scale": rounded(obj.scale),
                "dimensions": rounded(obj.dimensions),
                "hide_render": bool(obj.hide_render),
                "hide_viewport": bool(obj.hide_viewport),
                "data": getattr(getattr(obj, "data", None), "name", None),
                "parent": obj.parent.name if obj.parent else None,
            }
        )
    return rows


def snapshot(label: str):
    payload = scene_fingerprint_payload()
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    edit008 = []
    for name in [
        "V06O8_TrueSteppedCanopy_LowerRibbon",
        "V06O8_TrueSteppedCanopy_UpperRibbon",
        "V06O8_TrueSteppedCanopy_Fold_01",
    ]:
        obj = bpy.data.objects.get(name)
        edit008.append(
            {
                "name": name,
                "exists": obj is not None,
                "hide_render": bool(obj.hide_render) if obj else None,
                "hide_viewport": bool(obj.hide_viewport) if obj else None,
            }
        )
    chairs = []
    for name in [f"V05_DiningChair_{i:02d}_ProfessionalProxy" for i in range(1, 5)]:
        obj = bpy.data.objects.get(name)
        chairs.append(
            {
                "name": name,
                "exists": obj is not None,
                "loc": rounded(obj.location) if obj else None,
                "rot_z": round(float(obj.rotation_euler.z), 8) if obj else None,
            }
        )
    material_users = {
        name: int(bpy.data.materials[name].users) if name in bpy.data.materials else 0
        for name in [
            "FW_PottsvilleSandstone_SurfaceVisualV2",
            "FW_StainlessSteel",
            "FW_DisplayProxy_DarkMaterial_Open",
            "FW_DisplayProxy_FurnishingWood_Open",
            "FW_DarkGapVoid_DisplayProxy",
            "FW_DarkMetalDetail_AlloyFinishOpen_VisualProxy",
            "FW_DarkCoatedComponent_IdentityOpen_VisualProxy",
            "FW_DressingDesk_WoodSpeciesFinishOpen_GrainX_VisualProxy",
            "FW_DressingDesk_WoodSpeciesFinishOpen_GrainZ_VisualProxy",
        ]
    }
    return {
        "label": label,
        "scene_fingerprint_sha256": hashlib.sha256(raw).hexdigest().upper(),
        "active_object_count": len(bpy.context.scene.objects),
        "chairs": chairs,
        "edit008_candidates": edit008,
        "material_users": material_users,
    }


def furniture_audit(blend_path: Path):
    table = bpy.data.objects.get("V05_DropLeafDiningTable_ProfessionalProxy")
    chair_names = [f"V05_DiningChair_{i:02d}_ProfessionalProxy" for i in range(1, 5)]
    chairs = [bpy.data.objects.get(name) for name in chair_names]
    missing = [name for name, obj in zip(chair_names, chairs) if obj is None]
    if table is None:
        missing.append("V05_DropLeafDiningTable_ProfessionalProxy")
    dining = []
    locked = []
    expected_y = [1.35, 1.35, 0.465, 2.235]
    if table and not missing:
        tc = Vector(bbox_world(table)["center"][:2])
        for idx, chair in enumerate(chairs):
            cc3 = bbox_world(chair)["center"]
            cc = Vector(cc3[:2])
            to_table = tc - cc
            if to_table.length:
                to_table.normalize()
            local_facing = Vector((0.0, -1.0, 0.0))
            world_facing3 = chair.matrix_world.to_3x3() @ local_facing
            world_facing = Vector((world_facing3.x, world_facing3.y))
            if world_facing.length:
                world_facing.normalize()
            facing_dot = round(float(world_facing.dot(to_table)), 6)
            gap = plan_gap(chair, table)
            dining.append(
                {
                    "root": chair.name,
                    "loc": rounded(chair.location),
                    "rot_z_deg": round(math.degrees(float(chair.rotation_euler.z)) % 360, 6),
                    "bbox": bbox_world(chair),
                    "facing_dot_to_table": facing_dot,
                    "plan_relation_to_table": gap,
                }
            )
            locked.append(
                {
                    "chair": idx + 1,
                    "y_expected": expected_y[idx],
                    "y_actual": round(float(chair.location.y), 6),
                    "y_pass": abs(float(chair.location.y) - expected_y[idx]) <= 1e-5,
                    "facing_dot_expected": 1.0,
                    "facing_dot_actual": facing_dot,
                    "facing_pass": facing_dot >= 0.999,
                    "clearance_expected_m": 0.185,
                    "clearance_actual_m": gap["euclidean_gap_m"],
                    "clearance_pass": abs(gap["euclidean_gap_m"] - 0.185) <= 1e-4,
                }
            )
    stool = bpy.data.objects.get("V06_KitchenCompactStool_PlanDerivedProxy")
    worktable = bpy.data.objects.get("V05_WrightKitchenWorkTable_Assembly")
    kitchen = None
    if stool and worktable:
        kitchen = {
            "root": stool.name,
            "loc": rounded(stool.location),
            "rot_z_deg": round(math.degrees(float(stool.rotation_euler.z)) % 360, 6),
            "bbox": bbox_world(stool),
            "worktable_root": worktable.name,
            "worktable_bbox": bbox_world(worktable),
            "plan_relation_to_worktable": plan_gap(stool, worktable),
        }
    banquette = bpy.data.objects.get("V05_LivingBanquette_ProfessionalProxy")
    banquette_row = None
    if banquette:
        facing3 = banquette.matrix_world.to_3x3() @ Vector((0.0, -1.0, 0.0))
        banquette_row = {
            "root": banquette.name,
            "loc": rounded(banquette.location),
            "rot_z_deg": round(math.degrees(float(banquette.rotation_euler.z)) % 360, 6),
            "bbox": bbox_world(banquette),
            "seated_facing_xy": rounded((facing3.x, facing3.y)),
        }
    all_pass = bool(locked) and len(locked) == 4 and all(
        row["y_pass"] and row["facing_pass"] and row["clearance_pass"] for row in locked
    )
    return {
        "status": "PASS" if not missing and all_pass else "HOLD",
        "blend_sha256": sha256(blend_path),
        "blend_bytes": blend_path.stat().st_size,
        "dining_table_bbox": bbox_world(table) if table else None,
        "dining": dining,
        "edit011_locked_invariants": locked,
        "all_edit011_invariants_pass": all_pass,
        "missing_required_objects": missing,
        "kitchen_compact_stool": kitchen,
        "living_banquette": banquette_row,
        "authority_note": "Dining use logic is current-project spatial logic; exact historic furniture coordinates remain OPEN. Kitchen stool and banquette exact historic placements remain OPEN unless separately sourced.",
        "does_not_prove": ["historic exactness", "engineering approval", "field verification", "Design KEEP"],
    }


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if len(argv) != 2:
        raise SystemExit("expected -- <integrity_out.json> <furniture_out.json>")
    integrity_out = Path(argv[0])
    furniture_out = Path(argv[1])
    source = Path(bpy.data.filepath)
    pre_file_sha = sha256(source)
    pre_file_bytes = source.stat().st_size
    pre = snapshot("PRE_REFRESH_SAVE")
    bpy.ops.wm.save_as_mainfile(filepath=str(source), check_existing=False)
    saved_sha = sha256(source)
    saved_bytes = source.stat().st_size
    bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False)
    reopened_sha = sha256(source)
    post = snapshot("POST_REFRESH_REOPEN")
    checks = {
        "saved_reopened_sha_stable": saved_sha == reopened_sha,
        "scene_fingerprint_stable": pre["scene_fingerprint_sha256"] == post["scene_fingerprint_sha256"],
        "object_count_stable": pre["active_object_count"] == post["active_object_count"],
        "chairs_stable": pre["chairs"] == post["chairs"],
        "edit008_stable": pre["edit008_candidates"] == post["edit008_candidates"],
        "material_users_stable": pre["material_users"] == post["material_users"],
    }
    integrity = {
        "schema": "OLEANDER_FALLINGWATER_NATIVE_SAVE_REOPEN_INTEGRITY_v2",
        "status": "PASS" if all(checks.values()) else "HOLD",
        "source_path": str(source),
        "pre_refresh_sha256": pre_file_sha,
        "pre_refresh_bytes": pre_file_bytes,
        "final_saved_reopened_sha256": reopened_sha,
        "final_bytes": saved_bytes,
        "pre": pre,
        "post": post,
        "checks": checks,
        "does_not_prove": ["historic exactness beyond stated authority", "engineering capacity", "manufacturing readiness", "field verification", "Design KEEP"],
    }
    furniture = furniture_audit(source)
    integrity_out.write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    furniture_out.write_text(json.dumps(furniture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"integrity": integrity, "furniture_status": furniture["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
