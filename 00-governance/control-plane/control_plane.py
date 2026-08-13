#!/usr/bin/env python3
"""OLEANDER Project Control Plane v0.2 executable core with enforced schema."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

from schema_enforcer import load_schema, validate_instance

HERE = Path(__file__).resolve().parent
CARD_SCHEMA = load_schema(HERE / "control-card.schema.json")
MODES = {"EXPLORE", "CANDIDATE", "AUTHORITY"}
PROBLEM_LAYERS = {"Parameter", "Relation", "Geometry", "Topology", "Architecture", "Evidence"}
PROJECT_LEVELS = {"P0", "P1", "P2", "P3", "P4"}
PRIORITIES = {"Priority-0", "Priority-1", "Priority-2", "Priority-3"}
QA = {"Machine", "Visual", "Project"}
AUTHORITY_STATES = {"NONE", "WORKING_SOURCE", "CANDIDATE_AUTHORITY", "CANONICAL_AUTHORITY", "FROZEN_AUTHORITY", "UNLOCATED"}
SYNC_TRIGGERS = {"NONE", "RECEIPT", "PAP", "FULL_SYNC"}
REVIEW_RESULTS = {"PASS", "REVISE", "REJECT", "BLOCKED", "NOT_RUN"}
APPLICATION_RE = re.compile(r"^(?:B|CU|IP|SP)\d{2}$")
APPLICATION_PROJECT_RE = re.compile(r"^(?:B|CU|IP|SP)\d{2}(?:$|[-_])")
CASE_RE = re.compile(r"^C\d{2,}$")
LEGACY_CASE_PROJECT_RE = re.compile(r"^C\d{2,}(?:-(?:WS|VAL)-|$)")
KNOWLEDGE_RE = re.compile(r"^L[0-7](?:\b|\s|[-/:])")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")

@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str

@dataclass(frozen=True)
class GateProfile:
    mode: str
    base_qa: list[str]
    specialist_gates: list[str]
    persistence: str

@dataclass(frozen=True)
class BreakerResult:
    tripped: bool
    code: str
    next_allowed_action: str
    reason: str


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise ValueError("Control Card root must be a JSON object")
    return value


def validate_card(card: dict[str, Any]) -> list[Finding]:
    findings = [Finding("ERROR", "SCHEMA_VALIDATION", f"{e['path']}: {e['message']}") for e in validate_instance(card, CARD_SCHEMA)]
    obj = card.get("object") if isinstance(card.get("object"), dict) else {}
    project_id = obj.get("project_id")
    if project_id:
        if LEGACY_CASE_PROJECT_RE.match(project_id):
            findings.append(Finding("ERROR", "NAMESPACE_CASE_PROJECT_COLLISION", "Cnn / Cnn-WS-* / Cnn-VAL-* cannot be used as current Project Axis identity"))
        if APPLICATION_PROJECT_RE.match(project_id):
            findings.append(Finding("ERROR", "NAMESPACE_APPLICATION_PROJECT_COLLISION", "B/CU/IP/SP application codes cannot be used as Project IDs"))
    case_id = obj.get("case_id")
    if case_id is not None and (not isinstance(case_id, str) or not CASE_RE.match(case_id)):
        findings.append(Finding("ERROR", "NAMESPACE_CASE_ID", "case_id must be a canonical Cnn identifier"))
    knowledge = obj.get("knowledge_position")
    if knowledge is not None and (not isinstance(knowledge, str) or not KNOWLEDGE_RE.match(knowledge)):
        findings.append(Finding("ERROR", "KNOWLEDGE_POSITION", "knowledge_position must start with exact L0..L7"))
    mappings = obj.get("application_mapping", [])
    if isinstance(mappings, list) and any(not isinstance(x, str) or not APPLICATION_RE.match(x) for x in mappings):
        findings.append(Finding("ERROR", "APPLICATION_MAPPING", "application_mapping values must be Bnn/CUnn/IPnn/SPnn"))
    authority = card.get("authority_source") if isinstance(card.get("authority_source"), dict) else {}
    sha = authority.get("sha256")
    if sha not in (None, "") and (not isinstance(sha, str) or not SHA256_RE.match(sha)):
        findings.append(Finding("ERROR", "AUTHORITY_SHA256", "authority_source.sha256 must be a 64-character hex digest"))
    required_qa = card.get("required_qa")
    if card.get("mode") == "CANDIDATE":
        expected = {"Machine", "Visual", "Project"}
        if isinstance(required_qa, list) and not expected.issubset(required_qa):
            findings.append(Finding("ERROR", "GATE_PROFILE_CANDIDATE_QA", "CANDIDATE requires Machine + Visual + Project QA"))
    if card.get("mode") == "AUTHORITY":
        expected = {"Machine", "Visual", "Project"}
        if isinstance(required_qa, list) and not expected.issubset(required_qa):
            findings.append(Finding("ERROR", "GATE_PROFILE_AUTHORITY_QA", "AUTHORITY requires Machine + Visual + Project QA"))
        if authority.get("state") in {"NONE", "WORKING_SOURCE", "UNLOCATED", None}:
            findings.append(Finding("ERROR", "AUTHORITY_MODE_SOURCE", "AUTHORITY mode requires at least CANDIDATE_AUTHORITY source state"))
    return findings


def resolve_context(card: dict[str, Any]) -> dict[str, Any]:
    obj = card.get("object", {}) if isinstance(card.get("object"), dict) else {}
    return {
        "knowledge_position": obj.get("knowledge_position"),
        "application_mapping": obj.get("application_mapping", []),
        "project": {"id": obj.get("project_id"), "level": obj.get("project_level"), "case_id": obj.get("case_id"), "priority": obj.get("priority")},
        "decision_question": card.get("decision_question"),
        "problem_layer": card.get("problem_layer"),
        "authority_state": (card.get("authority_source") or {}).get("state") if isinstance(card.get("authority_source"), dict) else None,
    }


def select_gate_profile(card: dict[str, Any]) -> GateProfile:
    mode = card.get("mode")
    base = ["Authority Check", "Preflight", "Visual QA"] if mode == "EXPLORE" else ["Machine QA", "Visual QA", "Project QA"]
    gates: set[str] = set()
    artifact_type = card.get("artifact_type")
    claim_types = set(card.get("claim_types", []) or [])
    sync = card.get("sync_persistence_trigger")
    if mode == "AUTHORITY": gates.update({"Artifact Review", "Post-Generation Review"})
    if "rights" in claim_types: gates.add("Rights Gate")
    if "reality" in claim_types or "field" in claim_types: gates.add("Reality Gate")
    if "engineering" in claim_types: gates.add("Engineering Gate")
    if "human_test" in claim_types: gates.add("Human Test Gate")
    if artifact_type in {"production_binary", "release_package"} or sync in {"PAP", "FULL_SYNC"}: gates.add("Production Asset Persistence Gate")
    if mode == "AUTHORITY" and (artifact_type == "release_package" or "release" in claim_types or sync == "FULL_SYNC"):
        gates.add("AR-S09 Release Package Review")
    persistence = "NONE"
    if sync == "RECEIPT": persistence = "RECEIPT"
    elif sync in {"PAP", "FULL_SYNC"} or "Production Asset Persistence Gate" in gates: persistence = "PAP"
    if sync == "FULL_SYNC": persistence = "PAP + PROMOTION-FOCUSED FULL SYNC"
    return GateProfile(mode=mode, base_qa=base, specialist_gates=sorted(gates), persistence=persistence)


def revision_breaker(card: dict[str, Any]) -> BreakerResult:
    history = card.get("review_history", [])
    if not isinstance(history, list) or len(history) < 2:
        return BreakerResult(False, "CB-01_CLEAR", card.get("next_allowed_action", "CONTINUE"), "Fewer than two comparable review results")
    last_two = history[-2:]
    question, layer = card.get("decision_question"), card.get("problem_layer")
    same_context = all(isinstance(item, dict) and item.get("decision_question") == question and item.get("problem_layer") == layer for item in last_two)
    revises = all(item.get("visual_result") == "REVISE" or item.get("project_result") == "REVISE" for item in last_two if isinstance(item, dict))
    if same_context and revises:
        return BreakerResult(True, "CB-01_REPEATED_REVISE", "ROOT_CAUSE_RECLASSIFICATION", f"Two consecutive REVISE results for the same Decision Question at problem layer {layer}; same-layer tuning is blocked")
    return BreakerResult(False, "CB-01_CLEAR", card.get("next_allowed_action", "CONTINUE"), "No two-consecutive same-context REVISE pattern")


def _registry_candidates(registry: Any, name: str) -> Iterable[dict[str, Any]]:
    if isinstance(registry, dict): registry = registry.get("assets", [])
    if not isinstance(registry, list): return []
    target = name.casefold()
    return [item for item in registry if isinstance(item, dict) and target in str(item.get("name", item.get("id", ""))).casefold()]


def locate_asset(name: str, roots: Iterable[str | Path] = (), registry: Any = None) -> dict[str, Any]:
    registry_hits = list(_registry_candidates(registry, name)) if registry is not None else []
    fs_hits: list[str] = []
    target = name.casefold()
    for root in roots:
        p = Path(root)
        if not p.exists(): continue
        for candidate in p.rglob("*"):
            if candidate.is_file() and target in candidate.name.casefold(): fs_hits.append(str(candidate.resolve()))
    return {"query": name, "status": "FOUND" if registry_hits or fs_hits else "UNLOCATED", "registry_hits": registry_hits, "filesystem_hits": sorted(fs_hits), "external_provider_status": "REQUIRES_MATERIALIZATION_OR_REGISTRY_INPUT"}


def run_check(card: dict[str, Any]) -> dict[str, Any]:
    findings = validate_card(card)
    breaker = revision_breaker(card)
    profile = select_gate_profile(card) if card.get("mode") in MODES else None
    blocking = any(f.level == "ERROR" for f in findings) or breaker.tripped
    return {"status": "BLOCKED" if blocking else "PASS", "context": resolve_context(card), "findings": [asdict(f) for f in findings], "gate_profile": asdict(profile) if profile else None, "revision_breaker": asdict(breaker)}


def _print(value: Any) -> None: print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OLEANDER Project Control Plane v0.2")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "resolve", "gates", "breaker", "check"):
        p = sub.add_parser(name); p.add_argument("card")
    locate = sub.add_parser("locate"); locate.add_argument("name"); locate.add_argument("--root", action="append", default=[]); locate.add_argument("--registry")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "locate":
        registry = load_json(args.registry) if args.registry else None
        result = locate_asset(args.name, args.root, registry); _print(result); return 0 if result["status"] == "FOUND" else 3
    card = load_json(args.card)
    if args.command == "validate":
        findings = validate_card(card); ok = not any(f.level == "ERROR" for f in findings); _print({"status": "PASS" if ok else "FAIL", "findings": [asdict(f) for f in findings]}); return 0 if ok else 2
    if args.command == "resolve":
        findings = validate_card(card)
        if any(f.level == "ERROR" for f in findings): _print({"status":"FAIL","findings":[asdict(f) for f in findings]}); return 2
        _print(resolve_context(card)); return 0
    if args.command == "gates":
        findings = validate_card(card)
        if any(f.level == "ERROR" for f in findings): _print({"status":"FAIL","findings":[asdict(f) for f in findings]}); return 2
        _print(asdict(select_gate_profile(card))); return 0
    if args.command == "breaker":
        result = revision_breaker(card); _print(asdict(result)); return 4 if result.tripped else 0
    if args.command == "check":
        result = run_check(card); _print(result); return 0 if result["status"] == "PASS" else 5
    return 1

if __name__ == "__main__": raise SystemExit(main())
