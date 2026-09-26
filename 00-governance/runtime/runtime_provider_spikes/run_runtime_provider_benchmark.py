from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from provider_adapters import provider_adapters, runtime_environment_snapshot


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_CASES = HERE / "provider_conformance_cases_v0.1.json"
DEFAULT_OUTPUT = HERE / "results" / "OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.json"


def load_cases(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("provider conformance fixture must contain non-empty cases[]")
    return cases


def run_benchmark(*, cases_path: Path, provider_python: str | None) -> dict[str, Any]:
    cases = load_cases(cases_path)
    providers: list[dict[str, Any]] = []

    for adapter in provider_adapters(provider_python=provider_python):
        probe = adapter.native_probe().as_dict()
        case_results = [adapter.run_contract_case(case) for case in cases]
        contract_pass = all(row["state"] == "PASS" for row in case_results)
        providers.append(
            {
                "provider_id": adapter.provider_id,
                "contract_state": "CONTRACT_PASS" if contract_pass else "CONTRACT_FAIL",
                "native_probe": probe,
                "case_results": case_results,
                "passed_cases": sum(1 for row in case_results if row["state"] == "PASS"),
                "total_cases": len(case_results),
            }
        )

    identity_fingerprints: dict[str, set[str]] = {}
    for provider in providers:
        for row in provider["case_results"]:
            identity_fingerprints.setdefault(row["case_id"], set()).add(row["project_state_fingerprint_after"])
    contract_identity_stable = all(len(values) == 1 for values in identity_fingerprints.values())

    native_smoke_pass = all(p["native_probe"]["state"] == "NATIVE_PROVIDER_SMOKE_PASS" for p in providers)
    contract_pass = all(p["contract_state"] == "CONTRACT_PASS" for p in providers)
    return {
        "schema": "oleander.runtime-provider-benchmark.v0.1",
        "status": "PASS_CANDIDATE_SPIKE" if contract_pass and native_smoke_pass and contract_identity_stable else "HOLD_CANDIDATE_SPIKE",
        "benchmark_scope": "CONTRACT_SHIM_PLUS_BOUNDED_NATIVE_SMOKE",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "authority_ceiling": "EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY",
        "contract_ref": "00-governance/runtime/OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json",
        "cases_ref": str(cases_path.relative_to(ROOT)).replace("\\", "/"),
        "environment": runtime_environment_snapshot(provider_python),
        "providers": providers,
        "cross_provider_checks": {
            "contract_shim_identity_fingerprint_stable_across_providers": contract_identity_stable,
            "all_contracts_pass": contract_pass,
            "all_native_smokes_pass": native_smoke_pass,
        },
        "does_not_prove": [
            "provider_production_readiness",
            "provider_performance_superiority",
            "real_model_quality",
            "real_artifact_authoring_parity",
            "external_pilot_value",
            "design_quality",
            "professional_pass",
            "promotion",
        ],
        "next_required_evidence": [
            "REAL_NATIVE_ARTIFACT_ACTION_PER_PROVIDER",
            "PROVIDER_REMOVAL_AND_RESUME_TEST",
            "ACTION_GUARD_WITH_REAL_PROVIDER_APPROVAL_PATH",
            "FAILURE_RECOVERY_WITH_ACTUAL_PROVIDER_INTERRUPTION",
            "LATENCY_AND_IMPLEMENTATION_COMPLEXITY_MEASUREMENT",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OLEANDER provider-neutral runtime contract and native-provider smoke benchmark.")
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--provider-python", default=None, help="Python executable containing optional provider packages.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    result = run_benchmark(cases_path=Path(args.cases).resolve(), provider_python=args.provider_python)
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty))
    raise SystemExit(0 if result["status"] == "PASS_CANDIDATE_SPIKE" else 2)


if __name__ == "__main__":
    main()
