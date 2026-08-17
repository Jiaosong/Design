#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageFilter

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def load_rgb(path: Path) -> Image.Image:
    image = Image.open(path)
    if image.mode in {"RGBA", "LA"}:
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))
        image = Image.alpha_composite(background, image.convert("RGBA"))
    return image.convert("RGB")


def edge_mask(image: Image.Image, threshold: int = 24) -> np.ndarray:
    return np.asarray(image.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.uint8) > threshold


def dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask
    image = Image.fromarray((mask.astype(np.uint8) * 255), mode="L")
    return np.asarray(image.filter(ImageFilter.MaxFilter(radius * 2 + 1)), dtype=np.uint8) > 0


def metrics(
    reference: Image.Image,
    candidate: Image.Image,
    tolerance: int,
    rois: list[dict[str, Any]],
    *,
    full: bool = False,
) -> dict[str, Any]:
    if reference.size != candidate.size:
        return {"loss": 1e9, "same_canvas": False}

    ref = np.asarray(reference, dtype=np.uint8)
    cand = np.asarray(candidate, dtype=np.uint8)
    delta = np.abs(ref.astype(np.int16) - cand.astype(np.int16))
    changed = delta.max(axis=2) > tolerance
    mae_norm = float(delta.mean()) / 255.0
    changed_ratio = float(changed.mean())

    edge_mismatch = 0.0
    if full:
        ref_edge = edge_mask(reference)
        cand_edge = edge_mask(candidate)
        cand_edge_r1 = dilate(cand_edge, 1)
        ref_edge_r1 = dilate(ref_edge, 1)
        edge_mismatch = (
            float(np.logical_and(ref_edge, ~cand_edge_r1).sum() / max(1, ref_edge.sum()))
            + float(np.logical_and(cand_edge, ~ref_edge_r1).sum() / max(1, cand_edge.sum()))
        ) / 2.0

    roi_results: list[dict[str, Any]] = []
    roi_loss = 0.0
    weight_sum = 0.0
    for roi in rois:
        x, y, width, height = [int(roi[key]) for key in ("x", "y", "w", "h")]
        weight = float(roi.get("weight", 1.0))
        roi_delta = delta[y : y + height, x : x + width]
        roi_changed = roi_delta.max(axis=2) > tolerance
        changed_value = float(roi_changed.mean())
        mae_value = float(roi_delta.mean()) / 255.0
        roi_results.append(
            {
                "id": roi["id"],
                "changed_ratio": changed_value,
                "mae_norm": mae_value,
                "weight": weight,
            }
        )
        roi_loss += weight * (changed_value + 0.25 * mae_value)
        weight_sum += weight

    roi_loss = roi_loss / max(weight_sum, 1.0)
    if full:
        loss = 0.58 * roi_loss + 0.22 * edge_mismatch + 0.16 * changed_ratio + 0.04 * mae_norm
    else:
        # Search path intentionally avoids expensive edge filtering. Full edge readback is run once at the end.
        loss = 0.72 * roi_loss + 0.22 * changed_ratio + 0.06 * mae_norm

    return {
        "loss": loss,
        "same_canvas": True,
        "changed_ratio": changed_ratio,
        "mae_norm": mae_norm,
        "edge_mismatch_r1": edge_mismatch,
        "rois": roi_results,
    }


def render_svg(
    svg_path: Path,
    png_path: Path,
    width: int | None,
    height: int | None,
    renderer: str = "auto",
) -> str:
    if renderer in {"inkscape", "auto"} and shutil.which("inkscape"):
        command = ["inkscape", str(svg_path), "--export-filename", str(png_path)]
        if width:
            command.append(f"--export-width={width}")
        if height:
            command.append(f"--export-height={height}")
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "inkscape"
        except Exception:
            if renderer == "inkscape":
                raise

    if renderer in {"cairosvg", "auto"}:
        try:
            import cairosvg

            kwargs: dict[str, Any] = {}
            if width:
                kwargs["output_width"] = width
            if height:
                kwargs["output_height"] = height
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), **kwargs)
            return "cairosvg"
        except Exception:
            if renderer == "cairosvg":
                raise

    raise RuntimeError("Requested SVG renderer is unavailable")


def find_target(root: ET.Element, spec: dict[str, Any]) -> ET.Element:
    element_id = spec["id"]
    parent = None
    for element in root.iter():
        if element.get("id") == element_id:
            parent = element
            break
    if parent is None:
        raise KeyError(f"id {element_id} not found")

    tag = spec.get("tag")
    if not tag:
        return parent

    qualified = f"{{{SVG_NS}}}{tag}"
    matches = [element for element in parent.iter(qualified)]
    index = int(spec.get("index", 0))
    if index >= len(matches):
        raise IndexError(f"{element_id} {tag}[{index}] not found")
    return matches[index]


def parse_translate(value: str | None) -> tuple[float, float]:
    if not value:
        return (0.0, 0.0)
    match = re.search(r"translate\(\s*([-+0-9.eE]+)(?:[ ,]+([-+0-9.eE]+))?\s*\)", value)
    if not match:
        return (0.0, 0.0)
    return float(match.group(1)), float(match.group(2) or 0)


