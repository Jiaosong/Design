#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
REGISTRY = RUNTIME / "OLEANDER_TYPED_ENUM_SCHEMA_REGISTRY_v0.1.json"
MIGRATION = RUNTIME / "OLEANDER_TYPED_COMPATIBILITY_MIGRATION_MAP_v0.1.json"
MANIFEST = RUNTIME / "OLEANDER_TYPED_SCHEMA_COMPILER_MANIFEST_v0.1.json"


def die(msg: str) -> None:
    raise SystemExit(f"typed-schema compiler failed: {msg}")


def load(path: Path) -> Any:
    if not path.is_file():
        die(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        die(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def extract_rb_tokens(value: Any) -> list[str]:
    tokens: set[str] = set()

    def walk(v: Any) -> None:
        if isinstance(v, str):
            for token in re.findall(r"\bRB[0-4]\b", v):
                tokens.add(token)
        elif isinstance(v, list):
            for item in v:
                walk(item)
        elif isinstance(v, dict):
            for item in v.values():
                walk(item)

    walk(value)
    return sorted(tokens)


def resolve_pointer(data: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        die(f"unsupported pointer {pointer}")
    current = data
    for raw in pointer[1:].split("/"):
        segment = raw.replace("~1", "/").replace("~0", "~")
        if segment == "@keys":
            if not isinstance(current, dict):
                die(f"@keys requires object at {pointer}")
            current = sorted(current.keys())
            continue
        if segment == "@derived_readback_tokens":
            current = extract_rb_tokens(current)
            continue
        if isinstance(current, dict) and segment in current:
            current = current[segment]
            continue
        die(f"unresolved pointer {pointer}; missing segment {segment}")
    return current


def validate_source_owner(symbol: str, spec: dict[str, Any], source: dict[str, Any]) -> None:
    expected = spec.get("owner")
    declared = source.get("semantic_owner")
    declared_many = source.get("semantic_owners")
    if declared is not None and declared != expected:
        die(f"{symbol}: source semantic_owner={declared!r} != registry owner={expected!r}")
    if declared_many is not None and expected not in declared_many:
        die(f"{symbol}: registry owner {expected!r} not present in source semantic_owners")


def compile_package() -> dict[str, Any]:
    registry = load(REGISTRY)
    migration = load(MIGRATION)
    manifest = load(MANIFEST)

    if registry.get("principle") != "ONE_SEMANTIC_ENUM_ONE_OWNER_POINTER_NO_VALUE_COPY":
        die("enum registry principle mismatch")
    if manifest.get("inputs", {}).get("enum_registry") != REGISTRY.name:
        die("compiler manifest enum_registry pointer mismatch")
    if manifest.get("inputs", {}).get("migration_map") != MIGRATION.name:
        die("compiler manifest migration_map pointer mismatch")

    compiled: dict[str, Any] = {}
    semantic_scopes: dict[str, str] = {}

    for symbol, spec in registry.get("symbols", {}).items():
        source_name = spec.get("source_file")
        pointer = spec.get("json_pointer")
        scope = spec.get("semantic_scope")
        if not source_name or not pointer or not scope:
            die(f"{symbol}: missing source_file/json_pointer/semantic_scope")
        source_path = RUNTIME / source_name
        source = load(source_path)
        validate_source_owner(symbol, spec, source)
        values = resolve_pointer(source, pointer)
        if values in (None, [], {}):
            die(f"{symbol}: resolved enum values empty")
        if scope in semantic_scopes and semantic_scopes[scope] != symbol:
            die(f"semantic_scope {scope} claimed by both {semantic_scopes[scope]} and {symbol}")
        semantic_scopes[scope] = symbol
        compiled[symbol] = {
            "namespace": spec.get("namespace"),
            "owner": spec.get("owner"),
            "semantic_scope": scope,
            "source_file": source_name,
            "source_sha256": digest(source_path),
            "json_pointer": pointer,
            "values": values,
        }

    aliases = migration.get("mappings", {})
    for alias_id, mapping in aliases.items():
        if not isinstance(mapping, dict):
            die(f"migration mapping {alias_id} must be an object")
        if mapping.get("migration") == "LOSSLESS_ALIAS" and not mapping.get("canonical"):
            die(f"lossless alias {alias_id} missing canonical value")
        if mapping.get("migration") == "CONTEXTUAL_NOT_ONE_TO_ONE" and not mapping.get("mapping_guidance"):
            die(f"contextual mapping {alias_id} missing mapping_guidance")

    p4 = aliases.get("P4_REGISTRY_LABEL", {})
    assurance_values = set(compiled.get("ASSURANCE_TYPE", {}).get("values", []))
    declared_assurance = set(p4.get("allowed_assurance_types", []))
    if declared_assurance and declared_assurance != assurance_values:
        die(
            "P4 registry compatibility assurance types drift from P6 ASSURANCE_TYPE: "
            f"compat={sorted(declared_assurance)} owner={sorted(assurance_values)}"
        )

    return {
        "schema": "OLEANDER_TYPED_COMPILED_SCHEMA_v0.1",
        "status": "COMPILED_FROM_DRAFT_OWNERS_NOT_CURRENT",
        "compiler_manifest_sha256": digest(MANIFEST),
        "enum_registry_sha256": digest(REGISTRY),
        "migration_map_sha256": digest(MIGRATION),
        "enum_count": len(compiled),
        "enums": compiled,
        "compatibility_mappings": aliases,
        "hard_boundary": "COMPILED_SCHEMA_DOES_NOT_PROMOTE_GOVERNANCE_CURRENT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile OLEANDER typed enum/schema owner registry")
    parser.add_argument("--check", action="store_true", help="validate owner pointers and compatibility maps")
    parser.add_argument("--output", type=Path, help="write compiled package JSON")
    parser.add_argument("--json", action="store_true", help="print compiled package JSON")
    args = parser.parse_args()

    package = compile_package()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"typed-schema compiler PASS: enums={package['enum_count']} aliases={len(package['compatibility_mappings'])}")


if __name__ == "__main__":
    main()
