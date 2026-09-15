#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
REGISTRY = RUNTIME / "OLEANDER_TYPED_SYSTEM_VALIDATOR_RULE_REGISTRY_v0.1.json"
CENTRAL_EVALS = RUNTIME / "OLEANDER_TYPED_SYSTEM_REGRESSION_EVALS_v0.1.json"
BINDING_GLOB = "OLEANDER_P*_EXECUTABLE_BINDING_v0.1.json"
REPLAY_GLOB = "OLEANDER_REPLAY_*.json"
EXPECTED_PRINCIPLE = "EXECUTABLE_COMPANION_DOES_NOT_BECOME_SECOND_SEMANTIC_OWNER"


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"executable-companion validation failed: {path.name}: {exc}")


def expected_rule_refs(payload: dict[str, Any]) -> tuple[set[str], list[str], list[str]]:
    refs: set[str] = set()
    case_ids: list[str] = []
    malformed: list[str] = []
    for case in payload.get("cases", []):
        cid = case.get("id")
        if isinstance(cid, str) and cid:
            case_ids.append(cid)
        else:
            malformed.append(str(cid))
        expected = case.get("expected", [])
        if not isinstance(expected, list) or not expected:
            malformed.append(str(cid))
            continue
        for item in expected:
            if isinstance(item, str) and "/" in item:
                refs.add(item.split(":", 1)[0])
            else:
                malformed.append(str(cid))
    return refs, case_ids, malformed


