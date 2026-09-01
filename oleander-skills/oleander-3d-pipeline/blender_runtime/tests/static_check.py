"""Repository-level static checks for the OLEANDER Blender Runtime.

This intentionally does not import bpy. It verifies syntax and contract/version
consistency in ordinary CPython. Blender runtime behavior is covered separately
by validate_stage2.py inside a real Blender process.
"""

from __future__ import annotations

import ast
import json
import pathlib
import tomllib

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"


def fail(message: str) -> None:
    raise SystemExit(f"STATIC_CHECK_FAIL: {message}")


def parse_bl_info_version(init_path: pathlib.Path) -> str:
    tree = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "bl_info" for target in node.targets):
            continue
        value = ast.literal_eval(node.value)
        version = value.get("version")
        if not isinstance(version, tuple) or not all(isinstance(v, int) for v in version):
            fail("bl_info.version is not an integer tuple")
        return ".".join(str(v) for v in version)
    fail("bl_info assignment not found")
    return ""


def main() -> None:
    python_files = sorted(ADDON_ROOT.rglob("*.py")) + sorted((RUNTIME_ROOT / "tests").rglob("*.py"))
    if not python_files:
        fail("no Python files found")

    for path in python_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    manifest_path = ADDON_ROOT / "blender_manifest.toml"
    with manifest_path.open("rb") as handle:
        manifest = tomllib.load(handle)

    capability = json.loads((PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8"))
    schema = json.loads((ADDON_ROOT / "workbench_manifest.schema.json").read_text(encoding="utf-8"))

    bl_info_version = parse_bl_info_version(ADDON_ROOT / "__init__.py")
    manifest_version = manifest.get("version")
    capability_version = capability.get("runtime_version")

    versions = {bl_info_version, manifest_version, capability_version}
    if len(versions) != 1:
        fail(f"version mismatch bl_info={bl_info_version} manifest={manifest_version} capability={capability_version}")

    if capability.get("lifecycle_state") != "PROPOSED_UNVERIFIED_RUNTIME":
        fail("runtime must remain PROPOSED_UNVERIFIED_RUNTIME until real Blender validation evidence exists")

    if manifest.get("blender_version_min") != "5.1.0":
        fail("unexpected minimum Blender version")

    required_impl = {
        "dependency_graph",
        "stale_dependency_propagation",
        "geometry_baseline_diff",
        "review_state_separation",
        "export_manifest_v0.2",
    }
    implemented = set(capability.get("implementation_status", {}).get("IMPLEMENTED_UNVERIFIED", []))
    missing = sorted(required_impl - implemented)
    if missing:
        fail(f"capability contract missing implemented-unverified entries: {missing}")

    schema_const = schema.get("properties", {}).get("schema", {}).get("const")
    if schema_const != "OLEANDER_BLENDER_WORKBENCH_MANIFEST_v0.2":
        fail(f"workbench manifest schema const mismatch: {schema_const}")

    print(
        json.dumps(
            {
                "status": "PASS",
                "python_files_parsed": len(python_files),
                "runtime_version": bl_info_version,
                "lifecycle_state": capability["lifecycle_state"],
                "note": "Static PASS is not Blender runtime PASS.",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
