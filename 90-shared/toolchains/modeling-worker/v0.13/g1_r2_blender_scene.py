from __future__ import annotations

import bpy

import g1_geometry_core as base
import g1_r2_core as r2

SRC = "OLEANDER_SOURCE_AUTHORITY"
DER = "OLEANDER_DERIVED_EXECUTION"
QA = "OLEANDER_QA_RIG"


def clean() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    root = bpy.context.scene.collection
    default = bpy.data.collections.get("Collection")
    if default and default.name in root.children:
        root.children.unlink(default)
        bpy.data.collections.remove(default)


def col(name: str):
    collection = bpy.data.collections.get(name)
    if not collection:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def nurbs(name, pts, collection, role):
    data = bpy.data.curves.new(name + "_DATA", "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 24
    spline = data.splines.new("NURBS")
    spline.points.add(len(pts) - 1)
    for point, co in zip(spline.points, pts):
        point.co = (*co, 1.0)
        point.weight = 1.0
    spline.order_u = min(6, len(pts))
    spline.use_endpoint_u = True
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    obj.hide_render = True
    obj.display_type = "WIRE"
    obj["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    obj["OLEANDER_ROLE"] = role
    obj["OLEANDER_EDITABLE"] = True
    return obj


def profile(name, values, collection, role, axis):
    pts = []
    for i, value in enumerate(values):
        x = 0.190 * i / (len(values) - 1)
        if axis == "Y+":
            pts.append((x, float(value), 0))
        elif axis == "Y-":
            pts.append((x, -float(value), 0))
        elif axis == "Z-":
            pts.append((x, 0, -float(value)))
        else:
            pts.append((x, 0, float(value)))
    obj = nurbs(name, pts, collection, role)
    obj["OLEANDER_PROFILE_AXIS"] = axis
    obj["OLEANDER_CONTROL_VALUES"] = [float(value) for value in values]
    return obj


def theta_center_rad(data):
    if "theta_center_rad" in data:
        return float(data["theta_center_rad"])
    if data.get("theta_center") == "TOP_MERIDIAN":
        return 0.0
    raise ValueError("INTERFACE_DECK_BOUNDARY requires theta_center_rad or theta_center=TOP_MERIDIAN")


def sources(source, collection):
    own = base.own
    out = [
        nurbs(
            "OL_SRC_GRIP_AXIS",
            [tuple(map(float, point)) for point in own(source, "GRIP_AXIS")["control_points"]],
            collection,
            own(source, "GRIP_AXIS")["role"],
        )
    ]
    out += [
        profile(
            "OL_SRC_PALM_PROFILE",
            own(source, "PALM_PROFILE")["control_values"],
            collection,
            own(source, "PALM_PROFILE")["role"],
            "Z+",
        ),
        profile(
            "OL_SRC_THUMB_SIDE_PLAN",
            own(source, "THUMB_SIDE_PLAN")["control_values"],
            collection,
            own(source, "THUMB_SIDE_PLAN")["role"],
            "Y+",
        ),
        profile(
            "OL_SRC_OPPOSITE_SIDE_PLAN",
            own(source, "OPPOSITE_SIDE_PLAN")["control_values"],
            collection,
            own(source, "OPPOSITE_SIDE_PLAN")["role"],
            "Y-",
        ),
        profile(
            "OL_SRC_LOWER_RETURN_PROFILE",
            own(source, "LOWER_RETURN_PROFILE")["control_values"],
            collection,
            own(source, "LOWER_RETURN_PROFILE")["role"],
            "Z-",
        ),
    ]
    deck_data = own(source, "INTERFACE_DECK_BOUNDARY")
    deck = bpy.data.objects.new("OL_SRC_INTERFACE_DECK_BOUNDARY", None)
    collection.objects.link(deck)
    deck.empty_display_type = "CIRCLE"
    deck.empty_display_size = 0.012
    deck["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    deck["OLEANDER_ROLE"] = deck_data["role"]
    deck["OLEANDER_EDITABLE"] = True
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "depth_m", "core_fraction"):
        if key in deck_data:
            deck[key] = float(deck_data[key])
    deck["theta_center_rad"] = theta_center_rad(deck_data)
    deck["theta_center_semantics"] = str(deck_data.get("theta_center", "RADIAN"))
    deck["blend"] = str(deck_data.get("blend", "QUINTIC_SMOOTHERSTEP"))
    deck.location = r2.point(
        source,
        float(deck_data["u_center"]),
        theta_center_rad(deck_data),
        False,
        False,
    )
    out.append(deck)
    return out


def mesh_obj(name, verts, faces, collection, role):
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_NOT_AUTHORITY"
    obj["OLEANDER_ROLE"] = role
    obj["OLEANDER_EDITABLE"] = False
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    return obj
