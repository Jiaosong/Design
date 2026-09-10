"""OLEANDER Surface Decision Layer v0.5.

Separates measurement, analysis and promotion decision.
"""

def make_surface_decision(target, machine_result, visual_result, note=""):
    if machine_result == "PASS" and visual_result == "PASS":
        decision = "PROMOTE"
    elif machine_result == "PASS":
        decision = "REVISE"
    else:
        decision = "BLOCK"

    return {
        "target": target,
        "measurement": machine_result,
        "analysis": visual_result,
        "decision": decision,
        "note": note,
        "authority": "DERIVED"
    }

__all__ = ["make_surface_decision"]
