"""Runtime relation graph operations v0.3."""


def add_edge(graph: dict, source: str, target: str, relation: str, reason: str):
    graph.setdefault("edges", []).append({
        "from": source,
        "to": target,
        "relation": relation,
        "reason": reason,
    })
    return graph


def neighbors(graph: dict, node_id: str):
    return [e for e in graph.get("edges", []) if e["from"] == node_id or e["to"] == node_id]


__all__ = ["add_edge", "neighbors"]
