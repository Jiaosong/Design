VALID_STATES = ("OPEN", "PASS", "HOLD", "FAIL", "NA")


def _map_field(value):
    return {"VERIFIED": "PASS", "OPEN": "OPEN", "NOT_APPLICABLE": "NA"}.get(value, "OPEN")


def _map_engineering(value):
    return {"APPROVED": "PASS", "OPEN": "OPEN", "NOT_APPLICABLE": "NA"}.get(value, "OPEN")


def _map_manufacturing(value):
    return {"RELEASED": "PASS", "OPEN": "OPEN", "NOT_APPLICABLE": "NA"}.get(value, "OPEN")


def summarize_object_state(obj):
    meta = getattr(obj, "oleander", None)
    if not meta:
        return {
            "geometry": "OPEN",
            "field": "OPEN",
            "engineering": "OPEN",
            "manufacturing": "OPEN",
            "design": "OPEN",
            "stale": False,
            "overall": "OPEN",
        }

    geometry = obj.get("oleander_geometry_audit_state", "OPEN")
    field = _map_field(getattr(meta, "field_state", "OPEN"))
    engineering = _map_engineering(getattr(meta, "engineering_state", "OPEN"))
    manufacturing = _map_manufacturing(getattr(meta, "manufacturing_state", "OPEN"))
    design = getattr(meta, "design_review_state", "OPEN") or "OPEN"
    stale = bool(getattr(meta, "stale", False))

    states = [geometry, field, engineering, manufacturing, design]
    if "FAIL" in states:
        overall = "FAIL"
    elif "HOLD" in states or stale:
        overall = "HOLD"
    elif all(state in {"PASS", "NA"} for state in states):
        overall = "PASS"
    else:
        overall = "OPEN"

    return {
        "geometry": geometry,
        "field": field,
        "engineering": engineering,
        "manufacturing": manufacturing,
        "design": design,
        "stale": stale,
        "overall": overall,
    }
