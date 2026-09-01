VALID_STATES = ("OPEN", "PASS", "HOLD", "FAIL", "NA")


def summarize_object_state(obj):
    meta = getattr(obj, "oleander_meta", None)
    if not meta:
        return {
            "geometry": "OPEN",
            "field": "OPEN",
            "engineering": "OPEN",
            "manufacturing": "OPEN",
            "design": "OPEN",
            "overall": "OPEN",
        }

    geometry = obj.get("oleander_geometry_audit_state", "OPEN")
    field = getattr(meta, "field_status", "OPEN") or "OPEN"
    engineering = getattr(meta, "engineering_status", "OPEN") or "OPEN"
    manufacturing = getattr(meta, "manufacturing_status", "OPEN") or "OPEN"
    design = obj.get("oleander_design_review_state", "OPEN")

    states = [geometry, field, engineering, manufacturing, design]
    if "FAIL" in states:
        overall = "FAIL"
    elif "HOLD" in states:
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
        "overall": overall,
    }
