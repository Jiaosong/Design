#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
CONTRACT = RUNTIME / "OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json"
CASES = RUNTIME / "runtime_provider_spikes" / "provider_conformance_cases_v0.1.json"
RESULTS = RUNTIME / "runtime_provider_spikes" / "results"
EXECUTION_RECEIPTS = RUNTIME / "receipts"
BENCHMARK_RESULT = RESULTS / "OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.json"


def fail(message: str) -> None:
    raise SystemExit(f"runtime-provider-contract validation failed: {message}")


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive validator boundary
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    contract = load(CONTRACT)
    cases = load(CASES)
    if contract.get("status") != "CANDIDATE_NON_AUTHORITY":
        fail("provider contract must remain candidate/non-authority before explicit promotion")
    if contract.get("authority_ceiling") != "EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY":
        fail("authority ceiling drifted")
    providers = contract.get("providers_under_spike") or []
    if providers != ["native_cos", "deepseek_harness", "microsoft_agent_framework", "pydantic_ai_temporal"]:
        fail("provider spike set drifted")
    rules = set(contract.get("guard_rules") or [])
    for required in {
        "OLEANDER_ACTION_GUARD_PRECEDES_PROVIDER_NATIVE_APPROVAL",
        "PROVIDER_APPROVAL_MAY_NARROW_BUT_NEVER_WIDEN_OLEANDER_PERMISSION",
        "READ_ONLY_DOES_NOT_AUTO_AUTHORIZE_SENSITIVE_EXTERNAL_DISCLOSURE",
    }:
        if required not in rules:
            fail(f"missing guard rule {required}")
    ledger = contract.get("execution_ledger") or {}
    forbidden = set(ledger.get("forbidden_authority_fields") or [])
    for required in {"project_state", "project_current", "design_decision", "design_keep", "professional_pass", "promotion"}:
        if required not in forbidden:
            fail(f"missing forbidden authority field {required}")
    rows = cases.get("cases") or []
    ids = [row.get("case_id") for row in rows]
    if len(rows) != 9 or len(set(ids)) != 9:
        fail("expected exactly 9 unique conformance cases")
    required_fields = set(contract.get("action_envelope_required_fields") or [])
    for row in rows:
        action = row.get("action") or {}
        missing = sorted(required_fields - set(action))
        if missing:
            fail(f"{row.get('case_id')} missing action fields: {missing}")
    polluted = list(EXECUTION_RECEIPTS.glob("OLEANDER_RUNTIME_PROVIDER_BENCHMARK_*"))
    if polluted:
        fail("provider benchmark evidence must not live in runtime/receipts; it is not an Execution Receipt")
    if not RESULTS.is_dir():
        fail("candidate provider benchmark results directory missing")
    result = load(BENCHMARK_RESULT)
    if result.get("schema") != "oleander.runtime-provider-benchmark.v0.1":
        fail("benchmark result schema drifted")
    if result.get("benchmark_scope") != "CONTRACT_SHIM_PLUS_BOUNDED_NATIVE_SMOKE":
        fail("benchmark scope must remain explicitly bounded")
    if result.get("status") != "PASS_CANDIDATE_SPIKE":
        fail("committed benchmark evidence is not PASS_CANDIDATE_SPIKE")
    cross = result.get("cross_provider_checks") or {}
    if cross.get("contract_shim_identity_fingerprint_stable_across_providers") is not True:
        fail("contract-shim cross-provider identity stability is not proven")
    if "provider_switch_preserves_project_identity" in cross:
        fail("benchmark must not overclaim a real provider switch from shim identity stability")
    result_providers = result.get("providers") or []
    if [row.get("provider_id") for row in result_providers] != providers:
        fail("benchmark provider set/order drifted")
    for row in result_providers:
        if row.get("contract_state") != "CONTRACT_PASS" or row.get("passed_cases") != 9 or row.get("total_cases") != 9:
            fail(f"benchmark contract evidence incomplete for {row.get('provider_id')}")
    print("runtime provider contract: PASS")
    print("candidate/non-authority boundary: ENFORCED")
    print("provider benchmark != execution receipt: ENFORCED")
    print("committed bounded benchmark evidence: VERIFIED")
    print("4 provider spikes / 9 shared conformance cases: CONSISTENT")


if __name__ == "__main__":
    main()
