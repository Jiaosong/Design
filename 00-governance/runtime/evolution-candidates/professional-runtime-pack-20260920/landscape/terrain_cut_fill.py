#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    existing_m: float
    proposed_m: float
    area_m2: float


def cut_fill(cells: list[Cell]) -> dict[str, float]:
    cut = 0.0
    fill = 0.0
    for cell in cells:
        delta = cell.proposed_m - cell.existing_m
        volume = delta * cell.area_m2
        if volume >= 0:
            fill += volume
        else:
            cut += -volume
    return {
        "cut_m3": cut,
        "fill_m3": fill,
        "net_fill_minus_cut_m3": fill - cut,
    }


if __name__ == "__main__":
    cells = [
        Cell(100.0, 99.5, 10.0),
        Cell(100.0, 100.2, 10.0),
        Cell(100.0, 100.3, 10.0),
        Cell(100.0, 99.9, 10.0),
    ]
    result = cut_fill(cells)
    expected = {"cut_m3": 6.0, "fill_m3": 5.0, "net_fill_minus_cut_m3": -1.0}
    for key, value in expected.items():
        if not math.isclose(result[key], value, abs_tol=1e-9):
            raise SystemExit(f"{key}: {result[key]} != {value}")
    print(json.dumps({
        "runtime": "Python stdlib",
        "method": "per-cell elevation delta × authoritative cell area",
        "cell_count": len(cells),
        **result,
        "result": "PASS_RUNTIME_SMOKE",
        "does_not_prove": [
            "survey authority",
            "civil grading design",
            "drainage performance",
            "field quantity",
            "Landscape professional PASS"
        ]
    }, indent=2))