def main() -> None:
    registry = load(REGISTRY)
    central_evals = load(CENTRAL_EVALS)

    registry_rules: set[str] = set()
    for rules in registry.get("rules", {}).values():
        registry_rules.update(rules)

    replay_rules: set[str] = set()
    replay_sources: set[str] = set()
    for path in sorted(RUNTIME.glob(REPLAY_GLOB)):
        replay = load(path)
        replay_id = replay.get("replay_id")
        if replay_id:
            replay_sources.add(str(replay_id))
        raw = replay.get("replay_derived_rules", [])
        if isinstance(raw, dict):
            raw = list(raw)
        if isinstance(raw, list):
            replay_rules.update(x for x in raw if isinstance(x, str) and "/" in x)

    central_refs, central_ids, central_malformed = expected_rule_refs(central_evals)
    failures: list[str] = []
    notices: list[str] = []
    companion_refs: set[str] = set()
    binding_rules_all: set[str] = set()
    binding_names: list[str] = []

    if central_malformed:
        failures.append(f"central regression corpus has malformed cases: {sorted(set(central_malformed))}")
    if len(central_ids) != len(set(central_ids)):
        failures.append("central regression corpus has duplicate case IDs")

    bindings = sorted(RUNTIME.glob(BINDING_GLOB))
    if not bindings:
        failures.append("no executable companion bindings discovered")

    for binding_path in bindings:
        binding = load(binding_path)
        binding_names.append(binding_path.name)
        principle = binding.get("principle")
        if principle != EXPECTED_PRINCIPLE:
            failures.append(f"{binding_path.name}: principle mismatch")

        owners = binding.get("semantic_owners")
        if owners is None:
            owner = binding.get("semantic_owner")
            owners = [owner] if owner else []
        if not isinstance(owners, list) or not owners or any(not isinstance(x, str) or not x for x in owners):
            failures.append(f"{binding_path.name}: semantic_owner(s) missing")

        required_files = {
            "semantic_companion": binding.get("semantic_companion"),
            "implementation": binding.get("implementation"),
            "deterministic_self_test": binding.get("deterministic_self_test"),
            "regression_corpus": binding.get("regression_corpus"),
        }
        for field, filename in required_files.items():
            if not isinstance(filename, str) or not filename:
                failures.append(f"{binding_path.name}: missing {field}")
            elif not (RUNTIME / filename).is_file():
                failures.append(f"{binding_path.name}: {field} file missing: {filename}")

        rules = binding.get("executable_rules", [])
        if not isinstance(rules, list) or not rules:
            failures.append(f"{binding_path.name}: executable_rules missing/empty")
            continue
        rules_set = {x for x in rules if isinstance(x, str) and "/" in x}
        if len(rules_set) != len(rules):
            failures.append(f"{binding_path.name}: executable_rules contain duplicates or invalid IDs")
        binding_rules_all.update(rules_set)

        unregistered = sorted(rules_set - registry_rules)
        if unregistered:
            failures.append(f"{binding_path.name}: executable rules absent from central registry: {unregistered}")

        semantic_filename = binding.get("semantic_companion")
        if isinstance(semantic_filename, str) and (RUNTIME / semantic_filename).is_file():
            semantic = load(RUNTIME / semantic_filename)
            semantic_rules = set(semantic.get("validator_rules", [])) | set(semantic.get("replay_derived_rules", []))
            missing_semantic = sorted(rules_set - semantic_rules)
            if missing_semantic:
                failures.append(f"{binding_path.name}: executable rules absent from semantic companion: {missing_semantic}")

            declared_semantic_owners = semantic.get("semantic_owners")
            if declared_semantic_owners is None:
                declared = semantic.get("semantic_owner")
                declared_semantic_owners = [declared] if declared else []
            if declared_semantic_owners and not set(owners).issubset(set(declared_semantic_owners)):
                failures.append(
                    f"{binding_path.name}: binding semantic owner(s) drift from semantic companion: "
                    f"binding={sorted(owners)} companion={sorted(declared_semantic_owners)}"
                )

        eval_filename = binding.get("regression_corpus")
        if isinstance(eval_filename, str) and (RUNTIME / eval_filename).is_file():
            companion_eval = load(RUNTIME / eval_filename)
            eval_refs, case_ids, malformed = expected_rule_refs(companion_eval)
            if malformed:
                failures.append(f"{binding_path.name}: malformed companion eval cases: {sorted(set(malformed))}")
            if len(case_ids) != len(set(case_ids)):
                failures.append(f"{binding_path.name}: duplicate companion eval case IDs")
            unknown_refs = sorted(eval_refs - rules_set)
            if unknown_refs:
                failures.append(f"{binding_path.name}: companion eval references rules outside binding: {unknown_refs}")
            uncovered = sorted(rules_set - eval_refs)
            if uncovered:
                failures.append(f"{binding_path.name}: executable rules lack companion regression references: {uncovered}")
            companion_refs.update(eval_refs)

        replay_source_ids = binding.get("replay_sources", [])
        if not isinstance(replay_source_ids, list):
            failures.append(f"{binding_path.name}: replay_sources must be a list")
        else:
            unknown_sources = sorted({str(x) for x in replay_source_ids} - replay_sources)
            if unknown_sources:
                failures.append(f"{binding_path.name}: replay_sources not found in replay records: {unknown_sources}")

        non_replay_rules = sorted(rules_set - replay_rules)
        if non_replay_rules:
            notices.append(f"{binding_path.name}: executable rules not replay-derived in discovered replay JSON: {non_replay_rules}")

    covered = central_refs | companion_refs
    uncovered_replay = sorted(replay_rules - covered)
    registered_replay = replay_rules & registry_rules
    missing_registry = sorted(replay_rules - registry_rules)
    if missing_registry:
        failures.append(f"replay-derived rules absent from central registry: {missing_registry}")

    print("OLEANDER executable companion validation")
    print(f"bindings={len(bindings)} binding_rules={len(binding_rules_all)}")
    print(f"central_eval_refs={len(central_refs)} companion_eval_refs={len(companion_refs)}")
    print(f"replay_rules={len(replay_rules)} registered_replay_rules={len(registered_replay)}")
    print(f"uncovered_replay_rules={len(uncovered_replay)}")
    if uncovered_replay:
        print("coverage_debt=" + ",".join(uncovered_replay))
    for notice in notices:
        print("NOTICE: " + notice)

    if failures:
        for failure in failures:
            print("FAIL: " + failure)
        sys.exit(1)

    print("PASS: executable companion bindings, semantic-owner links, companion regressions and registry references are internally consistent")


if __name__ == "__main__":
    main()
