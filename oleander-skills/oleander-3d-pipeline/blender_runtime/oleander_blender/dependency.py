import bpy
from collections import defaultdict, deque


def _meta(obj):
    return getattr(obj, "oleander", None)


def object_id(obj):
    meta = _meta(obj)
    return (getattr(meta, "ole_id", "") or obj.name).strip()


def dependency_ids(obj):
    meta = _meta(obj)
    raw = getattr(meta, "dependencies", "") if meta else ""
    if not raw:
        raw = obj.get("oleander_dependencies", "")
    if isinstance(raw, str):
        return [item.strip() for item in raw.split(",") if item.strip()]
    return []


def build_dependency_graph(scene=None):
    scene = scene or bpy.context.scene
    objects = list(scene.objects)
    id_to_obj = {object_id(obj): obj for obj in objects}
    forward = defaultdict(set)
    reverse = defaultdict(set)
    missing = defaultdict(list)

    for obj in objects:
        oid = object_id(obj)
        for dep_id in dependency_ids(obj):
            forward[oid].add(dep_id)
            reverse[dep_id].add(oid)
            if dep_id not in id_to_obj:
                missing[oid].append(dep_id)

    return {
        "id_to_obj": id_to_obj,
        "forward": forward,
        "reverse": reverse,
        "missing": missing,
    }


def detect_cycles(graph):
    forward = graph["forward"]
    visiting = set()
    visited = set()
    cycles = []

    def walk(node, path):
        if node in visiting:
            try:
                idx = path.index(node)
            except ValueError:
                idx = 0
            cycles.append(path[idx:] + [node])
            return
        if node in visited:
            return
        visiting.add(node)
        path.append(node)
        for dep in forward.get(node, ()):
            walk(dep, path)
        path.pop()
        visiting.remove(node)
        visited.add(node)

    for node in set(forward):
        walk(node, [])
    return cycles


def mark_downstream_stale(source_ids, reason="UPSTREAM_CHANGED", scene=None):
    graph = build_dependency_graph(scene)
    reverse = graph["reverse"]
    id_to_obj = graph["id_to_obj"]
    queue = deque(source_ids)
    seen = set(source_ids)
    changed = []

    while queue:
        current = queue.popleft()
        for downstream in reverse.get(current, ()):
            if downstream in seen:
                continue
            seen.add(downstream)
            queue.append(downstream)
            obj = id_to_obj.get(downstream)
            if not obj:
                continue
            meta = _meta(obj)
            if meta and hasattr(meta, "stale"):
                meta.stale = True
            obj["oleander_stale_reason"] = reason
            changed.append(downstream)

    return changed


def clear_stale(obj):
    meta = _meta(obj)
    if meta and hasattr(meta, "stale"):
        meta.stale = False
    if "oleander_stale_reason" in obj:
        del obj["oleander_stale_reason"]
