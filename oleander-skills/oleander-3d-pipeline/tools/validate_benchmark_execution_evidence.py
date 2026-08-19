#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(code: str):
    raise SystemExit(code)


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get('schema') != contract.get('receipt_schema'):
        fail('FAIL_BENCHMARK_RECEIPT_SCHEMA')
    for key in contract.get('required', []):
        if key not in receipt:
            fail(f'FAIL_BENCHMARK_RECEIPT_MISSING_{key.upper()}')

    runtime = receipt.get('runtime') or {}
    for key in contract.get('runtime_required', []):
        if key not in runtime:
            fail(f'FAIL_RUNTIME_WITNESS_MISSING_{key.upper()}')

    invocation = receipt.get('invocation') or {}
    for key in contract.get('invocation_required', []):
        if key not in invocation:
            fail(f'FAIL_INVOCATION_WITNESS_MISSING_{key.upper()}')

    readback = receipt.get('output_readback') or {}
    for key in contract.get('output_readback_required', []):
        if key not in readback:
            fail(f'FAIL_OUTPUT_READBACK_MISSING_{key.upper()}')

    baseline = receipt.get('baseline_comparison') or {}
    for key in contract.get('baseline_required', []):
        if key not in baseline:
            fail(f'FAIL_BASELINE_COMPARISON_MISSING_{key.upper()}')

    execution = receipt.get('execution_result')
    if execution not in contract.get('execution_results', []):
        fail('FAIL_EXECUTION_RESULT_INVALID')
    if receipt.get('experiment_result') not in contract.get('experiment_results', []):
        fail('FAIL_EXPERIMENT_RESULT_INVALID')
    if receipt.get('evidence_result') not in contract.get('evidence_results', []):
        fail('FAIL_EVIDENCE_RESULT_INVALID')
    if receipt.get('design_result') not in contract.get('design_results', []):
        fail('FAIL_DESIGN_RESULT_INVALID')

    target = receipt.get('target_revision')
    if execution == 'PASS_EXECUTED':
        if not invocation.get('target_revision_invoked'):
            fail('FAIL_TARGET_REVISION_NOT_EXECUTED')
        if invocation.get('exit_code') != 0:
            fail('FAIL_EXECUTION_PASS_WITH_NONZERO_EXIT')
        if not readback.get('receipt_exists') or not readback.get('artifact_readback'):
            fail('FAIL_OUTPUT_READBACK_MISSING')
        if readback.get('receipt_target_revision') != target:
            fail('FAIL_RECEIPT_TARGET_REVISION_MISMATCH')
        if runtime.get('runtime_support_state') not in ('VERIFIED_AVAILABLE', 'VERIFIED_EXECUTED'):
            fail('FAIL_EXECUTION_PASS_WITH_UNVERIFIED_RUNTIME')

    if baseline.get('required'):
        if not baseline.get('baseline_revision') or not baseline.get('candidate_revision'):
            fail('HOLD_BENCHMARK_COMPARABILITY_UNRESOLVED')
        if baseline.get('candidate_revision') != target:
            fail('FAIL_BASELINE_CANDIDATE_TARGET_MISMATCH')
        if not baseline.get('same_runtime_or_declared_delta'):
            fail('HOLD_BENCHMARK_RUNTIME_COMPARABILITY_UNRESOLVED')
        if baseline.get('comparability') not in ('CONTROLLED', 'PARTIAL_DECLARED_RUNTIME_DELTA'):
            fail('FAIL_BENCHMARK_COMPARABILITY_INVALID')

    if execution == 'PASS_EXECUTED' and receipt.get('design_result') == 'PASS_INDEPENDENT_DESIGN_REVIEW':
        # Allowed only as an independently supplied result. It must not be inferred from machine state.
        if not receipt.get('independent_design_review_receipt'):
            fail('FAIL_MACHINE_EXECUTION_SELF_PROMOTED_TO_DESIGN_PASS')

    if not isinstance(receipt.get('does_not_prove'), list) or not receipt.get('does_not_prove'):
        fail('FAIL_DOES_NOT_PROVE_MISSING')
    return True


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) not in (1, 2):
        raise SystemExit('usage: validate_benchmark_execution_evidence.py RECEIPT.json [CONTRACT.json]')
    receipt = json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    contract_path = Path(argv[1]) if len(argv) == 2 else Path(__file__).resolve().parents[1] / 'contracts' / 'BENCHMARK_EXECUTION_EVIDENCE_CONTRACT_v1.json'
    contract = json.loads(contract_path.read_text(encoding='utf-8'))
    validate(receipt, contract)
    print('PASS_BENCHMARK_EXECUTION_EVIDENCE')


if __name__ == '__main__':
    main()
