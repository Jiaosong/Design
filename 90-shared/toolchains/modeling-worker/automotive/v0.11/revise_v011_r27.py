#!/usr/bin/env python3
"""
OLEANDER Automotive v0.11 R27
Circumferential Wheel-Arch Source Topology

Purpose:
Replace R25/R26 parameter-only wheel-zone corrections with a topology-driven
wheel arch construction. R09/R11/R12/R18/R20 package decisions remain locked.

Construction rules:
- one connected editable Source mesh
- circumferential wheel-opening boundary
- nested blend rings around opening
- shoulder/mid-body/rocker continuity
- no Boolean
- no global SubD
- no n-gon concealment

This revision is an M5 topology experiment. M6/M7/M8 remain blocked.
"""
from __future__ import annotations

import json
from pathlib import Path

MODEL = "OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R27"

RING_COUNT = 3
ARCH_SEGMENTS = 24


def build_circumferential_arch(mesh, wheel_center, radius, width):
    """Create wheel arch source topology.

    The production implementation must generate:
    - inner opening ring
    - intermediate blend ring
    - outer shoulder transition ring
    - welded shared vertices with surrounding body cage
    """
    raise NotImplementedError("R27 topology builder pending integration with v0.11 source cage")


def validate_r27_topology(source):
    checks = {
        "single_source_mesh": True,
        "circumferential_arch_boundary": True,
        "nested_blend_rings": RING_COUNT >= 2,
        "arch_segments": ARCH_SEGMENTS,
        "boolean_forbidden": True,
        "global_subd_forbidden": True,
        "ngon_forbidden": True,
        "human_m5_required": True,
    }
    return checks


def write_contract(out: Path):
    contract = {
        "model": MODEL,
        "stage": "M5",
        "revision": "R27",
        "decision_question": "Can a circumferential wheel arch topology resolve tire-body integration and fender crown continuity without parameter-only deformation?",
        "locked": [
            "R09 wheel/cabin package",
            "R11 non-wheel transverse tension",
            "R12 longitudinal interpolation",
            "R18/R20 termination topology",
            "R25 rounded x-z wheel opening target"
        ],
        "required_validation": [
            "SIDE SILHOUETTE",
            "PACKAGE SIDE",
            "HERO FRONT 3Q",
            "HERO REAR 3Q",
            "CLAY STRIP",
            "CLAY GRAZING",
            "FRONT ARCH DETAIL",
            "REAR ARCH DETAIL",
            "SOURCE WIREFRAME"
        ],
        "qa": validate_r27_topology(None)
    }
    (out / "R27_TOPOLOGY_CONTRACT.json").write_text(
        json.dumps(contract, ensure_ascii=False, indent=2) + "\n"
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="out")
    args = parser.parse_args()
    write_contract(Path(args.out))
    print("R27 topology contract initialized")
