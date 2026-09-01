"""Repository-level static checks for the OLEANDER Blender Runtime.

This intentionally does not import bpy. It verifies syntax, contract/version
consistency, and validation-receipt integrity in ordinary CPython. Blender
runtime behavior is covered separately by validate_stage2.py inside a real
Blender process.
"""

from __future__ import annotations

import ast
import hashlib
import json
import pathlib
import tomllib

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"
VALIDATION_SCRIPT = RUNTIME_ROOT / "tests" / "validate_stage2.py"

UNVERIFIED_STATE = "PROPOSED_UNVERIFIED_RUNTIME"
VALIDATED_STATE = "VALIDATED_STAGE2_HEADLESS_CORE"
VALIDATED_SCOPE = "STAGE2_HEADLESS_CORE_AND_EXTENSION_PACKAGE"


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


def runtime_source_fingerprint() -> str:
    """Fingerprint files whose material change invalidates runtime evidence."""
    paths = [
        path
        for path in ADDON_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}
    ]
    paths.append(VALIDATION_SCRIPT)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        rel = path.relative_to(PIPELINE_ROOT).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_validation_receipt(capability: dict) -> dict | None:
    lifecycle = capability.get("lifecycle_state")
    receipt_ref = capability.get("validation_receipt")

    if lifecycle == UNVERIFIED_STATE:
        if receipt_ref:
            fail("unverified lifecycle must not claim a validation receipt")
        return None

    if lifecycle != VALIDATED_STATE:
        fail(f"unsupported lifecycle_state: {lifecycle}")

    if not isinstance(receipt_ref, str) or not receipt_ref.strip():
        fail("validated lifecycle requires validation_receipt")

    repo_root = PIPELINE_ROOT.parents[1]
    receipt_path = repo_root / receipt_ref
    try:
        receipt_path.relative_to(repo_root)
    except ValueError:
        fail("validation receipt must resolve inside repository")
    if not receipt_path.is_file():
        fail(f"validation receipt not found: {receipt_ref}")

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("validation_state") != "PASS":
        fail("validated lifecycle requires validation_state PASS")
    if receipt.get("validation_scope") != VALIDATED_SCOPE:
        fail(f"unexpected validation scope: {receipt.get('validation_scope')}")
    if receipt.get("runtime_id") != capability.get("runtime_id"):
        fail("validation receipt runtime_id mismatch")
    if receipt.get("runtime_version") != capability.get("runtime_version"):
        fail("validation receipt runtime_version mismatch")
    if receipt.get("runtime_result") != "PASS":
        fail("validation receipt runtime_result must be PASS")

    expected_fingerprint = runtime_source_fingerprint()
    receipt_fingerprint = receipt.get("source_fingerprint_sha256")
    if receipt_fingerprint != expected_fingerprint:
        fail(
            "runtime validation receipt is stale for current source fingerprint "
            f"receipt={receipt_fingerprint!r} current={expected_fingerprint}"
        )

    workflow = receipt.get("workflow", {})
    if workflow.get("conclusion") != "success" or not workflow.get("run_id") or not workflow.get("job_id"):
        fail("validation receipt must identify a successful workflow run and job")

    package = receipt.get("extension_package", {})
    package_gates = (
        "source_manifest_validate",
        "build",
        "built_package_validate",
    )
    failed_package_gates = [gate for gate in package_gates if package.get(gate) != "PASS"]
    if failed_package_gates:
        fail(f"extension-package validation gates not PASS: {failed_package_gates}")
    if not package.get("sha256") or not package.get("size_bytes"):
        fail("validated extension package requires SHA256 and byte size")

    host = receipt.get("host", {})
    if host.get("checksum_manifest_result") != "PASS" or not host.get("blender_archive_sha256"):
        fail("validated Blender host requires official checksum PASS and archive SHA256")

    tested_head = receipt.get("tested_branch_head")
    if not isinstance(tested_head, str) or len(tested_head) != 40:
        fail("validation receipt tested_branch_head must be a full commit SHA")

    return receipt


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

    receipt = load_validation_receipt(capability)

    if manifest.get("blender_version_min") != "5.1.0":
        fail("unexpected minimum Blender version")

    required_impl = {
        "dependency_graph_resolution",
        "stale_dependency_propagation",
        "geometry_baseline_diff",
        "review_state_separation",
        "export_manifest_v0.2_core",
    }
    status = capability.get("implementation_status", {})
    declared = set(status.get("VALIDATED_STAGE2_HEADLESS", [])) | set(status.get("IMPLEMENTED_UNVERIFIED", []))
    missing = sorted(required_impl - declared)
    if missing:
        fail(f"capability contract missing required implementation entries: {missing}")

    validated = set(status.get("VALIDATED_STAGE2_HEADLESS", []))
    if capability.get("lifecycle_state") == VALIDATED_STATE:
        receipt_checks = set((receipt or {}).get("runtime_checks", []))
        required_receipt_checks = {
            "registration",
            "persistent_metadata",
            "dependency_graph",
            "stale_propagation",
            "geometry_baseline_diff",
            "configuration_capture_restore",
            "bom_grouping_and_conflict_detection",
            "review_state_separation",
            "scene_unit_scale_round_trip",
            "blend_save_reopen_persistence",
            "audit_v0.2",
            "manifest_v0.2",
        }
        missing_checks = sorted(required_receipt_checks - receipt_checks)
        if missing_checks:
            fail(f"validated lifecycle receipt missing required runtime checks: {missing_checks}")
        if not validated:
            fail("validated lifecycle requires non-empty VALIDATED_STAGE2_HEADLESS capability set")

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
                "source_fingerprint_sha256": runtime_source_fingerprint(),
                "validation_receipt": capability.get("validation_receipt", ""),
                "note": "Static PASS validates receipt/contract integrity; it is not a substitute for Blender runtime execution.",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
