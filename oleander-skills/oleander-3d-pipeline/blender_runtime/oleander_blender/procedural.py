import bpy


PROCEDURAL_SCHEMA = "OLEANDER_GEOMETRY_NODES_BINDING_v0.1"


def mesh_evaluated_counts(obj, depsgraph=None):
    depsgraph = depsgraph or bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        return {
            "vertices": len(mesh.vertices),
            "edges": len(mesh.edges),
            "polygons": len(mesh.polygons),
        }
    finally:
        evaluated.to_mesh_clear()


def create_passthrough_geometry_nodes(obj, group_name="OLEANDER_GN_PASSTHROUGH"):
    """Bind a governed no-op Geometry Nodes group to an object.

    This proves Blender Geometry Nodes runtime availability and establishes a
    traceable procedural binding. It does not claim Houdini-equivalent SOP
    capability, CAD authority, dimensional truth, or engineering correctness.

    Blender 5.2 no longer accepts arbitrary ID properties on NodesModifier.
    Governed provenance therefore lives on the GeometryNodeTree data-block,
    which is an ID data-block and persists through save/reopen. The modifier
    remains only the native binding between the object and that governed tree.
    """
    if obj is None:
        raise ValueError("object is required")
    if obj.type not in {"MESH", "CURVE", "FONT", "VOLUME", "POINTCLOUD"}:
        raise TypeError(f"unsupported Geometry Nodes object type: {obj.type}")

    node_group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    node_group.is_modifier = True
    node_group["oleander_schema"] = PROCEDURAL_SCHEMA
    node_group["oleander_procedural_role"] = "PASSTHROUGH_RUNTIME_PROBE"
    node_group["oleander_geometry_authority"] = "BLENDER_PROCEDURAL_DERIVATIVE"
    node_group["oleander_solver_claim"] = False
    source_id = getattr(getattr(obj, "oleander", None), "ole_id", "")
    node_group["oleander_source_ole_id"] = source_id

    node_group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    node_group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    input_node = node_group.nodes.new("NodeGroupInput")
    input_node.name = "OLEANDER_INPUT"
    output_node = node_group.nodes.new("NodeGroupOutput")
    output_node.name = "OLEANDER_OUTPUT"
    input_node.location = (-160.0, 0.0)
    output_node.location = (160.0, 0.0)
    node_group.links.new(input_node.outputs["Geometry"], output_node.inputs["Geometry"])

    modifier = obj.modifiers.new(name="OLEANDER Geometry Nodes", type="NODES")
    modifier.node_group = node_group
    return modifier, node_group


def describe_geometry_nodes_binding(obj):
    bindings = []
    for modifier in obj.modifiers:
        if modifier.type != "NODES" or modifier.node_group is None:
            continue
        group = modifier.node_group
        bindings.append(
            {
                "modifier": modifier.name,
                "node_group": group.name,
                "tree_type": group.bl_idname,
                "schema": group.get("oleander_schema", ""),
                "role": group.get("oleander_procedural_role", ""),
                "source_ole_id": group.get("oleander_source_ole_id", ""),
                "solver_claim": bool(group.get("oleander_solver_claim", False)),
                "node_count": len(group.nodes),
                "link_count": len(group.links),
            }
        )
    return bindings