def set_param(tree: ET.ElementTree, parameter: dict[str, Any], value: float) -> None:
    element = find_target(tree.getroot(), parameter["target"])
    kind = parameter.get("kind", "attribute")

    if kind == "attribute":
        element.set(parameter["attribute"], f"{value:.6g}")
        return

    if kind in {"translate_x", "translate_y"}:
        x, y = parse_translate(element.get("transform"))
        if kind == "translate_x":
            x = value
        else:
            y = value
        element.set("transform", f"translate({x:.6g} {y:.6g})")
        return

    raise ValueError(f"Unsupported parameter kind: {kind}")


def read_param(tree: ET.ElementTree, parameter: dict[str, Any]) -> float:
    element = find_target(tree.getroot(), parameter["target"])
    kind = parameter.get("kind", "attribute")

    if kind == "attribute":
        return float(element.get(parameter["attribute"]))

    x, y = parse_translate(element.get("transform"))
    return x if kind == "translate_x" else y


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Coupled coordinate-descent solver for editable SVG reconstruction parameters. "
            "It never moves or warps the reference and cannot grant Design/technical/field approval."
        )
    )
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--candidate-svg", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--tolerance", type=int, default=0)
    parser.add_argument("--renderer", choices=["auto", "inkscape", "cairosvg"], default="auto")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    rois = spec.get("rois", [])
    parameters = spec["parameters"]
    stages = spec.get("stages", [])
    if not stages:
        stages = sorted({parameter.get("stage", "E2") for parameter in parameters})

    reference = load_rgb(args.reference)
    width, height = reference.size
    args.out_dir.mkdir(parents=True, exist_ok=True)

    tree = ET.parse(args.candidate_svg)
    trace: list[dict[str, Any]] = []
    render_count = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        def evaluate(tag: str) -> tuple[dict[str, Any], str]:
            nonlocal render_count
            svg_path = temp_path / f"{tag}.svg"
            png_path = temp_path / f"{tag}.png"
            tree.write(svg_path, encoding="utf-8", xml_declaration=True)
            renderer_used = render_svg(svg_path, png_path, width, height, args.renderer)
            render_count += 1
            return metrics(reference, load_rgb(png_path), args.tolerance, rois), renderer_used

        current, renderer_used = evaluate("initial")
        trace.append({"event": "initial", "metrics": current})

        max_cycles = int(spec.get("max_cycles", 3))
        epsilon = float(spec.get("epsilon", 1e-10))

        for cycle in range(max_cycles):
            cycle_start = current["loss"]
            cycle_changed = False

            for stage in stages:
                stage_parameters = [p for p in parameters if p.get("stage", "E2") == stage]
                for parameter in stage_parameters:
                    schedule = parameter.get("steps", [parameter.get("step", 1.0)])
                    for step in schedule:
                        improved = True
                        while improved:
                            improved = False
                            base_value = read_param(tree, parameter)
                            best = (current["loss"], base_value, current)

                            for candidate_value in [base_value - step, base_value + step]:
                                if "min" in parameter and candidate_value < parameter["min"]:
                                    continue
                                if "max" in parameter and candidate_value > parameter["max"]:
                                    continue

                                set_param(tree, parameter, candidate_value)
                                candidate_metrics, _ = evaluate(
                                    f"c{cycle}_{parameter['name']}_{candidate_value:.5g}"
                                )
                                if candidate_metrics["loss"] + epsilon < best[0]:
                                    best = (candidate_metrics["loss"], candidate_value, candidate_metrics)

                            set_param(tree, parameter, best[1])
                            current = best[2]
                            if best[1] != base_value:
                                improved = True
                                cycle_changed = True
                                trace.append(
                                    {
                                        "event": "accept",
                                        "cycle": cycle,
                                        "stage": stage,
                                        "parameter": parameter["name"],
                                        "value": best[1],
                                        "step": step,
                                        "loss": current["loss"],
                                    }
                                )
                            else:
                                set_param(tree, parameter, base_value)

            trace.append(
                {
                    "event": "cycle_end",
                    "cycle": cycle,
                    "loss": current["loss"],
                    "improvement": cycle_start - current["loss"],
                }
            )
            if not cycle_changed or cycle_start - current["loss"] <= epsilon:
                break

        final_svg = args.out_dir / "SOLVED.svg"
        tree.write(final_svg, encoding="utf-8", xml_declaration=True)
        final_png = args.out_dir / "SOLVED.png"
        renderer_used = render_svg(final_svg, final_png, width, height, args.renderer)
        final_metrics = metrics(reference, load_rgb(final_png), args.tolerance, rois, full=True)

    values = {parameter["name"]: read_param(tree, parameter) for parameter in parameters}
    result = {
        "tool": "oleander-technical-drawing/svg_parameter_solver.py",
        "renderer": renderer_used,
        "render_count": render_count + 1,
        "initial": trace[0]["metrics"],
        "final": final_metrics,
        "values": values,
        "trace": trace,
        "does_not_prove": [
            "technical correctness",
            "design KEEP",
            "engineering adequacy",
            "field truth",
            "fabrication/construction permission",
        ],
    }
    (args.out_dir / "SOLVER_RESULT.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
