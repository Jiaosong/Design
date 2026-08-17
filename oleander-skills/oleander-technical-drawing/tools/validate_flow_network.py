#!/usr/bin/env python3
import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "{http://www.w3.org/2000/svg}"
NON_PROMOTED = {"CANDIDATE_NOT_PROMOTED", "REVIEW_PENDING", "REVISE"}
EDGE_TAGS = {"path", "polyline", "line"}


def fail(message: str):
    raise AssertionError(message)


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def angle_delta(a: float, b: float) -> float:
    d = (a - b + 180.0) % 360.0 - 180.0
    return abs(d)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--svg", required=True)
    parser.add_argument("--register", required=True)
    args = parser.parse_args()

    try:
        register = json.loads(Path(args.register).read_text(encoding="utf-8"))
        root = ET.fromstring(Path(args.svg).read_text(encoding="utf-8"))
        if root.tag != SVG_NS + "svg":
            fail("root is not svg")

        nodes_by_svg_id = {}
        for node in root.iter():
            node_id = node.attrib.get("id")
            if node_id:
                if node_id in nodes_by_svg_id:
                    fail(f"duplicate svg id: {node_id}")
                nodes_by_svg_id[node_id] = node

        if register.get("status") not in NON_PROMOTED:
            fail("flow register must remain non-promoted")
        if register.get("network_editability_target") != "SEMANTIC_FLOW_GRAPH":
            fail("network_editability_target must be SEMANTIC_FLOW_GRAPH")

        base_id = register.get("base_geometry_id")
        if not base_id or base_id not in nodes_by_svg_id:
            fail("missing registered base geometry")

        route_classes = register.get("route_classes") or {}
        required_classes = set(register.get("required_route_classes") or [])
        if not required_classes:
            fail("required_route_classes must be declared")
        missing_classes = required_classes - set(route_classes)
        if missing_classes:
            fail(f"missing route classes: {sorted(missing_classes)}")
        if len(required_classes) < 2:
            fail("flow regression must preserve at least two route classes")

        graph_nodes = register.get("nodes") or []
        node_by_id = {n["id"]: n for n in graph_nodes}
        if len(node_by_id) != len(graph_nodes):
            fail("duplicate flow node ids")
        for node_id, node_spec in node_by_id.items():
            svg_id = node_spec.get("svg_id")
            if not svg_id or svg_id not in nodes_by_svg_id:
                fail(f"node {node_id} missing svg object")

        edges = register.get("edges") or []
        edge_by_id = {e["id"]: e for e in edges}
        if len(edge_by_id) != len(edges):
            fail("duplicate flow edge ids")
        if len(edges) < 3:
            fail("flow regression requires >= 3 route edges")

        class_counts = {name: 0 for name in route_classes}
        for edge_id, edge in edge_by_id.items():
            start = edge.get("start_node")
            end = edge.get("end_node")
            if start not in node_by_id or end not in node_by_id:
                fail(f"edge {edge_id} references unknown start/end node")
            route_class = edge.get("route_class")
            if route_class not in route_classes:
                fail(f"edge {edge_id} uses unknown route class {route_class}")
            class_counts[route_class] = class_counts.get(route_class, 0) + 1
            svg_id = edge.get("svg_id")
            if not svg_id or svg_id not in nodes_by_svg_id:
                fail(f"edge {edge_id} missing svg carrier")
            if local_name(nodes_by_svg_id[svg_id].tag) not in EDGE_TAGS:
                fail(f"edge {edge_id} svg carrier must be line/path/polyline")
            svg_edge = nodes_by_svg_id[svg_id]
            if svg_edge.attrib.get("data-route-class") != route_class:
                fail(f"edge {edge_id} svg route class metadata mismatch")
            if svg_edge.attrib.get("data-start-node") != start or svg_edge.attrib.get("data-end-node") != end:
                fail(f"edge {edge_id} svg node metadata mismatch")
            base_binding = edge.get("base_binding")
            if base_binding not in {"CENTERLINE-BOUND", "EDGE-BOUND", "CORRIDOR-BOUND", "FREE ANALYTICAL VECTOR", "UNKNOWN / UNRECOVERABLE"}:
                fail(f"edge {edge_id} invalid base binding")

        for route_class in required_classes:
            if class_counts.get(route_class, 0) == 0:
                fail(f"required route class {route_class} has no edge")

        for node_id, node_spec in node_by_id.items():
            declared = set(node_spec.get("connected_edges") or [])
            actual = {e["id"] for e in edges if e.get("start_node") == node_id or e.get("end_node") == node_id}
            if declared != actual:
                fail(f"node {node_id} connected_edges mismatch declared={sorted(declared)} actual={sorted(actual)}")
            degree = int(node_spec.get("degree", -1))
            if degree != len(actual):
                fail(f"node {node_id} degree mismatch {degree} != {len(actual)}")

        markers = register.get("direction_markers") or []
        marker_ids = set()
        max_tangent_error = float(register.get("max_marker_tangent_error_deg", 2.0))
        for marker in markers:
            marker_id = marker["id"]
            if marker_id in marker_ids:
                fail(f"duplicate marker id {marker_id}")
            marker_ids.add(marker_id)
            edge_id = marker.get("route_edge")
            if edge_id not in edge_by_id:
                fail(f"marker {marker_id} references unknown edge")
            svg_id = marker.get("svg_id")
            if not svg_id or svg_id not in nodes_by_svg_id:
                fail(f"marker {marker_id} missing svg object")
            svg_marker = nodes_by_svg_id[svg_id]
            if svg_marker.attrib.get("data-route-edge") != edge_id:
                fail(f"marker {marker_id} svg owner edge mismatch")
            position = marker.get("position")
            if position not in {"start", "interior", "end", "continuation"}:
                fail(f"marker {marker_id} invalid position")
            marker_angle = float(marker["marker_angle_deg"])
            tangent_angle = float(marker["local_tangent_deg"])
            if angle_delta(marker_angle, tangent_angle) > max_tangent_error:
                fail(f"marker {marker_id} not tangent to route: {marker_angle} vs {tangent_angle}")
            ratio = float(marker.get("marker_to_stroke_ratio", 0))
            min_ratio, max_ratio = register.get("marker_to_stroke_ratio_range", [0.5, 5.0])
            if not (float(min_ratio) <= ratio <= float(max_ratio)):
                fail(f"marker {marker_id} marker/stroke ratio out of contract")

        directed_edges = [e for e in edges if e.get("directed") is True and e.get("requires_direction_marker", True)]
        for edge in directed_edges:
            owned = [m for m in markers if m.get("route_edge") == edge["id"]]
            if not owned:
                fail(f"directed edge {edge['id']} has no direction marker")

        labels = register.get("route_labels") or []
        for label in labels:
            label_id = label["id"]
            svg_id = label.get("svg_id")
            edge_id = label.get("route_edge")
            if edge_id not in edge_by_id:
                fail(f"label {label_id} references unknown edge")
            if not svg_id or svg_id not in nodes_by_svg_id or local_name(nodes_by_svg_id[svg_id].tag) != "text":
                fail(f"label {label_id} missing editable text object")
            if nodes_by_svg_id[svg_id].attrib.get("data-route-edge") != edge_id:
                fail(f"label {label_id} svg route binding mismatch")

        mode_symbols = register.get("mode_symbols") or []
        for symbol in mode_symbols:
            symbol_id = symbol["id"]
            svg_id = symbol.get("svg_id")
            if not svg_id or svg_id not in nodes_by_svg_id:
                fail(f"mode symbol {symbol_id} missing svg object")
            owner_node = symbol.get("node_id")
            owner_edge = symbol.get("edge_id")
            if bool(owner_node) == bool(owner_edge):
                fail(f"mode symbol {symbol_id} must bind to exactly one node or edge")
            if owner_node and owner_node not in node_by_id:
                fail(f"mode symbol {symbol_id} references unknown node")
            if owner_edge and owner_edge not in edge_by_id:
                fail(f"mode symbol {symbol_id} references unknown edge")

        external = register.get("external_continuations") or []
        for continuation in external:
            edge_id = continuation.get("edge_id")
            if edge_id not in edge_by_id:
                fail("external continuation references unknown edge")
            if edge_by_id[edge_id].get("route_class") not in {"external", "continuation"}:
                fail(f"external continuation edge {edge_id} must use external/continuation class")

    except (AssertionError, OSError, json.JSONDecodeError, ET.ParseError, KeyError, TypeError, ValueError) as exc:
        print(f"OLEANDER FLOW NETWORK: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("OLEANDER FLOW NETWORK: STRUCTURE PASS")
    print(f"nodes={len(graph_nodes)} edges={len(edges)} markers={len(markers)} labels={len(labels)} mode_symbols={len(mode_symbols)}")
    print("NOTE: flow-graph structure PASS does not equal visual fidelity, pixel fidelity, route truth, or Design KEEP.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
