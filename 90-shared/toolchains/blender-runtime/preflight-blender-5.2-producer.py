#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path


class PreflightError(ValueError):
    pass


def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def assignment_targets(tree: ast.AST) -> list[tuple[str, ast.AST | None]]:
    found: list[tuple[str, ast.AST | None]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                found.append((dotted_name(target), node.value))
        elif isinstance(node, ast.AnnAssign):
            found.append((dotted_name(node.target), node.value))
    return found


def parse_path(path: Path) -> ast.AST:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PreflightError(f"cannot read {path}: {exc}") from exc
    try:
        return ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise PreflightError(f"syntax failure in {path}: {exc}") from exc


def inspect_producer(path: Path) -> list[str]:
    tree = parse_path(path)
    targets = assignment_targets(tree)

    render_engine_written = any(name.endswith(".render.engine") for name, _ in targets)
    stale_eevee_constant = any(
        isinstance(node, ast.Constant) and node.value == "BLENDER_EEVEE_NEXT"
        for node in ast.walk(tree)
    )

    uses_empty_factory = False
    creates_world = False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        call_name = dotted_name(node.func)
        if call_name == "bpy.ops.wm.read_factory_settings":
            for keyword in node.keywords:
                if (
                    keyword.arg == "use_empty"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ):
                    uses_empty_factory = True
        elif call_name == "bpy.data.worlds.new":
            creates_world = True

    assigns_scene_world = any(name.endswith(".world") for name, _ in targets)
    writes_world_color = any(name.endswith(".world.color") for name, _ in targets)

    problems: list[str] = []
    if render_engine_written and stale_eevee_constant:
        problems.append(
            "stale Blender 5.2 render-engine enum BLENDER_EEVEE_NEXT; use the validated 5.2 enum contract"
        )
    if uses_empty_factory and writes_world_color and not (creates_world or assigns_scene_world):
        problems.append(
            "factory empty startup writes scene.world.color without explicitly creating/binding a World"
        )
    return problems


def preflight(producer: Path, validator: Path | None = None) -> None:
    problems = inspect_producer(producer)
    if validator is not None:
        parse_path(validator)
    if problems:
        details = "\n - ".join(problems)
        raise PreflightError(
            "OLEANDER Blender 5.2 producer preflight failed before runtime download:\n - "
            + details
        )


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print(
            "usage: preflight-blender-5.2-producer.py PRODUCER.py [VALIDATOR.py]",
            file=sys.stderr,
        )
        return 2

    producer = Path(argv[1])
    validator = Path(argv[2]) if len(argv) == 3 and argv[2] else None
    try:
        preflight(producer, validator)
    except PreflightError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"OLEANDER Blender 5.2 producer preflight: PASS ({producer})")
    if validator is not None:
        print(f"OLEANDER Blender validation syntax preflight: PASS ({validator})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
